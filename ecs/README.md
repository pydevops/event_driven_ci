## AWS ECS Event Driven Continuous Delivery Example
Many AWS customers use separate AWS accounts (usually in conjunction with Consolidated Billing) for their development and production resources. This separation allows them to cleanly separate different types of resources and can also provide some security benefits.
Furthermore, an AWS account can be used exclusively for CICD purpose.  Jenkins, Gitlab CI can be managed under this CICD account. The Jenkins can be used to deploy different versions of applications under different AWS accounts such as DEV account in our example.

There are 2 AWS accounts in the example
1. DEV account `123456789012`
2. CICD account unspecified

### Event Publisher under CICD account
AWS security best practice whitepaper recommends starting with a minimum set of permissions and grant additional permissions as necessary.
In this case, the SNS topic publishing IAM policy is the least privilege CICD needs.  

Please set up a the cross account IAM role for publishing message under CICD account to a SNS topic under DEV account by following  [How to Use a Single IAM User to Easily Access All Your Accounts by Using the AWS CLI](https://aws.amazon.com/blogs/security/how-to-use-a-single-iam-user-to-easily-access-all-your-accounts-by-using-the-aws-cli/#more-956)

#### example code
* `app_deploy.py` provides a command line interface in Python by using STS assume role for publishing the application deploy/rollback message to the DEV account. Please note it uses `cicd` named profile for the cross account role.
* `deploy.sh` is the CLI wrapper for integrating with any CI such as Jenkins, CircleCI etc.
* `app_deploy_sns.sh` can be used to test if a SNS message can be published under CICD account to the DEV account.


### Event Subscriber under DEV account
Lambda function `lambda_deploy_ecs.py` can be used to deploy and rollback dockerized application in ECS given docker image, tag (timestamp or git commit hash), ECS cluster name.

#### example code

* `make create` creates the lambda function in the DEV account
* `make update` updates the lambda function in the DEV account
* `make delete` delete the lambda function in the DEV account
