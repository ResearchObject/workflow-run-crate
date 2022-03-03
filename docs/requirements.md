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

## Competenency Questions / User stories

id | CQ description | Existing/new terms | Rationale | Issue # |
 | -- | -- | -- | -- | -- |
 CQ1 | What containers do I need to rerun this workflow? | container ID, image URL | |
 CQ2 | How much memory/cpu/disk was used, so that I can find the right hardware for running? | memory, disk, cpu, architecture, gpu |  |
 CQ3 | What are the configuration files used in a workflow execution step? | | I would like to capture configuration files for reproducibility purposes |  |
 CQ4 | What is the environment/container file used in a specific workflow execution step? | | Knowing the environment helps debugging and reproducing the setup |  |
 CQ5 | How long does this workflow component takes to run? (estimate) | | If a workflow step is computationally expensive, I may need to get an estimate for impatient users, or show a warning |  |
 CQ6 | How long does this workflow take to run? | | Same as CQ5, but with the full workflow |  |
 CQ7 | Was the workflow execution successful? | | Needed to know whether or not retrieve the results |  |
 CQ8 | What are the inputs and outputs of the overall workflow (I don't care about the intermediate results) |  | High level representation of the workflow execution |
