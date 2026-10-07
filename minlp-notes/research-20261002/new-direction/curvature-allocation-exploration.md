# Shared coordinate intervals and certified pruning remove occurrence

Date: 2026-10-02. Status: a mathematical route to an occurrence-free
approximation algorithm; an independent review found no flaw in its central
contraction and pruning argument. Section 10 gives a simpler reduction to
the existing point-grid algorithm. This exploration
uses only the local notes and direct derivations. It makes no external
priority claim.

The main result is stronger than the initial curvature-allocation idea.
Coordinate intervals are shared exactly across all bags, and conditional
dynamic-programming bounds prune their ranges after each solve. The first
change prevents copy drift. The second keeps tensor products of geometric
grids within an FPT bound.

## 1. Proposed theorem

Let

\[
 F(x)=\tfrac12x^THx+b^Tx+a,\qquad x\in X=\prod_i[l_i,u_i]
\]

have rational data, a supplied tree decomposition of its interaction graph
with bag size at most \(p\), and a rational bound \(M\ge\|H\|_2\).
Assume a unique minimizer \(x^*\) and global quadratic growth

\[
 F(x)-F(x^*)\ge g\|x-x^*\|_2^2\quad(x\in X),\qquad g>0.
 \tag{1}
\]

Write \(I\) for total binary input length. The construction below gives a
rational feasible point and a valid global lower bound with gap at most
\(2^{-q}\) in

\[
 f\bigl(p,\max\{1,M/g\}\bigr)(I+q+1)^C
 \tag{2}
\]

bit operations, for an absolute exponent \(C\). Neither a bound on variable
occurrence nor a supplied growth constant is needed. The unknown-growth
claim uses dovetailing of sound trials, described below.

The exact-output extension uses the existing rational-height bounds and
rational reconstruction in [the box-QP note](../geometric-dp/exact-box-qp.md).
The new argument here is the approximation bound and its pruning invariant.

Fixed coordinates can first be substituted out. If no coordinates remain,
the problem is immediate. If \(H=0\), minimize the affine objective at box
endpoints. Below, \(n\ge1\), every side has positive length, and \(M>0\).

## 2. Canonical allocation and a global absolute-Hessian bound

Sum any supplied local coefficients to obtain the global quadratic, then
assign each nonzero Hessian entry to one bag containing its indices.
Assign each diagonal, linear term, and the constant once as well. Let
\(a_t\) be the resulting bag quadratic and \(H_t\) its Hessian. Embedded
in the full coordinate space, these satisfy

\[
 \sum_t H_t=H,\qquad \sum_t|H_t|=|H|,
 \tag{3}
\]

where absolute values are entrywise. No curvature bound on an arbitrary
original factorization is used.

If the graph has degeneracy at most \(w\), orient its edges with outdegree
at most \(w\) and write \(H=\operatorname{diag}(H)+B+B^T\).
For every vector \(v\), rowwise Cauchy--Schwarz gives

\[
 \||B|v\|_2^2
 \le w\sum_jv_j^2\sum_iH_{ij}^2
 \le w\|H\|_2^2\|v\|_2^2.
\]

Consequently

\[
 \||H|\|_2\le(1+2\sqrt w)\|H\|_2.
 \tag{4}
\]

Treewidth at most \(p-1\) implies degeneracy at most \(p-1\). To avoid
irrational algorithmic constants, use the rational bound

\[
 K=(2p+1)M\ge\||H|\|_2.
 \tag{5}
\]

The loose factor in (5) only changes the parameter function.

## 3. One interval label per coordinate

At a stage, coordinate \(i\) has one finite partition \(\mathcal I_i\)
of its current interval domain. A bag state chooses one interval for each
coordinate in the bag. Adjacent bags must choose the **same interval
label** for each shared coordinate. Running intersection then gives one
label \(I_i\) for every occurrence of \(i\).

This is stronger than requiring geometric intersection. The continuous
copies may still differ inside their common interval, but they cannot
walk through a chain of adjacent cells.

Let \(d_i\) denote the length of \(I_i\), and let \(B_t\) be their product
in bag \(t\), with midpoint \(m_t\). Define the affine lower model

