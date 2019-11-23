remote_state {
  backend = "s3"
  config  = {
    bucket         = "${run_cmd("tf-util", "-c", "bucket")}"
    key            = "${run_cmd("tf-util", "-c", "object")}"
    dynamodb_table = "${run_cmd("tf-util", "-c", "table")}"
    region         = "${run_cmd("tf-util", "-k", "region")}"

    encrypt                   = true
    skip_bucket_accesslogging = true

    s3_bucket_tags = {
      Project     = "${run_cmd("tf-util", "-k", "app_name")}"
      Environment = "${run_cmd("tf-util", "-c", "env")}"
      Owner       = "${run_cmd("tf-util", "-k", "owner")}"
      Name        = "Terraform Remote State"
      ManagedBy   = "Terraform"
    }

    dynamodb_table_tags = {
      Project     = "${run_cmd("tf-util", "-k", "app_name")}"
      Environment = "${run_cmd("tf-util", "-c", "env")}"
      Owner       = "${run_cmd("tf-util", "-k", "owner")}"
      Name        = "Terraform Lock Table"
      ManagedBy   = "Terraform"
    }
  }
}

terraform {
  extra_arguments common_var {
    commands = get_terraform_commands_that_need_vars()
    arguments = [
      "-var-file=${get_terragrunt_dir()}/${path_relative_from_include()}/common.tfvars"
    ]
  }
}
