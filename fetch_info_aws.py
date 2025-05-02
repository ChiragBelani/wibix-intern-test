# Chirag Belani
# Script to get inventory info like EC2 and S3 from a CloudFormation stack
# Note: This does NOT use any access keys, only IAM role or instance profile

import boto3  # AWS SDK for Python
import argparse  # to get CLI arguments

# function to get resources created by the given stack
def get_stack_resources(stack_name):
    cf = boto3.client('cloudformation')  # making client for cloudformation
    try:
        response = cf.describe_stack_resources(StackName=stack_name)
        return response['StackResources']  # list of all resources
    except Exception as e:
        print(f"Some error while getting stack resources: {e}")
        return []

# function to get all EC2 instances
def list_ec2_instances():
    ec2 = boto3.client('ec2')
    print("\n========== EC2 INSTANCES ==========")
    try:
        reservations = ec2.describe_instances()['Reservations']
        for res in reservations:
            for instance in res['Instances']:
                print(f"Instance ID: {instance['InstanceId']}, State: {instance['State']['Name']}")
    except Exception as e:
        print("Couldn't fetch EC2 instances. Error:", e)

# function to get all S3 buckets
def list_s3_buckets():
    s3 = boto3.client('s3')
    print("\n========== S3 BUCKETS ==========")
    try:
        response = s3.list_buckets()
        for bucket in response['Buckets']:
            print(f"Bucket Name: {bucket['Name']}")
    except Exception as e:
        print("Couldn't fetch S3 buckets. Error:", e)

# main part of the script
def main():
    parser = argparse.ArgumentParser(description="This script fetches details from your CloudFormation stack")
    parser.add_argument("--stack-name", required=True, help="Pass your CloudFormation stack name or ARN here")
    args = parser.parse_args()

    print(f"\n>> Fetching resources for stack: {args.stack_name}")
    resources = get_stack_resources(args.stack_name)

    print("\n========== STACK RESOURCES ==========")
    for res in resources:
        print(f"{res['ResourceType']} | Logical ID: {res['LogicalResourceId']} | Physical ID: {res.get('PhysicalResourceId', 'N/A')}")

    # now checking inventory
    list_ec2_instances()
    list_s3_buckets()

# run the main() function
if __name__ == "__main__":
    main()

