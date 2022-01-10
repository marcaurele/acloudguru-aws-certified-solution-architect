"""An AWS Python Pulumi program"""

import pulumi
import json
import pulumi_aws as aws

config = pulumi.Config()

bucket_config = config.require_object("bucket")
aws_account = config.get("awsaccount")

s3_appconfig_buckets = []
for bucket in bucket_config.get("appconfigs"):
    s3_appconfig_buckets.append(aws.s3.get_bucket(bucket))

dev1_user = aws.iam.get_user(user_name="dev1")
dev3_user = aws.iam.get_user(user_name="dev3")

s3_appconfig_policy = aws.iam.Policy("S3RestrictedPolicy",
    name="S3RestrictedPolicy",
    path="/",
    description="S3 access role to appconfig buckets",
    policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": ["s3:*"],
                "Effect": "Allow",
                "Resource": [
                    b.arn for b in s3_appconfig_buckets
                ],
            },
            {
                "Action": "s3:ListAllMyBuckets",
                "Effect": "Allow",
                "Resource": "*",
            },
        ],
    }))

appconfig_role = aws.iam.Role("S3RestrictedRole",
    name="S3RestrictedRole",
    path="/",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": ["sts:AssumeRole"],
                "Effect": "Allow",
                "Principal": {
                    "AWS": f"arn:aws:iam::{aws_account}:root"
                },
                "Sid": "",
            },
        ],
    })
)

appconfigRolePolicyAttach = aws.iam.RolePolicyAttachment("appconfigAttach",
    role=appconfig_role.name,
    policy_arn=s3_appconfig_policy.arn
)

dev1_policy = aws.iam.UserPolicyAttachment("s3_app_config_attach_dev1",
  user="dev1",
  policy_arn=s3_appconfig_policy.arn)

s3_assumerole_policy = aws.iam.Policy("S3AssumeRolePolicy",
    name="S3AssumeRolePolicy",
    path="/",
    description="Assume role",
    policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": ["sts:AssumeRole"],
                "Effect": "Allow",
                "Resource": [
                    f"arn:aws:iam::{aws_account}:role/S3RestrictedRole",
                ],
            },
        ],
    }))

dev3_policy = aws.iam.UserPolicyAttachment("s3_app_config_attach_dev3",
  user="dev3",
  policy_arn=s3_assumerole_policy.arn)
