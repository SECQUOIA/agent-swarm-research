# Certified inexact oracles for regridded decomposition certificates

Date: 2026-10-02. Status: independently derived extension of
[the regridding theorem](note.md). A separate agent checked the slope-error
and gradient-incidence estimates. This note gives certified approximation
requirements and preserves the theorem's certificate and oracle-call counts;
it does not assume arbitrary convex functions have efficient evaluation or
optimization oracles.

## 1. Result

The regridding algorithm does not need exact local minimizers, exact bag
gradients, or exact incumbent objective values. It suffices to have:

- A certified lower bound and an exactly feasible approximate point for each
  local convex problem, with objective gap at most \(d h_j^2\).
- Approximate current-center slopes with aggregate error at most
  \(\zeta\sqrt N h_j\). Certified bag-gradient vector errors of order
  \(h_j\) suffice.
- A certified upper objective value at each reconstructed consistent point,
  with error at most \(\omega N h_j^2\).

Here \(d,\zeta,\omega\ge0\) are fixed constants, independent of the stage
and number of local problems. With a changed constant \(B\), the final box
count remains \(O(N(4/\theta)^p(J+1))\), total created boxes remain
\(O(N(4/\theta)^p(J+1)^2)\), and total convex-oracle calls remain
\(O(N3^p(4/\theta)^p(J+1)^3)\). The required local objective accuracy is
quadratic in the core width, not divided by the total number of solved
leaf-cell pairs.

The key distinction is that local solve errors accumulate through one chosen
problem per bag during backtracking. Unchosen problems affect which certified
lower bound is selected, but their errors are not added to that configuration.

## 2. Local oracle and the lower dynamic program

