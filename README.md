# hello-spring-boot-aws-secrets
A Spring Boot example application demonstrating how to populate Spring configuration from AWS Secrets Manager and Parameter Store.

# setup
- install awscli if not installed
```bash
brew install awscli
```
- create env files with necessary properties
    - `./env/secrets.env`
    - `./env/params.env`
 
  use comments if necessary on a new line only 
- run the application
```bash
docker compose up
```
- verify if secrets were successfully created in LocalStack
```bash
alias awsls='aws --endpoint-url https://localhost.localstack.cloud:4566 --region us-east-1'
awsls secretsmanager list-secrets | jq
```
- verify parameters
```bash
awsls ssm describe-parameters | jq
awsls ssm get-parameters-by-path --path /config/hello-app/ | jq
```