variable "project_name" {
  description = "Project name"
  type        = string
  default     = "ai-autonomous-devops-healer"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "ap-south-1"
}

variable "vpc_cidr" {
  description = "VPC CIDR Block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "key_name" {
  description = "AWS Key Pair Name for EC2"
  type        = string
  default     = "ai-devops-key"
}

variable "instance_type" {
  description = "EC2 Instance Type"
  type        = string
  default     = "c7i-flex.large"
}

variable "node_instance_type" {
  description = "EKS Node Instance Type"
  type        = string
  default     = "c7i-flex.large"
}

variable "desired_nodes" {
  description = "Desired EKS nodes"
  type        = number
  default     = 2
}

variable "min_nodes" {
  description = "Minimum EKS nodes"
  type        = number
  default     = 1
}

variable "max_nodes" {
  description = "Maximum EKS nodes"
  type        = number
  default     = 3
}
