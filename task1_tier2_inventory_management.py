import json
import random
import string
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = "inventory-db"  # DynamoDB table

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            # Return as int if there's no fractional part, otherwise as float
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def build_response(status_code, body):
    """
    Utility function to build a standard HTTP response.
    """
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, cls=DecimalEncoder)
    }

def lambda_handler(event, context):
    """
    This Lambda function handles two actions:
      1) Add a new item with a randomly generated product_id.
      2) Update the quantity of an existing item.

    Expected JSON input format for adding an item:
    {
      "action": "add_item",
      "product_name": "Apple",
      "quantity": 50
    }

    Expected JSON input format for updating an item:
    {
      "action": "update_item",
      "product_id": "ab123",
      "quantity": 75
    }
    """
    try:
        # Parse input JSON (either directly or from the "body" key)
        body = json.loads(event["body"]) if "body" in event else event

        action = body.get("action")
        table = dynamodb.Table(TABLE_NAME)

        if action == "add_item":
            product_name = body.get("product_name")
            quantity = body.get("quantity")

            # Validate input
            if not product_name or quantity is None:
                return build_response(400, {
                    "message": "Invalid input. Must include product_name and quantity."
                })

            # Generate product_id: two random letters + a random number between 100 and 100000
            random_letters = ''.join(random.choices(string.ascii_letters, k=2))
            random_number = random.randint(100, 100000)
            product_id = f"{random_letters}{random_number}"

            # Put item into DynamoDB
            item = {
                "product_id": product_id,
                "product_name": str(product_name),
                "quantity": int(quantity)
            }
            table.put_item(Item=item)

            return build_response(200, {
                "message": "Item added successfully",
                "item": item
            })

        elif action == "update_item":
            product_id = body.get("product_id")
            new_quantity = body.get("quantity")

            # Validate input
            if not product_id or new_quantity is None:
                return build_response(400, {
                    "message": "Invalid input. Must include product_id and quantity."
                })

            # Update item in DynamoDB
            response = table.update_item(
                Key={"product_id": product_id},
                UpdateExpression="set quantity = :q",
                ExpressionAttributeValues={":q": int(new_quantity)},
                ReturnValues="ALL_NEW"
            )

            updated_item = response.get("Attributes", {})
            return build_response(200, {
                "message": "Item updated successfully",
                "updated_item": updated_item
            })

        else:
            return build_response(400, {
                "message": "Invalid action. Must be either 'add_item' or 'update_item'."
            })

    except Exception as e:
        return build_response(500, {
            "message": f"Server error: {str(e)}"
        })
