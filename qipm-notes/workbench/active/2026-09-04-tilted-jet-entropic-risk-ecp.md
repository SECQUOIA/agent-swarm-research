# Certified scenario compression for one-factor entropic-risk conic programs

Status: Proved; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the reduction, cone lift, certificates, and stated
access-model bounds

## Main result

Consider a scenario distribution with probabilities \(p_i>0\),
\(\sum_i p_i=1\), and scalar scenario loadings
\(\lambda_i\in[-\Lambda,\Lambda]\), where \(\Lambda>0\).  For a risk
parameter \(\beta>0\), define the closed restricted-sector perspective of
the one-factor entropic risk

\[
 {\cal R}_\beta(U,V)
 =\frac V\beta\log\left(
       \sum_{i=1}^Np_i e^{\beta\lambda_iU/V}
   \right),\qquad V>0,
 \tag{1}
\]

and set \({\cal R}_\beta(0,0)=0\).  We only use it on the closed sector

\[
 0\leq V\leq V_{\max},\qquad |U|\leq LV.
 \tag{2}
\]

The sector makes the value in (1) converge to zero as \(V\downarrow0\),
uniformly over feasible \(U/V\), so the stated closure is continuous.  Put

\[
 K=\beta\Lambda L.
 \tag{3}
\]

We take \(L>0\).  The degenerate cases \(\Lambda=0\) or \(L=0\) have zero
scenario-risk term and need no compilation.

Let \({\cal X}\) be a convex feasible set with a sparse conic lift, let
\(U(x),V(x)\) be affine, and assume (2) is part of that lift.  Let
\(\phi(x)\) be a convex conic-representable deterministic cost and
\(\gamma\geq0\).  The original scenario program is

\[
 P=\inf_{x\in{\cal X}}
 \left\{\phi(x)+\gamma{\cal R}_\beta(U(x),V(x))\right\}.
 \tag{4}
\]

Assume the infimum is finite and attained.  No sign assumption on \(\phi\)
or \(P\), and no strong convexity or optimizer-stability assumption, is
needed.

Apply the independently audited tilted-jet compiler from
[the signed exponential compiler](2026-09-04-robust-signed-exponential-moment-grid-compiler.md)
to the normalized slopes \(X_i=\lambda_i/\Lambda\).  With probability at
least \(1-\alpha\), it returns \(R\) public-grid slopes
\(\widehat\lambda_j\in[-\Lambda,\Lambda]\), positive weights
\(\theta_j\), and explicit \(0<L_*\leq U_*\) such that

\[
 L_* f(z)\leq g(z)\leq U_*f(z),\qquad |z|\leq K,
 \tag{5}
\]

where

\[
 f(z)=\sum_i p_i e^{z\lambda_i/\Lambda},\qquad
 g(z)=\sum_{j=1}^R\theta_j e^{z\widehat\lambda_j/\Lambda},
 \tag{6}
\]

and

\[
 R=O\bigl(K+\log(1/\epsilon)\bigr),\qquad
 1-\epsilon\leq L_*\leq U_*\leq1+\epsilon.
 \tag{7}
\]

Define the compressed perspective

\[
\widetilde{\cal R}_\beta(U,V)
 =\frac V\beta\log\left(
       \sum_{j=1}^R\theta_j e^{\beta\widehat\lambda_jU/V}
   \right).
 \tag{8}
\]

Set \(\widetilde{\cal R}_\beta(0,0)=0\), again using the continuous
sector closure.

Taking logarithms in (5) and multiplying by \(V/\beta\) gives the global
pointwise sandwich

\[
 \widetilde{\cal R}_\beta(U,V)-{V\over\beta}\log U_*
 \leq {\cal R}_\beta(U,V)
 \leq
 \widetilde{\cal R}_\beta(U,V)-{V\over\beta}\log L_*.
 \tag{9}
\]

It remains valid at \(V=0\) by continuity.  Let \(P_-\) and \(P_+\) be the
optimal values obtained from (4) by replacing \({\cal R}_\beta\) with the
left and right sides of (9), respectively.  Then

\[
 P_-\leq P\leq P_+,\qquad
 0\leq P_+-P_-
 \leq {\gamma V_{\max}\over\beta}
       \log{U_*\over L_*}.
 \tag{10}
\]

All certificates from (9) onward are conditional on the compiler's
simultaneous-success event, which has probability at least \(1-\alpha\).

