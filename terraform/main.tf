terraform {
    # provides where to store terraform state data files which are used to keep track of metadata of resources
    backend "s3" {
    bucket = "redditstatedata"
    key    = "path/to/my/key"
    region = "us-east-1"
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
     redshift = {
      source = "brainly/redshift"
      version = "1.0.3"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = var.region
}




# S3 Bucket Setup

# contains our source data
resource "aws_s3_bucket" "source" {
  bucket = var.bucketname

  tags = {
    Name        = "chuks"
    Environment = "Dev"
  }
}




# REDSHIFT SERVERLESS SETUP

 # Fetch Redshift IAM Role for RedShift
  data "aws_iam_role" "redshift_role" {
    name = var.redshift_role
  }

 
# Create namespace, and attach redshift role
resource "aws_redshiftserverless_namespace" "example" {
  admin_username = var.username
  admin_user_password = var.password
  db_name = var.db_name
  namespace_name = var.namespace_name
  iam_roles = [data.aws_iam_role.redshift_role.arn]
  default_iam_role_arn = data.aws_iam_role.redshift_role.arn
  
}

# Create workgroup, that is publicly accessible
resource "aws_redshiftserverless_workgroup" "DWH" {
  namespace_name = aws_redshiftserverless_namespace.example.namespace_name
  workgroup_name = var.workgroup_name
  publicly_accessible = true
  security_group_ids = [var.security_group_id]
}


# connect to Redshift database using username password host,and 
provider "redshift" {
  host     = aws_redshiftserverless_workgroup.DWH.endpoint[0].address
  port     = aws_redshiftserverless_workgroup.DWH.endpoint[0].port
  username = aws_redshiftserverless_namespace.example.admin_username
  password = aws_redshiftserverless_namespace.example.admin_user_password
  database = aws_redshiftserverless_namespace.example.db_name
}

