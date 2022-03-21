"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

iam_for_lambda = aws.iam.get_role(name="lambda-execution-role")

remote_lambda_asset = pulumi.RemoteAsset("https://raw.githubusercontent.com/ACloudGuru-Resources/SQSLambdaTriggers/master/lambda_function.py")
asset_archive = pulumi.AssetArchive({
    "lambda_function.py": remote_lambda_asset
})
sqs_messages = aws.sqs.get_queue(name="Messages")

test_lambda = aws.lambda_.Function("SQSDynamoDB",
    name="SQSDynamoDB",
    code=asset_archive,
    role=iam_for_lambda.arn,
    handler="lambda_function.lambda_handler",
    runtime="python3.8")

test_lambda_event = aws.lambda_.EventSourceMapping("SQSEvent",
    event_source_arn=sqs_messages.arn,
    function_name=test_lambda.arn)
