# Approximation for indicator quadratics with a positive low-rank update

Date: 2026-09-27. Status: proof independently reviewed; external novelty
assessment pending. The spectral approximation construction is already in
the repository's [2026-09-12 DAG approximation-set theorem](../notes/research-20260912-dag-psd-approximation-set.md).
The additions here are retaining the minimum additive cost in each existing
dynamic-program state and applying that refinement to positive low-rank
indicator quadratics. These are applications and a modest extension of the
earlier theorem, not a new spectral approximation mechanism.

## One exact budget on the earlier DAG approximation set

Use the model and assumptions of the earlier theorem: an explicit finite
DAG, rational PSD prior \(K_0\), rational PSD edge matrices \(W_e\) of
fixed order \(p\), and path matrix \(K(P)=K_0+\sum_{e\in P}W_e\).
Give each edge an additional rational scalar cost \(a_e\), and put
\(a(P)=\sum_{e\in P}a_e\).

**Cost refinement.** For rational \(0<\varepsilon<1\), a family of paths
can be constructed in polynomial time in the input bit length and
\(1/\varepsilon\), for fixed \(p\), such that for every feasible path
\(P\), some returned path \(T\) satisfies

\[
 a(T)\le a(P),\qquad
 (1-\varepsilon)K(P)\preceq K(T)
                    \preceq(1+\varepsilon)K(P).        \tag{A}
\]

The costs can have either sign. In particular, imposing a single exact
budget \(a(P)\le A\) with a binary-encoded \(A\) requires no enlargement
of the graph by budget states.

**Proof.** In each state of the earlier construction, retain a path of
minimum exact rational cost instead of an arbitrary path. Every feasible
suffix appends the same cost to either prefix at that state. Therefore
minimum-cost replacement preserves an extension with no larger cost, by
induction over a topological order. The earlier spectral proof uses only
the equality of recorded state keys and the completed anchor-owner mask;
it is unchanged. For rank-zero paths, find a minimum-cost path in the
zero-matrix subgraph instead of an arbitrary path. Signed costs are harmless
in a finite DAG. At the end, deleting paths with cost above \(A\) preserves
a representative for every original path meeting the budget. Exact rational
cost additions and comparisons have polynomial bit complexity. This proves
(A). No graph state records the numerical budget. \(\square\)

This extends the earlier note's stated scope: a binary-encoded resource
budget need not have a polynomial-size graph expansion, but one scalar
budget can instead be handled by minimum-cost representatives. It does not
establish the same conclusion for two independently imposed exact budgets.

## Model and guarantees

Let \(D\) be a positive rational diagonal matrix,
\(U\in\mathbb Q^{n\times r}\), and \(b,c\in\mathbb Q^n\). The supplied
factorization is \(Q=D+UU^T\). Consider

\[
 V^*=\min\{x^TQx-2b^Tx+c^Tz:
          x_i(1-z_i)=0,\ z\in\{0,1\}^n\}.                 \tag{1}
\]

The activation costs may have either sign. There are no other constraints.
The activation set can include a zero continuous coordinate.

The strongest direct consequence concerns a budgeted version. For supplied
nonnegative rational costs \(a_i\) and budget \(A\ge0\), define

\[
 G^*=\max\{b_S^TQ_{SS}^{-1}b_S:\ \sum_{i\in S}a_i\le A\}.
                                                               \tag{B}
\]

**Budget theorem.** For fixed \(r\), problem (B) has a fully
polynomial-time approximation scheme: a support \(T\) satisfying the
budget exactly and

\[
 b_T^TQ_{TT}^{-1}b_T\ge(1-\varepsilon)G^*
\]

can be found in time polynomial in the binary input length and
\(1/\varepsilon\). A cardinality restriction can be imposed at the same
time by recording the count. In the statistical interpretation where
\(Q\) is a regression Gram matrix and \(b\) is its predictor-response
vector, the maximized quantity is the reduction in least-squares error
relative to the zero predictor. The guarantee is multiplicative for that
reduction, not for the residual least-squares error.

The budget is not discretized. The dynamic program keeps the support of
minimum exact rational cost at each state and removes final representatives
whose cost exceeds \(A\). Thus no pseudopolynomial dependence on the budget
occurs. The case \(n=0\) is immediate and is excluded in the construction
below.

