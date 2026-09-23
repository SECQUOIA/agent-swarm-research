#!/usr/bin/env python3
"""Export the canonical Lean dependency closure; not needed to verify the bundle."""
import argparse
import hashlib
import json
from pathlib import Path

ENDPOINTS = (
    "Formal.CubicGap.Ratios",
    "Formal.CubicGap.RoundingUpper",
    "Formal.CubicGap.RoundingOptimalityLaw",
    "Formal.CubicGap.AnalyticResults",
    "Formal.MultilinearGap.EnvelopeFunctions",
    "Formal.MultilinearGap.PaperFoundations",
)



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="canonical formal/ directory")
    parser.add_argument("--check", action="store_true", help="compare without writing")
    args = parser.parse_args()
    source = args.source.resolve()
    target = Path(__file__).resolve().parents[1] / "formal"
    modules = set()

    def visit(module):
        if module in modules:
            return
        modules.add(module)
        path = source / (module.replace(".", "/") + ".lean")
        for line in path.read_text().splitlines():
            if line.startswith("import Formal."):
                for dependency in line.removeprefix("import ").split():
                    visit(dependency)

    for module in ENDPOINTS:
        visit(module)
    paths = sorted(module.replace(".", "/") + ".lean" for module in modules)
    paths += ["lakefile.toml", "lake-manifest.json", "lean-toolchain"]
    expected = {path: (source / path).read_bytes() for path in paths}
    expected["Formal.lean"] = "".join(
        f"import {module}\n" for module in sorted(modules)
    ).encode()
    obsolete = {
        str(path.relative_to(target)) for path in (target / "Formal").rglob("*.lean")
    } - set(paths)
    if obsolete:
        raise SystemExit(f"Remove obsolete exported proof files explicitly: {sorted(obsolete)}")
    if args.check:
        failures = [path for path, data in expected.items()
                    if not (target / path).is_file() or (target / path).read_bytes() != data]
        if failures:
            raise SystemExit(f"Export differs from canonical source: {failures}")
    else:
        for path, data in expected.items():
            dest = target / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
        manifest = {
            "endpoints": list(ENDPOINTS),
            "proof_modules": len(modules),
            "canonical_files_sha256": {
                path: hashlib.sha256((source / path).read_bytes()).hexdigest()
                for path in paths
            },
        }
        (target / "verification" / "export.json").write_text(
            json.dumps(manifest, indent=2) + "\n")
    print(f"PASS: {'compared' if args.check else 'exported'} {len(modules)} proof modules.")


if __name__ == "__main__":
    main()
