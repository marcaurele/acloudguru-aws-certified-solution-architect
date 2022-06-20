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
- does not support multi-AZ deployments.
- best HA option is to use a multi-node clusters which support data replication and node recovery.

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

### Data models documentation

- <https://d1.awsstatic.com/whitepapers/Storage/AWS%20Storage%20Services%20Whitepaper-v9.pdf>
- <https://d1.awsstatic.com/whitepapers/Multi_Tenant_SaaS_Storage_Strategies.pdf>
- <https://d0.awsstatic.com/whitepapers/performance-at-scale-with-amazon-elasticache.pdf>
- [AWS re:Invent 2017: Deep dive on S3 and Glacier storage management](https://www.youtube.com/watch?v=SUWqDOnXeDw)
- [AWS re:Invent 2017: ElastiCache Deep Dive: Best Practices and Usage Patterns](https://www.youtube.com/watch?v=_YYBdsuUq2M)
- [AWS re:Invent 2017: Deep Dive: Using Hybrid Storage with AWS Storage Gateway to Solve On-Premises Storage Problems](https://www.youtube.com/watch?v=9wgaV70FeaM)
- <https://d1.awsstatic.com/whitepapers/cost-optimization-storage-optimization.pdf>

## Network

- 5 addresses are not usable in each range (0=NetAddress,1=AWS-VPC-router,2=AWS-DNS,3=AWS-Future-Use,255=Broadcast=Reserved-as-not-usable).
- VPCs support IPv4 netmask range from /16 to /28.

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

### Network documentation

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

## Security

### Accounts

![accounts structure](assets/2022-05-30_20-24.png)

### AWS Directory Services

- AWS Cloud Directory: cloud-native directory to share and control access to hierachical data between applications
- Amazon Cognito: Sign-up and Sign-in functionality that scales and federated to public social media services
- AWS Directory Service for MS AD: AWS-managed full Microsft AD
- AD Connector: Allow on-prem users to log in into AWS using existing AD credentials. Allow also EC2 to join AD domain. Can used IAM roles. Support Radius MFA.
- Simple AD: low scale, low cost AD implementation based on Samba (simple user directory with LDAP compatibility). MFA not supported. Kerberos based SSO. Does not support trust relationship with other domains.

### DDoS

- minimize surface attack: NACLs, SGs, VPC design
- scale to absorb: auto scaling groups, CloudFront, Static website on S3
- safeguard exposed resources: route53, AWS WAF, AWS Shield
- learn normal behavior: AWS GuardDuty, CloudWatch

### AWS Service Catalog

- framework allowing administrators to create pre-definied products and landscapes for their users.
- granular control over which users have access to hwhich offerings
- makes use of adopted IAM roles so users don't need underlying service access
- allow end users to be self-sufficient while upholding enterprise standards for deployments
- based on CloudFormation templates
- administrators can version and remove products. Existing running product versions will not be shutdown.
- use constraints:
  - Launch constraint
    - what: IAM role that Service Catalog assumes when an end-user launches a product.
    - why: without a launch constraint, the end-user must have all permissions needed within their own IAM credentials.
  - Notification Constraint:
    - what: specifies the Amazon SNS topic to receive notifications about stack events.
    - why: can get notifications when products are maunched or have problems.
  - Template Constraint:
    - what: one or more rules that narrow allowable values an end-user can select.
    - why: adjust product attributes based on choices a user makes (ex: only allow certain instances types for DEV environment).
- can be shared through multi-account with the templates within the master. Auto cascading of changes to sub accounts. Must rewrite launch stack to target the sub-account otherwise it will try in the main one (owner of the template)

### Security documentation

- [Organizing Your AWS Environment Using Multiple Accounts](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html)
- [AWS Best Practices for DDoS Resiliency](https://d1.awsstatic.com/whitepapers/Security/DDoS_White_Paper.pdf)
- [AWS re:Invent 2017: Best Practices for Managing Security Operations on AWS](https://www.youtube.com/watch?v=gjrcoK8T3To)
- [AWS re:Invent 2018: [REPEAT 1] Become an IAM Policy Master in 60 Minutes or Less](https://www.youtube.com/watch?v=YQsK4MtsELU)
- [AWS re:Invent 2017: Architecting Security and Governance Across a Multi-Account Stra](https://www.youtube.com/watch?v=71fD8Oenwxc)
- [AWS re:Inforce 2019: Managing Multi-Account AWS Environments Using AWS Organizations](https://www.youtube.com/watch?v=fxo67UeeN1A)
- [AWS Well-Architected Framework - Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/wellarchitected-security-pillar.pdf)

## Migrations

### Strategies

- Re-host: lift ans shift
- Re-platform: Lift and reshape
- Re-Purchase: drop and shop
- Reachitect: redesign in a cloud native manner
- Retire: get rid of apps not needed
- Retain: do nothing option

### Cloud Adoption Framework

<https://aws.amazon.com/professional-services/CAF/>

### Migration tools

- Server migration: agent for Vmware or HyperV to clone and periodically sync AMI changes to move or backup/recovery image on the cloud.
- Database migration service: can use a data conversion tool to help migrating to cloud DB (Redshift, RDS, Dynamodb)
- Application Discovery Service: collects config, usage and bhavior data from on prem servers to help estimate TCO of running on AWS. Gather information about on-prem data centers (inventory).

### Network migrations and cutovers

Start with VPN connection from on-prem. Later move to Direct Connect (BGP) with VPN as backup, requires to setup BGP preferences to use the Direct Connect link instead of the VPN (while having the same BGP prefix for both). On AWS Direct Conenct is always the preferred route.

### Migration documentation

- [AWS Migration Whitepaper](https://d1.awsstatic.com/whitepapers/Migration/aws-migration-whitepaper.pdf)
- [Overview of AWS Cloud Adoption Framework](https://docs.aws.amazon.com/whitepapers/latest/overview-aws-cloud-adoption-framework/overview-aws-cloud-adoption-framework.pdf)
- [Migrating Applications Running Relational Databases to AWS](https://d1.awsstatic.com/whitepapers/Migration/migrating-applications-to-aws.pdf)
- [Cloud-Driven Enterprise Transformation on AWS](https://d1.awsstatic.com/whitepapers/cloud-driven-enterprise-transformation-on-aws.pdf?did=wp_card&trk=wp_card)
- [AWS re:Invent 2017: How to Assess Your Organization's Readiness to Migrate at Scale](https://www.youtube.com/watch?v=id-PY0GBHXA)
- [AWS re:Invent 2017: Migrating Databases and Data Warehouses to the Cloud](https://www.youtube.com/watch?v=Y33TviLMBFY)
- [AWS re:Invent 2017: Deep Dive: Using Hybrid Storage with AWS Storage Gateway to Solve Pn-Prem Storage Problems](https://www.youtube.com/watch?v=9wgaV70FeaM)

## Architecting to Scale

- scale in + scale out = horizontal scaling terms
- scale up + scale down = vertical scaling terms

### Auto scaling

- autoscaling launch configuration cannot be edited.
- terminate the oldest first, and try to spread the termination over the AZs.

### Kinesis

- collection of services for processing streams of various data.
- data is processed in "shards" - with each shart able to ingest 1000 records per second.
- a default limit of 500 shards, but can be increase to unlimited
- record consists of partition key, sequence number and data blob (up to 1MB)
- transient data store - default retention of 24 hours, but can be configured for up to 7 days.

### SQS

- KMS encryption available to encrypt messages.
- transient storage - default 4 days, max 14 days.
- optionally support FIFO queue ordering
- maximum message size of 256KB, but with a special Java SQS SDK, messages can be as large as 2GB (stored on S3).

### Amazon MQ

- managed implementation of Apache ActiveMQ
- support JMS, NMS, MQTT, WebSocket
- less features than SQS

### Simple Workflow Service

- create distributed asynchronous systems as workflows.
- supports both sequential and parallel processing.
- tracks state of your workflow which you interact and update via API.
- best suited for human-enabled workflows like an order fulfillment.
- AWS recommends new applications, look at Step Functions over SWF.

### AWS Steps Fucntions

- managed workflow and orchestration platform.
- define your app as a state machine.
- create tasks, sequential steps, paralelle steps, branching paths or timers.
- amazon state language declarative JSON.
- apps can interact and update the stream via Step Function API.
- visual interface describes flow and realtime status.
- detailed logs of each step execution.

### Architecting to scale Documentation

- [Web Application Hosting in the AWS Cloud](https://d1.awsstatic.com/whitepapers/aws-web-hosting-best-practices.pdf)
- [Introduction to Scalable Gaming Patterns on AWS](https://d0.awsstatic.com/whitepapers/aws-scalable-gaming-patterns.pdf)
- [Performance at Scale with Amazon ElastiCache](https://d0.awsstatic.com/whitepapers/performance-at-scale-with-amazon-elasticache.pdf)
- [Automating Elasticity](https://d1.awsstatic.com/whitepapers/cost-optimization-automating-elasticity.pdf)
- [AWS re:Invent 2017: Scaling Up to Your First 10 Million Users](https://www.youtube.com/watch?v=w95murBkYmU)
- [AWS re:Invent 2017: Learn to Build a Cloud-Scale WordPress Site That Can Keep Up](https://www.youtube.com/watch?v=dPdac4LL884)
- [AWS re:Invent 2017: Elastic Load Balancing Deep Dive and Best Practices](https://www.youtube.com/watch?v=9TwkMMogojY)
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [Implementing Microservices on AWS](https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices-on-aws.pdf)

## Business Continuity

- RTO: Recovery Time Objective
- RPO: Recovery Point Objective (acceptable amount of data loss measured in time)

![RTP - RPO](./assets/2022-06-06_20-42.png)

![HA - DR - RPO](./assets/2022-06-06_20-44.png)

### Business Continuity Documentation

- [AWS Prescriptive Guidance / Backup and recovery approaches on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/backup-recovery/backup-recovery.pdf)
- [Getting Started with Amazon Aurora](https://d1.awsstatic.com/whitepapers/getting-started-with-amazon-aurora.pdf)
- [Reliability Pillar / AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/wellarchitected-reliability-pillar.pdf)
- [AWS re:Invent 2017: Models of Availability](https://www.youtube.com/watch?v=xc_PZ5OPXcc)
- [AWS re:Invent 2017: How to Design a Multi-Region Active-Active Architecture](https://www.youtube.com/watch?v=RMrfzR4zyM4)
- [AWS re:Invent 2017: Disaster Recovery with AWS: Tiered Approaches to Balance Cost with Recovery Objectives](https://www.youtube.com/watch?v=a7EMou07hRc)

## Deployment and Operations management

### Elastic Beanstack

_AWS PaaS_

- Orchestration service to make it push-button easy to deploy scalable web landscapes.
- Wide range of supported platforms (Docker, PHP, Java, Node.js...).
- Multiple environments within the application (DEV, QA, ...).
- Great for ease of deployment, but not great if you need lots of control and flexibility.

### CloudFormation

- using JSON or YAML to model and provision entire landscapes.
- repeatable and automatic deployments and rollbacks.
- terms:
  - Templates (TF files): JSON/YAML file containing instructions for the building-out the AWS environment.
  - Stacks (TF workspaces): the entire environment described by the template and created, updated and deleted as a single unit.
  - Change sets (TF plan): a summary of proposed changes to your stack that will allow you to see how those changes might impact your existing resources before implementing them.
- Stack policies deny you to do any update, so it must be declared in the policy to allow such operations.

### AWS Config

- Allow you to assess, audit and evaluate configurations of your AWS resources.
- Very useful for Configuration Management as part of an ITIL program.
- Creates a baseline of various configuration settings and files then can track drift.
- Can check resources for certain desired conditions and if violations are found, the resource is flagged as _noncompliant_.

### AWS OpsWorks

- managed instance of Chef and Puppet.
- OpsWorks Stack is Chef single agent, requires Stack in each region as it can only control resources in that same region.

### AWS System Manager

- inventory: collect inventory from OS, applications instances.
- state-manager: creates state that represents a certain configuration is applied to instances
- logging: CloudWatch Log agent streams logs directly to CloudWatch
- parameter-store: shared secured storage for config data
- resource-groups: group resource through tagging for organization
- maintenance-window: define schedule for instances patch, update apps...
- automation:automating routine maintenance tasks and scripts
- run-command: run commands and scripts without loggin in via SHH/RDP
- patch-manager: automates process of patching

### Business Applications and End-USer Computing

- Amazon Workspaces: remote desktop (full desktop)
- Amazon AppStream: show only a hosted application (application hosting)
- AWS Connect: center solution with configurable call
- Amazon Chime: online meeting and video conferencing service
- Amazon WorkDocs: like GDrive
- Amazon WorkEmail: fully managed email service
- Amazon WorkLink: provide secure access to internal web applications for mobile devices
- Alexa for Businnes: Alexa functionnality and skills for internal in your enterprise

### AWS Machine Learning

- SageMaker: ML services managed by AWS
- Amazon Comprehend: NLP
- Amazon Polly: test tp speech in many languages

### Deployment and Operations management Documentation

- [Overview of Deployment Options on AWS](https://d0.awsstatic.com/whitepapers/overview-of-deployment-options-on-aws.pdf)
- [Infrastructure as Code](https://d1.awsstatic.com/whitepapers/DevOps/infrastructure-as-code.pdf)
- [Practicing Continuous Integration and Continuous Delivery on AWS](https://d1.awsstatic.com/whitepapers/DevOps/practicing-continuous-integration-continuous-delivery-on-AWS.pdf)
- [Overview of Deployment Options on AWS](https://d1.awsstatic.com/whitepapers/overview-of-deployment-options-on-aws.pdf)
- [AWS re:Invent 2017: Deep Dive on AWS CloudFormation](https://www.youtube.com/watch?v=01hy48R9Kr8)
- [AWS re:Invent 2017: Moving to Containers: Building with Docker and Amazon ECS](https://www.youtube.com/watch?v=Qik9LBktjgs)
- [AWS re:Invent 2017: Continuous Integration Best Practices for Software Development Teams](https://www.youtube.com/watch?v=GEPJ7Lo346A)

## Cost Management

- [Cost Optimization Pillar](https://d1.awsstatic.com/whitepapers/architecture/AWS-Cost-Optimization-Pillar.pdf)
- [Maximizing Value with AWS](https://d1.awsstatic.com/whitepapers/total-cost-of-operation-benefits-using-aws.pdf)
- [Introduction to AWS Economics](https://d1.awsstatic.com/whitepapers/introduction-to-aws-cloud-economics-final.pdf)
- [AWS re:Invent 2017: Building a Solid Business Case for Cloud Migration](https://www.youtube.com/watch?v=CcspJkc7zqg)
- [AWS re:Invent 2017: Running Lean Architectures: How to Optimize for Cost Efficiency](https://www.youtube.com/watch?v=XQFweGjK_-o)
- [AWS re:Invent 2017: How Hess Has Continued to Optimize the AWS Cloud After Migrating](https://www.youtube.com/watch?v=1Z4BfRj2FiU)