\[
 \ell_t(z)=a_t(m_t)+\nabla a_t(m_t)^T(z-m_t)
                 -\tfrac18d_{V_t}^T|H_t|d_{V_t}.
 \tag{6}
\]

The exact quadratic Taylor identity gives, throughout \(B_t\),

\[
 0\le a_t(z)-\ell_t(z)
       \le\tfrac14d_{V_t}^T|H_t|d_{V_t}.
 \tag{7}
\]

Unlike an isotropic maximum-side bound, (7) does not charge every private
coordinate the width of a distant shared coordinate.

Fix a common center \(c\), which need only lie in the original box.
For a nonroot bag \(t\) with separator \(S_t\), set

\[
 \lambda_{t,i}=\sum_{s\in\operatorname{sub}(t):i\in V_s}
                       \partial_i a_s(c_{V_s}),\qquad i\in S_t.
 \tag{8}
\]

For each bag label assignment, its discrete local cost is

\[
 b_t(B_t)=\min_{z\in B_t}\left[
       \ell_t(z)-\lambda_t^Tz_{S_t}
          +\sum_{u\text{ child of }t}\lambda_u^Tz_{S_u}\right],
 \tag{9}
\]

omitting the own-separator term at the root. This is affine minimization
over a box: choose a minimizing endpoint in each coordinate, including
when the coefficient is zero.

Ordinary finite-state tree-decomposition DP minimizes the sum of (9),
requiring equality of separator labels. Call its minimum \(L\).
Every consistent original point has a feasible label assignment and
copies, for which all slope terms cancel and (6) is a lower bound.
Thus \(L\) is a valid lower bound on the current box problem.

## 4. An occurrence-free error inequality

For any configuration, let \(z^t\in B_t\) be its selected local points
and let \(\Phi\) be the sum of its local objective and slope terms.
Choose \(x_i\) from the highest bag containing \(i\). Then

\[
 |z_i^t-x_i|\le d_i
 \tag{10}
\]

at every occurrence. In particular, \(x\) is a feasible original point.

Expanding each bag quadratic around \(c\), the slope terms (8) telescope
with its linear Taylor terms. Their sum is exactly
\(\nabla F(c)^T(x-c)\), even if linear coefficients are large.
The remaining copy error is quadratic. Equations (3), (7), and (10)
give

\[
 F(x)-\Phi
 \le K\|x-c\|_2\|d\|_2+\tfrac34K\|d\|_2^2.
 \tag{11}
\]

For detail, the sum of model errors is at most \(K\|d\|^2/4\).
Writing each copy as \(x_{V_t}+\delta^t\), the other terms are bounded
by \(|x-c|^T|H|d+d^T|H|d/2\). This proves (11) directly;
there is no sum over the number of occurrences.

## 5. Coordinate grading and contraction

Let \(h>0\) and let \(\theta=2^{-\mu}\), \(\mu\ge1\).
Around \(c_i\), partition the central interval \([-h,h]\) into steps
\(\theta h\). On either side, partition each shell
\([2^rh,2^{r+1}h]\), \(r\ge0\), into steps
\(\theta2^rh\), then clip to the current coordinate domain.
Only intervals with positive length are retained. A singleton coordinate
domain can instead be kept as a single zero-width label.

Every resulting interval satisfies

\[
 d_i\le\theta(h+|x_i-c_i|)\qquad(x_i\in I_i).
 \tag{12}
\]

Put \(R=\|x-x^*\|\), \(C_c=\|c-x^*\|\). Since
\(\|d\|\le\theta(\sqrt n h+\|x-c\|)\), (11) implies, for
\(\theta\le1\),

\[
 F(x)-\Phi
 \le6K\theta R^2+6K\theta C_c^2+2K\theta n h^2.
 \tag{13}
\]

Indeed, the right side of (11) is at most
\(3K\theta\|x-c\|^2+2K\theta n h^2\), and
\(\|x-c\|^2\le2R^2+2C_c^2\).

For the analysis set \(\bar g=\min\{g,K\}\), and suppose the trial uses

\[
 \theta\le\bar g/(96K).
 \tag{14}
\]

The algorithm does not need to know \(\bar g\). If \(x\) is reconstructed
from a minimizing configuration, then \(\Phi=L\le F(x^*)\), because
all pruning below preserves the original optimizer. With
\(\delta=F(x)-F(x^*)\), growth and (13) give

