# Constant-accuracy convex point output contains Square Root Sum

Date: 2026-10-02. Status: complete proof with a
[fresh independent actual-file review](../reviews/convex-point-radical-review.md).
This is a conditional complexity implication, not an
NP-hardness claim or a proof that polynomial-time point output is
impossible. The [canonical-selector construction](canonical-selector-radical-comparison.md)
is a simpler antecedent; the present result applies to any optimizer.

There is a polynomial-time one-query reduction, with direct preprocessing,
from Square Root Sum to finding a
point within distance `1/4` of any optimizer of a rational convex
quartic on a rational box. The constructed optimizer is unique. The
primal interaction graph has treewidth at most two, all numerical coefficients and
box widths are bounded by absolute constants, and the construction can
be mapped to a unit box. Thus a deterministic polynomial-time point
algorithm on this class would decide Square Root Sum in polynomial time.
An expected polynomial-time algorithm that always returns a correct
point would give the corresponding Las Vegas algorithm.

Objective approximation remains a convex optimization problem. A compact
definition of the optimizer by the original convex program is also
immediate. The implication concerns efficient evaluation of optimizer
coordinates, rather than either of these weaker outputs.
The [focused primary-source comparison](../prior-art/convex-point-radical-prior.md)
credits established strong-approximation and convex-optimization
antecedents without asserting publication priority.

## 1. The two strongly convex comparison problems

The source predicate is

\[
                   \sum_{i=1}^n\sqrt{a_i}\le B,             \tag{1}
\]

where the `a_i` are positive binary integers and `B` is an integer.
Zero radicands, an empty sum, and nonpositive targets are handled
directly. If every radicand is a perfect square, decide (1) by integer
arithmetic. Otherwise the sum is not an integer, as proved below, so
equality in (1) cannot occur.

Use the normalization from the independently reviewed
[active-bound construction](convex-active-set-radical-comparison.md).
Choose powers of two `R_i` with `R_i^2<=a_i<4R_i^2`, put
`c_i=a_i/R_i^2`, `M=max_i R_i`, and `w_i=R_i/M`. Let `K` be the least
power of two at least `max(2,n)`. A complete binary tree with `K` leaves
has real leaf variables `u_i in [1,2]` and signals `w_i u_i`; padded
leaves have fixed signal zero. Each internal variable lies in `[0,2]`
and has residual equal to itself minus half the sum of its child
signals. Write `s` for the root variable and set

\[
 F_0(u,v)=\sum_i(u_i^3/3-c_i u_i)+\sum_j r_j^2,
 \qquad s^0=\frac{\sum_i\sqrt{a_i}}{KM}.                    \tag{2}
\]

The unique minimizer of `F_0` has `u_i=sqrt(c_i)` and every residual
zero, so its root equals `s^0`. The cited construction proves throughout
the box that `H_F0>=I/8`. Its proof uses the averaging matrix `P`, with
`||P||_2<=1/sqrt(2)<3/4`, and
`d'H_F0 d>=2||(I-P)d||^2`.

If `B>=2KM`, predicate (1) is immediately true. In the remaining case
write `b=B/(KM) in [0,2]` and `epsilon=1/32`. Make two independent
copies of the tree variables and introduce `t_+,t_- in [0,1]`:

\[
 \begin{aligned}
 H_+(w_+,t_+)&=F_0(w_+)+t_+^2+\epsilon t_+(b-s_+),\\
 H_-(w_-,t_-)&=F_0(w_-)+t_-^2+\epsilon t_-(s_--b).
 \end{aligned}                                             \tag{3}
\]

Both Hessians are at least `I/16`: appending `t^2` preserves the
`I/8` bound, and either bilinear perturbation has Hessian norm
`epsilon`. Each problem therefore has a unique optimizer. On its
`t=0` face, the unique minimizer is the unperturbed point in (2).
The derivative in `t` there is respectively
`epsilon*(b-s^0)` and `epsilon*(s^0-b)`. Convex box KKT conditions give

\[
 \begin{array}{ll}
 t_+^*=0\ \Longleftrightarrow\ s^0\le b,
 &t_+^*>0\ \Longleftrightarrow\ s^0>b,\\
 t_-^*=0\ \Longleftrightarrow\ s^0\ge b,
 &t_-^*>0\ \Longleftrightarrow\ s^0<b.
 \end{array}                                               \tag{4}
\]

