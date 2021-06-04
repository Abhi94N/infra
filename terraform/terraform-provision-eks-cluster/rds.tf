
resource "aws_db_subnet_group" "private" {
  subnet_ids = module.vpc.private_subnets
}

resource "aws_rds_cluster" "database" {
  cluster_identifier      = "aurora-cluster-illumidesk"
  engine                  = "aurora-postgresql"
  backup_retention_period = 5
  preferred_backup_window = "07:00-09:00"
  database_name           = var.db_name
  master_username         = var.db_username
  master_password         = var.db_password
  vpc_security_group_ids  = [aws_security_group.postgres_security.id]
  db_subnet_group_name    = aws_db_subnet_group.private.name

  skip_final_snapshot = true
}
