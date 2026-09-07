# Changelog

## 0.6

* Updated all three profiles and their examples to align with RO-Crate 1.3 and Workflow RO-Crate 1.1.
* The IRI mappings for `ComputationalWorkflow`, `FormalParameter`, `input`, and `output` were updated in the [RO-Crate 1.3 JSON-LD context](https://www.researchobject.org/ro-crate/specification/1.3/context.jsonld). This means that from this version onward, Workflow Run Crate and Provenance Run Crate are not backward compatible with RO-Crate 1.1/Workflow RO-Crate 1.0. The changes are shown in the table below:

    | Term | RO-Crate 1.3 context (latest) | RO-Crate 1.2 context | RO-Crate 1.1 context |
    | --- | --- | --- | --- |
    | ComputationalWorkflow | <https://bioschemas.org/terms/ComputationalWorkflow> | https://bioschemas.org/ComputationalWorkflow | https://bioschemas.org/ComputationalWorkflow |
    | FormalParameter | <https://bioschemas.org/terms/FormalParameter> | https://bioschemas.org/FormalParameter | https://bioschemas.org/FormalParameter |
    | input | <https://bioschemas.org/terms/input> | https://bioschemas.org/properties/input | https://bioschemas.org/ComputationalWorkflow#input |
    | output | <https://bioschemas.org/terms/output> | https://bioschemas.org/properties/output | https://bioschemas.org/ComputationalWorkflow#output |

    Note that `ComputationalWorkflow` and `FormalParameter` did not have IRI changes between 1.1 and 1.2, whereas `input` and `output` had IRI changes between all three versions.

* Implementers should further note: while RO-Crate 1.2 was never formally supported by the Process Run Crate, Workflow Run Crate, or Provenance Run Crate profiles, there may nonetheless be crates which declare conformance to both RO-Crate 1.2 and one or more of these profiles, and therefore use the RO-Crate 1.2 context mappings.

## Compatibility table

| RO-Crate version | Workflow RO-Crate version | Compatible Workflow Run RO-Crate version(s) |
| --- | --- | --- |
| 1.1 | 1.0 | 0.1 - 0.5 |
| 1.2 | None | None |
| 1.3 | 1.1 | 0.6 |
| later minor versions | 1.1, unless context changes are made that affect terms used in the profile | 0.6, unless context changes are made that affect terms used in the profiles |
