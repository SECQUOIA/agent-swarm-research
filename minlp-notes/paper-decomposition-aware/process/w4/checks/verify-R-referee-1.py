"""Verify R-referee-1: page budget of the main text and the savings of the proposed cuts.

Page spans come from /tmp/dpaper/out/main.aux (section start pages).
Block sizes are estimated as (tex words of block) / (tex words per page of the
containing section), with the section's page span taken from main.aux.
This is an estimate (+-25%), adequate for judging a page target.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import re, subprocess
S = (_PUBLIC_REPO + '/paper-decomposition-aware/sections/')

def words(f, a=1, b=None):
    L = open(S + f).read().splitlines()
    b = len(L) if b is None else b
    return len(" ".join(L[a-1:b]).split())

pages = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", "/tmp/dpaper/out/main.pdf"], capture_output=True, text=True).stdout).group(1))
print("PDF pages:", pages)
nbib = open("/tmp/dpaper/out/main.bbl").read().count("\\bibitem")
print("bibitems:", nbib)

# section word totals and page spans (from main.aux: start pages)
sec = {
 "7": (["recourse.tex", "recourse-valuefn.tex", "recourse-local.tex", "recourse-convex.tex", "recourse-cuts.tex", "recourse-mixed.tex", "recourse-balanced.tex"], 44 - 31),
 "8": (["constraints.tex"], 53 - 44),
 "9": (["optsets.tex"], 62 - 53),
 "10": (["limits.tex"], 71 - 62),
 "11": (["computation.tex"], 78 - 71),
 "1": (["intro.tex"], 7 - 1),
}
wpp = {}
for k, (fs, pg) in sec.items():
    w = sum(words(f) for f in fs)
    wpp[k] = w / pg
    print(f"Sec {k}: {w} words over ~{pg} pages -> {wpp[k]:.0f} words/page")

blocks = [
 ("7.2 after thm:cr-filter (multilevel text, prop:star setup+statement)", "7", "recourse-local.tex", 75, 147, 2),   # keep ~2 lines: one sentence on prop:star
 ("7.3 affine recognition", "7", "recourse-convex.tex", 282, 302, 2),
 ("7.3 cv-limit discussion", "7", "recourse-convex.tex", 304, 345, 2),
 ("8.6 TU exact (keep constants+thm statement)", "8", "constraints.tex", 477, 571, None),
 ("prop:tu-misaligned + ex:tu-sum", "8", "constraints.tex", 590, 650, 2),
 ("9.3 diag certificate (keep rem:shor short + thm statement)", "9", "optsets.tex", 476, 660, None),
 ("10.4-10.7 proofs", "10", "limits.tex", None, None, 0),
 ("E3 paragraph", "11", "computation.tex", 189, 199, 0),
 ("novelty sentence", "1", "intro.tex", 109, 112, 0),
]
total = 0.0
for name, s, f, a, b, keep_lines in blocks:
    if name.startswith("10.4"):
        w = sum(words(f, x, y) for x, y in [(422, 466), (502, 545), (576, 607), (647, 660)])
    else:
        w = words(f, a, b)
    if name.startswith("8.6"):
        w -= words(f, 486, 500) + words(f, 546, 560)  # keep constants paragraph and theorem statement (approx.)
    if name.startswith("9.3"):
        w -= words(f, 518, 537) // 2 + words(f, 597, 622)  # half of rem:shor + thm statement (approx.)
    if keep_lines:
        w -= 12 * keep_lines
    p = w / wpp[s]
    total += p
    print(f"{name:62s} {w:5d} words  ~{p:4.1f} pages")
print(f"Estimated saving of the listed cuts: ~{total:.1f} pages; main text ~80 -> ~{80 - total:.0f} pages")
