output "load_balancer_sg_id" {
  description = "Load Balancer SG ID"
  value       = aws_security_group.load_balancer.id
}

output "workstation_sg_id" {
  description = "Workstation SG ID"
  value       = aws_security_group.workstation.id
}

output "eks_cluster_sg_id" {
  description = "EKS Cluster SG ID"
  value       = aws_security_group.eks_cluster.id
}

output "eks_nodes_sg_id" {
  description = "EKS Nodes SG ID"
  value       = aws_security_group.eks_nodes.id
}
