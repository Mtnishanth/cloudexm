import boto3

s3 = boto3.client('s3')

def list_buckets():
    response = s3.list_buckets()

    print("\nS3 Buckets:")
    for b in response['Buckets']:
        print(b['Name'])