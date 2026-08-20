variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "localstack_endpoint" {
  type    = string
  default = "http://localhost:4566"
}

variable "project_name" {
  type    = string
  default = "content-scarcity"
}

variable "environment" {
  type    = string
  default = "local"
}
