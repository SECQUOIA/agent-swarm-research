# Exact smoothed mixed-integer QP by integer-gap cell closure

Date: 2026-10-02. Status: complete derivation with targeted exact checks and
a [fresh independent review](../reviews/smoothed-miqp-cell-closure-adversary.md).
No publication-priority claim is made.

An exact convex-MIQP oracle can certify more than a point value. It can
also compute the gap to every different integer assignment using a small
number of exclusion solves. That gap gives a robust cell-closure test.
If the test fails near the global optimum, independent perturbations of
the original integer coefficients make the failure rare through an
integer-label isolation bound. This extends exact cell closure to genuine
mixed-integer recourse without enumerating all integer assignments during
the usual search.

## 1. Result and notation

Let

\[
 \mathcal P=\{x\in\mathbb R^n:Mx\le b_X\},\qquad
 X=\mathcal P\cap(\mathbb Z^p\times\mathbb R^{n-p}),
 \qquad F(x)=\tfrac12x^TAx+b^Tx+c,
\]

where the data are rational, \(\mathcal P\) is bounded, and \(X\)
is nonempty. There are \(q\) input inequalities. Empty mixed feasibility
can first be detected by the exact convex-MIQP oracle. Lower-dimensional
polytopes, redundant inequalities, and nonunique optimizers are allowed.

Suppose rational \(\alpha>0\) and a full-row-rank
\(T\in\mathbb Q^{k\times n}\), \(1\le k\le n\), satisfy

\[
 P=A+\alpha T^TT\succeq0,\qquad \|T\|_2\le1,
 \qquad \ker P\subseteq\ker T.                         \tag{1}
\]

The reviewed normalization supplies these conditions with
\(k=n_-(A)\), \(2\nu\le\alpha<4\nu\), and
\(TT^T\succeq63I/64\), where
\(\nu=\max\{0,-\lambda_{\min}(A)\}>0\). For \(k=0\),
one exact convex-MIQP solve suffices.

Fix a rational \(\sigma>0\). Section 6 specifies one power-of-two
\(N\), determined by the base input before sampling, and sample all
\(n\) coordinates independently from

\[
 \{-\sigma+2\sigma j/(N-1):j=0,\ldots,N-1\}.            \tag{2}
\]

For every draw \(\gamma\), the algorithm returns an exact rational
optimizer and value of \(F_\gamma(x)=F(x)+\gamma^Tx\). It uses
the same draw for the search and exact fallback. If \(I\) is the base
encoding length including \(\sigma\), its expected bit work is

\[
 f(p)C^k(1+H_{\rm amb})(I+1)^C,                         \tag{3}
\]

for an absolute constant \(C\), with the explicit geometric factor
\(H_{\rm amb}\) below. This invokes the existing exact convex-MIQP
algorithm parameterized by integer dimension, as specified in the
[mixed Fenchel theorem](negative-inertia-miqp.md).

Write

\[
 D=(TT^T)^{-1}T,\quad E=I-T^TD,\quad
 d=D\gamma,\quad r=E\gamma,\quad \gamma=T^Td+r.
\]

Compute \(\ell_i=\min_{\mathcal P}(Tx)_i\),
\(u_i=\max_{\mathcal P}(Tx)_i\), and put

\[
 s_i=\sigma\|D_i\|_1,\qquad
 A_{\rm aux}=\prod_i[\ell_i-s_i/\alpha,u_i+s_i/\alpha],
 \quad w_i=u_i-\ell_i+2s_i/\alpha,\quad s=\max_iw_i.
\]

All these quantities are rational and fixed before sampling. Define

\[
 W_r(a)=\min_{x\in X}\{F(x)+r^Tx+\tfrac\alpha2\|a-Tx\|^2\},
 \qquad V_\gamma(a)=W_r(a)+d^Ta.
\]

Square completion gives

\[
 \min_{A_{\rm aux}}V_\gamma=\min_{\mathbb R^k}V_\gamma
 =f_\gamma^*-\|d\|^2/(2\alpha).                        \tag{4}
\]

The mixed envelope need not be differentiable, but it remains continuous
and \(\alpha\)-semiconcave. The ambient volume lemma and local
neighboring comparisons therefore give the same continuous-noise count
as in the [ambient continuous-QP theorem](smoothed-ambient-cell-closure.md):

\[
 H_{\rm amb}=\prod_{i=1}^k
 \left[2+\frac{(1+2k)\alpha\sqrt n\,w_i}{2\sigma}\right].
                                                               \tag{5}
\]

