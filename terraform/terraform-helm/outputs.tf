output "k8s_subpath" {
  description = "k8s sub_path"
  value       = local.extra_volume_mounts_subpath
}

# output "token" {
#   description = "k8s token"
#   value       = var.jupyterhub_proxy_token
# }