The second inequality follows from the elementary rule that if two
objectives differ pointwise by a number in \([0,D]\), then their infima
differ by at most \(D\).  Thus it does not require the two compressed
programs to have nearby optimizers.

If \(x_+\) minimizes the upper compressed program, then it is a certified
solution for the original problem:

\[
 \phi(x_+)+\gamma{\cal R}_\beta(U(x_+),V(x_+))-P
 \leq {\gamma V_{\max}\over\beta}
       \log{U_*\over L_*}.
 \tag{11}
\]

More generally, let \({\rm LB}_-\leq P_-\) be a certified lower bound for
the lower compressed program, and let \(x_+\) be feasible for the upper
compressed program with
\({\rm UB}_+=F_+(x_+)\), where \(F_+\) is its objective.  If

\[
 (P_--{\rm LB}_-)+({\rm UB}_+-P_+)\leq\delta_{\rm opt},
\]

then
\([{\rm LB}_-,{\rm UB}_+]\) is a certified interval for \(P\).
Combining these certificates with (9) also gives

\[
 {\rm UB}_+-{\rm LB}_-
 \leq\delta_{\rm opt}+{\gamma V_{\max}\over\beta}
       \log{U_*\over L_*}.
 \tag{12}
\]

The same right side bounds the original suboptimality of \(x_+\), because
the original objective at \(x_+\) is at most \(F_+(x_+)\).

For \(0<\epsilon\leq1/2\),
\(\log(U_*/L_*)\leq\log((1+\epsilon)/(1-\epsilon))\leq3\epsilon\).
Consequently compiler accuracy

\[
 \epsilon\leq
 \min\left\{\frac12,
 {\beta\tau\over6\gamma V_{\max}}\right\}
 \tag{13}
\]

and solver gap \(\delta_{\rm opt}\leq\tau/2\) yield an end-to-end additive
\(\tau\) optimal-value and solution certificate.  The case
\(\gamma V_{\max}=0\) is deterministic and needs no scenario compilation.
If the original objective is additionally \(\mu\)-strongly convex in a
specified norm, (12) also gives the standard distance certificate
\[
 \|x_+-x^*\|\leq
 \sqrt{\frac{2}{\mu}\left(
 \delta_{\rm opt}+{\gamma V_{\max}\over\beta}
 \log{U_*\over L_*}\right)}.
\]
Strong convexity is used only for this optional distance statement.

## Explicit sparse exponential-cone formulation

The epigraph condition

\[
 t\geq V\log\left(
       \sum_{j=1}^R\theta_j e^{\beta\widehat\lambda_jU/V}
                         \right)
 \tag{14}
\]

has the exact lift

\[
 (\beta\widehat\lambda_jU-t,\ V,\ r_j)\in K_{\exp}
 \quad(1\leq j\leq R),\qquad
 \sum_{j=1}^R\theta_jr_j\leq V.
 \tag{15}
\]

Here
\(K_{\exp}=\operatorname{cl}\{(a,b,c):b>0,\ c\geq b e^{a/b}\}\);
this fixes the coordinate convention.
Indeed, for \(V>0\), the cone inequalities say
\(r_j\geq V e^{\beta\widehat\lambda_jU/V-t/V}\); summing them proves (14),
and equality choices prove the converse.  Closure of the exponential cone
handles \(V=0\): the sector forces \(U=0\), while the \(V=0\) face of
\(K_{\exp}\) gives \(t\geq0\) and \(r_j\geq0\); positive \(\theta_j\) and
\(\sum_j\theta_jr_j\leq0\) then force every \(r_j=0\).  This is exactly the
closed epigraph at the sector origin.  The lower and upper programs
minimize, respectively,

\[
 \phi(x)+{\gamma\over\beta}(t-V\log U_*),\qquad
 \phi(x)+{\gamma\over\beta}(t-V\log L_*),
 \tag{16}
\]

over the same lift.

To make the inner/outer directions explicit, write the two risk functions
in (9) as \({\cal R}_-\leq {\cal R}_\beta\leq {\cal R}_+\).  Their
epigraphs satisfy

\[
 \operatorname{epi}({\cal R}_+)
 \subseteq \operatorname{epi}({\cal R}_\beta)
 \subseteq \operatorname{epi}({\cal R}_-).
\]

Thus the lower program uses an outer epigraph relaxation, whereas the upper
program uses an inner epigraph restriction.  Both are represented by (15)
with only the linear objective shift in (16) changed.

