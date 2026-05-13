# Changelog

## 0.6-DRAFT

* Updated all three profiles and their examples to align with RO-Crate 1.2 and Workflow RO-Crate 1.1.
* The IRI mappings for the properties `input` and `output` have been updated in the [RO-Crate 1.2 JSON-LD context](https://www.researchobject.org/ro-crate/specification/1.2/context.jsonld). This means that from this version onward, Workflow Run Crate and Provenance Run Crate are not backward compatible with RO-Crate 1.1/Workflow RO-Crate 1.0.
    * `input` has changed from `https://bioschemas.org/ComputationalWorkflow#input` to `https://bioschemas.org/properties/input` .
    * `output` has changed from `https://bioschemas.org/ComputationalWorkflow#output` to `https://bioschemas.org/properties/output`.
