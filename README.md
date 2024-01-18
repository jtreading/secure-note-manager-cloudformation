# Secure Note Manager CloudFormation Stack

This CloudFormation stack deploys a Secure Note Manager application on AWS. The application consists of the following resources:

- EC2 Nginx Reverse Proxy Server
- EC2 PostgreSQL Database
- ECS Fargate Cluster for UI
- ECS Fargate Cluster for API
- CodePipeline for automatic CI/CD

## Prerequisites

Before deploying the stack, make sure you have the following:

- AWS CLI installed and configured
- AWS credentials with sufficient permissions
- Docker installed (for local development)

## Deployment Steps

1. Clone this repository:

    ```bash
    git clone https://github.com/your-repo/secure-note-manager-cloudformation.git
    ```

2. Navigate to the project directory:

    ```bash
    cd secure-note-manager-cloudformation
    ```

3. Deploy the CloudFormation stack:

    ```bash
    aws cloudformation deploy --template-file stack.yml --stack-name secure-note-manager-stack --capabilities CAPABILITY_IAM
    ```

4. Wait for the stack deployment to complete.

5. Access the Secure Note Manager application using the provided URLs.

## Configuration

The CloudFormation stack can be customized by modifying the `stack.yml` file. You can adjust parameters such as instance types, database credentials, and container images.

## Development

To run the application locally for development purposes, follow these steps:

1. Install the required dependencies:

    ```bash
    npm install
    ```

2. Start the development server:

    ```bash
    npm run dev
    ```

3. Access the application at `http://localhost:3000`.

## CI/CD

The CodePipeline included in this stack automatically builds and deploys the application whenever changes are pushed to the repository. The pipeline is triggered by changes to the `main` branch.

## Cleanup

To delete the CloudFormation stack and all associated resources, run the following command:
