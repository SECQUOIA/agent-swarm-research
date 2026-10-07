"""Rejection tests for verify_box_cert.py: corrupted certificates must fail.

Usage: python3 test_verify_box_cert.py CERT_B.json CERT_BP.json
Each mutation is written to a temporary file and verified; the test passes if the verifier
returns a nonzero status for every mutation (and zero for the unmodified certificates).
"""
import sys, json, copy, tempfile, os, io, contextlib
from fractions import Fraction as Fr
import verify_box_cert as V


def run(d, duplicate_json_key=False, raw=None):
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as fh:
        if raw is None:
            raw = json.dumps(d)
        if duplicate_json_key:
            lf = next(lf for lf in d['leaves'] if lf['type'] == 'cut' and lf['v'])
            j = next(iter(lf['v']))
            entry = json.dumps({j: lf['v'][j]})[1:-1]
            raw = raw.replace('"v": {', '"v": {' + entry + ', ', 1)
        fh.write(raw)
        name = fh.name
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            rc = V.main(name)
        except Exception as e:          # a crash on corrupted input also counts as rejection
            rc = 2
    os.unlink(name)
    return rc


def mutations(d):
    fam = d['family']
    out = []
    for name, lam in (
        ('negative lam_hat entry', ['-1'] + d['lam'][1:]),
        ('missing lam_hat entry', d['lam'][:-1]),
        ('extra nonnegative lam_hat entry', d['lam'] + ['0']),
        ('extra negative lam_hat entry', d['lam'] + ['-5']),
    ):
        m = copy.deepcopy(d); m['lam'] = lam
        out.append((name, m))
    m = copy.deepcopy(d); m['lam'] = [str(Fr(x) * Fr(9, 10)) for x in d['lam']]
    out.append(('lam_hat scaled by 9/10', m))
    m = copy.deepcopy(d); m['leaves'] = m['leaves'][1:]
    out.append(('one leaf removed', m))
    m = copy.deepcopy(d); m['status'] = 'incomplete: time limit'
    out.append(('status incomplete', m))
    i = next(k for k, lf in enumerate(d['leaves']) if lf['type'] == 'cut' and lf['v'])
    m = copy.deepcopy(d); j = next(iter(m['leaves'][i]['v']))
    v = m['leaves'][i]['v'][j]; m['leaves'][i]['v'][j] = [v[1], v[0]]
    out.append(('test vector of a cut leaf swapped', m))
    m = copy.deepcopy(d); m['leaves'][i]['type'] = 'skip'
    out.append(('cut leaf relabelled skip', m))
    m = copy.deepcopy(d); m['leaves'][i]['lo'] = [str(Fr(x) - Fr(1, 2 ** 20)) for x in m['leaves'][i]['lo']]
    out.append(('leaf box moved', m))
    j = next(iter(d['leaves'][i]['v']))
    m = copy.deepcopy(d); m['leaves'][i]['v']['0' + j] = m['leaves'][i]['v'][j]
    out.append(('aliased vector ray key', m))
    m = copy.deepcopy(d); m['leaves'][i]['v']['0' + j] = m['leaves'][i]['v'].pop(j)
    out.append(('non-canonical vector ray key', m))
    for bad_key in ('-1', str(len(d['rays']))):
        m = copy.deepcopy(d); m['leaves'][i]['v'][bad_key] = m['leaves'][i]['v'].pop(j)
        out.append(('out-of-range vector ray ' + bad_key, m))
    if fam == 'B':
        k = next(k for k, lf in enumerate(d['leaves']) if lf['type'] == 'excl')
        m = copy.deepcopy(d); m['leaves'][k]['v'] = ['1', '0']
        out.append(('exclusion vector replaced by e_1', m))
        m = copy.deepcopy(d); m['sbar'] = [str(Fr(d['sbar'][0]) + 1)] + d['sbar'][1:]
        out.append(('sbar changed', m))
    else:
        k = next((k for k, lf in enumerate(d['leaves']) if lf['type'] == 'cut' and lf.get('kb')), None)
        if k is not None:
            m = copy.deepcopy(d); m['leaves'][k]['kb'] = []
            out.append(('kept-boundary rays dropped', m))
            j = d['leaves'][k]['kb'][0]
            m = copy.deepcopy(d); m['leaves'][k]['kb'].append(j)
            out.append(('repeated kept-boundary ray', m))
            m = copy.deepcopy(d); m['leaves'][k]['kb'].append('0' + j)
            out.append(('aliased kept-boundary ray', m))
            m = copy.deepcopy(d); m['leaves'][k]['kb'][0] = '0' + j
            out.append(('non-canonical kept-boundary ray', m))
            m = copy.deepcopy(d); m['leaves'][k]['v'][j] = ['1', '0']
            out.append(('same ray in vectors and kept-boundary', m))
            for bad_key in ('-1', str(len(d['rays']))):
                m = copy.deepcopy(d); m['leaves'][k]['kb'][0] = bad_key
                out.append(('out-of-range kept-boundary ray ' + bad_key, m))
        m = copy.deepcopy(d); m['lam'] = [str(Fr(x) / 2) for x in d['lam']]
        for lf in m['leaves']:
            if lf['type'] == 'cut':
                for js, v in list(lf['v'].items()):
                    lf['v']['0' + js] = v
                lf['kb'] = lf.get('kb', []) * 2
        out.append(('reviewer false point with doubled rays', m))
        m = copy.deepcopy(d); m['bpchart'] = 'pq' if d.get('bpchart') == 'u' else 'u'
        out.append(('chart kind changed', m))
    return out


