# A matching full-SQ lower bound for sparse inverse quadratic forms

Status: Proved; independently audited; targeted literature screen completed  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the reduction; moderate on novelty because the main
matrix-function lower bound is prior work

## Main theorem

Fix \(\kappa\geq4\), sparsity \(s\geq5\), and
\(0<\epsilon\leq\epsilon_0\) for a sufficiently small constant
\(\epsilon_0\).  There is a real symmetric positive definite matrix
\(H\) with

\[
 \kappa^{-1}I\preceq H\preceq I,\qquad
 \kappa(H)=\kappa,                                         \tag{1}
\]

and two public two-sparse unit vectors \(b_+,b_-\), such that the following
task has randomized classical query complexity

\[
 \boxed{
 \Omega\!\left(
 \frac{
 ((s-1)/2)^{\,\Omega(\sqrt\kappa\log(1/\epsilon))}
 }{
 \log(s)\sqrt\kappa\log(1/\epsilon)
 }
 \right).}                                                 \tag{2}
\]

The task is to return relative-\(\epsilon\) estimates of both positive
inverse quadratic forms

\[
 q_\pm=b_\pm^TH^{-1}b_\pm.                                 \tag{3}
\]

The lower bound survives full sampling-and-query access to \(H\), including
entry and sparse-location queries, row and column norm queries, conditional
sampling inside any row or column, global squared-entry sampling, and the
Frobenius norm.  It also survives exact \(SQ(b_\pm)\), which is public and
constant cost.

Equivalently, any classical algorithm promised an arbitrary \(s\)-sparse
SPD Newton matrix and \(SQ(b)\), and required to estimate
\(b^TH^{-1}b\) relatively for every input \(b\), needs

\[
 \exp\!\left(
 \Omega(\sqrt\kappa\log s\log(1/\epsilon))
 \right)                                                   \tag{4}
\]

queries up to the displayed polynomial factor.  Together with the companion
upper bound, this closes the exponential dependence on conditioning,
sparsity, and relative accuracy for the scalar inverse-quadratic contract.

Moreover, the same matrix is the analytic-center Hessian, up to a factor two,
of a sparse box LP whose constraint matrix also has constant-hidden-query
full SQ.  Thus (2) is a genuine sparse-LP Newton-decrement lower bound, not
only a black-box SPD-system statement.  The box barrier has parameter
\(\Theta(N)\); the constant-barrier affine-slice LP and the one-cone SOCP
notes isolate different structural tradeoffs.

There is also a finite-input strengthening.  If \(\kappa\) and \(\epsilon\)
are rational, then the public clock weights can be chosen dyadic with
\(O(\log(\kappa/\epsilon))\) fractional bits.  For every \(s\geq9\), choosing
the Hadamard block size to be the largest power of four allowed by \(s\)
makes the whole hard matrix rational while changing the base in (2) only
from \((s-1)/2\) to \((s-1)/8\).  The box-LP constraint matrix can likewise
be made exactly rational.  This statement is nonuniform in the public
table; a terminating uniform generator exists, but no polynomial-time or
numerically stable generator is established below.

## Step 1: normalized reciprocal and its exact approximate degree

Put

\[
 a=\kappa^{-1},\qquad
 m=\frac{1+a}{2},\qquad
 h=\frac{1-a}{2},
\]

and define the bounded continuous function

\[
 f_\kappa(x)=\frac{a}{m+hx},\qquad -1\leq x\leq1.           \tag{5}
\]

It takes values in \([a,1]\).  Let

\[
 \rho=\frac{\sqrt\kappa-1}{\sqrt\kappa+1}.                 \tag{6}
\]

The exact best degree-\(n\) uniform approximation error for
\(f_\kappa\), for \(n\geq1\), is

\[
 E_n(f_\kappa)
 =\frac{\kappa-1}{2\kappa}\rho^{\,n}.                      \tag{7}
\]

