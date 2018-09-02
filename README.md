# Globus Endpoint Manager

## Configuration

K8S_NAMESPACE - Kubernetes pod namespace
K8S_POD_SELECTOR - Label selector to find DTN Pods

GLOBUS_ENDPOINT_ID - endpoint id to update
GLOBUS_CERT_SUBJECT - certificate_subject

/credentials/{client_id,client_secret} - Path to secrets

## Creating credentials

1. Create an app at developers.globus.org
  * Not native app
  * create a secret after creating app
1. Give new client globus id  (@globusid.org credential) access to endpoint
1. create kubernetes secret with client_id and client_secret
