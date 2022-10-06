---
title: Process Run Crate
---

* Part of: [Workflow Run RO-Crate](profile)
* Version: 0.1-DRAFT
* Authors: [Workflow Run RO-Crate members](index#community)


## Overview

Process Run Crate is the most coarse-grained level of the [Workflow Run RO-Crate profile](profile#profiles). It is used to describe the execution of an _implicit_ workflow, indicating that one or more computational tools have been executed, typically generating some result files that are represented as [data entities](https://www.researchobject.org/ro-crate/1.1/data-entities.html) in the RO-Crate.

By "implicit workflow" we mean that the composition of these tools may have been done by hand (a user executes one tool following another) or by some script that has not yet been included as part of the crate (for instance because it is an embedded part of a larger application).

This profile requires the indication of [Software used to create files](https://www.researchobject.org/ro-crate/1.1/provenance.html#software-used-to-create-files), namely a [SoftwareApplication](http://schema.org/SoftwareApplication) (the tool) and a [CreateAction](http://schema.org/CreateAction) (the execution of said tool).


## Example

```json
[
    {
        "@id": "./",
        "@type": "Dataset",
        "hasPart": [
            {"@id": "pics/2017-06-11%2012.56.14.jpg"},
            {"@id": "pics/sepia_fence.jpg"}
        ],
        "mentions": {"@id": "#SepiaConversion_1"},
        "name": "My Pictures"
    },
    {
        "@id": "https://www.imagemagick.org/",
        "@type": "SoftwareApplication",
        "url": "https://www.imagemagick.org/",
        "name": "ImageMagick",
        "version": "ImageMagick 6.9.7-4 Q16 x86_64 20170114"
    },
    {
        "@id": "#SepiaConversion_1",
        "@type": "CreateAction",
        "name": "Convert dog image to sepia",
        "description": "convert -sepia-tone 80% test_data/sample/pics/2017-06-11\\ 12.56.14.jpg test_data/sample/pics/sepia_fence.jpg",
        "endTime": "2018-09-19T17:01:07+10:00",
        "instrument": {"@id": "https://www.imagemagick.org/"},
        "object": {"@id": "pics/2017-06-11%2012.56.14.jpg"},
        "result": {"@id": "pics/sepia_fence.jpg"},
        "agent": {"@id": "https://orcid.org/0000-0001-9842-9718"}
    },
    {
        "@id": "pics/2017-06-11%2012.56.14.jpg",
        "@type": "File",
        "description": "Original image",
        "encodingFormat": "image/jpeg",
        "name": "2017-06-11 12.56.14.jpg (input)"
    },
    {
        "@id": "pics/sepia_fence.jpg",
        "@type": "File",
        "description": "The converted picture, now sepia-colored",
        "encodingFormat": "image/jpeg",
        "name": "sepia_fence (output)"
    },
    {
        "@id": "https://orcid.org/0000-0001-9842-9718",
        "@type": "Person",
        "name": "Stian Soiland-Reyes"
    }
]
```

Note that the command line shown in the action's `description` is not directly re-executable, as file paths are not required to match the RO-Crate locations. For a more structural and reproducible description of tool executions, see [Workflow Run Crate](workflow_run_crate).


## Requirements

<table>

  <tr>
   <td><strong>Property</strong></td>
   <td><strong>Required?</strong></td>
   <td><strong>Description</strong>
   </td>
  </tr>

  <tr>
   <td colspan="3"><strong>SoftwareApplication</strong> </td>
  </tr>

  <tr>
   <td>@type</td>
   <td>MUST</td>
   <td>SHOULD include <a href="http://schema.org/SoftwareApplication">SoftwareApplication</a>, <a href="http://schema.org/SoftwareSourceCode">SoftwareSourceCode</a> or <a href="https://bioschemas.org/ComputationalWorkflow">ComputationalWorkflow</a></td>
  </tr>

  <tr>
   <td>@id</td>
   <td>MUST</td>
   <td>SHOULD be an absolute URI, but MAY be a relative URI to a data entity in the crate (e.g. <code>"bin/simulation4"</code>) or a local identifier for tools that are not otherwise described on the web (e.g. <code>"#statistical-analysis"</code>)</td>
  </tr>

  <tr>
   <td>name</td>
   <td>SHOULD</td>
   <td>A human readable name for the tool <em>in general</em> (not just how it was used here)</td>
  </tr>

  <tr>
   <td>url</td>
   <td>SHOULD</td>
   <td>Homepage, documentation or source for the tool</td>
  </tr>

  <tr>
   <td>version</td>
   <td>SHOULD</td>
   <td>The version string for the software application</td>
  </tr>

  <tr>
   <td colspan="3"><strong>CreateAction</strong></td>
  </tr>

  <tr>
   <td>@type</td>
   <td>MUST</td>
   <td>SHOULD be <a href="http://schema.org/CreateAction">CreateAction</a> to indicate that this tool created the <code>result</code> data entities. MAY be <a href="http://schema.org/ActivateAction">ActivateAction</a> if the provenance does not include any <code>result</code>. MAY be <a href="http://schema.org/UpdateAction">UpdateAction</a> if the tool modified an existing data entity or database in-place.</td>
  </tr>

  <tr>
   <td>@id</td>
   <td>MUST</td>
   <td>A unique identifier for the execution, e.g. <code>"urn:uuid:50ec5c76-1f7a-4130-8ef6-846756b228c1"</code>, <code>"#f99a8e6c"</code>. MAY be an absolute URI, e.g. <a href="http://example.com/runs/846756b228c1">http://example.com/runs/846756b228c1</a>. The use of randomly generated <a href="https://datatracker.ietf.org/doc/html/rfc4122">UUIDs</a> (type 4) is RECOMMENDED. SHOULD be listed under <a href="http://schema.org/mentions">mentions</a> of the [root data entity](https://www.researchobject.org/ro-crate/1.1/root-data-entity.html).</td>
  </tr>

  <tr>
   <td>name</td>
   <td>SHOULD</td>
   <td>Short human-readable description of the execution.</td>
  </tr>

  <tr>
   <td>description</td>
   <td>SHOULD</td>
   <td>Details of the execution, for instance command line arguments or settings. This field is for information only, no particular structure is to be assumed.</td>
  </tr>

  <tr>
   <td>endTime</td>
   <td>SHOULD</td>
   <td>The time the process ended, i.e. when the result files have been created.</td>
  </tr>

  <tr>
   <td>startTime</td>
   <td>MAY</td>
   <td>The time the process started, i.e. the earliest time the process may have accessed its <code>object</code></td>
  </tr>

  <tr>
   <td>instrument</td>
   <td>MUST</td>
   <td>Identifier of the executed tool.</td>
  </tr>

  <tr>
   <td>agent</td>
   <td>SHOULD</td>
   <td>Identifier of a <a href="https://www.researchobject.org/ro-crate/1.1/contextual-entities.html#people">Person</a> or <a href="https://www.researchobject.org/ro-crate/1.1/contextual-entities.html#organizations-as-values">Organization</a> contextual entity that started/executed this tool.</td>
  </tr>

  <tr>
   <td>object</td>
   <td>MAY</td>
   <td>The identifier of one or more entities of the RO-Crate that were consumed by this action, e.g. input files or reference datasets.</td>
  </tr>

  <tr>
   <td>result</td>
   <td>SHOULD</td>
   <td>The identifier of one or more entities that were created or modified by this action, e.g. output files.</td>
  </tr>

</table>

Entities referenced by an action's [object](http://schema.org/object) or [result](http://schema.org/result) SHOULD be of type `File` (an RO-Crate alias for [MediaObject](http://schema.org/MediaObject)) or [Dataset](http://schema.org/Dataset) (directory), but MAY be a [CreativeWork](http://schema.org/CreativeWork) for other types of data (e.g. an online database); they MAY be of type [PropertyValue](http://schema.org/PropertyValue) to capture numbers/strings that are not stored as files.


## Multiple processes

A process crate can be used to indicate one single execution as a single `CreateAction`, or a series of processes that generate different data entities. These actions MAY form an *implicit workflow* by following the links between entities that appear as `result` in an action and as `object` in the following one, but a process crate is not required to ensure such consistency (e.g. there may be an intermediate action that has not been recorded).

<img alt="Multiple processes diagram" src="img/multiple_processes.svg" width="800" />