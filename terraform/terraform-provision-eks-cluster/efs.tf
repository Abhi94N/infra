resource "aws_efs_file_system" "efs" {
  tags = {
    Name = "${local.cluster_name}-efs"
  }
}

resource "aws_efs_mount_target" "efs_targets" {
  count           = length(module.vpc.private_subnets)
  file_system_id  = aws_efs_file_system.efs.id
  subnet_id       = module.vpc.public_subnets[count.index]
  security_groups = [aws_security_group.nfs_security.id]
}