# LOG8415E - final project
# infra.tf
# Terraform configuration relative to instance definitions

# Declaring 4 instances of the t2 type for the cluster
resource "aws_instance" "t2_cluster" {
  count                       = 4
  ami                         = "ami-0a6b2839d44d781b2"
  instance_type               = "t2.large"
  associate_public_ip_address = true
  user_data = count.index == 0 ? templatefile("../scripts/cluster-master-setup-v2.sh.tftpl", {}) : templatefile("../scripts/cluster-data-node-setup-v2.sh.tftpl", {})
  subnet_id              = aws_subnet.cluster_subnet.id
  vpc_security_group_ids = [aws_security_group.network_sg.id]
  key_name = "log8415-finalprojet-keypair"

  tags = {
    "Name" = var.cluster_instance_names[count.index]
  }
}

# Declaring 1 instance of the t2 type for the stand-alone
resource "aws_instance" "t2_stand-alone" {
  ami                         = "ami-0149b2da6ceec4bb0"
  instance_type               = "t2.large"
  associate_public_ip_address = true
  user_data = templatefile("../scripts/standalone-setup.sh.tftpl", {})
  subnet_id              = aws_subnet.standalone_subnet.id
  vpc_security_group_ids = [aws_security_group.network_sg.id]
  key_name = "log8415-finalprojet-keypair"

  tags = {
    "Name" = "standalone"
  }
}

#declaring 1 instance for the proxy
resource "aws_instance" "t2-proxy" {
  ami                         = "ami-0149b2da6ceec4bb0"
  instance_type               = "t2.large"
  associate_public_ip_address = true
  #user_data = templatefile("", {})
  subnet_id              = aws_subnet.standalone_subnet.id
  vpc_security_group_ids = [aws_security_group.network_sg.id]
  key_name = "log8415-finalprojet-keypair"

  tags = {
    "Name" = "proxy"
  }
}

variable cluster_instance_names {
    type = list(string)
}