import boto3
import os
import json
from datetime import datetime, timedelta
from decimal import Decimal

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

MAX_EMAILS_PER_DAY = 3


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


def can_send_email(counter_key):

    today = datetime.utcnow().strftime("%Y-%m-%d")

    counter_id = f"EMAIL_COUNTER#{counter_key}"

    response = current_table.get_item(
        Key={
            "InstanceId": counter_id
        }
    )

    if "Item" not in response:

        current_table.put_item(
            Item={
                "InstanceId": counter_id,
                "Date": today,
                "EmailCount": 1
            }
        )

        return True

    item = response["Item"]

    count = int(item.get("EmailCount", 0))

    if item.get("Date") != today:

        current_table.put_item(
            Item={
                "InstanceId": counter_id,
                "Date": today,
                "EmailCount": 1
            }
        )

        return True

    if count >= MAX_EMAILS_PER_DAY:

        return False

    current_table.update_item(
        Key={
            "InstanceId": counter_id
        },
        UpdateExpression="SET EmailCount = :c",
        ExpressionAttributeValues={
            ":c": Decimal(count + 1)
        }
    )

    return True


def lambda_handler(event, context):
    results = []

    running_count = 0
    stopped_count = 0
    underutilized_count = 0
    underutilized_instances = []

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

                if 0 < cpu < 10:
                    recommendation = "Stop Instance"
                    status = "Underutilized"
                    underutilized_count += 1

                    underutilized_instances.append({
                        "Name": instance_name,
                        "CPU": cpu,
                        "InstanceId": instance_id
                    })

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

    if underutilized_instances:
        message = f"""
AWS Cost Optimizer Report

Running Instances : {running_count}
Stopped Instances : {stopped_count}
Underutilized : {underutilized_count}

--------------------------------
"""

        for i, instance in enumerate(underutilized_instances, start=1):
            message += f"""
{i}. {instance['Name']}
   Instance ID : {instance['InstanceId']}
   CPU : {instance['CPU']}%
"""

        message += """

Recommendation

Stop or resize these EC2 instances to reduce AWS costs.
"""

        if can_send_email("SUMMARY"):

            try:
                sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Subject="AWS Cost Optimizer Summary",
                    Message=message
                )
            except Exception as e:
                print(f"SNS Error: {e}")

    # Publish custom CloudWatch metric
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