For the normalized factor, this is at most

\[
 \left[2+(1+2k)
 \left(2n+\frac{2\nu\sqrt n\operatorname{diam}(\mathcal P)}\sigma\right)
 \right]^k.                                               \tag{6}
\]

Thus the result is polynomial in expected work for each fixed \(p,k\)
under the displayed numerical bounds. The powers of \(n\) depend on
\(k\); this is not an FPT bound in \((p,k)\) and a dimension-free
curvature/noise ratio. Independent perturbations of the original integer
coefficients are used essentially in the proof.

## 2. A certified best-other-label oracle

Let \(z=x_{1:p}\) denote the integer label. At a rational query \(a\),
solve the convex MIQP defining \(W_r(a)\), and let \(z_*\) be the
integer label of an attaining witness. Define

\[
 \Delta(a)=\min_{x\in X:\,x_{1:p}\ne z_*}
 \{F(x)+r^Tx+\tfrac\alpha2\|a-Tx\|^2\}-W_r(a),          \tag{7}
\]

with \(\Delta=+\infty\) when no competing label exists.
Every other integer tuple satisfies at least one of the \(2p\) bounds

\[
 x_i\le z_{*,i}-1\quad\hbox{or}\quad x_i\ge z_{*,i}+1.
\]

Solving those convex MIQPs and taking their least feasible value computes
(7) exactly, with an attaining competing witness if finite. Each problem
has the same integer dimension and one additional linear inequality.
Thus (7) costs at most \(2p\) additional exact convex-MIQP calls.
For \(p=0\), no competitor exists and the gap is infinite.

Fixing \(z_*\), polish the winner by an exact continuous convex-QP
solve. Extract a continuous active-basis critical region \(R_J\) and
quadratic value formula \(q_J(a,r)\), using the optimal-set vertex and
nonnegative multiplier procedure of
[continuous cell closure](smoothed-exact-cell-closure.md). The integer
coordinates are fixed constants during this extraction. It yields the
value function of the fixed label on \(R_J\), not automatically the
mixed value function.

Choose the rational diameter bound

\[
 C_T=\max\{1,\sum_i(u_i-\ell_i)\}
 \ge\operatorname{diam}(T\mathcal P),\qquad
 \Lambda=\alpha k C_T.                                   \tag{8}
\]

Consider a level-\(j\) cell whose coordinate lengths are at most
\(h_j\), with a queried corner \(v\). The following is a sufficient
condition for exact closure:

\[
 C\subseteq R_J,\qquad \Delta(v)\ge\Lambda h_j.          \tag{9}
\]

**Proof.** Subtract the common term \(\alpha\|a\|^2/2\) from
all fixed-label value functions. Each becomes a minimum of affine
functions with slopes \(-\alpha Tx\). For any two feasible labels,
the difference of their value changes from \(v\) to \(a\) has
absolute value at most
\(\alpha\operatorname{diam}(T\mathcal P)\|a-v\|\).
This follows by bounding each minimum's change between the least and
greatest scalar slopes in direction \(a-v\), then subtracting the
bounds. Every competing label is therefore at least

\[
 \Delta(v)-\alpha C_T\|a-v\|
 \ge\Delta(v)-\alpha C_T\sqrt k\,h_j\ge0
\]

above the winner throughout the cell. The first condition in (9) supplies
its exact quadratic formula there. Hence \(W_r=q_J\) throughout the
cell. QED.

The test is valid even at integer ties: it never assumes that identical
corner labels alone certify a cell. Exactly minimize \(q_J+d^Ta\)
over a certified cell by the usual \(3^k\) box-face stationarity
enumeration and store its attaining fixed-label affine witness.

## 3. Active gradients and continuous-region failures

Bound the possible integer labels from LP ranges over \(\mathcal P\):
let \(L_i=\lceil\min_{\mathcal P}x_i\rceil\),
\(U_i=\lfloor\max_{\mathcal P}x_i\rfloor\), and set

\[
 Z=\prod_{i=1}^p(U_i-L_i+1),\qquad
 R=Z2^q,\qquad K=R(q+n+1).                               \tag{10}
\]

Use \(Z=1\) if \(p=0\). Nonempty mixed feasibility ensures all
factors are positive. These integers can be exponentially large, but their
encoding lengths are polynomial in \(I\). There are at most \(R\)
fixed-label continuous KKT bases. No such enumeration occurs in the search.

