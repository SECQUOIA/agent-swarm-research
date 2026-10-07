"""Review r2: adversarial probes of the revised verifiers (beyond the r1 duplicate-ray probe).

Box verifier (code/verify_box_cert.py), base certificate logs/boxcert_thm14_BP.json
(lam = (1/5, 0, 1/6)). The false point used by r1 is lam/2 = (1/10, 0, 1/12); it is not in Cl_BP.
Every probe that tries to double-count a ray is applied to that false point, so a correct
verifier must reject it. Two further probes test the handling of lam itself.

Closure verifier (code/verify_closure_cert.py): pruning on an unbounded inactive coordinate,
run against the revised verifier and against the HEAD (pre-revision) version, and a negative
lam entry on an inactive coordinate.

Each probe prints the verifier's exit code (2 = crash, which also counts as rejection).
"""
import contextlib
import copy
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.normpath(os.path.join(HERE, '..', '..', 'code'))
LOGS = os.path.normpath(os.path.join(HERE, '..', '..', 'logs'))
sys.path.insert(0, CODE)
import verify_box_cert as VB          # noqa: E402
import verify_closure_cert as VC      # noqa: E402


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(main, d=None, raw=None):
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as fh:
        fh.write(raw if raw is not None else json.dumps(d))
        name = fh.name
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            rc = main(name)
        except Exception as e:  # crash = rejection
            rc = 2
            print('EXC %r' % e)
    os.unlink(name)
    last = [l for l in buf.getvalue().splitlines() if l.startswith('FAIL') or l.startswith('EXC')][:2]
    return rc, last


results = []


def report(name, rc, expect_reject, detail):
    status = 'rejected' if rc != 0 else 'ACCEPTED'
    verdict = 'as expected' if (rc != 0) == expect_reject else 'UNEXPECTED'
    results.append((name, rc, expect_reject))
    print('%-72s exit %d  %-8s (%s) %s' % (name, rc, status, verdict, detail if rc != 0 else ''), flush=True)


base = json.load(open(os.path.join(LOGS, 'boxcert_thm14_BP.json')))
print('base certificate: instance %s, family %s, lam %s' % (base['instance'], base['family'], base['lam']))

rc, det = run(VB.main, base)
report('BP original certificate', rc, False, det)
half = copy.deepcopy(base)
half['lam'] = [str(Fr(x) / 2) for x in base['lam']]
rc, det = run(VB.main, half)
report('false point lam/2, no tricks', rc, True, det)


def every_cut(d, f):
    m = copy.deepcopy(d)
    for lf in m['leaves']:
        if lf['type'] == 'cut':
            f(lf)
    return m


# --- routes to count a ray twice, all on the false point
probes = [
    ('alias "0_0" (int() accepts underscores)', lambda lf: lf['v'].update({'0_' + k: v for k, v in list(lf['v'].items())})),
    ('alias " 0" (int() strips whitespace)', lambda lf: lf['v'].update({' ' + k: v for k, v in list(lf['v'].items())})),
    ('alias "+0"', lambda lf: lf['v'].update({'+' + k: v for k, v in list(lf['v'].items())})),
    ('alias "-0" style ("-"+key)', lambda lf: lf['v'].update({'-' + k: v for k, v in list(lf['v'].items()) if k == '0'})),
    ('alias with Unicode digit (Arabic-Indic)', lambda lf: lf['v'].update({chr(0x660 + int(k)): v for k, v in list(lf['v'].items())})),
    ('alias with full-width digit', lambda lf: lf['v'].update({chr(0xFF10 + int(k)): v for k, v in list(lf['v'].items())})),
    ('kb entries as JSON integers, doubled', lambda lf: lf.update({'kb': [int(j) for j in lf.get('kb', [])] * 2})),
    ('kb as a string "00" (iterates to two keys)', lambda lf: lf.update({'kb': ''.join(lf.get('kb', [])) * 2})),
    ('kb as an object with the same key twice via alias', lambda lf: lf.update({'kb': {j: 1 for j in lf.get('kb', [])} | {'0' + j: 1 for j in lf.get('kb', [])}})),
    ('every v ray also as kb ray', lambda lf: lf.update({'kb': list(lf.get('kb', [])) + [k for k in lf['v'] if k not in lf.get('kb', [])]})),
]
for name, f in probes:
    rc, det = run(VB.main, every_cut(half, f))
    report('false point + ' + name, rc, True, det)

