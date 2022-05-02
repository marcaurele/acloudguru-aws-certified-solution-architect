"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

remote_lambda_archive = pulumi.RemoteArchive("https://github.com/ACloudGuru-Resources/course-aws-certified-solutions-architect-associate/raw/main/lab/9/mysql.zip")
sg = aws.ec2.get_security_group(tags={"Name": "DatabaseSG"})
all_subnets = aws.ec2.get_subnets(
    filters=[aws.ec2.GetSubnetFilterArgs(
        name="tag:aws:cloudformation:logical-id",
        values=["Private*"]
    )],
)

pulumi.export("subnets", all_subnets)
pulumi.export("sg", sg)
