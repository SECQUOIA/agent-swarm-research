# A low-rank spectral-ball path with constant-expected-query states and hard readout

Status: New exact construction; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the algebra and query reductions; novelty priority still requires specialist review

## Main result

There is one sparse rank-\(r\) objective on one spectral-norm matrix ball
for which four resource measures separate on the same instance family:

1. every normalized primal central-point state, normalized central
   predictor state, and normalized canonical rank-\(r\) optimizer state is
   exactly the same state and has a heralded preparation using an expected
   \(O(1)\) raw coefficient queries;
2. estimating the optimum or a fixed finite central objective to additive
   error \(\epsilon\) has quantum and randomized query complexities
   \[
     \Theta\!\left(\min\{N,Ar/\epsilon\}\right),\qquad
     \Theta\!\left(\min\{N,(Ar/\epsilon)^2\}\right);             \tag{1}
   \]
3. returning a sufficiently accurate full classical optimizer on a
   balanced promise requires \(\Theta(rN)\) quantum or randomized raw
   coefficient queries; and
4. every primal path from the analytic center to an interior
   \(\epsilon\)-accurate point has distance
   \(\Omega(\sqrt r\log(Ar/\epsilon))\) in the
   standard spectral-ball metric, while the exact central path has
   effective rank at most \(r\) and matching movement
   \[
      \Theta\!\left(\sqrt r\,[1+\log(Ar/\epsilon)]\right)        \tag{2}
   \]
   in the nontrivial accuracy regime, independently of the ambient barrier
   parameter \(P\), which may be arbitrarily larger than \(r\).

These are **simultaneous, max-type statements**.  In particular, (1) or
the \(\Theta(rN)\) readout bound must not be multiplied by (2).  Formula
(2) is both the order of the exact central-path length and the
path-independent distance scale for this objective family in the explicit
standard primal barrier metric.  It yields a lower bound only for methods
whose moves have bounded Dikin norm in that metric.  It does not apply to
arbitrary barriers or unrestricted nonlocal algorithms.

## 1. Sparse rank-\(r\) family and access model

Fix integers \(N,r,P\) with \(1\le r\le P\), and put
\(q=\max\{P,r(N+1)\}\).  The first \(r(N+1)\) columns are labelled
\((i,j)\), where \(i\in[r]\) and \(j\in\{0,\ldots,N\}\); any remaining
columns are public zeros.  The input is a bit array
\(b=(b_{ij})_{i\in[r],j\in[N]}\), promised to have the same Hamming
weight \(h\) in every row.  Column \((i,0)\) is a public anchor.  For a
public scale \(A>0\), define
\[
 C_b={A\over2\sqrt{N+1}}\sum_{i=1}^r e_i
 \left(e_{(i,0)}^T+\sum_{j=1}^N(1+b_{ij})e_{(i,j)}^T\right).
                                                                    \tag{3}
\]
Thus \(C_b\in\mathbb R^{P\times q}\) has rank \(r\), exactly
\(r(N+1)\) nonzeros, column sparsity one, row sparsity \(N+1\), and a
public support pattern.  It can be extremely sparse relative to the
ambient \(Pq\) matrix when \(P\gg r\).

The **raw coefficient oracle** coherently maps
\(|i,j,z\rangle\mapsto|i,j,z\oplus b_{ij}\rangle\) for \(j\ge1\);
anchors are public.  One coefficient-value query and its inverse cost one
raw bit query each.  The support locations and \(A,N,r,P\) are public.
An oracle that returns exact row norms, the operator/Frobenius/nuclear norm,
the common singular value, or already normalized SQ metadata is strictly
stronger: any one of these quantities reveals \(h\) and destroys the
scalar lower bound.  The state-preparation result below is for a
raw-backed state-preparation procedure, not for a free norm oracle.

Consider
\[
       \min_{\|X\|_{\rm op}\le1}-\langle C_b,X\rangle,
       \qquad
       \phi(X)=-\log\det(I_P-XX^T)\quad(\|X\|_{\rm op}<1).       \tag{4}
\]
Thus the optimization problem uses the closed ball, while the explicit
barrier and central path live on its interior.  The barrier has parameter
\(P\).

