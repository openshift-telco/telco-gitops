# OCP dual-stack (IPv4 & IPv6) notes:

- (OCP 4.8.x or earlier) Ingress VIP & API VIP can *only* be IPv4 or IPv6. This means an OCP dual-stack deployment can interact with the K8s API only over one of the stacks when using VIPs. A way to work around this is using an external LB that understands how to handle dual-stack
- The "default" CIDR for clusterNetwork and serviceNetwork is the first one listed in the array
- The order of the CIDR type on clusterNetwork & serviceNetwork must match or deployment will fail. Meaning, if the clusterNetwork list an IPv6 CIDR first, the serviceNetwork must also list an IPv6 CIDR first. Mixing one with IPv4 and one with IPv6 will fail installation or end up with an unusable cluster.
- When the Pod does not specify spec.ipFamilies or spec.ipFamilyPolicy, the Pod will only receive an IP from the "default" CIDR (as defined above). Please refer to upstream [Kubernetes docs](https://kubernetes.io/docs/concepts/services-networking/dual-stack/) for details on how to use dual stack in K8s.
- Kubernetes uses the [Happy Eyeballs](https://en.wikipedia.org/wiki/Happy_Eyeballs) algorithm (RFC 8305) to select the preferred IP stack for communication with another named object (e.g. FQDN) returning dual-stack addresses 