For completeness, a negative derivative on the zero face gives an
improving feasible direction, and no other point on that face can be
optimal. At `t=1`, either derivative is at least
`2-2epsilon>0`; consequently any positive optimal `t` is strictly below
one. Reversing the sign in the second copy therefore causes no
upper-bound exception.

Since equality was removed, exactly one of `t_+^*,t_-^*` is positive.

## 2. A convex quartic forces every optimizer to reveal the sign

Introduce `y in [0,1]`, let `eta=1/192`, and define

\[
 F=H_++H_-+
          \eta\bigl[t_+^2(y-1)^2+t_-^2y^2\bigr].            \tag{5}
\]

This polynomial is jointly convex on its whole box. To check the
claim without dividing by either `t`, for a direction `(p,q)` in
`(t,y)` use the identity

\[
 D^2\bigl[t^2(y-c)^2\bigr][(p,q)]^2
       =2\bigl(tq+2(y-c)p\bigr)^2-6(y-c)^2p^2.              \tag{6}
\]

Apply (6) with `(t,c)=(t_+,1)` and `(t_-,0)`. Since both `|y-c|<=1`,
the two possible losses are at most `6eta*p_+^2` and
`6eta*p_-^2`. They act on different base coordinates. The Hessian of
`H_++H_-` is at least `I/16` on all its variables, so the full quadratic
form is at least

\[
              (1/16-6\eta)\|p_{\mathrm{base}}\|^2
                       =\|p_{\mathrm{base}}\|^2/32\ge0.    \tag{7}
\]

The remaining terms in (6) are nonnegative. This proof covers the
boundary cases `t_+=0` or `t_-=0` as well.

Let `h_+^*,h_-^*` be the two independent optimal values. Equation (5)
is always at least `h_+^*+h_-^*`. If `s^0>b`, set both base copies to
their optimizers and choose `y=1`; (4) makes both added terms zero.
If `s^0<b`, choose `y=0` instead, again making both terms zero. The
lower bound is therefore attained. Every optimizer of (5) must
simultaneously minimize each strongly convex base problem and make
the nonnegative additional terms zero. Hence it is unique, and

\[
 y^*=\begin{cases}
        1,&\sum_i\sqrt{a_i}>B,\\
        0,&\sum_i\sqrt{a_i}<B.
      \end{cases}                                         \tag{8}
\]

A point at Euclidean or maximum-norm distance at most `1/4` from any
optimizer has its `y` coordinate on the same side of `1/2` as (8).
Thus one constant-accuracy point query decides (1). Feasibility of the
reported point is not needed for this implication, although an
optimization algorithm may also guarantee it.

## 3. Equality preprocessing needs no factorization

Let `E=Q(sqrt(a_1),...,sqrt(a_n))`, a finite field extension of `Q`.
If `a_i` is not a perfect square, trace transitivity gives

\[
 \operatorname{Tr}_{E/\mathbb Q}(\sqrt{a_i})
 =[E:\mathbb Q(\sqrt{a_i})]
       \operatorname{Tr}_{\mathbb Q(\sqrt{a_i})/\mathbb Q}
                    (\sqrt{a_i})=0.                       \tag{9}
\]

The trace of an integer is its product with `[E:Q]`. If the positive
radical sum were the integer `B`, applying the trace would force `B`
to equal the sum of the perfect-square terms. Subtracting these terms
from the original equality would make a sum of strictly positive
nonsquare radicals zero, a contradiction. Thus an integer equality
requires every radicand to be a perfect square. The algorithm uses
only polynomial-time integer square-root tests and integer arithmetic;
it does not compute the field, its degree, or squarefree decompositions.

## 4. Size, sparsity, and conditioning qualifications

The two trees and their rational normalization have polynomial encoding
length in the source input. The polynomial has degree four and a linear
number of local factors. All coefficient magnitudes are bounded by an
absolute constant: `c_i<4`, `w_i<=1`, `b<=2`, and `epsilon,eta` are
fixed constants. Original intervals have width at most two. Mapping
each interval affinely to `[0,1]` preserves degree, factor scopes, and
absolute coefficient bounds, because every factor has constant scope
and degree and each affine scale and shift is bounded.
After this change, discard the aggregate constant term: individual
factor constants are bounded, but their sum need not be. Every
nonconstant monomial has only a bounded number of contributing factors
in this construction, so the expanded polynomial with its constant
removed has the claimed absolute coefficient bound as well.

