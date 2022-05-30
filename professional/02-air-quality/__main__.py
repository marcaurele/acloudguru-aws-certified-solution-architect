"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

glue_air_quality_catalog_database = aws.glue.CatalogDatabase(
    "awsGlueAirQualityCatalogDatabase",
    name="AirQuality"
)

crawler_air_quality = aws.glue.Crawler("air-quality",
    database_name=glue_air_quality_catalog_database.name,
    role=aws_iam_role["example"]["arn"],
    s3_targets=[aws.glue.CrawlerS3TargetArgs(
        path=f"s3://openaq-fetches/realtime/2018-10-09/",
    )])
