variable "region" {
  default = "us-east-2"
}

variable "namespace" {
  type    = string
  default = "illumidesk"
}

# variable "slack_app_token" {
#   type        = string
#   description = "Slack App Token"
# }

# Jupyterhub variables
variable "jupyterhub_debug" {
  type        = bool
  description = "Activate debug mode"
  default     = false
}

variable "jupyterhub_proxy_token" {
  type        = string
  description = "Jupyterhub Proxy Token"
  sensitive   = true
}

variable "jupyterhub_api_token" {
  type        = string
  description = "Jupyterhub API Token"
  sensitive   = true
}

variable "jupyterhub_crypt_key" {
  type        = string
  description = "Jupyterhub Cryptography Key"
  sensitive   = true
}

# Single User Notebook Variables
variable "single_user_image" {
  type        = string
  description = "Provide a single user notebook image in the following format image:tag"
  default     = "illumidesk/illumidesk-notebook:latest"
}

#Hub Image variables
variable "hub_image" {
  type        = string
  description = "Provide a hub image in the following format image:tag"
  default     = "illumidesk/jupyterhub:k8s-beta.13"
}

#Auth Variables
variable "custom_auth_type" {
  type        = string
  description = "Custom auth type"
  default     = "LTI13"
}

## LTI 1.1
variable "lti_consumer_key" {
  type        = string
  description = "LTI 1.1 Consumer Key"
  default     = "lti_11_consumer_key"
}

variable "lti_shared_secret" {
  type        = string
  description = "LTI 1.1 Shared Secret"
  default     = "lti_11_shared_secret"
}

## LTI 1.3
variable "lti_13_client_id" {
  type        = string
  description = "LTI 1.3 Client Id"
  default     = "125900000000000246"
}
variable "lti_13_endpoint" {
  type        = string
  description = "LTI 1.3 Endpoint"
  default     = "https://illumidesk.instructure.com/api/lti/security/jwks"
}
variable "lti_13_authorize_url" {
  type        = string
  description = "LTI 1.3 Authorize URL"
  default     = "https://illumidesk.instructure.com/api/lti/authorize_redirect"
}
variable "lti_13_token_url" {
  type        = string
  description = "LTI 1.3 Token URL"
  default     = "https://illumidesk.instructure.com/login/oauth2/token"
}

## OIDC
variable "oidc_client_id" {
  type        = string
  description = "OIDC Client ID"
  default     = ""
}
variable "oidc_client_secret" {
  type        = string
  description = "OIDC Client Secret"
  default     = ""
}
variable "oidc_callback_url" {
  type        = string
  description = "OIDC Callback URL"
  default     = ""
}

variable "oidc_authorize_url" {
  type        = string
  description = "OIDC Authorize URL"
  default     = ""
}

variable "oidc_token_url" {
  type        = string
  description = "OIDC Token URL"
  default     = ""
}
variable "oidc_userdata_url" {
  type        = string
  description = "OIDC Userdata URL"
  default     = ""
}

##Postgres Variables
variable "postgres_host" {
  type        = string
  description = "Postgres Host"
  default     = "postgres"
}

variable "postgres_user" {
  type        = string
  description = "Postgres DB User"
  default     = "postgres"
}

variable "postgres_password" {
  type        = string
  description = "Postgres Password"
  sensitive   = true
}
variable "postgres_db" {
  type        = string
  description = "Postgres DB"
  default     = "illumidesk"
}

## Ingress Resources
variable "alb_host" {
  type        = string
  description = "Alb Ingress Resource"
  default     = "illumidesk.illumidesk.com"
}
