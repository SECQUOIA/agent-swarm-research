# Adversarial review of canonical algebraic witness recovery

Date: 2026-09-27. Status: independent review of the complete
[author's note](algebraic-witness-recovery.md) and its dependencies. No
counterexample or substantive proof gap was found in the canonical
minimum-norm witness result. The review is
conditional on the Hessian-span value/QE argument and exact feasibility
algorithm in the two linked notes below.

## 1. Scope and dependencies examined

The proposed result concerns a nonempty closed convex set defined by rational
convex quadratic inequalities and rational affine constraints. With explicit
rational bounds, or with a proved effective radius replacing them, it seeks
the unique point

\[
 x^*=\operatorname*{argmin}_{x\in S}\|x\|_2^2.
\]

The parameter is the dimension `h` of the span of the native Hessian matrices.
The reviewer read the entire active-system, multiplier-compression, adjugate,
and singleton-elimination argument in
[the Hessian-span note](hessian-span-reduction.md), and the exact decision
algorithm in [the feasibility note](hessian-span-exact-feasibility.md).
The present review does not independently reprove the quantitative
quantifier-elimination theorem or the finite-precision ellipsoid theorem.

The author's note gives the intended output precisely: a tuple of real algebraic numbers,
each given by an integer polynomial and a rational interval isolating its
intended real root, is an exact point representation. A rational approximate
point alone is not an exact witness, and need not be feasible.

## 2. Coordinate degree and height

The existing active-system argument extends to coordinates, with one
important use of uniqueness. Choose the minimum-norm feasible point, delete
inactive rows, make active affine rows equations, and add the affine
differences of dependent active quadratics. The reduced problem retains the
same minimum norm. Its objective is strictly convex, so it has the same
unique minimizer. Rational parametrization `x=x_0+Vu` makes the objective
strictly convex in `u`, because `V` has independent columns.

Relax all retained quadratic rows to `q_i(u)<=epsilon`. A retained feasible
point bounds the objective of every relaxed minimizer from above. Coercivity
therefore bounds the minimizers, even when a numerical bound was not known
beforehand. Every accumulation point is feasible for the limiting reduced
problem and has minimum norm. Uniqueness implies convergence of the whole
family to `x*`. Thus the scalar limit formula can track a coordinate rather
than only an optimal value. The coordinate is an affine rational expression
in the adjugate numerator divided by the determinant, and introduces no
additional quantified variables.

The sparse KKT support can still be fixed along a sequence tending to zero;
the proof does not require a support that works on an entire interval.
Keeping every retained feasibility row in the formula is essential. An
arbitrary solution of the supported stationarity equations alone need not
be a feasible minimizer.

The coordinate formula has the same bounded number of quantifier blocks and
`O(h+1)` quantified variables. Consequently every coordinate has an integer
annihilator of degree and coefficient bit length `N^{O(h+1)}`. This is an
existence argument; the algorithm need not discover the unknown active
system.

An annihilator bound is not literally a minimal-polynomial height bound.
The required passage is elementary. If an integer annihilator `A` has
degree at most `D` and coefficients of magnitude at most `2^B`, the primitive
minimal polynomial `p` divides `A` in `Z[T]`. Its leading coefficient divides
the leading coefficient of `A`, and all its roots have magnitude at most
`1+2^B`. Expanding its factorization gives

\[
 H(p)\le 2^B2^D(1+2^B)^D.
\]

Thus its coefficient bit length is `O(D(B+1))`, still
`N^{O(h+1)}`. This correction was sent to the author.

## 3. Certified approximation through exact decisions

Let `theta=||x*||^2`. Exact feasibility queries with one additional convex
quadratic row `||x||^2<=b` locate a rational upper bound satisfying

\[
 \theta\le b\le\theta+\delta.
\]

The Hessian span rises by at most one. The initial upper bound is supplied
by the input box or the effective radius. Each decision query has polynomial
bit length when the requested accuracy has polynomial logarithmic size.

For every `x` in the nonempty sublevel set
`S_b=S intersect {||x||^2<=b}`, projection optimality gives

\[
 \langle x^*,x-x^*\rangle\ge0,
 \qquad
 \|x-x^*\|^2\le\|x\|^2-\|x^*\|^2\le\delta.
\]

Repeatedly bisecting coordinate intervals and retaining a half-box whose
intersection with `S_b` is feasible leaves a nonempty final box. Its rational
center is close to some point of `S_b`, and hence to `x*`. Closed halves
cover the parent box, so a midpoint on the feasible set causes no difficulty.
No step requires a rational feasible point. Affine box cuts do not increase
the Hessian span.

For example, to obtain Euclidean error below `eta`, use
`delta<=eta^2/16` and final coordinate widths at most
`eta/(2n)` when `n>=1`. The midpoint error is at most `eta/4`, and the
distance from any retained feasible point to `x*` is at most `eta/4`.
The total is below `eta`. The number of oracle calls is polynomial in
`n`, the original bound's bit length, and `log(1/eta)`.

## 4. Recovery theorem and root selection

The original primary source was checked directly: Kannan, A. K. Lenstra,
and Lovasz, *Polynomial Factorization and Nonrandomness of Bits of
Algebraic and Some Transcendental Numbers*, Mathematics of Computation
50 (1988), 235--250, Theorem 1.19 on printed page 241. An openly available
[scan of the original paper](https://www.math.cmu.edu/~af1p/Teaching/AdditiveCombinatorics/LLLL.pdf)
places that page at PDF page 12.

The theorem reconstructs a minimal polynomial deterministically in time
polynomial in degree and logarithmic height from a certified approximation
of sufficiently high polynomial precision. It applies to arbitrary
magnitude, using reciprocals if necessary. Thus the coordinate bounds from
Section 2 and approximations from Section 3 are sufficient. Merely trying
an integer-relation algorithm at an unproved numerical precision would not
justify this conclusion.

The recovered minimal polynomial can have several real roots. The author
uses the integer discriminant and a Cauchy root bound to obtain the
conservative separation `delta=2^{-4D^2(H+2)}`. The reviewer independently
checked it: isolate one squared root difference in the discriminant
product, bound the leading coefficient by `2^H` and every other difference
by `2(1+2^H)`, and use the nonzero integer discriminant's absolute value
of at least one. The stated bound is weaker than the resulting bound and
therefore valid.

An approximation error below `delta/8` and interval half-width `delta/4`
then put the intended root strictly inside the interval and exclude every
other root. Thus the note does not require a separate root-isolation
algorithm or leave an endpoint ambiguity. A polynomial without this
identifying interval would have been insufficient.

## 5. Joint field degree: a valid stronger argument

Polynomial degree for each coordinate alone does not bound the degree of
their joint number field by a polynomial. For example, independently chosen
square roots can generate a field of exponentially growing degree.

The author proposed a stronger argument that survives review. Apply the
coordinate limit formula to `c^T x*` for an arbitrary rational vector `c`.
Its coefficient height can depend on the size of `c`, but its polynomial
degrees, number of polynomials, and quantifier-block sizes do not. The
quantifier-elimination degree bound therefore gives one uniform
`D=N^{O(h+1)}` such that

\[
 [\mathbb Q(c^Tx^*):\mathbb Q]\le D
 \quad\text{for every }c\in\mathbb Q^n.
\]

Since each coordinate is algebraic, the primitive-element theorem supplies
a rational linear combination generating the finite extension
`K=Q(x*_1,...,x*_n)`. Applying the uniform bound to that combination yields
`[K:Q]<=D`. The statement must explicitly separate coefficient-height
dependence from degree dependence; absorbing the encoding of `c` into an
undifferentiated input length would not establish this uniform conclusion.

There is also a bounded search for a primitive element. For
`alpha_k=sum_{j=1}^n k^{j-1}x*_j`, every pair of distinct embeddings of `K`
agrees on `alpha_k` for at most `n-1` values of `k`. Thus one of
`k=0,...,(n-1)D(D-1)/2` separates all embeddings. Recovering all these
minimal polynomials and choosing one of maximum degree identifies a
primitive element; the coefficient bits of these linear combinations are
polynomially bounded. This does not, by itself, give formulas expressing
every coordinate as a rational polynomial in that element. Such an output
format requires an additional field-arithmetic or height argument. The
coordinatewise output format already gives an exact witness.

The reviewer subsequently read the complete saved Section 5 containing
this argument. Its candidate range has one more integer than the upper
bound on bad choices, the linear-form coefficient bits remain polynomial,
and choosing maximum recovered degree does identify a primitive generator.
No gap was found in this additional algorithmic claim.

## 6. Limits of the review

The complete author's note was read after the initial premise review.
Its direct unbounded argument supplies its own radius, so its witness
theorem does not need an additional unbounded-feasibility theorem as a
dependency. The reviewer independently checked the case `h=0`, the
norm-value and coordinate bisection bounds, and the conservative
`N^{O((h+1)^2)}` complexity obtained after feeding enlarged rational
inputs to the boxed decision oracle.

One exposition correction was requested and applied: state explicitly that the
polynomial KKT formula includes nonnegative multipliers and positive
determinant, as well as all primal inequalities and complementarity.
Those conditions were already implicit in its description as a KKT
formula; omitting them from an actual formula would be a gap.

This argument concerns the canonical minimum-norm feasible point. It does
not yet recover a minimizer of an arbitrary, possibly non-strictly convex
objective. Near-optimal objective value alone need not imply proximity to
one selected optimizer.

The independent checks were symbolic proof checks and a primary-source
inspection. No numerical reconstruction was treated as proof of a general
degree or complexity bound. No Lean formalization, ellipsoid implementation,
project-wide verification, or CI inspection was performed.

Targeted document checks: `git diff --check --
research-20260927/algebraic-witness-review.md` returned no output (the file
was untracked, so that command alone did not validate its contents). A
direct Python check of this file's final newline, trailing whitespace,
and control characters passed.