Indeed, the classical best-approximation formula for \(1/x\) on
\([a,1]\) is

\[
 E_n(1/x)
 =2\rho^{\,n-1}
 \left[\frac12\left(\frac1{\sqrt a}-1\right)\right]^2,
\]

and multiplication by \(a\) gives
\[
 \frac{(\sqrt\kappa-1)^2}{2\kappa}\rho^{\,n-1}
 =\frac{\kappa-1}{2\kappa}\rho^n.
\]
For \(\kappa\geq4\), the prefactor in (7) lies between \(3/8\) and \(1/2\),
while

\[
 \log(1/\rho)
 =\log\frac{\sqrt\kappa+1}{\sqrt\kappa-1}
 =\Theta(\kappa^{-1/2}).                                   \tag{8}
\]

Consequently,

\[
 \widetilde{\deg}_\tau(f_\kappa)
 =\Theta(\sqrt\kappa\log(1/\tau))                          \tag{9}
\]

uniformly for \(0<\tau\leq\tau_0\).  Formula (7), rather than only a
one-sided Chebyshev construction, is useful here because the lower reduction
depends on approximate degree.

## Step 2: the Montanaro--Shao entry lower

Montanaro and Shao prove that, for any continuous
\(f:[-1,1]\to[-1,1]\) and any \(d\geq4\), there is a real
\(d\)-sparse symmetric matrix \(A\), with \(\|A\|\leq1\), and two
computational-basis indices \(i,j\), such that estimating

\[
 e_i^Tf(A)e_j
\]

to additive error \(\tau/4\) needs

\[
 \Omega\!\left(
 \frac{
 (d/2)^{(\widetilde{\deg}_{2\tau}(f)-1)/6}
 }{
 \log(d)\widetilde{\deg}_{\tau}(f)
 }
 \right)                                                   \tag{10}
\]

randomized classical sparse-oracle queries.  Apply their theorem to
\(f=f_\kappa\).  Equations (9)--(10) give the exponential term in (2).

The hard matrix in their proof is a weighted Feynman clock

\[
 A=\sum_t\beta_t\left(
 |t\rangle\langle t-1|\otimes U_t+
 |t-1\rangle\langle t|\otimes U_t^T
 \right),                                                  \tag{11}
\]

where the weights \(\beta_t\) are public and the gates \(U_t\) are public
block Hadamards or hidden diagonal sign gates from Forrelation.

## Step 3: affine shift to an SPD inverse

Define

\[
 H=mI+hA.                                                   \tag{12}
\]

Then

\[
 aI\preceq H\preceq I,\qquad
 f_\kappa(A)=aH^{-1}.                                      \tag{13}
\]

The condition number in (13) is at most \(\kappa\).  To make it exactly
\(\kappa\), take a direct sum with two public scalar blocks \(A=-1\) and
\(A=1\) before applying (12).  This adds no hidden information, changes
neither the hard matrix element nor the asymptotic sparsity, and supplies
eigenvalues \(a\) and \(1\).

The shift adds one diagonal entry per row.  Thus if the Montanaro--Shao
matrix has sparsity \(d\), then \(H\) has sparsity at most \(s=d+1\).

## Step 4: polarization turns an entry into two positive decrements

Their construction is real, and \(i\neq j\).  Set

\[
 b_+=\frac{e_i+e_j}{\sqrt2},\qquad
 b_-=\frac{e_i-e_j}{\sqrt2}.                               \tag{14}
\]

Both vectors have an exact public \(SQ\) interface.  Polarization gives

\[
 \frac a2(q_+-q_-)
 =a\,e_i^TH^{-1}e_j
 =e_i^Tf_\kappa(A)e_j.                                    \tag{15}
\]

Since the spectrum of \(H^{-1}\) lies in \([1,\kappa]\),

\[
 1\leq q_\pm\leq\kappa.                                   \tag{16}
\]

