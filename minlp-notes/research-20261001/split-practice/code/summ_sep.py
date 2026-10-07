"""Summarise logs/sep_*.jsonl (one line per point)."""
import json, sys
def g(d, *ks):
    for k in ks:
        if d is None: return None
        d = d.get(k) if isinstance(d, dict) else None
    return d
def f(x, n=4):
    return '-' if x is None else (f'{x:.{n}g}' if isinstance(x, (int, float)) else str(x))
for p in sys.argv[1:]:
    print('file rank@1e-5 | fam1 fam2 fam3 viol | ratio(q,supp,vmax,t) | grb1 q,t,st | grb3 | grb10 | thm3 q, qY, digits, t')
    for l in open(p):
        d = json.loads(l)
        r = d['ratio']
        row = [d['file'].replace('.npz',''), d['rank']['1e-05'],
               '|', f(g(d,'fam1','max_viol')), f(g(d,'fam2','max_viol')), f(g(d,'fam3','max_viol')),
               '|', f(r['ratio']), f(r['q']), r['supp'], r['vmax'], f(r['time'],2), 'c' if r['complete'] else 'INC']
        for K in (1,3,10):
            gg = d.get(f'grb{K}', {})
            row += ['|', f(gg.get('q'),6), f(gg.get('time'),2), (gg.get('status') or '')[:4]]
        t = d.get('thm3')
        if t:
            row += ['|', f(t.get('q'),6), f(t.get('q_at_Y'),3), t.get('vmax_digits'), f(t.get('time'),2)]
        print(*row)
