# ============================================================
# CHURN PREDICTION — API CLIENT
# ============================================================
# This script acts as the CONSUMER of the Flask API defined in predict.py.
# It simulates a real-world system (e.g. a CRM or marketing platform)
# that needs to decide whether to send a promotional email to a customer.
#
# Flow:
#   Build customer dict → POST to API → parse response → business decision

import requests


# -------------------------------------------------------
# STEP 1 — Define the target endpoint
# -------------------------------------------------------
# The URL must match the host, port, and route defined in the Flask server.
# localhost = the server is running on the same machine as this script.
# In production this would be a real domain or internal service URL.

url = 'http://localhost:2909/predict'


# -------------------------------------------------------
# STEP 2 — Define the customer to evaluate
# -------------------------------------------------------
# customer_id is used only for logging/tracking — it is NOT sent to the model.
# The model only receives the features it was trained on.
#
# All feature names and values must match exactly what the model expects:
# same column names, same encoding (e.g. lowercase strings, no spaces).
# Mismatches here would result in wrong predictions or silent errors.

customer_id = 'xyz-123'

customer = {
    "gender": "female",
    "seniorcitizen": 0,            # binary: 0 = not a senior citizen
    "partner": "yes",
    "dependents": "no",
    "phoneservice": "no",
    "multiplelines": "no_phone_service",
    "internetservice": "dsl",
    "onlinesecurity": "no",
    "onlinebackup": "yes",
    "deviceprotection": "no",
    "techsupport": "no",
    "streamingtv": "no",
    "streamingmovies": "no",
    "contract": "month-to-month",  # shorter contracts correlate with higher churn risk
    "paperlessbilling": "yes",
    "paymentmethod": "electronic_check",
    "tenure": 5,                   # months as a customer — low tenure = higher churn risk
    "monthlycharges": 79.85,
    "totalcharges": 5 * 79.85      # derived from tenure × monthlycharges
}


# -------------------------------------------------------
# STEP 3 — Send the POST request and parse the response
# -------------------------------------------------------
# requests.post serializes the dict to JSON automatically when using json=.
# .json() on the response deserializes the returned JSON back into a Python dict.
#
# Expected response format:
# {"churn_probability": 0.73, "churn": true}

response = requests.post(url, json=customer).json()
print(response)


# -------------------------------------------------------
# STEP 4 — Apply the business rule
# -------------------------------------------------------
# The model's binary prediction drives a real business action.
# This is the final step in the ML pipeline: turning a probability
# into a decision with a tangible outcome (send or don't send email).
#
# In production this logic would typically be part of a larger
# workflow (e.g. a scheduler, event-driven trigger, or CRM integration).

if response['churn'] == True:
    print('send promo: %s' % customer_id)
else:
    print('not send promo: %s' % customer_id)