Suppose a decrement routine returns
\(|\widehat q_\pm-q_\pm|\leq\epsilon q_\pm\).  After constant success
amplification, run it for both signs and output

\[
 \widehat z=\frac a2(\widehat q_+-\widehat q_-).
\]

Equations (15)--(16) imply

\[
 |\widehat z-e_i^Tf_\kappa(A)e_j|
 \leq\frac a2\epsilon(q_++q_-)
 \leq\epsilon.                                             \tag{17}
\]

To match the accuracy convention in (10) exactly, set its parameter to
\(\tau=4\epsilon\).  Then (17) supplies the required additive error
\(\tau/4\), while (7)--(9) give
\(\widetilde{\deg}_{2\tau}(f_\kappa),
\widetilde{\deg}_{\tau}(f_\kappa)
=\Theta(\sqrt\kappa\log(1/\epsilon))\).  This proves (2), after changing
only universal constants.
The subtraction in (15) does not create an overlap assumption: each oracle
call is required only to estimate a positive quadratic form relatively, and
their public upper bound \(\kappa\) makes the propagated additive error
explicit.

## Step 5: why the prior lower survives full matrix SQ

The published theorem is stated for the standard sparse-location/value
oracle.  Its particular Forrelation clock has a stronger property.  In row
\((t,x)\), the nonzero blocks are weighted by the public adjacent clock
weights \(\beta_t\).  A block-Hadamard transition has a public support and
all nonzero magnitudes equal; a hidden diagonal transition has one public
location and a magnitude independent of its hidden sign.  Therefore:

- every row and column squared norm is a public function of the clock index;
- conditional squared-entry sampling chooses a public adjacent clock block
  and is then either uniform on a block-Hadamard support or deterministic;
- a sampled or queried value uses at most one hidden sign query;
- global row, column, or squared-entry sampling first samples a clock index
  from an \(O(T)\)-element hardwired public distribution and then samples the data
  index uniformly; and
- the Frobenius norm is an explicit public sum of the clock weights.

The diagonal term in (12) has disjoint support from the clock transitions,
so it is incorporated by one additional public branch.  The two scalar
direct-sum blocks are public.  Hence every full-\(SQ(H)\) operation is
simulated with at most a constant number of hidden Forrelation queries,
after access to the hardwired \(O(T)\)-entry public weight table.  In the
ideal-real query model this public preprocessing is free relative to hidden
queries.  The same source-query lower bound therefore holds after granting
full matrix SQ.  The next subsection supersedes the ideal-real value
assumption for rational problem parameters; only efficient preprocessing of
the public table remains open.

This oracle check is necessary.  A generic sparse-oracle lower bound does
not automatically survive norm and sampling queries.

### Finite-bit public tables

The existential Jacobi weights can be rounded without losing the lower
bound.  Here is a quantitative version.  Let \(\tau\) be the additive
source accuracy in (10), let \(J\) be the scalar Jacobi matrix underlying
the clock, and put

\[
 \theta=\frac{\tau}{128\kappa},\qquad
 2^{-L}\leq\frac{\tau}{256\kappa}.
\]

Replace every positive off-diagonal weight by

\[
 \widehat\beta_t
 =2^{-L}\left\lfloor 2^L(1-\theta)\beta_t\right\rfloor . \tag{18}
\]

The scalar Jacobi matrix is nonnegative and bipartite.  Perron--Frobenius
monotonicity and the tridiagonal row-sum bound therefore give

\[
 \|\widehat J\|\leq1-\theta,
 \qquad
 \|\widehat J-J\|
 \leq2(\theta+2^{-L}).                                   \tag{19}
\]

For any contractions \(X,Y\), the resolvent identity gives

\[
 \begin{aligned}
 \|f_\kappa(X)-f_\kappa(Y)\|
 &\leq ah\|(mI+hX)^{-1}\|\|(mI+hY)^{-1}\|\|X-Y\|\\
 &\leq h\kappa\|X-Y\|
 \leq \frac\kappa2\|X-Y\|.                             \tag{20}
 \end{aligned}
\]

