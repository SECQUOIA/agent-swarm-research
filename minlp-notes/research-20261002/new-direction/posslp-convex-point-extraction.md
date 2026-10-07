# Constant-accuracy convex polynomial point extraction contains PosSLP

Date: 2026-10-02. Status: complete reduction with a
[fresh actual-file review](../reviews/posslp-convex-point-review.md)
finding no substantive gap. No external search or index edit was used.
This is a conditional complexity implication, not an NP-hardness claim
or a separation of complexity classes.

Given a straight-line circuit over constants `0,1` and operations
addition, subtraction, and multiplication, let `A` be its integer output.
The decision problem PosSLP asks whether `A>0`.

There is a polynomial-time transformation of such a circuit into an
explicit rational polynomial of degree at most four on a rational box,
together with a direct convexity proof, such that every minimizer has
one designated coordinate

\[
                 y=1\quad\hbox{if }A>0,
 \qquad         y=0\quad\hbox{if }A\le0.
 \tag{1}
\]

Consequently, polynomial-time approximation within `1/4` in maximum
norm of **some** true minimizer would decide PosSLP in polynomial time.
The same implication holds for Euclidean point error `1/4`, and does not
depend on selecting a canonical optimizer. Treewidth is unrestricted.

The [focused primary-source comparison](../prior-art/convex-point-posslp-prior.md)
credits earlier PosSLP reductions to constant-gap actual-solution
approximation and exact convex feasibility. It identifies the present
target class without claiming publication priority or a strict complexity
separation from Square Root Sum.

## 1. A bounded rational circuit preserving the sign

Represent every integer-circuit value `a` by a rational pair `(u,v)`
with `v>0` and `u/v=a`. Use `(0,1/4)` for zero and `(1/4,1/4)` for
one. Given two earlier pairs, implement addition or subtraction by

\[
 u=\frac{u_1v_2\mathbin{\pm}u_2v_1}{4},
 \qquad v=\frac{v_1v_2}{4},
 \tag{2}
\]

and multiplication by

\[
 u=\frac{u_1u_2}{4},\qquad v=\frac{v_1v_2}{4}.
 \tag{3}
\]

These operations preserve the stated ratios and positivity of exact
denominators. All pair coordinates stay in `[-1/4,1/4]`. Indeed the
addition numerator has magnitude at most `1/32`, and each normalized
product has magnitude at most `1/64`.

For the output pair append the affine gate

\[
 t=\frac{2u-v}{4}=\frac v4(2A-1).
 \tag{4}
\]

Thus the exact output `t*` is nonzero, and is positive exactly when
`A>0`. Its gate polynomial has magnitude at most `3/16` on the entire
pair box. No zero-case oracle is needed.

Order all pair coordinates and the last gate topologically as
`x_1,...,x_N`, with `x_N=t`. Write their equations as
`x_i=p_i(x_1,...,x_{i-1})`. There are only linearly many such coordinates
in the source circuit size. Each `p_i` is a rational polynomial of
degree at most two, with at most two monomials. On the fixed box

\[
 \mathcal B=[-1/4,1/4]^N
\]

the explicit gate formulas satisfy

\[
 |p_i|\le\tfrac14,\qquad
 \|\nabla p_i\|_1\le1,\qquad
 \|\nabla^2p_i\|_2\le1.
 \tag{5}
\]

These bounds also cover repeated inputs, constants, and the final affine
gate. Exact gate evaluation defines a feasible point `x*`, even though
writing its rational coordinates explicitly may require many bits. The
reduction writes only the gate equations; it never expands those exact
values or introduces explicit doubly small constants.

## 2. A strongly convex weighted gate objective

Set

\[
 a_i=64^{N-i},\qquad r_i=x_i-p_i(x),\qquad
 G(x)=\sum_{i=1}^N a_i r_i(x)^2.
 \tag{6}
\]

The triangular gate equations have exactly one solution, namely `x*`.
Thus `G>=0` and `G(x*)=0`, with a unique zero in the box.
We now prove the stronger property `H_G>=I` throughout the box.

Let `D=diag(sqrt(a_i))`, and let `L` be the strictly lower-triangular
matrix with entries `L_ij=partial_j p_i`. The residual Jacobian is
`I-L`. For `E=DLD^{-1}`, the weight ratio and (5) give

\[
 \|E\|_\infty\le\tfrac18,
 \qquad
 \|E\|_1\le\sum_{k\ge1}8^{-k}=\tfrac17.
 \tag{7}
\]

For the row bound, every predecessor has weight ratio at most `1/64`,
and the derivative absolute row sum is at most one. For the column
bound, each later topological position occurs once and each individual
derivative has magnitude at most one. Consequently
`||E||_2<=1/sqrt(56)<1/4`. For every direction `h`, the positive
Jacobian part of the Hessian satisfies