Every slice's continuous Hessian is \(P_{cc}\succeq0\). If
\(P_{cc}v=0\), then the full vector with zero integer coordinates has
zero \(P\)-quadratic form, hence lies in \(\ker P\) and is
annihilated by \(T\). Thus the kernel condition needed by the continuous
slice extraction holds. Each slice envelope is \(C^1\), although
the minimum over slices need not be.

More directly, if \(x\) is any attaining mixed witness at \(v\),
the global quadratic

\[
 Q_x(a)=F(x)+r^Tx+\tfrac\alpha2\|a-Tx\|^2+d^Ta
\]

is an upper bound on \(V_\gamma\) and touches it at \(v\).
Its own global minimum is at least \(\min V_\gamma\), so completing
its square gives

\[
 \|\alpha(v-Tx)+d\|^2
 \le2\alpha[V_\gamma(v)-\min V_\gamma].                 \tag{11}
\]

This holds for **every** attaining witness. Nonsmoothness introduces no
choice of a favorable gradient into the argument.

As in continuous closure, each extracted fixed-label piece has gradient
\(H_Ja+p_J(r,z)\), with \(H_J\) independent of \(r,z\) and
\(p_J\) affine in \(r\) for fixed \(z\). A uniform rational bound
\(\|H_J\|\le H_0\) is obtained from the response KKT system only:
clear denominators of \(P_{cc},M_c,\alpha T_c^T\), bound scaled
entries by \(C\ge1\), and use

\[
 H_0=\alpha[1+nk(2n)!C^{2n}].                            \tag{12}
\]

The bound is independent of integer values, residual perturbations, and
sampled denominators. If there are no continuous variables, each slice
piece has Hessian \(\alpha I\), and (12) still bounds it.

A retained unresolved cell has a corner with value at most
\(\min V_\gamma+2B_j\), where
\(B_j=\alpha\sum_i h_{ij}^2/8\le k\alpha h_j^2/8\).
If its winner's fixed-label region does not contain the cell, (11) and
the critical-region argument put the noise in an ambient tube about one
of at most \(K\) fixed hyperplanes. The tube width is
\(\sqrt k(\alpha+H_0)h_j\). The normals are nonzero after pulling
back to ambient noise because their factor normal \(u\) and ambient
normal \(w\) satisfy \(Tw=u\), just as in the continuous theorem.
Consequently the probability of this type of failure under (2) is at most

\[
 K\left[\frac{nk(\alpha+H_0)h_j}{\sigma}+\frac1N\right].
                                                               \tag{13}
\]

We used \(nk\ge\sqrt{nk}\) for a rational coefficient. The integer
labels only increase the finite hyperplane count; they do not change the
geometric argument.

## 4. Integer-label isolation controls gap failures

Put

\[
 G=\sum_{i=1}^p(U_i-L_i),
 \qquad C_{\rm gap}=k\alpha s/4+\Lambda.                 \tag{14}
\]

The following elementary finite-grid isolation bound, independently
derived in [the integer-label isolation note](integer-label-isolation.md),
applies to any objective with these integer labels, including an arbitrary
optimized continuous part:

\[
 \Pr_N\{\text{two distinct labels have feasible values}
                  \le f_\gamma^*+\varepsilon\}
 \le G(\varepsilon/\sigma+1/N).                         \tag{15}
\]

To prove it, condition on every noise coefficient except the \(i\)-th
integer coefficient. Group feasible points by their integer value \(t\)
in this coordinate, and minimize over all other variables. The group
value is \(a_t+\gamma_i t\), where \(a_t\) is independent of
\(\gamma_i\). Only finitely many groups are nonempty. Their lower
envelope has at most \(U_i-L_i\) breakpoints, since its minimizing
slope decreases monotonically and the slopes are distinct integers.

If a winning group and a different group are within \(\varepsilon\)
in value, their two lines cross within distance \(\varepsilon\) of
the current coefficient, since their slope difference has magnitude at
least one. Moving toward that crossing encounters an actual lower-envelope
breakpoint no later. Thus the coefficient lies in the union of the
\(\varepsilon\)-neighborhoods of at most \(U_i-L_i\) fixed
breakpoints. An interval of length \(2\varepsilon\) has grid probability
at most \(\varepsilon/\sigma+1/N\). If two distinct labels are
near-optimal, compare a global winning label with a distinct near-optimal
one and choose a coordinate where they differ. Union over integer
coordinates proves (15). Ties are included as zero-distance breakpoints.
When \(G=0\), there is only one possible label and the event is empty.

