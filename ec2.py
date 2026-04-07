import boto3 
from config import REGION

ec2 = boto3.client('ec2', region_name=REGION)

def get_instances():
    response = ec2.describe_instances()
    instances = []

    for r in response['Reservations']:
        for i in r['Instances']:
            instance_id = i['InstanceId']
            state = i['State']['Name']
            inst_type = i['InstanceType']

            print(f"ID: {instance_id}, State: {state}, Type: {inst_type}")
            instances.append(instance_id)

    return instances