One family, constructed from the cost vector and accuracy, works for every
budget \(A\ge0\) simultaneously. Sort its supports by exact cost and retain
the running maximum gain. The resulting finite step function approximates
the entire budget--gain curve within factor \(1-\varepsilon\), with a
feasible support witnessing each returned value. The family depends on the
cost vector; it is not a universal approximation for every cost vector.

The budgeted theorem maximizes \(g(S)\). It does not also preserve an
independent activation penalty \(c(S)\) in the objective: one minimum-cost
representative per state controls one scalar cost. In particular, it does
not establish an FPTAS for \(c(S)-g(S)\) subject to a separate budget
\(a(S)\le A\).

**Penalized theorem.** For fixed \(r\), rational
\(0<\varepsilon<1\), and rational input data, a feasible rational solution
to (1) with objective at most

\[
 V^*+\varepsilon B,\qquad B=\sum_{i=1}^n b_i^2/D_{ii},     \tag{2}
\]

can be computed in time polynomial in the input bit length and
\(1/\varepsilon\). The polynomial exponent depends on \(r\).
More precisely, the construction has at most \((n+r)^{r+1}\) branches,
each with a dynamic program on

\[
 \left(O\!\left(\frac{n^2(r+1)^2}{\varepsilon}\right)\right)^{(r+1)(r+2)/2}
\]

integer states at each of \(n\) stages. This is an additive approximation
scheme relative to the stated data scale. It is not a multiplicative
approximation of (1), whose optimum can be negative or zero, and is not a
fixed-parameter tractability claim in \(r\).

The construction also works with a cardinality upper bound, lower bound,
or specified cardinality on \(z\), by recording the activation count in
the dynamic program. It does not establish the same conclusion for arbitrary
matroid constraints.

## Fixed-support benefit as a Schur complement

Write \(d_i=D_{ii}\), and let \(u_i^T\) be row \(i\) of \(U\).
For a support \(S\), minimization over the continuous variables gives

\[
 x_S=Q_{SS}^{-1}b_S,\quad x_{[n]\setminus S}=0,
 \qquad V(S)=c(S)-g(S),\quad
 g(S)=b_S^TQ_{SS}^{-1}b_S.                              \tag{3}
\]

All quantities in (3) are rational. Set \(p=r+1\) and define rational
positive semidefinite matrices of order \(p\):

\[
 W_i=\frac1{d_i}
 \begin{pmatrix}u_i\\b_i\end{pmatrix}
 \begin{pmatrix}u_i\\b_i\end{pmatrix}^{\!T},\qquad
 K_0=\operatorname{diag}(I_r,0),\qquad
 K(S)=K_0+\sum_{i\in S}W_i.                              \tag{4}
\]

The upper left block of \(K(S)\) is
\(I_r+U_S^TD_S^{-1}U_S\). The Woodbury identity yields

\[
 g(S)=\sum_{i\in S}\frac{b_i^2}{d_i}
 -\left(\sum_{i\in S}\frac{b_i u_i}{d_i}\right)^T
 \left(I_r+\sum_{i\in S}\frac{u_i u_i^T}{d_i}\right)^{-1}
 \left(\sum_{i\in S}\frac{b_i u_i}{d_i}\right).
                                                               \tag{5}
\]

Equivalently, \(g(S)\) is the Schur complement of the upper left block,
and it has the variational form

\[
 g(S)=\min_{y\in\mathbb R^r}(y,1)^T K(S)(y,1).           \tag{6}
\]

Thus \(K(T)\succeq(1-\varepsilon)K(S)\) implies
\(g(T)\ge(1-\varepsilon)g(S)\). Notice that this implication concerns
the original coordinates in (4), even though the construction below works
in a different basis. Also,

\[
 0\le g(S)\le\sum_{i\in S}b_i^2/d_i\le B.              \tag{7}
\]

The matrix \(K(S)\) is positive definite whenever \(S\) contains an index
with \(b_i\ne0\): the fixed vectors \(e_1,\ldots,e_r\) span the first
\(r\) coordinates, and that selected vector adds a nonzero last coordinate.
If every selected \(b_i\) is zero, then \(g(S)=0\). The best such support
is obtained directly by selecting negative-cost indices among those with
\(b_i=0\), with a simple sort if a cardinality restriction is present.

## A polynomial family that preserves a small PSD matrix