If the base lift has barrier parameter \(\nu_0\), each compressed program
has

\[
 \nu\leq\nu_0+3R+O(1)
 =\nu_0+O\bigl(K+\log(1/\epsilon)\bigr),
 \tag{17}
\]

using the standard parameter-three barrier for each three-dimensional
exponential cone.  The uncompressed scenario formulation has \(N\)
exponential cones and parameter \(\nu_0+3N+O(1)\).
This is the barrier parameter of the displayed product formulation, not an
intrinsic lower bound for every lift of the projected low-dimensional
epigraph.

The lift can preserve literal sparsity.  Replace the shared \(U,V,t\) by
local copies at the \(R\) cone leaves, enforce consensus through balanced
binary copy trees using two-sparse equalities, and aggregate
\(\sum_j\theta_jr_j\) through a binary partial-sum tree using three-sparse
equalities.  Apart from the base affine rows defining \(U(x)\) and \(V(x)\),
every added row and column then has \(O(1)\) incidence.  The lift adds
\(O(R)\) variables and rows.  If those two base affine maps have at most
\(s_{\rm link}\) nonzeros and the base formulation has row sparsity \(s_0\),
the compiled formulation has row sparsity
\(O(\max\{s_0,s_{\rm link},1\})\), rather than a hidden dense scenario-sum
row.  This construction does not alter or improve any pre-existing dense
columns in the base formulation.

## Source-query and barrier frontier

With coherent preparation of \(\sum_i\sqrt{p_i}|i\rangle\) and coherent
value access to \(\lambda_i\), the compilation cost is

\[
 \widetilde O(e^K/\epsilon)
 \tag{18}
\]

source queries.  The cited tilted-jet theorem is stated for \(K\geq1\);
when \(0<K<1\), apply it on the padded interval \([-1,1]\), which changes
(18) only by a universal constant and accounts for the \(1+\) term below.
If indexed weight-and-value access is additionally
available, explicitly reading the source gives the combined bound

\[
 \widetilde O\left(\min\left\{N,{e^K\over\epsilon}\right\}\right).
 \tag{19}
\]

At target optimization accuracy \(\tau\), (13) therefore gives

\[
 \widetilde O\left(
 \min\left\{N,
 e^K\max\left\{1,
 {\,\gamma V_{\max}\over\beta\tau}\right\}
 \right\}\right)
 \tag{20}
\]

source queries and

\[
 R=O\left(1+K+\log_+{\gamma V_{\max}\over\beta\tau}\right)
 \tag{21}
\]

exponential cones, where \(\log_+x=\max\{0,\log x\}\).  These are source
compilation costs; solving the resulting explicit conic programs incurs the
ordinary classical or quantum IPM cost for a formulation with parameter
(17).  No end-to-end runtime speedup is claimed without specifying that
solver and the base conic model.

In particular, at target accuracy the displayed product formulation has

\[
 \nu\leq\nu_0+
 O\left(1+K+\log_+{\gamma V_{\max}\over\beta\tau}\right).
 \tag{21a}
\]

For fixed \(K>0\) and
\(\gamma V_{\max}/(\beta\tau)\to\infty\), the sharper fixed-sector
compression bound gives

\[
 R=O_K\left(
 {\log(\gamma V_{\max}/(\beta\tau))\over
  \log\log(\gamma V_{\max}/(\beta\tau))}
 \right).
 \tag{21b}
\]

The source-query scale is optimal in the large-source, nontrivial-accuracy
regime \(0<\tau\leq c\gamma V_{\max}/\beta\).  Restrict
(4) to the singleton \(U=LV_{\max},V=V_{\max}\), take \(\phi=0\), and use
the binary source \(\lambda_i\in\{-\Lambda,+\Lambda\}\).  Around
\(\Pr[\lambda_i=+\Lambda]=\Theta(e^{-2K})\), changing this probability by a
relative \(\Theta(\beta\tau/(\gamma V_{\max}))\) changes the optimal value
by \(\Theta(\tau)\).  Indeed, its MGF is
\(M_K(p)=e^{-K}+(e^K-e^{-K})p\), so for
\(p=\Theta(e^{-2K})\) and \(\Delta p=\Theta(p\eta)\),
\(\log M_K(p+\Delta p)-\log M_K(p)=\Theta(\eta)\).
Approximate counting therefore gives the quantum lower bound

\[
 \Omega\left({e^K\gamma V_{\max}\over\beta\tau}\right),
 \tag{22}
\]

