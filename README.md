# Solution Architect Associate

## Notes

- AWS whitepapers: <https://aws.amazon.com/whitepapers> look at the well architecture framework (operation excellence, security, reliability, performance effiency, cost optimization).

### IAM

Exercise 1, remove permission on the group fo developer and fetch AWS account keys.

### EC2

- InstanceProfile volume are available on some instance type, and is an ephemereal volume (don't survive stop operation, only reboot). Cost is included in instance type.

## RDS

- 35 days max for backups
- MySQL engine, not MariaDB!

### VPC

- default VPC is user friendly with things already defined with internet access (public + private IP), having `172.31.0.0/16`.
- AWS keeps 5 IPv4 addresses for them (0,1,2,3,255).
- NACL: only 1 per subnet, rules evaluated from lowest numbered rule, stateless so require inbound + outbound rules. Way to block IP Addresses to access VPC. Ephemereal ports issue as they must be defined in rule.

### SQS

Know the defaults for the exam!

- no realtime message delivery
- delivery delay setting between 0 and 15 minutes
- 256KB of text max for the message
- not encrypted by default at rest by default, only in transit
- message retention, default 4 days, max 14, min 1 day
- long polling isn't the default but should be used by default
- queue depth can trigger autoscaling
- visibility timeout: lock on message by default on 30s to hide it until marked as done
- dead letter queue is another SQS queue
  - max retry value: number of retries before msg sent to the dead letter queue
- fifo queue when ordering is important or cannot have duplicates, but 300 msg/sec max, higher cost
  - requires a message group id

### SNS

Settings:

- subscribers
- 256KB of text for the message
- dead letter queue as well with SQS queue
- can have a access policy
- fifo SNS only supports SQS as subscribers
- no retry except for http(s)

### API Gateway

- to protect API with a WAF
- versioning (done with stages)
- protect with abuse / throttling

### Kinesis

- real time message delivery (but complicated)
- Kinesis firehose (almost real time), simpler
- auto scalling
- store data up to 1 year

### Athena

query language for S3 data

### Lambda

- 15 min max, 10GB RAM max

### EventBridge

CloudWatch Events version 2.0. Event based lambda function trigger.

### AWS Shield

DDoS protection

### Guard duty

Protection looking at logs (VPC flow, DNS, ...) based on AI to learn behavior.

### Macie

Monitoring of S3 buckets for sensitive data. Usefull for GDPR.

### Parameter store

Max 10'000 items.

### System Manager

- run command on your hosts
- require the system manager to be installed and a role
- Automation document / Runbook to fix S3 permissions for example, configure inside EC2 instances
- free when running for AWS resources.

### CloudFront

- global distributuin, no specific countries
- can force an expiration of content from the cache without waiting for TTL
- only solution to have TPPS in front of S3 bucket website

### Organizations

- create a dedicated account for logging
- consolidated billing
- service control policies (limit what user can do in account) - even applied to the root account, and only way to restrict that root account.

### Resource Access Manger (RAM)

Share resources across accounts, like VPC, subnets, internet gateway, ... so remove the need to create those everywhere.

### AWS Config

- allow to query by resource type, tag, even to see deleted architecture
- enforce: to flag when something is going wrong/rule violated, and can trigger a fix
- history: when did it change, who made the call?

## Pulumi notes

```console
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export PULUMI_CONFIG_PASSPHRASE=
```