\[
 2\|D(I-L)h\|^2
     \ge\tfrac98\|Dh\|^2.
 \tag{8}
\]

The remaining Hessian term is `-2 sum_i a_i r_i H_p_i`.
Since `|r_i|<=1/2` and `p_i` depends only on earlier coordinates,
its quadratic form is bounded below by

\[
 \begin{aligned}
 -\sum_i a_i\|h_{<i}\|^2
 &=-\sum_j h_j^2\sum_{i>j}a_i\\
 &\ge-\tfrac1{63}\sum_j a_jh_j^2.
 \end{aligned}
 \tag{9}
\]

Combining (8) and (9) gives

\[
 H_G\succeq\left(\tfrac98-\tfrac1{63}\right)D^2
                    \succeq I.
 \tag{10}
\]

In particular, because all residuals vanish at `x*`, its ambient
gradient also vanishes, including coordinates whose exact gate values
lie on a box bound. Hence
`G(x)>=||x-x*||^2/2` on the box.

The objective `G` has degree at most four and only `O(N)` expanded
monomials before combining duplicates. Every weight has `O(N)` bits;
the complete encoding and the algebraic convexity certificate have
polynomial length. The gate structure and all bounds used above can
be checked in polynomial time.

## 3. Two strongly convex sign tests

Use independent copies `x+` and `x-` of the gate variables, with output
coordinates `t+` and `t-`. Append `a+,a- in [0,1]`, put `epsilon=1/32`,
and define

\[
 \begin{aligned}
 H_+(x^+,a_+)&=G(x^+)+a_+^2-\epsilon a_+t_+,\\
 H_-(x^-,a_-)&=G(x^-)+a_-^2+\epsilon a_-t_-.
 \end{aligned}
 \tag{11}
\]

These are rational quartics. The Hessian of each added bilinear term
has operator norm `epsilon`, whereas `G+a^2` has Hessian at least `I`.
Thus each `H_+` and `H_-` is strongly convex with modulus
`1-epsilon=31/32`, and in particular at least `1/2`.

On the face `a=0`, each objective has the unique minimizer `x*`.
The new lower-bound derivatives there are `-epsilon t*` and
`+epsilon t*`, respectively. Convex box KKT conditions therefore give

\[
 \begin{aligned}
 a_+^*>0&\quad\Longleftrightarrow\quad t^*>0,\\
 a_-^*>0&\quad\Longleftrightarrow\quad t^*<0.
 \end{aligned}
 \tag{12}
\]

For completeness, a nonnegative lower-bound derivative certifies the
point `(x*,0)` as the unique minimizer. A negative derivative provides
an improving feasible direction; no other point on that face can be
globally optimal, since its restriction has only the minimizer `x*`.
At `a=1`, the derivative is at least `2-epsilon/4>0`, so a positive
optimal auxiliary coordinate is strictly below one.

Since `t*!=0`, exactly one of `a_+*` and `a_-*` is positive. No
quantitative lower bound on that positive number is required.

## 4. A convex quartic amplifier fixes the final coordinate

Append `y in [0,1]`, put `eta=1/192`, and define

\[
 \begin{aligned}
 F(x^+,a_+,x^-,a_-,y)
 &=H_+(x^+,a_+)+H_-(x^-,a_-)\\
 &\quad+\eta\bigl[a_+^2(y-1)^2+a_-^2y^2\bigr].
 \end{aligned}
 \tag{13}
\]

This is the paired amplifier already used in the
[Square Root Sum point construction](convex-point-radical-comparison.md).
The proof below is included so this reduction does not depend on that link.

To verify joint convexity, let `p` denote a direction in all base
coordinates, with auxiliary components `p_+` and `p_-`, and let `q`
be its `y` component. Each quartic term has the Hessian identity

\[
 \begin{aligned}
 d^TH_{a_+^2(y-1)^2}d
   &=2\bigl(a_+q-2(1-y)p_+\bigr)^2-6(1-y)^2p_+^2,\\
 d^TH_{a_-^2y^2}d
   &=2\bigl(a_-q+2yp_-\bigr)^2-6y^2p_-^2.
 \end{aligned}
 \tag{14}
\]

The sum of the base Hessians is at least `I/2`. Since `0<=y<=1`,
the negative terms in (14) have total magnitude at most
`6eta(p_+^2+p_-^2)`. Consequently

\[
 (p,q)^TH_F(p,q)\ge
       (1/2-6\eta)\|p\|^2=\tfrac{15}{32}\|p\|^2\ge0.
 \tag{15}
\]

