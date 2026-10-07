# Exact active-bound recognition contains radical-sum comparison

Date: 2026-10-02. Status: direct reduction with a
[fresh actual-file review](../reviews/convex-active-set-radical-review.md)
finding no substantive gap. A scoped primary-source comparison is pending.
This is an output-contract distinction, not an NP-hardness claim or a
new convex optimization method.

There is a polynomial-time reduction from the decision problem

\[
             \sum_{i=1}^n\sqrt{a_i}\le B                      \tag{1}
\]

for binary-encoded positive integers `a_i` and integer `B`, to deciding
whether one specified coordinate of the unique optimizer is at its lower
bound. The resulting objective is an explicitly represented rational
cubic on a bounded rational box. It is uniformly strongly convex, has
upper coordinate curvature at most five, and has a tree decomposition
with bag size three. All domain widths and numerical coefficient
magnitudes are bounded by absolute constants.

Consequently a polynomial-time exact active-bound routine on this
restricted class would decide Square Root Sum in polynomial time. The
reduction does not show that this class is hard to approximate or to
represent by an exact implicit convex subproblem. The original convex
problem already provides such a representation.

## 1. Normalize the radicals and form a balanced average

Remove zero radicands if the source formulation allows them, and handle
an empty sum or negative target directly. For each remaining `a_i`,
choose the power of two `R_i` satisfying

\[
 R_i^2\le a_i<4R_i^2.
\]

Set

\[
 c_i=a_i/R_i^2\in[1,4),\quad
 M=\max_iR_i,\quad w_i=R_i/M\in(0,1].
\]

Let `K` be the least power of two at least `max(2,n)`. Use a complete
binary tree with `K` leaf slots. A real leaf has variable `u_i in [1,2]`
and signal `w_i u_i`; every padded leaf has fixed signal zero. Each
internal node has a variable `v in [0,2]`. Its residual is

\[
 r_v=v-\tfrac12(\hbox{left-child signal}
                         +\hbox{right-child signal}),       \tag{2}
\]

where an internal child's signal is its own variable. Denote the root
variable by `s`. Define

\[
 F_0(u,v)=\sum_{i=1}^n(u_i^3/3-c_i u_i)+\sum_v r_v^2.       \tag{3}
\]

The derivative of a leaf objective is `u_i^2-c_i`, so its unique
minimum on `[1,2]` occurs at `u_i=sqrt(c_i)`. All residual squares can
simultaneously vanish by assigning the internal averages. Therefore
these values specify the unique minimizer of (3), and its root is

\[
                    s^*=\frac{\sum_i\sqrt{a_i}}{KM}.        \tag{4}
\]

The independent strong-convexity proof below also establishes uniqueness.
Padding-only subtrees simply have zero optimal internal coordinates.

If `B>=2KM`, the source decision is immediately true; all remaining
cases have

\[
                         b=B/(KM)\in[0,2].                 \tag{5}
\]

All normalization operations and expanded factor coefficients have
polynomial binary length in the source input. The complete tree has
fewer than `2n` leaves when `n>=2`; the `n=1` case uses two. Thus the
construction has linear size apart from ordinary index encoding.

## 2. A single bound encodes the decision

Introduce `y in [0,1]`, set `epsilon=1/32`, and minimize

\[
 F(u,v,y)=F_0(u,v)+y^2+\epsilon y(b-s).                     \tag{6}
\]

As proved below, (6) is strongly convex on its whole box. On the face
`y=0`, its unique minimizer is the point in (4). At that point the
derivative in the new coordinate is

\[
                         \partial_yF=\epsilon(b-s^*).
\]

If (1) holds, this derivative is nonnegative. The other coordinates
satisfy the convex first-order conditions for `F_0`, so the point with
`y=0` satisfies the box KKT conditions for (6) and is its unique global
minimizer. This includes equality in (1).

If (1) fails, increasing `y` slightly while holding the other coordinates
fixed decreases (6). No optimizer can have `y=0`, since its restriction
to that face has only the minimizer already considered. Hence

\[
      y^*=0\quad\Longleftrightarrow\quad
                         \sum_i\sqrt{a_i}\le B.             \tag{7}
\]

