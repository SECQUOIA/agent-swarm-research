# Exact .gms vs OSIL comparison (rows/objective via exact_forms.compare on this /tmp copy)
# plus exact comparison of variable types and bounds. Writes nothing outside this directory.
import json, os, re, sys, time
import xml.etree.ElementTree as ET
from fractions import Fraction as F
import exact_forms as X
X.POINTS = {}
_orig = X.gms_objective
def _gobj(g):
    try:
        return _orig(g)
    except AssertionError:
        # epigraph form: objvar appears in an inequality row and stays a variable in the OSIL
        return None, {((g['objvar'], 1),): F(1)}
X.gms_objective = _gobj
NS = X.NS
INF = None
def gms_vars(path):
    text = open(path).read()
    decl = {}
    for kind, body in re.findall(r"(?ms)^(Positive|Negative|Binary|Integer|SOS1|SOS2|Semicont|Semiint)?\s*Variables\s+(.*?);", text):
        for v in re.split(r"[\s,]+", body.strip()):
            if v:
                decl[v] = (kind or 'Free') if v not in decl or kind else decl[v]
    lb, ub = {}, {}
    for v, k in decl.items():
        lb[v], ub[v] = {'Free': ('-inf', 'inf'), 'Positive': ('0', 'inf'), 'Negative': ('-inf', '0'),
                        'Binary': ('0', '1'), 'Integer': ('0', 'inf')}[k]
    for v, att, val in re.findall(r"(?<![\w.])([A-Za-z_]\w*)\.(lo|up|fx)\s*=\s*([-+0-9.eE]+)\s*;", text):
        if att in ('lo', 'fx'): lb[v] = val
        if att in ('up', 'fx'): ub[v] = val
    return decl, lb, ub
def osil_vars(path):
    d = ET.parse(path).getroot().find(NS + 'instanceData')
    out = {}
    for v in d.find(NS + 'variables'):
        t = v.get('type', 'C')
        lb = v.get('lb', '0'); ub = v.get('ub', 'INF')
        if t == 'B' and v.get('ub') is None: ub = '1'
        out[v.get('name')] = (t, lb, ub)
    return out
def num(s):
    s = s.strip().lower()
    if s in ('inf', '+inf'): return 'inf'
    if s == '-inf': return '-inf'
    return F(s)
kmap = {'Free': 'C', 'Positive': 'C', 'Negative': 'C', 'Binary': 'B', 'Integer': 'I'}
for name in sys.argv[1:]:
    t0 = time.time()
    r = X.compare(name)
    decl, glb, gub = gms_vars(os.path.join(X.HERE, 'pages', 'models', 'gms', name + '.gms'))
    ov = osil_vars(os.path.join(X.OSIL, name + '.osil'))
    obj = decl.pop('objvar', None) if 'objvar' not in ov else None
    bad = []
    if set(decl) != set(ov):
        bad.append(('names', len(set(decl) ^ set(ov))))
    for v, (t, lb, ub) in ov.items():
        if v not in decl: continue
        if kmap[decl[v]] != t: bad.append((v, 'type', decl[v], t))
        if num(glb[v]) != num(lb): bad.append((v, 'lb', glb[v], lb))
        if num(gub[v]) != num(ub): bad.append((v, 'ub', gub[v], ub))
    print(json.dumps(dict(name=name, sense=r['sense'], rows_gms=r['rows_gms'], rows_osil=r['rows_osil'],
          rows_equal=r['rows_equal'], rows_different=r['rows_different'], objective_diffs=r['objective'].get('n'),
          nvars=len(ov), var_mismatches=len(bad), first=bad[:4], sec=round(time.time() - t0, 1)), default=str), flush=True)
