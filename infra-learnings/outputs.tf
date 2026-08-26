output "server_instance_id" {
  value = aws_instance.timesheet_server.id
}

output "server_public_ip" {
  value = aws_instance.timesheet_server.public_ip
}

output "db_instance_id" {
  value = aws_instance.timesheet_db.id
}

output "db_public_ip" {
  value = aws_instance.timesheet_db.public_ip
}

output "db_root_volume_id" {
  value = aws_instance.timesheet_db.root_block_device[0].volume_id
}

output "db_additional_volume_id" {
  value = one([
    for volume in aws_instance.timesheet_db.ebs_block_device :
    volume.volume_id
  ])
}