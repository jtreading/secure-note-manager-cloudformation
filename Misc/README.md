# CloudFormation Stack: EC2-PostgreSQL-Nginx-App

### Overview

This CloudFormation stack sets up a basic infrastructure with an EC2 instance for a PostgreSQL database, an EC2 instance for an Nginx reverse proxy, and associated security groups. The stack is designed to follow best security practices and provides a foundation for deploying a containerized web application.

### Prerequisites

- AWS CLI installed and configured with necessary credentials.
- AWS Key Pair for EC2 instances.

### Parameters

- `DatabaseSecurityGroupIngressCIDR`: CIDR range for inbound traffic to the PostgreSQL database.
- Ensure your AWS CLI is configured with the necessary permissions.

### Instructions

1. Clone this repository:

`git clone https://github.com/your-username/ec2-postgresql-nginx-app.git`

2. Navigate to the project directory:

`cd ec2-postgresql-nginx-app`

3. Deploy the CloudFormation stack using the AWS CLI:

```
aws cloudformation create-stack
--stack-name EC2-PostgreSQL-Nginx-App
--template-body file://template.yaml
--parameters ParameterKey=DatabaseSecurityGroupIngressCIDR,ParameterValue=0.0.0.0/0
--capabilities CAPABILITY_NAMED_IAM
```

Replace `0.0.0.0/0` with the desired CIDR range.

4. Monitor the stack creation progress in the AWS Management Console or using the CLI:

`aws cloudformation describe-stacks --stack-name EC2-PostgreSQL-Nginx-App`

5. Once the stack creation is complete, find the details of the created resources in the AWS Management Console.
6. To delete the stack when it's no longer needed, use the following command:

`aws cloudformation delete-stack --stack-name EC2-PostgreSQL-Nginx-App`

Confirm the deletion when prompted.

### Customization

- Adjust the CloudFormation parameters and template as needed for your specific use case.
- Update IAM roles, security groups, and instance configurations based on your security and performance requirements.
- For production use, consider incorporating additional security measures, such as SSL certificates, database backups, and more.

### Disclaimer

This CloudFormation template provides a basic setup and may require additional configurations based on your specific needs. Use it as a starting point and ensure that it aligns with your security and operational requirements.
