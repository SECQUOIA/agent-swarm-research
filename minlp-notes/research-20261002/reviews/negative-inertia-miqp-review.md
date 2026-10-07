# Review of the mixed-integer negative-inertia extension

Date: 2026-10-02. Reviewer: fresh Astra adversarial review.

Verdict: the [mixed-integer theorem](../new-direction/negative-inertia-miqp.md)
is mathematically sound under its stated bounded-domain and global-growth
assumptions. I found no remaining mathematical blocker. This review checks
the mixed-domain extension and its composition with the previously reviewed
continuous auxiliary algorithm. It does not establish publication priority
or implement the general FPT mixed-integer oracle.

## Exact oracle and bit output

I read the primary local [Del Pia source](../../literature/papers/pia2025-convex-quadratic-sets-and-the/fulltext.md),
its [source record](../../literature/papers/pia2025-convex-quadratic-sets-and-the/paper.md),
and pages 18–23 of the local PDF using `pdftotext -layout` because the
Markdown extraction omits displayed formulas.

Theorem 3 on page 13 defines accurate solution to include an exact minimum
and an attaining point, and asserts FPT time in the number of integer
variables. Proposition 4 on pages 18–20 returns a mixed-feasible point or
certifies emptiness. Its recursion reduces the integer dimension, preserves
mixed points under rational affine maps, and uses exact continuous convex
QP at its leaves. Theorems 1 and 2 handle lower-dimensional sets; no bound
on the continuous dimension is required. Pages 22–23 bound objective
magnitudes and denominators and use binary search. After isolating the
exact optimum, one more Proposition 4 call at that value explicitly
recovers an attaining point. This supports the required exact value-and-point
oracle, not merely an approximate or decision oracle.

For each rational auxiliary query, the residual Hessian is PSD, the mixed
feasible domain is fixed, and the integer dimension does not increase.
Its data length is polynomial in the original input and query length.
Multiplying the outer call bound by this FPT oracle cost keeps an absolute
polynomial exponent.

FPT runtime by itself gives an FPT output-length bound, not automatically
a polynomial bound independent of the parameter. The draft correctly
supplies the stronger bound separately: boundedness bounds the encoding
length of the returned integer tuple; fixing that tuple and solving the
continuous convex QP produces a uniformly polynomial-height attaining
witness. This step preserves the exact mixed optimum. Constant objective
calls also supply the initial mixed-feasibility check.

Continuous KKT multipliers certify only the fixed-tuple continuous solve.
They cannot certify that another integer tuple has no better objective.
The note correctly relies on the exact mixed-integer algorithm for its
global lower bounds, permitting an FPT computation trace or rerun without
asserting a polynomial-size global KKT certificate.

## Geometry, heights, and stopping

The square-completion identity requires neither convexity nor connectedness
of the feasible domain. The auxiliary function minus its common quadratic
term is an infimum of affine functions, even when the minimizing integer
tuple changes. Thus its upper coordinate curvature remains valid at branch
switches. Both growth-transfer constants follow from inequalities holding
at every mixed-feasible point. They require no continuous interpolation
between mixed points.

Continuous LP coordinate bounds may overestimate the mixed image, which is
harmless: all auxiliary optima remain in the initial box and every query
has the same nonempty compact mixed domain. The constant-image case is
also valid. Corner rounding, pruning with original mixed-feasible witnesses,
and packing depend only on the auxiliary curvature and global growth.
They never count or enumerate the integer tuples. The matrix-only rational
spectral normalization is unaffected by integrality.

For rational heights, every feasible integer coordinate lies between
continuous LP extrema of the bounded polytope. Their polynomial encoding
bounds therefore hold uniformly over all tuples. Fixing an optimal tuple
produces a compact rational continuous slice with polynomial-length data.
Choose a global optimizer in a face of minimum dimension. In its relative
interior the tangent gradient vanishes and the tangent Hessian is PSD by
local optimality, even though the original quadratic can be indefinite.
A nonzero tangent null direction would keep the quadratic constant until
it reached a smaller face, contradicting this choice. Consequently the
tangent Hessian is positive definite unless the face is a vertex. The
independent active equalities and the fixed integer coordinates then give
a nonsingular rational KKT system. Uniform determinant bounds give one
short rational global optimizer and the short optimum value. The proof
does not find or enumerate that tuple or face.

For the projected version, only one short optimizer is needed: since all
global optimizers have the same image, its rational image is the unique
auxiliary optimum. No claim that every original optimizer is rational is
needed or appropriate. This gives the denominator bounds for exact value
and image reconstruction.

The unknown growth constant controls the number of refinement levels,
but is not used as an acceptance test. A prematurely reconstructed image
is harmless because acceptance requires an exact mixed-feasible witness
whose original objective equals the already isolated optimum. At the true
image, every exact inner optimizer passes. Keeping the best auxiliary value
separate from the best original objective is necessary and retained.

## Targeted rational check

I ran one inline `python - <<'PY'` check using `fractions.Fraction` on

\[
 z\in\{0,1\},\quad 0\le y\le1,\qquad
 F(z,y)=(z-y)^2-\tfrac12y^2-\tfrac13y+\tfrac56z.
\]

With \(T(z,y)=y\) and \(\alpha=1\), the residual Hessian is PSD
of rank one, while the original Hessian has one negative eigenvalue.
The optimum is \((z,y)=(0,1/3)\), with \(F^*=-1/18\).
Projected growth holds with \(g_T=1/8\), giving \(g_W=1/10\).
One can append \(w=2y\) and \(0\le u\le1\), leaving the objective
unchanged, to obtain a lower-dimensional polytope with a continuum of
original optimizers and the same unique optimal image. These extra
coordinates require no change to the exact oracle calculation.

For each integer tuple the exact inner optimizer is

\[
 y_z(a)=\operatorname{clip}_{[0,1]}(z+a/2+1/6).
\]

Taking the smaller of the two exact inner values supplies an independent
closed-form mixed oracle for this fixture. For \(a\in[0,1]\), its two
branches are

\[
 W_0(a)=a^2/4-a/6-1/36,\qquad W_1(a)=(a-1)^2/2.
\]

They switch at \((5-\sqrt6)/3\), so this test includes
nonsmooth recourse. At \(a=1\), the mixed oracle returns \(W(1)=0\).
The continuous-relaxation point \((z,y)=(1/4,1)\) instead has augmented
value \(-1/16<F^*\). Substituting the continuous relaxation for the
mixed oracle would therefore break the argument, and the check explicitly
rejects that substitution.

The script passed 242 sampled original-growth inequalities, 399 sampled
cell-rounding and lifted-growth inequalities, and 12 retained-cell checks.
The exact dyadic auxiliary search made 11 distinct corner evaluations,
rejected two premature bounded-denominator image reconstructions, and
recovered the exact image \(1/3\) at level four. It checked the certified
gap and the original mixed-feasible acceptance rule at each level.

These are exact-arithmetic checks of one adversarial fixture; the sampled
inequalities are not a substitute for the general proof above. The fixture
enumerates its two integer values only to provide an independent diagnostic
oracle. The claimed general algorithm uses Del Pia's FPT oracle and does
not enumerate integer intervals. The checker does not implement that
algorithm, rational spectral preprocessing, or universal denominator-bound
construction.

A separate inline Python link check confirmed that all three relative
links in this review resolve to existing local files.

No project-wide verification, CI status inspection, external search, or
literature ingestion was performed. A broken relative source link in the
initial mixed draft was reported for correction; it did not affect the
mathematical verdict.
