# General block log-det condensation and conditioning theorem

Date: 2026-09-02

This note abstracts the capacity transition found in the sparse holonomy SDP.

## Algorithmic corollary: central-state synthesis versus winner search

The abstract condensation theorem has a clean component-oracle consequence.  The
statement below separates a standard quantum search fact from the optimization-specific
central weights; it does not claim a new search primitive or a new interior-point
iteration.

### Oracle and output model

Assume the \(G\) component inputs are independent and one component is promised to have
the public winner cost \(C_W\), while the other \(G-1\) components have the public
homogeneous loser cost \(C_L\).  A clean coherent evaluator acts as
\[
V_f|g,0\rangle=|g,f_g\rangle,
\qquad
f_g=1\iff g\text{ is the winner}, \tag{A1}
\]
and costs \(T_{\rm eval}\) raw component-oracle queries.  Its inverse has the same cost.
If only a bounded-error evaluator is available, all bounds below acquire the standard
polylogarithmic error-reduction factor needed to make coherent misclassification smaller
than the final state error.

At a fixed positive barrier parameter, homogeneity implies that the central root state
has the form
\[
\rho_p=
p|w\rangle\langle w|\otimes\rho_W
+\frac{1-p}{G-1}\sum_{g\ne w}|g\rangle\langle g|\otimes\rho_L, \tag{A2}
\]
where \(w\) is the unique winner, \(p\) is its trace mass, and the normalized local
states \(\rho_W,\rho_L\) are public once the two costs, \(G\), and the barrier parameter
are fixed.  They are the normalized resolvents supplied by the abstract central-path
formula.  Let
\[
a_W=p,
\qquad
a_L=\frac{1-p}{G-1},
\qquad
a_{\max}=\max\{a_W,a_L\}. \tag{A3}
\]
The winner is the heaviest component whenever \(p\ge1/G\), in which case
\(a_{\max}=p\).

The output in this section is either a purification of (A2), a winning component label,
or a compact optimizer supported on that component.  Materializing every component is
not included and would erase a search advantage by output size.

### Coherent rejection preparation of the central state

There is a direct preparation algorithm that does not first learn \(w\).

1. Prepare \(G^{-1/2}\sum_g|g\rangle\), and coherently copy the label to an environment
   register so that tracing out the copy will make (A2) block diagonal.
2. Apply \(V_f\).  Conditional on \(f_g=b\), rotate an acceptance qubit with amplitude
   \(\sqrt{a_b/a_{\max}}\), where \(a_1=a_W\) and \(a_0=a_L\).
3. Conditional on \(b\), use a public local circuit to prepare a purification of
   \(\rho_W\) or \(\rho_L\).
4. Amplify the acceptance subspace and retain all label, predicate, and local-purifying
   registers as environment.  Reversing the trial circuit supplies the reflection
   required by amplitude amplification.

The one-trial acceptance probability is exactly
\[
P_{\rm acc}
=\frac1G\left(\frac{a_W}{a_{\max}}+(G-1)\frac{a_L}{a_{\max}}\right)
=\frac1{Ga_{\max}}. \tag{A4}
\]
Conditioned on acceptance, label \(g\) has probability \(a_{f_g}\), and its local
reduced state is the required \(\rho_{f_g}\).  Tracing out the copied label and local
purification registers therefore gives exactly (A2).

Fixed-point amplification yields the component-query upper bound
\[
\widetilde O\!\left(T_{\rm eval}\sqrt{Ga_{\max}}
+T_{\rm loc}\sqrt{Ga_{\max}}\right), \tag{A5}
\]
where \(T_{\rm loc}\) is the gate cost, not a raw component-query cost, of the two public
constant-block state preparations.  When \(p\ge1/G\), the raw-query part is
\[
\widetilde O\!\left(T_{\rm eval}\sqrt{Gp}\right). \tag{A6}
\]
The tildes hide only accuracy logarithms.  The scalar secular equation determining
\(p\), and the two fixed-size resolvents, can be solved classically before the circuit is
run.  For variable block size \(d\), their arithmetic and state-synthesis cost must be
charged separately as \(\operatorname{poly}(d,\log(1/\epsilon))\).

Equation (A6) is useful beyond winner extraction: it is an alternative central-state
preparation method on the promised block family.  Its query cost increases as the
central path condenses, because a rare label must receive progressively larger amplitude.
It assumes that exactly one winner exists.  If the promise also permits no winner, first
distinguishing zero from one winner costs \(\Theta(\sqrt G)\) component evaluations in
the generic oracle model.

### Extracting a winner from a central state

If a central state is already available as copies, label measurement proposes the winner
with probability \(p\).  Exact verification with (A1) and repetition costs
\[
O\!\left(\frac{Q_\rho+T_{\rm eval}}p\log\frac1\delta\right), \tag{A7}
\]
where \(Q_\rho\) is the raw-query cost of one copy.  If a coherent preparation unitary
\(U_\rho\), its inverse, and the clean winner reflection are available, fixed-point
amplitude amplification improves this to
\[
O\!\left(\frac{Q_U+T_{\rm eval}}{\sqrt p}
\log\frac1\delta\right). \tag{A8}
\]
Trace-distance accuracy is enough for (A7).  Equation (A8) additionally needs an
operator-level implementation guarantee for \(U_\rho\) and its inverse; accuracy of the
single prepared density matrix does not constrain the unitary completion off
\(|0\rangle\).

Combining (A6) and (A8) gives the cancellation
\[
\widetilde O(T_{\rm eval}\sqrt{Gp})\cdot O(p^{-1/2})
=\widetilde O(T_{\rm eval}\sqrt G). \tag{A9}
\]
Thus condensation changes where the work is paid, but not the end-to-end component-
oracle cost of finding the winner.  In the diffuse regime the state is cheap to prepare
and expensive to filter; in the condensed regime it is expensive to prepare and easy to
measure.

### Direct search, solution recovery, and lower-bound assumptions

Applying quantum search directly to the clean predicate (A1) finds \(w\) with failure
\(\delta\) using
\[
\widetilde O(T_{\rm eval}\sqrt G) \tag{A10}
\]
raw queries.  Once \(w\) is known, return the public winner optimizer, run a solver on
that one component, or recover its original coordinates.  The honest end-to-end bound is
\[
\widetilde O(T_{\rm eval}\sqrt G)
+T_{\rm solve}+T_{\rm recover}. \tag{A11}
\]
This is a search-then-crossover module.  It is not a new QIPM unless
\(T_{\rm solve}\) is supplied by a separately analyzed interior-point method.

A matching lower bound does not follow merely by declaring that one evaluation costs
\(T_{\rm eval}\).  For a rigorous composition theorem, suppose each independent
component contains a total Boolean function \(f\) with bounded-error quantum query
complexity \(q\), under the same local oracle used by the global algorithm.  The general
adversary composition theorem then gives
\[
Q(\operatorname{UniqueOR}_G\circ f)=\Theta(q\sqrt G). \tag{A12}
\]
If the clean evaluator is query-optimal up to logarithms,
\(T_{\rm eval}=\widetilde\Theta(q)\), (A10)--(A11) are optimal in their component-query
dependence.

Composing (A8) with (A12) gives the preparation tradeoff
\[
Q_U+T_{\rm eval}=\Omega(q\sqrt{Gp}), \tag{A13}
\]
and copy-based verified repetition gives
\[
Q_\rho+T_{\rm eval}=\Omega(pq\sqrt G). \tag{A14}
\]
These are conditional on the stated independent-oracle composition.  They should not be
claimed for an arbitrary structured component representation whose queries overlap or
whose oracle already supplies an aggregate winner flag.

### Consequences across the abstract condensation regimes

For a simple winner pole and finite loser capacity, the abstract theorem gives
\[
p=\begin{cases}
\Theta(1),&\text{condensed/subcritical regime},\\
\Theta(G^{-1/2}),&\text{critical regime},\\
\Theta(G^{-1}),&\text{diffuse/supercritical regime}.
\end{cases} \tag{A15}
\]
Equations (A6)--(A8) give
\[
\begin{array}{c|c|c|c}
\text{regime}&\text{central preparation}&\text{copy extraction}&
\text{coherent extraction}\\ \hline
\text{condensed}&\widetilde O(T_{\rm eval}G^{1/2})&O(1)&O(1)\\
\text{critical}&\widetilde O(T_{\rm eval}G^{1/4})&O(G^{1/2})&O(G^{1/4})\\
\text{diffuse}&\widetilde O(T_{\rm eval})&O(G)&O(G^{1/2}).
\end{array} \tag{A16}
\]
The product of the central-preparation and coherent-extraction factors is
\(\widetilde O(T_{\rm eval}\sqrt G)\) in every row.  Copy extraction is quadratically
worse except in the condensed regime.

