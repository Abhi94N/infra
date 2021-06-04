module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = local.cluster_name
  cluster_version = "1.20"
  subnets         = module.vpc.public_subnets
  enable_irsa     = true
  tags = {
    Environment = "poc"
    GithubRepo  = "infra"
    GithubOrg   = "illumidesk"
  }

  vpc_id = module.vpc.vpc_id

  node_groups_defaults = {
    root_volume_type = "gp2"
  }

  node_groups = {
    core = {
      name             = "core"
      desired_capacity = 1
      max_capacity     = 3
      min_capacity     = 1
      instance_types   = ["t3.micro"]
      key_name         = aws_key_pair.ssh_key.key_name
      k8s_labels = {
        "hub.jupyter.org/node-purpose" = "core"
      }
      additional_tags = {
      }
    }
    notebook = {
      name             = "notebook"
      desired_capacity = 1
      max_capacity     = 10
      min_capacity     = 1
      key_name         = aws_key_pair.ssh_key.key_name
      instance_types   = ["t3.medium"]
      k8s_labels = {
        "hub.jupyter.org/node-purpose" = "user"
      }
      additional_tags = {
      }
    }
  }
}

data "aws_eks_cluster" "cluster" {
  name = module.eks.cluster_id
}

data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_id
}