def reviewer_probes(d):
    """Round 2 box probes, all double-counting attempts on the false half-point."""
    half = copy.deepcopy(d)
    half['lam'] = [str(Fr(x) / 2) for x in d['lam']]
    out = [('reviewer false half-point, no tricks', half)]
    probes = [
        ('underscore alias', lambda lf: lf['v'].update({'0_' + k: v for k, v in list(lf['v'].items())})),
        ('whitespace alias', lambda lf: lf['v'].update({' ' + k: v for k, v in list(lf['v'].items())})),
        ('plus alias', lambda lf: lf['v'].update({'+' + k: v for k, v in list(lf['v'].items())})),
        ('minus-zero alias', lambda lf: lf['v'].update({'-' + k: v for k, v in list(lf['v'].items()) if k == '0'})),
        ('Arabic-Indic alias', lambda lf: lf['v'].update({chr(0x660 + int(k)): v for k, v in list(lf['v'].items())})),
        ('full-width alias', lambda lf: lf['v'].update({chr(0xFF10 + int(k)): v for k, v in list(lf['v'].items())})),
        ('integer kb entries doubled', lambda lf: lf.update(kb=[int(j) for j in lf.get('kb', [])] * 2)),
        ('kb as a doubled string', lambda lf: lf.update(kb=''.join(lf.get('kb', [])) * 2)),
        ('kb as an object with aliases', lambda lf: lf.update(kb={j: 1 for j in lf.get('kb', [])} | {'0' + j: 1 for j in lf.get('kb', [])})),
        ('every v ray also in kb', lambda lf: lf.update(kb=list(lf.get('kb', [])) + [k for k in lf['v'] if k not in lf.get('kb', [])])),
    ]
    for name, mutate in probes:
        m = copy.deepcopy(half)
        for lf in m['leaves']:
            if lf['type'] == 'cut':
                mutate(lf)
        out.append(('reviewer ' + name, m))
    m = copy.deepcopy(half); m['leaves'] += copy.deepcopy(m['leaves'])
    out.append(('reviewer every leaf listed twice', m))
    listed = {j for lf in d['leaves'] if lf['type'] == 'cut'
              for j in list(lf['v']) + list(lf.get('kb', []))}
    for j in range(len(d['rays'])):
        if str(j) not in listed:
            m = copy.deepcopy(d); m['lam'][j] = '-1'
            out.append(('reviewer negative entry on unlisted ray', m))
    raw_v = json.dumps(half).replace('"v": {', '"v": {"0": ["1", "0"]}, "v": {', 1)
    raw_lam = json.dumps(d).replace('"lam": [', '"lam": ' + json.dumps(half['lam']) + ', "lam": [', 1)
    return out, [('reviewer duplicate literal v key', raw_v),
                 ('reviewer duplicate top-level lam key', raw_lam)]


def main():
    allok = True
    rejected = total = 0
    for path in sys.argv[1:]:
        d = json.load(open(path))
        rc = run(d)
        print('%s: unmodified certificate -> exit %d (%s)' % (path, rc, 'ok' if rc == 0 else 'UNEXPECTED'))
        allok &= rc == 0
        rc = run(d, duplicate_json_key=True)
        print('   duplicate literal JSON ray key           -> exit %d (%s)'
              % (rc, 'rejected' if rc != 0 else 'NOT REJECTED'))
        allok &= rc != 0
        total += 1; rejected += rc != 0
        cases = mutations(d)
        raw_cases = []
        if d['family'] == 'BP':
            probes, raw_cases = reviewer_probes(d)
            cases += probes
        for name, m in cases:
            rc = run(m)
            print('   %-40s -> exit %d (%s)' % (name, rc, 'rejected' if rc != 0 else 'NOT REJECTED'))
            allok &= rc != 0
            total += 1; rejected += rc != 0
        for name, raw in raw_cases:
            rc = run(d, raw=raw)
            print('   %-40s -> exit %d (%s)' % (name, rc, 'rejected' if rc != 0 else 'NOT REJECTED'))
            allok &= rc != 0
            total += 1; rejected += rc != 0
    print('%d of %d mutations rejected' % (rejected, total))
    print('ALL REJECTION TESTS PASS' if allok else 'SOME REJECTION TEST FAILED')
    sys.exit(0 if allok else 1)


if __name__ == '__main__':
    main()