The diffuse-row preparation bound concerns an exact state or accuracy fine enough to
resolve its \(O(1/G)\) exceptional mass.  At fixed trace-distance error, the exceptional
component may be below the output tolerance, and a zero-query homogeneous-loser state
can already be a valid approximation.  Therefore (A16) must not be used to claim an
\(\Omega(T_{\rm eval})\) lower bound for constant-error diffuse-state preparation.

### Comparison with central continuation

For \(d\times d\) root blocks, the root product barrier has parameter \(dG\).  A
short-step method that reduces the scaled barrier from a constant to the
\(\Theta(1/G)\) condensation scale uses
\[
O(\sqrt{dG}\log G) \tag{A17}
\]
Newton steps.  If every root is represented by \(P\) copied physical PSD blocks, the
unreduced product barrier parameter is \(dGP\), giving
\(O(\sqrt{dGP}\log G)\) iterations under the conventional formulation.  These are
iteration counts only; they do not include matrix access, linear-system conditioning,
state preparation, tomography, or recovery.

When the abstract mass--conditioning theorem applies, reaching constant winner mass
also forces a reduced Euclidean Hessian condition number growing with \(G\).  One must
not multiply this condition number by (A17) without specifying a particular solver and
preconditioner, but it rules out a condition-independent continuation claim.

The clean algorithmic dichotomy is:

- If a central state is required as an output on the exactly-one-winner promise,
  coherent rejection preparation (A5) is a direct, \(p\)-sensitive alternative to
  following the path.
- If the goal is the winner, optimum, or active face, direct search followed by one
  component solve (A11) is never asymptotically worse in component queries and avoids
  the ill-conditioned condensed part of the global central path.
- If a QIPM has already produced a central state for another reason, (A7)--(A8) are
  valid marginal-cost procedures for extracting the active component.

The first procedure is central-state synthesis by amplitude reweighting; the second is
search-then-crossover; only the third is naturally a postprocessing step of a QIPM.

### Literature calibration

Amplitude amplification, minimum finding, and general-adversary composition are standard.
Relevant primary sources are Boyer--Brassard--Høyer--Tapp,
*Tight bounds on quantum searching* (arXiv:quant-ph/9605034), Dürr--Høyer,
*A Quantum Algorithm for Finding the Minimum* (arXiv:quant-ph/9607014), and
Høyer--Lee--Špalek, *Tight adversary bounds for composite functions*
(arXiv:quant-ph/0509067).

The potentially useful new statement is the optimization-specific conservation law
(A9): the abstract log-det condensation mass controls central-state synthesis and
winner extraction in reciprocal ways, leaving \(\widetilde\Theta(q\sqrt G)\) total
component-query work under an independently composed oracle.  This is an algorithmic
corollary of the condensation theorem, not a claim that the quantum primitives are new.

## 1. Model and exact central path

Fix a block dimension \(d\).  There is one winning cost \(C_*\) and \(G-1\)
identical losing costs \(C_L\).  Subtract the winning optimum \(v_*\) from both
costs.  Assume
\[
 \operatorname{spec}(C_*-v_*I)
   =\{\underbrace{0,\ldots,0}_{m},\gamma_{m+1},\ldots,\gamma_d\},
 \qquad \gamma_i>0,                                         \tag{1}
\]
and
\[
 \operatorname{spec}(C_L-v_*I)=\{\delta_1,\ldots,\delta_d\},
 \qquad \delta_j>0.                                         \tag{2}
\]
Thus the winner ground multiplicity is \(1\le m\le d\), and the winner is
unique at the block level.  All dimensions and gaps are fixed while \(G\)
grows.

Consider
\[
 \min\left\{\langle C_*,Z_*\rangle+
       \sum_{g=2}^G\langle C_L,Z_g\rangle
       -\tau\sum_{g=1}^G\log\det Z_g:
       Z_g\succ0,\ \sum_g\operatorname{tr}Z_g=1\right\}.    \tag{3}
\]
If \(\lambda\) is the trace multiplier, put \(x=v_*-\lambda>0\) and
\[
 A(x)={m\over x}+\sum_{i=m+1}^d{1\over x+\gamma_i},
 \qquad B(x)=\sum_{j=1}^d{1\over x+\delta_j}.                \tag{4}
\]
The unique center is
\[
 Z_*=\tau(C_*-\lambda I)^{-1},\qquad
 Z_g=\tau(C_L-\lambda I)^{-1}\quad(g>1),                    \tag{5}
\]
where \(x\) is the unique positive solution of
\[
                         1=\tau\{A(x)+(G-1)B(x)\}.           \tag{6}
\]
The winner trace mass is \(p_G=\tau A(x)\).

The exact equations immediately give useful finite-\(G\) bounds.  Put
\(\delta_{\max}=\max_j\delta_j\).  Since \(B\) is decreasing,
\[
                 \boxed{p_G\ge1-\tau(G-1)B_0.}             \tag{6a}
\]
Moreover \(A(x)\le d/x\) and
\(B(x)\ge d/(x+\delta_{\max})\).  Thus, whenever \(p_G\ge p_0>0\),
\[
 x\le\frac{d\tau}{p_0},\qquad
 1-p_G\ge
 \frac{d\tau(G-1)}{\delta_{\max}+d\tau/p_0}.               \tag{6b}
\]
Consequently, for \(G\ge2\) and \(0<\varepsilon<1\),
\[
 \tau\le\frac{\varepsilon}{B_0(G-1)}
 \quad\Longrightarrow\quad p_G\ge1-\varepsilon,            \tag{6c}
\]
whereas, if \(G-1-\varepsilon/(1-\varepsilon)>0\),
\[
 p_G\ge1-\varepsilon
 \quad\Longrightarrow\quad
 \tau\le
 \frac{\varepsilon\delta_{\max}}
 {d\{G-1-\varepsilon/(1-\varepsilon)\}}.                  \tag{6d}
\]
Thus constant concentration requires \(\tau=O(1/G)\), and the transition
occurs on the \(1/G\) scale.

For fixed \(G\), let
\[
 A_{\rm reg}(0)=\sum_{i=m+1}^d\gamma_i^{-1}.
\]
Expansion of (6) at \(\tau=0\) gives
\[
 \begin{aligned}
 x&=m\tau+
 m\{A_{\rm reg}(0)+(G-1)B_0\}\tau^2+O_G(\tau^3),\\
 p_G&=1-(G-1)B_0\tau
       +m(G-1)\beta\tau^2+O_G(\tau^3).
 \end{aligned}                                             \tag{6e}
\]
The empty regular sum is zero when \(m=d\), so these formulas include that
edge case without modification.

## 2. General condensation threshold

Define
\[
 B_0=B(0)=\sum_j\delta_j^{-1},\qquad
 \beta=-B'(0)=\sum_j\delta_j^{-2},\qquad
 \alpha_*=B_0^{-1}.                                        \tag{7}
\]
Set \(\tau=\alpha/G\) with fixed \(\alpha>0\).  Direct expansion of (6)
gives the complete phase law:

* If \(0<\alpha<\alpha_*\), then
  \[
  {x\over\tau}\longrightarrow {m\over1-\alpha B_0},
  \qquad p_G\longrightarrow1-\alpha B_0.                   \tag{8}
  \]
* If \(\alpha=\alpha_*\), then
  \[
  \sqrt G\,x\longrightarrow\sqrt{m/\beta},
  \qquad \sqrt G\,p_G\longrightarrow\alpha_*\sqrt{m\beta}.
                                                                    \tag{9}
  \]
* If \(\alpha>\alpha_*\), there is a unique \(x_\alpha>0\) with
  \(B(x_\alpha)=1/\alpha\), and
  \[
  x\longrightarrow x_\alpha,
  \qquad Gp_G\longrightarrow\alpha A(x_\alpha).           \tag{10}
  \]

The proof is the same pole-versus-capacity calculation in all dimensions.
Below capacity, \(m/x\) supplies the missing trace.  At capacity,
\(\tau m/x\) balances \(\alpha_*\beta x\).  Above capacity, the winner term
vanishes after division by \(G\), leaving \(B(x_\alpha)=1/\alpha\).

## 3. Exact Hessian decomposition and finite sandwich

At the center, put \(D_*=C_*-\lambda I\) and
\(D_L=C_L-\lambda I\).  The Frobenius root Hessian on
\[
 \mathcal T=\{Y=(Y_1,\ldots,Y_G):\sum_g\operatorname{tr}Y_g=0\}
\]
has quadratic form
\[
 \mathcal Q(Y)={1\over\tau}\left{
       \operatorname{tr}(D_*Y_*D_*Y_*)+
       \sum_{g=2}^G\operatorname{tr}(D_LY_gD_LY_g)\right\}. \tag{11}
\]
In eigenbases of the costs, diagonal and off-diagonal symmetric coordinates
are orthogonal invariant subspaces.  An off-diagonal \((i,j)\) coordinate has
weight \(d_i d_j/\tau\), while a diagonal coordinate has weight
\(d_i^2/\tau\).  Only the diagonal coordinates are coupled by the trace
constraint.

