terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region                      = var.aws_region
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true

  endpoints {
    apigateway     = var.localstack_endpoint
    cloudwatch     = var.localstack_endpoint
    dynamodb       = var.localstack_endpoint
    iam            = var.localstack_endpoint
    lambda         = var.localstack_endpoint
    s3             = var.localstack_endpoint
    secretsmanager = var.localstack_endpoint
    ses            = var.localstack_endpoint
    sns            = var.localstack_endpoint
    sqs            = var.localstack_endpoint
    sts            = var.localstack_endpoint
  }
}
