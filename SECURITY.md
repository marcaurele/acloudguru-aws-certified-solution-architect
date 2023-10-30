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

### S3

- S3 ACL's are for fine grained access controls on individual file/object.
- Bucket policies limited to 20kb, might require to use ACLs.

### Conflicts

What happens when IAM policy conflicts with an S3 policy which conflicts with an S3 ACL?

-> union of them 3
-> always starts at the DENY
-> Is there an explicit DENY
-> Is there an explicit ALLOW, yes then ALLOW
-> otherwise DENY

### S3 Cross Region Replication

- Cross account, the dest account must have object permission to read object and read access list (READ_ACP) in order for the objects to be replicated.
- AWS KMS key encryption allow replication if enabled explicitly.
- no need for explicit bucket policy to have replication over TLS (it's the default).
- Versioning must be enabled.
- Delete markers are replicated, deleted versions of files are not.

## Links

- [Best practices for Security, Identity & Compliance](https://aws.amazon.com/architecture/security-identity-compliance/?cards-all.sort-by=item.additionalFields.sortDate&cards-all.sort-order=desc&awsf.content-type=*all&awsf.methodology=*all)