In fact the alternative has `0<y^*<1`: at `y=1`,
`partial_y F=2+epsilon(b-s)>=2-2epsilon>0`, which violates the
first-order condition at an upper-bound minimizer.

## 3. Uniform conditioning

Collect the `u` and `v` coordinates into one vector. Let `P` have a
zero row at each real leaf and, at each internal row, the child
coefficients appearing in (2). Each nonzero coefficient is at most
`1/2`, each row has at most two, and each variable is a child of at
most one parent. Distinct rows thus have disjoint column supports.
Consequently

\[
 PP^T\preceq\tfrac12I,\qquad \|P\|_2\le1/\sqrt2<3/4.
\]

For every vector `d`, the leaf Hessians satisfy `2u_i>=2`, and the
residuals are affine. Hence

\[
 d^T\nabla^2F_0d
 \ge2\|(I-P)d\|^2
 \ge\tfrac18\|d\|^2.                                     \tag{8}
\]

Appending `y^2` preserves the lower Hessian bound `I/8`. The additional
bilinear term has Hessian operator norm exactly `epsilon`, supported on
the root and `y`. Thus throughout the full box,

\[
 \nabla^2F\succeq(1/8-1/32)I=3I/32\succeq I/16.           \tag{9}
\]

Strong convexity and the box first-order condition imply global point
growth at the constrained minimizer with `g=1/32`.

Each leaf diagonal Hessian entry is at most `4+1/2=9/2`; each internal
entry is at most `2+1/2=5/2`; and the new coordinate's entry is two.
The bilinear term changes none of these diagonals. Therefore `L=5` is
a valid upper coordinate curvature bound, and

\[
                    L/g\le160.                             \tag{10}
\]

Negative curvature is zero. Large numerical curvature, long domain
intervals, or poor conditioning do not explain the exact comparison
embedded in (7).

## 4. Sparse structure and output scope

For each internal residual use the bag consisting of its variable and
its nonconstant child variables. Join a bag to its parent's bag.
Adjacent bags share just the child internal variable. Each real leaf
variable occurs in only its parent's bag, which also holds its unary
cubic factor. Attach the bag `{s,y}` at the root. This is a valid tree
decomposition of maximum bag size three, with running intersection and
complete factor coverage. Numerical coefficients are bounded because
`c_i<4`, `w_i<=1`, `b<=2`, and `epsilon=1/32`.

The construction clarifies an output distinction in the
[implicit convex-patch theorem](implicit-convex-patch-certificate.md)
and the [smoothed polynomial theorem](smoothed-sparse-polynomial.md).
An exact implicit point together with certified arbitrary-precision
evaluation does not automatically provide an exact test of whether a
coordinate equals a bound. Evaluation at any finite precision may leave
that equality unresolved. The same applies to an exact comparison of
general algebraic objective values from approximation access alone.

No reduction to the difficulty of **producing** the implicit descriptor
is asserted: (6), its box, and (9) are already a compact valid descriptor.
Nor is this a separation of complexity classes. The conclusion is the
specific implication (7). The [focused source comparison](../prior-art/convex-active-set-radical-prior.md)
identifies the canonical Square Root Sum predicate, its known upper bounds,
and the distinction between threshold comparison, equality testing, and
approximate convex optimization. It makes no publication-priority claim.

## Verification status

The author ran

```sh
python3 -B research-20261002/new-direction/check_convex_active_set_radicals.py
```

The [persistent checker](check_convex_active_set_radicals.py), using
exact fractions, passed 14 construction fixtures, including a 400-bit
radicand; 54 bags with edge coverage and running intersection; 14 exact
positive-LDL checks of the Hessian lower matrix minus `I/16` and the
coordinate-curvature bounds; and 12 perfect-square KKT comparisons.
The last cases include equality and explicit improving feasible
directions when the comparison fails. These checks do not replace the
symbolic argument for arbitrary radicals or dimensions.

The independent reviewer read the actual note and checked the
normalization, Gram bound, uniform constants, graph, equality case,
and output scope by direct algebra. The reviewer did not rerun the
author's diagnostic. No general optimizer, project-wide check, CI
inspection, or external source search was used in this derivation.
