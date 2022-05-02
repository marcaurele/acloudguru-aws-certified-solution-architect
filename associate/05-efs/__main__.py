"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

vpc = aws.ec2.get_vpc(cidr_block="10.0.0.0/16", default=False)
subnet = aws.ec2.get_subnet(id="subnet-0d12bfd0f0a24b8d5")
sg = aws.ec2.get_security_group(id="sg-0f7f4e8f7eb6a6f72")

efs_volume = aws.efs.FileSystem("shareweb",
    tags={
        "Name": "SharedWeb",
    },
    availability_zone_name="us-east-1a",
    encrypted=True
)


mount_target = aws.efs.MountTarget("efsMountServer",
    file_system_id=efs_volume.id,
    security_groups=[sg.id],
    subnet_id=subnet.id
)

extra_rule = aws.ec2.SecurityGroupRule("extraRule",
    type="ingress",
    from_port=2049,
    to_port=2049,
    protocol="tcp",
    security_group_id=sg.id,
    cidr_blocks=["0.0.0.0/0"],
    description="Allow NFS access")

pulumi.export('efs', efs_volume)
pulumi.export("vpc.id", vpc.id)