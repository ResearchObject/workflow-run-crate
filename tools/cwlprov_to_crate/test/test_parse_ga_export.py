from provenance_profile import ProvenanceProfile
from load_ga_export import load_ga_history_export, GalaxyJob


def test_ga_history_loading(data_dir, tmpdir):
    export_dir = "test_ga_history_export"
    export_path = data_dir / export_dir / "history_export"

    metadata_export = load_ga_history_export(export_path)
    jobs = []
    for job in metadata_export["jobs_attrs"]:
        job_attrs = GalaxyJob()
        job_attrs.parse_ga_jobs_attrs(job)
        jobs.append(job_attrs.attributes)

        assert isinstance(job_attrs, GalaxyJob)

    assert len(jobs) == 4


def test_ga_history_parsing(data_dir, tmpdir):
    export_dir = "test_ga_history_export"
    export_path = data_dir / export_dir / "history_export"
    prov_path = tmpdir / "provenance"
    prov = ProvenanceProfile(export_path, "PDG", "https://orcid.org/0000-0002-8940-4946")

    assert isinstance(prov, ProvenanceProfile)

    prov.finalize_prov_profile(out_path=prov_path, serialize=True)
