# Stage 5, round 1: independent review 4

Date: 2026-09-22. I read Section 7, both new scripts, figure/README, author and
literature records, source snapshot, bibliography additions, and coverage.
I did not read another current review, coordinate findings, alter manuscript
files, or rerun formal verification.

## Verdict

Accept stage 5. No valid major or minor issue identified. In particular the
stronger finite-grid lower constant, the N=2 upper bound, the rational mesh
encoding bound, and the objective-specific separation argument are correct.
The figure and finite-check claims match their actual scope.

## Lower bound

The Gram witnesses are realizable in two dimensions: both diagonal entries
are at least 4/5 and the determinant is bounded below by 12/25. The same
witnesses embed in every replication dimension under consideration.

A nonstrict cut excludes a witness only when its aggregate value is strictly
positive. This gives the strict exclusion inequality used in the proof.
Zero coordinate multipliers cannot exclude any witness. For two positive
diagonal weights, replacing the third weight by its good-cone upper bound
correctly yields `t/tau + tau/t < 2*(1+10*eta)`, including interior multipliers
and multipliers with zero third coordinate.

Adding two exclusions and applying AM--GM gives
`(tau-sigma)^2 < 4*tau*sigma*(a^2-1)`. The bound `tau*sigma<=4` and
`eta=1/(400*N^2)` yield exactly
`16*(a^2-1)=4/(5*N^2)+1/(100*N^4)<1/N^2`, including N=1.
Thus the N+1 grid requires more exclusions than N cuts can provide. Equality
with a cut is correctly treated as retention in its closed sublevel set.

The witnessing omitted boundary multiplier has operator norm
`tau+1/tau<=5/2`, giving gradient norm at most `5*sqrt(2)` on the entire convex
product of unit balls. The witness and every point of D_r lie there, so the
mean-value inequality applies along their joining segment. Violation `2*eta`
gives distance at least `2*eta/(5*sqrt(2))=sqrt(2)/(2000*N^2)`.
Unbounded relaxations cause no exception, and no attainment of the infimum
over families is required. This proof covers rescaling and arbitrary interior
good multipliers, rather than merely sampled extreme rays.

## Upper bound and encoding

Endpoint cuts bound both vector norms. The absolute row-sum bound 5/2 for the
slack matrix gives the second-derivative bound 10. At an interior global
minimizer the first derivative vanishes, and a mesh point is at most half a
maximum gap away. Taylor's upper estimate at that mesh point proves the
claimed all-angle lower bound `-5*Delta^2/4`. This argument remains valid
when N=2 and the endpoints are the only sampled angles.

The radial identity has the right sign and mixes with a matrix bounded below
by I/2. Taking `s=(1+2*a)^(-1/2)` corrects all nonnegative-direction defects;
the proof never incorrectly requires the slack matrix to be PSD. Its distance
bound and the elementary convex tangent inequality give the displayed upper
constant. The explicit epsilon cut count handles integer rounding without
assuming existence of an optimal family.

The integer lists have exactly one shared central multiplier, giving 2m+1
distinct rays. Their angles cover both halves of the quadrant, with gaps at
most 1/m by the arctangent Lipschitz bound. Their rank-one multiplier identity
is exact. The stated binary digit bound is conservative but valid, including
zero; the paper correctly distinguishes entry encoding from full formulation
size or numerical accuracy.

## Objective statements

The support-function identity is justified by nearest-point projection onto
the compact convex hull. Bounded P_F is itself compact, since it is a finite
intersection of closed sublevels, and contains D_r. The projection's normal
supports D_r, yielding the reverse inequality with the correct supremum.

For one-objective exactness, every good aggregation is convex, making the
vector-valued map order-convex for the dual cone. This correctly proves
convexity of the augmented epigraph E. It has nonempty interior because the
dual cone contains the positive orthant. The point `(0,v)` lies on its
boundary; supporting the closure is valid despite possible nonclosedness of E.
The recession directions force the multiplier into the original closed good
cone and the objective multiplier to be nonnegative. Strict negativity of
every nonzero good aggregate at the origin rules out a zero objective
multiplier. After normalization, the inequality and complementary evaluation
at the hull minimizer establish common attainment on a single aggregate
sublevel set. The nonzero objective excludes the zero aggregate. No hidden
boundedness requirement on that single-cut relaxation is needed.

The paper distinguishes this classical duality consequence from uniform
representation complexity and from any cut-selection or solver iteration cost.

## Figure, literature, and checks

I viewed the PNG figure and inspected its code. Its exact radial expression is
the smaller root of `a*rho^4-rho^2+3/4=0`, rationalized correctly even on the
axes. The sampled cut radial bounds have the correct numerator `1-sin*cos`.
The N=3/5/9 curves are nested outer approximations, their styles and legend
agree, and the enlarged panel shows the indicated first-quadrant region.
The caption does not mistake this planar illustration for a full-dimensional
Hausdorff computation.

The exact script verifies finite rational meshes, Gram identities, constants,
and radial examples. Its exclusions correctly state that these checks do not
prove the universal pigeonhole, separation, or Hausdorff results. The stronger
manuscript constant is not silently attributed to the deferred formal package.

The added literature comparisons avoid claiming a new approximation exponent
or duality principle. I independently opened
[Rote's author-hosted record](https://page.mi.fu-berlin.de/rote/Papers/abstract/The%2Bconvergence%2Brate%2Bof%2Bthe%2BSandwich%2Balgorithm%2Bfor%2Bapproximating%2Bconvex%2Bfunctions.html),
which supports the tangent/chord and optimal quadratic-rate context. The
paper's positive contribution is carefully restricted to its prescribed good
quadratic family, with dimension-uniform constants and interior-cut lower bounds.

## Targeted commands actually run

Source/provenance reads used `cat`, `tail`, `rg --files`, and targeted `rg -n`.
A search under `/tmp/quadratic-paper-literature` found no Rote/Boyd/approximation
filename; it made no source-verification claim. The Rote record was opened
directly as described above.

From `paper-quadratic-aggregation/`:

```sh
python3 supplement/check_approximation.py
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=/tmp/quadratic-stage05-review4 main.tex
rg -n 'Warning|Overfull|Underfull|undefined' /tmp/quadratic-stage05-review4/main.log /tmp/quadratic-stage05-review4/main.blg
```

The exact script passed 64 meshes and 606 Gram witnesses plus radial checks.
The independent build passed and produced 30 pages; final TeX/BibTeX log scans
found no matches. I additionally loaded the plotting script with `python3 -B`
and `runpy.run_path` without invoking its file-writing main function, then
checked its exact-boundary residual, outer containment, and active sampled-cut
residual on 8,001 directions for N=2,3,5,9. All checks passed at the stated
floating-point tolerances, with no figure files written.

No project-wide tests, CI inspection, formal rerun, or subagent was used.
