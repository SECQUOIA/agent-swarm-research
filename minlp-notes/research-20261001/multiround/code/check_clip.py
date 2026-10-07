"""Clipping check (review r1, item o1): count stored round states whose LP value exceeds SCIP's
z_bil, and the largest excess relative to |z_bil| and to the root gap.  Reads logs/main and
logs/new (the records behind Sections 2-4).  Usage: python3 check_clip.py"""
import recio
n = above = 0; worst_rel = worst_gap = 0.0
for pat in ('../logs/main/*.jsonl', '../logs/new/*.jsonl'):
    for f, r in recio.records(pat):
        gap = r['zbil'] - r['zlp']
        for ri in r['rounds']:
            n += 1
            if ri['z'] > r['zbil']:
                above += 1
                worst_rel = max(worst_rel, (ri['z'] - r['zbil']) / max(1.0, abs(r['zbil'])))
                worst_gap = max(worst_gap, (ri['z'] - r['zbil']) / gap)
print('round states %d; LP value above z_bil in %d; max excess %.2g relative to max(1, |z_bil|), %.2g of the root gap'
      % (n, above, worst_rel, worst_gap))
