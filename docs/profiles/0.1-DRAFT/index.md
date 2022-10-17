---
title: The Workflow Run RO-Crate Profile Collection
---


# The Workflow Run RO-Crate Profile Collection

This section defines three [RO-Crate profiles](https://www.researchobject.org/ro-crate/profiles.html) for capturing the provenance of an execution of a computational workflow with increasing granularity:

* [Process Run Crate](process_run_crate) can be used to describe the execution of one or more tools that contribute to the same computation;
* [Workflow Run Crate](workflow_run_crate) is similar to Process Run Crate, but assumes that the coordinated execution of the tools is driven by a [computational workflow](https://bioschemas.org/types/ComputationalWorkflow/1.0-RELEASE)
* [Provenance Run Crate](provenance_run_crate) extends Workflow Run Crate with guidelines for describing the internal details of each step of the workflow.

All of the above profiles extend the [RO-Crate recommendations on representing software used to create files](https://www.researchobject.org/ro-crate/1.1/provenance.html#software-used-to-create-files).