Write \(\delta_{\min}=\min_j\delta_j\),
\(\delta_{\max}=\max_j\delta_j\), and let \(r\) be the multiplicity of
\(\delta_{\min}\).  If \(m<d\), also put
\(\gamma_{\min}=\min_{i>m}\gamma_i\).  Let
\[
 b(x)=\min\bigl(\{x+\delta_{\min}\}
       \cup\{x+\gamma_{\min}:m<d\}\bigr).                 \tag{12}
\]

If \(m\ge2\), a diagonal difference of two winner ground coordinates (or a
ground--ground off-diagonal coordinate) lies in \(\mathcal T\) and has
curvature \(x^2/\tau\).  No ambient weight is smaller, so
\[
                 \boxed{\lambda_{\min}(\mathcal Q|_{\mathcal T})
                         ={x^2\over\tau}\quad(m\ge2).}      \tag{13}
\]

Now suppose \(m=1\).  Let \(\lambda_{\rm diag}\) be the least curvature on
the diagonal trace hyperplane.  Writing the soft winner coordinate as \(a\)
and the other \(dG-1\) coordinates as \(z\), one has
\({\bf1}^Tz=-a\), hence \(\|z\|^2\ge a^2/(dG-1)\).  Conversely, cancel
\(a\) equally over the \(r(G-1)\) loser coordinates with gap
\(\delta_{\min}\).  This gives the finite bounds
\[
 {1\over\tau}{(dG-1)x^2+b(x)^2\over dG}
 \le\lambda_{\rm diag}\le
 {1\over\tau}{r(G-1)x^2+(x+\delta_{\min})^2
                    \over r(G-1)+1}.                       \tag{14}
\]
If \(m<d\), the winner has the feasible soft--stiff off-diagonal curvature
\[
                         {x(x+\gamma_{\min})\over\tau}.      \tag{15}
\]
Equations (14)--(15), together with the hard loser off-diagonal weights, imply
the uniform fixed-data law
\[
 \lambda_{\min}(\mathcal Q|_{\mathcal T})\asymp{1\over\tau}
 \begin{cases}
 \min\{x(x+\gamma_{\min}),\ x^2+(x+\delta_{\min})^2/G\},
       &m=1<d,\\
 x^2+(x+\delta_1)^2/G,&m=d=1.
 \end{cases}                                                \tag{16}
\]
The second line is the scalar-block case; there is no within-block
off-diagonal direction.

For \(G\ge3\), opposite maximum-eigenvector diagonal directions in two loser
blocks show
\[
 { (x+\delta_{\max})^2\over\tau}
 \le\lambda_{\max}(\mathcal Q|_{\mathcal T})
 \le{(x+\Lambda)^2\over\tau},                              \tag{17}
\]
where \(\Lambda=\max(\{\delta_j\}\cup\{\gamma_i:i>m\})\), omitting the
second set when \(m=d\).  Thus
\(\lambda_{\max}\asymp(x+\Lambda)^2/\tau\), with constants depending only
on the fixed spectral data.

The assumption \(m<d\) is needed only for the particular local soft--stiff
mode (15).  It is not needed for the diagonal sandwich, the condensation
transition, or the finite mass theorem below.  When \(m=d=1\), trace spread
over the losing blocks replaces (15).

## 4. Multiplicity-dependent conditioning phase law

Combining (8)--(10) with (13), (16), and (17) gives, for fixed \(\alpha>0\)
and \(G\to\infty\),
\[
 \boxed{
 \kappa_{\rm red}=\begin{cases}
 \Theta(G^2),&m\ge2,\ 0<\alpha<\alpha_*,\\
 \Theta(G),&m=1,\ 0<\alpha\le\alpha_*,\\
 \Theta(G),&m\ge2,\ \alpha=\alpha_*,\\
 \Theta(1),&\alpha>\alpha_*\quad\text{for every }m.
 \end{cases}}                                               \tag{18}
\]
At subcritical scale and \(m\ge2\), the ground--ground curvature is
\(x^2/\tau=\Theta(G^{-1})\), whereas hard loser curvatures are \(\Theta(G)\).
At criticality, \(x^2/\tau=\Theta(1)\).  For \(m=1\), the diagonal
trace-spread mode in (14) has curvature \(\Theta(1)\) on both sides of the
critical point up to and including equality.  Above capacity all shifted
gaps are bounded away from zero and all curvatures are \(\Theta(G)\).

## 5. Finite mass forces poor conditioning

> **Theorem (finite mass--conditioning obstruction).**  Fix the spectral data,
> \(p_0>0\), and sufficiently large \(G\).  If the exact center has winner
> mass \(p_G\ge p_0\), then
> \[
> \kappa_{\rm red}=\Omega_{p_0,\mathrm{data}}(G).
> \]
> If \(m\ge2\), the stronger conclusion
> \(\kappa_{\rm red}=\Omega_{p_0,\mathrm{data}}(G^2)\) holds.

**Proof.**  Since \(A(x)\le d/x\),
\[
                         x\le {d\tau\over p_0}.              \tag{19}
\]
Also \(B(x)\ge d/(x+\delta_{\max})\).  Equation (6) implies
\[
 \tau\le {\delta_{\max}\over d(G-1-1/p_0)}
          =O_{p_0,\mathrm{data}}(G^{-1}).                    \tag{20}
\]
For \(G\ge3\), (17) gives
\(\lambda_{\max}=\Omega(1/\tau)=\Omega(G)\).

If \(m=1\), choose the soft winner diagonal with coefficient one and put
coefficient \(-1/(G-1)\) on one fixed eigenvector in each loser.  This is a
trace-zero direction, and its Rayleigh quotient is
\[
 {x^2+(x+\delta_j)^2/(G-1)\over
       \tau\{1+1/(G-1)\}}
 =O_{p_0,\mathrm{data}}\left(\tau+{1\over\tau G}\right).    \tag{21}
\]
Together with \(\lambda_{\max}=\Omega(1/\tau)\), this gives
\[
 \kappa_{\rm red}
 =\Omega_{p_0,\mathrm{data}}
   \left({1\over\tau^2+1/G}\right)=\Omega(G),
\]
because (20) gives \(\tau=O(1/G)\).  Notice that the chosen Rayleigh
quotient need not be \(O(1)\) when \(\tau\ll1/G\); only its ratio to the
hard loser curvature is needed.  If \(m\ge2\), (13) and (19)--(20) give
\(\lambda_{\min}=x^2/\tau=O(G^{-1})\), proving the stronger quadratic
bound. \(\square\)

### Exact finite mass--conditioning inequalities

The asymptotic obstruction above has the following sharper finite form.  It
also shows directly how the conditioning is controlled by the observable
winner mass rather than by a prescribed temperature schedule.

> **Theorem (mass--conditioning law).**  Let \(G\ge3\), and let
> \(p=p_G\in(0,1)\) be the winner trace mass at an exact center.  Put
> \[
>                 R_G(p)={(G-1)p\over1-p}.                 \tag{MC1}
> \]
> Under (1)--(3):
>
> * if \(m\ge2\), then
>   \[
>                         \kappa_{\rm red}\ge R_G(p)^2;    \tag{MC2}
>   \]
> * if \(m=1<d\), then
>   \[
>    \kappa_{\rm red}\ge
>      \min\left\{1,{\delta_{\max}\over\gamma_{\min}}\right\}R_G(p);
>                                                               \tag{MC3}
>   \]
> * if \(m=d=1\), writing \(\delta=\delta_1\), then the condition
>   number is exactly
>   \[
>    \boxed{\displaystyle
>    \kappa_{\rm red}={G\over
>      1+(1-p)^2/\{(G-1)p^2\}}}.                            \tag{MC4}
>   \]
>
> For scalar blocks with \(G=2\), the tangent space is one-dimensional and
> \(\kappa_{\rm red}=1\); formula (MC4) is therefore asserted only for
> \(G\ge3\).

**Proof.**  The exact mass equations are
\[
 p=\tau A(x),\qquad 1-p=\tau(G-1)B(x).                    \tag{MC5}
\]
Because \(A(x)\le d/x\) and
\(B(x)\ge d/(x+\delta_{\max})\),
\[
 {1-p\over p}=(G-1){B(x)\over A(x)}
 \ge (G-1){x\over x+\delta_{\max}},
 \qquad
 {x+\delta_{\max}\over x}\ge R_G(p).                   \tag{MC6}
\]
For \(G\ge3\), opposite diagonal directions along a
\(\delta_{\max}\)-eigenvector in two loser blocks are trace zero, so
\[
 \lambda_{\max}\ge{(x+\delta_{\max})^2\over\tau}.        \tag{MC7}
\]
If \(m\ge2\), equation (13) says
\(\lambda_{\min}=x^2/\tau\); (MC2) follows from (MC6)--(MC7).

