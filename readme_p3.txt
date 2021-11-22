dynamodb:
java -D"java.library.path=./DynamoDBLocal_lib" -jar DynamoDBLocal.jar

check all the tables:
aws dynamodb list-tables --endpoint-url http://localhost:8000/

Verify Redis is running:
redis-cli ping