in the coherent weighted-sampling model.  Here the oracle prepares the
source distribution but does not reveal a short explicit list of its
weights; the standard two-Bernoulli amplitude-estimation lower bound
applies in the usual black-box state-preparation model with access to the
unitary, its inverse, and arbitrary but fixed hidden completion, and has no
finite-\(N\) qualification.  It would not apply to an oracle that explicitly
reveals the two probabilities.

For i.i.d. classical samples from the same hidden weighted source, the
Bernoulli KL bound gives

\[
 \Omega\left({e^{2K}\gamma^2V_{\max}^2
                  \over\beta^2\tau^2}\right).
 \tag{23}
\]

The tilted-jet construction has a matching sampling upper bound, up to
confidence logarithms.  Thus this scenario program exhibits the full
quadratic separation between coherent access and classical sampling access,
while both procedures return an ordinary classical sparse conic
formulation.  Equations (22)--(23) are optimal-value lower bounds, not
hardness of solving an already explicit compressed program.

For finite uniform scenarios under indexed value access, integer Hamming
weights impose an additional resolution condition.  A sufficient
large-source condition for the unsaturated quantum lower bound (22) is

\[
 N=\Omega\left(
 e^{2K}{\gamma V_{\max}\over\beta\tau}
 \right),
 \tag{24}
\]

up to integer rounding and fixed constants.  The corresponding classical
indexed-source law is, up to confidence logarithms,

\[
 \widetilde\Theta\left(
 \min\left\{N,\,
 e^{2K}{\gamma^2V_{\max}^2\over\beta^2\tau^2}
 \right\}\right).
 \tag{24a}
\]

Consequently the full unsaturated quadratic comparison in the indexed
model requires the stronger condition

\[
 N=\Omega\left(
 e^{2K}{\gamma^2V_{\max}^2\over\beta^2\tau^2}
 \right).
 \tag{24b}
\]

Condition (24) only guarantees that the binary hard pair exists at the
resolution needed for the quantum lower bound.  Between (24) and (24b),
classical access is already in its finite-population saturation regime.
Below these thresholds the interpolation is the one proved in the
source-compiler note.

## Fixed-scale log-sum-exp corollary

When \(V\equiv1\), (1) is the ordinary one-factor entropic-risk or
log-expectation-exponential objective.  The two compressed objectives in
(16) differ only by the constant

\[
 {\gamma\over\beta}\log{U_*\over L_*}.
\]

The two compressed programs therefore have exactly the same minimizers
(not necessarily the same minimizers as the original program).  A single
solve of the unshifted compressed problem produces \(\widehat x\), and
shifting its
certified optimal-value interval by
\(-\gamma\log U_*/\beta\) and
\(-\gamma\log L_*/\beta\) gives both the original value bracket and the
solution guarantee.  This is stronger than a generic perturbation theorem:
no curvature or uniqueness is required.

A concrete sparse instance is

\[
 \min_{x\in\mathbb R^n}
 \left\{c^Tx+{\gamma\over\beta}
 \log\sum_{i=1}^Np_i
 e^{\beta\lambda_i(a^Tx+a_0)}:
 Ax=b,\ Cx\leq d,\ |a^Tx+a_0|\leq L\right\}.
 \tag{25}
\]

If \(A,C,a\) are sparse, the copy and aggregation trees above give an
explicit sparse \(R\)-exponential-cone program.  This model covers a
one-factor scenario shock multiplying a common portfolio exposure or
recourse quantity.  It does not cover arbitrary scenario vectors
\(a_i^Tx\); extending the compiler beyond a shared scalar exposure is a
separate problem.

A bounded-temperature one-factor EVaR model is also included.  Adding the
deterministic linear term

\[
 {V\over\beta}\log {1\over1-\rho},\qquad 0<\rho<1,
 \tag{26}
\]

to (1), and minimizing over an allowed interval of \(V\), gives the usual
perspective cumulant term in EVaR.  Term (26) is absorbed into \(\phi\) and
does not affect the compiler, sandwich, source-query count, or cone count.
Assumption (2) makes the temperature search compact and keeps every queried
MGF argument inside \([-K,K]\); a claim for unbounded temperature or
unbounded exposure would require a separate tail argument.

## Sharp cone-count lower bound for reusable positive-atom models

