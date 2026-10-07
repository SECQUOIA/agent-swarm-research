# Strict copositivity remains hard at treewidth three

Date: 2026-10-02. Status: a direct reduction with a
[fresh independent review](../reviews/strict-copositive-width3-review.md)
finding no substantive gap. A scoped source comparison remains pending.
Complementarity and homogenization are standard reduction tools. No
claim of a new hardness mechanism is made.

## What this limits

Recognizing strict copositivity of a rational quadratic is coNP-hard
even when its interaction graph has treewidth at most three and a
decomposition into positive semidefinite and entrywise nonnegative
matrices is supplied explicitly. The same construction has Hessian
bounded below by minus the identity.

This separates the unconditioned
[bounded articulation-block algorithm](articulation-copositive-elimination.md)
from a proposed extension depending only on treewidth. It does not
exclude an algorithm parameterized by treewidth and negative
curvature divided by a positive growth margin. No uniform positive
margin is asserted, and deciding ordinary, non-strict copositivity is
trivial for every instance constructed here.

## Construction

Start with SUBSET SUM: positive integers `a_1,...,a_n` and positive
integer target `B`, all encoded in binary, with `n>=1`. Use nonnegative
variables

```
t,   z_1,...,z_n,   w_1,...,w_n,   y_0,...,y_n.
```

There are `3n+2` variables. Define the homogeneous quadratic

\[
\begin{split}
q(t,z,w,y)={}&y_0^2+(y_n-Bt)^2\\
 &+\sum_{i=1}^n(z_i+w_i-t)^2\\
 &+\sum_{i=1}^n(y_i-y_{i-1}-a_i z_i)^2
   +\sum_{i=1}^n z_iw_i.                       \tag{1}
\end{split}
\]

Each term is nonnegative on the nonnegative orthant. Thus `q` is
copositive, and (1) is an explicit certificate of that fact. More
precisely, if `q(v)=v'Av`, its square terms give a rational PSD matrix
`P`, while the products give the symmetric entrywise nonnegative matrix
`N` with `N_(z_i,w_i)=N_(w_i,z_i)=1/2`. Hence `A=P+N` is explicitly
SPN. Here SPN means a sum of a positive semidefinite matrix and an
entrywise nonnegative matrix.

Expanding the squares produces integer or half-integer matrix entries
with polynomial binary encoding length. Coefficients such as `a_i^2`
and `B^2` double the corresponding bit lengths; they do not require
unary encoding. The construction therefore takes polynomial time.

## Zero vectors encode exactly the subsets

All summands of (1) must vanish at any nonnegative vector of value zero.
They imply

\[
 y_0=0,\qquad z_i+w_i=t,\qquad z_iw_i=0,
 \qquad y_i=y_{i-1}+a_i z_i,\qquad y_n=Bt.       \tag{2}
\]

If `t=0`, nonnegativity and `z_i+w_i=0` force every `z_i,w_i` to be
zero. The recurrence and `y_0=0` then force every `y_i` to be zero.
Consequently every nonzero zero vector has `t>0`.

For such a vector, (2) gives `z_i/t` in `{0,1}` and

\[
 \sum_i a_i(z_i/t)=B.                           \tag{3}
\]

Thus the indices with `z_i=t` solve SUBSET SUM. Conversely, any
solving subset defines a rational nonzero zero vector by setting
`t=1`, `z_i` to its indicator, `w_i=1-z_i`, and `y_i` to the running
selected sum. Every term in (1) is then zero.

We have proved

```
q is strictly copositive  <=>  the SUBSET SUM instance has no solution.
```

When there is no solution, strict positivity on nonzero orthant vectors
and compactness imply a positive Euclidean growth margin

\[
 g=\min_{v\ge0,\ \|v\|=1}q(v)>0.                \tag{4}
\]

