#!/usr/bin/env python3

import yaml
import base64
import subprocess

# open config file
config_data = None
with open(r'secrets/config.yaml') as f:
    
    config_data = yaml.load(f, Loader=yaml.FullLoader)
    print(config_data)
f.close()

# open secrets template file
secrets_manifest = None
with open('secrets/jupyter_secrets.yaml', 'r') as fp:
    secrets_manifest = yaml.load(fp, Loader=yaml.FullLoader)
    print(secrets_manifest)
fp.close()

with open('secrets/jupyter_secrets.yaml', 'w') as ft:
    # Base64 encoding of aws access key id
    access_key_bytes = config_data['AWS_ACCESS_KEY_ID'].encode('ascii')
    secrets_manifest['data']['AWS_ACCESS_KEY_ID'] = base64.b64encode(access_key_bytes).decode("ascii") 
    #Base 64 encoding of aws secret access key
    access_secret_access_key_bytes = config_data['AWS_SECRET_ACCESS_KEY'].encode('ascii')
    secrets_manifest['data']['AWS_SECRET_ACCESS_KEY'] = base64.b64encode(access_secret_access_key_bytes).decode("ascii") 
    print(secrets_manifest)
    yaml.dump(secrets_manifest, ft)
ft.close()


proxy_token  = subprocess.run(['openssl', 'rand', '-hex', '32'], stdout=subprocess.PIPE, text=True).stdout.strip()
print(proxy_token)
jupyterhub_config = None
with open('jupyterhub/z2jh-config.yaml', 'r') as fp:
    jupyterhub_config = yaml.load(fp, Loader=yaml.FullLoader)
    print(jupyterhub_config)
fp.close()

with open('jupyterhub/z2jh-config.yaml', 'w') as ft:
    jupyterhub_config['proxy']['secretToken'] = proxy_token
    print(jupyterhub_config)
    yaml.dump(jupyterhub_config, ft)
ft.close()

