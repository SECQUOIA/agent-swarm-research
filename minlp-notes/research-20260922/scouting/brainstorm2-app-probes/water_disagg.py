import re, sys
src, dst = sys.argv[1], sys.argv[2]
txt = open(src).read()
# split into header / equations / rest
eqs = {}
for m in re.finditer(r'^(e\d+)\.\.(.*?);', txt, re.S | re.M):
    eqs[m.group(1)] = (m.start(), m.end(), ' '.join(m.group(2).split()))
lb, ub = {}, {}
for m in re.finditer(r'(x\d+)\.(lo|up|fx) = ([-\d.eE+]+);', txt):
    v, k, val = m.group(1), m.group(2), float(m.group(3))
    if k in ('lo', 'fx'): lb[v] = val
    if k in ('up', 'fx'): ub[v] = val
hl = {}   # pipe -> (eq, q, C, c, A, xi, xj)
pat = re.compile(r'SignPower\((x\d+),1\.852\)-([\d.eE+-]+)\*\(([\d.]+)\*(x\d+)\)\*\*2\.435\*\((-?[\d.]+|x\d+)-(-?[\d.]+|x\d+)\)=E=0')
pat2 = re.compile(r'SignPower\((x\d+),1\.852\) - ([\d.eE+-]+)\*\(([\d.]+)\*(x\d+)\)\*\*2\.435\*\( ?(-?[\d.]+) - (x\d+)\) =E= 0')
pat3 = re.compile(r'SignPower\((x\d+),1\.852\) - ([\d.eE+-]+)\*\(([\d.]+)\*(x\d+)\)\*\*2\.435\*\( ?(x\d+) - ([\d.]+)\) =E= 0')
un = 0
for e, (s, t, body) in eqs.items():
    if 'SignPower' not in body: continue
    m = pat.search(body.replace(' ',''))
    if not m: print('UNPARSED', e, body); un += 1; continue
    hl[e] = m.groups()
area = {}  # A var -> list of (a_d, b)
for e, (s, t, body) in eqs.items():
    m = re.match(r'(x\d+) ((?:- [\d.eE+-]+\*b\d+ ?)+)=E= 0', body)
    if m:
        area[m.group(1)] = [(float(a), b) for a, b in re.findall(r'- ([\d.eE+-]+)\*(b\d+)', m.group(2))]
vel = {}
for e, (s, t, body) in eqs.items():
    m = re.match(r'(x\d+) - ([\d.]+)\*(x\d+) =L= 0', body)
    if m: vel[m.group(1)] = float(m.group(2))
print('headloss rows', len(hl), 'unparsed', un, 'area rows', len(area), 'vel', len(vel))
def bnd(v, side):
    try: return float(v)  # constant
    except ValueError: return (lb if side == 'lo' else ub)[v]
newvars, neweqs, newbnds = [], [], []
cut = []
for e, (q, C, c, A, xi, xj) in hl.items():
    C, c = float(C), float(c)
    dh_expr = f"({xi} - {xj})"
    Hmax = max(abs(bnd(xi, 'up') - bnd(xj, 'lo')), abs(bnd(xi, 'lo') - bnd(xj, 'up')))
    vq = vel[q]
    qs, ds = [], []
    for k, (a, b) in enumerate(area[A]):
        qn, dn = f"q{e}_{k}", f"h{e}_{k}"
        newvars += [qn, dn]
        R = C * (c * a) ** 2.435
        hcap = min(Hmax, (vq * a) ** 1.852 / R)
        neweqs.append((f"hl{e}_{k}", f"SignPower({qn},1.852) - {R!r}*{dn} =E= 0"))
        neweqs.append((f"qu{e}_{k}", f"{qn} - {vq*a!r}*{b} =L= 0"))
        neweqs.append((f"ql{e}_{k}", f"{qn} + {vq*a!r}*{b} =G= 0"))
        neweqs.append((f"du{e}_{k}", f"{dn} - {hcap!r}*{b} =L= 0"))
        neweqs.append((f"dl{e}_{k}", f"{dn} + {hcap!r}*{b} =G= 0"))
        newbnds.append(f"{qn}.lo = {-vq*a!r}; {qn}.up = {vq*a!r}; {dn}.lo = {-hcap!r}; {dn}.up = {hcap!r};")
        qs.append(qn); ds.append(dn)
    neweqs.append((f"qs{e}", f"{q} - " + " - ".join(qs) + " =E= 0"))
    neweqs.append((f"ds{e}", f"{dh_expr} - " + " - ".join(ds) + " =E= 0"))
    cut.append(e)
# rebuild text: replace original head-loss equation bodies by flow-sum equations
out = txt
qsum = {n: b for n, b in neweqs if n.startswith('qs')}
for e in sorted(cut, key=lambda e: -eqs[e][0]):
    s, t, _ = eqs[e]
    out = out[:s] + f"{e}.. " + qsum['qs' + e] + ";" + out[t:]
neweqs = [(n, b) for n, b in neweqs if not n.startswith('qs')]
# declare new variables/equations before 'Model' line
decl = "Variables " + ",\n".join(newvars) + ";\nEquations " + ",\n".join(n for n, _ in neweqs) + ";\n"
body = "\n".join(f"{n}.. {b};" for n, b in neweqs) + "\n" + "\n".join(newbnds) + "\n"
i = out.index('Model m')
out = out[:i] + body + out[i:]
j = re.search(r'^e1\.\.', out, re.M).start()
out = out[:j] + decl + out[j:]
open(dst, 'w').write(out)
