# Small coefficients for exact root penalties

Date: 2026-09-27. Status: independently reviewed supporting theoretical
consequence. Qualitative exact
fractional penalties and the effective algebraic estimates used below are
prior work. This is not currently a principal originality claim.

## Statement and input convention

Let `X` be a compact native domain described by rational quadratic weak
inequalities, equalities, and finite rational variable bounds, with some
variables required to be integer. Let `f` be a rational quadratic objective.
Additional rational quadratic equations and weak inequalities define a nonempty
feasible subset `S` of `X`. All polynomials are explicitly expanded, and `N`
counts their ordinary binary input length, including the bounds. No convexity
or constraint qualification is assumed.

Define `V(x)` as the maximum of zero, the positive violations of the
additional inequalities, and the absolute violations of their equalities.
Compute rational integers `H,B>=1` with `V<=H` and `|f|<=B` on the input
box by termwise absolute-value bounds. Their bit lengths are polynomial in
`N`. Set `R=V/H`, so `0<=R<=1` on `X` and `S={x in X:R(x)=0}`.

**Theorem.** There is a universal integer-valued polynomial `p` such that

\[
 \min_{x\in X}\{f(x)+(4B+1)R(x)^{2^{-p(N)}}\}
 =\min_{x\in S}f(x),
\]

and the minimizer sets coincide. Both the penalty coefficient and the
rational exponent have polynomial binary length. A depth-`p(N)` quadratic
lift represents the augmented objective with polynomially many bounded
auxiliary variables and polynomial-bit rational coefficients.

The universal constants in `p` have not been evaluated for numerical use.
The claim is a uniform representation bound. It gives no efficient global
optimization algorithm or favorable numerical conditioning.

## Removing discrete quantifiers without enumerating slices

For an integer coordinate with bounds `ell<=z<=u`, first replace the bounds
by their integral ceiling and floor. An empty range is incompatible with
the assumed nonempty feasible set. Write

\[
 z=\ell+\sum_{j=0}^{k-1}2^j b_j,\qquad
 b_j(1-b_j)=0,
\]

retain `ell<=z<=u`, and bound each `b_j` in `[0,1]`. Use enough bits to
cover `u-ell`; when this difference is zero no bits are needed. The input
length bounds the total number of introduced bits polynomially. Keeping
`z` and its affine expansion avoids any unnecessary substitution. The lift
is compact, remains quadratic, and has polynomial coefficient bits. Its
projection is exactly the original mixed-integer set.

For the proof, regard these bits as real variables constrained by their
quadratic equations. Below, `w` denotes all lifted coordinates, and `X'`
and `S'` the lifted native and feasible sets. All functions ignore auxiliary
bits except through the original coordinates.

## A rational description that avoids the unknown optimum

Let `v=min_S f`. Compactness and nonemptiness imply that `v` exists and
belongs to `[-B,B]`. Define the interval

