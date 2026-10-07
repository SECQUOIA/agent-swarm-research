"""Review r2: recompute the SCIP random-sampling minima quoted in note Section 4 (optional point O3) directly from
the compressed logs, without the stream's scip_random_minima.py.  scipA = uncompleted set C_{R_theta},
scipB = its upward closure (SCIP's Case-4 set), as documented in code/rb.py (scip_bound docstring)."""
import gzip, json, glob
rows = []
for f in sorted(glob.glob('../../logs/scip_random_*.log.gz')):
    n = 0
    for line in gzip.open(f, 'rt'):
        line = line.strip()
        if line.startswith('{') and '"scipB"' in line:
            rows.append(json.loads(line)); n += 1
    print(f.split('/')[-1], n, 'corners')
print('total corners:', len(rows))
for lab, sel in [('D <= 2', lambda r: r['D'] <= 2), ('D <= 2, cond <= 10', lambda r: r['D'] <= 2 and r['cond'] <= 10)]:
    sub = [r for r in rows if sel(r)]
    for key in ['scipB', 'scipA']:
        m = min(sub, key=lambda r: r[key])
        print('%-20s n = %5d  min %s = %.4f at D = %.3f, cond = %.1f' % (lab, len(sub), key, m[key], m['D'], m['cond']))
