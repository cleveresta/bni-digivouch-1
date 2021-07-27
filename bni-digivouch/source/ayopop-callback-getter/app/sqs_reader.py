import boto3
import os
# Create SQS client

sqs = boto3.client('sqs')
queue_url = os.getenv('SQS_URL', 'https://sqs.ap-southeast-2.amazonaws.com/395824552236/q-ayopop-callback-dev')

while True:
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        WaitTimeSeconds=10
    )
    try:    
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        # Delete received message from queue
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        print('Received and deleted message: %s' % message)
    except KeyError:
        pass




#def get_from_queue():
#    # Receive message from SQS queue
#    while True:
#        
#        response = sqs.receive_message(
#            QueueUrl=queue_url,
#            AttributeNames=[
#                'SentTimestamp'
#            ],
#            MaxNumberOfMessages=1,
#            MessageAttributeNames=[
#                'All'
#            ],
#            VisibilityTimeout=0,
#            WaitTimeSeconds=10
#        )
#        try: 
#            yield from response['Messages']
#        except KeyError:
#            return 
#        
#        message = response['Messages'][0]
#        receipt_handle = message['ReceiptHandle']
#        # Delete received message from queue
#        sqs.delete_message(
#            QueueUrl=queue_url,
#            ReceiptHandle=receipt_handle
#        )
#        print('Received and deleted message: %s' % message)
#
#if __name__ == '__main__':
#    for message in get_from_queue(queue_url):
#        print(json.dumps(message))