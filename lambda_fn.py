import boto3

lambda_client = boto3.client('lambda')

def list_functions():
    response = lambda_client.list_functions()

    print("\nLambda Functions:")
    for f in response['Functions']:
        print(f['FunctionName'])