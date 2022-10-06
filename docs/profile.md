---
title: Workflow Run RO-Crate Profile
---

* Version: 0.1-DRAFT
* Authors: [Workflow Run RO-Crate members](index#community)


## Overview

Workflow Run RO-Crate defines an [RO-Crate profile](https://www.researchobject.org/ro-crate/profiles.html) for capturing the provenance of an execution of a computational workflow.


## Concepts

The Workflow Run RO-Crate profile uses terminology from the [RO-Crate 1.1 specification](https://w3id.org/ro/crate/1.1).


## Profiles

The Workflow Run RO-Crate profile is defined in three levels of increasing granularity, which extend [RO-Crate 1.1](https://www.researchobject.org/ro-crate/1.1/provenance.html#software-used-to-create-files) to specify ways to capture the execution of a computational workflow:

* [Process Run Crate](process_run_crate) can be used to describe the execution of one or more tools that contribute to the same computation;
* [Workflow Run Crate](workflow_run_crate) is similar to Process Run Crate, but assumes that the coordinated execution of the tools is driven by a [computational workflow](https://bioschemas.org/types/ComputationalWorkflow/1.0-RELEASE)
* [Provenance Run Crate](provenance_run_crate) extends Workflow Run Crate with guidelines for describing the internal details of each step of the workflow.
