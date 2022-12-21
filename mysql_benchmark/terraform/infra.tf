# LOG8415E - final project
# infra.tf
# Terraform configuration relative to instance definitions

# Declaring 4 instances of the t2 type for the cluster
resource "aws_instance" "t2_cluster" {
  count                       = 4
  ami                         = "ami-0149b2da6ceec4bb0"
  instance_type               = "t2.micro"
  associate_public_ip_address = true
#   user_data = templatefile("../scripts/instance-config.sh.tftpl", {
#     number = count.index
#   })
  subnet_id              = aws_subnet.cluster_subnet.id
  vpc_security_group_ids = [aws_security_group.network_sg.id]
  key_name = "log8415-finalprojet-keypair"

  tags = {
    "name" = format("cluster-%d", count.index + 1)
  }
}

# Declaring 1 instance of the t2 type for the stand-alone
resource "aws_instance" "t2_stand-alone" {
  ami                         = "ami-0149b2da6ceec4bb0"
  instance_type               = "t2.micro"
  associate_public_ip_address = true
  user_data = templatefile("../scripts/standalone-setup.sh.tftpl", {})
  subnet_id              = aws_subnet.standalone_subnet.id
  vpc_security_group_ids = [aws_security_group.network_sg.id]
  key_name = "log8415-finalprojet-keypair"

  tags = {
    "name" = "standalone"
  }
}

# Resource to create key_pair, conflicts if duplicated
# resource "aws_key_pair" "keypair" {
#     key_name = "log8415-finalprojet-keypair"
#     public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCo+0+9wXNMpFmjvAU70chPe1FpqppYdhtHgaovk51XnQ9JBWP331g3Q7jwYUWlxZMH6ZPbo5Ftt0AWHxw16pSkB43w7zfhTl99O+OqjapjAeklAKTUc2AYMq7uyzSMZWkW972DwxBfzV37FtJKRoEG4DIhPqIOWjijhiBs9oPGS+S6ZLMw815a6QHqxL9RV4SnFwI5F2vss0gaoIZ71eCaLJDOdhAlLfAl0hsJ/Pwis6WZqhRXNDg1mHeE3Wl5c1tTncpBzset+jProaxPif+p0vMHlEGu0JP7Q3zXKt38hOYj1O94YFbNglwvCh3Ywiot13Se8XK3zrV4MU7MhUV9 log8415-finalprojet-keypair"
# }