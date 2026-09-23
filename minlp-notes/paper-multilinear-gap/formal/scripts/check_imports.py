"""Require an explicit root import for every bundled proof module."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
expected = {".".join(p.relative_to(root).with_suffix("").parts)
            for p in (root / "Formal").rglob("*.lean")}
actual = {line.removeprefix("import ").strip()
          for line in (root / "Formal.lean").read_text().splitlines()
          if line.startswith("import ")}
if not expected or expected != actual:
    raise SystemExit(f"Import mismatch: missing={sorted(expected - actual)}, "
                     f"unexpected={sorted(actual - expected)}")
print(f"PASS: all {len(expected)} bundled proof modules are imported.")