The block clock is block-unitarily equivalent to \(J\otimes I\), so (19)
also controls the full lifted perturbation.  More specifically,
Montanaro--Shao's scalar propagated-endpoint coefficient is
\(p=[f_\kappa(J)]_{ij}\), with \(|p|\geq\tau\), whereas the observed
computational-basis entry is \(p\Phi\).  Equation (20) gives

\[
 |\widehat p-p|\leq\frac{3\tau}{256},\qquad
 |\widehat p|\geq\frac{253\tau}{256}.
\]

Thus an additive-\(\tau/4\) estimate of \(\widehat p\Phi\) estimates \(\Phi\)
to error at most \(64/253<0.253\), below half the Forrelation promise gap
\((3/5-1/100)/2=0.295\).  This explicitly preserves the reduction and its
query exponent.  In particular, a rounded-to-zero edge cannot disconnect
the two scalar hard endpoints: that would set \(\widehat p=0\), contradicting
the displayed bound.  The shifted core

\[
 \widehat H=mI+h\widehat A
\]

has a strict public spectral margin inside \([a,1]\), and adjoining the
public scalar blocks \(a\) and \(1\) makes its condition number exactly
\(\kappa\).  All hidden dependence is still confined to signs.  Hence row
and column norms, all sampling probabilities, and the Frobenius norm remain
public.  A strict finite-output convention may return squared norms (which
are rational); returning their positive square roots is equivalent public
algebraic postprocessing and reveals no hidden bit.

For a completely rational instance, take the data-block dimension to be a
power of four.  Its normalized Walsh--Hadamard entries are then dyadic.  For
an arbitrary sparsity budget \(s\geq9\), the largest such block allowed by
\(s\) has size at least \((s-1)/8\), so this restriction loses only a
constant in the base of (2).  Rational unit right-hand sides are obtained by

\[
 \widetilde b_+=\frac{3e_i+4e_j}{5},\qquad
 \widetilde b_-=\frac{3e_i-4e_j}{5}.                     \tag{21}
\]

Their diagonal terms cancel, and

\[
 a e_i^T\widehat H^{-1}e_j
 =\frac{25a}{48}\left(
 \widetilde b_+^T\widehat H^{-1}\widetilde b_+
 -\widetilde b_-^T\widehat H^{-1}\widetilde b_-
 \right).                                                \tag{22}
\]

The propagated error is at most \(25\epsilon/24\), because both quadratic
forms lie in \([1,\kappa]\).  Thus it suffices that the finite rational
version use a source parameter \(\tau\geq5\epsilon\) with
\(\tau=\Theta(\epsilon)\), instead of the earlier \(4\epsilon\); all degree
and query asymptotics are unchanged.

The underlying public Jacobi data can also be described algebraically, not
only by invoking an abstract dual witness.  The even part of (5) is

\[
 g_\kappa(x)=\frac{f_\kappa(x)+f_\kappa(-x)}2
 =\frac{am}{m^2-h^2x^2}.
\]

Restrict \(y=x^2\) to \([1/2,1]\) and set \(t=4y-3\).  Then

\[
 g_\kappa(x)=\frac{C}{A-t},\qquad
 C=\frac{4am}{h^2},\qquad A=4(m/h)^2-3.
\]

Write \(E_r\) for the exact degree-\(r\) minimax error on this interval:

\[
 E_r=\frac{C}{A^2-1}
 \left(A-\sqrt{A^2-1}\right)^r,
 \qquad
 \frac{C}{A^2-1}=\frac{mh^2}{2(2m^2-h^2)}=\Theta(1).
\]

