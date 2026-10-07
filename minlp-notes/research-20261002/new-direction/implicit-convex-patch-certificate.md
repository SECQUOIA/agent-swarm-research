# Exact implicit polynomial optimization by a certified convex patch

Date: 2026-10-02. Status: complete derivation with a
[fresh actual-file review](../reviews/implicit-convex-patch-review.md)
and targeted exact diagnostics. No priority claim is made.

A sparse polynomial optimizer need not have a short expanded algebraic
representation. Nevertheless, a finite rational certificate can identify
it as the unique solution of a strongly convex box problem of
`f(p,kappa) poly(I)` encoding length, polynomial in the input at fixed
parameters. The box may touch original bounds; neither the exact
active set nor signs of gradients over an isolating rectangle need be
resolved. The output admits certified approximation to any requested
precision within the same parameterized complexity bound.

The result requires a quantitative positive lower bound on the full
continuous Hessian at the optimizer, comparable to point growth. That
condition is automatic when all continuous optimizer coordinates are
interior. At boundary optima it is an additional assumption. Merely
positive definiteness without a quantitative comparison is insufficient
for the stated bound; Section 7 explains why.

## 1. Input, parameters, and exact output

Let `X` be a bounded rational mixed box with continuous coordinates
`C` and native integer coordinates `Z`. Round integer endpoints inward,
reject empty domains, and substitute fixed coordinates. The objective is
an explicit sum of rational polynomial factors of fixed total degree
`d_0`; each factor scope is in a bag of a supplied tree decomposition
with `N` bags of size at most `p`. Let `I` be the total input length,
including a rational `L>0` and its verifiable curvature bounds

\[
         \partial_{ii}F(x)\le L
           \quad\text{on the full continuous box hull of }X.
 \tag{1}
\]

As in the [polynomial grid extension](polynomial-pruned-grid-extension.md),
coefficientwise interval bounds at fixed degree are one admissible
polynomial-size certificate for (1). Complexity uses the bound actually
verified; there is no untrusted curvature oracle.

If preprocessing leaves no variable, return the unique feasible point
and its rational value immediately. Otherwise `n>=1`, and the largest
remaining side width `s` used below is positive.

Assume a unique global optimizer `a` and a positive number `g` for which

\[
 F(x)-F(a)\ge g\|x-a\|^2\quad(x\in X),\qquad
             \nabla^2_{CC}F(a)\succeq gI.                       \tag{2}
\]

Neither `a` nor `g` is supplied. Put `kappa=max(1,L/g)`. The second
condition is vacuous for a pure integer problem. If `a_C` lies in the
relative interior of its original continuous box, the first condition
implies the stronger `H_CC(a)>=2gI` by taking two-sided directional
limits with integer coordinates fixed. For a boundary optimum, the
second condition in (2) must be included in the scope of the runtime
guarantee.

**Theorem.** There is a deterministic algorithm with construction and
verification cost `f_{d_0}(p,kappa) poly(I)` that outputs:

1. The exact integer assignment `a_Z`.
2. A rational continuous box `B` and the polynomial restricted to
   `x_Z=a_Z`.
3. A rational `tau>0`, a certificate that the restricted Hessian is
   at least `tau I` throughout `B`, and the complete pruning records
   proving that every original global optimizer lies in
   `{a_Z} times B`.

The unique constrained minimizer of this certified strongly convex
subproblem is the **exact implicit optimizer output**. The optimum
value is represented by evaluating the original polynomial at that
implicit point. Expanded algebraic coordinates, minimal polynomials,
and an expanded exact value are not output.

For any requested `q`, this representation produces a rational feasible
point within Euclidean distance `2^{-q}` of the optimizer, together
with certified objective bounds of width at most `2^{-q}`, in
`f_{d_0}(p,kappa) poly(I+q)` bit work. Section 6 gives an explicit
interpretation as a unique polynomial KKT system and proves this
evaluation guarantee. Acceptance is sound without (2); those conditions
ensure termination and the parameterized bound.

## 2. Verified global containment from polynomial grid pruning

Use the construction and exact rational evaluation from the
[polynomial pruned-grid theorem](polynomial-pruned-grid-extension.md).
At stage `j`, its base mesh is `h_j=s 2^{-j}`, where `s>0` is the
largest original side width. It computes corrected grid minima and
coordinate min-marginals, updates a feasible upper bound `U_j`, and
retains coordinate hulls of intervals whose endpoint min-marginal
minimum is at most `U_j`.

