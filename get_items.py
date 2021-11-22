import hug
import boto3
import datetime

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
table = dynamodb.Table('Polls')

resp = table.get_item(Key={'Username': 'danny', 'PollTitle': 'Testing1'})

print(resp['Item'])