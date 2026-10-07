"""Estimate the page span of each block that C-writing-1 proposes to move.

Uses pdftotext -layout output of /tmp/dpaper/out/main.pdf. A position is
page + (line index on page)/(lines on page); spans are differences.
"""
import re, subprocess
subprocess.run(['pdftotext', '-layout', '/tmp/dpaper/out/main.pdf', '/tmp/cw1.txt'], check=True)
pages = open('/tmp/cw1.txt').read().split('\f')
lines = []  # (page, frac)
for pi, p in enumerate(pages):
    pl = p.split('\n')
    for li, l in enumerate(pl):
        lines.append((pi + 1 + li / max(len(pl), 1), l))

def find(pat, after=0.0):
    for pos, l in lines:
        if pos >= after and re.search(pat, l):
            return pos
    raise ValueError(pat)

def span(start, end, after=0.0):
    a = find(start, after)
    b = find(end, a + 1e-9)
    return a, b, b - a

blocks = [
    ('7.2 Prop 7.5 setup+statement', r'^Grid min-marginals are not certified', r'^7\.3\s+Certified convex', 0),
    ('7.3 Thm 7.12, Prop 7.13 + discussion', r'^Recognizing a globally affine', r'^7\.4\s+Separately', 0),
    ('Rem 8.2 + Prop 8.3', r'^Remark 8\.2', r'^8\.2\s+Feasible rounding', 0),
    ('Ex 8.11', r'^Example 8\.11', r'^8\.5\s+Complexity', 0),
    ('8.6 TU exact', r'^8\.6\s+Exact output', r'^8\.7\s+The uniform', 0),
    ('Prop 8.15 + Ex 8.16', r'Natural non-uniform alternatives fail', r'^Remark 8\.17', 0),
    ('proof Prop 9.1', r'^Proof\. The instance', r'Other methods solve this instance', 0),
    ('proof Lem 9.6', r'^Proof\.', r'^Theorem 9\.7', find(r'^Lemma 9\.6')),
    ('proof Cor 9.8', r'^Proof\.', r'^Remark 9\.9', find(r'^Corollary 9\.8')),
    ('PROX..before Prop 9.16', r'Lemma 9\.10 checks a candidate', r'^Proposition 9\.16', 0),
    ('  of which Thm 9.15 (kept)', r'^Theorem 9\.15', r'^Proposition 9\.16', 0),
    ('proof Prop 10.7', r'^Proof\.', r'^10\.5\s+Point growth', find(r'^Proposition 10\.7')),
    ('proof Prop 10.8', r'^Proof\.', r'^\s*\S', find(r'^Proposition 10\.8')),
    ('proof Prop 10.10', r'^Proof\.', r'^10\.7\s+Local corrections', find(r'^Proposition 10\.10')),
    ('Sec 10 bullet list', r'Conditioning and width \(Sections', r'^Del Pia and Khajavirad prove that cont', 0),
]
tot = 0
for name, s, e, after in blocks:
    try:
        a, b, d = span(s, e, after)
        print(f'{name:40s} p{a:7.2f} -> p{b:7.2f}  span {d:5.2f}')
    except ValueError as ex:
        print(name, 'not found', ex)
for sec, s, e in [('S1', r'^1\s+Introduction', r'^2\s+Related work'), ('S2', r'^2\s+Related work', r'^3\s+Problem class'),
                  ('S3-6', r'^3\s+Problem class', r'^7\s+Conditional recourse'), ('S7-9', r'^7\s+Conditional recourse', r'^10\s+Structural limits'),
                  ('S10', r'^10\s+Structural limits', r'^11\s+Implementation'), ('S11-12', r'^11\s+Implementation', r'^References')]:
    a, b, d = span(s, e)
    print(f'{sec:8s} {a:7.2f} -> {b:7.2f} span {d:5.2f}')
