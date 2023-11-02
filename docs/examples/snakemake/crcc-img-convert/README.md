Example of "manual" creation of an RO-Crate for an execution of [fair-crcc-img-convert](https://github.com/crs4/fair-crcc-img-convert/tree/main) on a slide from the [Cancer Moonshot Biobank - Prostate Cancer Collection (CMB-PCA)](https://doi.org/10.7937/25T7-6Y12). The crate is actually created by `gen_crate.py` from the `wf-prov` directory:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python gen_crate.py wf-prov -o fair-crcc-img-convert-run
```

See `README.md.crate` for additional information.

Note that the license for the RO-Crate is [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) except for the workflow, which is licensed under the [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).

Some files have been truncated to zero length to avoid bloating the repo. For instance, `MSB-02917-01-02.svs`.
