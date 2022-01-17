"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

import json
import os
import mimetypes

# Create an AWS resource (S3 Bucket)
bucket = aws.s3.Bucket('my-bucket-071343648403',
    bucket='my-bucket-071343648403',
    website=aws.s3.BucketWebsiteArgs(
        index_document="index.html",
        error_document="error.html"))

for file in os.listdir('.'):
    if file.endswith('.html'):
        file_path = os.path.join('.', file)
        file_type, _ = mimetypes.guess_type(file_path)
        obj = aws.s3.BucketObject(
            file,
            bucket=bucket.id,
            source=pulumi.FileAsset(file_path),
            content_type=file_type
        )

bucket_arn = bucket.arn

def public_read_policy_for_bucket(bucket_name):
    return json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                f"{bucket_name}/*",
            ]
        }]
    })


bucket_policy = aws.s3.BucketPolicy("allowPublicReadAccessWebsite",
    bucket=bucket.id,
    policy=bucket.arn.apply(public_read_policy_for_bucket)
)

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)
pulumi.export('bucket_arn', bucket.arn)
pulumi.export('website_url', bucket.website_endpoint)