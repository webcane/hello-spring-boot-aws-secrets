import os
import json
import boto3

APP_NAME = os.getenv("APP_NAME")
DATA_DIR = os.getenv("DATA_DIR")
SECRETS_FILENAME = os.getenv("SECRETS_FILENAME")
PARAMS_FILENAME = os.getenv("PARAMS_FILENAME")
SECRETS_FILE = f"{DATA_DIR}/{SECRETS_FILENAME}"
PARAMS_FILE = f"{DATA_DIR}/{PARAMS_FILENAME}"
SECRET_NAME = f"{APP_NAME}-secrets"

AWS_DEFAULT_REGION = os.environ['AWS_DEFAULT_REGION']
AWS_ENDPOINT = os.environ['AWS_ENDPOINT']
AWS_ACCESS_KEY_ID= os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY= os.environ['AWS_SECRET_ACCESS_KEY']

secrets_client = boto3.client(
    "secretsmanager",
    region_name=AWS_DEFAULT_REGION,
    endpoint_url=AWS_ENDPOINT,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

ssm_client = boto3.client(
    "ssm",
    region_name=AWS_DEFAULT_REGION,
    endpoint_url=AWS_ENDPOINT,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


def load_env_file(filepath):
    result = {}
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return result

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            result[key.strip()] = value.strip()
    return result


def init_secrets():
    secrets = load_env_file(SECRETS_FILE)
    if not secrets:
        print("No secrets loaded.")
        return
    try:
        print(f"Creating secret '{SECRET_NAME}' in Secrets Manager...")
        secrets_client.create_secret(Name=SECRET_NAME,
            SecretString=json.dumps(secrets))
        print(f"Secret '{SECRET_NAME}' created successfully.")
    except secrets_client.exceptions.ResourceExistsException:
        print(f"Secret '{SECRET_NAME}' already exists. Skipping.")
    except botocore.exceptions.ClientError as e:
        print(f"AWS ClientError: {e.response['Error']['Message']}")
    except botocore.exceptions.BotoCoreError as e:
        print(f"BotoCoreError: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")


def init_parameters():
    params = load_env_file(PARAMS_FILE)
    if not params:
        print("No parameters loaded.")
        return
    try:
        for key, value in params.items():
            param_name = f"/config/{APP_NAME}/{key}"
            print(f"Putting parameter: {param_name} = {value}")
            ssm_client.put_parameter(Name=param_name,
                Value=value,
                Type="String",
                Overwrite=True)
    except botocore.exceptions.ClientError as e:
        print(f"AWS ClientError: {e.response['Error']['Message']}")
    except botocore.exceptions.BotoCoreError as e:
        print(f"BotoCoreError: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    print("Parameters uploaded successfully.")


def main():
    print("Initializing secrets and params in LocalStack...")
    init_secrets()
    init_parameters()


main()