"""Targeted regressions for review-response checks; no scientific script is imported."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile

import check_package
from finish_paths import OUT
from smoke import compare_output


def main():
    smoke = json.loads((OUT / "logs/smoke-results.json").read_text())
    tree = Path(smoke["tree"])
    record = next(r for r in smoke["checks"] if r["id"] == "powerflow0030p")
    actual = (OUT / record["output"]).read_text()
    reference = (OUT / record["reference"]).read_text()
    assert compare_output(record["id"], actual, reference, tree)[0]
    lines = actual.splitlines(True)
    for bad in ("", "".join(lines[:-1]), "".join(lines + lines[-1:]),
                "".join(reversed(lines)), actual.replace("RIGOROUS", "UNVERIFIED")):
        assert not compare_output(record["id"], bad, reference, tree)[0]
    mixed = 'message\n{"bound": 12, "seconds": 1.0}\n'
    assert compare_output("fixture", mixed.replace("1.0", "9.0"), mixed, tree)[0]
    for bad in (mixed.replace("message", "changed"), mixed.replace("12", "13")):
        assert not compare_output("fixture", bad, mixed, tree)[0]

    results = json.loads((OUT / "result-map.json").read_text())
    audits = json.loads((OUT / "audit-map.json").read_text())
    count = check_package.check_maps(results, audits)
    bad = copy.deepcopy(results[:1])
    bad[0]["numeric_evidence"][0]["value"] = "-123456789.987654321"
    try:
        check_package.check_maps(bad, [])
    except AssertionError as error:
        assert "absent from" in str(error)
    else:
        raise AssertionError("An absent mapped number passed")
    bad[0]["numeric_evidence"][0]["value"] = "0.554668764938124"
    try:
        check_package.check_maps(bad, [])
    except AssertionError as error:
        assert "absent from" in str(error)
    else:
        raise AssertionError("A prefix of a different number passed")

    original_root = check_package.ROOT
    with tempfile.TemporaryDirectory(prefix="repro-manifest-check-") as temp:
        check_package.ROOT = Path(temp)
        try:
            path = Path(temp) / "evidence.txt"
            path.write_text("changed")
            manifest = dict(files=[dict(path="evidence.txt", sha256=hashlib.sha256(b"old").hexdigest()),
                                   dict(path="missing.txt", sha256="0" * 64)], archives=[])
            errors = check_package.check_manifest(manifest)
            assert {e["problem"] for e in errors} == {"stale hash", "missing", "not inventoried"}
        finally:
            check_package.ROOT = original_root
    print(json.dumps(dict(smoke_comparator_regressions="passed", mapped_numbers=count,
                          missing_number_and_prefix_rejected=True,
                          manifest_staleness_diagnostics="passed"), indent=2))


if __name__ == "__main__":
    main()
