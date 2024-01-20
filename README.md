# Secure Note Manager CloudFormation

These CloudFormation templates aim to **deploy infrastructure and CI/CD pipelines** for a Secure Note Manager application on Amazon Web Services. This project utilizes many technologies that are listed below, and is created for **professional development** as well as a **demonstration of skill** with the technologies in use. The primary goal is to **automate complete environment deployment, minimize deployment effort, maximize consistency and mitigate risk while maintaining best practices** for application development, security, source control management, etc.

### Work in Progress Warning

This project is a work in progress. Some features may not work as intended and implementation details may change significantly.

### Technologies in Use

The following technologies and practices are targeted within this project.

* **Infrastructure as Code**: All infrastructure is created as code with AWS CloudFormation, providing automated and consistent deployments with many additional benefits that come with using source control management.
* **CI/CD Pipelines**: Stacks are included to create CI/CD Pipelines for two containerized applications, a Node.js web application as well as an Node.js Express API.
* **Container Orchestration**: Both of the Node.js applications have been containerized with Docker, providing portability, flexibility with deployment, as well as the increased efficiency achieved through virtualization.
* **Nginx Configuration**: The application is accessed through an Nginx server that is configured as a reverse proxy, providing an additional layer of security, as well as access control and logging.
* **Cybersecurity Principles**: Security is one of the top concerns with every part of this application. Great care is taken to restrict traffic to what is necessary through the use of security groups. In addition, no direct access is allowed to application infrastructure, with all inbound requests being served through the reverse proxy.

### Template Guide

Within this repository, you will find the following folders.

* **Config**: This folder contains CloudFormation templates for base configuration, primarily including resources with little to no dependencies. S3 buckets, security groups, network configuration, and IAM roles may be found here.
* **Containers**: This folder contains a CloudFormation template for an ECS Fargate Cluster as well as its accompanying services and tasks needed for running the UI and API containers.
* **Nested Stacks**: This folder contains a nested stack that will deploy all other included CloudFormation templates with one action. This is useful for quickly setting up an independent environment, for testing purposes or otherwise. *(Work in Progress!)*
* **Pipelines**: This folder contains CloudFormation templates needed for a completely automated CI/CD pipeline using CodeCommit, CodeBuild, and CodePipeline.
* **Scripts**: This folder contains supporting shell scripts that aid deployment.
* **Servers**: This folder contains CloudFormation templates for EC2 instances that host an Nginx reverse proxy server as well as a Postgresql database. Creation and configuration scripts are included with each to quickly deploy the desired server configuration.

### Known Issues & Potential Enhancements

* **Nested Stack**: The nested stack is still in development and will require further orchestration work for seamless deployment.
* **Auto-scaling**: For ease of demonstration and expedited development, auto-scaling groups have not yet been included. Auto-scaling groups provide a simple and configurable way to vertically or horizontally scale applications based on either preconfigured or user-defined metrics. They can be implemented with the reverse proxy server as well as configured within the ECS tasks to provide a more robust, resilient, and load-bearing application.

### More Information

You can learn more about the technologies and principles used in this project by visiting the following web pages.

* CloudFormation, Infrastructure as Code: [AWS Docs: Cloudformation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
* CodePipeline, CI/CD: [AWS Docs: CodePipeline](https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html)
* Containerization with Docker: [Docker Docs: Overview](https://docs.docker.com/get-started/overview/)
* Nginx: [What is NGINX?](https://www.nginx.com/resources/glossary/nginx/)
* Cybersecurity:
  * [Synopsys: Application Security](https://www.synopsys.com/glossary/what-is-application-security.html)
  * [AWS Docs: Security Groups](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html)
  * [Antisyphon: Pay What You Can Training](https://www.antisyphontraining.com/pay-what-you-can/)