Moreover \(\operatorname{arcosh}A=\Theta(\kappa^{-1/2})\), so the degree in
\(x\) is \(2r=\Theta(\sqrt\kappa\log(1/\epsilon))\).  Choose \(r\) so that
\(E_r\geq5\epsilon>E_{r+1}\), and calibrate the preceding rounding with
\(\tau:=E_r\).  Since
\(E_{r+1}/E_r=A-\sqrt{A^2-1}\) is bounded below by a positive universal
constant for \(\kappa\geq4\), this gives \(\tau=\Theta(\epsilon)\).
The Chebyshev error polynomial has algebraic alternation points
\(y_j\in[1/2,1]\).  Normalized alternation weights annihilate every
polynomial in \(y\) through degree \(r\).  Applying the even inverse-Jacobi
identity of Montanaro--Shao to the symmetric nodes
\(\{0,\pm\sqrt{y_j}\}\) gives algebraic positive clock weights and
\(|p|=E_r=\tau\).  Certified root isolation and the Stieltjes recurrence
therefore give an effective route to the ideal weights before (18).  Their
even-parity Jacobi lemma places this coefficient at indices \((2,N-1)\);
the public identity transitions padded at both ends of their Forrelation
clock make those indices compatible with the same source reduction.

This is a genuinely finite public-table result, but its uniformity must be
stated carefully.

- **Nonuniform statement proved here.**  There is an
  \(O(N\log(\kappa/\epsilon))\)-bit dyadic weight table, where
  \(N=\Theta(\sqrt\kappa\log(1/\epsilon))\), and the lower bound charges
  only queries to hidden signs.
- **Computable uniform statement.**  A terminating Turing-machine generator
  exists.  One route is to compute the algebraic alternation data for the
  reciprocal minimax problem and apply the Montanaro--Shao inverse-Jacobi
  construction.  A more elementary route enumerates dyadic tables and uses
  exact rational arithmetic to test the spectral inequalities and the
  endpoint resolvent coefficient; (18)--(20) guarantee that the search
  terminates.
- **Not proved.**  We do not have a polynomial-time generator, a bound on
  the guard precision needed by an inverse-spectral implementation, or a
  polylogarithmic-time SQ data structure.  Those require conditioning and
  root-separation estimates absent from the cited construction.

## Step 6: an actual sparse box-LP Hessian

The clock matrix (11) is block tridiagonal.  Write

\[
 \mu=\frac{\kappa+1}{2\kappa},\qquad
 \nu=\frac{\kappa-1}{2\kappa},
\]

so \(H=\mu I+\nu A\).  It has a block-bidiagonal Cholesky factor
\(H=BB^T\).  Set

\[
 d_0=\sqrt\mu,\qquad
 e_t=\frac{\nu\beta_t}{d_{t-1}},\qquad
 d_t=\sqrt{\mu-e_t^2},                                    \tag{23}
\]

and take

\[
 B_{t,t}=d_tI,\qquad B_{t,t-1}=e_tU_t.                    \tag{24}
\]

With the harmless convention \(e_0=0\), equations (23)--(24) give diagonal
blocks \((d_t^2+e_t^2)I=\mu I\) and off-diagonal blocks
\(d_{t-1}e_tU_t=\nu\beta_tU_t\), hence \(BB^T=H\).
All square roots in (23) are positive because they are the scalar pivots of
the positive-definite block Jacobi matrix \(H\).  The optional public scalar
direct-sum blocks have public scalar Cholesky factors.

Put \(M=B^T\), and for each sign consider the box LP

\[
 \max_x\ b_\pm^Tx
 \qquad\text{subject to}\qquad
 -\mathbf1\leq Mx\leq\mathbf1.                            \tag{25}
\]

Its paired logarithmic barrier is

\[
 \phi(x)=-\sum_j\log(1-(Mx)_j^2).
\]

At the public analytic center \(x=0\),

\[
 \nabla^2\phi(0)=2M^TM=2BB^T=2H.                          \tag{26}
\]

For objective multiplier \(\eta>0\), the squared Newton decrement is

