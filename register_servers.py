#!/usr/bin/env python

import os
import globus_sdk
from kubernetes import client, config

K8S_NAMESPACE = os.environ['K8S_NAMESPACE']


def get_dtn_pod_ips(label_selector):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    pods = v1.list_namespaced_pod(K8S_NAMESPACE, label_selector=label_selector)

    ipSet = set()

    active_pods = filter(lambda p: p.metadata.deletionTimestamp is None, pods.items)
    for pod in active_pods:
        ipSet.add(pod.status.pod_ip)

    return ipSet


def update_endpoint_ips(globus_client, endpoint_id, ips):
    servers = globus_client.endpoint_server_list(endpoint_id)
    existing_ips = set()
    server_map = dict()
    for server in servers:
        existing_ips.add(server['hostname'])
        server_map[server['hostname']] = server

    delete_ips = existing_ips - ips
    add_ips = ips - existing_ips

    for ip in delete_ips:
        result = globus_client.delete_endpoint_server(endpoint_id, server_map[ip]['id'])

    for ip in add_ips:
        new_server = dict()
        new_server['DATA_TYPE'] = 'server'
        new_server['hostname'] = ip
        new_server['subject'] = os.environ['GLOBUS_CERT_SUBJECT']
        result = globus_client.add_endpoint_server(endpoint_id, new_server)


def get_globus_client():
    with open('/credentials/client_id', 'r') as f:
        client_id = f.read()

    with open('/credentials/client_secret', 'r') as f:
        client_secret = f.read()

    confidential_client = globus_sdk.ConfidentialAppAuthClient(client_id=client_id, client_secret=client_secret)

    scopes = "urn:globus:auth:scopes:transfer.api.globus.org:all"
    cc_authorizer = globus_sdk.ClientCredentialsAuthorizer(
        confidential_client, scopes)
    # create a new client
    transfer_client = globus_sdk.TransferClient(authorizer=cc_authorizer)

    return transfer_client


def main():
    pods = get_dtn_pod_ips(os.environ['K8S_POD_SELECTOR'])
    globus_client = get_globus_client()
    update_endpoint_ips(globus_client, os.environ['GLOBUS_ENDPOINT_ID'], pods)


if __name__ == "__main__":
    main()
