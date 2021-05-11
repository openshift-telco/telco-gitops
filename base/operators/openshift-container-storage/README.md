# OpenShift Container Storage operator

```
- oc get storagecluster

```bash
NAME                 AGE    PHASE   EXTERNAL   CREATED AT             VERSION
ocs-storagecluster   114m   Ready              2021-02-16T20:10:20Z   4.6.0
```

```bash
- oc get storageclass

```bash
NAME                                    PROVISIONER                             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
localblock                              kubernetes.io/no-provisioner            Delete          WaitForFirstConsumer   false                  4h5m
ocs-storagecluster-ceph-rbd (default)   openshift-storage.rbd.csi.ceph.com      Delete          Immediate              true                   3h21m
ocs-storagecluster-ceph-rgw             openshift-storage.ceph.rook.io/bucket   Delete          Immediate              false                  3h21m
ocs-storagecluster-cephfs               openshift-storage.cephfs.csi.ceph.com   Delete          Immediate              true                   3h21m
openshift-storage.noobaa.io             openshift-storage.noobaa.io/obc         Delete          Immediate              false                  3h11m
```

- oc get pods -n openshift-storage

```bash
NAME                                                              READY   STATUS      RESTARTS   AGE
csi-cephfsplugin-46xw6                                            3/3     Running     4          116m
csi-cephfsplugin-4bjhn                                            3/3     Running     0          116m
csi-cephfsplugin-5mxsh                                            3/3     Running     0          116m
csi-cephfsplugin-bxzrn                                            3/3     Running     0          116m
csi-cephfsplugin-provisioner-77c87bd6b6-md67n                     6/6     Running     14         116m
csi-cephfsplugin-provisioner-77c87bd6b6-stnhc                     6/6     Running     0          116m
csi-cephfsplugin-qn5w4                                            3/3     Running     0          116m
csi-cephfsplugin-sdd6m                                            3/3     Running     0          116m
csi-rbdplugin-6p5v7                                               3/3     Running     0          116m
csi-rbdplugin-7jr9p                                               3/3     Running     0          116m
csi-rbdplugin-d5qln                                               3/3     Running     0          116m
csi-rbdplugin-jx7dm                                               3/3     Running     0          116m
csi-rbdplugin-n6qr4                                               3/3     Running     0          116m
csi-rbdplugin-provisioner-79cffcd6df-4mxhr                        6/6     Running     1          116m
csi-rbdplugin-provisioner-79cffcd6df-s6x85                        6/6     Running     0          116m
csi-rbdplugin-zd2j6                                               3/3     Running     4          116m
noobaa-core-0                                                     1/1     Running     0          20m
noobaa-db-0                                                       1/1     Running     0          20m
noobaa-endpoint-94c7bdccb-kjdsw                                   1/1     Running     0          17m
noobaa-operator-6d6b46745d-p62mb                                  1/1     Running     0          3h14m
ocs-metrics-exporter-5557759dd8-m764x                             1/1     Running     0          3h14m
ocs-operator-d67758886-sbxkk                                      1/1     Running     0          77m
rook-ceph-crashcollector-leo1-66c546c49-2dwvk                     1/1     Running     0          115m
rook-ceph-crashcollector-leo2-7dbcbcff86-fdgdk                    1/1     Running     0          115m
rook-ceph-crashcollector-leo3-5cbf98b47-vczch                     1/1     Running     0          115m
rook-ceph-mds-ocs-storagecluster-cephfilesystem-a-56f9d5f9pqkpm   1/1     Running     0          20m
rook-ceph-mds-ocs-storagecluster-cephfilesystem-b-b796b8d65t9kh   1/1     Running     0          20m
rook-ceph-mgr-a-5d985f559d-jtfcg                                  1/1     Running     0          110m
rook-ceph-mon-a-68d4f76cbb-49wm8                                  1/1     Running     0          115m
rook-ceph-mon-b-6b5c9dd645-77s92                                  1/1     Running     0          115m
rook-ceph-mon-c-544c6b997b-sktxn                                  1/1     Running     0          115m
rook-ceph-operator-7b8d579586-mf5hb                               1/1     Running     0          3h14m
rook-ceph-osd-0-6dc6c8df86-4tt4j                                  1/1     Running     0          20m
rook-ceph-osd-1-d7d5ddc75-ppmd2                                   1/1     Running     0          20m
rook-ceph-osd-2-cd8f54897-x5szn                                   1/1     Running     0          108m
rook-ceph-osd-3-bc5677757-sxgnp                                   1/1     Running     0          108m
rook-ceph-osd-4-5cf56d89b5-8d9vr                                  1/1     Running     0          108m
rook-ceph-osd-5-dd68f8765-7rh68                                   1/1     Running     0          108m
rook-ceph-osd-prepare-ocs-deviceset-0-data-0-hjjcf-292t8          0/1     Completed   4          110m
rook-ceph-osd-prepare-ocs-deviceset-0-data-1-k9xwp-ztgd6          0/1     Completed   0          20m
rook-ceph-osd-prepare-ocs-deviceset-1-data-0-9prdt-xrr2x          0/1     Completed   4          110m
rook-ceph-osd-prepare-ocs-deviceset-1-data-1-qrwgb-nv7f4          0/1     Completed   0          20m
rook-ceph-osd-prepare-ocs-deviceset-2-data-0-h955g-v65vn          0/1     Completed   0          110m
rook-ceph-osd-prepare-ocs-deviceset-2-data-1-4kr99-ll9hm          0/1     Completed   0          110m
rook-ceph-rgw-ocs-storagecluster-cephobjectstore-a-58bd64458549   1/1     Running     0          19m
rook-ceph-rgw-ocs-storagecluster-cephobjectstore-b-664d8cdcl7tx   1/1     Running     0          19m
```
