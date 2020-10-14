# Fotower Gallery

Fotower Gallery is a place where users can store and organise images.

This project is part of a learning experience into [AWS infrastructure](https://aws.amazon.com/) and the [Serverless Framework](https://www.serverless.com/). For now, the focus is to develop and host the backend of this platform. 

## Contents

- [Getting Started](#getting-started)
- [Backend-as-a-Service: AWS/Serverless](#backend-as-a-service-aws-/-serverless)
- [Deployment](#deployment)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Getting Started

### Prerequisites

Setup `aws cli` by following the steps in the [AWS documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html). Setup `serverless` by following the steps in the [Serverless documentation](https://www.serverless.com/framework/docs/getting-started/).

Ensure that **Python3.7** is installed. This can be obtained from the [official Python website](https://www.python.org/downloads/).

Finally, verify all required installations by executing the following commands:

```script
aws --version
serverless --version
python3.7 --version
```

### Configuration

Configuring AWS CLI involves first creating a *user* through the [Identity and Access Management (IAM)](https://console.aws.amazon.com/iam) with **Programmatic access**, which provides an *access key ID* and a *secret access key* for various development tools, including AWS CLI.

> NOTE: The *secret access key* is only visible right after user creation, so make sure to save it.

Execute the following command on your terminal configure and follow the prompts:
```script
aws configure
```

This will create a folder named `.aws` in your *home directory* containing your configuration and credentials. Serverless uses these files when interacting with AWS.

### Python Virtual Environment

This step is not required to deploy the serverless application, but it provides virtual development environment where `boto3` (and any other Python package) can be installed without affecting your global installation. To do this, navigate to `services/` and execute the following commands:

```script
pip3.7 install virtualenv
python3.7 -m virtualenv -p python3.7 env
source env/bin/activate
pip install -r requirements.txt
```

> *Remember to exit the virtual environment by executing the command: `deactivate`.*

### Template

*NOTE: This section is not required to deploy this project, however, it's just here for completeness.*

A template project can be created by simply executing the following command on the folder you want to set as the root of your serverless application. You can specify what template to use depending on what programming language you want to use, check out the full list of [available templates](https://www.serverless.com/framework/docs/providers/aws/cli-reference/create#available-templates).

```script
serverless create --template <template-name>
```

> NOTE: The `serverless` and `sls` commands can be used interchangably.

A dialog will appear asking you if you want to create a new project; enter `Y` and follow the prompts.

## Backend-as-a-Service: AWS / Serverless

AWS is a cloud platform consisting of a multitude of individual services targeting different usages (e.g. networking, compute, analytics, storage, etc.). Even though AWS has a user friendly console that allows users to access all these services, I will use the Serverless Framework to access all these services with in a *programmatic* way.

The [`serverless.yml`](services/serverless.yml) file contains all the configuration related to the way the code is deployed to all the relevant services.

> For reference, check out this [sample `serverless.yml` file](https://www.serverless.com/framework/docs/providers/aws/guide/serverless.yml/) containing all the possible settings that can be tweaked.

Serverless takes care of creating API Gateway resources, and linking them to a corresponding **Lambda-proxy function**, defined under  `functions` in the `serverless.yml` file.

[**Boto3**](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) is the AWS SDK for Python and it provides with low-level access to various AWS services.

### Tech Stack

[Lambda](https://aws.amazon.com/lambda/) functions are at the core of our tech stack. The following Amazon web services will be directly used:

* [API Gateway](https://aws.amazon.com/api-gateway/): through a **lambda-proxy** integration (recommended by Serverless) the request processing and response formatting is conducted by the lambda function. This gives us direct control over the REST API. For more information, checkout the [API Gateway integration documentation](https://www.serverless.com/framework/docs/providers/aws/events/apigateway/).
* [DynamoDB](https://aws.amazon.com/dynamodb/): is being used to store picture metadata, as well as user information. The table configuration is done as a *service* in the `serverless.yml` file.
* [Cognito](https://aws.amazon.com/cognito/): is a user management system that allows us to restrict certain endpoints to authenticated users.
* [S3](https://aws.amazon.com/s3/): offers scalable storage in buckets, this will be used to store the *image* part of a *picture* object (i.e. the actual `.png` or `.jpg` file).

### Folder Structure

The serverless code resides in the **services/** directory of the repository. This folder contains the following important files:
- [**serverless.yml**](services/serverless.yml) - This file is at the centre of a Serverless application. It contains all the configuration related to the way the code is deployed to all the relevant Amazon web services.
- [**apis/**](services/apis) - Contains `.py` files defining API handlers in the form of Lambda functions.

Looking in more depth at **apis/**:

```
apis
├── [feed]
│   ├── (feed.serverless.yml)
│   ├── fetch_feed.py
│   └── fetch_user_wall.py
├── [pictures]
│   ├── fetch_picture.py
│   ├── modify_picture.py
│   ├── (pictures.serverless.yml)
│   ├── remove_picture.py
│   └── upload_picture.py
└── [users]
    ├── create_user.py
    ├── delete_user.py
    ├── fetch_user.py
    ├── update_user.py
    └── (users.serverless.yml)
```

- The folders in square brackets represent the 3 major *API resources*, all other resources fall under one of these three.
- The `*.serverless.yml` files in round brackets contain the serverless definitions of the functions in the same folder as them. These get imported to the main `serverless.yml` file. *NOTE: All the file paths in these files are relative to the  `serverless.yml` file*

## Deployment

Once `aws` has been configured, you can deploy your serverless application using the following command:

```script
sls deploy
```

> NOTE: The `serverless` and `sls` commands can be used interchangably.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

- Thanks to [Alex DeBrie](https://www.serverless.com/author/alexdebrie) for a quick guide on how to [Build a Python REST API with Serverless, Lambda, and DynamoDB](https://www.serverless.com/blog/flask-python-rest-api-serverless-lambda-dynamodb).
- Thanks to [Serverless Stack](https://serverless-stack.com/) for a guide on how to [organize serverless projects](https://serverless-stack.com/chapters/organizing-serverless-projects.html).