## 2. Exact SVD, central path, and invariant state

Disjoint row supports and the equal-weight promise give
\[
 C_bC_b^T=\lambda_h^2\operatorname{Diag}(I_r,0),\qquad
 \lambda_h=Aw_h,qquad
 w_h={1\over2}\sqrt{1+{3h\over N+1}}\in[1/2,1].                 \tag{5}
\]
Consequently \(P_b=C_b/\lambda_h\) is a rank-\(r\) partial isometry.
The optimum of (4) is
\[
                         \operatorname{OPT}_b=-r\lambda_h=-Arw_h. \tag{6}
\]

Write
\[
                  \rho(z)={z\over1+\sqrt{1+z^2}}.
\]
The exact spectral-ball central-path formula gives
\[
                  X_b(\eta)=\rho(\eta\lambda_h)P_b.              \tag{7}
\]
Therefore, for every \(\eta>0\),
\[
 { |\operatorname{vec}X_b(\eta)\rangle}
       ={ |\operatorname{vec}C_b\rangle\over\|C_b\|_F},
 \qquad
 { |\operatorname{vec}\dot X_b(\eta)\rangle}
       ={ |\operatorname{vec}C_b\rangle\over\|C_b\|_F},       \tag{8}
\]
where a dot may denote either \(d/d\eta\) or \(d/d\log\eta\);
the omitted scalar is positive.  The canonical minimum-Frobenius optimizer
is \(P_b\), and its normalized Frobenius state
\(|\operatorname{vec}P_b\rangle/\sqrt r\) is the same state.  Other
optimizers can have arbitrary components on the inactive singular
subspaces, so the claim is deliberately about this canonical optimizer.

To prepare (8), start uniformly over the public active support.  Query the
bit and rotate an ancilla with amplitude \(1/2\) on an anchor or a zero bit
and amplitude \(1\) on a one bit.  Postselection succeeds with probability
\[
        {N+1+3h\over4(N+1)}=w_h^2\in[1/4,1].                    \tag{9}
\]
It follows that exact heralded preparation takes an expected constant
number of bit queries; constant-error preparation with bounded failure
probability also takes \(O(1)\) queries.  Classical rejection sampling
from the squared amplitudes has the same expected \(O(1)\) raw-query cost.
Thus this is an output-contract separation, not by itself a quantum-over-
classical sampling advantage.

There is also a right-hand-side-specific linear-solve statement.  At
\(X=xP_b\), direct differentiation along \(P_b\) gives
\[
 \nabla^2\phi(xP_b)[P_b]
       ={2(1+x^2)\over(1-x^2)^2}P_b.                             \tag{10}
\]
Hence the central predictor right-hand side and solution lie on a
one-dimensional Hessian-invariant ray: the effective condition number on the
reached Krylov subspace is one.  This does **not** say that the ambient
Hessian is well conditioned, that its block encoding is free, or that its
eigenvalue is public without learning \(h\).  It only makes the normalized
predictor state QLS-friendly in the exact instance.

## 3. Sharp scalar query law

From (5),
\[
 {3\over8(N+1)}\le {dw_h\over dh}
       \le {3\over4(N+1)}.                                      \tag{11}
\]
Thus additive \(\epsilon\) estimation of (6) is, up to universal
constants, additive estimation of the mean \(h/N\) to error
\(\delta=\epsilon/(Ar)\).  The equal-row promise does not make this easier:
for the lower bound restrict to inputs whose \(r\) rows are identical, and
for the upper bound query only the first row.  Standard approximate
counting and its polynomial lower bound yield, for
\(0<\epsilon\le cAr\) and constant success probability,
\[
 Q_2(\operatorname{OPT},\epsilon)
     =\Theta\!\left(\min\{N,Ar/\epsilon\}\right),
 \quad
 R_2(\operatorname{OPT},\epsilon)
     =\Theta\!\left(\min\{N,(Ar/\epsilon)^2\}\right).           \tag{12}
\]
The constants only determine where the trivial zero-query regime begins.
At \(\epsilon=O(Ar/N)\), both complexities saturate at \(\Theta(N)\).

