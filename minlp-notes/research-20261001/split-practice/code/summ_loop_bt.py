"""Compare the B-T replication (SDP + split closure) with B-T's Table 2."""
import json, sys, collections, statistics as st
BT_TABLE2 = {0: (4.12, 100.00), 1: (2.71, 95.71), 2: (4.21, 79.77), 3: (5.75, 61.12), 4: (5.33, 56.44),
             5: (5.71, 49.70), 6: (3.91, 64.24), 7: (3.59, 57.50), 8: (2.71, 60.07), 9: (2.27, 49.25),
             10: (1.83, 55.12)}  # p -> (GAP %, STD ALL % of SDP gap closed)
rows = [json.loads(l) for l in open(sys.argv[1])]
by = collections.defaultdict(list)
errs = [r for r in rows if 'error' in r]
for r in rows:
    if 'error' in r: continue
    p = int(r['name'].split('_p')[1].split('_')[0])
    gap = 100 * (r['opt'] - r['root']) / abs(r['opt'])
    closed = 100 * (r['final'] - r['root']) / (r['opt'] - r['root']) if r['opt'] - r['root'] > 1e-7 else None
    maxrank = max(h['rank']['1e-05'] for h in r['hist'])
    tsep = sum(h['t_sep'] for h in r['hist']); nr = r['rounds']
    gen = sum(1 for h in r['hist']
              if all(h['fam_viol'].get(k, 0) <= 1e-6 for k in ('1', '2', '3'))
              and -(h['ratio_q'] or 0) > 1e-6)
    by[p].append((gap, closed, maxrank, r['final_rank']['1e-05'], nr, tsep, gen, r['time']))
print(f"errors: {len(errs)}")
print("p | our GAP% | B-T GAP% | our closed% (mean over open) | B-T STD ALL% | rounds | max rank | final rank | rounds with only general splits | sep time/inst s")
allc = []; allg = []
for p in sorted(by):
    L = by[p]
    cl = [c for _, c, *_ in L if c is not None]
    allc += cl; allg += [g for g, *_ in L]
    print(p, '|', round(st.mean(g for g, *_ in L), 2), '|', BT_TABLE2[p][0], '|', round(st.mean(cl), 1) if cl else '-',
          f'({len(cl)})', '|', BT_TABLE2[p][1], '|', round(st.mean(x[4] for x in L), 1), '|',
          max(x[2] for x in L), '|', round(st.mean(x[3] for x in L), 1), '|', round(st.mean(x[6] for x in L), 1),
          '|', round(st.mean(x[5] for x in L), 2))
print('average', round(st.mean(allg), 2), '| B-T 3.83 |', round(st.mean(allc), 1), '| B-T 66.36')
