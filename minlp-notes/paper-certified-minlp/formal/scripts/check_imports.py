#!/usr/bin/env python3
"""Reject missing, duplicate, or unexpected project umbrella imports."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
expected = {"CertifiedMinlp." + ".".join(p.relative_to(root / "CertifiedMinlp").with_suffix("").parts)
            for p in (root / "CertifiedMinlp").rglob("*.lean")}
lines = (root / "CertifiedMinlp.lean").read_text().splitlines()
imports = [line.removeprefix("import ").strip() for line in lines if line.startswith("import ")]
if not expected or set(imports) != expected or len(imports) != len(set(imports)):
    raise SystemExit(f"Import mismatch: expected={sorted(expected)}, actual={imports}")
print(f"PASS: all {len(expected)} proof modules are imported exactly once.")
