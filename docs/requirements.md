---
title: Requirements for Workflow Run Crate
---

## Previous requirement gathering exercises

- [WfExS possible RO-Crate profiles](https://docs.google.com/document/d/1ALo0yQITwrzvmRPGzNqdG3zstr0XZ1FSliBjU2CNNwY/edit)
- [2021-02 Workflow run RO-crate draft](https://docs.google.com/document/d/1joew-17-C53xbi7xWdc-VWSMSrikA84J2wvy2Zv9Zvc/edit#)
- [2020-10-28 Workflow Run RO-Crate discussion](https://docs.google.com/document/d/1E02lUmHBBDrXi0JsQ9FZd4rXecl3XNfoGJuMfuQ2X2M/edit)
- [Profile for recording workflow runs](https://www.researchobject.org/2021-packaging-research-artefacts-with-ro-crate/manuscript.html#profile-for-recording-workflow-runs) (conceptual ideas from RO-Crate paper)

## Key concept

- Extend, nest or reference a [Workflow Crate](https://w3id.org/workflowhub/workflow-ro-crate/) for the workflow that has been executed
- Use [Provenance of software run](https://www.researchobject.org/ro-crate/1.1/provenance.html) to detail that a workflow run has occurred
- Recommend [CWLProv-like](https://w3id.org/cwl/prov/0.6.0) structure of RO-Crate folders for inputs/outputs/intermediate?
- Optional detailed workflow run provenance in separate PROV files

## Competency Questions / User stories

id | CQ description | Existing/new terms | Rationale | Issue # |
 | -- | -- | -- | -- | -- |
 CQ1 | What containers were used by run? | container ID, image URL | To archive images before they disappear so workflow can run later in time | |
 CQ2 | How much memory/cpu/disk was used in run? | memory, disk, cpu, architecture, gpu  (possibly http://schema.org/memoryRequirements http://schema.org/storageRequirements ) | To find the right hardware for running workflow |  |
 CQ3 | What are the configuration files used in a workflow execution step? | http://schema.org/actionOption ? |For reproducibility purposes, the values/settings inside config files can have big impact on output |  |
 CQ4 | What is the environment/container file used in a specific workflow execution step? | | Knowing the environment helps debugging and reproducing the setup |  |
 CQ5 | How long does this workflow component takes to run? (estimate) | | If a workflow step is computationally expensive, I may need to get an estimate for impatient users, or show a warning |  |
 CQ6 | How long does this workflow take to run? | | Same as CQ5, but with the full workflow |  |
 CQ7 | Was the workflow execution successful? | http://schema.org/actionStatus to http://schema.org/FailedActionStatus or http://schema.org/CompletedActionStatus  - can also provide https://schema.org/error | Needed to know whether or not retrieve the results |  |
 CQ8 | What are the inputs and outputs of the overall workflow (I don't care about the intermediate results) |  | High level representation of the workflow execution |
 CQ9 | What is the source code version of the component executed in a workflow step? Is it a script? and executable? | | Knowing which release/software version was used (reproducibility) |
 CQ10 | What is the script used to wrap up a software component? | | Many executables are complicated, and need an additional script to wrap them up or simplify. For example a "run.sh" script that exposes a simpler set of parameters and fixes another set. |
