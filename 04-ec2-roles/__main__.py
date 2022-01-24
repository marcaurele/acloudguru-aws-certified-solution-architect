"""An AWS Python Pulumi program"""

# Dev s3 bucket name = cfst-3035-57cbb5a63d74b7f8de7294585ff-s3bucketdev-10kdexq8fmtg2
# Prod s3 bucket name = cfst-3035-57cbb5a63d74b7f8de7294585f-s3bucketprod-olrdduhq8vv1
# Engineering s3 bucket name = cfst-3035-57cbb5a63d74b7f8de7-s3bucketengineering-780c0hmetvj
# Secret s3 bucket name = cfst-3035-57cbb5a63d74b7f8de729458-s3bucketsecret-1e44g0j3qks3u

import json

import pulumi
import pulumi_aws as aws

dev_role = aws.iam.Role("DEV_ROLE",
    name="DEV_ROLE",
    path="/",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": ["sts:AssumeRole"],
                "Effect": "Allow",
                "Principal": {
                    "Service": "ec2.amazonaws.com"
                },
                "Sid": "",
            },
        ],
    })
)

allow_readaccess_s3_policy = aws.iam.Policy("DevS3ReadAccess",
    name="DevS3ReadAccess",
    path="/",
    description="S3 access role to appconfig buckets",
    policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
            "Sid": "AllowUserToSeeBucketListInTheConsole",
            "Action": ["s3:ListAllMyBuckets", "s3:GetBucketLocation"],
            "Effect": "Allow",
            "Resource": ["arn:aws:s3:::*"]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:Get*",
                    "s3:List*"
                ],
                "Resource": [
                    "arn:aws:s3:::cfst-3035-57cbb5a63d74b7f8de7294585ff-s3bucketdev-10kdexq8fmtg2/*",
                    "arn:aws:s3:::cfst-3035-57cbb5a63d74b7f8de7294585ff-s3bucketdev-10kdexq8fmtg2"
                ]
            }
        ]
    })
)

s3readonlydev_s3_read_access = aws.iam.RolePolicyAttachment("dev_s3_read_access",
    role=dev_role.name,
    policy_arn=allow_readaccess_s3_policy.arn
)

profile = aws.iam.InstanceProfile("DEV_PROFILE", role=dev_role.name)

aws_linux = aws.ec2.get_ami(most_recent=True,
    filters=[
        aws.ec2.GetAmiFilterArgs(
            name="name",
            values=["Amazon Linux 2*"],
        ),
        aws.ec2.GetAmiFilterArgs(
            name="virtualization-type",
            values=["hvm"],
        ),
    ],
    owners=["892710030684"])

# i-05a8ab7ad97cc5f66
# https://github.com/pulumi/pulumi-aws/issues/1605
# webserver = aws.ec2.Instance("Web Server",
#     instance_type="t3.micro",
#     ami=aws_linux.id,
#     tags={"Name": "Web Server"},
#     iam_instance_profile=profile.name
# )

pulumi.export('DevS3ReadAccess.arn', allow_readaccess_s3_policy.arn)