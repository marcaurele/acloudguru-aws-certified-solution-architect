"""Deploy an Amazon RDS Multi-AZ and Read Replica in AWS"""

import pulumi
import pulumi_aws as aws

initial_db_instance = aws.rds.Instance("inital",
    db_name="wordpress",
    identifier="wordpress",
    multi_az=False,
    instance_class="db.t3.micro",
    engine_version="8.0.28",
    engine="mysql",
    username="wpuser",
    port=3306,
    ca_cert_identifier="rds-ca-2019",
    deletion_protection=False,
    password="QhhT*l6_",
    allocated_storage=20,
    availability_zone="us-east-1a",
    db_subnet_group_name="cfst-3048-e99b5ac66f130600ccabb4787a32509f-dbsubnetgroup-13pu3nqadfzvp",
    vpc_security_group_ids=["sg-0b7143f1423953f30"],
    tags={"UserId": "13592608"}
)
pulumi.export("initial_db", initial_db_instance)


# rds_cluster = aws.rds.Cluster("acloudguru",
#     allocated_storage=100,
#     availability_zones=[
#         "us-east-1a",
#         "us-east-1b",
#         "us-east-1c",
#     ],
#     cluster_identifier="acloudguru",
#     db_cluster_instance_class="db.r6gd.large",
#     engine="mysql",
#     master_password="mustbeeightcharaters",
#     master_username="test")

# cluster_instances = []

# for range in [{"value" : i} for i in range(0, 2)]:
#     cluster_instances.append(
#         aws.rds.ClusterInstance(
#             f"clusterInstances-r{range['value']}",
#             identifier=f"cluster-acloudguru-db-{range['value']}",
#             cluster_identifier=rds_cluster.id,
#             instance_class="db.r6gd.large",
#             engine=rds_cluster.engine,
#             engine_version=rds_cluster.engine_version
#         )
    # )
