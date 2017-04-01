#!/usr/bin/env python
from __future__ import print_function
import boto3
from datetime import datetime
import json
import logging
import sys
import click
from pprint import pprint


logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.getLogger('botocore').setLevel(logging.WARNING)
ch = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(ch)

TOPIC_APP_DEPLOY_ARN='arn:aws:sns:us-east-1:123456789012:deploy-ecs'
CROSS_ACCOUNT_ROLE='arn:aws:iam::123456789012:role/crossaccount-cicd-ecs'
APP_DEPLOY='deploy'
APP_ROLLBACK='rollback'
AWS_REGION='us-east-1'

@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    pass


@cli.command()
@click.argument('docker_image')
@click.argument('docker_image_tag')
@click.argument('cluster_name')
def deploy(docker_image=None, docker_image_tag='latest', cluster_name=None):
    message={
        'docker-image':docker_image,
        'docker-image-tag': docker_image_tag,
        'cluster-name': cluster_name,
        'deploy-type':APP_DEPLOY
    }
    client_sns=assume_role()
    response = client_sns.publish(
        TargetArn=TOPIC_APP_DEPLOY_ARN,
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure='json'
    )
    logger.info(response)


@cli.command()
@click.argument('revision')
@click.argument('cluster_name')
def rollback(cluster_name=None,revision=None):
    message={
            'revision': revision,
            'cluster-name': cluster_name,
            'deploy-type':APP_ROLLBACK
        }
    client_sns=assume_role()
    response = client_sns.publish(
            TargetArn=TOPIC_APP_DEPLOY_ARN,
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json'
        )
    logger.info(response)


def assume_role():

    # create an STS client object that represents a live connection to the
    # STS service
    session = boto3.session.Session(profile_name='cicd', region_name=AWS_REGION)
    sts_client = session.client('sts')
    # Call the assume_role method of the STSConnection object and pass the role
    # ARN and a role session name.
    assumedRoleObject = sts_client.assume_role(
        RoleArn=CROSS_ACCOUNT_ROLE,
        RoleSessionName="CrossAccountRole"
    )

    # From the response that contains the assumed role, get the temporary
    # credentials that can be used to make subsequent API calls
    credentials = assumedRoleObject['Credentials']

    session=boto3.Session(
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
        region_name=AWS_REGION
    )
    client_sns = session.client('sns')
    return client_sns


if __name__ == "__main__":
   cli=cli()
    #app_deploy(docker_image='flask',docker_image_tag='20170105.232110', cluster_name='ecs-demo')
    #app_rollback(revision=10, cluster_name='ecs-demo')
    #assume_role()
