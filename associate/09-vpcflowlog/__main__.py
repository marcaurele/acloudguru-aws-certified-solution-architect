"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

config = pulumi.Config()
flowBucket = config.get("flowBucket")
flowIAMDeliverRole = config.get("flowIAMDeliverRole")
vpc_main = aws.ec2.get_vpc(cidr_block="10.0.0.0/16")

webserver = aws.ec2.get_instance(filters=[
    aws.ec2.GetInstanceFilterArgs(
        name="tag:Name",
        values=["Web Server"],
    )
])

flow_log_s3 = aws.ec2.FlowLog("s3FlowLog",
    log_destination=flowBucket,
    log_destination_type="s3",
    max_aggregation_interval=60,
    traffic_type="ALL",
    vpc_id=vpc_main.id,
    tags={"Name": "s3-flow-log"})

flowlog_group = aws.cloudwatch.LogGroup("flowLog",
    name="VPCFlowLogs")

flow_log_cloudwatch = aws.ec2.FlowLog("cloudwatchFlowLog",
    iam_role_arn=flowIAMDeliverRole,
    log_destination=flowlog_group.arn,
    log_destination_type="cloud-watch-logs",
    max_aggregation_interval=60,
    traffic_type="ALL",
    vpc_id=vpc_main.id,
    tags={"Name": "cloudwatch-flow-log"})


pulumi.export('webserver', webserver)
pulumi.export('flowlogs3', flow_log_s3)
pulumi.export('flowlogcloudwatch', flow_log_cloudwatch)
