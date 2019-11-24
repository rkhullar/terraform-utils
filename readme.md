## Terraform Utils

This project provides a helper command intended to be used with [terraform][terraform-github] and [terragrunt][terragrunt-github] for applications hosted on AWS. The utility is available on [pypi][pypi-link] and requires Python 3.6.1+.

One of the ways terragrunt helps keep infrastructure code DRY is by injecting the remote state configuration to the current module. The `tf-util` command generates names for the terraform state bucket, object, and lock table based on the protect structure.

``` hcl
# modules/app/main.tf
terraform {
  required_version = ">= 0.12"
  # The configuration for this backend will be filled in by Terragrunt
  backend "s3" {}
}
```

### Project Structure
If you are using terragrunt use two repositories to separate your live configuration from your modules. Here's what the tree structure for the live repo looks like. Within the root there are two files meant for [common values](data/common.tfvars) and [remote state management](data/terragrunt.hcl). The first level of folders correspond to each environment you want to create, i.e dev, qa, and prd. The nested folders represent individual constructs within an environment. The resources within a construct share the same terraform state and are managed together.
```
.
├── common.tfvars
├── dev
│   ├── app
│   │   └── terragrunt.hcl
│   ├── iam
│   │   └── terragrunt.hcl
│   └── network
│       └── terragrunt.hcl
└── terragrunt.hcl
```

### Example Usage
```
$ pip install terraform-utils
$ cd path/to/live/repo
# verifiy content of common.tfvars
$ cd dev/network
$ tf-util -c bucket
example-terraformstate-dev-company
$ tf-util -c object
app/terraform.tfstate
$ tf-util -c table
example-terraformlock-dev-company
```

### Code Quality
Run the following commands to analyze the project with sonar.
``` sh
docker run -d --name sonarqube -p 9000:9000 sonarqube
pip install coverage
nosetests --with-xunit --with-coverage --cover-xml
sonar-scanner -D project.settings=cicd/sonar-project.properties
```

[terraform-github]: https://github.com/hashicorp/terraform
[terragrunt-github]: https://github.com/gruntwork-io/terragrunt
[pypi-link]: https://pypi.org/project/terraform-utils
