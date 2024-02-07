import boto3
import json
import os
import json
import subprocess
import pprint

def CreateStack(stack_name, template_file, parameters, aws_profile, aws_region, resource_locators):
    # Create the CloudFormation stack with parameters
    print(f"Creating {stack_name}.")
    client = boto3.client('cloudformation', region_name=aws_region)
    os.environ['AWS_PROFILE'] = aws_profile
    response = client.create_stack(
        StackName=stack_name,
        TemplateBody=open(template_file).read(),
        Capabilities=['CAPABILITY_NAMED_IAM'],
        Parameters=parameters
    )

    # Wait for stack creation to complete
    print("Waiting for stack creation to complete...")
    client.get_waiter('stack_create_complete').wait(StackName=stack_name)

    # Check stack creation status
    response = client.describe_stacks(StackName=stack_name)
    stack_status = response['Stacks'][0]['StackStatus']

    if stack_status == "CREATE_COMPLETE":
        print("Stack creation completed successfully.")

        if 'Outputs' in response['Stacks'][0]:
            stack_outputs = response['Stacks'][0]['Outputs']
        else:
            stack_outputs = []
        for output in stack_outputs:
            resource_locators[output['ExportName']] = output['OutputValue']

        print("Resource locators:")
        pprint.pprint(resource_locators)
    else:
        print(f"Stack creation failed. Status: {stack_status}")

    return resource_locators

def CreateSourceStack(config_data, resource_locators):
    # Configuration
    AWS_PROFILE = "default"
    AWS_REGION = "us-east-1"
    STACK_NAME = f"{config_data.get('AppName')}-source-stack"
    TEMPLATE_FILE = "../../Pipelines/source.yml"

    # Parameters
    AppName = config_data.get('AppName')
    ProjectName = config_data.get('ProjectName')
    Environment = config_data.get('Environment')

    PARAMETERS = [
        {"ParameterKey": "AppName", "ParameterValue": AppName},
        {"ParameterKey": "ProjectName", "ParameterValue": ProjectName},
        {"ParameterKey": "Environment", "ParameterValue": Environment}
    ]

    return CreateStack(STACK_NAME, TEMPLATE_FILE, PARAMETERS, AWS_PROFILE, AWS_REGION, resource_locators)

def SyncRepository(github_repo_url, codecommit_repo_url):
    subprocess.run(["git", "pull", github_repo_url, "main"])
    subprocess.run(["git", "push", codecommit_repo_url, "main"])

    print("GitHub to CodeCommit sync completed.")

def CreateNetworkStack(config_data, resource_locators):
    # Configuration
    AWS_PROFILE = "default"
    AWS_REGION = "us-east-1"
    STACK_NAME = f"{config_data.get('AppName')}-network-stack"
    TEMPLATE_FILE = "../../Config/network.yml"

    # Parameters
    AppName = config_data.get('AppName')
    ProjectName = config_data.get('ProjectName')
    Environment = config_data.get('Environment')
    IngressCIDR = f'{config_data.get('IngressIP')}/32'

    PARAMETERS = [
        {"ParameterKey": "AppName", "ParameterValue": AppName},
        {"ParameterKey": "ProjectName", "ParameterValue": ProjectName},
        {"ParameterKey": "Environment", "ParameterValue": Environment},
        {"ParameterKey": "IngressCIDR", "ParameterValue": IngressCIDR}
    ]

    return CreateStack(STACK_NAME, TEMPLATE_FILE, PARAMETERS, AWS_PROFILE, AWS_REGION, resource_locators)

def CreateServiceRolesStack(config_data, resource_locators):
    # Configuration
    AWS_PROFILE = "default"
    AWS_REGION = "us-east-1"
    STACK_NAME = f"{config_data.get('AppName')}-service-role-stack"
    TEMPLATE_FILE = "../../Config/serviceroles.yml"

    # Parameters
    AppName = config_data.get('AppName')
    ProjectName = config_data.get('ProjectName')
    Environment = config_data.get('Environment')

    PARAMETERS = [
        {"ParameterKey": "AppName", "ParameterValue": AppName},
        {"ParameterKey": "ProjectName", "ParameterValue": ProjectName},
        {"ParameterKey": "Environment", "ParameterValue": Environment}
    ]

    return CreateStack(STACK_NAME, TEMPLATE_FILE, PARAMETERS, AWS_PROFILE, AWS_REGION, resource_locators)

