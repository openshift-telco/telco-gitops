# GitOps Principles

Based on CNCF Open GitOps [principles](https://github.com/open-gitops/documents/blob/v0.1.0/PRINCIPLES.md) as per active discussion in CNCF [GitOps Principles Working Group](https://github.com/open-gitops/documents/pull/9#issuecomment-867118191)

1. **Declaratively:** A system's desired state is declarative

    A system managed by GitOps must have its `Desired State` expressed declaratively as data in a format writable and readable by both humans and machines.

2. **Immutably:** Declarations are stored as immutable versions

    `Desired State` is stored in a way that supports versioning, immutability of versions, and retains a complete version history.

3. **Continuous Reconciliation:** State reconciliation is continuous

    Software agents continuously, and automatically, compare a system's `Actual State` to its `Desired State`. If the actual and desired states differ for any reason, automated actions to reconcile them are initiated.

4. **Declarative Operations:** Operations is through versioned mutation of the declaration

    The *only* mechanism through which the system is intentionally operated on is through these principles.
