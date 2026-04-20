variable "project_name" {
  type    = string
  default = "ai-autonomous-devops-healer"
}

variable "environment" {
  type    = string
  default = "production"
}

variable "vpc_id" {
  type = string
}

variable "private_subnet_ids" {
  description = "List of Private Subnet IDs"
  type        = list(string)
}

variable "eks_cluster_sg_id" {
  type = string
}

variable "eks_nodes_sg_id" {
  type = string
}

variable "node_instance_type" {
  type    = string
  default = "t3.medium"
}

variable "desired_nodes" {
  type    = number
  default = 2
}

variable "min_nodes" {
  type    = number
  default = 1
}

variable "max_nodes" {
  type    = number
  default = 3
}
