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

| Q  |  New terms? | Issue |
| -- | -- | -- |
| What containers do I need to rerun this workflow? | container ID, image URL |