\[
 \frac\delta{\bar g},\quad \|x-x^*\|^2
 \le \frac{C_c^2}{15}+\frac{n h^2}{45}.
 \tag{15}
\]

Start at the lower corner \(c_0\) with
\(h_0=\max_i(u_i-l_i)\), and use \(h_j=2^{-j}h_0\).
After stage \(j\), set \(c_j\) to its reconstructed minimizing point
and update a feasible incumbent value \(U_j\). Since
\(\|c_0-x^*\|^2\le n h_0^2\), (15) proves by induction

\[
 \|c_j-x^*\|^2\le n h_j^2,\qquad
 0\le U_j-F(x^*)\le\tfrac{13}{45}\bar g n h_j^2.
 \tag{16}
\]

The same calculation bounds the actual certificate gap:

\[
 0\le U_j-L_j\le\tfrac{13}{45}\bar g n h_j^2.
 \tag{17}
\]

To verify (17), use \(U_j\le F(c_j)\) in (13), and substitute
\(R^2\le13nh_j^2/45\) and \(C_c^2\le4nh_j^2\).

## 6. Exact conditional bounds prune the scale range

After the solve and incumbent update, compute, for every coordinate
interval label \(I\in\mathcal I_i\),

\[
 m_i(I)=\min\{\Phi:\text{the global label of coordinate }i\text{ is }I\}.
 \tag{18}
\]

These are exact DP min-marginals. A pass of messages in each direction on
the decomposition supplies each bag's conditional table; minimizing that
table over all other coordinates gives (18) at the highest bag for \(i\).
No enumeration of global label assignments is needed.

Discard only labels with \(m_i(I)>U_j\). A feasible original point whose
coordinate lies in a discarded label has objective at least \(m_i(I)>U_j\).
Every label containing an original optimizer survives. Replace the current
coordinate domain by the closed hull of its surviving intervals. This
preserves the optimizer and may harmlessly reinclude gaps between surviving
intervals. Save the conditional bounds as certificates for the cuts.

For any surviving label, (18) has a minimizing configuration with
\(\Phi\le U_j\). Apply (13), (16), and growth to its reconstructed point:

\[
 \|x-x^*\|^2\le\tfrac{61}{45}n h_j^2.
 \tag{19}
\]

The constant uses only the weaker bound
\((U_j-F(x^*))/\bar g\le n h_j^2\): rearrangement gives
\((16/15)(1+1/4+1/48)=61/45\).

For any \(y_i\) in that surviving interval, (12), (16), and (19) give

\[
 \begin{aligned}
 |y_i-c_{j,i}|
 &\le\|x-x^*\|+\|c_j-x^*\|+d_i\\
 &\le\left(\sqrt{61/45}+1\right)\sqrt n h_j
       +\theta\left(h_j+
            \left(\sqrt{61/45}+2\right)\sqrt n h_j\right)\\
 &\le7\sqrt n h_j.
 \end{aligned}
 \tag{20}
\]

Thus every coordinate's next domain lies within distance \(7\sqrt n h_j\)
of its new center. The labels of the minimizing configuration survive,
so the new center also belongs to the smaller box. With
\(h_{j+1}=h_j/2\), the shell radius ratio
is at most \(14\sqrt n\).

All cuts are sound for every positive choice of \(\theta\), including
choices that fail (14). Growth is used only to count surviving labels.
Excluded regions have saved lower bounds exceeding the incumbent at the
time of exclusion, hence exceeding every later incumbent. If a current
lower bound exceeds the incumbent, return the incumbent as the global
lower bound; otherwise the current lower bound is already global once
the saved cuts are included. This bookkeeping proves soundness without
trusting a guessed growth constant.

## 7. Why tensor grids now have an FPT count

The first grid has only \(O(\theta^{-1})\) intervals per coordinate,
because the initial side length is at most \(2h_1\). Every later grid,
by (20), has at most

\[
 Q=O\left(\theta^{-1}(1+\log(n+1))\right)
 \tag{21}
\]

intervals per coordinate. A bag table has at most \(Q^p\) states.
The logarithm's exponent does not become an input-length exponent:
for every \(n\ge1\),