Thus `F` is jointly convex on its rational box. It has degree at most
four and a polynomial-size explicit rational encoding.

Let `m_+` and `m_-` be the two base minima. The coupling in (13) is
nonnegative, so `F>=m_++m_-`. If `t*>0`, the unique base minimizers
have `a_+*>0` and `a_-*=0`. Choosing `y=1` makes both coupling terms
zero, attaining this lower bound. Every global optimizer must therefore
attain both base minima and make the coupling zero; the positive
`a_+*` forces `y=1`. If `t*<0`, the symmetric argument forces `y=0`.

The base minimizers are unique, and the final coordinate is forced.
Hence the complete final optimizer is unique in both source cases.
Its Hessian is positive definite: (15) is strict for any nonzero base
direction, and for a pure `y` direction the curvature is
`2eta((a_+*)^2+(a_-*)^2)>0`. No useful numerical lower bound on this
last curvature is asserted.

Combining (4) and (12) gives (1). A point within `1/4` of the true
minimizer has its designated coordinate above `1/2` exactly when `A>0`.
This proves the reduction without evaluating any gate output, auxiliary
coordinate, or source sign during construction.

## 5. Scope and representations

The reduction does not resolve the complexity of PosSLP. Its conclusion
is the implication: a deterministic polynomial-time algorithm for this
constant-accuracy convex polynomial point task would put PosSLP in
deterministic polynomial time. An always-correct randomized point routine
with expected polynomial running time would instead give a Las Vegas
expected polynomial-time algorithm for PosSLP. An expected-time guarantee
alone is not a deterministic polynomial-time conclusion.

Value approximation is a different output contract. Tiny auxiliary
coordinates can make the objective difference distinguishing the cases
very small. The original polynomial and box already form a compact
implicit optimizer descriptor; the implication concerns polynomial-time
evaluation of a point near a true minimizer from that description. It
does not apply to value-only approximation or to an unevaluated `argmin`
descriptor. Long exact encodings of gate values or algebraic coordinates
are separate issues: the requested output coordinate here is exactly
zero or one, and only constant accuracy is used.

If bounded coefficient magnitudes are desired, multiply the entire final
objective by `64^(-N)`. This preserves all optimizers and convexity, gives
gate weights `64^(-i)`, and keeps every expanded coefficient bounded by
an absolute constant. Their rational encoding lengths remain polynomial;
the base curvature is then scaled as well. An affine change sends the
fixed rational box to a unit box without changing the degree or polynomial
encoding length. No bounded-treewidth claim is made.

## 6. Core-only noise does not remove the implication

Append an independent core coordinate `v in [0,1]` and add
`(v-1/2)^2+gamma v`, with core noise `gamma in [-1/2,1/2]` and no
noise in the residual coordinates. The core upper curvature is two.
For every draw the unique core optimum is `v_gamma=1/2-gamma/2`, and
the projected value gap is exactly `(v-v_gamma)^2`. Thus the core
dimension is one and projected quadratic growth is one, with all these
parameters fixed independently of the source circuit.

Every draw has the same residual optimizer and the same decision
coordinate `y` from (1). A full-point theorem for merely convex residual
objectives that is always correct and has expected polynomial work over
an efficiently sampled finite rational core-noise law would therefore
give a Las Vegas expected polynomial-time PosSLP algorithm. This also
applies to an exact descriptor accompanied by a polynomial-time full-point
Cauchy evaluator. Sampling only this independent core cannot hide an
incorrect residual endpoint or turn a value guarantee into a point
guarantee.

## Verification status

The pair normalization, weighted convexity estimate, paired Hessian
identities, and endpoint conclusions were derived algebraically. A scoped
`git diff --check` passed. An inline `python3 - <<'PY'` command checked
whitespace, all C0/C1 control characters, paired math delimiters, equation
numbering, and the local link. Exact calculations verified 11 gate-bound
forms, including repeated inputs; nine rational normalization and sign
fixtures, including zero and negative source outputs; the weighted-norm
constants; and both quartic Hessian identities. All checks passed.

The [independent review](../reviews/posslp-convex-point-review.md) passed
the final actual file, including the deterministic versus Las Vegas,
independent noisy-core, and full-point Cauchy-evaluator scope in Sections
5–6. Its separate
[exact checker](../reviews/check_posslp_gate_review.py) and
[saved results](../reviews/posslp-gate-review-results.json) cover four
source circuits, 41 normalized pairs, 447 local vertices, 688 gate jets,
and 32 rational Hessian checks. Those reviewer checks were not rerun by
the author. No external search, project-wide checks, or CI inspection
was used.
