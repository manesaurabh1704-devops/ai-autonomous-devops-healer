output "workstation_public_ip" {
  description = "Workstation Public IP"
  value       = aws_instance.workstation.public_ip
}

output "workstation_instance_id" {
  description = "Workstation Instance ID"
  value       = aws_instance.workstation.id
}
