# Example of a WR RO-Crate capturing provenance data from WSI conversion

Example of "manual" creation of a [Workflow Run
RO-Crate](https://www.researchobject.org/workflow-run-crate/profiles/) to
capture provenance data from an execution of the
[fair-crcc-img-convert](https://github.com/crs4/fair-crcc-img-convert/tree/main)
workflow on a whole-slide image from the [Cancer Moonshot Biobank - Prostate
Cancer Collection (CMB-PCA)](https://doi.org/10.7937/25T7-6Y12). The crate is
actually created by `gen_crate.py` script found in the `wf-prov` directory. To
install its dependencies and run it use the following commands:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python gen_crate.py wf-prov -o fair-crcc-img-convert-run
```

See `README.md.crate` for additional information on the RO-Crate.

Note that the license for the RO-Crate is [CC BY
4.0](https://creativecommons.org/licenses/by/4.0/), except for the workflow,
which is licensed under the
[GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).

Some files have been truncated to zero length to avoid bloating the repo. For
instance, `MSB-02917-01-02.svs`.
