# Intel VRAN Acceleration Operators

For details refer to official documentation at:

- https://github.com/open-ness/openshift-operator/tree/main/spec
- https://github.com/open-ness/openshift-operator/blob/main/spec/openshift-pacn3000-operator.md
- https://github.com/open-ness/openshift-operator/blob/main/spec/openshift-sriov-fec-operator.md
- https://github.com/open-ness/openshift-operator/blob/main/spec/vran-accelerators-supported-by-operator.md

## Isolated Network Installation
For isolated network deployments, consult either (or ideally both):

[N3000](https://github.com/open-ness/openshift-operator/blob/main/spec/openshift-pacn3000-operator.md#setting-up-operator-registry-locally) documentation

[SRIOV-FEC](https://github.com/open-ness/openshift-operator/blob/main/spec/openshift-sriov-fec-operator.md#setting-up-operator-registry-locally) documentation


# Random notes
```shell
$ oc get n3000nodes.fpga.intel.com
NAME                 FLASH
node1.png.intel.com   Succeeded
node2.png.intel.com   Succeeded
```

## Get sriovfecnodeconfigs
`lspci -v -nn -mm -s 0000:6a:00.0`
