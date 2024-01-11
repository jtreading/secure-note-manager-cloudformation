# CloudFormation Template: debian-nginx.yml

This CloudFormation template deploys an Nginx web server on a Debian-based EC2 instance.

### Prerequisites

Before deploying this CloudFormation template, make sure you have the following:

- An AWS account
- An existing VPC and subnet in your AWS account

### Parameters

This CloudFormation template accepts the following parameters:

- **VpcId**: The ID of the VPC where the EC2 instance will be deployed.
- **SubnetId**: The ID of the subnet where the EC2 instance will be deployed.
- **InstanceType**: The EC2 instance type to use for the Nginx server.
- **KeyName**: The name of an existing EC2 key pair to enable SSH access to the instance.

### How to Use

To deploy this CloudFormation template, follow these steps:

1. Clone this repository to your local machine.
2. Open the AWS Management Console and navigate to the CloudFormation service.
3. Click on "Create stack" and select "Upload a template file".
4. Choose the `debian-nginx.yml` file from your local repository.
5. Fill in the required parameters, such as the VPC and subnet IDs.
6. Click on "Next" and follow the on-screen instructions to complete the stack creation process.

### Outputs

This CloudFormation template provides the following outputs:

- `WebServerURL`: The URL of the Nginx web server.

### License

This CloudFormation template is licensed under the [MIT License](LICENSE).