def CreateAPIBuildStack(config_data, resource_locators):
    # Configuration
    AWS_PROFILE = "default"
    AWS_REGION = "us-east-1"
    STACK_NAME = f"{config_data.get('AppName')}-api-build-stack"
    TEMPLATE_FILE = "../../Pipelines/build.yml"

    # Parameters
    AppName = f"{config_data.get('AppName')}-api"
    ProjectName = config_data.get('ProjectName')
    Environment = config_data.get('Environment')
        
    CodeCommitRepo = resource_locators.get(f'{AppName}-cc-repository-url')
    DockerHubUsername = input("Enter DockerHub username: ")
    DockerHubPassword = input("Enter DockerHub password: ")
    CodeBuildServiceRole = resource_locators.get(f'{config_data.get('AppName')}-codebuild-service-role-arn')
    ECRRepositoryURL = resource_locators.get(f'{AppName}-ecr-repository-url')
    ECRRepositoryName = ECRRepositoryURL.split("/")[-1]

    PARAMETERS = [
        {"ParameterKey": "AppName", "ParameterValue": AppName},
        {"ParameterKey": "ProjectName", "ParameterValue": ProjectName},
        {"ParameterKey": "Environment", "ParameterValue": Environment},
        {"ParameterKey": "AWSRegion", "ParameterValue": AWS_REGION},
        {"ParameterKey": "CodeCommitRepo", "ParameterValue": CodeCommitRepo},
        {"ParameterKey": "DockerHubUsername", "ParameterValue": DockerHubUsername},
        {"ParameterKey": "DockerHubPassword", "ParameterValue": DockerHubPassword},
        {"ParameterKey": "CodeBuildServiceRole", "ParameterValue": CodeBuildServiceRole},
        {"ParameterKey": "ECRRepositoryURL", "ParameterValue": ECRRepositoryURL},
        {"ParameterKey": "ECRRepositoryName", "ParameterValue": ECRRepositoryName}
    ]

    return CreateStack(STACK_NAME, TEMPLATE_FILE, PARAMETERS, AWS_PROFILE, AWS_REGION, resource_locators)

def CreateUIBuildStack(config_data, resource_locators):
    # Configuration
    AWS_PROFILE = "default"
    AWS_REGION = "us-east-1"
    STACK_NAME = f"{config_data.get('AppName')}-ui-build-stack"
    TEMPLATE_FILE = "../../Pipelines/build.yml"

    # Parameters
    AppName = f"{config_data.get('AppName')}-ui"
    ProjectName = config_data.get('ProjectName')
    Environment = config_data.get('Environment')
        
    CodeCommitRepo = resource_locators.get(f'{AppName}-cc-repository-url')
    DockerHubUsername = input("Enter DockerHub username: ")
    DockerHubPassword = input("Enter DockerHub password: ")
    CodeBuildServiceRole = resource_locators.get(f'{config_data.get('AppName')}-codebuild-service-role-arn')
    ECRRepositoryURL = resource_locators.get(f'{AppName}-ecr-repository-url')
    ECRRepositoryName = ECRRepositoryURL.split("/")[-1]

    PARAMETERS = [
        {"ParameterKey": "AppName", "ParameterValue": AppName},
        {"ParameterKey": "ProjectName", "ParameterValue": ProjectName},
        {"ParameterKey": "Environment", "ParameterValue": Environment},
        {"ParameterKey": "AWSRegion", "ParameterValue": AWS_REGION},
        {"ParameterKey": "CodeCommitRepo", "ParameterValue": CodeCommitRepo},
        {"ParameterKey": "DockerHubUsername", "ParameterValue": DockerHubUsername},
        {"ParameterKey": "DockerHubPassword", "ParameterValue": DockerHubPassword},
        {"ParameterKey": "CodeBuildServiceRole", "ParameterValue": CodeBuildServiceRole},
        {"ParameterKey": "ECRRepositoryURL", "ParameterValue": ECRRepositoryURL},
        {"ParameterKey": "ECRRepositoryName", "ParameterValue": ECRRepositoryName}
    ]

    return CreateStack(STACK_NAME, TEMPLATE_FILE, PARAMETERS, AWS_PROFILE, AWS_REGION, resource_locators)

def CreateStacks():
    # Read config.json file
    with open('config.json') as config_file:
        config_data = json.load(config_file)

    app_name = config_data.get('AppName')

    # Create CodeCommit and ECR Repositories
    resource_locators = {}
    resource_locators = CreateSourceStack(config_data, resource_locators)

    # Sync GitHub repositories to CodeCommit
    SyncRepository(config_data.get('APIGitHubURL'), resource_locators.get(f'{app_name}-api-cc-repository-url'))
    SyncRepository(config_data.get('UIGitHubURL'), resource_locators.get(f'{app_name}-ui-cc-repository-url'))

    # Create Network Resources
    resource_locators = CreateNetworkStack(config_data, resource_locators)

    # Create Service Roles
    resource_locators = CreateServiceRolesStack(config_data, resource_locators)

    # Create Build Stacks
    resource_locators = CreateAPIBuildStack(config_data, resource_locators)
    resource_locators = CreateUIBuildStack(config_data, resource_locators)

    # Run Builds

    # Create EC2 Server Stacks

    # Create Fargate Stacks

    # Create Pipeline Stacks

    # Celebrate victory?

CreateStacks()