\[
 \boxed{
 \Lambda_{\eta,\pm}^2
 =\frac{\eta^2}{2}b_\pm^TH^{-1}b_\pm
 =\frac{\eta^2}{2}q_\pm.}                                 \tag{27}
\]

Thus two associated LP instances and the polarization calculation (15)
transfer the lower bound to estimating an ordinary LP Newton decrement at
an exact public analytic center.

The factor \(M\) has one diagonal block and one clock-transition block per
row and column, so its sparsity is \(O(d)\).  Its row and column norms are
public functions of \(d_t,e_t\), and the same equal-magnitude
Hadamard/diagonal-sign argument gives constant-hidden-query full SQ.
Moreover \(\kappa(M)=\sqrt{\kappa(H)}\leq\sqrt\kappa\).

The rational finite-bit clock admits an **exact rational** factor, so square
roots in (23) are not an obstruction.  Write its diagonal block as \(\mu I\)
and its off-diagonal block as \(w_tU_t\).  The scalar block \(LDL^T\)
recurrence is

\[
 D_0=\mu,\qquad
 \ell_t=\frac{w_t}{D_{t-1}},\qquad
 D_t=\mu-\frac{w_t^2}{D_{t-1}},                           \tag{28}
\]

with \(L_{t,t}=I\) and \(L_{t,t-1}=\ell_tU_t\).  Every number in (28) is
positive and rational.  If \(D_t=p_t/q_t\) in lowest terms, Lagrange's
four-square theorem supplies integers \(z_{t,1},\ldots,z_{t,4}\) such that

\[
 p_tq_t=\sum_{r=1}^4z_{t,r}^2,
 \qquad
 D_t=\sum_{r=1}^4\left(\frac{z_{t,r}}{q_t}\right)^2.      \tag{29}
\]

Replace the block row \(\sqrt{D_t}(L^T)_{t,*}\) by four block rows
\((z_{t,r}/q_t)(L^T)_{t,*}\).  The resulting rectangular rational matrix
\(M_{\rm rat}\) satisfies

\[
 M_{\rm rat}^TM_{\rm rat}=LDL^T=\widehat H              \tag{30}
\]

exactly.  The same construction factors the public scalar pads \(a\) and
\(1\).  Each new row still contains only one identity block and one clock
gate block: its row sparsity remains \(1+q\) for a \(q\)-sparse gate, and
its column sparsity grows by at most four.  Thus it is \(O(s)\)-sparse when
the clock is \(s\)-sparse; this does not claim the identical numerical
sparsity budget without adjusting the constant in the Hadamard block size.
Its full-SQ interface remains hidden-sign blind.
Thus the rational box LP has Hessian exactly \(2\widehat H\), not merely a
nearby rounded Hessian.  The factor table is effectively computable from
the dyadic weights by rational arithmetic and a four-square search, but no
strong bit-complexity claim is made for that preprocessing.

The barrier in (25) has parameter equal to its ambient number of paired
intervals.  The result therefore closes the local scalar Newton-diagnostic
frontier, but does not by itself prove a low-iteration end-to-end IPM
separation.

## Coherent-query sanity check

The hard clock has more structure than a generic inverse problem, but it
does **not** justify a generic QSVT matching claim.  Gauging away the clock
gates reduces its inverse to a public scalar tridiagonal inverse times the
hidden Forrelation circuit.  Consequently, for the rational vectors (21),

\[
 q_\pm=D\pm C\Phi,                                       \tag{31}
\]

where \(D,C\) are computable from the public scalar clock and \(\Phi\) is
the hidden Forrelation amplitude.  More precisely, if
\(c_f=[f_\kappa(\widehat J)]_{ij}\), then (20) and the original exact
coefficient \(\tau\) imply \(c_f=\Theta(\tau)\), and

\[
 |C|=\frac{24}{25}\frac{|c_f|}{a}=\Theta(\kappa\tau).     \tag{32}
\]

