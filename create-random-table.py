import boto3
import random

# Create a DynamoDB client
client = boto3.client('dynamodb')

# Set the name of the table
table_name = 'my-table'

# Set the attributes of the table
attributes = [
    {
        'AttributeName': 'id',
        'AttributeType': 'N'
    },
    {
        'AttributeName': 'name',
        'AttributeType': 'S'
    }
]

# Set the primary key of the table
key_schema = [
    {
        'AttributeName': 'id',
        'KeyType': 'HASH'
    },
    {
        'AttributeName': 'name',
        'KeyType': 'RANGE'
    }
]

# Set the capacity units of the table
provisioned_throughput = {
    'ReadCapacityUnits': 1,
    'WriteCapacityUnits': 1
}

# Create the table
client.create_table(
    TableName=table_name,
    AttributeDefinitions=attributes,
    KeySchema=key_schema,
    ProvisionedThroughput=provisioned_throughput
)

# Wait until the table is created
client.get_waiter('table_exists').wait(TableName=table_name)

# Generate some random data
data = []
for i in range(10):
    data.append({
        'id': {'N': str(i)},
        'name': {'S': 'Item ' + str(i)}
    })

# Add the data to the table
client.batch_write_item(
    RequestItems={
        table_name: [
            {
                'PutRequest': {
                    'Item': item
                }
            } for item in data
        ]
    }
)
