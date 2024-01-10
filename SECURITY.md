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

Custom SSL certificate can be stored in IAM in regions where ACM is not available.

### KMS

- MUST DO: read KMS FAQ
- Keys are region based, but option can be activated to have a multi-region one (replicated) - region selection required.
- CMK can be rotate automatically once a year.
- Min 7 days waiting period for key deletion, + getting error message about key being in deletion process
- External managed keys CMK (Customer Master Key - imported material) are done through wrapping key and import token to secure the transfer
  - No need to wait 7 days for deletion
  - Same key can be re-imported (same key for all regions)
  - custom key generation choice
- AWS KMS keys are rotated every year
- Able to encrypt a non-encrypted EBS from a snapshot, when copying it, or can change the key used to encrypt the volume
- EC2 keypair only appends the key to any existing authorized_keys file existing in the base image. Can be used to restore access using keys only with a new image creation and new instance.
- Keys admin can administrate but not use.
- Keys users can use the key but not manage it (rotation, ...).
- Key in the destination region must be used for cross region replication.
- Imported key material, AWS manages lifecycle of the key, if the key has an expiry, it is automatically deleted at that date without soft deletion period.

#### KMS Grants

Grants are an alternative access control mechanism to a Key Policy:

- done programmatically, delegate the use of KMS CMKs to other AWS principals (a user - in another account)
- temporary, granular permissions (encrypt, decrypt, re-encrypt, describekey...)
- allow access, **not deny**
- use Key policies for relatively static permissions and explicit deny.

Used for just in-time access to key material for key operations.

```console
#Create a new key and make a note of the region you are working in
aws kms create-key

#Test encrypting plain text using my new key:
aws kms encrypt --plaintext "hello" --key-id <key_arn>

#Create a new user called Dave and generate access key / secret access key
aws iam create-user --user-name dave
aws iam create-access-key --user-name dave

#Run aws configure using Dave's credentials creating a CLI profile for him
aws configure --profile dave
aws kms encrypt --plaintext "hello" --key-id <key_arn> --profile dave

#Create a grant for user called Dave
aws iam get-user --user-name dave
aws kms create-grant --key-id <key_arn> --grantee-principal <Dave's_arn> --operations "Encrypt"

#Encrypt plain text as user Dave:
aws kms encrypt --plaintext "hello" --key-id <key_arn> --grant-tokens <grant_token_from_previous_command> --profile dave

#Revoke the grant:
aws kms list-grants --key-id <key_arn>
aws kms revoke-grant --key-id <key_arn> --grant-id <grant_id>

#Check that the revoke was successful:
aws kms encrypt --plaintext "hello" --key-id <key_arn> --profile dave

https://docs.aws.amazon.com/cli/latest/reference/kms/create-grant.html
```

#### KMS Policy Conditions

Specific policies for KMS, most import is `kms:ViaService`: a condition key which can allow or deny access to your CMK depending on which service originated the request.

#### KMS cross account

Enable access in the Key Policy for the external account in the account which owns the CMK, enable access to KMS in the IAM policy for the external account, both required in order for the share access to work.

### AWS WAF & Shield

- CloudFront WAF is global
- ALB WAF is regional
- WAF: can allow, deny or count request
- CloudFront can be used to protect website not hosted on AWS (support custom origin)

- Shield, simple mode activated by default to protect against DDoS
- Advanced mode with incident response team and in depth reporting, not paying for resources due to DDoS attack

### Dedicated instances vs Hosts

Both on dedicated physical hardware but the main differences are from the dedicated hosts:

- provide a static list of physical hosts
- pay per the host, not the instances
- visibility over the physical resources (sockets, cores, host ID)

Dedicated hosts are usually needed with regulatory requirements or licensing conditions.

## Data Protection With VPCs

- Session Manager (recall): use to perform remote login on EC2 instance without opening a port (done through AWS HTTP API). Can be used with browser, cli or SDK to have bash/powershell sessions. All logged (all commands and their output).

### HSM

- single tenant
- price per usage now

