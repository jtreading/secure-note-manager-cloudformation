# PostgreSQL EC2 Instance with CloudFormation

This CloudFormation template deploys an EC2 instance with PostgreSQL installed and configured. The template includes a security group that allows SSH and PostgreSQL access, making it suitable for hosting a PostgreSQL database.

### Parameters

- **IngressCIDR**: The CIDR range for SSH and PostgreSQL access. Default: 0.0.0.0/0 (Allow from all IP addresses)
- **KeypairName**: The name of the EC2 key pair to associate with the instance. Default: SNMKeypair
- **AMI**: The Amazon Machine Image (AMI) to use for the instance. Default: ami-058bd2d568351da34

### How to Use

1. Open the AWS CloudFormation console.
2. Create a new stack and upload this template.
3. Provide values for the required parameters (IngressCIDR, KeypairName, AMI).
4. Review and create the stack.
5. Once the stack is created, retrieve the public IP of the EC2 instance from the AWS Console.
6. Connect to the EC2 instance using SSH.
7. Verify PostgreSQL installation and configuration.

### Notes

- Make sure to replace the default password 'CHANGEME' for the 'webuser' when deploying in a production environment.
- The template allows access from all IP addresses (0.0.0.0/0) by default. Consider restricting access for security purposes.
