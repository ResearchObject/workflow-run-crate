# Test data


## revsort-run-1

[CWLProv RO Example from the CWLProv repository](https://github.com/common-workflow-language/cwlprov/tree/ce3f469745f4c8a2c029f872d522a4c57fba947b/examples/revsort-run-1).

License: [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

* © 2015-2018 Common Workflow Language contributors https://www.commonwl.org/#Individual_Contributors
* © 2018 Software Freedom Conservancy (SFC) https://sfconservancy.org/


## revsortlcase-run-1

Nested workflows example. The first step uses a simplified implementation of [revsort](#revsort-run-1) as a subworkflow, while the second calls a tool that converts all lines to lower case.


## exome-alignment-packed.cwl

Packed (`cwltool --pack`) version of the [exome alignment workflow](https://github.com/inab/ipc_workflows/blob/fefede132f217184a25767fc4f42e2ae4606ff25/exome/alignment/workflow.cwl) from [inab/ipc_workflows@fefede1](https://github.com/inab/ipc_workflows/tree/fefede132f217184a25767fc4f42e2ae4606ff25), with step order altered to make it more distant from the topological order.

License: [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

WorkflowHub entry: https://workflowhub.eu/workflows/239


## no-output-run-1

Copy of `prov_data_annotations/example2/ro_old` from [RenskeW/cwlprov-provenance](https://github.com/RenskeW/cwlprov-provenance/tree/f5dd87a950eeaf7f96bd39dc218164832ff3cbea/prov_data_annotations/example2/ro_old).

License: [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)


## grepucase-run-1

For each file in the input directory, search for the specified pattern, convert matching lines to upper case and write results to a file in the output directory. Used to test support for directory I/O.


## echo-scatter-run-1

Write all strings in the input array to stdout. Used to test support for scatter jobs.


## no-input-run-1

Output a predefined integer. Used to test support for tools / workflows that take no input.


## type-zoo-run-1

Build a fake command line and write it to the output file (all parameter settings are passed to the echo tool). Used to test support for various parameter types.
