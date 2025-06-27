# hello-spring-boot-aws-secrets
A Spring Boot example application demonstrating how to populate Spring configuration from AWS Secrets Manager and Parameter Store.

# Setup

## Prerequisites
- install docker, awscli and jq if not installed
```bash
brew install awscli
```

## Configuration properties
- create env files with configuration properties using `UPPER_SNAKE_CASE` naming conventions
    - `./env/secrets.env`
```properties
APP_USERNAME=sa
APP_PASSWORD=pwd
```
  - `./env/params.env`
```properties
MANAGEMENT_ENDPOINTS_WEB_BASE-PATH=/management
MANAGEMENT_ENDPOINTS_WEB_EXPOSURE_INCLUDE=env
LOGGING_LEVEL_CANE_BROTHERS=DEBUG
```
 
  use comments if necessary on a new line only 

## Running
- start LocalStack and the application with Docker Compose 
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