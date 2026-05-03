import requests

#url = 'http://localhost:8080/predict'
#url_render = 'https://churn-prediction-zoomcamp.onrender.com/predict'
host_aws = 'churn-predict-env.eba-ykukcufr.sa-east-1.elasticbeanstalk.com'
host_aws = 'churn-predict-env.eba-ykukcufr.sa-east-1.elasticbeanstalk.com'
url_aws = f'http://{host_aws}/predict'
customer_id = 'xyz-123'

customer = {
    "gender": "female",
    "seniorcitizen": 0,
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
    "contract": "month-to-month",
    "paperlessbilling": "yes",
    "paymentmethod": "electronic_check",
    "tenure": 1,
    "monthlycharges": 89.85,
    "totalcharges": 1 * 89.85
}


response = requests.post(url_aws, json=customer).json()     # response for AWS
#response = requests.post(url, json=customer).json()        # response for local and Render
print(response)

if response['churn'] == True:
    print('send promo: %s' % customer_id)
else:
    print('not send promo: %s' % customer_id)