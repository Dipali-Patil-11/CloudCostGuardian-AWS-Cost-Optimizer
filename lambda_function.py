import boto3
import os
import json
from datetime import datetime, timedelta

# AWS Clients
ec2 = boto3.client("ec2")
cloudwatch = boto3.client("cloudwatch")
dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")

TABLE_NAME = os.environ["TABLE_NAME"]
CURRENT_TABLE = os.environ["CURRENT_TABLE"]
SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]

history_table = dynamodb.Table(TABLE_NAME)
current_table = dynamodb.Table(CURRENT_TABLE)


def get_instance_name(tags):
    if not tags:
        return "No Name"
    for tag in tags:
        if tag["Key"] == "Name":
            return tag["Value"]
    return "No Name"


def get_cpu(instance_id):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=10)

    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName="CPUUtilization",
        Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=["Average"]
    )

    datapoints = response.get("Datapoints", [])

    if not datapoints:
        return 0.0

    datapoints.sort(key=lambda x: x["Timestamp"])
    return round(datapoints[-1]["Average"], 2)


def lambda_handler(event, context):
    results = []

    running_count = 0
    stopped_count = 0
    underutilized_count = 0

    reservations = ec2.describe_instances()["Reservations"]

    for reservation in reservations:
        for instance in reservation["Instances"]:

            instance_id = instance["InstanceId"]
            instance_name = get_instance_name(instance.get("Tags", []))
            state = instance["State"]["Name"]

            cpu = 0.0
            recommendation = "Instance Stopped"
            status = "Stopped"

            if state == "running":
                running_count += 1
                cpu = get_cpu(instance_id)

                if cpu < 10:
                    recommendation = "Stop Instance"
                    status = "Underutilized"
                    underutilized_count += 1

                    try:
                        sns.publish(
                            TopicArn=SNS_TOPIC_ARN,
                            Subject="AWS Cost Optimizer Alert",
                            Message=f"""EC2 Instance: {instance_name}
Instance ID: {instance_id}
CPU Utilization: {cpu} %

Recommendation:
Stop or resize this EC2 instance to reduce AWS cost."""
                        )
                    except Exception as e:
                        print(f"SNS Error: {e}")

                else:
                    recommendation = "No Action Needed"
                    status = "Healthy"

            else:
                stopped_count += 1

            timestamp = datetime.utcnow().isoformat()

            item = {
                "InstanceId": instance_id,
                "Timestamp": timestamp,
                "InstanceName": instance_name,
                "State": state,
                "CPUUtilization": str(cpu),
                "Recommendation": recommendation,
                "Status": status,
                "Region": ec2.meta.region_name
            }

            # History table
            history_table.put_item(Item=item)

            # Current status table (one row per instance)
            current_table.put_item(Item=item)

            results.append({
                "InstanceId": instance_id,
                "InstanceName": instance_name,
                "State": state,
                "CPUUtilization": cpu,
                "Recommendation": recommendation,
                "Status": status,
                "Region": ec2.meta.region_name,
                "Timestamp": timestamp
            })

    # Publish custom CloudWatch metrics
    cloudwatch.put_metric_data(
        Namespace="CloudCostGuardian",
        MetricData=[
            {
                "MetricName": "RunningInstances",
                "Value": running_count,
                "Unit": "Count"
            },
            {
                "MetricName": "StoppedInstances",
                "Value": stopped_count,
                "Unit": "Count"
            },
            {
                "MetricName": "UnderutilizedInstances",
                "Value": underutilized_count,
                "Unit": "Count"
            }
        ]
    )

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS"
        },
        "body": json.dumps(results)
    }
