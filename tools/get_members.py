import json
from pathlib import Path
import re

THIS_DIR = Path(__file__).absolute().parent
INDEX_FILE = THIS_DIR.parent / "docs" / "index.md"
MEMBER_LINE = re.compile(r"^- ([^<]+)<([^>]+)>$")
OUTPUT_FILE = "members.json"


def read_members():
    members = []
    with open(INDEX_FILE) as f:
        for line in f:
            m = MEMBER_LINE.match(line.strip())
            if not m:
                continue
            name, orcid = [_.strip() for _ in m.groups()]
            members.append((name, orcid))
    return members


def build_jsonld(members):
    jsonld = {
        "@graph": [
            {
                "@id": "https://www.researchobject.org/workflow-run-crate/",
                "@type": "Project",
                "name": "Workflow Run RO-Crate task force",
                "member": [{"@id": orcid} for (_, orcid) in members],
                "parentOrganization": {
                    "@id": "https://www.researchobject.org/ro-crate/community"
                }
            }
        ]
    }
    for name, orcid in members:
        jsonld["@graph"].append({
            "@id": orcid,
            "@type": "Person",
            "name": name,
        })
    return jsonld


def main():
    members = read_members()
    jsonld = build_jsonld(members)
    with open(OUTPUT_FILE, "wt", encoding="utf8") as f:
        json.dump(jsonld, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
