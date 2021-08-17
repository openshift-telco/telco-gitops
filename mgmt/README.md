# Telco Managment Cluster

The Telco management cluster *MUST* be OpenShift 4.8.x or higher and *MUST* be deployed using one of the following methods:
- Assisted Installer / Assisted Service Operator
- Baremetal IPI

These method are the *ONLY* methods that deploy and configure the `cluster-baremetal-operator` in the cluster which is a requirement for some of the ZTP automation flows.

**NOTE:** Due to `BZ-1953979` the minimum version for mgmt cluster is `4.8.0-0.nightly-2021-05-31-085539`

## EXAMPLES

The following are examples of Telco management clusters using the `telco-gitops` repository:

- https://github.com/openshift-telco/telco-gitops-mgmt
- https://github.com/novacain1/carslab-public/tree/main/rhocp-clusters/volt.cars.lab