```console
openssl genrsa -aes256 -out customerCA.key 2048
openssl req -new -x509 -days 3652 -key customerCA.key -out customerCA.crt
nano <cluster_id>_ClusterCsr.csr
openssl x509 -req -days 3652 -in <cluster_id>_ClusterCsr.csr \
                              -CA customerCA.crt \
                              -CAkey customerCA.key \
                              -CAcreateserial \
                              -out <cluster_id>_CustomerHsmCertificate.crt
wget https://s3.amazonaws.com/cloudhsmv2-software/CloudHsmClient/EL7/cloudhsm-client-latest.el7.x86_64.rpm
sudo yum install -y ./cloudhsm-client-latest.el7.x86_64.rpm
cp customerCA.crt /opt/cloudhsm/etc/customerCA.crt
sudo /opt/cloudhsm/bin/configure -a <cluster_IP>
/opt/cloudhsm/bin/cloudhsm_mgmt_util /opt/cloudhsm/etc/cloudhsm_mgmt_util.cfg
enable_e2e
listUsers
loginHSM PRECO admin password
changePswd PRECO admin <NewPassword>
listUsers
logoutHSM
loginHSM CO admin acloudguru
createUser CU ryan acloudguru
listUsers
logoutHSM
quit
sudo service cloudhsm-client start
/opt/cloudhsm/bin/key_mgmt_util
loginHSM -u CU -s ryan -p acloudguru
genSymKey -t 31 -s 32 -l aes256
genRSAKeyPair -m 2048 -e 65537 -l rsa2048
genSymKey -t 31 -s 16 -sess -l export-wrapping-key
exSymKey -k <symmetric_key> -out aes256.key.exp -w <wrapping_key>
exportPrivateKey -k <private_key> -out rsa2048.key.exp -w <wrapping_key>
exportPubKey -k 22 -out rsa2048.pub.exp
logoutHSM
exit
```

- 2 accounts created by default: PRECO (Precrypto Officer) and CO (Crypto Officer)
- 2 other extra types of user: CU (Crypto User) and AU (Appliance User)
- CO: performs user management
- CU: for key management: create, delete, share, import, export, encrypt, decrypt, sign, verify
- AU: manage the appliance - cloning, syncing.

*<https://docs.aws.amazon.com/cloudhsm/latest/userguide/manage-hsm-users-chsm-cli.html#user-permissions-table-chsm-cli>*

## Incident Response & AWS In The Real World

- AWS Shield: free service that protects AWS customers on ELB, CloudFront and Route53. Protect against SYN/UDP floods, reflection attacks and other layer 3+4. Paying package provides more advanced protection.
- AWS WAf only works with CloudFront and Application Load Balancer.
- API Gateway have a default 10K req./s for steady-state, burst limit of 5K. Cache, by default to 5 minutes and up to 1 hour.

## Updates Based On Student Feedback

### Amazon Macie

Fully managed data security and data privacy service that uses machine learning and pattern matching to discover, monitor, and protect **your sensitive data stored in your data lake**. Macie can be used to scan your data lakes and discover sensitive information such as PII or financial data, and identify and report overly permissive or unencrypted buckets. Great for PCS-DSS compliance. Mainly scanning S3 bucket content to classify data.

### AWS GuardDuty

AWS GuardDuty is a managed service that can watch CloudTrail, VPC Flow Logs and DNS Logs, **watching for malicious activity**. It has a build-in list of suspect IP addresses and you can also upload your own lists of IPs. GuardDuty can trigger CloudWatch events which can then be used for a variety of activities like notifications or automatically responding to a threat based on Lambdas.

### SES - Simple Email Service

Can use standard SMTP interface or SES API to send emails. Use port `587` or `2587` to avoid throttling which occurs on port `25` by AWS. Need to configure SG to allow communication with the corresponding port.

### Security Hub

Central hub for AWS alerts and findings coming from their security tools:

- GuardDuty
- Macie
- Inspector
- IAM Access Analyzer
- Firewall Manager
- 3rd party tools
- CloudWatch + events -> triggering Lambda actions

Provide an ongoing security audit.

### AWS Artifact

Central resource to download compliance and security documents. Can also evaluate your own cloud architecture. Can be used to assess effectiveness of current company controls.

### Notes

No packet inspection tool from AWS, only available using 3rd party vendors (on the marketplace).

## Read and watch

### Read

- [ ] KMS Best practices
- [ ] KMS crypto details
- [ ] DDOS best practices
- [ ] Logging in AWS
- [ ] well architecture frameowkr, security pillar

### Watch

- [ ] [AWS re:invent 2017: Best Practices for Implementing AWS Key Management Service (SID330)](https://www.youtube.com/watch?v=X1eZjXQ55ec)
- [ ] [AWS re:Invent 2017: A Deep Dive into AWS Encryption Services (SID329)](https://www.youtube.com/watch?v=gTZgxsCTfbk)
- [ ] [Best Practices for DDoS Mitigation on AWS](https://www.youtube.com/watch?v=HnoZS5jj7pk)

## Troubleshooting Scenarios

- [IAM Policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)
- KMS: keys themselves require key policy (admin, user or external account access)


## Links

- [Best practices for Security, Identity & Compliance](https://aws.amazon.com/architecture/security-identity-compliance/?cards-all.sort-by=item.additionalFields.sortDate&cards-all.sort-order=desc&awsf.content-type=*all&awsf.methodology=*all)
