#!/bin/bash


# TODO: Convert this into yaml to use with GitOps patch functionality

echo "DO NOT RUN DIRECTLY. MANUALLY CHOOSE ONE OPTION"
exit 1

####################################
### CHOOSE ONE OF THE FOLLOWING ####
####################################

# Setup hostpath as the "scratch space"
oc patch CDIConfig config --type='json' -p='[{"op": "replace", "path": "/spec/scratchSpaceStorageClass", "value": "hostpath-provisioner"}]'

# Setup Ceph RBD as the "scratch space"
oc patch CDIConfig config --type='json' -p='[{"op": "replace", "path": "/spec/scratchSpaceStorageClass", "value": "ocs-storagecluster-ceph-rbd"}]'
