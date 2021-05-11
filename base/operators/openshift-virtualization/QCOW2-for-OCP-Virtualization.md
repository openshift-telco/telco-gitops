# Preparing QCOW2 for OCP Virtualization

The following procedure applies to `OpenShift Virtualization` and `KubeVirt`.


## Obtaining a QCOW2 image 

- Obtain a qcow2 image

```bash
curl -L -o /var/lib/libvirt/images/centos7.qcow2 \
https://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud-2009.qcow2 
```

## Cutomizing a QCOW2 image 

Note: This procedure requires `libguestfs-tools`

```bash
yum install -y libguestfs-tools
```

- Apply desired customizations

```bash
export LIBGUESTFS_BACKEND=direct
virt-customize -a /var/lib/libvirt/images/centos7.qcow2  --root-password password:centos123
```

## Container from QCOW2 image

- Create `Containerfile` definition

```bash
# Containerfile
FROM registry.access.redhat.com/ubi8/ubi:latest AS builder
ADD --chown=107:107 centos7.qcow2 /disk/
RUN chmod 0440 /disk/*

FROM scratch
COPY --from=builder /disk/* /disk/
```

```bash
export LOCAL_REGISTRY=<registry.example.com:5000>
export LOCAL_REGISTRY_PATH=$LOCAL_REGISTRY/vms

# Build container
podman build --tag $LOCAL_REGISTRY_PATH/centos7:2009 --file Containerfile .

# Push container to local registry
podman push $LOCAL_REGISTRY_PATH/centos7:2009 $LOCAL_REGISTRY_PATH/centos7:2009
```
