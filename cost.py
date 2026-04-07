import boto3
from datetime import datetime
from config import START_DATE, REGION

ce = boto3.client('ce', region_name=REGION)

def get_total_cost():
    today = datetime.today().strftime('%Y-%m-%d')

    response = ce.get_cost_and_usage(
        TimePeriod={
            'Start': START_DATE,
            'End': today
        },
        Granularity='MONTHLY',
        Metrics=['UnblendedCost']
    )

    cost = float(response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])
    return cost


def get_service_usage_and_cost(service_name=None):
    today = datetime.today().strftime('%Y-%m-%d')

    groupby = [{'Type':'DIMENSION','Key':'SERVICE'}]
    response = ce.get_cost_and_usage(
        TimePeriod={
            'Start': START_DATE,
            'End': today
        },
        Granularity='MONTHLY',
        Metrics=['UnblendedCost', 'UsageQuantity'],
        GroupBy=groupby
    )

    report = []
    for group in response['ResultsByTime'][0].get('Groups', []):
        name = group['Keys'][0]
        if service_name and service_name.lower() not in name.lower(): continue
        cost_amount = float(group['Metrics']['UnblendedCost']['Amount'])
        usage_quantity = float(group['Metrics']['UsageQuantity']['Amount']) if 'Amount' in group['Metrics']['UsageQuantity'] else 0.0

        report.append({
            'name': name,
            'location': REGION,
            'usage': usage_quantity,
            'bill': cost_amount
        })

    return report