For each tree residual use its variable and its nonconstant child
variables as a bag. The original leaf and tree factors have bags of
size at most three. Attach `{s_+,t_+}` and `{s_-,t_-}` at their roots.
Attach the new bags `{t_+,y}` and `{t_-,y}` to these respective bags,
and join the two new bags. This is a tree decomposition of maximum bag
size three; every variable has connected bag occurrences. Thus the
graph has treewidth at most two.

Upper coordinate curvature is bounded by an absolute constant (`L=5`
on the displayed boxes, or `L=20` after the stated unit-box changes).
Negative curvature is zero. However, the construction does **not**
retain the base problems' uniform point-growth constant. At its optimum
the `y` curvature is

\[
                 2\eta\bigl((t_+^*)^2+(t_-^*)^2\bigr),     \tag{10}
\]

which can be very small. In particular, moving `y` inward by a small
amount while holding the base optimizers fixed gives objective gap
`eta*((t_+^*)^2+(t_-^*)^2)` times squared displacement. No input-polynomial
conditioning bound is asserted. This is consistent with the completed
algorithms that parameterize point growth or assume a quantitative
positive residual modulus.

## 5. Consequence for core-only noise and exact representations

Adjoin an independent core variable `v in [0,1]` with objective

\[
                        (v-1/2)^2+\gamma v,                \tag{11}
\]

where any sampled `gamma in [-1/2,1/2]` is allowed. The core optimizer
is `1/2-gamma/2`, its projected growth is one, and its upper curvature
is two. Every residual fiber is the same convex polynomial problem
(5). There is no residual noise. On every draw, the unique full
optimizer still has the `y` coordinate in (8).

Consequently a general core-only-noise theorem for merely convex
residuals, with expected polynomial initial work and a correct
polynomial-time coordinate-evaluation oracle, would give an expected
polynomial-time algorithm for Square Root Sum even at one fixed,
constant output precision. This remains true with fixed core dimension,
fixed noise scale, fixed core curvature, and constant graph width.
For an always-correct algorithm with expected running time, the induced
decision algorithm is Las Vegas; no deterministic running-time claim
is inferred from that expectation.

This does not rule out compact exact descriptions. The original convex
program is already one. What is at issue is a promised evaluation
algorithm whose work is polynomial in input length plus requested
coordinate bits. Nor does the reduction impede certified objective
approximation: standard convex optimization applies to (5), without
providing distance to its optimizer. No NP-hardness assertion or
unconditional complexity-class separation follows from this reduction.
The [independent significance assessment](convex-point-comparison-assessment.md)
also separates this comparison implication from an unconditional size
bound for explicitly listed coordinate polynomials, including sparse
listings. It does not apply that size bound to circuit representations.

## Verification status

The author ran the focused command

```sh
python3 -B research-20261002/new-direction/check_convex_point_radicals.py
```

The [persistent checker](check_convex_point_radicals.py) passed 11 exact
source comparisons; seven tree decompositions with 190 bags, checking
scope coverage and running intersection; and 35 paired endpoint and tie
checks, including positive comparison coordinates at 1000-bit scales.
These checks support the construction and do not replace its symbolic
proof. The predecessor has separate saved verification; its tests are
not claimed as new tests of (5).

Fresh actual-file mathematical reviews found no blocker. The unit-box
coefficient statement was clarified to discard its aggregate constant
term, and the reduction and graph terminology were made explicit.
The [independent review](../reviews/convex-point-radical-review.md) passed.
Its [separate exact diagnostic](../reviews/check_convex_point_radical_review.py)
passed 80 Hessian fixtures, 560 principal minors, and 2,160 identities
and bounds, including zero amplitudes, tiny positive amplitudes, and
indefiniteness of the added quartic before the base curvature is included.
The reviewer owns these runs; the author did not duplicate them. No
index edits, project-wide tests, or CI checks were made.
