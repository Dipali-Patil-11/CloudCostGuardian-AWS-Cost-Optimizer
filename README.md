# ☁️ CloudCost Guardian - AWS Multi-Instance Cost Optimization System

![AWS](https://img.shields.io/badge/AWS-Cloud-orange)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Lambda](https://img.shields.io/badge/AWS-Lambda-yellow)
![DynamoDB](https://img.shields.io/badge/Amazon-DynamoDB-blue)
![CloudWatch](https://img.shields.io/badge/Amazon-CloudWatch-red)
![SNS](https://img.shields.io/badge/Amazon-SNS-green)

---

# 📌 Project Overview

CloudCost Guardian is a serverless AWS monitoring application that continuously monitors all EC2 instances in an AWS account.

The system automatically analyzes CloudWatch CPU utilization metrics, identifies underutilized EC2 instances, stores monitoring history in DynamoDB, publishes custom CloudWatch metrics, sends a consolidated Amazon SNS summary email containing all underutilized instances, and displays the monitoring information through a real-time web dashboard.

This project demonstrates the practical implementation of multiple AWS cloud services working together to optimize cloud infrastructure costs.

---

# 🎯 Project Objectives

- Monitor all EC2 instances in an AWS account
- Fetch real-time CPU utilization from Amazon CloudWatch
- Identify underutilized EC2 instances
- Send email alerts using Amazon SNS
- Store monitoring history in Amazon DynamoDB
- Maintain the latest EC2 status
- Display all monitoring information on a web dashboard
- Reduce unnecessary AWS infrastructure costs

---

# 🏗️ System Architecture

![Architecture](architecture/architecture.png)

---

# 🔄 Project Workflow

![Workflow](architecture/workflow-diagram.png)

---

# ☁️ AWS Services Used

- Amazon EC2
- AWS Lambda
- Amazon CloudWatch
- Amazon DynamoDB
- Amazon SNS
- Amazon API Gateway
- IAM
- Apache Web Server (Ubuntu EC2)

---

# ✨ Features

✅ Automatic EC2 Discovery

- Detects all EC2 instances automatically

---

✅ Real-Time CPU Monitoring

- Reads CPU utilization from Amazon CloudWatch

---

✅ Intelligent Cost Optimization

If CPU Utilization < 10%

→ Recommend stopping or resizing the EC2 instance.

---

✅ Email Summary Notifications

Amazon SNS sends a single summary email listing all underutilized EC2 instances detected during a monitoring cycle.

The summary includes:

• Total Running Instances
• Total Stopped Instances
• Underutilized Instance Count
• Instance Name
• Instance ID
• CPU Utilization
• Optimization Recommendation

---

✅ Monitoring History

Stores every monitoring cycle in DynamoDB.

Table:

```
EC2MonitoringLogs
```

---

✅ Current Instance Status

Maintains the latest status of every EC2 instance.

Table:

```
EC2CurrentStatus
```

---

✅ CloudWatch Custom Metrics

Publishes custom monitoring metrics:

- RunningInstances
- StoppedInstances
- UnderutilizedInstances

---

✅ REST API

Amazon API Gateway exposes Lambda through REST endpoints.

---

✅ Live Dashboard

Displays

- Total EC2 Instances
- Running Instances
- Stopped Instances
- Underutilized Instances
- CPU Utilization
- Recommendations
- Search & Filter
- Auto Refresh
- Consolidated SNS Email Summary

---

# 📂 Project Structure

```
CloudCostGuardian-AWS/
│
├── README.md
├── LICENSE
├── lambda_function.py
├── index.html
│
├── architecture/
│   ├── architecture.png
│   └── workflow-diagram.png
│
├── screenshots/
│   ├── dashboard.png
│   ├── dynamodb.png
│   ├── cloudwatch.png
│   └── sns-email.png
│
└── docs/
    └── deployment-guide.md
```

---

# 📷 Project Screenshots

## Dashboard

![Dashboard](screenshots/dashboard.png)

---

## DynamoDB Monitoring

![DynamoDB](screenshots/dynamodb.png)

---

## CloudWatch Custom Metrics

![CloudWatch](screenshots/cloudwatch.png)

---

## SNS Email Alerts

![SNS Email](screenshots/sns-email.png)

---

# 🚀 Project Flow

```
EC2 Instances
       │
       ▼
CloudWatch CPU Metrics
       │
       ▼
AWS Lambda
       │
 ┌─────┼────────────────────────────┐
 │     │                            │
 ▼     ▼                            ▼
DynamoDB                 Amazon SNS Summary
(History &               (Single Email Report)
Current Status)
       │
       ▼
CloudWatch Custom Metrics
       │
       ▼
API Gateway
       │
       ▼
CloudCost Guardian Dashboard
```

---

# ⚙️ Technologies Used

- Python
- HTML
- CSS
- JavaScript
- AWS SDK (Boto3)

---

# 📈 Future Enhancements

• Automatic EC2 Stop/Start
• AWS Cost Explorer Integration
• Multi-Region Monitoring
• CloudWatch Alarms
• Slack & Microsoft Teams Notifications
• Weekly Cost Optimization Reports
• User Authentication
• Historical Trend Analysis

---

# 👩💻 Author

**Dipali Patil**

B.Tech Artificial Intelligence & Machine Learning

AWS Cloud | Python | AI/ML | Web Development

---

# ⭐ If you found this project useful

Please consider giving this repository a ⭐ on GitHub.