Every global optimizer survives every stage, independently of any
growth assumption. The verifier checks the full rational Bellman
tables and each removal decision. It then uses the coordinatewise
interpolation lemma, whose soundness follows from (1). These records
are a certificate about the original domain, not just the final box.

For a trial with `theta^2<=1/(8kappa)`, the analysis gives the following
post-stage bounds around the corrected-grid point `y_j`:

\[
 \begin{array}{ll}
 |x_i-(y_j)_i|\le5\sqrt{n\kappa}\,h_j,&i\in C,\\
 |x_i-(y_j)_i|\le1+5\sqrt{n\kappa}\,h_j,&i\in Z,
 \end{array}                                                    \tag{3}
\]

for every point in the retained hull. Each grid coordinate has at most
`100 theta^{-1} ceil(log_2(n+2))` labels under the same condition.
These bounds depend on global point growth, but the recorded pruning
decisions do not trust that condition.

For this theorem, run the requested refinement stages even if an early
objective-gap test succeeds. A small objective gap need not make the
retained box small or convex. Stop only when the exact patch checks
below succeed.

## 3. A necessary additional integer-label filter

Ordinary interval retention alone does not make an integer hull a
singleton: a unit interval touching a good label can survive forever.
Add the following sound rule. Whenever the current integer grids list
**every** feasible integer label in their current intervals, retain only
labels whose exact min-marginal is at most `U_j`, and take their hulls.

To see soundness, fix an integer coordinate at one listed label `v`.
Its unary rounding correction is zero because all its intervals are
unit intervals. Round the other coordinates as in the interpolation
proof. The min-marginal at `v` is a lower bound for every objective
value with that coordinate fixed. Thus a label with min-marginal above
`U_j` cannot occur in a global optimizer. The corrected-grid point
also survives, since each of its coordinate min-marginals is at most
the root lower bound, which is at most `F(a)<=U_j`.

The rule eventually fixes all integer coordinates. In an admissible
trial, the witness estimate for a retained min-marginal gives

\[
        \|z-a\|^2\le\frac{22}{15}\kappa n h_j^2.                \tag{4}
\]

If

\[
                       h_j\le\frac1{10\sqrt{n\kappa}},          \tag{5}
\]

then the right side of (4) is less than one. Every retained integer
label must therefore equal its optimizer coordinate.

At this same stage, all integer labels really are listed. The preceding
hull bound gives a maximum outward distance
`R<=1+10sqrt(nkappa)h_j<=2` from the current integer center.
Since `theta<=1/4` and `h_j<=1/10`, every integer step
`max(1,floor(h_j+theta t))` is one. Stage zero also lists all labels
if (5) already holds: the whole original width is then below one,
so no nonfixed integer coordinate exists. Thus (5) suffices for
both applicability and singleton conclusion of the new rule.

This argument uses native integer spacing one. General rational
lattices can be treated with spacing-dependent thresholds, but no
unmentioned rescaling is part of this theorem.

## 4. A rational certificate of uniform convexity

Compute a rational number

\[
 T\ge\max\left\{1,
   \max_{i\in C}\sum_{j,k\in C}
         \sup_{x\in\operatorname{hull}(X)}
                              |\partial_{ijk}F(x)|\right\}.
 \tag{6}
\]

Explicit fixed-degree monomials and rational box bounds give such a
number in polynomial work with polynomial bit length. It is harmless
to sum bounds over all third derivatives instead of taking the row
maximum. No numerical dependence on `T` will enter a grid state count.
If there are no continuous coordinates, set `T=1`; no Hessian test
will be needed after the integer labels are fixed.

Once the integer-label filter leaves one assignment, restrict to it.
Let `B` be the current continuous hull, let `c` be its rational midpoint,
and put `r=max_i width(B_i)/2`. Remove any now-fixed continuous
coordinates; if none remain, the retained point is an exact rational
optimizer already.

For any `x` in `B`, the mean-value bound and the maximum-row-sum bound
for symmetric matrices imply

\[
 \|H_{CC}(x)-H_{CC}(c)\|_2\le T\|x-c\|_\infty\le Tr.          \tag{7}
\]

For a positive rational trial threshold `tau`, check by exact rational
linear algebra that

\[
                   H_{CC}(c)-(Tr+\tau)I\succ0.                  \tag{8}
\]

A rational LDL factorization with positive diagonal is a polynomial-size
certificate of this strict positive definiteness; no square-root
encoding is needed. Equation (7) proves `H_CC(x)>=tau I` throughout
`B`. This supplies a strongly convex subproblem, even if `B` touches
original lower or upper bounds. No gradient signs at its implicit
optimizer are required.

