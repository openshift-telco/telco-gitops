# Local Storage Operator (LSO)

NOTE: The namespace manifest on [01-install.yaml](01-install.yaml) has been annotated to allow LSO to be used on any node. To modify that behavior, modify the namespace annotations.

There are two types of configurations for LSO, one with dynamic local discovery and one with static LocalVolume profiles. This folder provide examples for both configurations.

LSO on the management cluster is used as bare-metal storage backend for OpenShift Container Storage (OCS). For that configuration SLO is configured automated discovery mechanisms and LocalVolumeSet for block devices to be consumed for the storage cluster.

LSO on the CU or DU clusters is used with static LocalVolume profiles definitions.

## Using Manifests without automation

### Using directly with Kustomize flag

- To deploy LSO into a cluster

    ```bash
    oc apply -k .
    ```

- Create a local storage policy (dynamic discovery or static) 
- Enable local storage only for nodes using label from policy. Example [04-lso-profile1-EXAMPLE.yaml](04-config-lso-profile0-EXAMPLE.yaml)

    ```bash
    oc label node <node> ran.openshift.io/ran.openshift.io/lso-profile1=''
    ```

### Manual steps

- Annotate namespace to allow ANY node to use LSO

    ```bash
    oc annotate ns openshift-local-storage openshift.io/node-selector=''
    ```

- Install operator

    ```bash
    oc apply -f 01-install.yaml
    ```

- Create a local storage policy (dynamic discovery or static)
- Enable local storage only for nodes using label from policy
