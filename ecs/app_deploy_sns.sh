#!/bin/bash
TOPIC_ARN='arn:aws:sns:us-east-1:123456789012:deploy-ecs'
aws sns publish --topic-arn $TOPIC_ARN --message "msg from awscli"
