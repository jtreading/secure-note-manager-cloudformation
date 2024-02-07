#!/bin/bash

# Configuration
AWS_PROFILE="default"
AWS_REGION="us-east-1"
STACK_NAME="SNM-Source-Stack"
TEMPLATE_FILE="../Pipelines/source.yml"

# Parameters
AppName="snm-demo"
ProjectName="SecureNoteManager"
Environment="Development"

PARAMETERS="ParameterKey=AppName,ParameterValue=$AppName ParameterKey=ProjectName,ParameterValue=$ProjectName ParameterKey=Environment,ParameterValue=$Environment"

# Create the CloudFormation stack with parameters
echo "Creating CloudFormation stack..."
aws cloudformation create-stack \
    --profile $AWS_PROFILE \
    --region $AWS_REGION \
    --stack-name $STACK_NAME \
    --template-body file://$TEMPLATE_FILE \
    --capabilities CAPABILITY_IAM \
    --parameters $PARAMETERS

# Wait for stack creation to complete
echo "Waiting for stack creation to complete..."
aws cloudformation wait stack-create-complete \
    --profile $AWS_PROFILE \
    --region $AWS_REGION \
    --stack-name $STACK_NAME

# Check stack creation status
STACK_STATUS=$(aws cloudformation describe-stacks \
    --profile $AWS_PROFILE \
    --region $AWS_REGION \
    --stack-name $STACK_NAME \
    --query 'Stacks[0].StackStatus' \
    --output text)

if [ $STACK_STATUS = "CREATE_COMPLETE" ]; then
    echo "Stack creation completed successfully."
    # Get stack outputs
    echo "Fetching stack outputs..."
    STACK_OUTPUTS=$(aws cloudformation describe-stacks \
        --profile $AWS_PROFILE \
        --region $AWS_REGION \
        --stack-name $STACK_NAME \
        --query 'Stacks[0].Outputs')

    echo "Stack outputs:"
    echo "$STACK_OUTPUTS"
else
    echo "Stack creation failed. Status: $STACK_STATUS"
fi
