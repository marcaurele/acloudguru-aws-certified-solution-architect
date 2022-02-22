"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

config = pulumi.Config()
security_group_id = config.get("securityGroupId")
web_sg = aws.ec2.get_security_group(id=security_group_id)

vpc_db = aws.ec2.get_vpc(cidr_block="10.0.0.0/16")
subnets = aws.ec2.get_subnets()
rds_subnet = aws.rds.SubnetGroup("app-database-subnetgroup",
    subnet_ids=subnets.ids)

default_db = aws.rds.Instance("default",
    allocated_storage=10,
    availability_zone="us-east-1a",
    db_subnet_group_name=rds_subnet.id,
    engine="mysql",
    engine_version="8.0",
    identifier="wordpress",
    instance_class="db.t2.micro",
    name="wordpress",
    password="wordpress",
    publicly_accessible=False,
    skip_final_snapshot=True,
    username="wordpress",
    vpc_security_group_ids=[
        web_sg.id
    ])

# Export the name of the bucket
pulumi.export('rds_instance', default_db)