The fixed-\(K\) order in (21b) is asymptotically optimal within the natural
class of reusable positive-atom scenario models.  More sharply, the
existential minimax support count in this class has an exact leading
constant.  Fix \(K,\beta,\gamma,V_0>0\), put
\(L=K/(\beta\Lambda)\), and for a source measure \(\mu\) on \([-1,1]\)
define on \(y\in[-L,L]\)

\[
 h_\mu(y)={\gamma V_0\over\beta}
 \log M_\mu(\beta\Lambda y),\qquad
 v_\mu(a)=\inf_{|y|\leq L}\{h_\mu(y)+ay\}.
 \tag{27}
\]

This is the specialization of (4) with \(V=V_0\), \(U=V_0y\), and
deterministic linear tilt \(ay\).

Suppose one positive \(m\)-atomic measure \(\nu\), supported on
\([-1,1]\), is reused for every
linear tilt in the bounded interval
\(|a|\leq B:=\gamma V_0\Lambda\) and satisfies

\[
 \sup_{|a|\leq B}|v_\mu(a)-v_\nu(a)|\leq\tau.
 \tag{28}
\]

Then

\[
 \sup_{|y|\leq L}|h_\mu(y)-h_\nu(y)|\leq\tau.
 \tag{29}
\]

Indeed, extend each \(h\) by \(+\infty\) outside \([-L,L]\).  The extended
functions are closed and convex, and
\(v_\mu(a)=-h_\mu^*(-a)\).  Moreover,
\[
 h_\mu'(y)=\gamma V_0\Lambda\,
 {\int x e^{\beta\Lambda yx}\,d\mu(x)\over
  \int e^{\beta\Lambda yx}\,d\mu(x)},
 \qquad
 |h_\mu'(y)|,\ |h_\nu'(y)|\leq\gamma V_0\Lambda=B,
\]
with the analogous formula for \(\nu\).
At every interior point, the tangent slope therefore lies in \([-B,B]\)
and realizes the Fenchel biconjugate supremum; the one-sided tangent does
the same at either endpoint.  Thus the conjugates restricted to
\([-B,B]\) already recover both functions on \([-L,L]\), and (28) gives
(29).
Writing \(\delta=\beta\tau/(\gamma V_0)\), (29) implies

\[
 \sup_{|z|\leq K}
 { |M_\mu(z)-M_\nu(z)|\over M_\mu(z)}
 \leq e^\delta-1.
 \tag{30}
\]

Conversely, a uniform relative MGF error at most \(\epsilon<1\) gives
\[
 \sup_{|y|\leq L}|h_\mu(y)-h_\nu(y)|
 \leq {\gamma V_0\over\beta}[-\log(1-\epsilon)],
\]
and hence the same bound for all the tilted optimal values.  Thus the
support minimax upper and lower bounds apply in both directions.

Apply this to the fixed uniform source on \([-1,1]\) in
[the exponential-mixture support lower bound](2026-09-04-exponential-mixture-support-lower-bound.md).
Together with the matching Gaussian upper bound, it proves that the least
number of positive atoms needed to guarantee (28) for every source obeys,
as \(\tau\downarrow0\),

\[
 \boxed{
 m_{\rm reusable}(\tau,K)
 =\left(\frac12+o(1)\right)
 {\log(\gamma V_0/(\beta\tau))\over
  \log\log(\gamma V_0/(\beta\tau))}.}
 \tag{31}
\]

Here \(m_{\rm reusable}\) denotes the least support size that guarantees
(28) for every source measure.

There is also a sharp joint sector--accuracy law.  Put
\(H=\log(\gamma V_0/(\beta\tau))\).  If \(H/K\to\infty\) and
\(H/W(H/(2K))\to\infty\), then for compressed slopes constrained to the
physical interval,

\[
 m_{\rm reusable}(\tau,K)
 =(1+o(1)){H\over2W(H/(2K))}.
 \tag{31a}
\]

This is the Lambert-\(W\) inversion of the uniform
\(2m\log(m/K)+O(m+K)\) support law.  The second condition only removes the
bounded-integer-support regime; for example, it holds when
\(\log(1/K)=o(H)\).

For fixed \(K\), if (28) is instead required for every \(a\in\mathbb R\),
the lower bound still has the same leading constant even when the compressed
slopes may lie anywhere on the real line.  A finite hard source with \(m+1\)
scenarios follows from the Gauss--Legendre version of the support lower
bound.  Since the direct positive-mixture lift uses one exponential cone
per retained atom, (31) matches the order of the cone count in (21b) within
this compiler class.  The exact leading-constant upper in (31) is
existential via Gaussian quadrature; it is not a leading-constant claim for
the particular robust tilted-jet recovery algorithm.

