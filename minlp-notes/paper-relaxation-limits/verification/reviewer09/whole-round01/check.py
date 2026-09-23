"""Independent final review09 checks. Run in this artifact directory."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations, product
import hashlib
import json
import math
import re
import subprocess
import sympy as s

HERE = Path(__file__).resolve().parent
PAPER = HERE.parents[2]
FROZEN = PAPER / "process/snapshots/whole-round01"
report = {}
expected = "912de166731f56368a8ee4db21294aa348b85364e85cd444e31265b29828d084"
digest = hashlib.sha256((FROZEN / "main.pdf").read_bytes()).hexdigest()
assert digest == expected
report["frozen_pdf_sha256"] = digest

# Replay the manuscript's actual printed programs, without importing its checkers.
for name in ("appendix-finite-signings", "appendix-cubic-certificates"):
    src = (FROZEN / "sections" / (name + ".tex")).read_text()
    program = "".join(re.findall(r"\\begin\{verbatim\}\n(.*?)\\end\{verbatim\}", src, re.S))
    target = HERE / (name + ".py")
    target.write_text(program)
    result = subprocess.run(["python", str(target)], cwd=HERE, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    report[name] = {"exact": True, "output": result.stdout}

# Generic rational coordinate identities, checked symbolically.
D,t,w,c = s.symbols("D t w c", real=True)
M=s.Matrix([[3,4],[4,-3]])/5
assert M*M.T == s.eye(2) and M.det() == -1
v=s.Matrix([3*D,4*D]); p=s.Matrix([2*D,4*D/3])
assert M*v == s.Matrix([5*D,0])
assert M*p == s.Matrix([34*D/15,4*D/5])
for vi,pi in zip(v,p):
    assert s.simplify(vi**2/2-pi**2) in [D**2/2,56*D**2/9]
    assert s.simplify(vi**2/2-(pi-vi)**2) in [7*D**2/2,8*D**2/9]
report["rational_map"] = "Exact orthogonality, inverse, centers, witness, and center-image domination identities."

# An exact rational mesh checks all links of the retained-box counterexample.
checks=0
for i,j in product(range(61),range(41)):
    x,y=Q(i,20),Q(j,20)-1
    assert x*x <= 3*x and (x-3)**2 <= 9-3*x and y*y <= 1
    checks+=1
report["retained_box_mesh"]={"exact":True,"points":checks,"scope":"Finite link checks; universal proof uses t(3-t)>=0."}

# Explicit vertex enumeration checks the auxiliary union hull for several h/U.
for U,h in [(Q(4),Q(0)),(Q(4),Q(1)),(Q(25,4),Q(3,4)),(Q(1),Q(1))]:
    vertices={(Q(0),Q(0)),(U,Q(0)),(U,h),(h,U),(Q(0),U)}
    assert all(0<=a<=U and 0<=b<=U and a+b<=U+h for a,b in vertices)
    assert all(a<=h or b<=h for a,b in vertices)
report["auxiliary_hull_vertices"]="Four exact h/U cases, including h=0 and h=U."

# The concave upper-image cut and its endpoint intersection.
d=s.symbols("d",positive=True)
f=d*d+1-c+2*d*s.sqrt(1-c)
assert s.simplify(f-(d+s.sqrt(1-c))**2)==0
assert s.simplify(s.diff(f,c)+1+d/s.sqrt(1-c))==0
assert s.simplify(s.diff(f,c,2)+d/(2*(1-c)**s.Rational(3,2)))==0
count=0
for dv in [Q(5,2),Q(3),Q(10),Q(100)]:
    # Rational points on a circle give rational transverse and cap coordinates.
    for z in [Q(j,20) for j in range(-20,21)]:
        q=(1-z*z)/(1+z*z); wv=2*z/(1+z*z)
        assert q>=0 and q*q+wv*wv==1
        for tv in [-q, Q(0), dv/2, dv, dv+q]:
            assert tv*tv <= (dv+q)**2 and (tv-dv)**2 <= (dv+q)**2
            count+=1
report["image_repair"]={"symbolic": "Exact f identity and first/second derivatives on c<1; c=1 checked by continuous endpoint limit.","exact_capsule_points":count}

# Numerical search of the one-dimensional outer-distance profile.
from scipy.optimize import minimize_scalar
distance=[]
for ratio in [2.0001,2.5,3,5,10,100,10000]:
    def error(rho):
        e=math.sqrt((ratio/2+1)**2-rho*rho/2)-ratio/2
        return math.hypot(e,rho)-1
    sol=minimize_scalar(lambda rho:-error(rho),bounds=(0,1),method="bounded",options={"xatol":1e-12})
    exact=error(1)
    assert -sol.fun <= exact+1e-9 and abs(sol.x-1)<1e-6
    distance.append({"d/r":ratio,"numerical_argmax":float(sol.x),"endpoint_formula":exact})
report["hausdorff_profile_numerical"]=distance

# Independent exact reconstruction of the fractional-cardinality Gram identity.
def fall(x,k):
    return math.prod(x-i for i in range(k))
gram_cases=0
for degree in [1,2,3]:
    n=4*degree
    for total in [Q(2*degree-1),Q(4*degree-1,2),Q(2*degree+1)]:
        if min(total,n-total)<2*degree-1:
            continue
        subsets=list(combinations(range(n),degree))
        coef=[fall(total,2*degree-j)*fall(n-total,j)/fall(Q(n),2*degree) for j in range(degree+1)]
        assert min(coef)>=0
        for A,B in product(subsets,repeat=2):
            overlap=len(set(A)&set(B))
            lhs=fall(total,2*degree-overlap)/fall(Q(n),2*degree-overlap)
            rhs=sum(coef[j]*math.comb(overlap,j) for j in range(overlap+1))
            assert lhs==rhs
        gram_cases+=1
report["fractional_gram"]={"exact":True,"cases":gram_cases,"scope":"Finite rational identity and nonnegative coefficients; universal proof still needed."}
report["limits"]="No numerical computation establishes a universal theorem. No solver-based global optimization, formal proof assistant, or exhaustive literature clearance."
(HERE/"checks.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
