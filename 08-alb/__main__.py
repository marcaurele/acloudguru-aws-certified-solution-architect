"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

config = pulumi.Config()
security_group_id = config.get("securityGroupId")
sg = aws.ec2.get_security_group(id=security_group_id)
vpc_main = aws.ec2.get_vpc(cidr_block="10.0.0.0/16")
subnets = aws.ec2.get_subnets()

# EC2 instance
aws_linux = aws.ec2.get_ami(most_recent=True,
    filters=[
        aws.ec2.GetAmiFilterArgs(
            name="name",
            values=["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"],
        ),
        aws.ec2.GetAmiFilterArgs(
            name="virtualization-type",
            values=["hvm"],
        ),
    ],
    owners=["099720109477"])

web_server_userdata = """#!/bin/bash
sudo apt-get update -y
sudo apt-get install apache2 unzip -y
echo '<html><center><body bgcolor="black" text="#39ff14" style="font-family: Arial"><h1>Load Balancer Demo</h1><h3>Availability Zone: ' > /var/www/html/index.html
curl http://169.254.169.254/latest/meta-data/placement/availability-zone >> /var/www/html/index.html
echo '</h3> <h3>Instance Id: ' >> /var/www/html/index.html
curl http://169.254.169.254/latest/meta-data/instance-id >> /var/www/html/index.html
echo '</h3> <h3>Public IP: ' >> /var/www/html/index.html
curl http://169.254.169.254/latest/meta-data/public-ipv4 >> /var/www/html/index.html
echo '</h3> <h3>Local IP: ' >> /var/www/html/index.html
curl http://169.254.169.254/latest/meta-data/local-ipv4 >> /var/www/html/index.html
echo '</h3></html> ' >> /var/www/html/index.html
"""


webserver = aws.ec2.Instance("Web Server 02",
    instance_type="t3.micro",
    ami=aws_linux.id,
    subnet_id=subnets.ids[0],
    associate_public_ip_address=True,
    user_data=web_server_userdata,
    vpc_security_group_ids=[sg.id],
    tags={"Name": "webserver-02"}
)

webserver01 = aws.ec2.get_instance(filters=[
    aws.ec2.GetInstanceFilterArgs(
        name="tag:Name",
        values=["webserver-01"],
    )
])

web_alb = aws.lb.LoadBalancer("LegacyApplication",
    internal=False,
    load_balancer_type="application",
    name="LegacyApplication",
    security_groups=[sg.id],
    subnets=subnets.ids,
    enable_deletion_protection=False,
    tags={
        "Environment": "production",
    })

web_target_group = aws.lb.TargetGroup("WebServerTargetGroup",
    name="TargetGroup",
    port=80,
    protocol="HTTP",
    stickiness=aws.lb.TargetGroupStickinessArgs(
        type="lb_cookie",
        cookie_duration=30),
    vpc_id=vpc_main.id)

web_listener = aws.lb.Listener("WebServerListener",
    default_actions=[aws.lb.ListenerDefaultActionArgs(
        type="forward",
        target_group_arn=web_target_group.arn)],
    load_balancer_arn=web_alb.arn,
    port=80,
    protocol="HTTP"
    )

web_target_group_att_instance01 = aws.lb.TargetGroupAttachment("TargetGroupAttachmentInstance01",
    target_group_arn=web_target_group.arn,
    target_id=webserver01.id,
    port=80)
web_target_group_att_instance02 = aws.lb.TargetGroupAttachment("TargetGroupAttachmentInstance02",
    target_group_arn=web_target_group.arn,
    target_id=webserver.id,
    port=80)

# Export the name of the bucket
pulumi.export('webserver', webserver)
pulumi.export('alb', web_alb)
