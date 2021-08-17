# Telco GitOps configuration

The `telco-gitops` configurations:

- Operates under the `telco-gitops` namespace on the management cluster
- Creates a `cli-job-sa` ServiceAccount for hooks
- Creates custom roles for ArgoCD ServiceAccounts
- When used to manage local and remote clusters, the ArgoCD instance runs with `cluster-admin` privileges
- The `telco-gitops` ArgoCD instance should ONLY be available for cluster-admin operations

## Accessing the `telco-gitops` ArgoCD

- To obtain the `admin` password for the `telco-gitops` ArgoCD instance

    ```bash
    oc get secret telco-gitops-cluster -o go-template='{{index .data "admin.password"}}' -n telco-gitops | base64 -d
    ```
