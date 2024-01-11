# CodePipeline CloudFormation Template

### Overview

This CloudFormation template deploys an AWS CodePipeline for continuous integration and continuous deployment (CI/CD) of a containerized React App that is hosted on ECR and deployed via AWS Fargate.

### Prerequisites

Before deploying this template, make sure you have the following:

- An existing Amazon ECS cluster
- An Amazon S3 bucket to store pipeline artifacts
- An AWS CodeCommit repository or an external Git repository

### How to Use

Follow these steps to deploy the ECS pipeline:

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-repo/ecs-pipeline.git
   ```
2. Navigate to the `ecs-pipeline` directory:

   ```bash
   cd ecs-pipeline
   ```
3. Deploy the CloudFormation stack using the AWS CLI:

   ```bash
   aws cloudformation create-stack --stack-name ecs-pipeline --template-body file://ecs_pipeline.yml --capabilities CAPABILITY_IAM
   ```
4. Monitor the stack creation progress in the AWS CloudFormation console.
5. Once the stack creation is complete, the ECS pipeline will be ready for use.

### Cleanup

To delete the ECS pipeline and associated resources, run the following command:

```bash
aws codepipeline delete-pipeline --name ecs-pipeline
```

- Note: deleting a pipleine does not delete the resources used in the pipeline.
