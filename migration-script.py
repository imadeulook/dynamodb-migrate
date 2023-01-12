import boto3

# Set up the DynamoDB client
client = boto3.client('dynamodb')

# Set the names of the source and target tables
source_table_name = 'my-table'
target_table_name = 'migrated-table'

# Get the details of the source table
source_table = client.describe_table(TableName=source_table_name)

# Get the attribute definitions and key schema of the source table
attribute_definitions = source_table['Table']['AttributeDefinitions']
key_schema = source_table['Table']['KeySchema']

# Set the read and write capacity units of the target table
provisioned_throughput = {
    'ReadCapacityUnits': 1,
    'WriteCapacityUnits': 1
}

# Create the target table with the same structure as the source table
client.create_table(
    TableName=target_table_name,
    AttributeDefinitions=attribute_definitions,
    KeySchema=key_schema,
    ProvisionedThroughput=provisioned_throughput
)

# Wait until the target table is created
client.get_waiter('table_exists').wait(TableName=target_table_name)

# Initialize the paginator for the scan operation
paginator = client.get_paginator('scan')

# Set the maximum number of items to retrieve per page
page_size = 50

# Use the paginator to retrieve all of the items from the source table
items = []
for page in paginator.paginate(TableName=source_table_name):
    items += page['Items']

# Write the items to the target table
client.batch_write_item(
    RequestItems={
        target_table_name: [
            {
                'PutRequest': {
                    'Item': item
                }
            } for item in items
        ]
    }
)
