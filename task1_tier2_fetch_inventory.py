import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = "inventory-db"  # Name of your DynamoDB table

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            # Convert to int if there's no fractional part; otherwise, to float
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def build_response(status_code, body):
    """
    Utility function to build a standard HTTP response using a custom JSON encoder.
    """
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, cls=DecimalEncoder)
    }

def lambda_handler(event, context):
    """
    This Lambda function retrieves all records from the 'inventory-db' table.
    No input required other than possibly an empty JSON.
    """
    try:
        table = dynamodb.Table(TABLE_NAME)
        response = table.scan()  # Scans entire table (suitable for small datasets)

        items = response.get("Items", [])
        return build_response(200, {
            "message": "Items fetched successfully",
            "items": items
        })
    except Exception as e:
        return build_response(500, {
            "message": f"Server error: {str(e)}"
        })
