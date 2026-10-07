"""Verify C-literature-1: HS (1990) content vs. the paper's related-work text.

Checks (read-only):
  1. The local HS full text contains the continuous log2(B/2eps) result, the
     O(n Delta) grid per iteration, the solution-space definition of
     eps-accuracy, and the TU algorithm (Algorithm 4.2 / Theorem 4.3).
  2. The paper cites HochbaumShanthikumar1990 exactly once and Meyer1977 never.
  3. The pre-W3 comparison paragraph existed and is absent now.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[4]
HS = ROOT / "literature/papers/hochbaum1990-convex-separable-optimization-is-not/fulltext.md"
PAPER = ROOT / "paper-decomposition-aware"

hs = HS.read_text()
checks = {
    "continuous log2(B/2eps) iterations (Sec 1.3)": "logz(B/2c) such iterations" in hs,
    "grid of O(n Delta) points per variable (Sec 1.3)": "grid of O(nA) points" in hs,
    "Theorem 1.1 with T(8n^2 Delta, m, Delta)": "T(8n2A, m, A)" in hs and "THEOREM 1.1" in hs,
    "eps-accuracy = sup-norm distance to an optimum": "11 i - x* I( m 5 E" in hs,
    "Theorem 3.8 (LP-s vs RP proximity 2ns Delta)": "THEOREM 3.8" in hs,
    "Algorithm 4.3 / Theorem 4.4 (continuous)": "Algorithm 4.3" in hs and "THEOREM 4.4" in hs,
    "Algorithm 4.2 / Theorem 4.3 (TU)": "Algorithm 4.2" in hs and "totally unimodular constraint matrix" in hs,
}
for k, v in checks.items():
    print(f"{'OK ' if v else 'MISSING'} {k}")

secs = "".join(p.read_text() for p in sorted((PAPER / "sections").glob("*.tex")))
print("cites of HochbaumShanthikumar1990 in sections:", len(re.findall(r"HochbaumShanthikumar1990", secs)))
print("cites of Meyer1977 in sections:", len(re.findall(r"Meyer1977", secs)))
print("Meyer1977 in references.bib:", "Meyer1977" in (PAPER / "references.bib").read_text())

old = (PAPER / "process/w3/sections-before-w3/constraints.tex").read_text()
print("pre-W3 HS paragraph present:", "Proximity scaling for separable convex objectives" in old)
print("current HS paragraph present:", "Proximity scaling for separable convex objectives" in secs)