This is not merely a boundary-optimum effect.  At the public finite
central parameter \(\eta_0=1/A\),
\[
       -\langle C_b,X_b(\eta_0)\rangle
             =-Ar\,w_h\rho(w_h).                                \tag{13}
\]
The derivative of \(w\mapsto w\rho(w)\) is bounded above and below by
positive universal constants on \([1/2,1]\).  Therefore (12) also holds,
up to constants, for estimating (13).  In contrast, receiving the
normalized state (8) alone does not reveal its missing classical norm.

## 4. Full classical output requires all hidden data

The scalar promise above may repeat one row.  For full-output hardness use
the different, balanced subpromise that \(N\) is even and every row is an
independent string of weight \(N/2\).  All scalar quantities in (5)--(7)
are then public; only the singular vectors remain hidden.

Let row \(i\) of a feasible output \(\widehat X\) be \(x_i^T\), and let
row \(i\) of \(P_b\) be \(v_i^T\).  If its objective gap is \(\tau\),
then \(\|x_i\|_2\le1\) and
\[
 \sum_{i=1}^r\|x_i-v_i\|_2^2
 \le2\sum_i(1-\langle x_i,v_i\rangle)
 ={2\tau\over\lambda_h}\le {4\tau\over A}.                   \tag{14}
\]
The anchor entry of each \(v_i\) equals
\(\alpha_h=(N+1+3h)^{-1/2}\), while a hidden entry equals either
\(\alpha_h\) or \(2\alpha_h\).  If
\[
                         \tau\le {A\over1024(N+1)},              \tag{15}
\]
then (14) makes every active-entry error at most
\(1/(16\sqrt{N+1})\le\alpha_h/8\).  Comparing hidden entry
\((i,j)\) with \(3/2\) times the returned anchor \((i,0)\) therefore
recovers \(b_{ij}\) with the correct sign for every coordinate.

For completeness, the quantum lower bound can be seen directly from the
adversary method.  On one weight-\(N/2\) row, use the adjacency matrix of
the Johnson graph \(J(N,N/2)\).  Its norm is \(N^2/4\); filtering on one
queried coordinate leaves a regular bipartite graph of norm \(N/2\).
For \(r\) rows, take the Kronecker sum of these adversaries.  Its norm is
\(rN^2/4\), while a query to one coordinate leaves norm \(N/2\).  Since
distinct inputs require distinct full outputs, the adversary ratio is
\(rN/2\).  Reading all coefficients is a matching upper bound.  Thus any
bounded-error quantum or randomized algorithm returning an explicit
classical matrix, or any classical representation from which all its active
entries can be recovered without further input queries, has raw query cost
\[
                              \Theta(rN).                         \tag{16}
\]
This is an information/readout theorem.  It does not apply to a single
copy of the quantum state (8), to sampling access, or to an implicit output
oracle whose later input queries are excluded from the accounting.

## 5. Matching path-independent and central-path movement

All \(r\) nonzero singular values equal \(\lambda_h=\Theta(A)\).  Hence
the exact squared speed with respect to \(d\log\eta\) is
\[
 r_{\rm eff}(\eta)
   =r\left(1-{1\over\sqrt{1+(\eta\lambda_h)^2}}\right).          \tag{17}
\]
The exact central objective error is
\[
                  E(\eta)=r\lambda_h[1-\rho(\eta\lambda_h)].    \tag{18}
\]
Integrating (17), or applying the rank-adaptive spectral-ball theorem,
shows that the central path from the analytic center to
\(E(\eta)\le\epsilon\) has length
\[
 L_{\rm P}=\Theta\!\left(
        \sqrt r\,[1+\log(Ar/\epsilon)]\right)                   \tag{19}
\]
for \(0<\epsilon\le cAr\), where \(c>0\) is a sufficiently small
universal constant.  Arclength checkpoints
give the same order of radius-\(R<1\) Dikin chords, with constants depending
only on \(R\).