The following specialization of the earlier DAG construction gives an
intermediate statement: it
returns a family \(\mathcal F\) of supports such that for every support
\(S\) with \(K(S)\succ0\), some \(T\in\mathcal F\) satisfies

\[
 c(T)\le c(S),\qquad
 (1-\varepsilon)K(S)\preceq K(T)
                    \preceq(1+\varepsilon)K(S).        \tag{8}
\]

If activation count is recorded, \(T\) has the same cardinality as \(S\).
The size of the family and the time to construct it have the bounds stated
above. In particular, these bounds do not involve the condition number of
\(K(S)\), the magnitudes of \(U\), or the reciprocals of the entries of
\(D\), except through their binary input lengths.

Subset selection is a layered DAG with an include and an exclude arc at
each item. The earlier result already constructs representatives preserving
\(K(S)\) in both PSD directions, including singular matrices. Applying
the cost refinement (A) proves (8) immediately. The following full-rank
specialization supplies a self-contained proof for the particular matrices
in (4). It uses an equivalent rational normalization and does not claim a
new normalization method.

For the proof only, write \(W_i=w_iw_i^T\) with
\(w_i=(u_i,b_i)/\sqrt{d_i}\), and regard \(K_0\) as the sum of the
\(r\) fixed rank-one atoms \(e_j e_j^T\). These vectors need not be
rational. The implemented algorithm uses only the rational atoms.

### Choosing an anchor matrix

Enumerate all sets \(J\) of \(p\) atoms among the \(n+r\) selectable
and fixed atoms. Retain sets whose sum \(A_J\) is positive definite.
For each retained set, call an atom \(W\) admissible if

\[
 \operatorname{tr}(A_J^{-1}W)\le p.                     \tag{9}
\]

Discard the branch if any fixed atom is inadmissible. In the remaining
branch, require the selectable atoms in \(J\) to be selected, and permit
only admissible selectable atoms.

Every target support \(S\) with \(K(S)\succ0\) is allowed in some
branch. To see this, choose a basis of maximum absolute determinant among
the generators present in \(K(S)\), and let \(H\) be its column matrix.
If \(w\) is any generator present in \(K(S)\), write \(a=H^{-1}w\).
Replacing column \(j\) of \(H\) with \(w\) multiplies its determinant
by \(a_j\). Maximality therefore gives \(|a_j|\le1\) for all \(j\).
Since \(A_J=HH^T\),

\[
 \operatorname{tr}(A_J^{-1}ww^T)=\|H^{-1}w\|^2\le p.
                                                               \tag{10}
\]

The fixed atoms and all atoms of \(S\) satisfy (9), and \(S\) includes
the selectable anchors. No maximum-volume basis needs to be computed: the
algorithm enumerates all choices, and this argument proves coverage.

### Rational normalization

Compute an exact rational factorization
\(A_J=L\Delta L^T\), where \(L\) is unit lower triangular and
\(\Delta\) is positive diagonal. For each diagonal entry \(\Delta_j\),
choose a positive integer power of two or its reciprocal \(s_j\) such that

\[
 1\le s_j^2\Delta_j<4.
\]

With \(R=\operatorname{diag}(s_j)L^{-1}\), this gives the rational
congruence

\[
 I_p\preceq R A_JR^T\prec4I_p.                         \tag{11}
\]

All rational factors and scales have polynomial encoding length. The
dimension is fixed, and rational elimination and powers-of-two comparisons
suffice; square roots are not computed.

For any admissible atom \(W\), (11) implies
\(R^TR\preceq4A_J^{-1}\), and therefore

\[
 \operatorname{tr}(RWR^T)\le
 4\operatorname{tr}(A_J^{-1}W)\le4p.                   \tag{12}
\]

Every entry of a positive semidefinite matrix has absolute value at most
its trace, so all transformed atom entries belong to \([-4p,4p]\).
For every allowed support \(S\),

\[
 R K(S)R^T\succeq R A_JR^T\succeq I_p.                 \tag{13}
\]

### Rounding and dynamic programming

Assume \(n\ge1\), and set \(\delta=\varepsilon/(pn)\).
For every admissible selectable atom, round each upper triangular entry
of \(R W_iR^T\) down to an integer multiple of \(\delta\). Store the
corresponding integer vector \(a_i\), of dimension
\(k=p(p+1)/2\). Its entries have absolute value at most
\(4p/\delta+1\).

