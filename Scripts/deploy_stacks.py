import boto3
import json
import os
import json
import time
import pprint
import getpass

def CreateStack(AWSProfile, AWSRegion, Parameters, ResourceLocators, StackName, TemplateFile):
    # Create the CloudFormation stack with parameters
    print(f"Creating {StackName}.")
    client = boto3.client('cloudformation', region_name=AWSRegion)
    os.environ['AWS_PROFILE'] = AWSProfile
    response = client.create_stack(
        StackName=StackName,
        TemplateBody=open(TemplateFile).read(),
        Capabilities=['CAPABILITY_NAMED_IAM'],
        Parameters=Parameters
    )

    # Wait for stack creation to complete
    print("Waiting for stack creation to complete...")
    client.get_waiter('stack_create_complete').wait(StackName=StackName)

    # Check stack creation status
    response = client.describe_stacks(StackName=StackName)
    stack_status = response['Stacks'][0]['StackStatus']

    if stack_status == "CREATE_COMPLETE":
        print("Stack creation completed successfully.")

        if 'Outputs' in response['Stacks'][0]:
            stack_outputs = response['Stacks'][0]['Outputs']
        else:
            stack_outputs = []
        for output in stack_outputs:
            ResourceLocators[output['ExportName']] = output['OutputValue']

        print("Resource locators:")
        pprint.pprint(ResourceLocators)
    else:
        print(f"Stack creation failed. Status: {stack_status}")

    return ResourceLocators

def GetSecretByARN(SecretARN):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=SecretARN)
    secret_value = response['SecretString']
    return secret_value

def PopulateCodeCommitRepository(CodeCommitRepoUrl, GithubRepoURL):
    # Clone GitHub repository
    import subprocess
    subprocess.run(["git", "clone", GithubRepoURL])

    # Change directory to the cloned repository
    import os
    RepoName = os.path.basename(GithubRepoURL).split('.')[0]
    os.chdir(RepoName)

    # Push to CodeCommit repository
    subprocess.run(["git", "push", CodeCommitRepoUrl, "--all"])

    # Navigate back to the parent directory
    os.chdir('..')

    # Delete the local repository
    try:
        import shutil
        shutil.rmtree(RepoName)
    except:
        print(f"Failed to delete the local repository: {RepoName}")

    print("GitHub to CodeCommit sync completed.")

def RunCodeBuildProject(CodebuildProjectARN):
    # Run CodeBuild project
    client = boto3.client('codebuild')
    response = client.start_build(projectName=CodebuildProjectARN)
    build_id = response['build']['id']
    print(f"CodeBuild project {CodebuildProjectARN.split('/')[-1]} started.")
    print(f"Build ID: {build_id}")

    # Wait for build to complete (capped at five minutes)
    print("Waiting for build to complete...")
    counter = 0
    while counter < 60:
      time.sleep(5)
      counter = counter + 1
      theBuild = client.batch_get_builds(ids=[build_id])
      buildStatus = theBuild['builds'][0]['buildStatus']

      print(f"Build status: {buildStatus}")
      if buildStatus == 'SUCCEEDED':
        time_to_build = theBuild['builds'][0]['endTime'] - theBuild['builds'][0]['startTime']
        time_to_build = time_to_build.total_seconds()
        print(f"Build completed successfully in {time_to_build} seconds.")
        break
      elif buildStatus == 'FAILED' or buildStatus == 'FAULT' or buildStatus == 'STOPPED' or buildStatus == 'TIMED_OUT':
        break

def CreateSecretsStack(ConfigData, ResourceLocators):
    # From Config
    AppName = ConfigData.get('AppName')
    AWSProfile = ConfigData.get('AWSProfile')
    AWSRegion = ConfigData.get('AWSRegion')
    Environment = ConfigData.get('Environment')
    ProjectName = ConfigData.get('ProjectName')
    StackName = f"{ConfigData.get('AppName')}-secrets-stack"
    TemplateFile = ConfigData.get('TemplateFilePaths').get('Secrets')

    # From User Input
    DockerUsername = input("Enter DockerHub username: ")
    # DockerPassword = input("Enter DockerHub password: ")
    DockerPassword = getpass.getpass("Enter DockerHub password: ")
    DatabaseUsername = input("Enter database username: ")
    # DatabasePassword = input("Enter database password: ")
    DatabasePassword = getpass.getpass("Enter database password: ")

    Parameters = [
        {"ParameterKey": "AppName", "ParameterValue": AppName},
        {"ParameterKey": "DatabaseUsername", "ParameterValue": DatabaseUsername},
        {"ParameterKey": "DatabasePassword", "ParameterValue": DatabasePassword},
        {"ParameterKey": "DockerHubUsername", "ParameterValue": DockerUsername},
        {"ParameterKey": "DockerHubPassword", "ParameterValue": DockerPassword},
        {"ParameterKey": "Environment", "ParameterValue": Environment},
        {"ParameterKey": "ProjectName", "ParameterValue": ProjectName}
    ]

    return CreateStack(AWSProfile, AWSRegion, Parameters, ResourceLocators, StackName, TemplateFile)

