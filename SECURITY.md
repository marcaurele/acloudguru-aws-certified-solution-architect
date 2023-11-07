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

## Infrastructure Security

## Data Protection With VPCs

## Incident Response & AWS In The Real World

## Updates Based On Student Feedback

## Troubleshooting Scenarios

## Links

- [Best practices for Security, Identity & Compliance](https://aws.amazon.com/architecture/security-identity-compliance/?cards-all.sort-by=item.additionalFields.sortDate&cards-all.sort-order=desc&awsf.content-type=*all&awsf.methodology=*all)
