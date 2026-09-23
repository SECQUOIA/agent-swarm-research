"""Save the exact manuscript input for an independent review round."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil

PAPER = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name")
    args = parser.parse_args()
    destination = PAPER / "process" / "snapshots" / args.name
    destination.mkdir(parents=True, exist_ok=False)
    paths = sorted(PAPER.glob("*.tex")) + sorted(PAPER.glob("*.bib"))
    paths += sorted((PAPER / "sections").glob("*.tex"))
    paths += sorted((PAPER / "appendices").glob("*.tex"))
    paths += sorted((PAPER / "figures").glob("*.pdf"))
    # Freeze paper-local certificates as well as the text that cites them.
    paths += sorted((PAPER / "verification").glob("*.py"))
    paths += sorted((PAPER / "verification").glob("*.json"))
    manifest = {}
    for source in paths:
        relative = source.relative_to(PAPER)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        manifest[str(relative)] = hashlib.sha256(source.read_bytes()).hexdigest()
    if (PAPER / "main.pdf").exists():
        shutil.copyfile(PAPER / "main.pdf", destination / "main.pdf")
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(destination)


if __name__ == "__main__":
    main()