This implication supplies no quantitative lower bound on `g`.
Complement SUBSET SUM reduces to strict copositivity, establishing
coNP-hardness. A polynomial-time strictness decision on these matrices
would therefore decide SUBSET SUM in polynomial time. The source
problem is weakly NP-complete; this reduction does not establish strong
hardness.

## A width-three decomposition

Use the path of bags

\[
 C_i=\{t,y_{i-1},y_i,z_i\},\qquad i=1,\ldots,n.
\]

For each `i`, attach to `C_i` the leaf bag

\[
 D_i=\{t,z_i,w_i\}.
\]

The recurrence square is supported in `C_i`, the complementarity square
and product in `D_i`, `y_0^2` in `C_1`, and `(y_n-Bt)^2` in `C_n`.
Thus every nonzero matrix entry has both endpoints in a bag. Running
intersection also holds: `t` occurs in every bag, each interior `y_i`
occurs in consecutive path bags, `z_i` occurs in `C_i,D_i`, and `w_i`
only in `D_i`. The maximum bag size is four, proving treewidth at most
three. It is not necessary to prove that the width is exactly three.

The biconnected blocks are not bounded in size by this decomposition.
For example, for positive weights and `n>=2`, the graph induced by
`t,z_1,...,z_n,y_1,...,y_n` contains the cycle

```
t,z_1,y_1,z_2,y_2,...,z_n,y_n,t.
```

All its listed edges have nonzero coefficients in (1), so one
biconnected block has at least `2n+1` vertices. This explains why the
articulation-block result does not already decide these instances.

## Negative curvature and the scope of the obstruction

The Hessian of each square term is PSD. The Hessian of `z_iw_i`, on
those two coordinates, is

\[
 \begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]

These coordinate pairs are disjoint. Their sum has minimum eigenvalue
minus one, and adding the PSD square Hessians cannot decrease that
minimum. Therefore

\[
 \nabla^2q\succeq-I,\qquad
 \nu:=\max\{0,-\lambda_{\min}(\nabla^2q)\}\le1. \tag{5}
\]

The positive curvature can be large. More importantly, the positive
margin in (4), when it exists, is not uniformly controlled. Hence (5)
does not prove hardness for bounded `nu/g`, or refute any of the
conditioned algorithms under consideration.

By homogeneity, the same strictness question is equivalent to whether
the origin is the unique global minimizer of `q` on the unit box.
A nonzero orthant zero can be scaled into that box; conversely every
nonzero box zero violates strict copositivity. Since (1) proves the
global minimum is zero in both cases, it is the strictness or uniqueness
decision that is hard here, not finding an optimal point or certifying
the minimum value. In particular, this is not a lower bound against
an optimization algorithm allowed to return the origin.

## Verification and prior-art boundary

The proof uses a standard binary-complementarity encoding and a running
sum, followed by homogeneous sum-of-squares penalties. The explicit
width-three graph and the distinction between strictness and already
certified nonnegativity are the purpose of recording it here. A scoped
comparison to existing bounded-width copositivity results is pending.

The construction checker was run as

```sh
python3 -B research-20261002/new-direction/check_strict_copositive_width3.py
```

The [persistent checker](check_strict_copositive_width3.py) passed 49
constructions (31 SUBSET SUM yes instances and 18 no instances), 246
decomposition bags with exact edge coverage and running intersection,
49 exact Gram identities for `Hessian(q)+I`, 1,568 direct-versus-matrix
evaluations, 1,044 scaled subset checks, and 35 nonzero unit-box zero
witnesses. A separate five-pivot rational LDL calculation certified
`A-I/100` positive definite for the no-instance `a_1=3,B=1`.
These are targeted finite checks; the general strictness conclusion
comes from (2)--(3), not numerical eigenvalues or sampled positivity.
The checker author also independently inspected the construction and
its scope. A separate
[actual-file review](../reviews/strict-copositive-width3-review.md)
checked the proof, graph, and complexity scope, inspected the checker,
and found no substantive gap. It did not rerun the author's diagnostic.
No project-wide checks or CI inspection are part of this note.