\[
 I=\{t\in[-B,B]:\text{there is no }y\in S'\text{ with }f(y)<t\}.
\]

Thus `I=[-B,v]`. Its displayed description has one quantified real block
over polynomially many variables and rational polynomials of degree two.
The integer bits are already represented by polynomial equations.

Standard coefficient-sensitive elimination of one real quantifier block
gives a quantifier-free description of `I` whose degrees and coefficient
bit lengths are both at most `2^{poly(N)}`. Only this bound, rather than
an implementation or the exponentially long formula, is needed. The
one-block quantitative elimination theorem is restated as Theorem 4.1 in
[Basu--Mohammad-Nezhad](https://doi.org/10.1017/fms.2024.66). Its statement
explicitly bounds output coefficient bits by
`tau d^{O(k)O(ell)}` for one quantified block of size `k` and `ell` free
variables. Here `d=2`, `k=poly(N)`, `ell=1`, and `tau=poly(N)`.

On the compact rationally described semialgebraic set `A=X' times I`, let

\[
 g(w,t)=\max\{0,t-f(w)\},\qquad h(w,t)=R(w).
\]

Their graphs have quantifier-free descriptions using the polynomials above
and quadratic comparisons. Both functions are continuous on `A`. If `h=0`,
then `w` is feasible and `t<=v<=f(w)`, so `g=0`. Also `0<=g<=M=2B`.
This construction includes native integer fibers with no feasible points
and avoids inserting the possibly irrational number `v` as a coefficient.

## Effective inequality and coefficient compression

The integer-coefficient part of Basu--Mohammad-Nezhad Theorem 2.2 gives

\[
 g^q\le C h,\qquad
 q\le2^{a(N)},\qquad \log_2\max\{1,C\}\le2^{a(N)}
 \tag{1}
\]

for a universal polynomial `a`, after increasing it if necessary. Indeed,
the number of variables is polynomial in `N`, and both the description
degree and coefficient bit bound are singly exponential in a polynomial
in `N`. Their bounds
`q=(8d)^{2(n+7)}` and
`log_2 C<=tau d^{O(n^2)}` retain this form. Denominators are cleared row by
row before applying the theorem. Increase `C` to at least one.

Choose `p(N)` large enough that `alpha=2^{-p(N)}` satisfies

\[
 \alpha q\le1,\qquad \alpha\log_2 C\le1.

\]

For positive `h`, use the elementary inequality
`min(a,b)<=a^{1-theta}b^theta`, with `theta=alpha q`, to obtain

\[
 g\le\min\{M,C^{1/q}h^{1/q}\}
 \le M^{1-\alpha q}C^\alpha h^\alpha
 \le2M h^\alpha.
 \tag{2}
\]

The last step uses `M>=1`. The same conclusion holds at `h=0`, since then
`g=0`. Restrict (2) to the allowed point `t=v`. For every native point,

\[
 f(x)+(2M+1)R(x)^\alpha
 \ge v+R(x)^\alpha.
\]

Every infeasible point is strictly worse than `v`; feasible minimizers
attain `v`. This proves the claimed value and minimizer-set equality. The
coefficient is `2M+1=4B+1`, with polynomial binary length.

## Exact quadratic lift

Introduce `t_0,...,t_p in [0,1]`, impose

\[
 t_{j+1}=t_j^2\quad(0\le j<p),\qquad Ht_p\ge V(x),
 \tag{3}
\]

and minimize `f(x)+(4B+1)t_0`. The last condition is represented by one
inequality for each signed equality residual and each inequality residual,
together with `t_p>=0`; a maximum variable is unnecessary. For each `x`,
the smallest feasible `t_0` is exactly `R(x)^{1/2^p}`. Thus (3) is an exact
quadratic lift of the augmented objective. The added equations are
nonconvex. Replacing them by convex epigraph inequalities in the opposite
direction would invalidate the construction.

The exponent denominator `2^p` has `p+1` ordinary binary digits. Both its
explicit rational encoding and the quadratic lift therefore have
polynomial description length. This changes the augmentation; it does not
refute the existing large-coefficient lower bounds for a prescribed norm
penalty.

## Scope, prior art, and limits

The [prior-art audit](holder-penalty-prior.md) identifies compact subanalytic
fractional penalties from Warga and Dedieu in 1992 and the modern explicit
comparison by Jiao--Pham--Tuyen. Effective exponent and coefficient bounds
also predate this note. The possible addition is their uniform encoding
consequence for a specified MINLP input model, including infeasible integer
fibers and a quadratic lift. The compression step itself is elementary.
No substantial originality claim is made on the basis of this bounded search.

An objective-range assumption is essential outside the stated quadratic
input model. The audit's sparse objective `x^(2^k)` on `[1,2]`, with the
additional requirement `x>=2`, forces coefficient at least `2^(2^k)-1`
for the unscaled residual `[2-x]_+`, regardless of the exponent.

Small binary descriptions are compatible with severe numerical difficulty.
For example, the added squaring chain makes the terminal residual tiny when
`t_0<1`. Approximate enforcement of its equations need not preserve the
exactness theorem. There is no guarantee about local minima, practical
penalty calibration, or solver speed.

## Verification status

The [independent review](root-penalty-review.md) checked the complete proof
and the explicit coefficient bound in the primary source. It required
stating weak inequalities and clarifying compactness in the prior-art
comparison; both corrections were made. The root independently reread
Theorem 4.1 and the review's encoding calculations and counterexamples.

The review also proves two useful limits. A native squaring curve with final
coordinate penalized at zero requires exponent at most `2^{-k}` for any
finite coefficient. A two-point native set with a binary improving slice at
residual `2^{-2^k}` needs exactly `rho>2^{alpha 2^k}` for minimizer-set
exactness. These are supporting examples based on familiar squaring chains,
not separate priority claims. The review gives an exact construction where
an absolute feasibility tolerance accepts a spurious zero-penalty lift.

No numerical or Lean verification has been run for this note. The proof
uses the cited general theorems; the review checks their application rather
than formally verifying those theorems. No project-wide checks or CI
inspection were performed.