A standard include-or-exclude dynamic program computes the minimum
activation cost for each attainable sum \(\sum_{i\in T}a_i\), respecting
the forced anchors. Store one realizing support at each state. Each stage
has at most

\[
 \left(2n(4p/\delta+1)+1\right)^k
 =\left(O(n^2p^2/\varepsilon)\right)^k                 \tag{14}
\]

states. Negative integer coordinates and negative activation costs do not
affect this finite, acyclic dynamic program. If a cardinality restriction
is wanted, also record the selected count, with an additional factor
\(n+1\). Forced anchors can be included at initialization or handled as
stages with only the include transition.

Fix an allowed target \(S\), and take the stored support \(T\) at its
final integer state. Then \(c(T)\le c(S)\). For each matrix entry, the
rounding remainder of a single atom belongs to \([0,\delta)\), including
when the entry is negative. Both support remainder sums lie in
\([0,n\delta)\); hence their difference has absolute value at most
\(n\delta\). The common fixed matrix cancels. Thus

\[
 \|R(K(T)-K(S))R^T\|_2\le p n\delta=\varepsilon.
                                                               \tag{15}
\]

Here the bound follows from the maximum absolute row sum of the symmetric
difference matrix. By (13),

\[
 (1-\varepsilon)R K(S)R^T
 \preceq R K(T)R^T
 \preceq(1+\varepsilon)R K(S)R^T.
\]

Congruence by \(R^{-1}\) proves (8). Collect the final representative
supports over all branches. This proves the claimed family construction.

## Completing the approximation proof

For the budget theorem, run (8) with \(c=a\). If an optimal budget-feasible
support \(S^*\) has positive benefit, it contains a nonzero \(b_i\), so
its matrix is positive definite. The representative \(T\) has
\(a(T)\le a(S^*)\le A\), and (6) gives
\(g(T)\ge(1-\varepsilon)g(S^*)\). When the optimal benefit is zero, the
empty support already proves the statement. If a cardinality restriction
excludes the empty support, retain the same-count representatives and
handle the zero-\(b_i\) class by choosing its cheapest support at each
allowed cardinality. This proves the budget theorem, including exact
feasibility. The algorithm evaluates all budget-feasible representatives
and returns the one with largest exact rational benefit. If cardinality
restrictions leave no feasible representative, report infeasibility.

For the penalized theorem, let \(S^*\) be an optimal support. If it has no
selected nonzero \(b_i\),
the separately generated support with minimum activation cost among the
zero-\(b_i\) indices is optimal within this class and is included.
Otherwise apply (8) and (6) to obtain a candidate \(T\) with

\[
 \begin{aligned}
 V(T)&=c(T)-g(T)\\
 &\le c(S^*)-(1-\varepsilon)g(S^*)\\
 &=V^*+\varepsilon g(S^*)
 \le V^*+\varepsilon B.
 \end{aligned}                                         \tag{16}
\]

Evaluate (3) exactly for every generated support and return the best.
Every candidate is feasible in the original indicator problem. Rational
linear algebra constructs the continuous variables with polynomial encoding
length. This establishes (2).

When all \(c_i\le0\), (16) also implies a multiplicative approximation
for the nonnegative maximization objective \(-V\):
\(-V(T)\ge(1-\varepsilon)(-V^*)\). For general positive activation costs,
cancellation between \(c(S)\) and \(g(S)\) prevents this conclusion.

## Two exact budgets do not admit the same FPTAS

The one-budget refinement has a sharp limitation even in the diagonal case.
Unless \(P=NP\), no FPTAS exists for maximizing \(g(S)\) subject to two
exact nonnegative additive budgets, even when \(Q=I\), \(b=\mathbf1\),
and hence \(g(S)=|S|\). This is the usual two-budget cardinality reduction;
no novelty is claimed for its hardness mechanism.

Take a cardinality-constrained SUBSET SUM instance with positive integer
weights \(a_i\), target \(B\), and required cardinality \(k\ge1\).
Choose an integer \(M>\max\{B,a_1,\ldots,a_n\}\). Impose

\[
 \sum_{i\in S}a_i\le B,\qquad
 \sum_{i\in S}(M-a_i)\le kM-B.                         \tag{17}
\]

