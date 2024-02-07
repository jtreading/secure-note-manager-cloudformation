#!/bin/bash

# Set the path to the CloudFormation templates directory
TEMPLATE_DIR="/path/to/cloudformation/templates"

# Set the path to the keypair.pem file
KEYPAIR_FILE="/path/to/keypair.pem"

# Send all local cloudformation templates to S3
aws s3 sync $TEMPLATE_DIR s3://my-bucket/cloudformation

# Deploy the nested template
aws cloudformation deploy \
    --template-file "$TEMPLATE_DIR/template1.yaml" \
    --stack-name stack1 \
    --capabilities CAPABILITY_IAM \
    --region us-west-2 \
    --profile default \
    --parameter-overrides Parameter1=Value1 Parameter2=Value2 \
    --tags Key1=Value1 Key2=Value2
