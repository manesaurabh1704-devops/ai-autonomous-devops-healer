variable "project_name" {
  type    = string
  default = "ai-autonomous-devops-healer"
}

variable "environment" {
  type    = string
  default = "production"
}

variable "public_subnet_id" {
  type = string
}

variable "workstation_sg_id" {
  type = string
}

variable "instance_type" {
  type    = string
  default = "t2.micro"
}

variable "key_name" {
  type = string
}
