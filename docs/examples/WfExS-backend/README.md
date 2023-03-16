# WfExS-backend examples

These RO-Crate Workflow Run examples were generated running WfExS-backend.

There are two RO-Crates for each execution, as one of them only contains
details gathered after staging the execution scenario but *before* the
execution, and the other one contains those details and all the provenance
gathered through and *after* the execution.

As WfExS-backend can run staged workflows more than once, all the different
executions should be represented inside the generated RO-Crates.

## COSIFER cwl workflow

* WfExS configuration file: [local_config_gocryptfs.yaml](https://github.com/inab/WfExS-backend/blob/b058b538f3334a4b8c657a541dc9b9fb40434f55/workflow_examples/local_config_gocryptfs.yaml)

* Stage description: [cosifer_test1_cwl_implicit_outputs_github.wfex.stage](https://github.com/inab/WfExS-backend/blob/b058b538f3334a4b8c657a541dc9b9fb40434f55/workflow_examples/ipc/cosifer_test1_cwl_implicit_outputs_github.wfex.stage)

* Staged RO-Crate: [cosifer-cwl_staged](cosifer-cwl_staged)

* Provenance RO-Crate: [cosifer-cwl_provenance](cosifer-cwl_provenance)

## COSIFER Nextflow workflow

* WfExS configuration file: [local_config_gocryptfs.yaml](https://github.com/inab/WfExS-backend/blob/b058b538f3334a4b8c657a541dc9b9fb40434f55/workflow_examples/local_config_gocryptfs.yaml)

* Stage description: [cosifer_test1_nxf.wfex.stage](https://github.com/inab/WfExS-backend/blob/b058b538f3334a4b8c657a541dc9b9fb40434f55/workflow_examples/ipc/cosifer_test1_nxf.wfex.stage)

* Staged RO-Crate: [cosifer-nxf_staged](cosifer-nxf_staged)

* Provenance RO-Crate: [cosifer-nxf_provenance](cosifer-nxf_provenance)
