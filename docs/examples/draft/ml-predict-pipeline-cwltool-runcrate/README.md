# Run of digital pathology tissue/tumor prediction workflow

This dataset is an [RO-Crate](https://www.researchobject.org/ro-crate/) representation of an execution of the tissue/tumor prediction workflow for digital pathology from [crs4/deephealth-pipelines](https://github.com/crs4/deephealth-pipelines/tree/c54840df08742e3aa454394e0e74d15fbd640f07). It follows the [Provenance Run Crate](https://w3id.org/ro/wfrun/provenance/0.1) profile.

The workflow has been run with [cwltool](https://github.com/common-workflow-language/cwltool/tree/3.1.20230213100550), using the `--provenance` option to generate a [CWLProv](https://doi.org/10.1093/gigascience/giz095) RO bundle, and then converted to an RO-Crate using [runcrate](https://github.com/ResearchObject/runcrate/tree/755fb7f0a8ba6fc238a2cb7a3218175644eb78b5). The input dataset is [Mirax2-Fluorescence-2](https://openslide.cs.cmu.edu/download/openslide-testdata/Mirax/Mirax2-Fluorescence-2.zip) by Yves Sucaet, from the [MIRAX test data](https://openslide.cs.cmu.edu/download/openslide-testdata/Mirax/).

The workflow stored in the crate (`packed.cwl`) is a [packed](https://www.commonwl.org/v1.2/Workflow.html#Packed_documents) representation of the [workflow from crs4/deephealth-pipelines](https://github.com/crs4/deephealth-pipelines/tree/c54840df08742e3aa454394e0e74d15fbd640f07/cwl), released under the following license:

```
MIT License

Copyright (c) 2021-2023 CRS4

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
