# Source and novelty audit: general symmetric output-error bodies

Date: 2026-09-05. Independent source audit of
[the general-norm draft](quadratic-general-norm-output-precision.md), separate
from its mathematical reviews.

The strong-separation-oracle version has a directly applicable classical
rounding source. I found no matching prior theorem constructing a rational
MILP within `O(n log(n+1))` integer coordinates of the unrestricted convex-lift
optimum for quadratic graphs under arbitrary symmetric error bodies. The
extension is a useful consequence of the repository's ellipsoidal covariance
and construction results. Its rounding algorithm is established; its proposed
contribution is the resulting whole-formulation guarantee, with overhead
independent of the number of outputs.

## Exact rounding import

Dadush, Peikert, and Vempala, *Enumerative Lattice Algorithms in Any Norm via
M-Ellipsoid Coverings*, author-hosted version dated 13 April 2011, Appendix B:

- Section B.2 uses binary encodings of rational matrices.
- Definition B.2 specifies strong separation at rational queries, with rational
  separating normals of polynomial encoding length. Algorithm runtimes depend
  on this polynomial bound.
- Theorem B.5, printed page 38, gives GLS-Round for a circumscribed convex body
  with that oracle. It outputs rational positive definite `A` and an ellipsoid
  `E(A)`, with `K subset t+E(A)` and either `vol(E(A))<=eta` or
  `t+E(A)/((d+1)sqrt(d)) subset K`.
- The stated runtime is polynomial in dimension, center encoding, and the
  logarithmic radius/threshold parameters. It is the deterministic GLS rounding
  routine, distinct from randomized M-ellipsoid routines elsewhere in the paper.

The authors explicitly attribute the rounding method to GLS. This audit checked
their primary statement, not the underlying GLS book proof.
[Author-hosted paper](https://sites.cc.gatech.edu/fac/cpeikert/pubs/svp-anynorm.pdf).

The draft originally mentioned a weak-separation alternative. The cited theorem
does not supply that extension. The author corrected the alternate effective-
body input model to strong separation during this audit; the present statement
therefore fits the checked source directly.

## How the draft meets the source assumptions

The following are checks of the draft's deductions rather than imported
rounding claims.

For the rational full-column-rank image basis `T`, the effective body is
`K_eff={z:Tz in K}`. Pulling an ambient strong separator back by `T^T` gives a
strong separator for this body. Its normal cannot vanish: the queried point
violates the inequality while zero belongs to the body. Rational elimination,
matrix multiplication, and the stated norm bounds give polynomial-size inputs
and queries. The known effective radii are

```
r = r_0/c_T,       R = R_0 c_L.
```

The rational threshold `eta=(r/d)^d/2` has polynomial binary encoding. The cube
`[-r/d,r/d]^d` lies in the known inner ball, so its volume already exceeds
`eta`. Consequently any outer ellipsoid has volume greater than `eta`, excluding
the small-volume alternative without a volume oracle.

Symmetry gives an exact recentering deduction. From `t+E/beta subset K_eff`,
negation and averaging imply `E/beta subset K_eff`. For `z in K_eff`, outer
containment of both `z` and `-z` gives `z-t,z+t in E`; their average is `z`.
Thus `K_eff subset E`. The final centered inner ellipsoid has rational matrix
`W=beta^2 A=d(d+1)^2 A`; the center and any matrix square root are unnecessary.

These observations resolve the volume-alternative, symmetry, and rational-
output issues. The dimension-zero case must remain separate, as in the draft.
Known inner and outer radii and polynomial-time rational strong separation are
material assumptions. The theorem does not establish such an oracle for every
informally specified norm, nor a practical running-time bound.

## Closest approximation literature

Cao's 2007 anisotropic interpolation paper already derives ellipsoidal measures
from derivative polynomials, identifies metrics minimizing interpolation-error
bounds in several norms, and develops a dimensional reduction approximation.
Thus derivative-based optimal metrics, ellipsoid optimization, and reduction
of the computation's dimension are established ideas. Its objective is mesh
interpolation error; it does not compare integer coordinates against arbitrary
convex lifted representations.
[Cao, SIAM Journal on Numerical Analysis 45, 2368–2391](https://epubs.siam.org/doi/10.1137/060667992).

Multi-output mesh adaptation also predates this work. Frey and Alauzet combine
several error metrics through metric intersection in their CFD mesh-adaptation
framework. The earlier
[weighted-precision source audit](quadratic-weighted-precision-algorithm-novelty.md)
records the inspected metric-intersection discussion and distinct tolerances.
[Frey–Alauzet, Anisotropic mesh adaptation for CFD computations (2005)](https://www.ljll.fr/~frey/publications/cmame05-3.pdf).
This is relevant motivation, but rounding a spatial mesh metric does not provide
the present formulation-optimality guarantee.

Naszódi and Venzin study convex covers of norm balls that remain inside a slightly
expanded ball when each covering body is doubled about its centroid. They use
these covers to improve approximate closest-vector algorithms under various
norms. This is a genuine precedent connecting norm geometry, convex covers,
precision, and integer algorithms. Its target is a fixed lattice's closest
vector problem, not choosing the integer dimension of a lifted quadratic graph
formulation.
[Covering Convex Bodies and the Closest Vector Problem, DCG 67 (2022), 1191–1210](https://link.springer.com/article/10.1007/s00454-022-00392-x).

Compact quadratic MILP approximation itself is also established; Beach and
coauthors construct logarithmic-size scalar quadratic formulations.
[Compact mixed-integer programming relaxations in quadratic optimization](https://arxiv.org/abs/2011.08823).
The current claim adds a general error-body model and a comparison against the
best arbitrary convex lift. No matching conclusion was found in these sources
or in focused searches for norm-dependent quadratic graph approximation and
minimum integer-variable formulations.

## What should carry the novelty claim

The image restriction is an elementary but consequential exact reduction:
imposing `w=a(x)+Tz` retains every graph point and costs no integer coordinates,
even when the original relaxation allowed errors outside `im(T)`. It makes the
rounding dimension `d<=n(n+1)/2`, rather than the output dimension `m`.

The covariance scaling then turns a norm distortion `alpha` into only
`(n/2)log2(alpha)` additional integer coordinates. Combining this with a
polynomial-in-`d` classical rounding factor preserves the existing
`O(n log(n+1))` overhead for arbitrary strongly separable symmetric bodies.
The count bound is independent of `m`; the input length and runtime are not.

This should be presented as a broad extension of the finite covariance
construction, with classical rounding prominently credited. It subsumes the
general `O(n log n)` existence guarantee for the l1 error ball whenever its
strong oracle and radii are provided. A separate l1 argument may still offer
a sharper constant or a more explicit covariance certificate, so it need not
be discarded solely because the broad order of the guarantee follows here.

Priority remains qualified: the search found no prior whole-formulation result,
but neither norm rounding nor dimensional reduction alone is proposed as new.
