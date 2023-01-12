---
title: Workflow Run Crate
---


# Workflow Run Crate

* Version: 0.1-DRAFT
* Permalink: <https://w3id.org/ro/wfrun/workflow/0.1-DRAFT> `TODO: update`
* Authors: [Workflow Run RO-Crate members](/workflow-run-crate/#community)

This profile uses terminology from the [RO-Crate 1.1 specification](https://w3id.org/ro/crate/1.1).


## Overview

This profile is used to describe the execution of a computational tool that has orchestrated the execution of other tools. Such a tool is represented as a [workflow](https://www.researchobject.org/ro-crate/1.1/workflows.html) that can be executed using a *workflow engine* (e.g. [cwltool](https://github.com/common-workflow-language/cwltool)).

This profile is a combination of [Process Run Crate](process_run_crate) and [Workflow RO-Crate](https://w3id.org/workflowhub/workflow-ro-crate/). The entity referenced by the action's `instrument` (which represents the software application that's been run) MUST be a `ComputationalWorkflow` that is further described according to the Workflow RO-Crate requirements. In particular, it MUST be the [mainEntity](http://schema.org/mainEntity) of the RO-Crate. The crate SHOULD have only one `CreateAction` corresponding to the workflow's execution. Details regarding the execution of individual workflow steps can be described with the [Provenance Run Crate](provenance_run_crate) profile.

Some workflows have multiple inputs/outputs that, in conformance with the [Bioschemas ComputationalWorkflow profile](https://bioschemas.org/profiles/ComputationalWorkflow/1.0-RELEASE) are defined as [FormalParameter](https://bioschemas.org/types/FormalParameter/1.0-RELEASE) entities. It is OPTIONAL to include these definitions on a `ComputationalWorkflow`. A data entity or `PropertyValue` that realizes a `FormalParameter` definition SHOULD refer to it via [exampleOfWork](https://schema.org/exampleOfWork); additionally, if the data entity or `PropertyValue` is an illustrative example of the parameter, the latter MAY refer back to the former using the reverse property [workExample](https://schema.org/workExample). This links the `input` of a `ComputationalWorkflow` to the `object` of a `CreateAction`, and the `output` of a `ComputationalWorkflow` to the `result` of a `CreateAction`. An `object` item that does not match a slot in the workflow's input interface (e.g., a [configuration file](process_run_crate#referencing-configuration-files) read from a predefined path) MUST NOT refer to a `FormalParameter` of the `ComputationalWorkflow` via `exampleOfWork`. A `FormalParameter` that maps to a `PropertyValue` SHOULD have a subclass of [DataType](https://schema.org/DataType) (e.g., [Integer](https://schema.org/Integer)) &mdash; or [PropertyValue](https://schema.org/PropertyValue), in the case of dictionary-like structured types &mdash; as its `additionalType`. See [CWL parameter mapping](/workflow-run-crate/cwl_param_mapping) for an example.


## Example

```json
{ "@context": "https://w3id.org/ro/crate/1.1/context", 
  "@graph": [
    {
        "@id": "ro-crate-metadata.json",
        "@type": "CreativeWork",
        "about": {"@id": "./"},
        "conformsTo": [
            {"@id": "https://w3id.org/ro/crate/1.1"},
            {"@id": "https://w3id.org/workflowhub/workflow-ro-crate/1.0"}
        ]
    },
    {
        "@id": "./",
        "@type": "Dataset",
        "conformsTo": [
            { "@id": "https://w3id.org/ro/wfrun/process/0.1" },
            { "@id": "https://w3id.org/ro/wfrun/workflow/0.1" },
            { "@id": "https://w3id.org/workflowhub/workflow-ro-crate/1.0"}            
        ],
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
    {   "@id": "https://w3id.org/ro/wfrun/process/0.1",
        "@type": "CreativeWork",
        "name": "Process Run Crate",
        "version": "0.1"
    },
    {   "@id": "https://w3id.org/ro/wfrun/workflow/0.1",
        "@type": "CreativeWork",
        "name": "Workflow Run Crate",
        "version": "0.1"
    },
    {   "@id": "https://w3id.org/workflowhub/workflow-ro-crate/1.0",
        "@type": "CreativeWork",
        "name": "Workflow RO-Crate",
        "version": "1.0"
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

This profile inherits the requirements of [Process Run Crate](process_run_crate) and [Workflow RO-Crate](https://w3id.org/workflowhub/workflow-ro-crate/). In particular, the entity acting as the `instrument` of the `CreateAction` MUST be the *main workflow*. This and other additional specifications are listed below.

<table>

  <tr>
   <td><strong>Property</strong></td>
   <td><strong>Required?</strong></td>
   <td><strong>Description</strong></td>
  </tr>

  <tr>
   <th colspan="3"><strong>Dataset</strong> (the <a href="https://www.researchobject.org/ro-crate/1.1/root-data-entity.html">root data entity</a>, e.g. <code>"@id": "./"</code>)</th>
  </tr>
  <tr>
   <td>conformsTo</td>
   <td>MUST</td>
   <td>Array MUST reference a <code>CreativeWork</code> entity with an <code>@id</code> URI that is consistent with the versioned <em>Permalink</em> of this document, and SHOULD also reference versioned permalinks for <a href="https://w3id.org/ro/wfrun/process/0.1">Process Run Crate</a> and <a href="https://w3id.org/workflowhub/workflow-ro-crate/1.0">Workflow RO-Crate</a>.
  </tr>

  <tr>
   <th colspan="3"><strong>CreateAction</strong></th>
  </tr>

  <tr>
   <td>instrument</td>
   <td>MUST</td>
   <td>Identifier of the <em>main workflow</em>, as specified in <a href="https://w3id.org/workflowhub/workflow-ro-crate/">Workflow RO-Crate</a>.</td>
  </tr>

  <tr>
   <th colspan="3"><strong>FormalParameter</strong></th>
  </tr>

  <tr>
   <td>workExample</td>
   <td>MAY</td>
   <td>Identifier of the data entity or <code>PropertyValue</code> instance that realizes this parameter. The data entity or <code>PropertyValue</code> instance SHOULD refer to this parameter via <a href="http://schema.org/exampleOfWork">exampleOfWork</a>.</td>
  </tr>

  <tr>
   <td>additionalType</td>
   <td>MUST</td>
   <td>SHOULD include: <code>File</code> or <code>Dataset</code> if it maps to a file or directory, respectively; <code>PropertyValue</code> if it maps to a dictionary-like structured value (e.g. a CWL <em>record</em>); <a href="http://schema.org/DataType">DataType</a> or one of its subtypes (e.g. <a href="http://schema.org/Integer">Integer</a>) if it maps to a non-structured value. A more specific type MAY be used instead of <code>File</code> when appropriate (see <a href="http://schema.org/MediaObject#subtypes">MediaObject subtypes</a>), e.g. <a href="http://schema.org/ImageObject">ImageObject</a>. Note that multiple types can apply, e.g. <code>["File", "http://edamontology.org/data_3671"]</code>.</td>
  </tr>

</table>
