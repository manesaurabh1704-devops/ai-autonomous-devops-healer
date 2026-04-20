variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

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
