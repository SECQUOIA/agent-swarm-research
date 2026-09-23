"""Inspect generated topic-15 query bodies after their targeted Lean build.

Run from formal/. This checks the specific implicit-cardinality regression;
it is not a compiler correctness or general runtime-cost verifier.
"""

from pathlib import Path
import re


base = Path(".lake/build/ir/Formal/NetworkSimplex")
targets = {
    "ThresholdObservedCache": ["observedCache"],
    "ThresholdObservedAlgorithm": ["observedMembership", "observedWitness"],
    "ThresholdObservedSeparation": ["observedSeparate"],
}

for module, names in targets.items():
    source = (base / f"{module}.c").read_text()
    for name in names:
        match = re.search(
            rf"LEAN_EXPORT lean_object\* [^\n]*_{name}\([^\n]*\)\{{", source
        )
        assert match, (module, name, "definition missing")
        start = match.end() - 1
        depth = 0
        for stop in range(start, len(source)):
            depth += (source[stop] == "{") - (source[stop] == "}")
            if depth == 0:
                break
        else:
            raise AssertionError((module, name, "unterminated body"))
        body = source[start : stop + 1]
        for forbidden in ("dedup", "toFinset", "orderIso", "card___"):
            assert forbidden not in body, (module, name, forbidden)
        assert "lean_array_size" in body or "lean_array_get_size" in body
        print(f"PASS {module}.{name}: cached size; no hidden deduplication")
