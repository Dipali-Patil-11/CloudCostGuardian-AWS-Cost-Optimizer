# 🚀 CloudCost Guardian - Deployment Guide

## Project Name

**CloudCost Guardian – AWS Multi-Instance Cost Optimization System**

---

# Deployment Architecture

```
EC2 Instances
      │
      ▼
CloudWatch Metrics
      │
      ▼
AWS Lambda
      │
 ┌────┼─────────────┐
 │    │             │
 ▼    ▼             ▼
DynamoDB        Amazon SNS
      │
      ▼
API Gateway
      │
      ▼
Ubuntu EC2 Dashboard
```

---

# Prerequisites

Before deploying the project, ensure the following AWS services are available.

- AWS Account
- IAM User
- EC2
- Lambda
- CloudWatch
- DynamoDB
- SNS
- API Gateway

---

# Step 1 : Launch Ubuntu EC2

Create an Ubuntu EC2 instance.

Example Configuration

- Ubuntu 22.04 LTS
- t2.micro
- Security Group
    - HTTP (80)
    - SSH (22)

Connect using SSH.

```bash
ssh -i your-key.pem ubuntu@YOUR_PUBLIC_IP
```

---

# Step 2 : Install Apache

```bash
sudo apt update

sudo apt install apache2 -y

sudo systemctl start apache2

sudo systemctl enable apache2
```

Verify

```
http://YOUR_PUBLIC_IP
```

---

# Step 3 : Deploy Dashboard

Copy

```
index.html
```

to

```
/var/www/html/
```

Restart Apache

```bash
sudo systemctl restart apache2
```

---

# Step 4 : Create DynamoDB Tables

Create

## Table 1

```
EC2MonitoringLogs
```

Partition Key

```
InstanceId
```

Sort Key

```
Timestamp
```

Purpose

Stores complete monitoring history.

---

## Table 2

```
EC2CurrentStatus
```

Partition Key

```
InstanceId
```

Purpose

Stores the latest monitoring status of every EC2 instance.

---

# Step 5 : Create SNS Topic

Create Topic

```
CostOptimizerAlerts
```

Create Email Subscription

Confirm the email subscription.

---

# Step 6 : Create Lambda Function

Runtime

```
Python 3.x
```

Upload

```
lambda_function.py
```

Environment Variables

```
TABLE_NAME = EC2MonitoringLogs

CURRENT_TABLE = EC2CurrentStatus

SNS_TOPIC_ARN = <SNS Topic ARN>
```

---

# Step 7 : Configure IAM Role

Attach the following permissions.

- AmazonEC2ReadOnlyAccess
- CloudWatchReadOnlyAccess
- AWSLambdaBasicExecutionRole
- AmazonDynamoDBFullAccess
- AmazonSNSFullAccess

Inline Permission

```
cloudwatch:PutMetricData
```

---

# Step 8 : Create REST API

Create

Amazon API Gateway

Create Resource

```
/status
```

Method

```
GET
```

Integrate with Lambda.

Deploy API.

Example

```
https://xxxxxxxx.execute-api.ap-south-1.amazonaws.com/prod/status
```

---

# Step 9 : Test Lambda

Create Test Event

```
{}
```

Expected Result

- Discover all EC2 instances
- Read CloudWatch CPU metrics
- Store data in DynamoDB
- Publish CloudWatch metrics
- Send SNS alerts
- Return JSON

---

# Step 10 : Verify Deployment

Verify Dashboard

```
http://YOUR_PUBLIC_IP
```

Verify

- Dashboard loads successfully
- API returns all EC2 instances
- Search works
- Auto refresh works
- Chart loads correctly

---

Verify DynamoDB

Table

```
EC2MonitoringLogs
```

Contains monitoring history.

Table

```
EC2CurrentStatus
```

Contains one record per EC2 instance.

---

Verify CloudWatch

Navigate to

```
CloudWatch

↓

Metrics

↓

CloudCostGuardian
```

Metrics

- RunningInstances
- StoppedInstances
- UnderutilizedInstances

---

Verify SNS

Receive email alert whenever a running EC2 instance has CPU utilization below 10%.

---

# Project Output

The system successfully

- Discovers all EC2 instances
- Reads CloudWatch CPU metrics
- Identifies underutilized resources
- Stores monitoring history
- Maintains latest instance status
- Sends email notifications
- Displays a live monitoring dashboard

---

# Technologies Used

- AWS EC2
- AWS Lambda
- Amazon CloudWatch
- Amazon DynamoDB
- Amazon SNS
- Amazon API Gateway
- Python
- HTML
- CSS
- JavaScript
- Apache Web Server

---

# Author

**Dipali Patil**

B.Tech Artificial Intelligence & Machine Learning

CloudCost Guardian - AWS Multi-Instance Cost Optimization System
