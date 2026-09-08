data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }

  filter {
    name   = "availability-zone"
    values = ["ap-south-1a"]
  }
}

# ---------------------------------------------------------
# Security Group
# ---------------------------------------------------------

resource "aws_security_group" "timesheet_sg" {
  name        = "timesheet-poc-sg"
  description = "Security group for Timesheet POC"
  vpc_id      = data.aws_vpc.default.id

  # SSH
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # PostgreSQL - for POC, allow from anywhere.
  # Later we can restrict this to the server private IP.
  ingress {
    description = "PostgreSQL"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "timesheet-poc-sg"
  }
}


# ---------------------------------------------------------
# Timesheet Application Server
# ---------------------------------------------------------

resource "aws_instance" "timesheet_server" {
  ami                    = var.ami_id
  instance_type          = var.server_instance_type
  subnet_id              = data.aws_subnets.default.ids[0]
  vpc_security_group_ids = [aws_security_group.timesheet_sg.id]
  key_name               = var.ssh_key_name

  root_block_device {
    volume_size = 20
    volume_type = "gp3"
  }

  tags = {
    Name = "timesheet-server"
  }
}


# ---------------------------------------------------------
# Timesheet DB Server
# ---------------------------------------------------------

resource "aws_instance" "timesheet_db" {
  ami                    = var.ami_id
  instance_type          = var.db_instance_type
  subnet_id              = data.aws_subnets.default.ids[0]
  vpc_security_group_ids = [aws_security_group.timesheet_sg.id]
  key_name               = var.ssh_key_name

  root_block_device {
    volume_size = 20
    volume_type = "gp3"
  }

  # This is similar to your existing infrastructure:
  #
  # additional EBS volume
  # delete_on_termination = false
  #
  tags = {
    Name = "timesheet-db"
  }
}

resource "aws_ebs_volume" "postgres_data" {
  availability_zone = "ap-south-1a"
  size              = 10
  type              = "gp3"

  tags = {
    Name = "timesheet-postgres-data"
  }

  lifecycle {
    prevent_destroy = false
  }
}

resource "aws_volume_attachment" "postgres_data" {
  device_name = "/dev/sdh"
  volume_id   = aws_ebs_volume.postgres_data.id
  instance_id = aws_instance.timesheet_db.id
}
