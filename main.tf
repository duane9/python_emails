provider "aws" {
  region = var.region
}

data "aws_caller_identity" "current" {}

# Lambda where everything runs on
resource "aws_lambda_function" "hello_world_lambda" {
  function_name    = "HelloWorldLambda"
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.13"
  filename         = "deployment_package.zip"
  source_code_hash = filebase64sha256("deployment_package.zip")
  timeout          = 60
}

