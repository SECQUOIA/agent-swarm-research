"""Identify the source network of MINLPLib waterno2_* (review round 1, minor issue 5).

Huang (2019), TU Darmstadt dissertation, Example 5.41 (p. 123) prints the pump energy
polynomial of one pump of the Tsinghua network n9p3a11 as
    C = 25.9267 w^3 + 18.1348 w^2 Q + 22.1276 w Q^2 - 42.6895 Q^3,  (w, Q) in [0.85, 1.0] x [0.4, 0.7].
This script counts how often the four coefficients (at the precision stored in the OSIL file)
occur in each waterno2 OSIL file, checks that they agree with the printed values when truncated to
four decimals (rounding would give 22.1277 for the third coefficient, so Huang truncated), and
compares the optimal values of Huang's Table 5.2 ("original" model, P[0,i]) with the MINLPLib
primal values of waterno2_01 ... waterno2_24 (from the cached MINLPLib pages).

    python3 waterno2_huang_match.py
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])
_PUBLIC_HOME = str(_PublicPath.home())

import html
import re
from decimal import Decimal, ROUND_DOWN

O = (_PUBLIC_HOME + '/.cache/minlplib/minlplib/osil/%s.osil')
PAGES = (_PUBLIC_REPO + '/research-20260929/bound-audit/pages/%s.html')
PRINTED = ["25.9267", "18.1348", "22.1276", "-42.6895"]
STORED = ["25.92674585", "18.13482123", "22.12766012", "-42.68950769"]
# Huang (2019) Table 5.2, "original" column: primal, dual (SCIP 5.0.1, 1 h)
HUANG = {1: (19.46, 19.46), 2: (39.57, 39.57), 3: (215, 215), 4: (247.63, 247.63), 6: (456, 163.65),
         9: (1113.14, 238.28), 12: (2603.85, 461.55), 18: (5909.72, 504.07), 24: (8380.79, 454.64)}

for p, s in zip(PRINTED, STORED):
    assert Decimal(s).quantize(Decimal("0.0001"), rounding=ROUND_DOWN) == Decimal(p), (p, s)
print("stored coefficients truncated to 4 decimals equal Huang's printed values:", ", ".join(f"{s} -> {p}" for p, s in zip(PRINTED, STORED)))

for T in (1, 2, 3, 4, 6, 9, 12, 18, 24):
    name = f"waterno2_{T:02d}"
    txt = open(O % name).read()
    counts = [len(re.findall(r"<el>%s</el>" % re.escape(s), txt)) for s in STORED]
    page = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", open(PAGES % name, encoding="utf-8").read())))
    prim = re.search(r"Primal Bounds \(infeas[^)]*\) \S+ ([-\d.]+)", page).group(1)
    hp, hd = HUANG[T]
    print(f"{name}: occurrences of the four coefficients {counts} (= 2 pumps x {T} periods: {counts == [2 * T] * 4}); "
          f"MINLPLib primal {prim}; Huang Table 5.2 P[0,{T}] primal {hp}, dual {hd}")