# same leaf listed twice (each copy must pass on its own; nothing is summed across leaves)
m = copy.deepcopy(half)
m['leaves'] = m['leaves'] + copy.deepcopy(m['leaves'])
rc, det = run(VB.main, m)
report('false point + every leaf listed twice', rc, True, det)

# duplicate JSON keys at the leaf level ("v" twice) and top level ("lam" twice, true value second)
raw = json.dumps(half).replace('"v": {', '"v": {"0": ["1", "0"]}, "v": {', 1)
rc, det = run(VB.main, raw=raw)
report('false point + duplicate literal "v" key in one leaf', rc, True, det)
raw = json.dumps(base).replace('"lam": [', '"lam": ["1/10", "0", "1/12"], "lam": [', 1)
rc, det = run(VB.main, raw=raw)
report('true certificate with a duplicate top-level "lam" key', rc, True, det)

# lam handling: a negative entry on a ray that no leaf lists (ray index 1 in this certificate)
listed = set()
for lf in base['leaves']:
    if lf['type'] == 'cut':
        listed |= set(lf['v']) | set(lf.get('kb', []))
print('rays listed in some cut leaf:', sorted(listed))
neg = copy.deepcopy(base)
neg['lam'] = [base['lam'][0], '-1', base['lam'][2]]
rc, det = run(VB.main, neg)
report('lam = (1/5, -1, 1/6): negative entry on an unlisted ray (not in Cl_BP)', rc, True, det)
longer = copy.deepcopy(base)
longer['lam'] = base['lam'] + ['-5']
rc, det = run(VB.main, longer)
report('lam with a fourth entry -5 for a three-ray corner', rc, True, det)

# ---------------- closure verifier
wc = json.load(open(os.path.join(LOGS, 'closure_cert_wcorner_A_A.json')))
print('W-corner certificate lam =', wc['instance']['lam'])
# (0, 0, 0, 2) is in X; (0, 0, 0, 1/2) is a valid cut vector for X (the (B) set of Theorem 11(d))
# and lies in the piece + cone{e_4}, so pruning this piece with x = (0,0,0,2) is unsound.
bad = copy.deepcopy(wc)
pc = bad['blocks'][0]['pieces'][0]
pc.pop('Y')
pc['outside'] = 0
bad_new = copy.deepcopy(bad)
bad_new['instance']['xpoints'] = [['0', '0', '0', '2']]
rc, det = run(VC.main, bad_new)
report('closure: prune W-corner piece with x = (0,0,0,2) [revised verifier]', rc, True, det)
old_path = os.path.join(HERE, 'old_verify_closure_cert.py')
src = subprocess.run(['git', 'show', 'HEAD:research-20261001/orbit-closure/code/verify_closure_cert.py'],
                     cwd=CODE, capture_output=True, text=True, check=True).stdout
with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as fh:
    fh.write(src)
    old_file = fh.name
VO = load_module('old_verify_closure_cert', old_file)
os.unlink(old_file)
bad_old = copy.deepcopy(bad)
bad_old['xpoints'] = [['0', '0', '0', '2']]       # the HEAD verifier read the top level
rc, det = run(VO.main, bad_old)
report('closure: same unsound pruning [HEAD verifier, before revision]', rc, True, det)
negc = copy.deepcopy(wc)
negc['instance']['lam'] = ['20', '20', '20', '-5']
rc, det = run(VC.main, negc)
report('closure: lam = (20, 20, 20, -5), negative inactive entry', rc, True, det)

print()
unexpected = [r for r in results if (r[1] != 0) != r[2]]
print('%d probes, %d unexpected outcomes:' % (len(results), len(unexpected)))
for r in unexpected:
    print('  ', r[0], 'exit', r[1])