def CreateSourceStack(ConfigData, ResourceLocators):
    # From Config
    AppName = ConfigData.get('AppName')
    AWSProfile = ConfigData.get('AWSProfile')
    AWSRegion = ConfigData.get('AWSRegion')
    Environment = ConfigData.get('Environment')
    ProjectName = ConfigData.get('ProjectName')
    StackName = f"{ConfigData.get('AppName')}-source-stack"
    TemplateFile = ConfigData.get('TemplateFilePaths').get('Source')

    Parameters = [
        {"ParameterKey": "AppName", "ParameterValue": AppName},
        {"ParameterKey": "Environment", "ParameterValue": Environment},
        {"ParameterKey": "ProjectName", "ParameterValue": ProjectName}
    ]

    return CreateStack(AWSProfile, AWSRegion, Parameters, ResourceLocators, StackName, TemplateFile)

def CreateNetworkStack(ConfigData, ResourceLocators):
    # From Config
    AppName = ConfigData.get('AppName')
    AWSProfile = ConfigData.get('AWSProfile')
    AWSRegion = ConfigData.get('AWSRegion')
    Environment = ConfigData.get('Environment')
    IngressCIDR = f"{ConfigData.get('IngressIP')}/32"
    ProjectName = ConfigData.get('ProjectName')
    StackName = f"{ConfigData.get('AppName')}-network-stack"
    TemplateFile = ConfigData.get('TemplateFilePaths').get('Network')

    Parameters = [
        {"ParameterKey": "AppName", "ParameterValue": AppName},
        {"ParameterKey": "Environment", "ParameterValue": Environment},
        {"ParameterKey": "IngressCIDR", "ParameterValue": IngressCIDR},
        {"ParameterKey": "ProjectName", "ParameterValue": ProjectName}
    ]

    return CreateStack(AWSProfile, AWSRegion, Parameters, ResourceLocators, StackName, TemplateFile)

def CreateServiceRolesStack(ConfigData, ResourceLocators):
    # From Config
    AppName = ConfigData.get('AppName')
    AWSProfile = ConfigData.get('AWSProfile')
    AWSRegion = ConfigData.get('AWSRegion')
    Environment = ConfigData.get('Environment')
    ProjectName = ConfigData.get('ProjectName')
    StackName = f"{ConfigData.get('AppName')}-service-role-stack"
    TemplateFile = ConfigData.get('TemplateFilePaths').get('ServiceRoles')

    Parameters = [
        {"ParameterKey": "AppName", "ParameterValue": AppName},
        {"ParameterKey": "Environment", "ParameterValue": Environment},
        {"ParameterKey": "ProjectName", "ParameterValue": ProjectName}
    ]

    return CreateStack(AWSProfile, AWSRegion, Parameters, ResourceLocators, StackName, TemplateFile)

def CreateAPIBuildStack(ConfigData, ResourceLocators):
    # From Config
    AppName = f"{ConfigData.get('AppName')}-api"
    AWSProfile = ConfigData.get('AWSProfile')
    AWSRegion = ConfigData.get('AWSRegion')
    Environment = ConfigData.get('Environment')
    ProjectName = ConfigData.get('ProjectName')
    StackName = f"{ConfigData.get('AppName')}-api-build-stack"
    TemplateFile = ConfigData.get('TemplateFilePaths').get('Build')

    # From Resource Locators
    CodeBuildServiceRole = ResourceLocators.get(f"{ConfigData.get('AppName')}-codebuild-service-role-arn")
    CodeCommitRepo = ResourceLocators.get(f"{AppName}-cc-repository-url")
    ECRRepositoryURL = ResourceLocators.get(f"{AppName}-ecr-repository-url")
    ECRRepositoryName = ECRRepositoryURL.split("/")[-1]

    # From Secrets Manager
    DockerSecretARN = ResourceLocators.get(f"{ConfigData.get('AppName')}-docker-secret-arn")
    SecretValue = GetSecretByARN(DockerSecretARN)
    SecretValue = json.loads(SecretValue)
    DockerHubUsername = SecretValue.get('username')
    DockerHubPassword = SecretValue.get('password')

    Parameters = [
        {"ParameterKey": "AppName", "ParameterValue": AppName},
        {"ParameterKey": "ProjectName", "ParameterValue": ProjectName},
        {"ParameterKey": "Environment", "ParameterValue": Environment},
        {"ParameterKey": "AWSRegion", "ParameterValue": AWSRegion},
        {"ParameterKey": "CodeCommitRepo", "ParameterValue": CodeCommitRepo},
        {"ParameterKey": "DockerHubUsername", "ParameterValue": DockerHubUsername},
        {"ParameterKey": "DockerHubPassword", "ParameterValue": DockerHubPassword},
        {"ParameterKey": "CodeBuildServiceRole", "ParameterValue": CodeBuildServiceRole},
        {"ParameterKey": "ECRRepositoryURL", "ParameterValue": ECRRepositoryURL},
        {"ParameterKey": "ECRRepositoryName", "ParameterValue": ECRRepositoryName}
    ]

    return CreateStack(AWSProfile, AWSRegion, Parameters, ResourceLocators, StackName, TemplateFile)

