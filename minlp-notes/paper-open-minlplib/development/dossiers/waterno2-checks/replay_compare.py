"""Compares the replayed vbb2 results with the reviewers' saved results (status, exact bound, node count)."""
import gzip, json, sys
old = {}
for l in gzip.open(sys.argv[1], 'rt'):
    r = json.loads(l)
    if r['kind'] == 'rec': old[r['rid']] = r
new = [json.loads(l) for l in open(sys.argv[2])]
same = 0; tn = to = 0
for r in sorted(new, key=lambda r: r['rid']):
    o = old[r['rid']]
    eq = (r['vbb2_status'], r['vbb2_bound'], r['nodes']) == (o['vbb2_status'], o['vbb2_bound'], o['nodes'])
    same += eq; tn += r['time']; to += o['time']
    print(r['rid'], 'period', r['t'], r['group'], r['vbb2_status'], 'nodes', r['nodes'], 'time %.2f s (review %.2f s)' % (r['time'], o['time']), 'identical:', eq)
print(f'certB records: {same}/{len(new)} identical to the review run (status, exact bound, nodes); task time {tn:.1f} s here, {to:.1f} s in the review run (loaded machine)')
a = json.load(open(sys.argv[4])); b = json.load(open(sys.argv[3]))
print('waterno2_09 period 6:', a['status'], a['bound'], 'nodes', a['nodes'], 'time %.1f s' % a['time'],
      '| identical to recheck log:', all(a[k] == b[k] for k in ('status', 'bound', 'nodes')))
