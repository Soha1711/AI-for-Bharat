import json
import os

def lambda_handler(event, context):
    # 1. Handle WhatsApp Webhook Verification (GET Request)
    if event.get('httpMethod') == 'GET':
        params = event.get('queryStringParameters', {})
        verify_token = os.environ.get('VERIFY_TOKEN') # We will set this in AWS later
        
        if params.get('hub.mode') == 'subscribe' and params.get('hub.verify_token') == verify_token:
            return {
                'statusCode': 200,
                'body': params.get('hub.challenge')
            }
        return {'statusCode': 403, 'body': 'Verification failed'}

    # 2. Placeholder for Processing Messages (POST Request)
    return {
        'statusCode': 200,
        'body': json.dumps({'status': 'ready_for_messages'})
    }