If \(m=1<d\), the winner ground--excited off-diagonal direction gives
\[
 \lambda_{\min}\le{x(x+\gamma_{\min})\over\tau}.
\]
For every \(x>0\),
\[
 {x+\delta_{\max}\over x+\gamma_{\min}}
 \ge\min\left\{1,{\delta_{\max}\over\gamma_{\min}}\right\}. \tag{MC8}
\]
Factoring the quotient of (MC7) by this upper bound on
\(\lambda_{\min}\), and then using (MC6), proves (MC3).

Finally suppose \(d=m=1\).  Set
\(a=x^2/\tau\) and \(b=(x+\delta)^2/\tau\).  On the scalar trace-zero
space, the \(G-2\) independent loser-difference directions have curvature
\(b\).  The remaining direction, which balances the winner against equal
changes in all losers, has curvature
\[
                         r={(G-1)a+b\over G}.              \tag{MC9}
\]
Since \(b>a\), these are respectively the largest and smallest eigenvalues.
Moreover, (MC5) reduces to
\[
 {x\over x+\delta}={1-p\over(G-1)p}.                      \tag{MC10}
\]
Thus \(\kappa_{\rm red}=b/r=G/\{1+(G-1)a/b\}\), and substitution of
(MC10) gives (MC4). \(\square\)

## 6. Scope

Identical losers are used to state a single sharp capacity \(B_0\) and to
attain the maximum curvature with two equal losing blocks.  Uniformly bounded
nonidentical loser spectra admit analogous empirical-resolvent limits, but
require convergence assumptions on their spectral distribution.  If some
\(\delta_j=0\), the winner is not spectrally unique and \(B(0)\) diverges;
the stated finite-capacity transition no longer applies.

All condition numbers are in the Frobenius root coordinate after equality
elimination.  They are not invariant under arbitrary input-dependent
preconditioning, and they do not describe the unreduced saddle KKT matrix.
The result is a structural log-barrier theorem, not by itself a quantum query
lower bound.

## 7. Literature and novelty calibration

