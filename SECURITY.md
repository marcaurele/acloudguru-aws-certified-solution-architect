# Security

## Security models

### CIA model

#### **C**onfidential

- MFA
- IAM

#### **I**ntegrity

- Auto-scaling
- Multi AZ

#### **A**vailability

- Certificate MAnager,
- IAM
- Bucket Policies

### AAA model

_Authentication (IAM), Authorization (Policies), Accounting (CloudTrail)._

### Non-repudiation

Can't deny.

## Security in AWS

- Cloud HSM for FIPS-140-2 compliance (dedicated hardware, no multi tenant)

## Identity Access Management, S3 & Security Policies

- to add about permission boundaries: AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries.

### S3

- S3 ACL's are for fine grained access controls on individual file/object. Only ACLs allow you define object level permissions in S3.
- Bucket policies limited to 20kb, might require to use ACLs.

### Conflicts

What happens when IAM policy conflicts with an S3 policy which conflicts with an S3 ACL?

-> union of them 3
-> always starts at the DENY
-> Is there an explicit DENY
-> Is there an explicit ALLOW, yes then ALLOW
-> otherwise DENY

### S3

- IAM policy condition to ensure it's through HTTPS is:

```json
"Condition": {
  "Bool": {"aws:SecureTransport": true}
}
```

### S3 Cross Region Replication

- Cross account, the dest account must have object permission to read object and read access list (READ_ACP) in order for the objects to be replicated.
- The owner of the destination bucket must grant the owner of the source bucket permissions to replicate objects with a bucket policy.
- AWS KMS key encryption allow replication if enabled explicitly.
- no need for explicit bucket policy to have replication over TLS (it's the default).
- Versioning must be enabled.
- Delete markers are replicated, deleted versions of files are not.

### STS

- Does not need to be a user in IAM when using Federation (typically ActiveDirectory).

### Glacier Vault Lock

- Initiate the lock by attaching the vault lock policy to the vault
- 24 hours to validate the policy and potentially to abort the operation
- once validated, lock policies are immutable.

### IAM

- Can request the credentials report with status of user's credentials in the account (last time password used, last time auth ley used...).
- Can be requested from the API/CLI with `aws iam generate-credentials-report` and `aws iam get-credentials-report`.
- CSV format for the report.

## Logging And Monitoring

### CloudTrail

- After the fact incident investigation
- Near realtime intrusion detection
- Compliance
- Send to S3 bucket (need to manage retention ourselves), delivered every 5 minutes up to 15 minutes delay, SNS notifications possible, can aggregate across regions and accounts
- enabled by default for 7 days (need config for extended time)
- logs are shipped with an optional integrity checksum file (SHA-256).

Info logged:

- Metadata around the API call
- Identity of the API caller
- Time of the API call
- Source IP
- Request parameters
- Response elements returned by the service

### CloudWatch

#### CloudWatch Events

- near realtime stream of system events (AWS resources state change, API calls, custom events, scheduled)
- rules to match events with target to handle the event.

### AWS Config

- assess, audit and evaluate configurations of your AWS resources.
- AWS managed rules which can be enabled
- customer managed rules. Can create Lambda to automate remediation.

### AWS Inspector

Automated security assessment service for vulnerabilities or deviations from best practices. Contains the CIS benchmark rules.

### AWS Trust Advisor

Online resource to help reduce cost, increase performance and improve security and fault tolerance by optimizing your AWS environment.

## Infrastructure Security

### KMS

- MUST DO: read KMS FAQ
- Keys are region based
- Min 7 days waiting period for key deletion, + getting error message about key being in deletion process
- External managed keys CMK (Customer Master Key - imported material) are done through wrapping key and import token to secure the transfer
  - No need to wait 7 days for deletion
  - Same key can be re-imported (same key for all regions)
  - custom key generation choice
- AWS KMS keys are rotated every year
- Able to encrypt a non-encrypted EBS from a snapshot, when copying it, or can change the key used to encrypt the volume
- EC2 keypair only appends the key to any existing authorized_keys file existing in the base image. Can be used to restore access using keys only with a new image creation and new instance.

## Data Protection With VPCs

## Incident Response & AWS In The Real World

## Updates Based On Student Feedback

## Troubleshooting Scenarios

## Links

- [Best practices for Security, Identity & Compliance](https://aws.amazon.com/architecture/security-identity-compliance/?cards-all.sort-by=item.additionalFields.sortDate&cards-all.sort-order=desc&awsf.content-type=*all&awsf.methodology=*all)
