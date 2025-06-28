# hello-spring-boot-aws-secrets
A Spring Boot example application demonstrating how to populate Spring configuration from AWS Secrets Manager and Parameter Store.

![Gradle Build](https://github.com/webcane/hello-spring-boot-aws-secrets/workflows/Gradle%20Build/badge.svg)

# Key Features
- Separates application properties into secrets and parameters
- Uses AWS Secrets Manager and AWS Parameter Store
- Supports .env file for both LocalStack and the application
- Avoids using `application.properties` or `application.yml` entirely
- Useful for CI/CD – no need to provide a large number of environment variables

# Setup

## Prerequisites
- install docker, awscli and jq if not installed
```bash
brew install awscli
```

## Configuration properties
- rename `default.env` to `.env`
```properties
SPRING_CONFIG_IMPORT=aws-secretsmanager:/secret/hello-app,aws-parameterstore:/config/hello-app/
SPRING_APPLICATION_NAME=hello-app
SPRING_CLOUD_AWS_ENDPOINT=http://localstack:4566
SPRING_CLOUD_AWS_REGION_STATIC=us-east-1
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test
```
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