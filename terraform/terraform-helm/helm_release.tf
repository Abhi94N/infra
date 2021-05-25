provider "helm" {
  kubernetes {
    host                   = data.aws_eks_cluster.cluster.endpoint
    cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority.0.data)
    exec {
      api_version = "client.authentication.k8s.io/v1alpha1"
      args        = ["eks", "get-token", "--cluster-name", data.aws_eks_cluster.cluster.name]
      command     = "aws"
    }
  }
}

resource "helm_release" "kubewatch" {
  name       = "kubewatch"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "kubewatch"

  values = [
    file("${path.module}/kubewatch-values.yaml")
  ]

  set_sensitive {
    name  = "slack.token"
    value = var.slack_app_token
  }
}

locals {
  single_user_pvc             = format("shared-pvc-, %s", var.namespace)
  single_user_pvc_subpath     = format("%s, /home/{username}", var.namespace)
  extra_volume_mounts_subpath = format("%s, /exchange/", var.namespace)
}
resource "helm_release" "illumidesk-stack" {
  name       = "illumidesk-stack"
  repository = "https://illumidesk.github.io/helm-chart/"
  chart      = "illumidesk/illumidesk"
  version    = "3.2.0"

  values = [
    file("${path.module}/illumidesk-values.yaml")
  ]


  set {
    name  = "jupyterhub.debug"
    value = var.jupyterhub_debug
  }

  # Hub Tokens
  set_sensitive {
    name  = "jupyterhub.proxy.secretToken"
    value = var.jupyterhub_proxy_token
  }
  set_sensitive {
    name  = "jupyterhub.hub.extraEnv.JUPYTERHUB_API_TOKEN"
    value = var.jupyterhub_api_token
  }
  set_sensitive {
    name  = "jupyterhub.hub.extraEnv.JUPYTERHUB_CRYPT_KEY"
    value = var.jupyterhub_crypt_key
  }

  #Single User
  set {
    name  = "jupyterhub.singleuser.storage.pvcName"
    value = local.single_user_pvc
  }
  set {
    name  = "jupyterhub.singleuser.storage.subPath"
    value = local.single_user_pvc_subpath
  }
  set {
    name  = "jupyterhub.singleuser.storage.extraVolumeMounts[0].subPath"
    value = local.extra_volume_mounts_subpath
  }

  set {
    name  = "jupyterhub.singleuser.image.name"
    value = element(split(":", var.single_user_image), 0)
  }
  set {
    name  = "jupyterhub.singleuser.image.tag"
    value = element(split(":", var.single_user_image), 1)
  }

  # Hub Vars
  set {
    name  = "jupyterhub.hub.image.name"
    value = element(split(":", var.single_user_image), 0)
  }
  set {
    name  = "jupyterhub.hub.image.tag"
    value = element(split(":", var.single_user_image), 1)
  }

  set {
    name  = "jupyterhub.hub.extraEnv.CUSTOM_AUTH_TYPE"
    value = var.custom_auth_type
  }
  set {
    name  = "jupyterhub.hub.extraEnv.LTI_CONSUMER_KEY"
    value = var.lti_consumer_key
  }
  set {
    name  = "jupyterhub.hub.extraEnv.LTI_SHARED_SECRET"
    value = var.lti_shared_secret
  }
  set {
    name  = "jupyterhub.hub.extraEnv.LTI13_CLIENT_ID"
    value = var.lti_13_client_id
  }
  set {
    name  = "jupyterhub.hub.extraEnv.LTI13_ENDPOINT"
    value = var.lti_13_endpoint
  }
  set {
    name  = "jupyterhub.hub.extraEnv.LTI13_AUTHORIZE_URL"
    value = var.lti_13_authorize_url
  }
  set {
    name  = "jupyterhub.hub.extraEnv.LTI13_TOKEN_URL"
    value = var.lti_13_token_url
  }
  set {
    name  = "jupyterhub.hub.extraEnv.OIDC_CLIENT_ID"
    value = var.oidc_client_id
  }
  set {
    name  = "jupyterhub.hub.extraEnv.OIDC_CLIENT_SECRET"
    value = var.oidc_client_secret
  }
  set {
    name  = "jupyterhub.hub.extraEnv.OIDC_CALLBACK_URL"
    value = var.oidc_callback_url
  }
  set {
    name  = "jupyterhub.hub.extraEnv.OIDC_AUTHORIZE_URL"
    value = var.oidc_authorize_url
  }
  set {
    name  = "jupyterhub.hub.extraEnv.OIDC_TOKEN_URL"
    value = var.oidc_token_url
  }
  set {
    name  = "jupyterhub.hub.extraEnv.OIDC_USERDATA_URL"
    value = var.oidc_userdata_url
  }
  set {
    name  = "jupyterhub.hub.extraEnv.POSTGRES_NBGRADER_USER"
    value = var.postgres_user
  }
  set {
    name  = "jupyterhub.hub.extraEnv.POSTGRES_NBGRADER_PASSWORD"
    value = var.postgres_password
  }
  set {
    name  = "jupyterhub.hub.extraEnv.POSTGRES_NBGRADER_HOST"
    value = var.postgres_host
  }

  set {
    name  = "jupyterhub.hub.extraEnv.POSTGRES_JUPYTERHUB_HOST"
    value = var.postgres_host
  }
  set {
    name  = "jupyterhub.hub.extraEnv.POSTGRES_JUPYTERHUB_DB"
    value = var.postgres_db
  }

  set {
    name  = "albIngress.host"
    value = var.alb_host
  }
  set {
    name  = "graderSetupService.postgresNBGraderUser"
    value = var.postgres_user
  }
  set {
    name  = "graderSetupService.postgresNBGraderPassword"
    value = var.postgres_password
  }
  set {
    name  = "graderSetupService.postgresNBGraderHost"
    value = var.postgres_host
  }

}