All costs and budgets are nonnegative. Adding (17) yields \(|S|\le k\).
A feasible set has cardinality \(k\) exactly when its first weight sum
equals \(B\). Thus an algorithm with approximation parameter
\(\varepsilon=1/(2k)\) must output a set of cardinality \(k\) on every
YES instance and cannot do so on a NO instance. It would decide that
NP-complete problem in polynomial time.

For completeness, cardinality-constrained SUBSET SUM is NP-hard directly
from ordinary positive SUBSET SUM with \(n\) items: append \(n\) zero
weights, add one to all \(2n\) weights, require cardinality \(n\), and
increase the target by \(n\). Any original subset can be padded to
cardinality \(n\), and every cardinality-\(n\) solution has the required
original sum. The transformed weights are positive. This is weak hardness
and a no-FPTAS statement with exact budgets, not a strong-hardness claim.

## Greedy selection can fail within rank one

The budgeted theorem is not a consequence of a uniform guarantee for
ordinary greedy selection. Let \(L\ge2\), take

\[
 D=I_3,\quad u=(L,L,0)^T,\quad
 b=(1,-1,1/L)^T,
\]

and allow two selected items, all of unit cost. The singleton benefits are
\(g(\{1\})=g(\{2\})=1/(1+L^2)\) and
\(g(\{3\})=1/L^2\), so greedy selects item 3 first. Item 3 has no
quadratic coupling to the others, so greedy's final value is
\(1/L^2+1/(1+L^2)<2/L^2\). In contrast, the vector \((1,-1)\) is
orthogonal to the first two coordinates of \(u\), giving
\(g(\{1,2\})=2\). The greedy approximation ratio is below \(1/L^2\),
and tends to zero. This exact example illustrates complementary predictors;
it is not a new general result about greedy regression methods.

## Certified approximate low-rank matrices

Suppose a supplied surrogate \(\widetilde Q=D+UU^T\) satisfies

\[
 \alpha\widetilde Q\preceq Q\preceq\beta\widetilde Q,
 \qquad 0<\alpha\le\beta.
\]

Principal-submatrix restriction and inversion give
\(\widetilde g(S)/\beta\le g(S)\le\widetilde g(S)/\alpha\) for every support.
Consequently applying the budgeted scheme to \(\widetilde Q\) and
evaluating the returned support under \(Q\) gives ratio at least
\((\alpha/\beta)(1-\varepsilon)\) for the true budgeted benefit. Reoptimize the
continuous variables on that support using the actual \(Q\).

For example, if \(Q=\widetilde Q+E\) and
\(0\preceq E\preceq\delta D\), then
\(\widetilde Q\preceq Q\preceq(1+\delta)\widetilde Q\), giving ratio
\((1-\varepsilon)/(1+\delta)\). This is an elementary perturbation
consequence. The decomposition and spectral bounds must be supplied or
certified separately; their discovery is not covered by the theorem.

## A separate relative guarantee for ridge loss

For rational \(y\in\mathbb Q^r\), consider the positive objective

\[
 \|U^Tx-y\|^2+x^TDx
\]

under the same indicator constraints and one exact nonnegative budget.
Here the linear coefficient satisfies \(b=Uy\). On a support \(S\), the
optimal loss is

\[
 \ell(S)=y^T\left(I_r+\sum_{i\in S}u_i u_i^T/d_i\right)^{-1}y.
\]

Apply the cost-preserving spectral family to the \(r\)-dimensional
information matrix in parentheses. Inverse order gives
\(\ell(T)\le\ell(S)/(1-\eta)\) for its no-more-expensive representative.
Choosing \(\eta=\varepsilon/(1+\varepsilon)\) gives a
\((1+\varepsilon)\)-approximation of the minimum ridge loss, with the
budget satisfied exactly. Cardinality can again be recorded. With no
separate budget, the same argument applies to loss plus nonnegative
activation penalties by retaining the minimum penalty at each state:
\(c(T)+\ell(T)\le[c(S)+\ell(S)]/(1-\eta)\).

This is a direct inverse-criterion application of the earlier PSD theorem;
the ridge identity is established in the prior literature. It relies on
\(b=Uy\). A relative gain guarantee for arbitrary \(b\) does not imply a
relative residual-loss guarantee after subtracting the gain from a fixed
baseline. For \(r=0\), the response is empty and the minimum unpenalized
loss is zero; handle that case directly.

## Why this matters, and limits

