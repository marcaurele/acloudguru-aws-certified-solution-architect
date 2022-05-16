# Solution Architect Professional

## Data models

- ACID: Atomic, Consistency, Isolated, Durable - like databases
- BASE: Basic Availibility, Soft-state, Eventual Consistency - like SNS/SQS, S3

Important:

- read the AWS Storage options whitepaper and note anti-patterns
- know when to use various data stores.

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

### EFS

- Implementation of NFS file share
- Pay as you use
- Multi AZ metadata and storage
- Can be mounted on prem, recommended with the DataSync service
- More expensive than S3 and EBS (of course)
- As of December 2016, the common mount target name of an EFS file system will resolve to its local mount target in each AZ. So, you only need to create mount targets in each AZ within the same subnet as the EC2 instances then use the common FQDN.

### Amazon Storage Gateway

- virtual machine that you run onprem with VMware or HyperV
- provides local storage resources backed by Glacier and S3
- use in cloud migration or disaster recovery
- different modes:
  - file gateway
  - volume gateway: async replication to s3
  - volume gateway cached mode: isci with data stored in s3 with frequent accessed data local on disk
  - tape gateway: virtual tape device for backups

### Amazon WorkDocs

- secure fully managed file collaboration service
- integrate with AS for SSO
- ISO compliant

### RDS

- Managed DB for:
  - MySQL,
  - Maria,
  - PostgreSQL,
  - Microsoft SQL,
  - Oracle,
  - MySQL-compatible Aurora
- Anti-patterns:
  - automated scaling: use DynamoDB (if possible)
  - complete control over the DB: use EC2
- Mutli-AZ for failover
- Read replicas for performance

### DynamoDB

- managed, multi AZ NoSQL data store with cross region replication option
- default to eventual consistent reads but can request strongly consistent read
- price on throughput rather than compute
- provision read and write capacity in anticipation if needed
- autoscale capacity
- on demand capacity flexible at a small premium cost
- can acieve ACID compliance with DynamoDB Transactions

- Primary key and sort key
- Possible local secondary index: same partition key as the table but different sort key. When you already know the partition key but want to quiclkly query on some other attribute.
- Possible global secondary index: partition key and sort key can be different from those on the table. For fast query when attributes fail outside of the primary key without need to do full scan

#### Secondary indexes

If you need to:

- access just a few attributes the fastest way possible:
  - consider projecting those few attibutes in a global secondary index
  - cost: minimal
  - benefit: lowest possible latency access for non-key items
- frequently access some non-key attributes:
  - consider projecting those attributes in a global secondary index
  - cost: moderateL aim to offset cost of table scans
  - benefit: lowest possible latency access for non-key items
- frequently access most non-key attributes:
  - consider projecting those attributes or even the entire table in a global secondary index
  - cost: up to double
  - benefit: maximum flexibility
- rarely query but write or update frequently:
  - consider projecting keys only for the global secondary index
  - cost: minimal
  - benefit: very fast write or updates for non-partition key items

### Amazon Redshift

- fully mamaged, cluster to petabyte
- extremely cost effective as compared to some other on-prem datawarehouse
- postgresql compatible with JDBC and ODBC drivers
- parallel processing and columnar data stores
- option to directly query files from s3 via redshift spectrum

_Redshift: name coming from moving away from Oracle datawarehouse / red logo color._

### Mamazon Neptune

- graph database fully managed
- support open graph API

### Amazon Elasticache

- fully managed of Redis or Memcached
- push button scalability for memory

#### Memcached

- simple
- you need to scale out and in as demand changes
- you need to run multiple CPU cores and threads
- you need to cache objects

#### Redis

- you need encryption
- you need HIPAA compliance
- support clustering
- you need high-availibility
- complex data types
- pub/sub scalability
- geospacial indexing
- backup and restore

### Amazon Athena

- SQL engine overlaid on S3 base on Presto
- use or convert data to Parquet format for big performance jump
- similar to Redshit spectrum
- format available for query ares: Parquet, JSON, Apache ORC but not XML

