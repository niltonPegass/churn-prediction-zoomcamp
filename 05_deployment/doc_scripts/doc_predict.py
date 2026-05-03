# ============================================================
# CHURN PREDICTION — REST API SERVER
# ============================================================
# This script serves a trained ML model as a web API using Flask.
# Any external system (app, script, pipeline) can send a customer's
# data via HTTP and receive a churn prediction in return.
#
# Architecture overview:
#   [Client] --(POST /predict)--> [Flask API] --> [Model] --> [JSON response]

import pickle
from flask import Flask
from flask import request
from flask import jsonify


# -------------------------------------------------------
# STEP 1 — Load the trained model from disk
# -------------------------------------------------------
# The model was saved as a .bin file using pickle after training.
# It contains TWO objects packed together: the DictVectorizer (dv)
# and the LogisticRegression model — both are needed at inference time.
#
# 'rb' = read in binary mode (required for pickle files).
# The model is loaded ONCE at startup, not on every request,
# which keeps the API fast under repeated calls.

model_file = 'model/model_C=1.0.bin'

with open(model_file, 'rb') as f_in:
    dv, model = pickle.load(f_in)  # unpack both objects saved together


# -------------------------------------------------------
# STEP 2 — Initialize the Flask application
# -------------------------------------------------------
# Flask is a lightweight web framework for Python.
# The string 'churn' is the application name — used internally by Flask
# for configuration and debugging context.

app = Flask('churn')


# -------------------------------------------------------
# STEP 3 — Define the prediction endpoint
# -------------------------------------------------------
# @app.route registers a URL path and the HTTP methods it accepts.
# POST is used (instead of GET) because we are SENDING data (customer info)
# to the server, not just retrieving a resource.

@app.route('/predict', methods=['POST'])
def predict():

    # Parse the incoming JSON body into a Python dict.
    # The client must send a Content-Type: application/json header.
    # Example payload: {"tenure": 5, "monthlycharges": 79.85, ...}
    customer = request.get_json()

    # Transform the customer dict into a feature matrix.
    # dv.transform (NOT fit_transform) uses the vocabulary learned during training —
    # this ensures the feature space matches exactly what the model was trained on.
    # The input is wrapped in a list [] because DictVectorizer expects an iterable of dicts.
    X = dv.transform([customer])

    # predict_proba returns [[P(churn=0), P(churn=1)]]
    # [0, 1] selects the first (and only) row, second column → P(churn=1)
    y_pred = model.predict_proba(X)[0, 1]

    # Apply a decision threshold of 0.5:
    # probability >= 0.5 → predict churn (True), otherwise → no churn (False)
    churn = y_pred >= 0.5

    # Build the response payload.
    # float() and bool() are explicit casts: numpy types are not JSON-serializable by default.
    result = {
        'churn_probability': float(y_pred),
        'churn': bool(churn)
    }

    # jsonify converts the Python dict to a proper JSON HTTP response
    # with the correct Content-Type: application/json header.
    return jsonify(result)


# -------------------------------------------------------
# STEP 4 — Start the development server
# -------------------------------------------------------
# This block only runs when the script is executed directly (not imported).
#
# debug=True   → auto-reloads on code changes; shows detailed error pages.
#               ⚠️ Never use debug=True in production.
# host='0.0.0.0' → listens on ALL network interfaces, not just localhost.
#                  Required when running inside Docker or a remote server.
# port=9696    → the port clients must connect to.

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=2909)