def CreateUIBuildStack(ConfigData, ResourceLocators):
    # From Config
    AppName = f"{ConfigData.get('AppName')}-ui"
    AWSProfile = ConfigData.get('AWSProfile')
    AWSRegion = ConfigData.get('AWSRegion')
    Environment = ConfigData.get('Environment')
    ProjectName = ConfigData.get('ProjectName')
    StackName = f"{ConfigData.get('AppName')}-ui-build-stack"
    TemplateFile = ConfigData.get('TemplateFilePaths').get('Build')

    # From Resource Locators
    CodeBuildServiceRole = ResourceLocators.get(f"{ConfigData.get('AppName')}-codebuild-service-role-arn")
    CodeCommitRepo = ResourceLocators.get(f"{AppName}-cc-repository-url")
    ECRRepositoryURL = ResourceLocators.get(f"{AppName}-ecr-repository-url")
    ECRRepositoryName = ECRRepositoryURL.split("/")[-1]

    # From Secrets Manager
    DockerSecretARN = ResourceLocators.get(f"{ConfigData.get('AppName')}-docker-secret-arn")
    SecretValue = GetSecretByARN(DockerSecretARN)
    SecretValue = json.loads(SecretValue)
    DockerHubUsername = SecretValue.get('username')
    DockerHubPassword = SecretValue.get('password')

    Parameters = [
        {"ParameterKey": "AppName", "ParameterValue": AppName},
        {"ParameterKey": "ProjectName", "ParameterValue": ProjectName},
        {"ParameterKey": "Environment", "ParameterValue": Environment},
        {"ParameterKey": "AWSRegion", "ParameterValue": AWSRegion},
        {"ParameterKey": "CodeCommitRepo", "ParameterValue": CodeCommitRepo},
        {"ParameterKey": "DockerHubUsername", "ParameterValue": DockerHubUsername},
        {"ParameterKey": "DockerHubPassword", "ParameterValue": DockerHubPassword},
        {"ParameterKey": "CodeBuildServiceRole", "ParameterValue": CodeBuildServiceRole},
        {"ParameterKey": "ECRRepositoryURL", "ParameterValue": ECRRepositoryURL},
        {"ParameterKey": "ECRRepositoryName", "ParameterValue": ECRRepositoryName}
    ]

    return CreateStack(AWSProfile, AWSRegion, Parameters, ResourceLocators, StackName, TemplateFile)

def CreateDatabaseStack(ConfigData, ResourceLocators):
    # From Config
    AMI = ConfigData.get('DebianAMI')
    AppName = ConfigData.get('AppName')
    AWSProfile = "default"
    AWSRegion = "us-east-1"
    Environment = ConfigData.get('Environment')
    ProjectName = ConfigData.get('ProjectName')
    StackName = f"{ConfigData.get('AppName')}-database-stack"
    TemplateFile = "../EC2/postgres.yml"

    # From Resource Locators
    DatabaseElasticIP = ResourceLocators.get(f"{AppName}-database-elastic-ip")
    KeypairName = ConfigData.get('KeypairName')
    SecurityGroup = ResourceLocators.get(f"{AppName}-database-security-group-id")
    SubnetId = ResourceLocators.get(f"{AppName}-database-subnet-id")

    # From Secrets Manager
    DatabaseSecretARN = ResourceLocators.get(f"{ConfigData.get('AppName')}-database-secret-arn")
    SecretValue = GetSecretByARN(DatabaseSecretARN)
    SecretValue = json.loads(SecretValue)
    DatabaseUsername = SecretValue.get('username')
    DatabasePassword = SecretValue.get('password')

    Parameters = [
        {"ParameterKey": "AppName", "ParameterValue": AppName},
        {"ParameterKey": "ProjectName", "ParameterValue": ProjectName},
        {"ParameterKey": "Environment", "ParameterValue": Environment},
        {"ParameterKey": "DatabaseElasticIP", "ParameterValue": DatabaseElasticIP},
        {"ParameterKey": "AMI", "ParameterValue": AMI},
        {"ParameterKey": "SecurityGroup", "ParameterValue": SecurityGroup},
        {"ParameterKey": "KeypairName", "ParameterValue": KeypairName},
        {"ParameterKey": "SubnetId", "ParameterValue": SubnetId},
        {"ParameterKey": "DatabaseUsername", "ParameterValue": DatabaseUsername},
        {"ParameterKey": "DatabasePassword", "ParameterValue": DatabasePassword}
    ]

    return CreateStack(AWSProfile, AWSRegion, Parameters, ResourceLocators, StackName, TemplateFile)

