# Telco Managment Cluster

The Telco management cluster must be OCP 4.8.x and be deployed using one of the following methods:
- Assisted Installer / Assisted Service Operator mode
- Baremetal IPI mode

These method are the only methods that deploy and configure the `cluster-baremetal-operator` in the cluster which is a requirement for some of the automation flows.

**NOTE:** Due to `BZ-1953979` the minimum version for mgmt cluster is `4.8.0-0.nightly-2021-05-31-085539`

##

One the cluster is deployed using one of the valid deployment methods for Telco Management Clusters

```bash
export KUBECONFIG="~/path/to/kubeconfig-telco-mgmt"
export TELCO_MGMT_PATH="~/path/to/this/path"
oc apply -k $TELCO_MGMT_PATH
```

- Sample run

```bash
wcabanba$ oc whoami --show-server
https://api.mgmt.telco.shift.zone:6443

wcabanba$ oc apply -k .
namespace/openshift-gitops-operator created
namespace/openshift-local-storage created
namespace/openshift-sriov-network-operator created
clusterrolebinding.rbac.authorization.k8s.io/cluster-admin-group created
clusterrolebinding.rbac.authorization.k8s.io/cluster-admin-telcoadmin created
...<snip>...
error: unable to recognize ".": no matches for kind "SriovOperatorConfig" in version "sriovnetwork.openshift.io/v1"
```

- Ignore the "no matches for kind 'SriovOperatorConfig' " error as the reason is the SR-IOV Operator is getting install but the deployment has not compelted by the time it tries to configure the CRs in the first run.
- Disconnection for the ingressVIP and apiVIP might be experienced as the configuration is modifying the corresponding operator configuration. There is a rolling update that is also kickstarted by the chrony configuration wich will apply to nodes. After few minutes the base configuration sould be completed
- Create secret from pull-secret for Assisted Installer Operator

    ```bash
    oc create secret generic assisted-deployment-pull-secret -n assisted-installer \
    --from-file=.dockerconfigjson=pull-secret.json --type=kubernetes.io/dockerconfigjson
    ```

- Patch metal3 so it can see all the `bmh` resources in all namespaces:
  
    ```bash
    oc patch provisioning provisioning-configuration --type merge -p '{"spec":{"watchAllNamespaces": true}}'
    ```
- To obtain the password for `openshift-gitops` ArgoCD `admin`
    ```bash
    oc get secret openshift-gitops-cluster -o go-template='{{index .data "admin.password"}}' | base64 -d
    ```