Now suppose the region condition in (9) holds at the near-optimal corner,
but the gap condition fails. Its winning and competing witnesses have
different integer labels. By (4) and square completion, their original
objective values are at most

\[
 f_\gamma^*+2B_j+\Delta(v)
 \le f_\gamma^*+\bigl(k\alpha s/4+\Lambda\bigr)h_j.
\]

Here \(h_j\le s\). Equation (15) therefore bounds the probability
of any such retained-cell gap failure by

\[
 G\left[C_{\rm gap}h_j/\sigma+1/N\right].                \tag{16}
\]

This event concerns the original optimization problem, so the grid's
adaptive choice of a corner creates no additional probability dependence.

## 5. Local-event counts and finite-grid transfer

Use the fixed nested equal-subdivision auxiliary grids from the continuous
theorem. For each deterministic node \(v\), let \(E_v\) require
all neighboring comparisons with tolerance \(2B_j\). Coordinate
semiconcavity is valid for mixed recourse, and the volume argument uses
only its dependence on the residual perturbation. Thus
\(\sum_v\Pr_{\rm cont}(E_v)\le H_{\rm amb}\) remains valid.

The finite-grid section bound needs one modification. Fix all but one
original noise coefficient and let the remaining coefficient vary along
a line. At one fixed auxiliary query, each fixed-label KKT basis supplies
a quadratic value on an interval, with at most \(R\) candidates.
The mixed value is the least of the available quadratics. Their interval
endpoints number at most \(2R\); their pairwise polynomial intersections
number at most \(R(R-1)\). Identical polynomial pairs require no split.
Thus at most \(2R^2\) points divide the line into intervals on which
one quadratic formula describes the mixed value. Values at the dividing
points can be handled separately.

The local event uses at most \(2k+1\) query values and \(2k\)
quadratic comparisons. The same root-count argument gives the uniform
section-component bound

\[
 C_{\rm sec}=[2(2k+1)R^2+1](8k+2).                       \tag{17}
\]

This remains valid for singular slices and empty or zero-dimensional
critical intervals. Replacing the independent noise coordinates one at a
time proves

\[
 |\Pr_N(E_v)-\Pr_{\rm cont}(E_v)|\le2nC_{\rm sec}/N.     \tag{18}
\]

This is a finite combinatorial bound with polynomial logarithm. It does
not require evaluating or enumerating the intervals or integer labels.

## 6. Fixed sampling precision, fallback, and bit work

Set

\[
 B=\max\{2,Z2^q\},\qquad
 C_{\rm bad}=Knk(\alpha+H_0)+G C_{\rm gap}.              \tag{19}
\]

Choose the least integer \(J\ge0\) such that

\[
 s2^{-J}\le\frac{\sigma}{2B C_{\rm bad}},
 \qquad Q_{\rm all}=(J+1)(2^J+1)^k,                     \tag{20}
\]

then choose the least power of two satisfying

\[
 N\ge\max\{2,\ 2B(K+G),\ 2nC_{\rm sec}Q_{\rm all}\}.  \tag{21}
\]

All choices use only base data. LP integer ranges, \(Z,R,K,G,B\),
and the rational response bound have polynomial encoding lengths.
Consequently \(J\) and \(\log N\) are polynomial in \(I\).

Run the continuous cell search with the additional test (9). Query all
corners, and try their extracted fixed-label regions and exact integer
gaps. Close a cell only with a valid certificate. After all incumbent
updates, retain unresolved cells whose corrected-corner lower bounds do
not exceed the incumbent. If no unresolved cells remain, the auxiliary
optimum and its original witness are exact. Every retained unresolved
cell has a near-optimal corner, whose failed test is covered by either
(13) or (16). At level \(J\), the probability that any such cell
remains is at most \(1/B\), by (19)--(21).

On that event, solve the same perturbed original problem by enumerating
all integer labels in the LP range box and applying the exact continuous
active-face QP fallback on every feasible slice. This takes at most
\(B\operatorname{poly}(I+\log N)\) bit operations. Minimal optimal
faces supply nonsingular stationary KKT candidates even when the slice
has flat or lower-dimensional optimal sets. In the purely integer case,
only feasibility and value evaluation of each label are needed. This
fallback is always correct, including on ties and noise atoms.

