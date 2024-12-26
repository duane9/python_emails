
# DynamoDB table definition
resource "aws_dynamodb_table" "words_table" {
  name           = "WordsTable"
  billing_mode   = "PAY_PER_REQUEST" # No need to provision capacity
  hash_key       = "word"            # Partition key
  attribute {
    name = "word"
    type = "S"                       # String type
  }
}