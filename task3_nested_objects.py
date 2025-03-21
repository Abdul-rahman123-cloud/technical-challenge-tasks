import json

def lambda_handler(event, context):
    try:
        # Extract the nested object and key path from the event
        nested_object = event.get('object', {})
        key_path = event.get('key', '')
        
        # Get the value using the key path
        result = get_nested_value(nested_object, key_path)
        
        # Return the result
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'object': nested_object,
                'key': key_path,
                'value': result
            })
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': str(e)
            })
        }

def get_nested_value(obj, path):
    """
    Extract a value from a nested object using a path string.
    
    Args:
        obj (dict): The nested object
        path (str): Path to the value, using '/' as separator
    
    Returns:
        The value at the specified path, or None if not found
    
    Raises:
        ValueError: If path is invalid or value is not found
    """
    # Split the path into individual keys
    keys = path.split('/')
    
    # Start with the root object
    current = obj
    
    # Traverse the object using the keys
    for key in keys:
        if key not in current:
            raise ValueError(f"Key '{key}' not found in path '{path}'")
        current = current[key]
    
    return current