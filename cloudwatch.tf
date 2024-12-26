# CloudWatch Event rule to trigger Lambda every day
resource "aws_cloudwatch_event_rule" "daily_trigger" {
  name        = "daily_lambda_trigger"
  description = "Trigger Lambda function once a day at 07:00 Berlin time"
  schedule_expression = "cron(0 6 * * ? *)"
}

# CloudWatch Event target to invoke the Lambda function
resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.daily_trigger.name
  arn       = aws_lambda_function.hello_world_lambda.arn
  target_id = "daily_lambda_target"
}
