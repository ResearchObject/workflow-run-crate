# Workflow Run RO-Crate website

The website is the `docs/` folder, built by GitHub Pages (Jekyll, `jekyll-theme-slate`) and published at <https://www.researchobject.org/workflow-run-crate/>.

## Never edit `docs/profiles/`

**Do not modify anything under `docs/profiles/` unless explicitly asked.** Those files are the deployed, versioned profiles (`0.1` ... `0.6`, `0.7-DRAFT`, and the symlinks `index.md`, `changelog.md`, `img`, `process_run_crate/`, `workflow_run_crate/`, `provenance_run_crate/`, which point at the latest release, `0.6`). Published versions are cited by their `w3id.org` permalinks and Zenodo DOIs, so they must stay as released. This includes `docs/profiles/index.md` and `changelog.md`.

## Skill: updating the website

Pages normally updated: `docs/index.md` (landing page) and `docs/outreach.md` (citations, publications, presentations). Also `docs/requirements.md` and `docs/cwl_param_mapping.md`.

1. **Inspect** the current pages and `git log` before changing anything; check what is already listed (grep for the URL/DOI) to avoid duplicates.
2. **Search for new material**: publications, specs, software, example crates, training. Look at the project's actual repo/paper rather than search snippets, and verify the claims you write (which profile and version it uses, version/release, licence, date).
3. **Place it in the right section of `docs/index.md`**:
   - *Implementations & examples* table: engines producing WRROC (Profile, version URL, example DOI). Keep the row format.
   - *Profiles building on WRROC*: profiles that extend or recommend WRROC. Say "recommends" if they do not formally extend.
   - *Tools*, *Training and outreach*, *Related Work* (loosely related profiles and approaches).
   - *Citation* and `docs/outreach.md`: papers (newest first under year headings), spec citations (permalink and Zenodo DOI), theses and posters.
4. **Too early or unverified?** Do not list it. Add an HTML comment `<!-- TODO: ... -->` after the Implementations table with the link, why it is held back, and the date, so it is not rendered.
5. **Members**: the members list in `docs/index.md` (`- Name <ORCID URL>` lines) is parsed by `tools/get_members.py` into `members.json`; keep that line format.
6. **Review and commit**: show `git diff` and commit with a short message.

## Git

**Never push to `main` unless explicitly asked.** Commit locally and wait for the request to push.

## Style

- Plain Markdown, existing tone; ORCIDs as `<https://orcid.org/...>`; DOIs as `https://doi.org/...`.
- Do not claim support for WRROC profiles that the source does not state.
