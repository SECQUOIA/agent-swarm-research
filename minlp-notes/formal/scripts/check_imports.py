"""Ensure the public root imports every checked-in proof module."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
expected = {
    ".".join(path.relative_to(root).with_suffix("").parts)
    for path in (root / "Formal").rglob("*.lean")
}
actual = {
    line.removeprefix("import ").strip()
    for line in (root / "Formal.lean").read_text().splitlines()
    if line.startswith("import ")
}
missing = expected - actual
unexpected = actual - expected
if missing or unexpected:
    raise SystemExit(
        f"Proof imports differ: missing={sorted(missing)}, unexpected={sorted(unexpected)}"
    )
print(f"PASS: all {len(expected)} proof modules are imported by Formal.lean.")