The exact positive-rank-one hardness construction in the
[earlier note](../research-20260925/integer-structure-exploration.md)
allows extremely small decision gaps. The proved transfer shows
that fixed positive coupling rank still permits certified additive
approximation at a scale determined by the uncoupled quadratic benefit,
without requiring a condition-number bound or a coefficient-magnitude
bound. Under a budget, the same construction gives a multiplicative
guarantee for retained quadratic benefit with no budget violation. The
earlier spectral family supplies the matrix approximation; retaining
minimum activation cost at each state supplies exact budget feasibility.

The displayed polynomial has a large exponent even for modest rank. No
practical speedup is established, and no implementation of the full
general algorithm is claimed here. Its direct potential is as a structural
approximation result or a starting point for a more efficient low-rank
oracle. The scale \(B\) can greatly exceed the optimal improvement after
activation costs, so the guarantee may be weak when those quantities nearly
cancel. Finding a low-rank decomposition of a general matrix is a separate
problem. The perturbation transfer above applies when its spectral
inequalities are certified; finding and certifying a suitable surrogate
is outside the theorem's scope.

## Literature comparison

The [prior-art audit](sparse-psd-prior.md) compares the budgeted gain theorem
with Das--Kempe's regression FPTAS, Bienstock--Chen's structured indicator
approximation, sparse ridge formulations, fixed-dimensional matrix
selection, and one-exact Pareto approximation. The earlier local PSD
construction supplies the main mechanism; the present cost refinement is
small. No matching external theorem was found in the bounded search, which
does not establish novelty. This work is a useful application and extension,
not yet evidence of a substantially new approximation principle.

## Verification record

- An [independent adversarial reviewer](positive-update-spectral-approximation-review.md)
  checked the anchor coverage,
  rational normalization, signed rounding, minimum-cost state replacement,
  Schur-complement comparison, and polynomial bit complexity. No substantive
  gap was reported. Edge cases identified in that review are reflected above:
  only item atoms are rounded, \(n=0\) is separate, zero-\(b_i\) supports
  respect each allowed cardinality, and rational \(D,U\) are supplied.
- That reviewer ran an exact Python heredoc, retained verbatim in
  [the checker command](checks/positive_update_gram_review.sh), with
  [its captured output](checks/positive_update_gram_review.stdout.txt).
  All 602 support-representative comparisons passed across 86 branches,
  including 204 additional members of colliding-key groups. This checks
  the lower matrix inequality, cost preservation, and benefit comparison
  in the sampled cases. It does not implement or test the dynamic program,
  branch coverage, general dimension, or polynomial bit complexity.
- A separate [normalization review](positive-update-normalization-review.md)
  checked 250 rational SPD examples in dimensions one through five. Its
  exact command and output are retained in
  [the execution record](checks/positive_update_normalization_review.json).
  These checks establish the reported instances of the normalization
  identities, not the entire approximation theorem.
- Another [independent adversarial review](sparse-psd-review.md) checked the
  budget, cardinality, and ridge-loss consequences. Its command
  `python research-20260927/sparse_psd_review_check.py` passed 11 rational
  instances, 137 nonsingular support branches, 66 rounded-state collisions,
  and 20 representative replacements. This checker implements the rounded
  dynamic program on each target's selected maximum-volume branch and
  includes a cost of \(2^{40}\) without a budget-coordinate expansion.
  It is a finite review program, not a full implementation or a proof of
  the asymptotic complexity.
- The parent research agent ran the targeted command
  `python3 -B research-20260927/sparse_gain_boundary_check.py`. It passed
  972 exact two-budget SUBSET SUM reductions and 31 rank-one greedy examples
  with \(L=2,\ldots,32\), using independent rational Gaussian elimination
  for the support values. These finite checks test the displayed examples
  and reduction instances, not the complexity-theoretic conclusion by
  themselves.
- The earlier spectral theorem has a separate Lean development, described
  in its source note. This new minimum-cost refinement and the Schur-complement
  application have not been added to that Lean development.
- No project-wide verification or CI status inspection was performed for
  this note. The actual commands above were run by the named independent
  reviewers and parent agent; they were not rerun by the note's author.
  The dynamic-program checks and external literature comparison are
  recorded in the linked review and source audit.

The independent review is evidence of correctness, not a guarantee. External
priority remains unresolved, and the prior repository theorem substantially
limits any claim of originality for the construction itself.
