import boto3
import requests
from requests_aws4auth import AWS4Auth

credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    "us-east-1",  # Replace with your region
    "es",
    session_token=credentials.token,
)

# Replace host URL with your ES domain's URL:
host = "https://vpc-aether-es-dynamodb-7gki7t76bffp76ds44eceheo4a.us-east-1.es.amazonaws.com"
url = host + "/lambda-index/lambda-type/"

headers = {"Content-Type": "application/json"}


def lambda_handler(event, context):
    count = 0
    for record in event["Records"]:
        # Get the primary key for use as the Elasticsearch ID
        id = (
            record["dynamodb"]["Keys"]["type"]["S"]
            + "_"
            + record["dynamodb"]["Keys"]["key"]["N"]
        )

        if record["eventName"] == "REMOVE":
            r = requests.delete(url + key, auth=awsauth)
        else:
            document = record["dynamodb"]["NewImage"]
            r = requests.put(url + key, auth=awsauth, json=document, headers=headers)
        print(r.text)
        count += 1
    return str(count) + " records processed."