This upper schedule is optimal even among noncentral feasible paths.  The
audited [active-principal-minor contraction
theorem](2026-09-04-spectral-ball-low-rank-objective-path.md#6-a-matching-path-independent-low-rank-lower-bound)
for the standard spectral-ball metric gives, for every interior feasible \(X\) with
objective error at most \(\epsilon\),
\[
 d_\phi(0,X)\ge\sqrt r
       \left[\log{r\lambda_h\over2\epsilon}\right]_+.           \tag{19a}
\]
Consequently, any sequence starting at zero with forward chords
\(\|X^{j+1}-X^j\|_{X^j}\le R<1\) and such an endpoint needs
\[
 T\ge {\sqrt r\over-\log(1-R)}
       \left[\log{r\lambda_h\over2\epsilon}\right]_+.           \tag{19b}
\]
Since \(\lambda_h\in[A/2,A]\), (19)--(19b) match up to universal and
\(R\)-dependent constants.  This is a path-independent lower bound for
bounded moves in the **fixed standard primal barrier metric**, not for
arbitrary self-concordant barriers or general quantum algorithms.

The ambient barrier parameter is \(P\), but the primal
path only resolves the \(r\) active singular directions.  In the conic
homogenization, the dual path carries the complementary squared speed
\(P+1-r_{\rm eff}\); (19) is deliberately a primal-slice statement.

For example, set \(A=N/r\) and keep \(r\) fixed.  Constant primal error
then gives \(O_R(\sqrt r\log N)\) central chords, constant-expected-query
normalized states, and \(\Theta(N)\) scalar readout.  Under the balanced full-output
promise, the accuracy in (15) is \(\Theta(1/r)\), also constant for fixed
\(r\), and the readout cost is \(\Theta(rN)\).  These costs coexist, but
no direct-product or temporal-hybrid argument has been proved; the correct
joint lower statement is their maximum, never their product.

## 6. Classical sparse linear algebra comparison

The family is intentionally transparent once its coefficients are read.
A classical scan of one row computes the common singular value and scalar
optimum in \(O(N)\) time.  Scanning all nonzeros constructs the exact compact
SVD \(C_b=\lambda_hP_b\), the central point (7), or a rank-factor/full
optimizer in \(O(rN)\) arithmetic and memory.  Direct row normalization is
already the relevant sparse SVD; an IPM is unnecessary.  Classical
squared-amplitude sampling also costs an expected constant number of raw
queries by (9).

Quantum approximate counting gives its usual quadratic advantage over
randomized scalar estimation only in the nonsaturated regime
\(1\ll Ar/\epsilon\ll N\).  At the fixed-accuracy scaling \(A=N/r\),
both scalar models saturate at \(\Theta(N)\).  The genuine message is not
an end-to-end quantum speedup: low effective-rank movement and easy quantum
state output can coexist with a hard classical norm, scalar, or full-output
contract, while elementary sparse classical linear algebra remains optimal
when explicit data are required.

## 7. A normalization-safe companion when rank may encode the bits

The exact-norm caveat is necessary for the fixed-rank family (3), because
\(\|C_b\|_F=\sqrt r\lambda_h\) and
\(\|C_b\|_*=r\lambda_h\).  If rank is allowed to grow with the hidden
string, a second construction removes that caveat while retaining the
state/readout separation.

Let \(k\ge1\), \(R=2k+1\le P\le q\), and put the following \(R\) entries
on the diagonal of an otherwise zero \(P\times q\) matrix:
\[
 D_b=A\operatorname{Diag}\left(2,
   (d_{\ell,1},d_{\ell,2})_{\ell=1}^k\right),
 \quad
 (d_{\ell,1},d_{\ell,2})=
 \begin{cases}
  (1,1),&b_\ell=0,\\
  (\sqrt{3/2},-1/\sqrt2),&b_\ell=1.
 \end{cases}                                                    \tag{20}
\]
This objective has exact rank \(R\), row and column sparsity one, public
support, and
\[
 \|D_b\|_F=A\sqrt{2k+4},\qquad \|D_b\|_{\rm op}=2A              \tag{21}
\]
for every input.  Its nuclear norm is
\[
 \|D_b\|_*=A[2+2k-dh],qquad
 d=2-{\sqrt3+1\over\sqrt2}>0,                                  \tag{22}
\]
where \(h=\sum_\ell b_\ell\).  Therefore, for
\(0<\epsilon\le cAk\), where \(c>0\) is a sufficiently small universal
constant, additive \(\epsilon\) estimation of the optimum
has the normalization-safe laws
\[
 Q_2=\Theta\!\left(\min\{k,Ak/\epsilon\}\right),\qquad
 R_2=\Theta\!\left(\min\{k,(Ak/\epsilon)^2\}\right).           \tag{23}
\]
At the public checkpoint \(\eta_0=1/A\), each zero bit contributes
\(A(2\sqrt2-2)\) to \(\langle D_b,X_{D_b}(\eta_0)\rangle\), where
\(X_{D_b}\) denotes the central path for objective \(D_b\), while each
one bit contributes
\(A(\sqrt{5/2}+\sqrt{3/2}-2)\).  Their positive difference
\[
             A\left(2\sqrt2-\sqrt{5/2}-\sqrt{3/2}\right)        \tag{24}
\]
is a positive universal constant times \(A\), so (23), after decreasing
\(c\) if necessary, also holds for this finite central objective.  Above a
constant fraction of the total \(\Theta(Ak)\) value range, a zero-query
estimate is possible and (23) is not asserted.

Every diagonal central or predictor amplitude is one of four public
magnitude functions of \(t=\eta A\), including the anchor, selected by one
bit.  A uniform-index, controlled-rotation construction therefore prepares
its exact normalized state with expected \(O(1)\) bit queries.  Indeed, the
coefficient scales lie in \([1/\sqrt2,2]\).  The maximum-to-minimum ratio is
bounded uniformly for all \(t>0\), both for \(\rho(st)\) and for
\(s\rho'(st)\): the ratios tend to ratios of \(s\)'s as \(t\downarrow0\),
to one for the central state as \(t\to\infty\), and to inverse ratios of
\(s\)'s for the predictor state as \(t\to\infty\).  Here
\(\rho'(z)=[\sqrt{1+z^2}(1+\sqrt{1+z^2})]^{-1}\), and continuity and
positivity cover the intervening compact range.  The canonical optimizer is the diagonal sign
matrix on the support, whose normalized state uses one phase query.
Moreover, if a feasible output has objective gap \(\tau<A/(4\sqrt2)\),
then \(|y_\ell|\le1\), every diagonal gap contribution is nonnegative,
and for every second entry \(y_\ell\),
\[
 b_\ell=0:\quad A(1-y_\ell)\le\tau,
 \qquad
 b_\ell=1:\quad {A\over\sqrt2}(1+y_\ell)\le\tau.
\]
Thus \(y_\ell>0\) in the first case and \(y_\ell<0\) in the second.  An
explicit classical optimizer therefore recovers all \(k\) bits and has
quantum and randomized query cost \(\Theta(k)\).

All \(R\) singular values lie in \([A/\sqrt2,2A]\).  Consequently, for
\(0<\epsilon\le c'AR\), where \(c'>0\) is a sufficiently small universal
constant, the same explicit standard-barrier central path has movement
\[
       \Theta\!\left(\sqrt R[1+\log(AR/\epsilon)]\right),       \tag{25}
\]
again independently of \(P\gg R\).  The geometric mean of these singular
values is exactly
\[
 \overline w_g=A\left[2\left({\sqrt3\over2}\right)^h\right]^{1/R}
 \in\left[{3^{1/4}\over\sqrt2}A,,2A\right].
\]
Thus the principal-minor theorem gives the matching path-independent
bounded-Dikin lower bound as in (19a)--(19b), with
\(r,\lambda_h\) replaced by \(R,\overline w_g\).  No positive lower
movement is asserted once the requested error is already achieved at the
analytic center.  Unlike (3), this variant remains scalar-hard when exact
Frobenius and operator norms are public and under charged SQ access:
coefficient and row-norm queries reveal at most the queried bit, and
squared-norm sampling first chooses the public anchor or one of the \(k\)
bit blocks with public probabilities \(2/(k+2)\) and \(1/(k+2)\),
respectively.  Conditional on a bit block, one bit query simulates its local
sample.  A charged normalized input-state preparation unitary and its
inverse are also exactly simulable with \(O(1)\) raw bit queries: prepare
the same public block weights, query the selected bit, rotate the local pair
to \((1,1)/\sqrt2\) or \((\sqrt3/2,-1/2)\), and unquery.  Therefore every
charged SQ call costs at most a constant number of raw queries, so the raw
approximate-counting and whole-string lower bounds transfer.  Its price is
exact in this construction: the number of hidden bits is \(k=(R-1)/2\), rather than
being arbitrarily larger than objective rank.

As before, (23), the full-output bound, and (25) are max-type statements,
not factors in one runtime lower bound.

## 8. Novelty boundary and references

The spectral-norm barrier, singular-value central path, approximate
counting bounds, adversary method, and quantum oracle interrogation are
classical ingredients.  See Nesterov--Nemirovskii, *Interior-Point
Polynomial Algorithms in Convex Programming* (1994), Chapter 6;
Brassard--Høyer--Mosca--Tapp,
*Quantum Amplitude Amplification and Estimation*, Contemporary Mathematics
305 (2002), arXiv:quant-ph/0005055; Nayak--Wu, *The Quantum Query
Complexity of Approximating the Median and Related Statistics*, STOC 1999,
doi:10.1145/301250.301349; Canetti--Even--Goldreich, *Lower Bounds for
Sampling Algorithms for Estimating the Average*, Information Processing
Letters 53 (1995), doi:10.1016/0020-0190(94)00171-T; Ambainis, *Quantum
Lower Bounds by Quantum Arguments*, JCSS 64 (2002),
doi:10.1006/jcss.2002.1826; and van Dam, *Quantum Oracle Interrogation*,
FOCS 1998, arXiv:quant-ph/9805006.  Van Dam supplies matching linear-order
whole-string interrogation context, not the lower bound used in (16).

Adjacent QIPM and output-contract work includes Dalzell et al., *Quantum
Algorithms: A Survey of Applications and End-to-End Complexities*, PRX
Quantum 4, 040325 (2023), which discusses optimization readout/tomography
bottlenecks; van Apeldoorn--Cornelissen--Gily\'en--Nannicini,
*Quantum tomography using state-preparation unitaries*, SODA 2023,
arXiv:2207.08800; and Chia--Li--Lin--Wang, *Quantum-inspired sublinear
classical algorithms for solving low-rank linear matrix equations with
polynomial dependence on the condition number*, arXiv:1901.03254.  The
latter uses sampling/query access, underscoring why the present raw-oracle
and norm/SQ distinction is material.

A targeted local and open-web search did not locate a direct prior instance
of this one-matrix-cone
synthesis: sparse rank-\(r\) coefficients, exact path-state invariance,
the sharp scalar and full-output query laws, the one-ray predictor solve,
and the effective-rank central schedule on the same family.  That synthesis
is the candidate contribution.  Priority and the precise strongest oracle-
interrogation comparison remain subject to specialist review.

## Independent hostile-audit result

The audit found no error after correcting the initial use of the open ball
as the optimization domain: the optimization problem must use
\(\|X\|_{\rm op}\le1\) for \(P_b\) to be an attained optimizer, while the
barrier lives on \(\|X\|_{\rm op}<1\).  The checks most likely to expose a
hidden scaling or oracle-model problem then gave:

- On one balanced row, \(J(N,N/2)\) has degree and norm \(N^2/4\).
  Filtering by coordinate \(j\) leaves an \(N/2\)-regular bipartite graph,
  hence norm \(N/2\).  For the Kronecker-sum adversary, all summands other
  than the queried row are killed by the filter, while the numerator norm
  is \(rN^2/4\).  The resulting adversary ratio is exactly \(rN/2\).
- Equation (15) implies total active Frobenius error at most
  \(1/(16\sqrt{N+1})\), hence each anchor and hidden-entry error is at most
  \(\alpha_h/8\).  In the comparison with \(3/2\) times the *returned*
  anchor, the perturbation is at most \((1+3/2)\alpha_h/8=5\alpha_h/16\),
  strictly below the true margin \(\alpha_h/2\).
- The map from the row mean to \(w_h\) is bi-Lipschitz at scale one because
  (11) holds throughout the full promise.  Restricting to identical rows
  exactly simulates one \(N\)-bit approximate-counting oracle, while one
  row supplies the matching upper bound.  This gives (12), including its
  \(N\)-query saturation regimes.
- Direct rectangular-matrix differentiation gives (10).  Since both the
  predictor right-hand side \(C_b\) and solution are multiples of \(P_b\),
  the reached Krylov subspace is exactly one-dimensional even though the
  ambient Hessian has additional eigendirections.
- Substituting \(z=\eta\lambda_h\) into the local speed gives each active
  contribution
  \(2\rho(z)^2/(1+\rho(z)^2)=1-(1+z^2)^{-1/2}\).  The terminal error requires
  \(z=\Theta(Ar/\epsilon)\), proving (19) in its stated nontrivial regime.
- The padding \(q=\max\{P,r(N+1)\}\) makes every matrix dimension valid
  without changing rank or the \(r(N+1)\) active coefficients.  Raw
  coefficient access supports both the heralded quantum preparation and
  classical rejection sampling at expected constant cost; exact norm or
  normalized-coordinate metadata would reveal \(h\) and is correctly
  excluded.  Reading one or all active rows gives the stated \(O(N)\) and
  \(O(rN)\) sparse classical baselines.  None of these query/readout costs
  is multiplied by the central-path movement.

The audit also changed “one-query” to “constant-expected-query”: a clean
state normally uses a bit query and its inverse on each heralding attempt,
and the success probability is bounded below by \(1/4\).  It clarified that
\(P_b\) is the canonical minimum-Frobenius optimizer rather than claiming
all boundary optimizers have the same state.  Novelty priority remains the
only unresolved issue.

### Audit of the normalization-safe companion

The later companion construction in Section 7 was separately checked:

- Each bit pair has squared norm exactly \(2A^2\), while the anchor has
  squared norm \(4A^2\), proving (21).  Its two possible nuclear
  contributions differ by
  \(Ad=A[2-(\sqrt3+1)/\sqrt2]>0\), proving (22)--(23) in the stated
  nontrivial accuracy regime.
- At \(\eta_0=1/A\), the identity
  \(s\rho(s)=\sqrt{1+s^2}-1\) gives the two checkpoint contributions in
  (24).  Their difference is approximately \(0.0225434A>0\).
- For scales \(s\in\{1/\sqrt2,1,\sqrt{3/2},2\}\), both
  \(\rho(st)\) and \(s\rho'(st)\) have a uniform maximum-to-minimum ratio
  for all \(t>0\).  This verifies constant expected postselection cost for
  both central and predictor states, including the limits \(t\downarrow0\)
  and \(t\to\infty\).
- A gap \(\tau<A/(4\sqrt2)\) makes every hidden second diagonal entry
  strictly positive for bit zero and strictly negative for bit one.  Hence
  explicit feasible output recovers the entire string and inherits the
  \(\Theta(k)\) oracle-interrogation bound.
- The exact public squared-norm sampling probabilities are \(2/(k+2)\)
  for the anchor and \(1/(k+2)\) for each bit block.  Entry, row-norm,
  sample, and normalized-state-preparation calls are each simulable using
  \(O(1)\) raw bit queries, including the inverse preparation unitary.
  Thus the charged-SQ lower-bound transfer is valid; it would not apply if
  a whole table of row norms or uncharged future queries were supplied.
- Since every singular value is within constant factors of \(A\), both
  the central movement and the principal-minor lower bound have order
  (25) for \(0<\epsilon\le c'AR\).  The explicit accuracy qualifications
  in (23) and (25) are necessary because sufficiently coarse accuracy has
  a zero-query or zero-movement solution.
