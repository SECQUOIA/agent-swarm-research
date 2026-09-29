"""Markdown tables for Section 6 of phase-transition.md (run from data/)."""
import json, collections, glob, os, numpy as np
def load(pattern):
    rows, seen = [], set()
    for fn in sorted(glob.glob(pattern)):
        for l in open(fn):
            r = json.loads(l)
            key = (r.get('p'), r.get('k'), r.get('rule'), r.get('n'), r.get('seed'), r.get('b'), r.get('alpha') if 'rule' not in r else None)
            if key in seen: continue
            seen.add(key); rows.append(r)
    return rows
def gm(v): return float(np.exp(np.mean(np.log(v))))

REDECIDED = {}
if os.path.exists('c1_redecided.jsonl'):
    for l in open('c1_redecided.jsonl'):
        r = json.loads(l); REDECIDED[(r['p'], r['k'], r['rule'], r['n'], r['seed'])] = r['status']

def exact_c1(r):
    """C1 decision; 'capped' runs are replaced by their exact re-decision (redecide_c1.py)."""
    c = r['c1']
    if c == 'capped':
        st = REDECIDED.get((r['p'], r['k'], r['rule'], r['n'], r['seed']))
        return {'C1': True, 'fail': False}.get(st, 'capped')
    return c

def table_c1(rows, title):
    d = collections.defaultdict(list)
    for r in rows: d[(r['p'], r['k'], r['rule'], r['n'])].append(r)
    print(f"\n{title}\n")
    print("| `p` | `k` | `lam` rule | `n` | `alpha` | runs | PWE root cert. | witness | C1 (exact) | mean `tau^2` | `2 log(p lam/n)` | `2 log p` | mean root gap |")
    print("|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for key in sorted(d):
        v = d[key]; p, k, rule, n = key; lam = v[0]['lam']
        c1 = sum(exact_c1(r) is True for r in v); cap = sum(exact_c1(r) == 'capped' for r in v)
        print("| %d | %d | %s | %d | %.2f | %d | %d | %d | %d%s | %.2f | %.2f | %.2f | %.3f |" % (
            p, k, ('tau0=' + rule) if rule != 'sqrtn' else 'sqrt n', n, n / (k * np.log(p)), len(v), sum(r['pwe'] for r in v),
            sum(r['wit'] for r in v), c1, (' (+%d)' % cap) if cap else '', np.mean([r['tau'] ** 2 for r in v]),
            2 * np.log(p * lam / n), 2 * np.log(p), np.mean([r['gap'] for r in v])))

def table_hard(rows, title):
    d = collections.defaultdict(list)
    for r in rows: d[(r['b'], r['alpha'], r['k'])].append(r)
    print(f"\n{title}\n")
    print("| signal `b` | `alpha` | `k` | `p` | `n` | runs (done) | nodes, geo. mean [min, max] | certified clique, median [min, max] |")
    print("|---:|---:|---:|---:|---:|---:|---|---|")
    for key in sorted(d):
        v = d[key]; b, a, k = key
        nodes = [r['nodes'] for r in v]; cl = [r['clique'] for r in v if 'clique' in r]
        print("| %g | %g | %d | %d | %d | %d (%d) | %.0f [%d, %d] | %s |" % (b, a, k, v[0]['p'], v[0]['n'], len(v), sum(r['done'] for r in v),
              gm(nodes), min(nodes), max(nodes), ("%.1f [%d, %d]" % (np.median(cl), min(cl), max(cl))) if cl else '-'))
    ok = all((r['nodes'] + 1) // 2 >= r['clique'] for r in rows if 'clique' in r)
    print(f"\nClique <= leaves in every completed run: {ok}.")

def table_rule(rows, title):
    d = collections.defaultdict(list)
    for r in rows: d[(r['p'], r['k'], r['alpha'])].append(r)
    print(f"\n{title}\n")
    print("| `p` | `k` | `alpha` | `n` | runs | `S*` optimal | removal half holds | C1 holds | median #failing forced-in nodes | `maxz` nodes, geo. mean [max] | `maxfrac` nodes, geo. mean [max] |")
    print("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|")
    for key in sorted(d):
        v = d[key]; p, k, a = key; w = [r for r in v if 'bad0' in r]
        print("| %d | %d | %.2f | %d | %d | %d | %d | %d | %.0f | %.0f [%d] | %.0f [%d] |" % (p, k, a, v[0]['n'], len(v), sum(r.get('rec', False) for r in v),
              sum(r['bad0'] == 0 for r in w), sum(r['bad0'] + r['bad1'] == 0 for r in w), np.median([r['bad1'] for r in w]),
              gm([r['maxz']['nodes'] for r in v]), max(r['maxz']['nodes'] for r in v),
              gm([r['maxfrac']['nodes'] for r in v]), max(r['maxfrac']['nodes'] for r in v)))

if __name__ == '__main__':
    table_c1(load('c1_p200_k8_t1.5.jsonl') + load('c1_scaleP_k8_t1.5.jsonl'), "Table 6.1")
    if os.path.exists('c1_gamma_half.jsonl'): table_c1(load('c1_gamma_half.jsonl'), "Table 6.2")
    table_c1(load('c1_sqrtn_k5.jsonl'), "Table 6.3")
    table_hard(load('hard_k3-8.jsonl') + load('hard_noise_k9-10.jsonl'), "Table 6.4")
    table_hard(load('hard_planted_lowalpha.jsonl'), "Table 6.5")
    table_rule(load('rule_p100_k6.jsonl') + load('rule_p200_k8.jsonl'), "Table 6.6")
