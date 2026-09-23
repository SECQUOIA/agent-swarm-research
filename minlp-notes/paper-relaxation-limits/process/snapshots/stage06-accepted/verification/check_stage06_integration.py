"""Exact finite checks of integrated formulas, source coverage and accepted-file integrity.

Run from any directory with SymPy available. Finite examples supplement proofs.
The check never modifies accepted snapshots or repository source programs.
"""
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import re
import sympy as s

PAPER = Path(__file__).resolve().parents[1]

def main():
    cases = []
    n, X, T, W = variables = s.symbols('n X T W')
    # Enumerate vertices of the eliminated four-dimensional polytope exactly,
    # independently comparing its result with the six disaggregated atoms.
    for ell, upper, a, b, N in [(s.Rational(1,3),s.Rational(7,5),s.Rational(-2,3),s.Rational(5,4),3),(0,2,-1,2,2),(1,3,0,4,1)]:
        U = N*upper
        slacks = [n,N-n,T-a,b-T,X-n*ell,n*upper-X,
            W-a*X,W-(b*X+U*T-U*b),a*X+U*T-U*a-W,b*X-W,
            b*X+ell*(N*T-N*a-n*(b-a))-W,
            W-a*X-ell*(N*T-N*b+n*(b-a))]
        rows = [(s.Matrix([[s.diff(f,z) for z in variables]]), f.subs(dict.fromkeys(variables,0))) for f in slacks]
        vertices = set()
        for subset in combinations(range(len(rows)),4):
            A = s.Matrix.vstack(*(rows[i][0] for i in subset))
            if A.det() == 0:
                continue
            v = tuple(A.inv()*s.Matrix([-rows[i][1] for i in subset]))
            if all((row*s.Matrix(v))[0]+constant >= 0 for row,constant in rows):
                vertices.add(v)
        expected = {(s.Integer(0),s.Integer(0),s.sympify(t),s.Integer(0)) for t in [a,b]}
        expected |= {(s.sympify(N),s.sympify(N*q),s.sympify(t),s.sympify(N*q*t)) for q,t in product([ell,upper],[a,b])}
        assert vertices == expected, (vertices, expected)
        cases.append({'parameters': list(map(str,[ell,upper,a,b,N])), 'vertices': len(vertices)})
    D,t,w = s.symbols('D t w', real=True)
    x,y = (3*t+4*w)/5,(4*t-3*w)/5
    assert s.expand(x*x+y*y-t*t-w*w) == 0
    assert s.expand((x-3*D)**2+(y-4*D)**2-(t-5*D)**2-w*w) == 0
    t0,w0 = s.Rational(34,15)*D,s.Rational(4,5)*D
    assert x.subs({t:t0,w:w0}) == 2*D
    assert y.subs({t:t0,w:w0}) == s.Rational(4,3)*D
    sign_checks = 0
    for k in [3,5,7]:
        for bits in product([0,1],repeat=k):
            signs=[2*x-1 for x in bits]
            slack=s.Rational(sum(signs)**2-1,4*k*k)
            centered=((sum(bits)-s.Rational(k,2))**2-s.Rational(1,4))/(k*k)
            assert slack == centered and slack >= 0
            sign_checks += 1
    assert -s.Rational(7,2)*s.Rational(3,2)-s.Rational(1,2) == -s.Rational(23,4)
    sources=[PAPER/'main.tex',*sorted((PAPER/'sections').glob('*.tex'))]
    text='\n'.join(p.read_text() for p in sources)
    labels=set(re.findall(r'\\label\{([^}]+)\}',text))
    ledger=(PAPER/'process/claim-coverage.md').read_text()
    cited=set(re.findall(r'`((?:app|sec|subsec|thm|prop|lem|cor|eq|tab):[^`]+)`',ledger))
    assert not cited-labels, sorted(cited-labels)
    snapshot=PAPER/'process/snapshots/stage05-accepted'
    accepted=[snapshot/'macros.tex',*sorted((snapshot/'sections').glob('*.tex'))]
    integrity={str(p.relative_to(snapshot)):p.read_bytes()==(PAPER/p.relative_to(snapshot)).read_bytes() for p in accepted}
    assert all(integrity.values())
    report={'scaling_exact_polytope_cases':cases,'rational_rotation_identities':'PASS',
        'sign_slack_binary_cases':sign_checks,'psd_prefactor_exponent':'-23/4',
        'coverage_labels_checked':len(cited),'missing_coverage_labels':[],
        'accepted_mathematical_files_unchanged':integrity,
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope':'Finite exact examples and integration checks; not general theorem certification.'}
    (PAPER/'verification/check_stage06_integration.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__ == '__main__':
    main()
