# Latest Ubuntu 22.04 AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# EC2 Workstation
resource "aws_instance" "workstation" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  subnet_id              = var.public_subnet_id
  vpc_security_group_ids = [var.workstation_sg_id]
  key_name               = var.key_name

  root_block_device {
    volume_size = 20
    volume_type = "gp3"
  }

  user_data = <<-EOF
    #!/bin/bash
    apt-get update -y
    apt-get install -y docker.io git curl unzip

    # Docker start
    systemctl start docker
    systemctl enable docker
    usermod -aG docker ubuntu

    # AWS CLI install
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    ./aws/install

    # kubectl install
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    chmod +x kubectl
    mv kubectl /usr/local/bin/

    # Terraform install
    curl -LO "https://releases.hashicorp.com/terraform/1.14.6/terraform_1.14.6_linux_amd64.zip"
    unzip terraform_1.14.6_linux_amd64.zip
    mv terraform /usr/local/bin/

    # Python + pip
    apt-get install -y python3 python3-pip
  EOF

  tags = {
    Name        = "${var.project_name}-workstation"
    Environment = var.environment
  }
}