Since every original global optimizer lies in the retained mixed box,
the minimum of the strongly convex subproblem is the original global
minimum. Strong convexity makes its constrained minimizer unique.
These conclusions follow from verified containment and (8), without
trusting the conditions in (2).

## 5. Unknown conditioning and a finite stage budget

For `mu=2,3,...`, restart the grid procedure on the original domain
with

\[
 K_\mu=2^{2\mu},\quad\theta=2^{-\mu},\quad
                    \tau_\mu=L/(4K_\mu).                       \tag{9}
\]

Abort a trial during grid generation if it would exceed the usual
coordinate cap `100 theta^{-1} ceil(log_2(n+2))`; never allocate
larger tables first. Apply the extra integer-label filter whenever
its stated finite-label condition holds. After each stage, try the
patch check with `tau=tau_mu` if the integer coordinates are fixed.

Run through the smallest stage `J_mu` satisfying both

\[
 h_j\le\frac1{10\sqrt{nK_\mu}},\qquad
 5\sqrt{nK_\mu}\,h_j\le\frac{L}{4TK_\mu}.                      \tag{10}
\]

Squaring these positive inequalities computes the stage budget by
rational comparisons against powers of four. If there are no integer
coordinates, the first condition can be omitted. Their logarithms show
`J_mu=poly(I)+O(mu)`; the magnitude of `T` appears only through its
polynomial encoding length. Unsuccessful trials simply restart with
the next `mu`; every completed certificate test remains sound.

Let `mu_*` be the first trial with `K_mu>=8kappa`. Then
`K_mu<=32kappa`, including the initial-trial case. The grid cap holds
and (3)--(5) fix all integer coordinates by the stage budget. The
continuous radius satisfies

\[
 r\le5\sqrt{n\kappa}\,h_j\le L/(4TK_\mu)\le g/(4T).           \tag{11}
\]

Because `a_C` belongs to `B`, (2) and (7) imply
`H_CC(c)>=(g-Tr)I`. Moreover `tau_mu<=g/4`. Therefore

\[
 H_{CC}(c)-(Tr+\tau_\mu)I
       \succeq(g-2Tr-\tau_\mu)I\succeq(g/4)I,
 \tag{12}
\]

so (8) succeeds. The algorithm stops no later than this trial.

The successful output consequently satisfies

\[
            \tau\ge L/(128\kappa),\qquad
                         2L/\tau\le256\kappa.                  \tag{13}
\]

This bound is useful for evaluating the implicit output. Choosing a
stage-dependent threshold that decreases far below the actual local
curvature would not by itself give the same evaluation bound.

The polynomial grid bit analysis bounds every table and message by
`poly(I+j+mu K_grid)` bits at fixed degree. Additions do not multiply
denominators across bags. The stage budget is polynomial in `I,mu`,
and coordinate state counts are
`O(2^mu log(n+2))`. Summing the capped trial costs through `mu_*`,
then absorbing the `p`th power of `log n` as in the grid theorem,
gives `f_{d_0}(p,kappa) poly(I)`. Rational derivative evaluation,
third-derivative bounds, and LDL certificates add polynomial work.

The final proof object needs only the successful trial's complete
pruning records, its integer-label removals, and its convexity
certificate. Aborted trials need not be part of the output.

## 6. What the implicit output means computationally

This representation is more specific than an instruction to solve the
original nonconvex problem. It describes a unique solution of a
certified strongly convex problem, with global optimality established
by the independent containment records.

For an explicit fixed-degree semialgebraic representation, write the
remaining nondegenerate continuous intervals as `[ell_i,u_i]`, and
introduce nonnegative multipliers `lambda_i,mu_i`. The system is

\[
 \begin{split}
 \nabla F_B(x)-\lambda+\mu&=0,\\
 \lambda_i(x_i-\ell_i)&=0,\qquad
 \mu_i(u_i-x_i)=0,\\
 \ell_i\le x_i\le u_i,\quad\lambda_i,\mu_i&\ge0.
 \end{split}                                                    \tag{14}
\]

Its degrees remain bounded by the fixed input degree and two. Its
number of monomials is polynomial in the explicit input size, while
the total coefficient encoding length is `f(p,kappa) poly(I)` because
it includes the retained grid endpoints. The certified Hessian bound makes
the primal solution unique. Since each interval is nondegenerate,
the multipliers are then uniquely determined as well: at most one
bound is active in each coordinate, and stationarity gives its
multiplier. Thus (14), together with the verified patch, is an exact
implicit definition rather than an expanded minimal polynomial.