def CreateReverseProxyStack(ConfigData, ResourceLocators):
    # From Config
    AMI = ConfigData.get('DebianAMI')
    AppName = ConfigData.get('AppName')
    AWSProfile = ConfigData.get('AWSProfile')
    AWSRegion = ConfigData.get('AWSRegion')
    Environment = ConfigData.get('Environment')
    IngressCIDR = f"{ConfigData.get('IngressIP')}/32"
    KeypairName = ConfigData.get('KeypairName')
    ProjectName = ConfigData.get('ProjectName')
    StackName = f"{ConfigData.get('AppName')}-reverse-proxy-stack"
    TemplateFile = "../EC2/nginx.yml"

    # From Resource Locators
    APIElasticIP = ResourceLocators.get(f'{AppName}-api-elastic-ip')
    ReverseProxyElasticIP = ResourceLocators.get(f'{AppName}-reverse-proxy-elastic-ip')
    SecurityGroup = ResourceLocators.get(f'{AppName}-reverse-proxy-security-group-id')
    SubnetId = ResourceLocators.get(f'{AppName}-reverse-proxy-subnet-id')
    UIElasticIP = ResourceLocators.get(f'{AppName}-ui-elastic-ip')

    Parameters = [
        {"ParameterKey": "AMI", "ParameterValue": AMI},
        {"ParameterKey": "AppName", "ParameterValue": AppName},
        {"ParameterKey": "Environment", "ParameterValue": Environment},
        {"ParameterKey": "IngressCIDR", "ParameterValue": IngressCIDR},
        {"ParameterKey": "KeypairName", "ParameterValue": KeypairName},
        {"ParameterKey": "ProjectName", "ParameterValue": ProjectName},
        {"ParameterKey": "APIElasticIP", "ParameterValue": APIElasticIP},
        {"ParameterKey": "ReverseProxyElasticIP", "ParameterValue": ReverseProxyElasticIP},
        {"ParameterKey": "SecurityGroup", "ParameterValue": SecurityGroup},
        {"ParameterKey": "SubnetId", "ParameterValue": SubnetId},
        {"ParameterKey": "UIElasticIP", "ParameterValue": UIElasticIP},
    ]

    return CreateStack(AWSProfile, AWSRegion, Parameters, ResourceLocators, StackName, TemplateFile)

def CreateStacks():
    # Set up configuration
    with open('config.json') as ConfigFile:
        ConfigData = json.load(ConfigFile)
    AppName = ConfigData.get('AppName')
    ResourceLocators = {}

    # Create Secrets Stack
    ResourceLocators = CreateSecretsStack(ConfigData, ResourceLocators)

    # Create CodeCommit and ECR Repositories
    ResourceLocators = CreateSourceStack(ConfigData, ResourceLocators)

    # Sync GitHub repositories to CodeCommit
    PopulateCodeCommitRepository(ConfigData.get('APIGitHubURL'), ResourceLocators.get(f'{AppName}-api-cc-repository-url'))
    PopulateCodeCommitRepository(ConfigData.get('UIGitHubURL'), ResourceLocators.get(f'{AppName}-ui-cc-repository-url'))

    # Create Network Resources
    ResourceLocators = CreateNetworkStack(ConfigData, ResourceLocators)

    # Create Service Roles
    ResourceLocators = CreateServiceRolesStack(ConfigData, ResourceLocators)

    # Create Build Stacks
    ResourceLocators = CreateAPIBuildStack(ConfigData, ResourceLocators)
    ResourceLocators = CreateUIBuildStack(ConfigData, ResourceLocators)

    # Run Builds
    RunCodeBuildProject(ResourceLocators.get(f'{AppName}-api-codebuild-project-arn'))
    RunCodeBuildProject(ResourceLocators.get(f'{AppName}-ui-codebuild-project-arn'))

    # Create EC2 Server Stacks
    ResourceLocators = CreateDatabaseStack(ConfigData, ResourceLocators)

    # Create Fargate Stacks

    # Create Pipeline Stacks

    # Celebrate victory?

CreateStacks()