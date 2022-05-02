# Solution Architect Professional

## Data models

- ACID: Atomic, Consistency, Isolated, Durable - like databases
- BASE: Basic Availibility, Soft-state, Eventual Consistency - like SNS/SQS, S3

### Amazon S3

- Introduced in 2006, one of the first service
- Maximum object size is 5TB, max object single PUT is 5GB
- Recommended to use multi-part upload for file larger than 100MB
- Get a good view of the S3 storage class available

### Amazon Galcier

- max filesize is 40TB
- Glacier Vault lock to avoid archive to be changed / modified

### EBS

- Is single AZ!
