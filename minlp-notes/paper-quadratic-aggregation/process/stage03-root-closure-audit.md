# Coordinator's closure audit

The stage 3 author will independently verify the proposed example below.
This record documents source inspection and an exact mathematical derivation,
not acceptance by the subsequent five paper reviewers.

## Primary text and search

Inspected the author-hosted published PDF of Kojima--Tuncel (2000),
https://www.math.uwaterloo.ca/~ltuncel/publications/nonconvex.pdf,
available in `/tmp/quadratic-paper-literature/kt.pdf` and its layout extraction.
Printed p.759 was also rendered and visually inspected. Theorem 4.2 states
exact equality of the SDP projection and convex-quadratic aggregation
relaxation. Its displayed dual-cone-intersection identity omits closure.
Printed p.750 states that F is compact throughout the paper. Sections 2.1--2.3
define the quadratic representation and SDP lift with actual existential
matrix witnesses, without a closure in the projection definition. Empty
feasible sets are expressly allowed in the introduction.

On 2026-09-22, searched combinations of the exact title and authors with
`erratum`, `errata`, `correction`, `error`, `closure`, `nonclosed`, and
`Theorem 4.2`. No matching erratum or documented correction was found.
The author publication directory
https://www.math.uwaterloo.ca/~ltuncel/publications/ and publisher record
https://epubs.siam.org/doi/10.1137/S1052623498336450 were inspected; neither
exposed an erratum. This is a bounded search, not proof that no correction
exists. Unrelated search results are not evidence about this theorem.

## Compact strictly feasible counterexample candidate

The earlier two-row nonclosed-projection example has unbounded feasible set,
so it alone should not be used to contradict a theorem with standing
compactness. A four-row strengthening removes that limitation:

```
f1(x,y)=2xy+1,       f2(x,y)=x^2-x,
f3(x,y)=-2xy-2,      f4(x,y)=1/4-x.
```

The non-strict feasible set is
`T={1/4<=x<=1, -1<=xy<=-1/2}`, a nonempty compact set; its y coordinates
lie in `[-4,-1/2]`. The strict system contains `(1/2,-3/2)`.
For nonnegative weights the quadratic coefficient matrix is
`[[lambda2,lambda1-lambda3],[lambda1-lambda3,0]]`.
It is PSD exactly when `lambda1=lambda3`. Every convex aggregation then is
`lambda2(x^2-x)+lambda4(1/4-x)-lambda1`.
Their intersection is exactly the closed strip `1/4<=x<=1`.

For `1/4<=x<1` and arbitrary y, choose `X11=(x^2+x)/2`,
`X12=-3/4`, and
`X22=y^2+(-3/4-xy)^2/((x-x^2)/2)`.
The covariance `X-(x,y)(x,y)^T` is PSD of rank one; lifted constraints
f1 and f3 have value -1/2, and f2 and f4 are nonpositive.
At x=1, the second row and PSD require X11=1; zero covariance in its first
diagonal forces X12=y. The remaining inequalities require
`-1<=y<=-1/2`, and an exact rank-one lift suffices there.
Consequently the actual projection is
`([1/4,1) x R) union ({1} x [-1,-1/2])`.
It is not closed, while its closure is the full aggregation strip.

The example illustrates why a closure qualification is necessary even with
strict feasibility and a compact original feasible set. It is not a novelty
claim about nonclosed SDP projections. The manuscript should prove the
precise closure relation it needs independently, credit the established
Fujie--Kojima relationship, and avoid importing the unqualified KT assertion.

## Targeted exact check

Ran the following standard-library check from the repository root. It passed
nine particular PSD lifts and the strict point; the universal formulas above
still require mathematical proof and review.

```sh
python3 - <<'PY'
from fractions import Fraction as F
for x in (F(1,4), F(1,2), F(99,100)):
    for y in (F(-100), F(0), F(100)):
        v=(x-x*x)/2
        z=F(-3,4)-x*y
        X11=(x*x+x)/2
        X12=F(-3,4)
        X22=y*y+z*z/v
        assert v>0 and (X11-x*x)*(X22-y*y)-(X12-x*y)**2==0
        assert 2*X12+1<0 and -2*X12-2<0
        assert X11-x<=0 and F(1,4)-x<=0
x,y=F(1,2),F(-3,2)
assert all(v<0 for v in (2*x*y+1,x*x-x,-2*x*y-2,F(1,4)-x))
print('PASS: nine exact PSD lifts and the strict feasible point')
PY
```

No project-wide check or CI inspection was run.
