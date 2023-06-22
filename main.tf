# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      hashicorp-learn = "lambda-api-gateway"
    }
  }

}

data "aws_ecr_repository" "bnbot_ecr_repo" {
  name = "bnbot-repo"
}

data "aws_ecr_repository" "availability_updater_repo" {
  name = "availability-updater-repo"
}

# resource "random_pet" "lambda_bucket_name" {
#   prefix = "bnbot-bucket"
#   length = 4
# }

resource "aws_s3_bucket" "bnbot_bucket" {
  bucket = var.bnbot_bucket_name

  # Enable versioning to keep track of object versions
  versioning {
    enabled = true
  }
}

resource "aws_s3_bucket_ownership_controls" "bnbot_bucket" {
  bucket = aws_s3_bucket.bnbot_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "bnbot_bucket" {
  bucket = aws_s3_bucket.bnbot_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_acl" "bnbot_bucket" {
  depends_on = [
    aws_s3_bucket_ownership_controls.bnbot_bucket,
    aws_s3_bucket_public_access_block.bnbot_bucket,
  ]

  bucket = aws_s3_bucket.bnbot_bucket.id
  acl    = "public-read"
}

# Create an IAM policy for the Lambda function
resource "aws_iam_policy" "bnbot_bucket_lambda_policy" {
  name        = "bnbot-bucket-policy"
  description = "Policy to allow access to the S3 bucket"
  policy      = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowLambdaAccess",
      "Effect": "Allow",
      "Action": [
        "s3:*"
      ],
      "Resource": [
        "${aws_s3_bucket.bnbot_bucket.arn}/*"
      ]
    }
  ]
}
EOF
}

# Create an IAM role for the Lambda function and attach the policy
resource "aws_iam_role" "availability_lambda_role" {
  name = "availability_lambda-function-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "availability_lambda_role_policy_attachment" {
  role       = aws_iam_role.availability_lambda_role.name
  policy_arn = aws_iam_policy.bnbot_bucket_lambda_policy.arn
}

resource "aws_iam_role_policy_attachment" "bnbot_lambda_lambda_role_policy_attachment" {
  role       = aws_iam_role.bnbot_lambda_role.name
  policy_arn = aws_iam_policy.bnbot_bucket_lambda_policy.arn
}

resource "aws_lambda_function" "availability_function" {
  function_name = "availability-updater-fn-${var.env_name}"
  timeout       = 10 # seconds
  image_uri     = "${data.aws_ecr_repository.availability_updater_repo.repository_url}:${var.env_name}"
  package_type  = "Image"

  role = aws_iam_role.availability_lambda_role.arn

  environment {
    variables = {
      ENVIRONMENT = var.env_name
      BUCKET_NAME = aws_s3_bucket.bnbot_bucket.id
    }
  }
}


resource "aws_lambda_function" "bnbot_function" {
  function_name = "bnbot-fn-${var.env_name}"
  timeout       = 10 # seconds
  image_uri     = "${data.aws_ecr_repository.bnbot_ecr_repo.repository_url}:${var.env_name}"
  package_type  = "Image"

  role = aws_iam_role.bnbot_lambda_role.arn

  reserved_concurrent_executions = 1 # Restrict 1 instance for testing 

  environment {
    variables = {
      ENVIRONMENT = var.env_name
      OPEN_AI_TOKEN = var.open_ai_token
      OPENAI_API_KEY = var.open_ai_token
      WHATSAPP_URL = var.whatsapp_url
      WHATSAPP_TOKEN = var.whatsapp_token
    }
  }
}

resource "aws_cloudwatch_log_group" "hello_world" {
  name = "/aws/lambda/${aws_lambda_function.bnbot_function.function_name}"

  retention_in_days = 30
}

resource "aws_iam_role" "bnbot_lambda_role" {
  name = "bnbot_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Sid    = ""
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.bnbot_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_apigatewayv2_api" "lambda" {
  name          = "serverless_lambda_gw"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "lambda" {
  api_id = aws_apigatewayv2_api.lambda.id

  name        = "serverless_lambda_stage"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw.arn

    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
      }
    )
  }
}

resource "aws_apigatewayv2_integration" "hello_world" {
  api_id = aws_apigatewayv2_api.lambda.id

  integration_uri    = aws_lambda_function.bnbot_function.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "hello_world" {
  api_id = aws_apigatewayv2_api.lambda.id

  route_key = "GET /hello"
  target    = "integrations/${aws_apigatewayv2_integration.hello_world.id}"
}

resource "aws_apigatewayv2_route" "hello_world_post" {
  api_id = aws_apigatewayv2_api.lambda.id

  route_key = "POST /hello"
  target    = "integrations/${aws_apigatewayv2_integration.hello_world.id}"
}

resource "aws_cloudwatch_log_group" "api_gw" {
  name = "/aws/api_gw/${aws_apigatewayv2_api.lambda.name}"

  retention_in_days = 30
}

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.bnbot_function.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.lambda.execution_arn}/*/*"
}
