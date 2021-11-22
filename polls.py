import hug
import boto3
import datetime

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

@hug.get("/create_table/")
def create_polls_table():

    table = dynamodb.create_table(
        TableName='Polls',
        KeySchema=[
            {
                'AttributeName': 'Username',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'PollTitle',
                'KeyType': 'Range'
            }
            
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Username',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'PollTitle',
                'AttributeType': 'S'
            },
            
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
        
    )
    return "Table is created"

# @hug
# # def createPoll(pollTitle, username, option1, option2, option3, option4):
# #     retrived the last POSTID ++
# #     use that POSTID to create the table
    
@hug.get("/createPoll/")
def add_items_to_table(
    username:hug.types.text,
    option1:hug.types.text, 
    option2:hug.types.text, 
    option3:hug.types.text, 
    option4:hug.types.text, 
    pollTitle:hug.types.text,
    ):
    #Poll_ID = username + str(datetime.datetime.now())

    
    table = dynamodb.Table('Polls')
    added_item = table.put_item(
        Item={
            'Username': username,
            'PollTitle': pollTitle,
            option1: ['A'],
            option2: ['B'],
            option3: ['C'],
            option4: ['D'],
            'Options': [option1, option2, option3, option4]
            # 'Option2': {
            #     "VoteList": [],
            # },
            # 'Option3': {
            #     "Choice": option3,
            #     "VoteList": [],
            # },
            # 'Option4': {
            #     "Choice": option4,
            #     "VoteList": [],
            # },
        }
    )
    return added_item

@hug.get("/deletepoll/")
def delete_item(username:hug.types.text,pollTitle:hug.types.text):
    table = dynamodb.Table('Polls')
    
    response = table.delete_item(
        Key={
            'Username': username,
            'PollTitle': pollTitle
        }
    )
    return response



@hug.get("/getAllPost/") 
def get_items_from_table():
    table = dynamodb.Table('Polls')
    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    return data

@hug.get("/vote/")
def vote(
    option:hug.types.text,
    uservoting:hug.types.text, 
    username:hug.types.text, 
    pollTitle:hug.types.text
    ):
    table = dynamodb.Table('Polls')
    response = table.get_item(
        Key={
            'Username': username,
            'PollTitle': pollTitle,
        }
    )
    options = response['Item']['Options']
    option1 = options[0]
    option2 = options[1]
    option3 = options[2]
    option4 = options[3]

    Voters = response['Item'][option1] + response['Item'][option2] + response['Item'][option3] + response['Item'][option4]


    if not uservoting in Voters:
        newlist = response['Item'][option] + [uservoting]
        updated_item = table.update_item(
        Key={
            'Username': username,
            'PollTitle': pollTitle
        },
        UpdateExpression="SET " + option + "= :val",
        ExpressionAttributeValues={
        ':val': newlist,
        },
        ReturnValues="UPDATED_NEW")
       
    else:
        return "You already voted in this poll"

    return updated_item

@hug.get("/getPoll/")
def getPoll(username=hug.types.text, pollTitle=hug.types.text):
    table = dynamodb.Table('Polls')
    response = table.get_item(
        Key={
            'Username': username,
            'PollTitle': pollTitle,
        }
    )

    return response['Item']