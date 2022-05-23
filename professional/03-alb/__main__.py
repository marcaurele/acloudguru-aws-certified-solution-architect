"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

main_vpc = aws.ec2.get_vpc(cidr_block="10.0.0.0/16")

subnet_a = aws.ec2.get_subnet(
    availability_zone="us-east-1a",
    filters=[aws.ec2.GetSubnetFilterArgs(
        name="tag:Name",
        values=["Public"],
)])

igw = aws.ec2.get_internet_gateway(filters=[aws.ec2.GetInternetGatewayFilterArgs(
    name="attachment.vpc-id",
    values=[main_vpc.id],
)])

subnet_b = aws.ec2.Subnet(
    "subnet_b",
    availability_zone="us-east-1b",
    cidr_block="10.0.2.0/24",
    tags={"Name": "Public B"},
    vpc_id=main_vpc.id
)

routetable_b = aws.ec2.RouteTable(
    "routetable_b",
    vpc_id=main_vpc.id
)

route_2_igw_for_public_b = aws.ec2.Route(
    "route_2_igw_for_public_b",
    destination_cidr_block="0.0.0.0/0",
    gateway_id=igw.id,
    route_table_id=routetable_b.id
)

route_table_association = aws.ec2.RouteTableAssociation("routeTableAssociation",
    subnet_id=subnet_b.id,
    route_table_id=routetable_b.id
)

nacl_b = aws.ec2.NetworkAcl(
    "nacl_b",
    vpc_id=main_vpc.id,
    subnet_ids=[subnet_b.id],
    egress=[
        aws.ec2.NetworkAclIngressArgs(
            protocol="tcp",
            rule_no=100,
            action="allow",
            cidr_block="0.0.0.0/0",
            from_port=0,
            to_port=65535
        ),
    ],
    ingress=[
        aws.ec2.NetworkAclIngressArgs(
            protocol="tcp",
            rule_no=100,
            action="allow",
            cidr_block="0.0.0.0/0",
            from_port=80,
            to_port=80
        ),
        aws.ec2.NetworkAclIngressArgs(
            protocol="tcp",
            rule_no=101,
            action="allow",
            cidr_block="0.0.0.0/0",
            from_port=443,
            to_port=443
        ),
        aws.ec2.NetworkAclIngressArgs(
            protocol="tcp",
            rule_no=102,
            action="allow",
            cidr_block="0.0.0.0/0",
            from_port=22,
            to_port=22
        ),
        aws.ec2.NetworkAclIngressArgs(
            protocol="tcp",
            rule_no=103,
            action="allow",
            cidr_block="0.0.0.0/0",
            from_port=1024,
            to_port=65535
        ),
    ]
)

# EC2 instance
aws_linux = aws.ec2.get_ami(most_recent=True,
    filters=[
        aws.ec2.GetAmiFilterArgs(
            name="name",
            values=["amzn2-ami-kernel-5*"],
        ),
        aws.ec2.GetAmiFilterArgs(
            name="virtualization-type",
            values=["hvm"],
        ),
    ],
    owners=["amazon"])

web_server_userdata = """#cloud-config
ssh_authorized_keys:
  - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOqxR74+cr66BvCK7hHwXq/jDdUnJy4EWanNtD9SkZhB
package_update: true
packages:
  - httpd
runcmd:
  - systemctl enable httpd
  - systemctl start httpd
  - usermod -a -G apache ec2-user
  - chown -R ec2-user:apache /var/www
  - chmod 2775 /var/www
  - find /var/www -type d -exec chmod 2775 {} \;
  - find /var/www -type f -exec chmod 0664 {} \;
write_files:
- path: /var/www/html/index.html
  owner: ec2-user:apache
  content: |
"""

web_sg = aws.ec2.get_security_group(
    filters=[aws.ec2.GetSecurityGroupFilterArgs(
        name="tag:aws:cloudformation:logical-id",
        values=["EC2SecurityGroup"]
    )]
)

lb_sg = aws.ec2.SecurityGroup(
    "allowTraffic",
    vpc_id=main_vpc.id,
    description="Allow HTTP",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            description="Allow HTTP",
            from_port=80,
            to_port=80,
            protocol="tcp",
            cidr_blocks=["0.0.0.0/0"]
        ),
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            description="Allow egress flow",
            from_port=0,
            to_port=65535,
            protocol="tcp",
            cidr_blocks=["0.0.0.0/0"]
        ),
    ]
)



webserver_a = aws.ec2.Instance(f"Web Server A",
    instance_type="t3.micro",
    ami=aws_linux.id,
    subnet_id=subnet_a.id,
    associate_public_ip_address=True,
    user_data=web_server_userdata + """    Request Handled by: Web-A""",
    vpc_security_group_ids=[web_sg.id],
    tags={"Name": "Web-A"}
)

webserver_b = aws.ec2.Instance(f"Web Server B",
    instance_type="t3.micro",
    ami=aws_linux.id,
    subnet_id=subnet_b.id,
    associate_public_ip_address=True,
    user_data=web_server_userdata + """    Request Handled by: Web-B""",
    vpc_security_group_ids=[web_sg.id],
    tags={"Name": "Web-B"}
)


web_tg = aws.lb.TargetGroup(
    "web_tg",
    name="nlbTargets",
    health_check=aws.lb.TargetGroupHealthCheckArgs(
        path="/",
        protocol="HTTP"
    ),
    port=80,
    protocol="HTTP",
    vpc_id=main_vpc.id
)

lb = aws.lb.LoadBalancer(
    "loadbalancer",
    internal=False,
    load_balancer_type="application",
    subnets=[subnet_a.id, subnet_b.id,],
    security_groups=[lb_sg.id],
    tags={
        "Name": "NLB4LAB"
    }
)

lb_attachment_web_a = aws.lb.TargetGroupAttachment(
    f"web_alb_attachment_a",
    target_group_arn=web_tg.arn,
    target_id=webserver_a.id,
    port=80
)
lb_attachment_web_b = aws.lb.TargetGroupAttachment(
    f"web_alb_attachment_b",
    target_group_arn=web_tg.arn,
    target_id=webserver_b.id,
    port=80
)

front_listener = aws.lb.Listener(
    "front_alb_listener",
    load_balancer_arn=lb.arn,
    port=80,
    protocol="HTTP",
    default_actions=[
        aws.lb.ListenerDefaultActionArgs(
            type="forward",
            target_group_arn=web_tg.arn
        )
    ]
)