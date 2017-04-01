#!/bin/bash -x
account_number=123456789012
lambda_function_name="$1"
lambda_function_description="deploy a new verion of service on ECS"

package=${lambda_function_name}.zip

if [[ ! -z "$lambda_function_name" ]]
then
    aws lambda create-function \
    --function-name $lambda_function_name \
    --zip-file fileb://$package \
    --description "$lambda_function_description" \
    --role arn:aws:iam::$account_number:role/ecs-deploy-lambda \
    --handler lambda_deploy_ecs.lambda_handler \
    --runtime python2.7 \
    --timeout 30 \
    --memory-size 200
    if [[ $? -eq 0 ]]
    then
        echo "successfully create lambda functions: $lambda_function_name"
    else
        echo "error failed to create lambda functions: $lambda_function_name"
    fi
fi