\[
 (1+\log(n+1))^p\le A(p)n
 \tag{22}
\]

for some computable \(A(p)\). For example, use \(n=e^t\),
\(\log(n+1)\le t+\log2\), and maximize
\((1+\log2+t)^p e^{-t}\) over \(t\ge0\).

Local costs, upward messages, downward messages, backtracking, and all
min-marginals therefore take
\(f(p,\theta^{-1})\operatorname{poly}(I)\) rational arithmetic
operations per stage, with a uniform polynomial exponent. The degree of
a decomposition node contributes only to the total number of message
additions, not to a product of child-state counts.

The essential distinction is between a full coordinate grid with
\(O(I+q)\) shell levels and the certified restricted grid with
\(O(\log n)\) levels. Bounding only the full grid's product would not
prove (2).

## 8. Bit bounds, unknown growth, and exact output

Take a common denominator \(D\) for input coefficients and endpoints.
Its bit length is \(O(I)\). For a fixed dyadic \(\theta=2^{-\mu}\),
all interval endpoints and centers through stage \(j\) have denominator
dividing \(D2^{j+\mu}\). New grid endpoints are the previous center plus
integer multiples of \(\theta h_j\) or a larger dyadic shell step;
clipping keeps old domain endpoints. Corner minimization introduces no
new coordinate denominators. Evaluating rational quadratic and affine
expressions, summing messages, and comparing them consequently has
polynomial bit cost in \(I+j+\mu\), with an absolute exponent.

Since \(\bar g\le K\), (17) reaches accuracy \(2^{-q}\) after
\(O(I+q+1)\) stages. A dyadic \(\theta\) satisfying (14) can be chosen
with \(\theta^{-1}=O(\max\{1,K/g\})\).

To avoid supplying \(g\), run trials \(\theta=2^{-\mu}\), \(\mu=1,2,\ldots\),
by ordinary computation-step dovetailing, assigning trial \(\mu\) a
\(2^{-\mu}\) share of the simulation. Every trial's lower bounds, cuts,
and stopping test are valid. The first trial satisfying (14) finishes
within the bound above; its simulation overhead is another parameter-only
factor. A poor trial must be preemptible while constructing its tables,
rather than being allowed to finish an arbitrarily expensive stage first.
This proves the unknown-growth version of (2).

For exact output, use the existing polynomial-bit height bounds for an
optimal rational vector and value. Isolate the optimum value in the
certified interval, attempt bounded-denominator reconstruction near
\(c_j\), and accept only a feasible reconstructed vector whose objective
equals that isolated value. This is a sound stopping test for all trials.
In a trial satisfying (14), (16) gives the required coordinate accuracy
after polynomially many further stages, so the exact extension has the
same parameter dependence and an absolute polynomial exponent.

## 9. What the initial curvature-allocation question established

An independent exploration found a simple positive answer if several
factors per bag are allowed: a chordal PSD decomposition of \(H+MI\)
gives PSD bag-supported matrices \(P_t\), and

\[
 H=\sum_tP_t-\sum_iM e_ie_i^T.
\]

The separate singleton negative factors have total negative curvature
\(MI\). Also \(P_t\preceq p\operatorname{diag}P_t\) and
\(\sum_t\operatorname{diag}P_t\preceq2MI\). These facts can support
stronger convex models, but the algorithm above does not need this
decomposition.

The same exploration found that two superficially similar variants fail.
Requiring exactly one grouped matrix per original edge bag forces a
\(\sqrt m\) negative-part load at the hub of the normalized \(m\)-leaf
star. And independently weighted local shells can contain a low-weight
bridge bag whose wide shared-coordinate interval connects incompatible
high-weight copies. Exact shared labels avoid that bridge mechanism.

## 10. A simpler point-grid version, including integer coordinates

The parent exploration identified a simpler use of the same pruning
principle. Start from the corrected point-grid algorithm in the
[existing theorem](../geometric-dp/theorem.md), with coordinate upper
curvature \(L>0\). Its corrected objective is

\[
 G(y)=F(y)-\tfrac L8\sum_i\ell_i(y_i)^2,
\]

where \(\ell_i(v)\) is the largest adjacent interval length, excluding
unit intervals for integer coordinates. Shared point labels already give
exact consistency. No full-Hessian bound or copy analysis is needed.

