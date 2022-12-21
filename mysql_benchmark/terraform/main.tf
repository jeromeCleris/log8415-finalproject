# LOG8415E - final project
# main.tf
# Terraform configuration relative to core providers and terraform initialization


terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

# Selecting the region as per the assignment requirements
provider "aws" {
  region = "us-east-1"
}