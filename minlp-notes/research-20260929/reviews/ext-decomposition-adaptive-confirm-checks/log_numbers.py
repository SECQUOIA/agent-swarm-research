"""Confirmation check: recompute from the author's logs the numbers restated in the revision
(extension-adaptive.md, Sections A.3-A.5, C.1-C.3, F item 8)."""
import os
import re
LG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "theory-decomposition", "adaptive", "logs")


def blocks(fname):
    cur = []
    for line in open(os.path.join(LG, fname)):
        if line.startswith("p="):
            cur.append(line)
        elif line.startswith("SUMMARY"):
            yield line, cur
            cur = []


print("== split per bag per level (live_mean), exact slopes, eps = 1e-6 ==")
for summ, rows in blocks("oracle_eps1e-6.log"):
    n = int(re.search(r" n=(\d+)", summ).group(1))
    lm = [float(re.search(r"live_mean=\s*([\d.]+)", r).group(1)) for r in rows]
    print("n=%2d max=%.1f (%.1f n)  per level/n: %s" % (n, max(lm), max(lm) / n, " ".join("%.1f" % (x / n) for x in lm)))

print("== processed / final size ==")
for f, tag in (("scaling_eps1e-4.log", "scaling"), ("random_n8_eps1e-4.log", "LS"), ("random_n16_eps1e-4.log", "LS"),
               ("oracle_eps1e-6.log", "oracle"), ("random_n8_eps1e-4.log", "oracle"), ("random_n16_eps1e-4.log", "oracle")):
    for summ, _ in blocks(f):
        if summ.split()[1].startswith(tag):
            size = int(re.search(r"size=(\d+)", summ).group(1)); tot = int(re.search(r"total_boxes=(\d+)", summ).group(1))
            print("  %-24s %-14s processed/size = %.2f" % (f, summ.split()[1] + " " + re.search(r" n=\d+", summ).group(0), tot / size))
print("== LS processed / oracle processed (C.2) ==")
for f in ("random_n8_eps1e-4.log", "random_n16_eps1e-4.log"):
    d = {summ.split()[1]: int(re.search(r"total_boxes=(\d+)", summ).group(1)) for summ, _ in blocks(f)}
    for s in (0, 1):
        print("  %s seed %d: %.2f" % (f, s, d["LS-seed%d" % s] / d["oracle-seed%d" % s]))

print("== |x_cons - x*|_inf / s_i in the final LS pass, random c ==")
for f in ("random_n8_eps1e-4.log", "random_n16_eps1e-4.log"):
    for summ, rows in blocks(f):
        if summ.split()[1].startswith("LS"):
            v = [(int(re.search(r"i=\s*(\d+)", r).group(1)), float(re.search(r"dxinf=([\d.e+-]+)", r).group(1))) for r in rows]
            v = [(i, dx / (2 * 2.0 ** -i)) for i, dx in v]
            print("  %s %s: levels>=6 %.2f-%.2f; levels 3-5 max %.2f" % (
                f, summ.split()[1], min(r for i, r in v if i >= 6), max(r for i, r in v if i >= 6),
                max(r for i, r in v if 3 <= i <= 5)))

print("== RC c = 0, n = 8 (widened test): absolute centre error = cen_inf/h * h ==")
txt = open(os.path.join(LG, "rc_zero_eps1e-6_tol.log")).read().split("SUMMARY")[1]
for line in txt.split("\n"):
    m = re.search(r"j=\s*(\d+) h=([\d.e+-]+).*lr=\s*([-\d.e+]+) UBD=\s*([-\d.e+]+) cen_inf/h=([\d.]+)", line)
    if m and int(m.group(1)) >= 12:
        j, h, lr, ubd, c = int(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4)), float(m.group(5))
        print("  j=%2d gap=%.3e UBD=%.3e centre error=%.3e (%.0f h)  stop test with exact incumbent: %s" % (
            j, -lr, ubd, c * h, c, lr >= -1e-6))
