# Fargate CloudFormation Template

### Overview

This repository contains a CloudFormation template for deploying resources using AWS Fargate.

### Prerequisites

Before deploying this CloudFormation template, make sure you have the following:

- An AWS account
- AWS CLI installed and configured

### Parameters

- IngressCIDR: The CIDR range allowed to access the cluster. Replace with reverse proxy server IP range.
- AccountId: Amazon account ID, used for locating default execution roles.
- AppName: Used to name the ECS cluster and ECR.
- VPCId: The ID of the VPC where the ECS cluster will be deployed.
- SubnetCIDR: CIDR block for the subnet where the ECS cluster will be deployed.

### How to Use

To deploy the Fargate resources using this CloudFormation template, follow these steps:

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/your-repo.git
   ```
2. Navigate to the `Fargate` directory:

   ```bash
   cd Fargate
   ```
3. Deploy the CloudFormation stack:

   ```bash
   aws cloudformation deploy --template-file fargate_resources.yml --stack-name fargate-stack --capabilities CAPABILITY_IAM
   ```
4. Monitor the stack creation progress in the AWS CloudFormation console.

### Cleanup

To delete the CloudFormation stack and associated resources, run the following command:

```bash
aws cloudformation delete-stack --stack-name fargate-stack
```

- Note: you cannot delete a stack that has termnation protection enabled.
