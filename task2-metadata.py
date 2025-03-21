import json
import boto3
import os

# Initialize boto3 client
ec2_client = boto3.client('ec2')

INSTANCE_ID = os.environ.get('INSTANCE_ID', 'i-0c0b9f37451e2c740')  # Default to your instance ID

def lambda_handler(event, context):
    """
    Lambda function that queries EC2 instance metadata and returns it as JSON.
    Supports retrieving specific keys individually via pathParameters.
    """
    try:
        # Get the metadata for the instance
        metadata = get_instance_metadata(INSTANCE_ID)
        
        # Check if a specific key is requested
        if event.get('pathParameters') and event.get('pathParameters').get('key'):
            key = event['pathParameters']['key']
            if key in metadata:
                # Return just the requested metadata field
                response_body = {key: metadata[key]}
            else:
                return {
                    'statusCode': 404,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': f'Metadata key "{key}" not found'})
                }
        else:
            # Return all metadata
            response_body = metadata
        
        # Return the response
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(response_body, default=str)  # default=str handles datetime objects
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

def get_instance_metadata(instance_id):
    """
    Retrieves metadata for a specific EC2 instance.
    
    Args:
        instance_id (str): The ID of the EC2 instance
        
    Returns:
        dict: A dictionary containing the instance metadata
    """
    # Get instance details
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    
    # Check if the instance exists
    if not response['Reservations'] or not response['Reservations'][0]['Instances']:
        raise Exception(f"Instance {instance_id} not found")
    
    # Get the instance data
    instance = response['Reservations'][0]['Instances'][0]
    
    # Extract and organize the metadata
    metadata = {
        'instanceId': instance['InstanceId'],
        'instanceType': instance['InstanceType'],
        'launchTime': instance['LaunchTime'],
        'availabilityZone': instance['Placement']['AvailabilityZone'],
        'state': instance['State']['Name']
    }
    
    # Add optional fields if they exist
    if 'ImageId' in instance:
        metadata['amiId'] = instance['ImageId']
    
    if 'VpcId' in instance:
        metadata['vpcId'] = instance['VpcId']
    
    if 'SubnetId' in instance:
        metadata['subnetId'] = instance['SubnetId']
    
    if 'PrivateIpAddress' in instance:
        metadata['privateIpAddress'] = instance['PrivateIpAddress']
    
    if 'PublicIpAddress' in instance:
        metadata['publicIpAddress'] = instance['PublicIpAddress']
    
    # Extract security groups
    if 'SecurityGroups' in instance:
        metadata['securityGroups'] = [
            {
                'groupId': sg['GroupId'],
                'groupName': sg['GroupName']
            }
            for sg in instance['SecurityGroups']
        ]
    
    # Extract tags
    if 'Tags' in instance:
        metadata['tags'] = {
            tag['Key']: tag['Value']
            for tag in instance['Tags']
        }
    
    return metadata