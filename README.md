# AWS Monitoring CLI

A Python-based command-line monitoring tool for AWS services including EC2, S3, Lambda, and cost tracking with SNS alert notifications.

## Features

- **EC2 Monitoring**: Detect idle instances based on CPU utilization thresholds
- **S3 Monitoring**: List and monitor S3 buckets
- **Lambda Monitoring**: Track Lambda functions
- **Cost Analysis**: Monitor AWS billing with cost threshold alerts
- **Service Report**: View service-wise usage and costs across the billing period
- **SNS Alerts**: Send email alerts for idle instances and cost overruns
- **CloudWatch Integration**: Real-time CPU metrics for EC2 instances

## Prerequisites

- Python 3.8+
- AWS Account with appropriate IAM permissions
- AWS CLI configured with credentials

## Installation

### 1. Clone or download the project

```bash
cd cloudexm
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install boto3
```

### 4. Configure AWS credentials

```bash
aws configure
```

Enter your:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., us-east-1)
- Output format (json)

## Configuration

Edit `config.py` and set:

```python
TOPIC_ARN = "arn:aws:sns:region:account-id:topic-name"  # Your SNS topic ARN
REGION = "us-east-1"                                     # Your AWS region
COST_THRESHOLD = 10.0                                    # Alert if cost > $10/month
CPU_THRESHOLD = 5.0                                      # Alert if CPU < 5%
START_DATE = "2025-03-01"                               # Cost tracking start date
```

## AWS Setup

### 1. Create SNS Topic

```bash
aws sns create-topic --name cost-alert-topic --region us-east-1
```

Copy the `TopicArn` and set it in `config.py`.

### 2. Subscribe to Topic

```bash
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:ACCOUNT-ID:cost-alert-topic \
  --protocol email \
  --notification-endpoint your-email@example.com
```

Confirm the subscription via email.

### 3. IAM Permissions Required

Attached policy example:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sns:Publish",
        "ec2:DescribeInstances",
        "s3:ListBuckets",
        "lambda:ListFunctions",
        "cloudwatch:GetMetricStatistics",
        "ce:GetCostAndUsage"
      ],
      "Resource": "*"
    }
  ]
}
```

## Usage

### Run the CLI

```bash
python main.py
```

### Menu Options

```
===== AWS MONITOR CLI =====
1. EC2 Monitor        - Check idle EC2 instances
2. S3 Monitor         - List S3 buckets
3. Lambda Monitor     - List Lambda functions
4. Cost Check         - View total billing cost
5. Service Report     - View service-wise usage & cost
6. Exit               - Exit the application
```

### Example: Check EC2 Instances

```
Enter choice: 1
ID: i-0cea8cd94c7b62cad, State: running, Type: t2.micro
Checking Idle Instances...
⚠️ EC2 i-0cea8cd94c7b62cad has no CPU data (treating as idle)
```

### Example: Service Report

```
Enter choice: 5
Service name | location | usage | bill
Amazon EC2 | us-east-1 | 100.5 | $45.32
Amazon S3 | us-east-1 | 2048.0 | $12.50
```

## File Structure

```
cloudexm/
├── main.py              # CLI entry point & menu
├── ec2.py               # EC2 monitoring functions
├── s3.py                # S3 bucket listing
├── lambda_fn.py         # Lambda function tracking
├── cloudwatch.py        # CloudWatch metrics (CPU)
├── cost.py              # Cost Explorer & service usage
├── sns_alert.py         # SNS email notifications
├── config.py            # Configuration (KEEP PRIVATE)
├── .gitignore           # Git ignore rules
├── README.md            # This file
└── venv/                # Virtual environment (ignored)
```

## Troubleshooting

### `InvalidParameterException: TopicArn`

- Verify `TOPIC_ARN` in `config.py` starts with `arn:aws:sns:`
- Confirm the topic exists in SNS console
- Check region matches in `TOPIC_ARN` and `aws configure`

### `boto3 ImportError`

```bash
source venv/bin/activate
pip install boto3
```

### No CPU data for instances

- EC2 instances need ~5-10 minutes to have CloudWatch metrics
- Ensure CloudWatch agent is running on instances (optional for basic metrics)
- Use larger time window in `cloudwatch.py` if needed

### Cost Explorer returns no data

- Ensure `START_DATE` in `config.py` is before today
- Wait 24 hours after instance creation for cost data to appear
- Verify Cost Explorer API access in IAM permissions

### Email alerts not arriving

1. Confirm subscription in SNS console (check "Confirmed" status)
2. Check spam/junk folder
3. Verify `TOPIC_ARN` value is correct
4. Test with small script:
   ```python
   from sns_alert import send_alert
   send_alert("Test alert")
   ```

## Security Notes

- **Never commit `config.py`** (contains ARNs and account ID)
- **Never commit AWS credentials** (use `.env` or `aws configure`)
- Use IAM roles/policies with least privilege
- Rotate AWS credentials regularly
- Store sensitive data in AWS Secrets Manager for production

## Development

### Add a new monitoring service

1. Create new module (e.g., `rds.py`)
2. Import in `main.py`
3. Add menu option in `main()` function
4. Handle exceptions with try-catch blocks

### Example: Add RDS monitoring

```python
# rds.py
import boto3

rds = boto3.client('rds', region_name=REGION)

def get_databases():
    response = rds.describe_db_instances()
    for db in response['DBInstances']:
        print(f"DB: {db['DBInstanceIdentifier']}, Status: {db['DBInstanceStatus']}")
```

## License

MIT License - Feel free to modify and extend

## Support

For issues or feature requests, contact your AWS administrator or check AWS documentation:

- [EC2 Documentation](https://docs.aws.amazon.com/ec2)
- [Cost Explorer API](https://docs.aws.amazon.com/awsaccountbilling/latest/userguide/ce-api.html)
- [SNS Documentation](https://docs.aws.amazon.com/sns)

---

**Last Updated**: April 2026  
**Version**: 1.0