There is also a certified approximation procedure. Strong convexity
and constrained first-order optimality give

\[
              F_B(x)-F_B(a_C)\ge(\tau/2)\|x-a_C\|^2.           \tag{15}
\]

Run the fixed-degree polynomial approximation algorithm on `B` with
its same factor scopes and curvature upper bound `L`. Its conditioning
is at most `2L/tau<=256kappa`. To obtain both position error at most
`2^{-q}` and an objective interval of width at most `2^{-q}`, request
gap

\[
           \varepsilon\le\min\{2^{-q},(\tau/2)2^{-2q}\}.        \tag{16}
\]

The bit length of this tolerance is `poly(I)+O(log kappa+q)`, since
`tau=L/(4K_mu)` at the successful trial. Equation (15) gives the
position guarantee and the grid lower/upper bounds give the value
guarantee. The restricted instance has `f(p,kappa) poly(I)` bits;
substituting that length into the approximation bound only changes
the parameter-dependent prefactor and the absolute input exponent.
This proves the claimed evaluation cost without an exact
algebraic-number oracle or an untrusted local nonlinear solver.

## 7. Scope and precision limitations

The [algebraic-output example](../geometric-dp/algebraic-output.md)
shows why expanded minimal polynomials are the wrong output contract
for a general polynomial extension. The
[interval-precision obstruction](implicit-optimum-precision-obstruction.md)
goes further: even with uniform global strong convexity, rectangular
enclosures that certify a particular active gradient uniformly can
require exponentially long rational endpoints. The present theorem
does not perform that sign-enclosure step. A retained box can touch
original bounds, and constrained convex minimization handles the
active-set choice implicitly.

The quantitative full-continuous-Hessian condition in (2) remains
material. Using the residual chain `F` and optimizer `a` from the
precision note, add a continuous variable `y in [0,1/2]` and define

\[
                       G(x,y)=F(x)+y+x_ny^2.                   \tag{17}
\]

Its unique optimizer is `(a,0)`. Since `y>=y^2` and `x_n>=0`, the
same fixed growth `9/16` is valid, and the coordinate curvature
bound remains `35/16`. At the optimizer, however, its full Hessian
is block diagonal with terminal entry `2a_n`, which is doubly
exponentially small while positive. Any ordinary-binary rational
positive full-Hessian lower bound is at most `2a_n` and requires
exponentially many denominator bits.

This is only a limit of retaining all those coordinates in a uniformly
strongly convex patch. Here `partial_y G=1+2x_n y>=1` proves globally
that `y=0`, after which the well-conditioned continuous block remains.
The example neither precludes active-bound elimination nor proves
hardness for every implicit certificate. Known active faces with valid
global elimination certificates can be substituted before applying
the theorem, but discovering such certificates is not assumed here.

The main positive result is exact implicit output under a quantitative
local-convexity condition, with the same width/growth parameter and
arbitrary-precision evaluation. It is not a general exact polynomial
output theorem for all boundary optima or all point-growth instances.

## 8. Review and targeted verification

The [fresh independent review](../reviews/implicit-convex-patch-review.md)
found no substantive gap after clarifying that the implicit output has
parameterized size `f(p,kappa) poly(I)`, rather than an unconditional
`poly(I)` bound. It checks integer-label filtering and timing, the
uniform Hessian certificate, the unknown-conditioning trial budget,
KKT uniqueness, and the conditioning of arbitrary-precision evaluation.
The coordinating researcher separately checked the full derivation.

The reviewer wrote and ran

```
python3 -B research-20261002/reviews/check_implicit_convex_patch_review.py
```

Its three rational closed-box patches, in dimensions 5, 10, and 18,
pass exact midpoint-Hessian and variation tests with `tau=1/2`.
Each patch nevertheless contains a point where the terminal active
gradient is negative, so it cannot support the rectangular sign
certificate excluded by the precision note. The endpoint denominators
have at most 12 bits; the diagnostic never expands the tiny terminal
optimizer coordinates. A separate mixed fixture confirms that ordinary
interval retention leaves an integer unit-interval halo, while the new
individual-label min-marginal filter fixes the correct integer value.

The diagnostic checks those distinct finite claims; it does not
implement the full polynomial pruning algorithm. Scoped whitespace,
mathematical-delimiter, equation-number, and local-link checks passed.
No project-wide verification or CI inspection was performed.