From (18) and (21), summing local events over all levels costs at most
\((J+1)H_{\rm amb}+1\) in expectation. Their corners cover retained
unresolved cells with incidence at most \(2^k\), and every retained
cell has at most \(2^k\) children. Each processed cell requires a
factor exponential only in \(k\), at most \(2p+1\) convex-MIQP
calls per queried corner, continuous polishing and extraction, and at
most \(3^k\) local face solves per closure. This proves (3).

For arithmetic, every oracle instance has rational input of polynomial
length in \(I+J+\log N\). The existing exact convex-MIQP algorithm
costs \(f(p)\) times a polynomial with an absolute exponent. Fixing
its returned bounded integer tuple and polishing the continuous convex
slice supplies uniformly polynomial-height values and witnesses. This
avoids propagating a merely parameter-dependent output-height bound.
The extracted critical formulas use the original fixed matrices and
bounded integer values, and grid centers do not depend on oracle output
denominators. Expected fallback work is at most
\((1/B)B\operatorname{poly}(I+\log N)\).

The proof therefore has no sampling/recovery precision circle. It uses
neither a growth hypothesis nor generic uniqueness, and it never discards
or resamples an exceptional draw.

## 7. Verification status and limitations

The parent researcher independently read the complete argument and found
no substantive gap in the value-change bound, kernel inheritance, active
upper-model gradients, original-label gap transfer, scalar-section count,
fixed law, or fallback. The
[fresh adversarial review](../reviews/smoothed-miqp-cell-closure-adversary.md)
also passed the complete argument and independently checked the exact
convex-MIQP oracle contract against its primary statement. A separate
reviewer confirmed the exclusion, gap-transport, and isolation steps.

The command
`python research-20261002/new-direction/check_smoothed_miqp_closure.py`
passed 23 exact-rational cases, 134 levels, and 463 processed cells. The
[checker](check_smoothed_miqp_closure.py) recorded 90 certified gap
closures, 152 ordinary prunes, 137 integer-gap events, and 84
continuous-region events. It checks whole-cell dominance against every
competing slice piece, exact local minima, the incumbent invariant, active
gradient bounds, and the original near-optimality of both witnesses in a
gap-failure event. The fixtures cover positive, zero, and negative
continuous-slice curvature, coupled integer and continuous variables, and
a literal finite-grid tie between distinct optimal labels.

Twenty-two cases finished by closure. One additional case used a
deliberately zero-stage cap to test the same-draw fallback. The initial
diagnostic incorrectly expected an original-label tie to force fallback;
tied optima may lie in separate auxiliary regions that can each be
certified. That assertion was replaced by the explicit cap test. The
final command passed. The diagnostic uses one binary and one continuous
variable with explicit exact slice minimization, not the production
convex-MIQP oracle or the theorem's potentially much larger cutoff.

The checker also verifies why corner labels alone are insufficient. On
\(X=[0,1]^2\), with the first variable binary, take
\(\alpha=4\), \(T=(1/4,1/2)\),
\(P=\left(\begin{smallmatrix}2&1\\1&1\end{smallmatrix}\right)\),
and \(b=(-15/16,0)\). Without noise, label zero is the strict winner
at both auxiliary endpoints \(0,1/2\), with its value formula identically
zero throughout that cell. Label one has lower value \(-1/16\) at
\(a=1/4\). The gap test correctly refuses this cell.

The mixed oracle must return certified exact values and feasible witnesses;
uncertified numerical values do not justify the gap test. No
polynomial-time oracle is claimed for unbounded integer dimension. The
continuous-QP proof's direct critical-region certificate alone does not
extend to mixed recourse: the additional gap test is essential to the
present argument.

The [focused prior-art audit](../prior-art/smoothed-exact-miqp-prior.md)
compares this statement with established exact convex-MIQP oracles,
parametric-QP critical regions, integer-label isolation, and deterministic
low-negative-inertia approximation. Those mechanisms are not claimed as
new. The distinction here is their use in a certified whole-cell test and
an expected exact bit-work bound for one fixed finite ambient-noise law.
The audit distinguishes the closest objective-range-relative
approximation bounds and discrete high-probability smoothed bounds from
this exact expected-work claim; it does not establish publication priority.

Scoped whitespace, mathematical-delimiter, local-link, and diagnostic
syntax checks passed.

No project-wide checks, CI inspection, or external search were performed
for this note. Its dependence on prior exact convex-MIQP theory is the
one recorded in the mixed Fenchel note; the isolation argument above is
included explicitly rather than claimed as a new principle.
