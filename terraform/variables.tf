variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "formalert"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}