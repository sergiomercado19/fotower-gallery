# Fotower Gallery

Fotower Gallery is a place where users can store and organise images.

This project is part of a learning experience into AWS infrastructure. For now, the focus is to develop a serverless backend for this platform. 

## Setting up AWS

### Prerequisites

Follow the steps in the [AWS documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) to setup `aws cli`.

Finally, verify the installation by executing the following command:
```script
aws --version
```

### Configuration

Configuring AWS CLI involves first creating a _user_ through the [Identity and Access Management (IAM)](https://console.aws.amazon.com/iam) with **Programmatic access**, which provides an _access key ID_ and a _secret access key_ for various development tools, including AWS CLI.

Execute the following command on your terminal configure:
```script
aws configure
```

NOTE: The _secret access key_ is only visible right after user creation, so make sure to save it.

## AWS Stack

The following Amazon web services will be used for the backend:

* API Gateway
* Lambda
* DynamoDB
* Cognito
* S3
