"""Reviewer sample: pick attempt records and copy them from the raw dumps.

Selection (seed 20261003):
  MINLPLib, per instance: up to 6 records of the stream's analysed sample with class 'ratio'
  (z_K > 0), up to 2 with class 'zeroface'/'allzero_w', and 4 uniformly random attempt indices
  from the whole dump (may be outside the stream's sample; used for the step-length check).
  Generator: 60 random analysed records each for mc11 and mc12.
Record index k = position among dump lines that are attempt records (lines starting '{"v":'),
the same numbering as the stream's analyze.py (checked afterwards on lp/cons/node).
Output: reviews/r1-logs/sample_records.jsonl.gz (raw dump lines with "inst","k","set" added).
Usage: python3 extract_sample.py [NPAR]"""
import os, sys, json, glob, gzip, random, subprocess, collections
from concurrent.futures import ProcessPoolExecutor
L = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../logs')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../r1-logs/sample_records.jsonl.gz')
rng = random.Random(20261003)


def cls(r):
    if r['wmax'] <= 0:
        return 'allzero'
    return 'zeroface' if r.get('zeroface_meets_S') else 'ratio'


want = collections.defaultdict(set)      # dump path -> set of k
setname = {}
# MINLPLib
an = collections.defaultdict(list); nrec = {}
for f in glob.glob(os.path.join(L, 'an_minlplib', '*.jsonl')) + glob.glob(os.path.join(L, 'an_minlplib2', '*.jsonl')):
    for l in open(f):
        r = json.loads(l)
        if 'sampling' in r:
            nrec[r['inst']] = r['sampling']['nrecords']
        elif r.get('status') == 'ok':
            an[r['inst']].append((r['k'], cls(r)))
for inst in sorted(nrec):
    p = os.path.join(L, 'runs_minlplib', inst + '.jsonl.gz')
    X = sorted(an.get(inst, []))
    rat = [k for k, c in X if c == 'ratio']; oth = [k for k, c in X if c != 'ratio']
    ks = set(rng.sample(rat, min(6, len(rat)))) | set(rng.sample(oth, min(2, len(oth))))
    ks |= set(rng.sample(range(nrec[inst]), min(4, nrec[inst])))
    want[p] |= ks; setname[p] = 'minlplib'
# generator
for st in ('mc11', 'mc12'):
    R = [json.loads(l) for l in open(os.path.join(L, 'an_%s.jsonl' % st))]
    R = [r for r in R if r.get('status') == 'ok']
    for r in rng.sample(R, 60):
        p = os.path.join(L, 'runs_' + st, r['inst'] + '.jsonl.gz')
        want[p].add(r['k']); setname[p] = st


def grab(p):
    ks = want[p]; out = []
    inst = os.path.basename(p).split('.')[0]
    proc = subprocess.Popen(['gzip', '-dc', p], stdout=subprocess.PIPE)
    k = -1
    for line in proc.stdout:
        if line.startswith(b'{"v":'):
            k += 1
            if k in ks:
                r = json.loads(line)
                r['inst'] = inst; r['k'] = k; r['set'] = setname[p]
                out.append(json.dumps(r))
                if len(out) == len(ks):
                    break
    proc.kill(); proc.wait()
    return p, out


if __name__ == '__main__':
    npar = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    paths = sorted(want, key=lambda p: -os.path.getsize(p))
    n = 0
    with gzip.open(OUT, 'wt') as fo, ProcessPoolExecutor(npar) as ex:
        for p, out in ex.map(grab, paths):
            for s in out:
                fo.write(s + '\n'); n += 1
            print(os.path.basename(p), len(out), 'of', len(want[p]), flush=True)
    print('records', n)