The resolvent center is classical, and in fact has a closer statistical-
mechanical interpretation than the phrase ``Bose condensation'' alone suggests.
After combining the blocks into
\(Z=Z_*\oplus Z_2\oplus\cdots\oplus Z_G\), problem (3) minimizes energy
minus matrix Burg entropy, since \(\operatorname{tr}\log Z=\log\det Z\).
Ishihara, [*Derivation of density operators for generalized entropies with
quantum analysis*](https://arxiv.org/abs/1904.03363), equations (27)--(32),
derives the corresponding Burg maximum-entropy density operator under trace
and energy constraints.  It is an affine resolvent of the Hamiltonian.  Thus
(5)--(6), including their matrix form, should not be claimed as a new Gibbs
state or a new use of the log-determinant barrier.

The exact mode-level analogue is **Rayleigh--Jeans (RJ) condensation**.  Baudin
et al., [*Rayleigh--Jeans condensation of classical light: Observation and
thermodynamic characterization*](https://arxiv.org/abs/2007.11950), use modal
occupancies
\[
                         n_p={T\over \beta_p-\mu}.
\]
Their equations (2)--(7) describe the same reciprocal-gap pole, saturation of
the excited modes as the chemical potential reaches the spectral edge,
macroscopic ground-mode occupation, and finite-size smoothing.  Zanaglia et
al., [*Bridging Rayleigh--Jeans and Bose--Einstein condensation of a guided
fluid of light with positive and negative
temperatures*](https://arxiv.org/abs/2405.06531), explicitly distinguish RJ
from Bose--Einstein thermodynamics.  Bose--Einstein occupancies have an
exponential denominator; they reduce to reciprocal-gap weights only in an
appropriate high-occupancy limit.  Accordingly, the precise terminology for
Theorem 1 is a *matrix Burg* or *Rayleigh--Jeans condensation analogue*.
``Bose-like'' is acceptable as an analogy, but ``Bose--Einstein distribution''
and ``log-sum-exp soft minimum'' are not.

The inverse-gap capacity also has a direct spherical-model precedent.
Lukkarinen, [*Multi-state condensation in Berlin--Kac spherical
models*](https://arxiv.org/abs/1806.01806), equations (2.8)--(2.13), separates
a finite condensate sector from a critical Gaussian normal fluid.  Its critical
norm density is the average of the inverse excited-mode gaps, and its
fluctuation control contains the corresponding inverse-square sum.  These are
the statistical-mechanical counterparts of \(B_0\) and \(\beta\).  The same
paper treats several ground modes, so neither excited-mode saturation nor
multi-state condensation is new by itself.  Crisanti, Sarracino, and Zannetti,
[*Condensation vs Ordering: From the Spherical Models to BEC in the Canonical
and Grand Canonical Ensemble*](https://arxiv.org/abs/1909.03855), give further
context for the spherical/Bose analogy.

The critical \(G^{-1/2}\) law comes from balancing one pole against the first
nonzero Taylor coefficient of an analytic bath resolvent.  Finite-size rounding
of condensation transitions is classical, and square-root central-path rates
also occur in other SDP settings: da Cruz Neto, Ferreira, and Monteiro,
[*Asymptotic behavior of the central path for a special class of degenerate SDP
problems*](https://optimization-online.org/2003/07/682/), obtain
\(O(\sqrt\nu)\) behavior for a fixed degenerate class.  Their setting is not the
present joint limit: here the blocks and gaps are fixed, the instance dimension
grows, \(\tau=\alpha_*/G\), and the coefficient in (9) is obtained from a
simple soft pole against a replicated analytic bath.  The exponent alone must
therefore not be advertised as new.

Generic SDP Newton ill-conditioning near a low-rank optimum is also known.
Alizadeh, Haeberly, and Overton,
[*Primal-Dual Interior-Point Methods for Semidefinite Programming: Convergence
Rates, Stability and Numerical
Results*](https://doi.org/10.1137/S1052623496304700), Section 4, analyze the
rank and unbounded conditioning of a central-path Schur complement.  Zhang and
Lavaei, [*Modified Interior-Point Method for Large-and-Sparse Low-Rank
Semidefinite Programs*](https://arxiv.org/abs/1703.10973), identify a
low-rank perturbation responsible for an ill-conditioned SDP Hessian and build
a preconditioner.  Those results concern Schur systems or general low-rank SDP
structure, not the equality-reduced primal Frobenius Hessian used here.  They do
not give the \(\Theta(G)\) versus \(\Theta(G^2)\) ground-multiplicity split or
the finite winner-mass implication in Section 5.

The defensible candidate contribution is therefore narrow: the explicit
growing-\(G\) block-SDP critical coefficients, the ground-multiplicity-dependent
reduced-Hessian exponents, the finite mass--conditioning theorem, and their
conjunction with the visibility, preparation, and raw-query consequences in
this note and the sparse holonomy specialization.  The collision identities
and amplitude-amplification primitives are elementary or standard once the
mass law is known.  A targeted open-primary-source search through September 2,
2026 found no theorem with this complete optimization/QIPM conjunction.  This
is evidence against an obvious exact collision, not proof of priority; the
Burg resolvent, inverse-gap capacity, condensation mechanism, square-root
finite-size balance, and generic SDP ill-conditioning are all excluded from
the novelty claim.

## Output theorem: visibility depends only on winner mass and loser symmetry

The following statement is independent of the detailed spectra and of the
condensation asymptotics.  Let \(C_W,C_L\in\mathbb S^d\), let \(G\ge2\),
and fix \(\tau>0\).  Compare the two trace-one block log-det centers
\[
 \rho_0=\arg\min_{Z_g\succ0,\ \sum_g\operatorname{tr}Z_g=1}
 \sum_{g=1}^G\langle C_L,Z_g\rangle-\tau\sum_g\log\det Z_g              \tag{O1}
\]
and
\[
 \rho_1=\arg\min_{Z_g\succ0,\ \sum_g\operatorname{tr}Z_g=1}
 \langle C_W,Z_1\rangle+\sum_{g=2}^G\langle C_L,Z_g\rangle
 -\tau\sum_g\log\det Z_g.                                                \tag{O2}
\]
We identify a block tuple with its block-diagonal density matrix.  Write
\[
 \rho_0=\bigoplus_{g=1}^G L_0,\qquad
 \rho_1=W_1\oplus\bigoplus_{g=2}^G L_1,\qquad
 p=\operatorname{tr}W_1.                                                  \tag{O3}
\]
Uniqueness and permutation symmetry give
\[
 \operatorname{tr}L_0={1\over G},\qquad
 \operatorname{tr}L_1={1-p\over G-1}.                                    \tag{O4}
\]

> **Theorem O (central-state visibility and collision).**  The exact trace
> distance and the two-copy component-collision gap obey
> \[
> \boxed{\left|p-{1\over G}\right|
> \le D_{\rm tr}(\rho_0,\rho_1)
> \le\max\left\{p,{1\over G}\right\},}                                  \tag{O5}
> \]
> \[
> \boxed{c_1-c_0={ (Gp-1)^2\over G(G-1)},\qquad
> c_0={1\over G},\quad
> c_1=p^2+{(1-p)^2\over G-1}.}                                           \tag{O6}
> \]
> The collision measurement is public and acts only on two component-label
> registers.  Thus (O6) is unchanged by arbitrary internal degeneracy or by
> replacing the centers with arbitrary purifications and then discarding the
> purifying registers.

**Proof.**  Measuring the distinguished component gives (O5)'s lower bound.
For the upper bound, the KKT equations have scalar trace multipliers
\(\lambda_0,\lambda_1\) and
\[
 L_b=\tau(C_L-\lambda_bI)^{-1}\quad(b=0,1).                               \tag{O7}
\]
The two matrices are therefore Loewner ordered.  If
\(\lambda_1\le\lambda_0\), then \(L_1\preceq L_0\), and (O4) implies
\(p\ge1/G\).  Hence
\[
 (G-1)\|L_1-L_0\|_1=p-{1\over G},qquad
 \|W_1-L_0\|_1\le p+{1\over G}.
\]
Adding the block trace norms and dividing by two gives
\(D_{\rm tr}(\rho_0,\rho_1)\le p\).  If
\(\lambda_1\ge\lambda_0\), the order reverses, \(p\le1/G\), and the same
calculation gives the upper bound \(1/G\).  Finally, the component
distributions are respectively
\[
 (1/G,\ldots,1/G),qquad
 \left(p,{1-p\over G-1},\ldots,{1-p\over G-1}\right).
\]
The probability that two independent labels agree gives (O6) by direct
subtraction. \(\square\)

The Loewner argument is the only part of (O5) that uses the central-path
form.  The lower bound and collision identity require only a uniform
all-loser marginal and exchangeable losers under the one-winner promise.
In the usual lower-cost-winner situation \(p\ge1/G\), (O5) simplifies to
\[
                         p-{1\over G}\le D_{\rm tr}\le p.                \tag{O8}
\]
Thus winner mass determines state visibility up to the unavoidable uniform
background \(1/G\), regardless of the winner's eigenvalue multiplicities.

### Conditioning--visibility dichotomy

Combining Theorem O with the finite mass--conditioning law gives an exact
constraint on any attempt to make the central density informative while
keeping the unpreconditioned reduced Hessian well conditioned.  Write
\(\kappa=\kappa_{\rm red}\).  For \(G\ge3\), (MC2)--(MC4) imply
\[
 p\le {\sqrt\kappa\over G-1+\sqrt\kappa}
       \quad(m\ge2),                                      \tag{CV1}
\]
\[
 p\le {\kappa\over c(G-1)+\kappa},\qquad
 c=\min\{1,\delta_{\max}/\gamma_{\min}\}
       \quad(m=1<d),                                      \tag{CV2}
\]
and, for scalar blocks,
\[
 p={1\over1+\sqrt{G-1}\sqrt{G/\kappa-1}}
       \quad(d=m=1).                                      \tag{CV3}
\]
Together with (O5), each right-hand side, maximized with \(1/G\), is an
upper bound on \(D_{\rm tr}(\rho_0,\rho_1)\).  In particular, bounded
\(\kappa\) makes the winner state only \(O(1/G)\)-visible in both the
simple and degenerate cases.

Conversely, if \(D_{\rm tr}(\rho_0,\rho_1)\ge\nu>1/G\), then (O5) forces
\(p\ge\nu\), and hence
\[
 \kappa\ge\left({(G-1)\nu\over1-\nu}\right)^2
       \quad(m\ge2),
 \qquad
 \kappa\ge c{(G-1)\nu\over1-\nu}
       \quad(m=1<d).                                      \tag{CV4}
\]
Thus constant trace-distance visibility costs \(\Omega(G^2)\) conditioning
for a degenerate winner ground space and \(\Omega(G)\) for a simple one.
The same conclusion applies to any constant-gap collision decoder, because
(O6) can stay bounded away from zero only when \(p=\Omega(1)\).  These are
statements about the specified Frobenius-coordinate Hessian; an
input-dependent preconditioner can change its condition number, but its
construction and recovery costs are outside this structural implication.

### Approximate outputs and the raw-access corollary

Suppose a state-preparation algorithm returns \(\widetilde\rho_b\) with
\(D_{\rm tr}(\widetilde\rho_b,\rho_b)\le\epsilon\) under promise
\(b\in\{0,1\}\).  The tensor-product triangle inequality gives
\[
 D_{\rm tr}(\widetilde\rho_b^{\otimes2},\rho_b^{\otimes2})\le2\epsilon.
\]
Therefore the observed collision-probability gap is at least
\[
 \Delta_{\rm out}\ge { (Gp-1)^2\over G(G-1)}-4\epsilon.                 \tag{O9}
\]
Whenever this is a fixed positive constant, a constant number of public
collision experiments on fresh independent preparations distinguishes the
promises.  More quantitatively,
\(O(\Delta_{\rm out}^{-2})\) experiments suffice by ordinary concentration.

Consequently, if distinguishing the underlying all-loser and unique-winner
input promises has quantum query lower bound \(Q_*\), any preparation
circuit in a regime with \(\Delta_{\rm out}=\Omega(1)\) uses
\[
                              \Omega(Q_*)                                  \tag{O10}
\]
raw queries.  This reduction makes no verification query to the hidden
winner and remains valid for mixed outputs.  For the holonomy composition,
\(Q_*=\Theta(N\sqrt G)\).

### Symmetry-light collision theorem

The equal-loser formula above has a more general form that is useful outside
the exact log-det model.  Let a public component measurement have probabilities
\(w_1,\ldots,w_G\).  Suppose the no-winner target is uniform, while on every
unique-winner input the winning component \(a\) has mass \(w_a=q\ge p\),
where \(p\ge1/G\).  The losing masses need not be equal and may depend on the
whole input.  Cauchy--Schwarz gives
\[
 \sum_{g=1}^G w_g^2
 \ge q^2+{(1-q)^2\over G-1}
 \ge p^2+{(1-p)^2\over G-1}.                              \tag{O12}
\]
Consequently the collision gap is at least
\[
 d(p,G):={ (Gp-1)^2\over G(G-1)}.                         \tag{O13}
\]
Equality holds exactly when the winning mass is \(p\) and the losing mass is
uniform.  Thus loser exchangeability is needed for the identity (O6), but not
for the lower bound used by the decoder.  More generally, if the no-winner
collision probability is only known to be at most \(b\), then (O13) is
replaced by
\[
 p^2+{(1-p)^2\over G-1}-b.                                \tag{O14}
\]
This separated public statistic, rather than exact permutation symmetry, is
the minimal output-side hypothesis.

For example, if \(p\ge p_0>0\) and \(G\ge2/p_0\), then
\[
                         d(p,G)\ge {p_0^2\over4}.          \tag{O15}
\]
Combining (O9) and (O15), any fixed trace error
\(\epsilon<p_0^2/16\) leaves a positive constant gap.  If the surviving gap
is \(\Delta>0\), \(O(\Delta^{-2}\log(1/\delta))\) independent two-copy
experiments, each using fresh preparations, achieve failure probability at
most \(\delta\).  Hence, if one
preparation costs \(q\) raw queries and the promise decision problem costs
\(L\), this particular decoder gives
\[
                              q=\Omega(L\Delta^2).         \tag{O16}
\]
In the constant-gap regime, this is \(q=\Omega(L)\).

### Explicit unique-winner composition bound

Here is a self-contained source of \(L\).  Let \(f:\mathcal X_0\sqcup
\mathcal X_1\to\{0,1\}\) be a possibly partial Boolean predicate, where
\(\mathcal X_b=f^{-1}(b)\).  There are \(G\) independently queried blocks,
with promise sets
\[
 \mathcal P_0=\mathcal X_0^G,
 \qquad
 \mathcal P_1=\bigsqcup_{a=1}^G
 \mathcal X_0^{a-1}\times\mathcal X_1\times
 \mathcal X_0^{G-a}.                                      \tag{O17}
\]
Let \(F\) denote the promise Boolean function that is zero on
\(\mathcal P_0\) and one on \(\mathcal P_1\).
Write \(A=\operatorname{Adv}^{\pm}(f)\) in the block's raw query model.

> **Theorem P (unique-OR adversary and state preparation).**  In the query
> model in which one query addresses one coordinate of one block,
> \[
> \operatorname{Adv}^{\pm}(F)
>                              \ge A\sqrt G.               \tag{O18}
> \]
> Therefore a circuit that, on every promised input, prepares a state within
> trace distance \(\epsilon\) of targets satisfying the hypotheses of
> (O12) uses \(\Omega(A\sqrt G)\) raw queries whenever
> \(d(p,G)-4\epsilon=\Omega(1)\).  Equivalently, by tightness of the general
> adversary bound, the lower bound is
> \(\Omega(Q(f)\sqrt G)\), up to universal constants.

**Proof.**  Take the rectangular zero-to-one block \(B\), from rows indexed
by \(\mathcal X_0\) to columns indexed by \(\mathcal X_1\), of a feasible
general-adversary matrix for \(f\), normalized so that
\[
 \|B\|=A,
 \qquad \max_j\|B\circ\Delta_j\|\le1.                    \tag{O19}
\]
Here \(\Delta_j[x,y]=1\) exactly when inner query \(j\) has different
answers on \(x\) and \(y\).  For the sector of \(\mathcal P_1\) whose
winner is block \(a\), set
\[
 C_a=I_0^{\otimes(a-1)}\otimes B\otimes I_0^{\otimes(G-a)},
 \qquad C=[C_1\ C_2\ \cdots\ C_G],                        \tag{O20}
\]
and use the Hermitian adversary matrix
\[
                 \Gamma=\begin{pmatrix}0&C\\C^*&0\end{pmatrix}.       \tag{O21}
\]
The sectors are disjoint, and
\[
 CC^*=\sum_{a=1}^G I_0^{\otimes(a-1)}\otimes BB^*\otimes
                         I_0^{\otimes(G-a)}.               \tag{O22}
\]
The summands commute.  A top eigenvector of \(BB^*\), tensored \(G\)
times, is a common eigenvector, so \(\|\Gamma\|=A\sqrt G\).  Filtering
by raw query \((a,j)\) kills every winner sector other than \(a\), because
the row and column inputs agree in block \(a\) there.  In sector \(a\), the
remaining block is \(B\circ\Delta_j\), whose norm is at most one by (O19).
Thus \(\Gamma\) is feasible and proves (O18).  A constant number of the
collision experiments above turns any claimed constant-error preparation
circuit into a bounded-error algorithm for (O17), proving the state lower
bound. \(\square\)

The lower bound uses only the following oracle-side assumptions:

1. all Cartesian-product inputs in (O17) are valid;
2. one raw query addresses one coordinate of one block, coherently over its
   address, rather than returning an aggregate of several blocks;
3. both fibers of \(f\) are nonempty and its adversary value is \(A\);
4. the component projectors used by the collision measurement are public;
5. the target marginals satisfy (O12), or more generally have the separated
   collision statistics in (O14).

No coherent evaluator for \(f\), candidate-verification query, inverse
state-preparation oracle, or promise on the internal conditional states is
needed.  A clean evaluator matters only for a matching Grover upper bound.
For an optimization coefficient oracle, its raw simulation cost must be
charged explicitly: if one coefficient-oracle call can be simulated using at
most \(s\) raw queries, Theorem P gives
\[
                    \Omega\!\left({A\sqrt G\over s}\right)             \tag{O23}
\]
coefficient calls.  Supplying winner bits, a winner phase oracle, an
input-dependent component projector, or an aggregate multi-block primitive
at unit cost is a stronger access model and can remove the inner factor
\(A\).  In the fixed-position XOR oracle for the sparse holonomy family,
\(s=1\), including controlled and adjoint calls, and
\(f=\operatorname{PARITY}_N\) yields \(\Omega(N\sqrt G)\).

There is also a sufficient zero-query boundary for fixed-error state
contracts.
The all-loser center \(\rho_0\) is public.  By (O5), on the zero-or-one
promise the zero-query algorithm that always returns \(\rho_0\) is valid
whenever
\[
                         \epsilon\ge\max\{p,1/G\}.                        \tag{O24}
\]
Hence a scalar objective can retain a constant winner gap while its
trace-normalized central density carries no constant-error query lower bound.
The collision and distance statements apply to block-density outputs, not
to normalized vectorizations of the blocks, whose component probabilities
are Frobenius-norm rather than trace weights.

## Multiwinner capacity law

The same calculation has a useful \(k\)-winner form.  Let
\(v=\lambda_{\min}(C_W)\), suppose its multiplicity is \(m\ge1\), and assume

\[
                         C_L-vI\succ0.                                  \tag{M1}
\]

For \(x>0\), define

\[
 A(x)=\operatorname{tr}(C_W-vI+xI)^{-1},\qquad
 B(x)=\operatorname{tr}(C_L-vI+xI)^{-1}.                                \tag{M2}
\]

Then

\[
 A(x)={m\over x}+O(1),\qquad
 B(0)<\infty,\qquad
 \beta:=-B'(0)=\operatorname{tr}(C_L-vI)^{-2}>0.                         \tag{M3}
\]

If exactly \(k\) of the \(G\) blocks have cost \(C_W\), the common trace
multiplier can be written \(\lambda=v-x\), and normalization becomes

\[
 1=\tau\{kA(x)+(G-k)B(x)\}.                                             \tag{M4}
\]

The total trace on the \(k\) winners is

\[
                         p_{G,k}=\tau kA(x),qquad
                         1-p_{G,k}=\tau(G-k)B(x).                         \tag{M5}
\]

> **Theorem M (sublinear-number multiwinner transition).**  Let
> \(k=k_G\) satisfy \(1\le k=o(G)\), put \(\alpha=\tau G\), and keep
> \(\alpha>0\) fixed.  With \(\alpha_*=1/B(0)\),
> \[
> p_{G,k}\longrightarrow1-\alpha B(0)
>       \quad(0<\alpha<\alpha_*),                                      \tag{M6}
> \]
> \[
> p_{G,k}\sim \alpha_*\sqrt{m\beta\,{k\over G}}
>       \quad(\alpha=\alpha_*),                                        \tag{M7}
> \]
> and, for \(\alpha>\alpha_*\),
> \[
> p_{G,k}\sim \alpha A(x_\alpha){k\over G},qquad
> B(x_\alpha)={1\over\alpha}.                                        \tag{M8}
> \]
> Below criticality,
> \[
> x\sim{\alpha m k\over
>              G[1-\alpha B(0)]};                                     \tag{M9}
> \]
> at criticality, \(x\sim\sqrt{mk/(\beta G)}\).

**Proof.**  Divide (M4) by \(G\) and use \(\tau=\alpha/G\).  Below
criticality, \(x\to0\); otherwise the winner term vanishes because
\(k/G\to0\), while the loser term is at most \(\alpha B(0)<1\).  Equation
(M5) then gives (M6), and the pole in (M3) gives (M9).  At criticality,
write \(q=k/G\).  The two expressions for the winner mass give

\[
 p_{G,k}=q+{\beta\over B(0)}x+o(q+x)
          ={qm\over B(0)x}+O(q).                                      \tag{M10}
\]

Balancing them proves (M7) and the critical formula for \(x\).  Above
criticality, compactness and monotonicity force \(x\to x_\alpha>0\), and
(M5) gives (M8). \(\square\)

The hypothesis \(k=o(G)\) is substantive.  If \(k/G\to q\in(0,1]\), the
limiting equation is

\[
             1=\alpha\{qA(x)+(1-q)B(x)\},                              \tag{M11}
\]

whose solution stays positive.  The winner pole is already extensive, so
there is no singular capacity transition at fixed \(\alpha\).  The total
winner mass instead converges to \(\alpha qA(x)>0\).

### Nonidentical losing blocks

The mass transition does not require identical losers.  Let the \(G-k\)
losing costs have resolvent traces \(B_{\ell,G}(x)\), and define their
empirical bath resolvent
\[
 \overline B_G(x)={1\over G-k}\sum_{\ell\ {\rm losing}}B_{\ell,G}(x).
                                                                    \tag{M12}
\]
The exact normalization equation is obtained from (M4) by replacing \(B\)
with \(\overline B_G\).  Suppose \(k=o(G)\) and
\(\overline B_G\to B\) locally uniformly on \(x\ge0\), where
\(B(0)=B_0\in(0,\infty)\).  Then the subcritical and supercritical conclusions
(M6), (M8), and (M9) remain valid with this limiting \(B\).  At criticality,
also assume
\[
 \overline B_G(0)-B_0=o(\sqrt{k/G}),\qquad
 \overline B_G(x)=\overline B_G(0)-\beta x+r_G(x)
                                                                    \tag{M13}
\]
with \(\beta>0\), where for every fixed \(C>0\),
\[
 \sup_{0<x\le C\sqrt{k/G}}{|r_G(x)|\over x}\longrightarrow0.
\]
The same pole--bath
balance then gives (M7) and
\[
                         x\sim\sqrt{mk/(\beta G)}.          \tag{M14}
\]
These hypotheses are sufficient rather than necessary; (M13) records the
finite-size accuracy needed not to shift the critical window.

This empirical-resolvent extension concerns only the mass law.  Nonidentical
losers need not give a uniform no-winner marginal, exchangeable losing mass,
or public common internal states.  Therefore the exact visibility identity,
collision decoder, and coherent preparation theorem below do not transfer
without their own output-side symmetry or separated-statistic assumptions.

### Multiwinner state visibility

Fix a particular winner set \(S\subseteq[G]\) of size \(k<G\), and let
\(q=k/G\).  The group marginal of its center assigns mass \(p_{G,k}/k\) to
each winner and \((1-p_{G,k})/(G-k)\) to each loser.  Repeating the proof of
Theorem O gives

\[
 \boxed{|p_{G,k}-q|\le
 D_{\rm tr}(\rho_0,\rho_{S})
 \le\max\{p_{G,k},q\}.}                                                \tag{M15}
\]

The Loewner direction, and hence which entry realizes the maximum, is
determined by the two trace multipliers exactly as in Theorem O.  In the
usual resolvent-dominant case \(A(x)\ge B(x)\), one has \(p_{G,k}\ge q\),
so the upper bound is simply \(p_{G,k}\).

The public two-copy label-collision gap is

\[
 \boxed{c_S-c_0=
 {p_{G,k}^2\over k}+{(1-p_{G,k})^2\over G-k}-{1\over G}
 ={(Gp_{G,k}-k)^2\over Gk(G-k)}.}                                     \tag{M16}
\]

This exposes an important multiwinner limitation.  Constant total winner
mass gives a constant collision gap when \(k=O(1)\), but only
\(O(1/k)\) in general.  Pairwise trace distance in (M15) does not by itself
provide a common measurement for the unknown set \(S\).  A structure-specific
public observable can give a stronger decoder, but no such observable is
available in the abstract two-matrix model without an additional access
assumption.

## Coherent preparation by amplitude multiplication

Here is the precise regime in which the natural upper bound matches the
mass-access lower bound.  Assume:

1. \(1\le k<G\) is known and the promise is **exactly \(k\)** winners,
   not zero versus \(k\);
2. a clean coherent winner marker costs \(T_{\rm mark}\) raw queries;
3. \(C_W,C_L,G,k,\tau\) are public, so \(x,p_{G,k}\) and purifications of
   the normalized internal resolvents are query-free; and
4. controlled marker calls and the inverse preparation circuit are
   available.

Starting from the uniform group state, put
\[
 a_W={p\over k},\qquad a_L={1-p\over G-k},\qquad
 a_{\max}=\max\{a_W,a_L\}.                                      \tag{AP0}
\]
After computing the clean membership bit, accept a winner with amplitude
\(\sqrt{a_W/a_{\max}}\) and a loser with amplitude
\(\sqrt{a_L/a_{\max}}\).  The trial succeeds with probability
\(1/(Ga_{\max})\).  Exact phase-matched amplification in the ideal query
model, or fixed-point amplification to fixed error, therefore uses

\[
                    O\!\left(\sqrt{Ga_{\max}}+1\right)              \tag{AP1}
\]

marker calls.  When \(p\ge q:=k/G\), this becomes
\(O(\sqrt{Gp/k}+1)\); when \(p<q\), it is
\(O(\sqrt{G(1-p)/(G-k)}+1)\).  Fixed-point amplification to variable
error \(\epsilon\) adds the standard \(O(\log(1/\epsilon))\) factor.
Copy the group label to an environment
register so that the system marginal will be block diagonal.  A final clean
membership bit controls public constant-dimensional purifications of

\[
 \omega_W={W\over p/k},\qquad
 \omega_L={L\over(1-p)/(G-k)}.                                        \tag{AP2}
\]

Here \(W\) and \(L\) are the common unnormalized winner and loser blocks
of the exact center.  Computing and uncomputing the membership bit changes
only the constant.  Tracing out the copied label and local purifying
registers gives the required block-density output.  Thus a
coherent purification unitary satisfies

\[
 \boxed{Q_U=O\!\left(T_{\rm mark}
       [\sqrt{Ga_{\max}}+1]\right).}                                 \tag{AP3}
\]

Input-independent arbitrary rotations are free in the exact-query model;
finite-gate-set synthesis adds its usual precision dependence.  If internal
eigenvectors, the scalar multiplier, or normalized resolvent states are not
public, their loading cost must be added to (AP3).

Conversely, amplitude amplification from a prepared purification finds a
winner using

\[
 O\!\left({Q_U+T_{\rm mark}\over\sqrt p}\right)                       \tag{AP4}
\]

raw queries.  Let \(q_f\) be the bounded-error raw-query complexity of the
local winner predicate.  If independent block composition gives the
winner-finding lower bound \(\Omega(q_f\sqrt{G/k})\), then

\[
 \boxed{Q_U+T_{\rm mark}
       =\Omega\!\left(q_f\sqrt{Gp/k}\right).}                         \tag{AP5}
\]

When \(p\ge k/G\), equations (AP3)--(AP5) match up to constants whenever
\(T_{\rm mark}=\Theta(q_f)\) and \(\sqrt{Gp/k}\to\infty\).  A
deliberately inefficient marker cannot strengthen the lower bound.  When the
amplification factor is \(O(1)\), the additive marker call can already
saturate (AP5); the argument gives no nonzero lower bound on preparation
itself.  For mixed-state output without a coherent unitary and its inverse,
(AP4) is unavailable.  Independent copies give only the weaker repetition
tradeoff.

For a parity marker, \(T_{\rm mark}=\Theta(N)\) and adversary composition
gives winner-finding complexity
\(\Theta(N\sqrt{G/k})\).  The exactly-\(k\) preparation upper therefore has
the phase profile

\[
 Q_U=\begin{cases}
  \Theta(N\sqrt{G/k}),&0<\alpha<\alpha_*,\\
  \Theta(N(G/k)^{1/4}),&\alpha=\alpha_*,\\
  O(N),&\alpha>\alpha_*,
 \end{cases}                                                          \tag{AP6}
\]

for \(k=o(G)\), with the first two lines matched by (AP5) for an exact
operator-level purification unitary and inverse.  The same scaling is robust
to sufficiently small operator-level implementation error \(O(p)\) when
controlled inverse access remains available; a mere trace-close mixed-state
output is not covered by the extraction argument.  At criticality \(p\to0\),
so a fixed-error output contract does not inherit this matching lower bound.
The supercritical
\(O(N)\) upper follows from the general \(a_{\max}=\Theta(1/G)\) form
even if \(p<k/G\).

### Why this is not a zero-versus-\(k\) upper bound

The circuit behind (AP3) is promised that \(k\ge1\).  The all-loser branch
has a different trace multiplier and a different normalized loser
resolvent.  Amplitude multiplication tuned to the exactly-\(k\) branch does
not prepare that zero-winner center.  For the zero-versus-\(k\) promise there
are instead two rigorous generic bounds:

* exact search for existence followed by conditional preparation costs
  \(O(T_{\rm mark}\sqrt{G/k})\); and
* always outputting the public all-loser center costs zero queries and has
  trace error at most \(\max\{p_{G,k},k/G\}\) by (M15).

If the collision gap (M16), after subtracting output error as in (O9), is a
positive constant, the composed decision lower bound matches the first
upper bound.  This includes fixed \(k\) throughout the subcritical regime.
For growing \(k\), at criticality, or above criticality, collision may be too
weak and the public approximation may already meet a fixed-error contract.
Determining the optimal intermediate-accuracy zero-versus-\(k\) state
conversion complexity requires a state-conversion adversary analysis; it
does not follow from mass-access extraction alone.

## Robust approximate centrality

The exact capacity theorem survives a natural relative stationarity error.
This section also shows that the mass--conditioning obstruction is not an
artifact of exact centrality or simultaneous diagonalization.

Retain the notation of Sections 1--5.  For positive definite blocks
\(\widetilde Z_g\) and a scalar \(\widetilde\lambda<v_*\), put
\[
 x=v_*-\widetilde\lambda,\qquad
 D_*=C_*-\widetilde\lambda I,\qquad
 D_L=C_L-\widetilde\lambda I,\qquad
 \widetilde T=\sum_g\operatorname{tr}\widetilde Z_g,qquad
 \widetilde p={\operatorname{tr}\widetilde Z_*\over\widetilde T}.       \tag{R1}
\]
Assume the relative block residual and trace residual satisfy
\[
 E_g={1\over\tau}\widetilde Z_g^{1/2}D_g
                    \widetilde Z_g^{1/2}-I,qquad
 \max_g\|E_g\|_{\rm op}\le\eta<1,qquad
 |\widetilde T-1|\le\zeta<1.                                           \tag{R2}
\]

> **Theorem R (robust capacity, mass, and conditioning).**  Every point
> satisfying (R1)--(R2) obeys the noncommutative Loewner sandwich
> \[
> (1-\eta)\tau D_g^{-1}\preceq\widetilde Z_g
>       \preceq(1+\eta)\tau D_g^{-1}.                                  \tag{R3}
> \]
> Consequently, with \(B_0\) from (7) and \(\alpha=\tau G\),
> \[
> \boxed{\quad
> \widetilde p\ge
> 1-{(1+\eta)\tau(G-1)B_0\over1-\zeta}
> \ge1-{(1+\eta)\alpha B_0\over1-\zeta}.\quad}                        \tag{R4}
> \]
> Hence a positive \(G\)-independent winner-mass lower bound is forced for
> families having a uniform strict margin
> \((1+\eta)\alpha B_0\le1-\zeta-c\) with \(c>0\).  Conversely, any
> family with
> \(G\to\infty\), \(\alpha\to\bar\alpha\), and \(x\to0\) must satisfy
> \[
>                       (1-\eta)\bar\alpha B_0\le1+\zeta.               \tag{R5}
> \]
> Thus
> \[
> (1+\eta)\alpha B_0=1-\zeta,\qquad
> (1-\eta)\alpha B_0=1+\zeta                                           \tag{R6}
> \]
> bracket the critical surface permitted by this residual contract.
>
> There is also a robust conditioning obstruction.  Suppose \(d\ge2\),
> \(\widetilde p\ge p_0\in(0,1)\), and set
> \[
> q_0=p_0(1-\zeta),\qquad
> \Gamma_* =\lambda_{\max}(C_*-v_*I),\qquad
> \delta_{\max}=\lambda_{\max}(C_L-v_*I).                              \tag{R7}
> \]
> Then
> \[
> x\le {d(1+\eta)\tau\over q_0},                                      \tag{R8}
> \]
> and, whenever the denominator is positive,
> \[
> \boxed{\quad
> \tau\le { (1-p_0)(1+\zeta)\delta_{\max}\over
> d\bigl((1-\eta)(G-1)
> -(1-p_0)(1+\zeta)(1+\eta)/q_0\bigr)}.\quad}                         \tag{R9}
> \]
> In particular, fixed positive approximate winner mass forces
> \(\tau=O(G^{-1})\).
>
> At the approximate point, consider the actual log-det Hessian
> \[
> \widetilde{\mathcal H}[Y]_g
>   =\tau\widetilde Z_g^{-1}Y_g\widetilde Z_g^{-1},\qquad
> \mathcal T=\{Y:\sum_g\operatorname{tr}Y_g=0\}.                      \tag{R10}
> \]
> Its Frobenius-metric Rayleigh quotients on \(\mathcal T\) include one
> at least
> \[
>                     {\delta_{\min}^2\over(1+\eta)^2\tau}             \tag{R11}
> \]
> and one at most
> \[
>                     {d(x+\Gamma_*)\over(1-\eta)q_0}.                 \tag{R12}
> \]
> It follows that, uniformly for fixed
> \(p_0,\eta,\zeta,C_*,C_L\),
> \[
> \boxed{\quad
> \kappa(\widetilde{\mathcal H}|_{\mathcal T})
> \ge {\delta_{\min}^2(1-\eta)q_0\over
> d(1+\eta)^2\tau(x+\Gamma_*)}=\Omega(G).\quad}                       \tag{R13}
> \]
> If the winner ground multiplicity is \(m\ge2\), the stronger bound
> \[
> \boxed{\quad
> \kappa(\widetilde{\mathcal H}|_{\mathcal T})
> \ge {\delta_{\min}^2(1-\eta)^2\over
>             (1+\eta)^2x^2}=\Omega(G^2)\quad}                         \tag{R14}
> \]
> holds.

**Proof.**  Equation (R2) gives
\[
 (1-\eta)I\preceq {1\over\tau}\widetilde Z_g^{1/2}D_g
                    \widetilde Z_g^{1/2}\preceq(1+\eta)I.
\]
Congruence by \(\widetilde Z_g^{-1/2}\), inversion, and multiplication by
\(\tau\) prove (R3).  Since
\(D_L=C_L-v_*I+xI\succeq C_L-v_*I\),
\[
 \sum_{g=2}^G\operatorname{tr}\widetilde Z_g
 \le(1+\eta)\tau(G-1)\operatorname{tr}D_L^{-1}
 \le(1+\eta)\tau(G-1)B_0.
\]
Division by \(\widetilde T\ge1-\zeta\) proves (R4).  On the other hand,
the lower half of (R3) gives
\[
 \widetilde T\ge
 (1-\eta)\tau(G-1)\operatorname{tr}D_L^{-1}.                           \tag{R15}
\]
Taking the limit specified in (R5), and using
\(\operatorname{tr}D_L^{-1}\to B_0\), proves that claim.

Winner mass and the upper half of (R3) imply
\[
 q_0\le\operatorname{tr}\widetilde Z_*
 \le(1+\eta)\tau\operatorname{tr}D_*^{-1}
 \le {d(1+\eta)\tau\over x},
\]
which is (R8).  Every eigenvalue of \(D_L\) is at most
\(x+\delta_{\max}\).  Applying the lower half of (R3) only to the loser
blocks, and using
\((1-\widetilde p)\widetilde T\le(1-p_0)(1+\zeta)\), gives
\[
 (1-p_0)(1+\zeta)
 \ge{(1-\eta)\tau(G-1)d\over x+\delta_{\max}}.
\]
Substitution of (R8) and rearrangement prove (R9).

It remains to prove the curvature claims without assuming that
\(\widetilde Z_g\) commutes with \(C_g\).  In an eigenbasis of any loser
block \(\widetilde Z_g\), take a Frobenius-unit symmetric off-diagonal
matrix.  It is trace zero and therefore belongs to \(\mathcal T\).  The
upper half of (R3) and \(D_L\succeq\delta_{\min}I\) show that every
eigenvalue of this block is at most
\((1+\eta)\tau/\delta_{\min}\).  The chosen direction has curvature
\(\tau/(z_i z_j)\), proving (R11).

The largest eigenvalue of the winner block is at least \(q_0/d\), while
the lower half of (R3) shows that every winner eigenvalue is at least
\((1-\eta)\tau/(x+\Gamma_*)\).  A normalized off-diagonal direction
between a largest-eigenvalue eigenvector and any orthogonal eigenvector has
curvature at most (R12).  The ratio proves (R13), and (R8)--(R9) give its
asymptotic form.

Finally suppose \(m\ge2\).  The lower half of (R3), restricted to the
winner ground eigenspace, and the min--max principle imply that the two
largest eigenvalues of \(\widetilde Z_*\) are each at least
\((1-\eta)\tau/x\).  Their normalized off-diagonal direction has curvature
at most \(x^2/((1-\eta)^2\tau)\).  Comparing it with (R11) proves the
finite bound in (R14); (R8)--(R9) then give \(\Omega(G^2)\). \(\square\)

For completeness, scalar blocks also have a robust linear obstruction.
Let \(d=1\), \(G\ge3\), and retain
\(\widetilde p\ge p_0\in(0,1)\).  Bounds (R8)--(R9) remain valid with
\(d=1\).  A difference of two loser coordinates has curvature at least
\[
 {\delta_1^2\over(1+\eta)^2\tau}.                                  \tag{R16}
\]
Balancing a unit winner coordinate by \(-1/(G-1)\) in every loser gives a
trace-zero direction whose Rayleigh quotient is at most
\[
 {\tau\over q_0^2}
 +{(x+\delta_1)^2\over(1-\eta)^2\tau(G-1)}.                         \tag{R17}
\]
The quotient of (R16) by (R17), together with (R8)--(R9), is
\(\Omega(G)\).  Thus the robust \(\Omega(G)\) conclusion also holds for
scalar blocks, although the finite exact formula (MC4) is sharper at exact
centrality.

The relative metric in (R2) is essential.  A small unscaled stationarity
residual need not imply (R3) near a singular spectral edge.  Equations
(R13)--(R14) concern the unpreconditioned log-det Hessian in ambient
Frobenius coordinates; they are not lower bounds for every possible
input-dependent preconditioned Newton system.
