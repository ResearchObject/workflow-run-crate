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

id | CQ description | Existing/new terms | Rationale | Profile[^1] | Issue # |
 | -- | -- | -- | -- | -- | -- |
 CQ1 | What container images (e.g., Docker) were used by the run? | Overload [image](http://schema.org/image)? The type of the target entity can be `File` if the image is a tarball from `docker save` | To archive images before they disappear so workflow can run later in time | 1, 3 | [~~9~~](https://github.com/ResearchObject/workflow-run-crate/issues/9) |
 CQ2 | How much memory/cpu/disk was used in run? | memory, disk, cpu, architecture, gpu  (possibly [memoryRequirements](http://schema.org/memoryRequirements) [storageRequirements](http://schema.org/storageRequirements)) | To find the right hardware for running workflow | 1, 2, 3 | [10](https://github.com/ResearchObject/workflow-run-crate/issues/10) |
 CQ3 | What are the configuration files used in a workflow execution step? | [ChooseAction](http://schema.org/ChooseAction)? Though maybe the crate generator should just merge the params with the other ones if it can parse the config file. To link to the config file as a black box instead we probably need a new property |For reproducibility purposes, the values/settings inside config files can have big impact on output | 1, 3 | [~~11~~](https://github.com/ResearchObject/workflow-run-crate/issues/11) |
 CQ4 | What is the environment/container file used in a specific workflow execution step? | Similar to the configuration file problem. Need env dump support from workflow engine | Knowing the environment helps debugging and reproducing the setup | 1, 3 | [12](https://github.com/ResearchObject/workflow-run-crate/issues/12) |
 CQ5 | How long does this workflow component take to run? (estimate) | [totalTime](http://schema.org/totalTime)? Allowed on [HowTo](http://schema.org/HowTo) and [HowToDirection](http://schema.org/HowToDirection) but not on [HowToStep](http://schema.org/HowToStep). Can also get actual duration from [endTime](http://schema.org/endTime) - [startTime](http://schema.org/startTime) on the action | If a workflow step is computationally expensive, I may need to get an estimate for impatient users, or show a warning | 1, 3 | [~~13~~](https://github.com/ResearchObject/workflow-run-crate/issues/13) |
 CQ6 | How long does this workflow take to run? | [totalTime](http://schema.org/totalTime). Can also get actual duration from [endTime](http://schema.org/endTime) - [startTime](http://schema.org/startTime) on the action | Same as CQ5, but with the full workflow | 2, 3 | [~~14~~](https://github.com/ResearchObject/workflow-run-crate/issues/14) |
 CQ7 | Was the execution successful? | [actionStatus](http://schema.org/actionStatus) to [FailedActionStatus](http://schema.org/FailedActionStatus) or [CompletedActionStatus](http://schema.org/CompletedActionStatus) - can also provide [error](http://schema.org/error) | Needed to know whether or not retrieve the results | 1, 2, 3 | [~~15~~](https://github.com/ResearchObject/workflow-run-crate/issues/15) |
 CQ8 | What are the inputs and outputs of the overall workflow (I don't care about the intermediate results) | [object](http://schema.org/object) and [result](http://schema.org/result) on the workflow run action | High level representation of the workflow execution | 2, 3 | [~~16~~](https://github.com/ResearchObject/workflow-run-crate/issues/16) |
 CQ9 | What is the source code version of the component executed in a workflow step? Is it a script? and executable? | [softwareVersion](http://schema.org/softwareVersion), though getting the version of the actual tool (e.g., `grep`) that was called by the wrapper might not be easy | Knowing which release/software version was used (reproducibility) | 1, 3 | [~~17~~](https://github.com/ResearchObject/workflow-run-crate/issues/17) |
 CQ10 | What is the script used to wrap up a software component? | We're mapping tool wrappers (e.g., `foo.cwl`) to [SoftwareApplication](http://schema.org/SoftwareApplication). Wrappers at lower levels can also be `SoftwareApplication`, but we need to draw the line somewhere | Many executables are complicated, and need an additional script to wrap them up or simplify. For example a "run.sh" script that exposes a simpler set of parameters and fixes another set. | 3 | [~~18~~](https://github.com/ResearchObject/workflow-run-crate/issues/18) |
 CQ11 | How were workflow parameters used in tool runs? | We're linking tool params directly (with [connectedTo](http://schema.org/connectedTo)), but that's inaccurate since those links only exist within a workflow. | Knowing how workflow parameters were passed to individual tools to find out how they affected the outputs | 3 | [~~25~~](https://github.com/ResearchObject/workflow-run-crate/issues/25) |

[^1]: 1: [Process Run Crate](process_run_crate); 2: [Workflow Run Crate](workflow_run_crate); 3: [Provenance Run Crate](provenance_run_crate).
