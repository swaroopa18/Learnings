variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "ami_id" {
  description = "Amazon Linux 2023 AMI"
  type        = string
  default     = "ami-0ac7b260cf76d8865"
}

variable "server_instance_type" {
  description = "Timesheet server instance type"
  type        = string
  default     = "t3.micro"
}

variable "db_instance_type" {
  description = "Timesheet DB instance type"
  type        = string
  default     = "t3.micro"
}

variable "ssh_key_name" {
  description = "Existing EC2 key pair name"
  type        = string
}