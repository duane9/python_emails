# Daily Python Standard Library Email Automation

## Overview

This project automates the daily delivery of an email one item from the Python
Standard Library. The email contains the item's name, module, and a brief
description. The project uses AWS Lambda, Amazon SES, and DynamoDB to deliver
the email.

## Motivation

This project is a fork on the
[Dutch Vocabulary](https://github.com/ThReinecke/dutch_vocabulary) project. I
wanted to do something similar but with the Python Standard Library.

## Simplified Architecture

A CloudWatch Event Rule triggers a Lambda each morning at 7:00. The Lambda
retrieves all previously sent Python items from DynamoDB. It then retrieves the
new item from ChatGPT, stores it in DynamoDB, and sends them to SES. SES
delivers them to the end user's email.

![Picture of architecture](/images/architecture.jpg)

## Setup

### Prerequisites

To deploy this project, ensure the following tools and configurations are in
place:

1. **Tools Installed:**

   - Python (Tested with Python 3.13)
   - pip (Tested with pip 19.2.3)
   - Terraform (Tested with Terraform 1.10.3)
   - AWS CLI (Tested with 2.15.58)

1. **Permissions:** Your AWS CLI user must have the appropriate permissions to
   deploy the resources. Refer to the Terraform files and apply the principle of
   least privilege.

1. **Amazon SES Verified Email:** You need a verified email address in Amazon
   SES. This email must match the one used in the project. Reference:
   [Verifying Email Addresses in Amazon SES](https://docs.aws.amazon.com/ses/latest/dg/creating-identities.html#verify-email-addresses-procedure).

1. **Optional:** You can zip the Lambda deployment package manually if you like:

   - Use the provided `setup.sh` script or follow the steps in the script
     manually.
   - Alternatively, use the pre-zipped package: `deployment_package.zip`.

### Deployment Steps

1. **Prepare Configuration:**

   - Copy `terraform.tfvars.example` to `terraform.tfvars`.
   - Fill out the required values in `terraform.tfvars`.

1. **Run the Terraform Workflow:**

   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

### Changes from the original project

- I made the project work with content from the Python Standard Library.
- I did this on a Mac, so I made some changes to the setup script to work on a
  Mac.
- I used Python 3.13 instead of Python 3.8.
- I added an MIT license.
