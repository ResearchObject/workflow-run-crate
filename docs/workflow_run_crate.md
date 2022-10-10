---
title: Workflow Run Crate
---


# Workflow Run Crate

* Part of: [Workflow Run RO-Crate](profile)
* Version: 0.1-DRAFT
* Authors: [Workflow Run RO-Crate members](index#community)


## Overview

This profile is used to describe the execution of a computational tool that has orchestrated the execution of other tools. Such a tool is represented as a [workflow](https://www.researchobject.org/ro-crate/1.1/workflows.html) that can be executed using a *workflow engine* (e.g. [cwltool](https://github.com/common-workflow-language/cwltool)).

This profile is a combination of [Process Run Crate](process_run_crate) and [Workflow RO-Crate](https://w3id.org/workflowhub/workflow-ro-crate/). The entity referenced by the action's `instrument` SHOULD be a `ComputationalWorkflow` that is further described according to the Workflow RO-Crate requirements. The `mainEntity` of the RO-Crate MUST be the workflow that has been executed. The crate SHOULD have only one `CreateAction` corresponding to the workflow's execution. Details regarding the execution of individual workflow steps can be described with the [Provenance Run Crate](provenance_run_crate) profile.

Some workflows have multiple inputs/outputs that, in conformance with the [Bioschemas ComputationalWorkflow profile](https://bioschemas.org/profiles/ComputationalWorkflow/1.0-RELEASE) are defined as [FormalParameter](https://bioschemas.org/types/FormalParameter/1.0-RELEASE) entities. It is OPTIONAL to include these definitions on a `ComputationalWorkflow`. A data entity or `PropertyValue` that realizes a `FormalParameter` definition SHOULD refer to it via [exampleOfWork](https://schema.org/exampleOfWork); additionally, if the data entity or `PropertyValue` is an illustrative example of the parameter, the latter MAY refer back to the former using the reverse property [workExample](https://schema.org/workExample). This links the `input` of a `ComputationalWorkflow` to the `object` of a `CreateAction`, and the `output` of a `ComputationalWorkflow` to the `result` of a `CreateAction`. A `FormalParameter` that maps to a `PropertyValue` SHOULD have a subclass of [DataType](https://schema.org/DataType) (e.g., [Integer](https://schema.org/Integer)) &ndash; or [PropertyValue](https://schema.org/PropertyValue), in the case of dictionary-like structured types &ndash; as its `additionalType`.


## Example

```json
[
    {
        "@id": "./",
        "@type": "Dataset",
        "hasPart": [
            {"@id": "Galaxy-Workflow-Hello_World.ga"},
            {"@id": "inputs/abcdef.txt"},
            {"@id": "outputs/Select_first_on_data_1_2.txt"},
            {"@id": "outputs/tac_on_data_360_1.txt"}
        ],
        "license": {"@id": "http://spdx.org/licenses/CC0-1.0"},
        "mainEntity": {"@id": "Galaxy-Workflow-Hello_World.ga"},
        "mentions": {"@id": "#wfrun-5a5970ab-4375-444d-9a87-a764a66e3a47"}
    },
    {
        "@id": "Galaxy-Workflow-Hello_World.ga",
        "@type": ["File", "SoftwareSourceCode", "ComputationalWorkflow"],
        "name": "Hello World (Galaxy Workflow)",
        "author": {"@id": "https://orcid.org/0000-0001-9842-9718"},
        "creator": {"@id": "https://orcid.org/0000-0001-9842-9718"},
        "conformsTo": {"@id": "https://bioschemas.org/profiles/ComputationalWorkflow/1.0-RELEASE"},
        "programmingLanguage": {"@id": "https://w3id.org/workflowhub/workflow-ro-crate#galaxy"},
        "input": [
            {"@id": "#simple_input"},
            {"@id": "#verbose-param"}
        ],
        "output": [
            {"@id": "#reversed"},
            {"@id": "#last_lines"}
        ]
    },
    {
        "@id": "#simple_input",
        "@type": "FormalParameter",
        "additionalType": "File",
        "conformsTo": {"@id": "https://bioschemas.org/profiles/FormalParameter/1.0-RELEASE"},
        "description": "A simple set of lines in a text file",
        "encodingFormat": [
            "text/plain",
            {"@id": "http://edamontology.org/format_2330"}
        ],
        "workExample": {"@id": "inputs/abcdef.txt"},
        "name": "Simple input",
        "valueRequired": "True"
    },
    {
        "@id": "#verbose-param",
        "@type": "FormalParameter",
        "additionalType": "Boolean",
        "conformsTo": {"@id": "https://bioschemas.org/profiles/FormalParameter/1.0-RELEASE"},
        "description": "Increase logging output",
        "workExample": {"@id": "#verbose-pv"},
        "name": "verbose",
        "valueRequired": "False"
    },
    {
        "@id": "#reversed",
        "@type": "FormalParameter",
        "additionalType": "File",
        "conformsTo": {"@id": "https://bioschemas.org/profiles/FormalParameter/1.0-RELEASE"},
        "description": "All the lines, reversed",
        "encodingFormat": [
            "text/plain",
            {"@id": "http://edamontology.org/format_2330"}
        ],
        "name": "Reversed lines",
        "workExample": {"@id": "outputs/tac_on_data_360_1.txt"}
    },
    {
        "@id": "#last_lines",
        "@type": "FormalParameter",
        "additionalType": "File",
        "conformsTo": {"@id": "https://bioschemas.org/profiles/FormalParameter/1.0-RELEASE"},
        "description": "The last lines of workflow input are the first lines of the reversed input",
        "encodingFormat": [
            "text/plain",
            {"@id": "http://edamontology.org/format_2330"}
        ],
        "name": "Last lines",
        "workExample": {"@id": "outputs/Select_first_on_data_1_2.txt"}
    },
    {
        "@id": "https://orcid.org/0000-0001-9842-9718",
        "@type": "Person",
        "name": "Stian Soiland-Reyes"
    },
    {
        "@id": "https://w3id.org/workflowhub/workflow-ro-crate#galaxy",
        "@type": "ComputerLanguage",
        "identifier": "https://galaxyproject.org/",
        "name": "Galaxy",
        "url": "https://galaxyproject.org/"
    },
    {
        "@id": "#wfrun-5a5970ab-4375-444d-9a87-a764a66e3a47",
        "@type": "CreateAction",
        "name": "Galaxy workflow run 5a5970ab-4375-444d-9a87-a764a66e3a47",
        "endTime": "2018-09-19T17:01:07+10:00",
        "instrument": {"@id": "Galaxy-Workflow-Hello_World.ga"},
        "subjectOf": {"@id": "https://usegalaxy.eu/u/5dbf7f05329e49c98b31243b5f35045c/p/invocation-report-a3a1d27edb703e5c"},
        "object": [
            {"@id": "inputs/abcdef.txt"},
            {"@id": "#verbose-pv"}
        ],
        "result": [
            {"@id": "outputs/Select_first_on_data_1_2.txt"},
            {"@id": "outputs/tac_on_data_360_1.txt"}
        ]
    },
    {
        "@id": "inputs/abcdef.txt",
        "@type": "File",
        "description": "Example input, a simple text file",
        "encodingFormat": "text/plain",
        "exampleOfWork": {"@id": "#simple_input"}
    },
    {
        "@id": "#verbose-pv",
        "@type": "PropertyValue",
        "exampleOfWork": {"@id": "#verbose-param"},
        "name": "verbose",
        "value": "True"
    },
    {
        "@id": "outputs/Select_first_on_data_1_2.txt",
        "@type": "File",
        "name": "Select_first_on_data_1_2 (output)",
        "description": "Example output of the last (aka first of reversed) lines",
        "encodingFormat": "text/plain",
        "exampleOfWork": {"@id": "#last_lines"}
    },
    {
        "@id": "outputs/tac_on_data_360_1.txt",
        "@type": "File",
        "name": "tac_on_data_360_1 (output)",
        "description": "Example output of the reversed lines",
        "encodingFormat": "text/plain",
        "exampleOfWork": {"@id": "#reversed"}
    },
    {
        "@id": "https://usegalaxy.eu/u/5dbf7f05329e49c98b31243b5f35045c/p/invocation-report-a3a1d27edb703e5c",
        "@type": "CreativeWork",
        "encodingFormat": "text/html",
        "datePublished": "2021-11-18T02:02:00Z",
        "name": "Workflow Execution Summary of Hello World"
    }
]
```


## Requirements

The requirements of this profile are those of [Process Run Crate](process_run_crate) plus those of [Workflow RO-Crate](https://w3id.org/workflowhub/workflow-ro-crate/). In particular, the entity acting as the `instrument` of the `CreateAction` MUST be the `mainEntity` of the crate, whose types include `File`, `SoftwareSourceCode` and `ComputationalWorkflow`.
