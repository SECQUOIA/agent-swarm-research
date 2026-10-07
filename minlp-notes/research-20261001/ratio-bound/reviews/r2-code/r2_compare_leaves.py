"""Review r2: optional point O7.  Compare the stored rho = 137 box file with the rerun file written by the current
certify_zB.py: same multiset of (facet, path, certificate type, certificate data)?  Also check the r_max values
quoted for H <= 3e3 in note Section 3.3 against sqrt(1 + H) from logs/rhomax.log."""
import gzip, json, re, math
def load(f):
    hdr, leaves = None, []
    for line in gzip.open(f, 'rt'):
        d = json.loads(line)
        if 'path' not in d:
            hdr = hdr or d
            continue
        leaves.append(json.dumps([d['facet'], d['path'], d['cert'], d['data']], sort_keys=True))
    return hdr, leaves
h1, a = load('../../logs/zB_cert/leaves_rho137.jsonl.gz')
h2, b = load('../../logs/rev1/leaves_rho137_rerun.jsonl.gz')
print('headers:', h1, '|', h2)
print('leaves: %d vs %d; identical as multisets: %s; identical in order: %s' % (len(a), len(b), sorted(a) == sorted(b), a == b))
print('--- rhomax.log lines mentioning H = 1000 or 3000:')
for line in open('../../logs/rhomax.log'):
    if re.search(r'\b(1000|3000|1e\+?0?3|3e\+?0?3)\b', line):
        print('   ', line.rstrip()[:160])
print('sqrt(1001) = %.4f, sqrt(3001) = %.4f, sqrt(1000) = %.4f' % (math.sqrt(1001), math.sqrt(3001), math.sqrt(1000)))
