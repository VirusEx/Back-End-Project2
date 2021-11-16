import hug
import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

@hug.get("/create_table/")
def create_polls_table():

    table = dynamodb.create_table(
        TableName='Polls',
        KeySchema=[
            {
                'AttributeName': 'Poll_ID',
                'KeyType': 'HASH'  
            },
            {
                'AttributeName': 'SK',
                'KeyType': 'Range'  
            }
            
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Poll_ID',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'SK',
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
    option1:hug.types.text, 
    option2:hug.types.text, 
    option3:hug.types.text, 
    option4:hug.types.text, 
    pollTitle:hug.types.text,
    ):

    
    table = dynamodb.Table('Polls')
    added_item = table.put_item(
        Item={
            'Poll_ID': 'U12345',
            'SK': 'C001',
            'Name': 'My first course',
            'Description': 'This is my first course.',
            'Author': 'Chris'
        }
    )
    return added_item