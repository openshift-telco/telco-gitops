# TELCO GITOPS "AS-IS" REFERENCES

> :heavy_exclamation_mark: *Red Hat does not provide commercial support for the content of these repos*

```bash
#############################################################################
DISCLAIMER: THESE ARE UNSUPPORTED COMMUNITY TOOLS.

THE REFERENCES ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#############################################################################
```

The design philosophy of this repository follows these [GitOps Principles](GitOps-Principles.md) to deploy, manage and operate OpenShift clusters for Telco use cases.

| Directory  | Description                                                               |
|------------|---------------------------------------------------------------------------|
| /base      | contains common operators and configs manifests for Telco blueprints      |
| /blueprints| various Telco cluster type configurations blueprints                      |
| /clusters  | various example cluster configurations for labs                           |
| /cnf       | various CNF examples                                                      |


## Development structure

> :heavy_exclamation_mark: *This work is under heavy development -- no guarantees of backwards compatibility on changes on `main` branch*

| Branch     | Description                                                          | Status                            |
|------------|----------------------------------------------------------------------|-----------------------------------|
| main       | Development branch using stable OCP releases and upcoming releases.  | Fast-moving development           |
| ocp-4.8    | GitOps structure used for OpenShift 4.8.x stable releases            | Balanced and steady progress      |
| ocp-4.7    | GitOps structure used for OpenShift 4.7.x stable releases            | No changes. Bug Fixes only        |
| ocp-4.6    | GitOps structure used for OpenShift 4.6.16 to 4.6.18 releases.       | No longer maintained (unreleased) |


**NOTE:** This is `main` branch. Currently being refactored with OCP 4.8 as default.
