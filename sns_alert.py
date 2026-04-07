import boto3
from config import TOPIC_ARN

sns = boto3.client('sns', region_name='us-east-1')

def send_alert(message):
    try:
        print("DEBUG: TopicArn:", TOPIC_ARN)

        response = sns.publish(
            TopicArn=TOPIC_ARN,
            Message=message,
            Subject="AWS Alert"
        )

        print("✅ Alert sent:", response['MessageId'])

    except Exception as e:
        print("❌ SNS ERROR:", e)