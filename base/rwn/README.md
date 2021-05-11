# RAN workload on Remote Worker Nodes (RWN)

Use Pod tolerations to mitigate the effects on Pods running on RWN after the control plane sets `node.kubernetes.io/unreachable` taint to `NoExecute` when it cannot reach a node and the `pod-eviction-timeout` has expired.

It is recommended for the RAN CU and DU workload deployed on RWN to have the following tolerations in the Pod spec:

```bash
spec:
    ...
    tolerations:
        - key: "node.kubernetes.io/unreachable"
            operator: "Exists"
            effect: "NoExecute"
        - key: "node.kubernetes.io/not-ready"
            operator: "Exists"
            effect: "NoExecute"
        - key: "node.kubernetes.io/unschedulable"
            operator: "Exists"
            effect: "NoExecute"
    ...
```

or to use the following "catch all" toleration

```bash
tolerations:
    - operator: "Exists"
```

For explanations on the different behaviors and timers refer to the [OpenShift RWN](https://docs.openshift.com/container-platform/4.7/nodes/edge/nodes-edge-remote-workers.html) documentation.

## Pod Topology Spread Constraints

Control how Pods are spread across failure-domains (regions, zones, nodes and user defined topology domains)

See Kubernetes upstream documentation [Pod Topology Spread Constraints](https://kubernetes.io/docs/concepts/workloads/pods/pod-topology-spread-constraints/)

## Prevent MC rollout/update to an MCP

- To pause the MC rollout/update from MCO set the `spec.pause=true` on MCP
  
  ```bash
  oc patch --type=merge --patch='{"spec":{"paused":true}}' machineconfigpool/worker'
  ```