Coherent amplitude estimation to error
\(\delta\) therefore gives additive error \(|C|\delta\) in each quadratic
form.  To meet the requested relative accuracy uniformly over the source
promise, the correct cost is

\[
 O\!\left(\frac{|C|}{\epsilon q_*}\right),\qquad
 q_*:=\min_{\text{allowed }\Phi,\,\pm}|D\pm C\Phi|,       \tag{33}
\]

up to logarithmic success factors; if \(|C|\leq\epsilon q_*\), outputting
the public value \(D\) uses no hidden query.  Since
\(\widehat H^{-1}\succeq I\), \(q_*\geq1\).  Positive-semidefinite
Cauchy--Schwarz and \(2uv\leq u^2+v^2\) give
\(|C|\leq D\leq\kappa\); hence the
lower-bound reduction uses \(\tau=\Theta(\epsilon)\), and (32)--(33) give
the unconditional structured bound \(O(\kappa/q_*)\subseteq O(\kappa)\).
In the high-accuracy range \(\kappa\epsilon=O(1)\), this is in particular
\(O(1/\epsilon)\).  The same \(O(1/\epsilon)\) conclusion over the whole
range would follow from the public noncancellation condition
\(q_*=\Omega(|C|)\), but that estimate has not been proved for the
Montanaro--Shao weights.  These are coherent hidden-sign queries; the same
count holds for an exact coherent matrix-value oracle because every
surviving clock weight is public and nonzero.  Distinguishing the underlying
Forrelation promise is easier than outputting both numerical quadratic forms
to relative error, so its constant-query quantum algorithm does not fill
this gap.

## Match to the classical upper bound

The companion estimator uses a degree
\[
 O(\sqrt\kappa\log(1/\epsilon))
\]
relative inverse polynomial, evaluates one requested coordinate in
\((s+1)^{O(\sqrt\kappa\log(1/\epsilon))}\) local work, and needs only
\(O(\kappa\epsilon^{-2})\) samples.  Its exponential part is

\[
 \exp\!\left(
 O(\sqrt\kappa\log(s+1)\log(1/\epsilon))
 \right).                                                  \tag{34}
\]

Equations (2) and (34) match, up to constants in the exponent and polynomial
factors, over the complete constant-to-high-accuracy range
\(0<\epsilon\leq\epsilon_0\).  Unlike the comparison to the structurally
realized SOCP family, no extra condition
\(\log(1/\epsilon)=\Omega(\log\kappa)\) is needed.

The two lower bounds answer different questions:

- this note closes the sparse-SPD/full-SQ scalar inverse frontier and realizes
  it as an actual sparse box-LP analytic-center decrement;
- the affine-slice LP has barrier parameter one and a hard conventional
  optimal value, while the parameterized one-cone SOCP also transfers to a
  hard conventional optimal value.

## Literature and novelty boundary

The main exponential lower-bound engine is the classical lower-bound theorem
of
[Montanaro--Shao](https://arxiv.org/abs/2311.06999), not a new result of this
note.  The exact error (7) is classical; a convenient modern source is
[Kraus--Vassilevski--Zikatanov](https://arxiv.org/abs/1002.1859), Corollary
2.2.

The apparently new contribution is the combination of:

1. affine restriction of their arbitrary continuous matrix function to the
   bounded normalized reciprocal \(f_\kappa\);
2. the polarization reduction from one inverse entry to two relative
   positive quadratic forms;
3. the explicit verification that their weighted Forrelation clock admits
   constant-hidden-query full SQ, not just sparse entry/location access; and
4. the robust finite-bit public-table strengthening and exact rational
   \(LDL^T\)/four-square box-LP realization; and
5. the match to the dimension-independent decrement estimator and to the
   other structurally realized conic lower families.

This is best framed as a sharp corollary and oracle strengthening of known
matrix-function hardness, not as a new approximate-degree lower-bound
technique.  A targeted search found no prior statement of the resulting
full-SQ relative inverse-quadratic frontier, but that is not a priority
guarantee.