The reuse condition in (28) is essential.  This is not a lower bound on
arbitrary exponential-cone extended formulations, nor on a compressor
allowed to construct a different summary after seeing one particular
linear tilt.  Its optimization content is that uniform accuracy for the
entire parametric family of optimal values forces uniform recovery of the
risk function by convex duality.

## Independent audit scope

This is genuinely an optimization theorem, not only an approximation
statement about a source MGF.  For any convex conic-representable base
problem satisfying the one-factor sector assumption, (10)--(13) give two
explicit conic programs, a certified bracket for the original optimal
value, and a certified original-objective guarantee for a feasible point
returned by the upper program.  No optimizer stability is used.

The scope is nevertheless specific.  The compiler covers a shared scalar
scenario loading \(\lambda_i U(x)\), bounded perspective scale \(V\), and
bounded normalized exposure \(U/V\).  It does not cover arbitrary scenario
vectors, unbounded temperature, or an end-to-end IPM running time without a
separately specified solver.  Moreover, the lower bounds use a singleton
feasible set.  They prove that optimal-value estimation (and hence any
general method promising the stated value certificate) inherits the source
oracle cost; they do not prove that solving an already explicit compressed
conic program is hard, nor that recovering a nontrivial optimizer is hard.

## Literature screen and novelty boundary

Entropic risk and log-expectation-exponential objectives are established.
For example, [Ahmadi-Javid and Fallah-Tafti](https://arxiv.org/abs/1708.05713)
study sample-based EVaR portfolio optimization, while the broader
[entropic-risk study](https://optimization-online.org/wp-content/uploads/2017/03/5925.pdf)
develops its moment-generating-function and perspective structure.  The recent
[SCENT paper](https://arxiv.org/abs/2602.02877) explicitly targets
log-expectation-exponential objectives with a huge inner sample set, using a
stochastic first-order dual method.  [Woerner and
Egger](https://arxiv.org/abs/1806.06893) use amplitude estimation for
financial VaR/CVaR evaluation, in a different risk functional and without
classical scenario compression.  Standard
[exponential-cone modeling of log-sum-exp](https://docs.mosek.com/modeling-cookbook/expo.html#log-sum-exp)
is also well known.  More specifically, [Dowson, Morton, and
Pagnoncelli](https://optimization-online.org/wp-content/uploads/2020/08/7984.pdf)
give scenario-wise exponential-cone formulations for entropic risk in
multistage stochastic programs.

Scenario reduction by quadrature and moment matching is established as
well; see
[Pennanen--Koivu](https://doi.org/10.1007/s00211-004-0571-4) and
[Mehrotra--Papp](https://doi.org/10.1137/110858082).  Classical
risk-averse scenario reduction is also a substantial literature; for
example, [Arpón, Homem-de-Mello, and
Pagnoncelli](https://optimization-online.org/wp-content/uploads/2018/03/6520.pdf)
develop reduction based on effective scenarios and probability metrics,
primarily for coherent tail-risk models.  The novelty claim therefore does
not include scenario reduction or moment-matching quadrature by itself.

Ahmadi-Javid and Fallah-Tafti already obtain a smooth optimization model
whose number of decision variables and constraints is independent of sample
size.  Their objective and derivatives still evaluate the empirical
scenario sum.  The claim here is different: it produces a reusable
classical positive-atom source summary, an explicit sparse conic lift whose
cone count is independent of \(N\), and certified inner/outer optimal-value
bounds after sublinear source access.

A targeted search on 2026-09-04 found no work combining these applications
with quantum source access, a certified uniform positive-atom scenario
compression, inner/outer sparse exponential-cone programs, the exact
optimal-value and returned-solution certificate (10)--(12), or the matched
\(e^K/\epsilon\) versus \(e^{2K}/\epsilon^2\) source-access frontier.  The
novelty candidate is this complete certified compression theorem, not the
definition of entropic risk, the exponential-cone lift, amplitude
estimation, or Caratheodory compression separately.  This screen is not a
priority claim and should be followed by an expert review of stochastic
programming and scenario-reduction literature.  In particular, (31)--(31a)
are optimization corollaries of the separately proved positive-exponential-
mixture support minimax theorem; they are not claimed as generic
scenario-reduction lower bounds.
