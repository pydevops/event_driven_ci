#!/usr/bin/env python
from __future__ import print_function
import boto3
import ast
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ECS client
ecs_client = boto3.client( 'ecs')

# configure the service
# due to the sprint scope, the following code is for a single service only to avoid complexity
# passing the service ARN from the CICD all the way the lambda function call.
account_number= '123456789012'
family = 'flask-service'
container_name = 'flask-service'
docker_repo = 'pythonrocks'
APP_DOCKER_IMAGE = 'flask'
APP_DEPLOY='deploy'
APP_ROLLBACK='rollback'

def lambda_handler(event, context):
    message = event['Records'][0]['Sns']['Message']
    logger.info("From SNS: {}".format(message))
    message_dict = ast.literal_eval(message)
    deploy_type=message_dict['deploy-type']

   # filter by the docker image name by this application
    if deploy_type == APP_DEPLOY:
            docker_image = message_dict['docker-image']
            if docker_image == APP_DOCKER_IMAGE:
                cluster_name = message_dict['cluster-name']
                docker_image_tag = message_dict['docker-image-tag']
                deploy(docker_image_tag=docker_image_tag, docker_image=docker_image, cluster_name=cluster_name)
    elif deploy_type == APP_ROLLBACK:
            cluster_name = message_dict['cluster-name']
            revision = message_dict['revision']
            rollback(cluster_name=cluster_name, revision=revision)
    else:
        logger.info('Unknow deploy_type:{}'.format(deploy_type))
    return message

def deploy(docker_image_tag='latest', docker_image=None, cluster_name=None):

    # look up the task name
    task_name='arn:aws:ecs:us-east-1:{}:task-definition/{}'.format(account_number,family)

    # look up the service name
    response = ecs_client.list_services(
        cluster=cluster_name,
        maxResults=1
        )
    service_name=response['serviceArns'][0]

   # Create a task definition
    response = ecs_client.register_task_definition(
        family=family,
        containerDefinitions=[
            {
            "name": container_name,
            "image": "{}/{}:{}".format(docker_repo,docker_image,docker_image_tag),
            "essential": True,
            "portMappings": [
                {
                "containerPort": 80,
                "hostPort": 0
                }
            ],
            "memory": 300,
            "cpu": 10,
            "environment": [
            {
              "name": "POWERED_BY",
              "value": "ecs"
            }
            ]
            }
            ]
        )


    response = ecs_client.update_service(
        cluster=cluster_name,
        service=service_name,
        taskDefinition=task_name,
        desiredCount=1
    )
   # pprint(response)

def rollback(revision=None,cluster_name=None):

   # figure out  the task name
    task_name='arn:aws:ecs:us-east-1:{}:task-definition/{}:{}'.format(account_number,family,revision)

    # look up the service name
    response = ecs_client.list_services(
        cluster=cluster_name,
        maxResults=1
        )
    service_name=response['serviceArns'][0]

    response = ecs_client.update_service(
        cluster=cluster_name,
        service=service_name,
        taskDefinition=task_name,
        desiredCount=1
    )
   # pprint(response)

if __name__ == "__main__":
    deploy(docker_image_tag='20170105.232110', docker_image='flask', cluster_name='ecs-demo')
   #rollback(cluster_name='ecs-demo',revision=8)
