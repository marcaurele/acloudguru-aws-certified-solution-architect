"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

vpc_db = aws.ec2.get_vpc(cidr_block="10.0.0.0/16")

# !! Need to change the RDS instance name
database = aws.rds.get_instance(db_instance_identifier="cdd8cbu2z4lq5p")

vpc_web = aws.ec2.Vpc(
    "web_vpc",
    cidr_block="192.168.0.0/16",
    tags={"Name": "Web_VPC"}
)

subnet_web_public = aws.ec2.Subnet(
    "subet_web_public",
    availability_zone="us-east-1a",
    cidr_block="192.168.0.0/24",
    tags={"Name": "WebPublic"},
    vpc_id=vpc_web.id
)

igw_web = aws.ec2.InternetGateway(
    "igw",
    vpc_id=vpc_web.id,
    tags={"Name": "WebIG"}
)

route_2_igw_for_web = aws.ec2.Route(
    "route2igw4web",
    destination_cidr_block="0.0.0.0/0",
    gateway_id=igw_web.id,
    route_table_id=vpc_web.main_route_table_id
)

vpc_peering_requester = aws.ec2.VpcPeeringConnection(
    "vpc-peering-requester",
    vpc_id=vpc_db.id,
    peer_vpc_id=vpc_web.id,
    auto_accept=False,
    tags={"Name": "DBtoWeb", "Side": "Requester"}
)
vpc_peering_accepter = aws.ec2.VpcPeeringConnectionAccepter(
    "vpc-peering-accepter",
    vpc_peering_connection_id=vpc_peering_requester.id,
    auto_accept=True,
    tags={"Name": "DBtoWeb", "Side": "Accepter"}
)

# Routes through VPC peering connection
peering_route_for_web = aws.ec2.Route(
    "peeringrouteweb",
    destination_cidr_block=vpc_db.cidr_block,
    vpc_peering_connection_id=vpc_peering_requester.id,
    route_table_id=vpc_web.main_route_table_id
)
peering_route_for_db = aws.ec2.Route(
    "peeringroutedb",
    destination_cidr_block=vpc_web.cidr_block,
    vpc_peering_connection_id=vpc_peering_requester.id,
    route_table_id=vpc_db.main_route_table_id
)

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
sudo apt update -y
sudo apt install php-curl php-gd php-mbstring php-xml php-xmlrpc php-soap php-intl php-zip perl mysql-server apache2 libapache2-mod-php php-mysql -y
wget https://github.com/ACloudGuru-Resources/course-aws-certified-solutions-architect-associate/raw/main/lab/5/wordpress.tar.gz
tar zxvf wordpress.tar.gz
cd wordpress
wget https://raw.githubusercontent.com/ACloudGuru-Resources/course-aws-certified-solutions-architect-associate/main/lab/5/000-default.conf
cp wp-config-sample.php wp-config.php
perl -pi -e "s/database_name_here/wordpress/g" wp-config.php
perl -pi -e "s/username_here/wordpress/g" wp-config.php
perl -pi -e "s/password_here/wordpress/g" wp-config.php
perl -i -pe'
  BEGIN {
    @chars = ("a" .. "z", "A" .. "Z", 0 .. 9);
    push @chars, split //, "!@#$%^&*()-_ []{}<>~\`+=,.;:/?|";
    sub salt { join "", map $chars[ rand @chars ], 1 .. 64 }
  }
  s/put your unique phrase here/salt()/ge
' wp-config.php
mkdir wp-content/uploads
chmod 775 wp-content/uploads
mv 000-default.conf /etc/apache2/sites-enabled/
mv /wordpress /var/www/
apache2ctl restart
"""

webserver_sg = aws.ec2.SecurityGroup(
    "allowHTTP",
    vpc_id=vpc_web.id,
    description="Allow HTTP",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            description="Allow HTTP",
            from_port=80,
            to_port=80,
            protocol="tcp",
            cidr_blocks=["0.0.0.0/0"]
        ),
        aws.ec2.SecurityGroupIngressArgs(
            description="Allow SSH",
            from_port=22,
            to_port=22,
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

webserver = aws.ec2.Instance("Web Server",
    instance_type="t3.micro",
    ami=aws_linux.id,
    subnet_id=subnet_web_public.id,
    associate_public_ip_address=True,
    user_data=web_server_userdata,
    vpc_security_group_ids=[webserver_sg.id],
    tags={"Name": "Web Server"}
)

db_sg = aws.ec2.SecurityGroupRule(
    "dbconnect",
    type="ingress",
    from_port=3306,
    to_port=3306,
    cidr_blocks=[vpc_web.cidr_block],
    protocol="tcp",
    description="connection to DB instance",
    security_group_id=database.vpc_security_groups[0]
)

pulumi.export("vpc.db", vpc_db)
pulumi.export("rds", database)
