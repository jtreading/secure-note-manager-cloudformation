#!/bin/bash

# Set the path to the CloudFormation templates directory
TEMPLATE_DIR="/path/to/cloudformation/templates"

# Set the path to the keypair.pem file
KEYPAIR_FILE="/path/to/keypair.pem"

# Deploy the first CloudFormation template
aws cloudformation deploy \
    --template-file "$TEMPLATE_DIR/template1.yaml" \
    --stack-name stack1 \
    --capabilities CAPABILITY_IAM \
    --region us-west-2 \
    --profile default \
    --parameter-overrides Parameter1=Value1 Parameter2=Value2 \
    --tags Key1=Value1 Key2=Value2

# Deploy the second CloudFormation template
aws cloudformation deploy \
    --template-file "$TEMPLATE_DIR/template2.yaml" \
    --stack-name stack2 \
    --capabilities CAPABILITY_IAM \
    --region us-west-2 \
    --profile default \
    --parameter-overrides Parameter1=Value1 Parameter2=Value2 \
    --tags Key1=Value1 Key2=Value2

# Deploy the third CloudFormation template
aws cloudformation deploy \
    --template-file "$TEMPLATE_DIR/template3.yaml" \
    --stack-name stack3 \
    --capabilities CAPABILITY_IAM \
    --region us-west-2 \
    --profile default \
    --parameter-overrides Parameter1=Value1 Parameter2=Value2 \
    --tags Key1=Value1 Key2=Value2

# Deploy the fourth CloudFormation template
aws cloudformation deploy \
    --template-file "$TEMPLATE_DIR/template4.yaml" \
    --stack-name stack4 \
    --capabilities CAPABILITY_IAM \
    --region us-west-2 \
    --profile default \
    --parameter-overrides Parameter1=Value1 Parameter2=Value2 \
    --tags Key1=Value1 Key2=Value2
