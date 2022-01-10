"""An AWS Python Pulumi program"""

import pulumi
import json
import pulumi_aws as aws

user1 = aws.iam.get_user(user_name="user-1")
user2 = aws.iam.get_user(user_name="user-2")
user3 = aws.iam.get_user(user_name="user-3")

s3_support_group = aws.iam.get_group(group_name="S3-Support")
ec2_support_group = aws.iam.get_group(group_name="EC2-Support")
ec2_admin_group = aws.iam.get_group(group_name="EC2-Admin")

s3support_membership = aws.iam.GroupMembership("s3-support",
    users=[user1.user_name],
    group=s3_support_group.group_name
)

ec2support_membership = aws.iam.GroupMembership("ec2-support",
    users=[user2.user_name],
    group=ec2_support_group.group_name
)

ec2admin_membership = aws.iam.GroupMembership("ec2-admin",
    users=[user3.user_name],
    group=ec2_admin_group.group_name
)