Compute exact min-marginals \(m_i(v)=\min_{y:y_i=v}G(y)\). For each
adjacent interval \([a,b]\), the bound

\[
 q_i([a,b])=\min\{m_i(a),m_i(b)\}
 \tag{23}
\]

is valid for every feasible original point whose coordinate lies in that
interval. To prove this, use the existing independent-rounding proof
restricted in coordinate \(i\) to its endpoints \(a,b\). Every rounded
point has that coordinate equal to an endpoint, so its corrected objective
is at least (23). Retain intervals with \(q_i\le U\), and take their
hulls as above. Fixed coordinate domains are retained separately.

Here is an independent derivation of the range bound. Put
\(\bar g=\min\{g,L\}\), \(\kappa=L/\bar g\ge1\), and
\(B=\max\{1,4\kappa/11\}\le\kappa\). For
\(\theta^2\le1/(8\kappa)\) and \(\theta\le1/2\), the existing theorem
gives new-center error at most \(Bn h^2\), old-center error at most
\(4Bn h^2\), and incumbent gap at most \(7Ln h^2/8\).

A retained interval has an endpoint witness \(y\) with \(G(y)\le U\).
If \(R=\|y-x^*\|\), its correction satisfies

\[
 \bar gR^2\le\tfrac78Ln h^2+\tfrac14Ln h^2
             +\tfrac12L\theta^2(R^2+4Bn h^2).
\]

Rearranging gives

\[
 R^2\le\left(\tfrac65\kappa+\tfrac4{15}B\right)n h^2
       \le\tfrac{22}{15}\kappa n h^2.
 \tag{24}
\]

For a continuous interval, its length is at most
\(h+\theta\|y-c_{\rm old}\|\). Combining (24) with the old and new
center bounds puts the entire interval within distance
\(5\sqrt{\kappa n}\,h\) of the new center.

For an integer interval, length one must be handled separately because
its correction is zero. The valid range bound is

\[
 5\sqrt{\kappa n}\,h+1.
 \tag{25}
\]

This additive one causes no state-count loss: the integer grid count uses
the effective base step \(\max\{h,1\}\). A claim that every retained
integer interval shrinks to zero radius would be false.

There is also a simple sequential alternative to dovetailing. For a trial
\(\theta\), verify after pruning that every coordinate hull is within
\(5\theta^{-1}\sqrt n\,h\) of the new center, adding one for integer
coordinates. If this observable check fails, restart with \(\theta/2\).
If it passes, the next stage has only
\(O(\theta^{-1}(1+\log(n+1)))\) nodes per coordinate: in the geometric
count, the leading \(\theta\) cancels the range factor \(\theta^{-1}\).
The check is guaranteed to pass when
\(\theta^2\le1/(8\kappa)\). The existing theorem supplies a fixed
number of stages for each accuracy target. Thus even unsuccessful trials
have an FPT work bound, and their costs sum geometrically. The radius
check can be implemented with rational squared comparisons, after
subtracting the integer additive one when applicable.

The point-grid version therefore appears preferable as the main theorem:
its curvature assumption is weaker, its certificate is simpler, and it
covers mixed integer boxes using the established rounding argument. The
earlier sections remain useful as an independent derivation of why
conditional pruning resolves the tensor-grid count.

## Verification record

An independent agent checked the shared-label contraction, conditional
pruning, hull argument, logarithmic-power absorption, min-marginal work
count, and degeneracy estimate. It found no flaw in those steps. This was
a mathematical review, not a software test or a priority investigation.

The targeted command actually run was `python3 - <<'PY'`, containing an
inline exact-`Fraction` check of the point-grid version. It passed 18
continuous or integer quadratic instances, 90 pruning stages, 500
conditional-interval checks, and 1,495 enumerated grid assignments.
Checks covered the certified objective interval, the existing contraction
and gap constants, preservation of the known optimizer, and the new
continuous and integer retained-hull radius bounds. The two-coordinate
quadratics included both signs of a coupling and fractional interior
optimizers. Exhaustive assignment enumeration supplied reference
min-marginals; the script was not a tree-DP implementation or a runtime
benchmark.

No project-wide verification, CI inspection, external search, or
knowledge-base access was performed.
