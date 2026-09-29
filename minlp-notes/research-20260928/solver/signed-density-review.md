# Adversarial review of exact separator consistency

Date: 2026-09-28.

Reviewed [sparse-putinar-exact-consistency.md](sparse-putinar-exact-consistency.md)
and the kernel interface and moment assumptions in
[sparse-putinar-kernel.md](sparse-putinar-kernel.md). No substantive
mathematical defect was found in the exact-consistency theorem as stated.
This is an independent proof audit, not a novelty assessment or a formal
verification. The established univariate kernel approximation estimate is
an input to the review; its entire literature derivation was not repeated.

## Degree and positivity audit

For a residual subset of size `j` in a bag of size `v`, set
`G=prod_(i notin J) Q_i` and `H=prod_(i in J) r_i`. Each polynomial
`delta^2-r_i^2` has an interval quadratic-module certificate whose terms
have degree at most `2D`. In the telescoping product identity its term
after multiplication by `G` and the earlier residual squares has degree
at most

\[
 (v-j)D+2D+2(i-1)D\le(v+j)D\le2wD\le2R.
\]

The other factors are SOS, so this multiplication introduces no products
of interval generators. Thus the upper bound
`L(GH^2)<=delta^(2j)L(G)` is justified by precisely the ordinary module
in the stated hierarchy.

Writing `G=sum_l q_l^2`, each `q_l H` has degree at most
`(v+j)D/2<=R`. This proves `L(GH^2)>=0` and makes the weighted
Cauchy--Schwarz inequality legitimate. More explicitly, the quadratic
form `L(G(a+bH)^2)` is nonnegative for every real `a,b`; its two-by-two
matrix is PSD, which gives

\[
 |L(GH)|^2\le L(G)L(GH^2).
\]

This argument includes the case `L(G)=0`; division by `L(G)` is neither
needed nor permissible without handling that case.

The coefficient bound on `G` uses source degree at most
`(v-j)D<=R`, so the companion bound `|L(T_alpha)|<=1` applies to every
coefficient used in the evaluation. The coefficient norm of a product
in separate coordinates is the product of the univariate coefficient
norms. Consequently `0<=L(G)<=B^(v-j)` holds under the stated degree
condition. The nonnegative `j=1` terms need only a single interval
certificate multiplied by SOS polynomials; their degree is at most
`vD`. The discarded negative terms therefore start at `j=2`, as claimed.

## Exact consistency and objective audit

The identity `int Qbar(x,y) dmu(y)=1` is a polynomial identity, not an
identity merely on the interval. Marginalizing a signed bag density
therefore leaves exactly the polynomial obtained from the shared source
moments. The latter has degree at most `|S|D<=R`, safely within the
separator equality constraints through degree `2R`.

Every bag uses the same scalar `Delta_w`. Since the reference measures
are product probability measures, their constant-one densities have
constant-one separator marginals. Thus the affine correction preserves
the separator equalities exactly, including an empty separator. The
corrected bag laws are nonnegative and have mass one. Their zero sets do
not obstruct gluing: conditional laws on a zero-mass separator set can
be chosen arbitrarily. Finite running intersection then gives a global
box-supported law with the corrected bag laws as its marginals.

The signed-objective calculation does not assume that `hbar_b` is
nonnegative. Its rearranged correction term compares the corrected bag
probability law with the reference probability law, and hence is bounded
by `Delta_w osc(f_b)`. This is the correct pair of measures for the
oscillation argument.

The normalized operator fixes constants exactly and has the companion
error bound on every positive Chebyshev mode. The tensor coefficient
estimate follows by expanding the product of the univariate images and
using the submultiplicative coefficient norm. The transformed objective
and the original objective have total degree at most `vD<=R`. Thus their
evaluation under a truncated functional is legitimate. Constants in the
objective create no error. Taking the infimum over feasible moment
points yields the relaxation-gap conclusion even if the infimum is not
attained.

An additional independent agent reviewed only the common correction,
the signed-objective step, and the rate while assuming the preceding
kernel and weighted inequalities. That review found no defect. Agreement
between reviews is supporting evidence, not a replacement for the proof.

## Uniformity and parameter choices

There is no hidden factor in the number of bags or the tree diameter.
The statement is uniform after retaining the explicitly displayed
`C_f=sum_b C_b`, and assuming bounded width and bounded local coordinate
degree. It does not assert that the absolute error or the SDP dimension
is independent of the number of bags. The source degree is
`D=O_w(s log s)`, so a sufficiently small width-dependent constant in
`s` of order `R/log R` satisfies `wD<=R`. This proves the claimed rate
for every sufficiently large order, not just a sequence of orders.

The final parameter choice in the note is

\[
 N=2\left\lceil\max\{3/2,(w+1)/4\}\log_2s\right\rceil.
\]

Put `m=max(3/2,(w+1)/4)`. Then `delta<=1/(2s^3)` and
`delta^2<=1/(4s^(4m))`. The same Taylor bound gives

\[
 \Delta_w=O_w\bigl(s^{w-2-4m}\log^{w-2}s\bigr)
          =O_w(\log^{w-2}s/s^3)
          =o_w(\log s/s^2)
\]

for `w>=2`; for `w=1` it is zero. The middle estimate uses
`4m>=w+1`. This independently verifies the final parameter choice after
its revision during review. The earlier larger choice
`N=2 ceil(max(3/2,w) log_2 s)` was also valid, but is no longer the
displayed choice.

## A concrete obstruction to a tempting invalid proof

Products of interval-nonnegative residuals cannot simply be declared
nonnegative under an ordinary-module pseudomoment functional. This can
fail even with only two variables.

Define an order-two functional by `L(1)=1`, all moments with an odd
coordinate exponent equal to zero, and

\[
 L(x^2)=L(y^2)=L(x^4)=L(y^4)=3/4,\qquad L(x^2y^2)=3/8.
\]

Its moment matrix is PSD: the block on `(1,x^2,y^2)` has Schur
complement
`(3/16) [[1,-1],[-1,1]]`, and the remaining diagonal entries, on
`(x,y,xy)`, are `3/4,3/4,3/8`. Its localizing matrices for `1-x^2`
and `1-y^2`, on `(1,x,y)`, are respectively
`diag(1/4,0,3/8)` and `diag(1/4,3/8,0)`. Nevertheless,

\[
 L((1-x^2)(1-y^2))=-1/8.
\]

This is not a counterexample to the reviewed theorem: these residuals
are a simpler example, and `v=2,D=2,R=2` violates its stronger degree
condition `R>=vD`. It confirms that the proof correctly treats the
multiple-residual terms as potentially negative and does not silently
substitute preordering positivity.

## Targeted verification

Command actually run:

```text
python research-20260928/solver/check_signed_density_review.py
```

Result: six exact residual-product identities; finite degree ledgers;
the common-shift and signed-objective identities; the exact feasible
pseudomoment obstruction above; and 256 finite correction/rate-bound
cases passed. The arithmetic is rational or symbolic after the integer
parameter choice. The script also checks that different individually
valid bag shifts can destroy separator equality.

These finite checks detect algebra and indexing errors and establish
the explicit obstruction exactly. They do not prove all-degree
inequalities, universal SOS representations, the measure-gluing result,
or the full theorem for arbitrary feasible pseudomoments. No
project-wide checks or CI inspection were performed.

The result remains a theorem about unconstrained optimization over a
box. The correction does not preserve extra local constraints,
integrality, or a discrete domain. This review makes no claim about
priority, numerical conditioning, practical hierarchy orders, or a
computational speedup.
