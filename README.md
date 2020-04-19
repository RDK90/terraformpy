# GCP Terraformpy Modules

## Introduction
Terraformpy is a Python library that can replaces the Hashicorp Configuration Language (HCL) in developing Terraform configurations. Terraformpy builds a Terraform JSON configuration from Python code which can then be executed using Terraform.

## Prerequisites

Python 3.6+
Terraform 0.12+

## Installation

Clone this repository

```bash
python3 -m pip install -r requirements.txt
```

See [this](https://cloud.google.com/docs/authentication/getting-started) guide for authentication options for GCP. 

Fill in the details for the instance template that you'd like to create.

Then run Terraformpy on the main.tf.py file

```bash
terraformpy plan -out=tf.plan
``` 

Use Terraform to apply these changes from the generated plan

```bash
terraform apply "tf.plan"
```