FUNCTION = app_deploy_ecs
PACKAGE=$(FUNCTION).zip
REGION = us-east-1
TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:deploy-ecs
LAMBDA_ARN=arn:aws:lambda:us-east-1:123456789012:function:app_deploy_ecs
SUB_ARN:=$(shell aws sns list-subscriptions-by-topic --topic-arn arn:aws:sns:us-east-1:123456789012:deploy-ecs --query "Subscriptions[?Protocol=='lambda'].SubscriptionArn" --output text)

.phony: clean

clean:
	rm -f -r $(FUNCTION)/
	rm -f $(PACKAGE)
	rm -f -r site-packages

build: clean
	zip -r $(FUNCTION).zip . -x "*.git*" "tests/*"

create: build
	./create_lambda_func.sh $(FUNCTION)
	aws sns subscribe --topic-arn $(TOPIC_ARN) --protocol lambda --notification-endpoint $(LAMBDA_ARN)
update:
	aws lambda update-function-code \
		--function-name $(FUNCTION) \
		--zip-file fileb://$(PACKAGE) \
		--publish \

delete:
	aws lambda delete-function --function-name $(FUNCTION)
	aws sns unsubscribe --subscription-arn $(SUB_ARN)
list:
	aws sns list-subscriptions-by-topic --topic-arn $(TOPIC_ARN)
