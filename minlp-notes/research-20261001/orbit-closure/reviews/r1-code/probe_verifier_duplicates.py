"""Reviewer's probe of verify_box_cert.py (stream code, run as a subprocess; not modified).

Builds a false certificate from logs/boxcert_thm14_BP.json: lam_hat is halved to (1/10, 0, 1/12),
which is NOT in Cl_BP (the (BP) set of bp_lower.log has all steps >= 2539/10000, so its cut gives
a^T lam <= (10000/2539)(1/10 + 1/12) < 0.73 < 1).  Every ray entry of every cut leaf is then listed
twice, once under its key 'j' and once under the key '0j' (int('0j') = j), and every kept-boundary
ray twice in 'kb'.  A sound verifier must reject the result.
Usage: python3 probe_verifier_duplicates.py
"""
import json, copy, subprocess, tempfile, os, sys
from fractions import Fraction as Fr

CODE = os.path.join(os.path.dirname(__file__), '..', '..', 'code')
d = json.load(open(os.path.join(CODE, '..', 'logs', 'boxcert_thm14_BP.json')))
m = copy.deepcopy(d)
m['lam'] = [str(Fr(x) / 2) for x in d['lam']]
for lf in m['leaves']:
    if lf['type'] == 'cut':
        for js, v in list(lf['v'].items()):
            lf['v']['0' + js] = v
        lf['kb'] = lf.get('kb', []) * 2
print('false point lam = %s; bound for the bp_lower.log set: a^T lam <= %s < 1'
      % (m['lam'], float(Fr(10000, 2539) * (Fr(1, 10) + Fr(1, 12)))))


def run(cert):
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as fh:
        json.dump(cert, fh)
        name = fh.name
    r = subprocess.run([sys.executable, 'verify_box_cert.py', name], cwd=CODE, capture_output=True, text=True,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    os.unlink(name)
    return r.returncode, r.stdout.strip().splitlines()[-2:]


m0 = copy.deepcopy(d); m0['lam'] = m['lam']
print('halved point, no duplicates  ->', run(m0))
print('halved point, duplicated rays ->', run(m))
