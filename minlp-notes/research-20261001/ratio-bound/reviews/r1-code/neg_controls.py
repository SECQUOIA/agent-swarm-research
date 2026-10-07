"""Reviewer: negative controls for indep_verify_boxes.py (it must reject a wrong rho, a missing leaf and a
duplicated leaf).  usage: python3 neg_controls.py"""
import indep_verify_boxes as V, gzip, json, io, contextlib, os
src = '../../logs/zB_cert/leaves_tan_eta1e-2_k4_rho3_2.jsonl.gz'
def run(lines, rho, tag):
    fn = '/tmp/r1_neg_%s.jsonl.gz' % tag
    with gzip.open(fn, 'wt') as f:
        for d in lines: f.write(json.dumps(d) + '\n')
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        V.main(fn, rho, 'tan:1/100:4')
    os.remove(fn)
    return buf.getvalue()
base = [json.loads(l) for l in gzip.open(src, 'rt')]
l1 = [dict(d) for d in base]
for d in l1:
    if 'facet_start' in d: d['rho'] = '1'
o = run(l1, '1', 'rho'); print('wrong rho (3/2 -> 1): leaf failures', o.count('LEAF FAIL'), '|', o.strip().splitlines()[-1])
k = [i for i, d in enumerate(base) if 'cert' in d][10]
l2 = base[:k] + base[k + 1:]
o = run(l2, '3/2', 'drop'); print('one leaf dropped:', [l for l in o.splitlines() if '!= 8' in l], '|', o.strip().splitlines()[-1])
l3 = base[:k] + [dict(base[k])] + base[k:]
o = run(l3, '3/2', 'dup'); print('one leaf duplicated:', [l for l in o.splitlines() if 'overlapping' in l or '!= 8' in l], '|', o.strip().splitlines()[-1])
