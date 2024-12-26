resource "aws_ssm_parameter" "open_ai_api_key" {
  name        = "OPEN_AI_API_KEY"
  type        = "SecureString"
  value       = var.open_ai_api_key
  description = "Open AI API key for the Lambda function"
}

resource "aws_ssm_parameter" "email_for_ses" {
  name        = "EMAIL_FOR_SES"
  type        = "SecureString"
  value       = var.ses_email
  description = "SES email address for sending emails"
}
