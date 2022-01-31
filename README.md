# Solution Architect Associate

## Notes

- AWS whitepapers: <https://aws.amazon.com/whitepapers> look at the well architecture framework (operation excellence, security, reliability, performance effiency, cost optimization).

### IAM

Exercise 1, remove permission on the group fo developer and fetch AWS account keys.

### EC2

- InstanceProfile volume are available on some instance type, and is an ephemereal volume (don't survive stop operation, only reboot). Cost is included in instance type.

## RDS

- 35 days max for backups

### VPC

- default VPC is user friendly with things already defined with internet access (public + private IP), having `172.31.0.0/16`.
- AWS keeps 5 IPv4 addresses for them (0,1,2,3,255).
- NACL: only 1 per subnet, rules evaluated from lowest numbered rule, stateless so require inbound + outbound rules. Way to block IP Addresses to access VPC. Ephemereal ports issue as they must be defined in rule.
