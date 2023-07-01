# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

# Input variable definitions

variable "aws_region" {
  description = "AWS region for all resources."

  type    = string
  default = "us-east-1"
}

variable "env_name" {
  description = "Prod"
}

variable "open_ai_token" {
  description = "OpenAI token"
}

variable "whatsapp_url" {
  description = "WhatsApp URL"
}

variable "whatsapp_token" {
  description = "WhatsApp URL"
}

variable "bnbot_bucket_name" {
  description = "Bucket Name"
  default = "bnbot-bucket" 
}
