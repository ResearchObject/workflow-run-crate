# WfExS-backend examples

These RO-Crate Workflow Run examples were generated running WfExS-backend.

There can be two RO-Crates for each execution, as one of them only contains
details gathered after staging the execution scenario but *before* the
execution, and the other one contains those details and all the provenance
gathered through and *after* the execution.

As WfExS-backend can run staged workflows more than once, all the different
executions are represented inside the generated RO-Crates as several
`CreateAction`. Also, CWL workflows are packed before they are run, so their
RO-Crates contain an additional CreateAction explaining the pack process from
the original workflow to the packed one.

Workflow execution error messages are also included. Also, a graphical representation
of the executed workflow is included. Due the nature of the different workflow
engines, this representation could be pre-computed before the execution
or after it. So, it is provided a copy of the representation for each execution.


## WOMBAT-Pipelines

* Nextflow workflow is available at https://github.com/wombat-p/WOMBAT-Pipelines

* Provenance RO-Crate from an execution using Docker containers. It includes a snapshot of the workflow: [wombat-pipelines_provenance](wombat-pipelines_provenance).


```bash
# Example of command line to generate this RO-Crate
python WfExS-backend.py -L workflow_examples/montblanc_config_gocryptfs.yaml staged-workdir create-prov-crate 047b6dfc-3547-4e09-92f8-df7143038ff4 /tmp/wombat-pipelines_provenance.zip --workflow --orcid 0000-0002-4806-5140 --licence https://spdx.org/licenses/CC-BY-4.0.html
```

## Wetlab2Variations (CWL flavor).

* CWL workflow is available at https://github.com/inab/Wetlab2Variations/blob/eosc-life/cwl-workflows/workflows/workflow.cwl

* Provenance RO-Crate from an execution using Singularity containers. It includes a snapshot of the consolidated workflow: [Wetlab2Variations_CWL_provenance](Wetlab2Variations_CWL_provenance)


```bash
# Example of command line to generate this RO-Crate
python WfExS-backend.py -L workflow_examples/local_config_gocryptfs.yaml staged-workdir create-prov-crate a37fee9e-4288-4a9e-b493-993a867207d0 /tmp/Wetlab2Variations_CWL_provenance.zip  --orcid 0000-0002-4806-5140  --licence https://spdx.org/licenses/CC-BY-4.0.html
```

## nf-core RNASeq

* Nextflow workflow is available at https://github.com/nf-core/rnaseq/

* Provenance RO-Crate from an execution using Singularity containers. It includes a snapshot of the consolidated workflow: [nfcore-rnaseq_provenance](nfcore-rnaseq_provenance).


```bash
# Example of command line to generate this RO-Crate
python WfExS-backend.py -L workflow_examples/bsclife002_config_docker_gocryptfs_20.yaml staged-workdir create-prov-crate 'sex-linked aortectasis' /tmp/example_nfcore_rnaseq_1.zip --orcid 0000-0002-4806-5140 --licence https://spdx.org/licenses/CC-BY-4.0.html
```

## COSIFER cwl workflow (using singularity)

* Generated RO-Crates contain a copy of the inputs, outputs and workflow.

* WfExS configuration file: [local_config_gocryptfs.yaml](https://github.com/inab/WfExS-backend/blob/b058b538f3334a4b8c657a541dc9b9fb40434f55/workflow_examples/local_config_gocryptfs.yaml)

* Stage description: [cosifer_test1_cwl_implicit_outputs_github.wfex.stage](https://github.com/inab/WfExS-backend/blob/b058b538f3334a4b8c657a541dc9b9fb40434f55/workflow_examples/ipc/cosifer_test1_cwl_implicit_outputs_github.wfex.stage)

* Staged RO-Crate: [cosifer-cwl_staged](cosifer-cwl_staged)

* Provenance RO-Crate: [cosifer-cwl_provenance](cosifer-cwl_provenance)


```bash
# Example of command line to generate this RO-Crate
python WfExS-backend.py -L workflow_examples/local_config_gocryptfs.yaml staged-workdir create-prov-crate 2400c32e-f875-4cd4-9d41-be6da8224c67 /tmp/cosifer-cwl_provenance.zip --inputs --outputs --workflow  --orcid 0000-0002-4806-5140 --orcid 0000-0003-4929-1219 --licence https://spdx.org/licenses/CC-BY-4.0.html
```

## COSIFER Nextflow workflow (using singularity)

* Generated RO-Crates contain a copy of the inputs, outputs and workflow.

* WfExS configuration file: [local_config_gocryptfs.yaml](https://github.com/inab/WfExS-backend/blob/b058b538f3334a4b8c657a541dc9b9fb40434f55/workflow_examples/local_config_gocryptfs.yaml)

* Stage description: [cosifer_test1_nxf.wfex.stage](https://github.com/inab/WfExS-backend/blob/b058b538f3334a4b8c657a541dc9b9fb40434f55/workflow_examples/ipc/cosifer_test1_nxf.wfex.stage)

* Staged RO-Crate: [cosifer-nxf_staged](cosifer-nxf_staged)

* Provenance RO-Crate: [cosifer-nxf_provenance](cosifer-nxf_provenance)


```bash
# Example of command line to generate this RO-Crate
python WfExS-backend.py -L workflow_examples/local_config_gocryptfs.yaml staged-workdir create-prov-crate 597708f2-952e-47c7-9b86-dbe3a9e5f651 /tmp/cosifer-nxf_provenance.zip --inputs --outputs --workflow --orcid 0000-0002-4806-5140 --orcid 0000-0003-4929-1219 --licence https://spdx.org/licenses/CC-BY-4.0.html
```
