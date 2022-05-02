"""An AWS Python Pulumi program"""

import json
import pulumi
import pulumi_aws as aws

config = pulumi.Config()
bucket_name = config.get("bucketName")

vpc_main = aws.ec2.get_vpc(cidr_block="10.0.0.0/16")
subnets = aws.ec2.get_subnets()
web_sg = aws.ec2.get_security_group(
    vpc_id=vpc_main.id,
    filters=[
        aws.ec2.GetSecurityGroupFilterArgs(
            name="tag:aws:cloudformation:logical-id",
            values=["SecurityGroupWeb"]
        )
    ])


instance01 = aws.ec2.get_instance(filters=[
    aws.ec2.GetInstanceFilterArgs(
        name="tag:aws:cloudformation:logical-id",
        values=["EC2InstanceMod1SvrA"],
    )
])

base_template = aws.ec2.AmiFromInstance(
    "AMITemplateSrvA",
    name="Base",
    source_instance_id=instance01.id
)


webserver = aws.ec2.Instance("Test Web Server",
    instance_type="t3.micro",
    ami=base_template.id,
    subnet_id=subnets.ids[0],
    associate_public_ip_address=True,
    vpc_security_group_ids=[web_sg.id],
    tags={"Name": "Test Web Server"}
)

tagged_instances01 = aws.ec2.get_instances(filters=[
    aws.ec2.GetInstancesFilterArgs(
        name="tag:Name",
        values=["*Mod. 1 *"],
    )
])
tagged_buckets01 = aws.s3.get_bucket(bucket=bucket_name)

ressource_startship = aws.resourcegroups.Group(
    "Starship-Monitor",
    name="Starship-Monitor",
    resource_query=aws.resourcegroups.GroupResourceQueryArgs(
        query=json.dumps(
            {
                "ResourceTypeFilters": [
                    "AWS::EC2::Instance",
                    "AWS::S3::Bucket",
                ],
                "TagFilters": [
                    {
                        "Key": "Module",
                        "Values": ["Starship Monitor"]
                    }
                ]
            }
        )
    )
)

ressource_warpdrive = aws.resourcegroups.Group(
    "Warp-Drive",
    name="Warp-Drive",
    resource_query=aws.resourcegroups.GroupResourceQueryArgs(
        query=json.dumps(
            {
                "ResourceTypeFilters": [
                    "AWS::EC2::Instance",
                    "AWS::S3::Bucket",
                ],
                "TagFilters": [
                    {
                        "Key": "Module",
                        "Values": ["Warp Drive"]
                    }
                ]
            }
        )
    )
)

myrule = aws.cfg.Rule(
    "myrule",
    name="myrule",
    source=aws.cfg.RuleSourceArgs(
        owner="AWS",
        source_identifier="APPROVED_AMIS_BY_ID",
    ),
    input_parameters=json.dumps({"amiIds": "ami-0f85ffd702a02721b"}),
    scope=aws.cfg.RuleScopeArgs(
        tag_key="Module",
        tag_value="Starship Monitor"
    ))


# role = aws.iam.Role("role", assume_role_policy="""{
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Action": "sts:AssumeRole",
#       "Principal": {
#         "Service": "config.amazonaws.com"
#       },
#       "Effect": "Allow",
#       "Sid": ""
#     }
#   ]
# }
# """)
# foo = aws.cfg.Recorder("foo", role_arn=role.arn)
# rule = aws.cfg.Rule(
#     "rule",
#     name="rule",
#     source=aws.cfg.RuleSourceArgs(
#         owner="AWS",
#         source_identifier="APPROVED_AMIS_BY_ID",
#     ),
#     opts=pulumi.ResourceOptions(depends_on=[foo]))

# role_policy = aws.iam.RolePolicy(
#     "rolePolicy",
#     role=role.id,
#     policy="""{
#   "Version": "2012-10-17",
#   "Statement": [
#   	{
#   		"Action": "config:Put*",
#   		"Effect": "Allow",
#   		"Resource": "*"

#   	}
#   ]
# }
# """)


pulumi.export("instance01", instance01)
pulumi.export("base_template", base_template)
pulumi.export("tagged_instances01", tagged_instances01.ids)
pulumi.export("tagged_buckets01", tagged_buckets01)
pulumi.export("ressource_startship", ressource_startship)
pulumi.export("ressource_warpdrive", ressource_warpdrive)