Use the continuous-box model of the main note and one approximate slope
\(\widehat\lambda_t\) per separator. At a fixed stage, all partitions and
slopes are fixed. Child messages already have certified intercepts
\(\widehat\beta_{u,D'}\).

For a bag leaf \(B\), define

\[
 b_{u,B}=\min\{\widehat\beta_{u,D'}:
                   D'\cap B_{S_u}\ne\varnothing\}.
\]

Store a minimizing child cell. For an own-separator cell \(D\) meeting
\(B_{S_t}\), let

\[
 C_{t,B,D}=\{v\in B:v_{S_t}\in D\},
\]

and define the convex local objective

\[
 q_{t,B,D}(v)=\sum_{a\text{ assigned to }t}f_{a,B_a}(v_a)
   +\sum_{u\in\operatorname{ch}(t)}
       [\widehat\lambda_u^Tv_{S_u}+b_{u,B}]
   -\widehat\lambda_t^Tv_{S_t}.                                \tag{1}
\]

At the root omit the incoming slope and separator cell. The oracle returns
rational numbers \(\ell_{t,B,D},u_{t,B,D}\) and a point
\(v_{t,B,D}\in C_{t,B,D}\) such that

\[
 \ell_{t,B,D}\le\min_{C_{t,B,D}}q_{t,B,D},\qquad
 q_{t,B,D}(v_{t,B,D})\le u_{t,B,D}
       \le\ell_{t,B,D}+\delta_{t,j}.                            \tag{2}
\]

The point must be actually feasible, not merely feasible to a numerical
tolerance. The inequalities are certified. The rational-number and rational-
point implementation is discussed in Section 7; the mathematical argument
also permits other exact representations satisfying (2).

Set

\[
 \widehat\beta_{t,D}=\min_{B:B_{S_t}\cap D\ne\varnothing}
                                      \ell_{t,B,D},
\]

and store an attaining leaf and its oracle point. At the root set
\(\operatorname{LB}\) to the minimum of its leaf lower bounds. The usual
child affine bound uses \(\widehat\lambda_u\) and \(b_{u,B}\).

All certificate inequalities remain valid. For every local pair, (2)
implies \(q(v)\ge\ell\ge\widehat\beta_{t,D}\) throughout its domain.
The child intercept minimum enforces the child-minorant condition. Bottom-up
validity therefore proves \(\operatorname{LB}\le f^*\) for any slopes,
partitions, and nonnegative error budgets. Maximal intercepts are unnecessary.

The child intercepts in (1) are exact rational constants once computed. A
convex solver can omit their sum from its numerical objective and add it
back exactly to both returned bounds. This prevents large inherited constants
from needlessly worsening a local absolute-accuracy request.

## 3. Backtracking adds one local error per bag

Backtrack from the root leaf with smallest reported lower bound. In a selected
bag-cell pair, use its stored feasible point and the stored child cells that
minimize \(b_{u,B}\), then repeat in each child.

The result is a valid configuration: each point belongs to its bag leaf and
own separator cell; each selected child cell meets the selected parent leaf.
Denote its value with the approximate slopes by

\[
 \widehat\Phi=\sum_t\sum_{a\text{ assigned to }t}
                   f_{a,B_{t,a}}(z_a^t)
    +\sum_{t\ne r}\widehat\lambda_t^T
                   (z^{p(t)}_{S_t}-z^t_{S_t}).                  \tag{3}
\]

Then

\[
 0\le\widehat\Phi-\operatorname{LB}
                  \le\sum_t\delta_{t,j}.                       \tag{4}
\]

For the upper bound, define a subtree configuration value by including its
internal slope terms and subtracting its incoming slope at its own bag
point. Induction gives that this value is at most
\(\widehat\beta_{t,D}+\sum_{u\in\operatorname{sub}(t)}\delta_{u,j}\).
At the selected point, (2) first pays \(\delta_{t,j}\). Replacing each
child intercept by its backtracked subtree contribution then pays the child
induction errors. Every bag occurs exactly once. At the root this proves
the upper half of (4). The lower half follows by applying the valid local
certificate inequalities along any configuration and telescoping them.

In particular, imposing \(\delta_{t,j}\le d h_j^2\) for every task of
bag \(t\) gives \(\widehat\Phi\le\operatorname{LB}+dNh_j^2\).
There is no factor equal to the number of cells, leaves, touching pairs,
or convex-oracle calls. Lower-bound errors in child tables are already
included through this same induction and must not be counted a second time.

## 4. Approximate slopes

Retain the notation of the main note:

\[
 C_0=k(k-1)p,\quad \eta=g/20,\quad
 Q=\sum_t b_t^2+\sum_{t\ne r}d_t^2,\quad R=\|x-c\|.
\]

Here \(d_t\) denotes separator width, as in the main note, while \(d\)
without a subscript is the local-solve error constant. Define

\[
 C_1=2p\max\{k-1,1\},\qquad
 \nu^2=\sum_{t\ne r}\|\widehat\lambda_t-\lambda_t(c)\|^2.
\]

The sum of squared edge copy differences satisfies

\[
 H:=\sum_{t\ne r}\|z^{p(t)}_{S_t}-z^t_{S_t}\|^2\le C_1Q.        \tag{5}
\]

Indeed an edge difference in any separator coordinate is at most
\(b_{p(t)}+d_t\). For a parent bag,
\(\sum_{u\in\operatorname{ch}(t)}|S_u|\le(k-1)|V_t|\), because
each of its coordinates occurs in at most \(k-1\) additional child bags.
Consequently

\[
 H\le2p(k-1)\sum_t b_t^2+2p\sum_{t\ne r}d_t^2\le C_1Q.
\]

No maximum branching factor appears. When \(k=1\), all separators are
empty and the actual quantities \(H\) and \(\nu\) are zero.

Let \(\Phi\) denote the same configuration value with exact current-center
slopes. Cauchy--Schwarz and the main note's grading bound give

\[
 |\widehat\Phi-\Phi|\le\nu\sqrt{C_1Q},\qquad
 Q\le12Nh_j^2+12k\theta^2R^2.
\]

Assume \(\nu\le\zeta\sqrt N h_j\). Young's inequality, with
\(R^2\) budget \(\eta/4\), then yields

\[
 |\widehat\Phi-\Phi|\le(\eta/4)R^2+K_sNh_j^2,
\quad
 K_s=\sqrt{12C_1}\,\zeta+\frac{12kC_1\zeta^2\theta^2}{\eta}.    \tag{6}
\]

Adding a full extra \(\eta R^2\) to the main estimate would leave
contraction factor \(1/4\), which is insufficient for its constant-times-
\(h_j^2\) induction when \(h_j\) halves. The smaller allocation in (6)
preserves a strict contraction margin.

### Certified bag gradients are sufficient

Let \(e_t=\widehat g_t-\nabla a_t(c_{V_t})\) be bag-gradient errors, and
form approximate separator slopes by the same subtree sums as for exact
gradients. Then

\[
 \nu^2\le G\sum_t\|e_t\|^2,\qquad G=k(k-1)/2.                  \tag{7}
\]

For each coordinate, the occurrence bags form a rooted tree of size at most
\(k\). The matrix mapping bag-gradient errors to subtree-slope errors has
a one for each descendant bag below an occurrence-tree edge. Its squared
Frobenius norm is the sum of occurrence depths, at most \(k(k-1)/2\).
Apply this bound coordinate by coordinate and sum.

Thus per-bag vector errors \(\|e_t\|\le\gamma h_j\) imply the required
slope budget with \(\zeta=\sqrt G\,\gamma\). Componentwise errors at
most \(\gamma h_j/\sqrt p\) suffice. If \(k=1\), no gradient accuracy
condition is needed for this perturbation. Approximate arithmetic in the
subtree sums must also be included in \(\nu\); exact sums of rational
gradient approximations avoid that extra error.

## 5. Contraction and termination with certified upper evaluations

Keep the original conditions on \(\theta\) and the original constant

\[
 C=12B_0+6kC_0M^2/\eta.
\]

Suppose the incumbent evaluator returns \(U_j\) satisfying

\[
 F(x^{(j)})\le U_j\le F(x^{(j)})+\omega Nh_j^2.
\]

Maintain the minimum of these certified feasible upper values. Define

\[
 K=C+K_s+d+\omega,
 \qquad B_{\rm in}=\max\{p,8K/(3g)\}.                          \tag{8}
\]

Then every stage satisfies

\[
 \|x^{(j)}-x^*\|^2\le B_{\rm in}Nh_j^2,
 \qquad
 0\le\operatorname{UBD}-\operatorname{LB}_j
                    \le gB_{\rm in}Nh_j^2.                    \tag{9}
\]

To prove this, the exact-current-slope estimate of the main note, (4), and
(6) give

\[
 F(x^{(j)})-\operatorname{LB}_j
       \le(g/16)\|x^{(j)}-x^{(j-1)}\|^2
                         +(C+K_s+d)Nh_j^2.                    \tag{10}
\]

Use \(\operatorname{LB}_j\le f^*\), quadratic growth, and
\(\|x^{(j)}-x^{(j-1)}\|^2\le2(e_j+e_{j-1})\). With the larger
constant \(K\) from (8), this gives

\[
 e_j\le e_{j-1}/7+(8K/(7g))Nh_j^2.                             \tag{11}
\]

The induction with \(h_{j-1}=2h_j\) closes because
\(4B_{\rm in}/7+8K/(7g)\le B_{\rm in}\). At stage zero use
\(e_{-1}\le pNh_0^2\) and (8). This proves the distance bound.

The center difference is at most \(10B_{\rm in}Nh_j^2\), including
the weaker bound needed at stage zero. Adding incumbent evaluation error
to (10) gives

\[
 \operatorname{UBD}-\operatorname{LB}_j
 \le[5gB_{\rm in}/8+K]Nh_j^2\le gB_{\rm in}Nh_j^2.
\]

Therefore termination occurs no later than

\[
 J=\max\{0,\lceil\log_2(s_0\sqrt{gB_{\rm in}N/\varepsilon})\rceil\}.
\]

The stopping test is sound even in trials whose grading ratio is too large:
valid lower certificates and certified feasible upper values do not depend
on the convergence restrictions. Fixed positive budgets \(d,\gamma,\omega\)
can be chosen without knowing \(g\); the proof constants absorb their ratios
to \(g\). Thus the main note's unknown-constant schedule still terminates,
provided each requested oracle call terminates.

## 6. Counts and what is certified

The partitions, incidence lists, and number of convex problems are unchanged.
Replace \(B\) by \(B_{\rm in}\) in the main note's stage bound. Final
leaves plus cells remain at most
\(2N(4/\theta)^p(J+1)\), and total local convex calls remain at most

\[
 N3^p(4/\theta)^p(J+1)(J+2)(2J+3)/6.
\]

Each local call requests a gap of order \(h_j^2\), and each bag gradient
requests error of order \(h_j\). Thus required accuracy in bits grows
linearly with the stage, in addition to input-dependent scale terms.
This does not bound the internal runtime of a local oracle.

The leaf-plus-cell count remains the established certificate size measure.
A serialized certificate that includes separate local lower-bound proofs
for every touching pair may contain more proof objects, following the pair
count, and numerical entries have their own bit lengths. No bound on those
extra sizes follows merely from counting boxes.

## 7. Exact feasibility and rational reconstruction

For a rational implementation, assume the original box, initial center,
\(h_j\), and grading parameters have rational representations, and that
shell construction preserves rational endpoints. Require each oracle point
in (2) to be rational. The consistent point takes coordinate \(i\) from
its top bag copy, so it is rational and lies exactly in the original box.
The next center and its fresh partitions therefore remain rational.

A local domain \(C_{t,B,D}\) is the coordinatewise intersection of rational
boxes. Determine emptiness by exact endpoint comparison. Touching pairs can
produce lower-dimensional faces: coordinates with equal lower and upper
endpoints must be fixed to that exact rational value and eliminated before
calling a solver on the remaining free coordinates. If all coordinates are
fixed, the task is certified function evaluation at one rational point.

Blindly rounding a floating-point minimizer can leave such a face even when
its displacement is arbitrarily small. A safe procedure constructs the final
rational point coordinate by coordinate inside the exact intervals, preserving
fixed coordinates exactly, and certifies its objective upper bound *after*
this reconstruction. It accepts the point only when the final bound satisfies
(2). Projecting a rational approximate vector onto these intervals by exact
clipping also guarantees feasibility; it does not by itself certify the
objective gap.

If a local objective has a supplied Lipschitz constant \(L_q\) on its
relative box, rounding one feasible point to another with coordinate
displacement at most \(\tau\) changes its value by at most
\(L_q\sqrt p\,\tau\). Concretely, start from a feasible point with a
certified upper value \(u_0\) satisfying \(u_0-\ell\le\delta_{t,j}/2\).
Choose a rational \(K_q\ge L_q\sqrt p\), construct the rational feasible
point within coordinate displacement \(\tau\), and transport the upper
value as \(u_{\rm new}=u_0+K_q\tau\). For \(K_q>0\), taking
\(\tau\le\delta_{t,j}/(2K_q)\) ensures the final certified gap is at
most \(\delta_{t,j}\). When \(L_q=0\), reconstruction incurs no
objective error. If the reconstructed point is freshly evaluated instead,
its evaluation uncertainty must fit the remaining gap budget, and the final
certified upper value must still satisfy (2).
This is a sufficient quantitative condition, not an assumption implied by
the original vertex-vanishing relaxation-error bound. Without such a modulus,
the oracle must certify the final point and gap directly.

No general polynomial bit-complexity claim is made for arbitrary supplied
convex functions. Such a claim requires an explicit representation with
certified lower-bound, feasible-point, value, and gradient routines; bounds
on their precision and runtime; and bounds on numeric entries in partitions
and messages. For particular LP or convex quadratic relaxations, primal
feasibility and a certified dual lower bound are natural ways to realize (2).
For other relaxations those requirements remain part of the oracle model.
Similarly, real or irrational domain endpoints need an appropriate exact
representation; a rational point cannot satisfy an irrational fixed
coordinate.

## 8. Verification status

The lower-DP and backtracking induction, error-budget contraction, and rational
face reconstruction were checked directly against the certificate definition.
A separate agent independently derived (5)--(7), including the absence of a
branching factor and the need to retain a strict contraction margin. That
agent then checked the written lower-DP induction, final constants, and
rational reconstruction conditions; no substantive error was found. A
targeted inline Python scan found and removed one control character in a
displayed fraction. No executable mathematical experiment or project-wide
verification was run for this note.