### Amazon Quantum Ledger Database (QLDB)

- based on blockchain concepts

### Amazon Blockchain

- Based on Ether

### Whitepapers

- <https://d1.awsstatic.com/whitepapers/Storage/AWS%20Storage%20Services%20Whitepaper-v9.pdf>
- <https://d1.awsstatic.com/whitepapers/Multi_Tenant_SaaS_Storage_Strategies.pdf>
- <https://d0.awsstatic.com/whitepapers/performance-at-scale-with-amazon-elasticache.pdf>
- [AWS re:Invent 2017: Deep dive on S3 and Glacier storage management](https://www.youtube.com/watch?v=SUWqDOnXeDw)
- [AWS re:Invent 2017: ElastiCache Deep Dive: Best Practices and Usage Patterns](https://www.youtube.com/watch?v=_YYBdsuUq2M)
- [AWS re:Invent 2017: Deep Dive: Using Hybrid Storage with AWS Storage Gateway to Solve On-Premises Storage Problems](https://www.youtube.com/watch?v=9wgaV70FeaM)
- <https://d1.awsstatic.com/whitepapers/cost-optimization-storage-optimization.pdf>

## Network

- 5 addresses are not usable in each range (0=NetAddress,1=AWS-VPC-router,2=AWS-DNS,3=AWS-Future-Use,255=Broadcast=Reserved-as-not-usable)

### Services

- AWS managed VPN: simple VPN connection
- AWS Direct Connect: dedicated network connection to AWS backbone (not encrypted by default - use AWS Direct Connect Plus VPN)
- AWS VPN CloudHub:
- Software VPN: provide your own VPN like OpenVPN
- Transit VPC: connecting geographically disperse VPCs (like a hub of VPCs), also to connect external providers VPCs like Azure.
- VPC peering: no transitive connection between multiple VPCs, need to set a route
- AWS PrivateLink: connection between VPCs, AWS services using interface endpoints. Pro: redundant, use AWS backbones. 1 interface gateway endpoint (dynamo and S3), the other are interface endpoint. For Gateway endpoints, security is with VPC Endpoint Policies.
- Egress-Only Internet Gateway: for IPv6 only as all addresses are public by default, this is stateful, must create a custom route `::/0`, to use instead of NAT IPv4.
- NAT Gateway is AWS managed, versus NAT Instance which a simple EC2 instance acting as a NAT. Gateway is high available in the AZ, not the NAT Instance.

### Enhanced networking

- custom virtual AWS network interface to get higher speed, available in AWS Linux AMI automatically.
- placement groups:
  - clustered: into single AZ
  - spread: max 7 instances per group
  - partition: extended spread when logical partition can be attached on the same rack hardware for performance, while still spreading the total cluster across multiple rack to ensure HA.

### Route53

- policies: simple, failover, geolocation, geoproximity, latency, multi-answers, weighted.

### Documentation

- [AWS re:Invent 2016: Amazon Global Network Overview with James Hamilton](https://www.youtube.com/watch?v=uj7Ting6Ckk)
- [Amazon Virtual Private Cloud
Connectivity Options](https://d0.awsstatic.com/whitepapers/aws-amazon-vpc-connectivity-options.pdf)
- [Integrating AWS with
Multiprotocol Label Switching](https://d1.awsstatic.com/whitepapers/Networking/integrating-aws-with-multiprotocol-label-switching.pdf)
- [Security in Amazon Virtual Private Cloud](https://docs.aws.amazon.com/vpc/latest/userguide/security.html)
- [AWS re:Invent 2017: Networking Many VPCs: Transit and Shared Architectures](https://www.youtube.com/watch?v=KGKrVO9xlqI)
- [AWS re:Invent 2017: Another Day, Another Billion Flows](https://www.youtube.com/watch?v=8gc2DgBqo9U)
- [AWS re:Invent 2017: Deep Dive into the New Network Load Balancer](https://www.youtube.com/watch?v=z0FBGIT1Ub4)
- [MLPS](https://aws.amazon.com/blogs/networking-and-content-delivery/tag/mpls/)
