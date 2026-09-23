# Exact selection-free Hermitian exposed-rank frontier

Status: Proved; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High; targeted literature screen complete, specialist priority review still needed

## Result

Fix \(\mathbb F\in\{\mathbb R,\mathbb C,\mathbb H\}\),
\(a=\dim_{\mathbb R}\mathbb F\), an order cap \(R\geq2\), and
\(B=a(R-1)\), and assume \(s\geq2\).  For a finite relative-Slater affine lift
\(\mathcal L\) of \(B_2^s\) over a product of
\(\mathbb F\)-Hermitian PSD cones of orders at most \(R\) and rays, let
\(\mathcal D_{\mathcal L}(v)\) be the full normalized certificate fiber of
\(1-v^Tx\).  Set

\[
 {\cal R}(\mathcal L)=
 \max_{v\in S^{s-1}}\ \min_{Y\in\mathcal D_{\mathcal L}(v)}
        \sum_i\operatorname{rank}_{\mathbb F}Y_i.             \tag{1}
\]

Then

\[
 \boxed{\displaystyle
 \inf_{\mathcal L}{\cal R}(\mathcal L)
   =q_{\mathbb F,R}(s):=
       \left\lceil {s-1\over a(R-1)}\right\rceil.}            \tag{2}
\]

In fact, for every fixed lift there is a dense open semialgebraic set
\(U_{\mathcal L}\subseteq S^{s-1}\), whose complement has surface measure
zero, such that
\[
       \min_{Y\in\mathcal D_{\mathcal L}(v)}
       \sum_i\operatorname{rank}_{\mathbb F}Y_i\geq q
       \qquad(v\in U_{\mathcal L}).                           \tag{2a}
\]
The perspective construction has equality away from its north pole.
Consequently the stronger essential-infimum frontier is exact:
\[
 \boxed{\displaystyle
 \inf_{\mathcal L}\ 
 \operatorname*{ess\,inf}_{v\in S^{s-1}}
 \min_{Y\in\mathcal D_{\mathcal L}(v)}
 \sum_i\operatorname{rank}_{\mathbb F}Y_i=q.}                \tag{2b}
\]

Thus the generic curvature lower bound is the exact selection-free
support-certificate minimax over every real, complex, and quaternionic
Hermitian order cap.  It can be strictly smaller than the globally
bi-\(C^1\) value

\[
 \kappa_{\mathbb F,R}(s)=
 \begin{cases}
  1,&R=2,\ s=a+1,\\
  \lceil s/[a(R-1)]\rceil,&\text{otherwise}.
 \end{cases}                                                \tag{3}
\]

The gap is one exactly in the non-spin divisible cases
\(a(R-1)\mid s-1\).

For a finite repeatable mixed dictionary of Hermitian block types, put
\[
 B_{\max}=\max_i
   \{(\dim_{\mathbb R}\mathbb F_i)(R_i-1)\}.
\]
The identical argument gives the exact mixed-dictionary value
\(\lceil(s-1)/B_{\max}\rceil\): the lower bound uses each block's own
cross-Peirce dimension, and the perspective construction uses any type
attaining \(B_{\max}\).

For a shared-factor lift of
\(\prod_{d=1}^b B_2^{s_d}\), global-certificate compression gives a
simultaneous contact and genuine pure-row certificates \(Y^d\) such that
every positive weighted sum has rank at least

\[
                  \sum_{d=1}^b q_{\mathbb F,R}(s_d),        \tag{4}
\]

and every primal tuple in the final fiber has at least this total
nullity.  Equation (4) is an additive **existence** theorem.  It does not
claim additivity of the minimum rank in the full aggregate-objective
certificate fiber.

## 1. Universal local lower bound

Choose a primal boundary lift and a minimum-total-rank normalized
certificate semialgebraically.  On a common full-dimensional \(C^1\)
stratum of the support sphere, differentiate

\[
                 \sum_i\langle X_i(u),Y_i(v)\rangle=1-u^Tv. \tag{5}
\]

At contact put
\(p_i=\operatorname{rank}_{\mathbb F}X_i\) and
\(q_i=\operatorname{rank}_{\mathbb F}Y_i\).  Complementarity gives
\(p_i+q_i\leq r_i\).  The mixed cross-Peirce channel in block \(i\) has
real dimension \(a p_iq_i\), so the rank-\((s-1)\) sphere metric yields

\[
 s-1\leq a\sum_i p_iq_i
      \leq a(R-1)\sum_iq_i.                                \tag{6}
\]

Because the selected certificate has minimum total rank in its full
fiber, (6) proves
\({\cal R}(\mathcal L)\geq q_{\mathbb F,R}(s)\).  This argument is local
on a generic semialgebraic stratum and assumes no global selection.
More precisely, take a finite common \(C^1\) stratification of the two
semialgebraic selectors.  The union of its full-dimensional strata is a
dense open semialgebraic subset of the sphere, and each such stratum is
open in the sphere.  Hence the mixed derivative at every point of that
union sees the full tangent space and proves (6) pointwise there.  This
gives (2a).  Its complement has semialgebraic dimension at most \(s-2\)
and therefore surface measure zero.  The perspective upper in Section 2
then proves (2b).

## 2. Rotated Hermitian perspective attaining the bound

First take the divisible dimension

\[
                         s=qB+1.                            \tag{7}
\]

Write a projected point as \(x=(w,b)\), where
\(w=(w_G)_{G=1}^q\in(\mathbb F^{R-1})^q\), and put
\(\delta=1-b\).  Introduce real scalars \(z_G\), impose

\[
 X_G=
 \begin{pmatrix}
  \delta&w_G^*\\
  w_G&z_GI_{R-1}
 \end{pmatrix}\succeq0,\qquad
                         \sum_Gz_G=1+b.                    \tag{8}
\]

The Schur complement says

\[
 \delta\geq0,\quad z_G\geq0,\quad
                         \|w_G\|^2\leq\delta z_G.           \tag{9}
\]

Summing (9) proves \(\|w\|^2+b^2\leq1\).  Conversely, every ball point
with \(b<1\) is lifted by taking
\(z_G\geq\|w_G\|^2/(1-b)\) with the required sum; the north pole has the
simplex \(z_G\geq0,\sum z_G=2\).  Hence (8) is an exact full-Slater lift.

Let a support be \(v=(c,\eta)\in S^{s-1}\), with
\(c=(c_G)\).  Under the real trace pairing, write a dual block as

\[
 Y_G=\begin{pmatrix}\alpha_G&-c_G^*/2\\-c_G/2&Z_G\end{pmatrix}.
                                                               \tag{10}
\]

Coefficient matching is exactly

\[
 Z_G\succeq0,\quad \operatorname{tr}_{\mathbb F}Z_G=\Gamma
       ={1-\eta\over2},\qquad
 \sum_G\alpha_G={1+\eta\over2},\qquad Y_G\succeq0.          \tag{11}
\]

Indeed, (8), (10), and (11) give

\[
 \sum_G\langle X_G,Y_G\rangle
 =(1-b){1+\eta\over2}+(1+b){1-\eta\over2}
        -\operatorname{Re}\sum_G\langle w_G,c_G\rangle
 =1-v^Tx.                                                   \tag{12}
\]

If \(\eta<1\), take

\[
 \alpha_G={\|c_G\|^2\over2(1-\eta)}.                       \tag{13}
\]

When \(c_G\neq0\), choose \(Z_G\) so that (10) is the rank-one Gram
matrix with off-diagonal entry \(-c_G/2\); its trace is \(\Gamma\)
because \(\alpha_G\Gamma=\|c_G\|^2/4\).  When \(c_G=0\), set
\(\alpha_G=0\) and choose any rank-one \(Z_G\succeq0\) of trace
\(\Gamma\).  The sphere identity makes the values in (13) sum to
\((1+\eta)/2\).  At \(\eta=1\), take \(Z_G=0\) and distribute positive
\(\alpha_G\)'s with sum one.  Thus every support has a certificate of
total rank at most \(q\), while on the dense open set where every
\(c_G\neq0\), positivity forces every block to be nonzero and hence the
minimum rank is exactly \(q\).  This proves equality in (2) for (7).

For a nondivisible \(s-1\), use \(q=\lceil(s-1)/B\rceil\), restrict the
last \(w_G\) to the required real coordinate subspace, and repeat the same
construction.  The coefficient calculation and the dense-open rank count
are unchanged.

## 3. Additive shared-factor lower bound

Fix positive row weights.  Choose row contacts sequentially.  After rows
\(e<d\), let \(W_i^{d-1}\) be the sum of their selected certificate
ranges and compress the whole original row-\(d\) certificate fiber by the
orthogonal projection \(P_i^{d-1}\) onto
\((W_i^{d-1})^\perp\).  Whole-cylinder complementarity preserves the
exact row-\(d\) slack identity after compression.  Relative Slater
uniformly bounds the original normalized fibers, so their compressed
images are nonempty compact semialgebraic families with closed graph.

Apply the generic-stratum argument (5)--(6) in these compressed
Hermitian faces.  It selects an original pure-row certificate whose
compressed total rank is at least \(q_{\mathbb F,R}(s_d)\).  For
\(Y=CC^*\),

\[
 \operatorname{rank}_{\mathbb F}(PYP)
 =\dim_{\mathbb F}(W+\operatorname{Ran}_{\mathbb F}Y)
     -\dim_{\mathbb F}W.                                   \tag{14}
\]

The increments telescope.  Positive Hermitian range additivity then
proves (4), and final-fiber complementarity gives the stated nullity
bound.

## 4. Scope and barrier distinction

The theorem concerns exposed Jordan rank of genuine affine-slice support
certificates.  Its strongest QIPM-facing consequence is a
formulation-universal hard-objective movement lower bound in the
restricted standard-logdet metric.

For every lift \(\mathcal L\), choose a hard support \(v_*\) from (2), any
attained certificate \(S=(S_i)\in\mathcal D_{\mathcal L}(v_*)\), and any
fixed interior reference \(X^c\) in the reduced affine slice.  Put

\[
 Q=\sum_i\operatorname{rank}_{\mathbb F}S_i\geq q,\qquad
 \Delta_c=Q\left[
  \prod_{i:S_i\ne0}
   \det_{c_i}(S_i)
   \det_{c_i}\!\bigl(P(c_i)X_i^c\bigr)
 \right]^{1/Q},                                             \tag{15}
\]

where \(c_i\) is the support idempotent of \(S_i\).  The audited
support-principal-minor theorem gives, for the entire lifted
\(\epsilon\)-objective-gap set,

\[
 d_F\!\left(X^c,\{X:1-v_*^T\pi X\leq\epsilon\}\right)
 \geq\left[\sqrt Q\log{\Delta_c\over\epsilon}\right]_+.
                                                               \tag{16}
\]

By (2a), the same statement with \(Q\geq q\) holds separately for every
fixed support in \(U_{\mathcal L}\), hence for surface-almost every
support objective.  The certificate and \(\Delta_c\) may depend on that
support; no support-uniform additive constant is claimed.

In particular, for \(0<\epsilon\leq1\),

\[
 d_F\geq
 \left[\sqrt q\log(1/\epsilon)-C_{\mathcal L,X^c,S}\right]_+,
 \quad
 C_{\mathcal L,X^c,S}
   =\sqrt Q\,\bigl[\log(1/\Delta_c)\bigr]_+.                \tag{17}
\]

The finite additive constant is formulation-, reference-, and
certificate-dependent; it is not claimed uniform over all lifts.
The coefficient \(\sqrt q\) is uniform, but the lower bound becomes
asymptotic only once \(\epsilon\) is below the lift-dependent scale
\(\Delta_c\).  Neither the hard support \(v_*\), the scale \(\Delta_c\),
nor a warm-start distance is uniform over formulations.

More generally, if a counted outer round has intrinsic displacement at
most \(B_0\), the start satisfies \(d_F(X_0,X^c)\leq D_0\), and the last
iterate is \(\epsilon\)-optimal for \(v_*\), then

\[
 T\geq
 {\left[\sqrt Q\log(\Delta_c/\epsilon)-D_0\right]_+\over B_0}.
                                                               \tag{18}
\]

For the concrete chord model, fix \(0\leq\rho<1\), \(0<\theta<1\), and
an integer \(m\geq1\).  If
\(\|X_0-X^c\|_{X^c}\leq\rho\) and every round contains at most \(m\)
feasible chords of starting-point Dikin norm at most \(\theta\), then

\[
 T\geq
 {\left[
  \sqrt Q\log(\Delta_c/\epsilon)-\log(1/(1-\rho))
 \right]_+\over
  m\log(1/(1-\theta))}.                                    \tag{19}
\]

Thus, for fixed \(\rho,\theta,m,\mathcal L,X^c,S\), the hard support needs
\(\Omega(\sqrt q\log(1/\epsilon))\) bounded-Dikin rounds.  This is an
outer-movement obstruction for algorithms represented by the stated
metric or chord model.  It is not an unrestricted QIPM runtime or query
lower bound, and it must not be multiplied by an independent query lower
bound without a same-instance composition theorem.

With one \(\theta\)-Dikin chord per round and an arbitrary start satisfying
\(d_F(X_0,X^c)\leq D_0\), the exact specialization of (18) is
\[
 T\geq{\left[\sqrt Q\log(\Delta_c/\epsilon)-D_0\right]_+
              \over-\log(1-\theta)}.                       \tag{19a}
\]

The order of quantifiers has a useful constant-free asymptotic form.  Let
\({\cal N}_{\mathcal L,X_0}^{\theta}(v,\epsilon)\) be the minimum number
of feasible forward \(\theta\)-Dikin chords, in the restricted standard
metric of \(\mathcal L\), needed to move from a fixed interior
\(X_0\) to objective gap at most \(\epsilon\) for support \(v\).
The lift and start are fixed before \(\epsilon\downarrow0\).  Then

\[
 \boxed{
 \inf_{\mathcal L,X_0}\ 
 \liminf_{\epsilon\downarrow0}\ 
 \sup_{v\in S^{s-1}}
 { {\cal N}_{\mathcal L,X_0}^{\theta}(v,\epsilon)
       \over\log(1/\epsilon)}
 \geq {\sqrt q\over-\log(1-\theta)}.}                     \tag{19b}
\]

Indeed, for each fixed lift the hard support, \(\Delta_c\), and the
finite start/reference distance may depend on that lift, but these
constants disappear after division by \(\log(1/\epsilon)\).  Equation
(19b) does not allow the lift or start to vary with \(\epsilon\), and it
does not assert one support or one accuracy threshold uniform over lifts.
If a counted outer round contains at most \(m\) such chords, divide the
right side by \(m\).

There is an objective-specific metric sharpness example, but not a
uniform algorithmic matching theorem.  For the perspective construction,
choose a support away from the north pole with every group \(c_G\ne0\).  Its
certificate is unique with total rank \(q\), its primal boundary fiber is
unique, and every primal block has nullity one.  The feasible segment from
a fixed Slater point to this boundary tuple has objective gap linear in
the segment parameter and standard-logdet length

\[
                    \sqrt q\log(1/\epsilon)+O(1).          \tag{20}
\]

Together with (16), this proves the exact asymptotic
\(\sqrt q\) **intrinsic-distance** coefficient for that fixed formulation
and objective.  The segment is not asserted to be a central path, a
warm-started QIPM trajectory, or an efficiently generated schedule.
For this perspective itself, a generic standard-barrier path-following
upper uses \(q\) order-\(R\) blocks and hence
\(\nu_{\rm ambient}=qR\).  Restriction gives
\(\nu_{\rm std,slice}\leq qR\), so that formulation's generic upper is
\[
                    O\!\left(\sqrt{qR}\log{qR\over\epsilon}\right).
                                                               \tag{21}
\]
No claim \(\nu_{\rm std,slice}\asymp q\) is made for the perspective.

The **minimax over lifts** nevertheless has a matching upper independent
of \(R\).  Use the audited grouped Hermitian Schur lift, except in the
rank-two spin cases in (3), where one uses the direct Hermitian/Lorentz
ball slice.  In either case its exact parameter is
\[
 g=\kappa_{\mathbb F,R}(s)
   \in\{q,q+1\},\qquad g\leq q+1\leq2q.                    \tag{22}
\]
At the analytic center of the grouped lift, \(s_G=1/g,w_G=0\), the dual
local norm of every unit support objective is \(1/\sqrt{2g}\); for the
direct spin slice it is \(1/\sqrt2\).  Thus the initial central-path scale
is uniform over the support sphere.  The standard approximate-centrality
gap bound is \(O(g/t)\), with a universal constant, so the terminal scale
needed for objective gap \(\epsilon\) is \(O(g/\epsilon)\), again uniformly
over the support.

A fixed-neighborhood short-step schedule can be chosen so that every
Newton update has starting-point local norm at most any prescribed
\(0<\theta<1\).  Such an update is a feasible forward
\(\theta\)-Dikin chord: local norm below one puts its endpoint in the
Dikin ellipsoid, and the whole segment is feasible by convexity.
Equivalently, one may subdivide the feasible line segments of a
conventional universal short-step schedule into \(O_\theta(1)\) such
chords.  Consequently the fixed analytic-center start works for every
support objective and uses
\[
                   O_\theta\!\left(\sqrt g\log{g\over\epsilon}\right)
        =O_\theta\!\left(\sqrt q\log{q\over\epsilon}\right) \tag{23}
\]
forward \(\theta\)-Dikin chords.  Consequently, for fixed problem
parameters before \(\epsilon\downarrow0\), (19b) and (23) give the sharp
minimax asymptotic order
\[
 { \sqrt q\over-\log(1-\theta)}
 \leq\inf_{\mathcal L,X_0}\liminf_{\epsilon\downarrow0}
   {\sup_v{\cal N}_{\mathcal L,X_0}^{\theta}(v,\epsilon)
      \over\log(1/\epsilon)}
 \leq\inf_{\mathcal L,X_0}\limsup_{\epsilon\downarrow0}
   {\sup_v{\cal N}_{\mathcal L,X_0}^{\theta}(v,\epsilon)
      \over\log(1/\epsilon)}
 \leq C_\theta\sqrt q.                                      \tag{24}
\]
The constants in (24) depend on the fixed Dikin-neighborhood convention,
not on \(R\) or on the support.  The lift, start, and problem parameters
\(s,R,\mathbb F\) are fixed before \(\epsilon\downarrow0\); (24) makes no
joint uniform claim when those parameters vary with \(\epsilon\).
Equation (23) is a standard-barrier upper construction, not a
query-complexity upper, and (24) does not multiply movement and query
costs.

This is not the exact restricted standard-barrier parameter.  In the
divisible cases, the perspective fiber at the north pole contains zero
blocks at simplex vertices, and those high-nullity points can make the
global parameter strictly larger than the favorable exposed rank.  The
companion standard-barrier theorem proves the grouped barrier value in
all nondivisible, all unbounded divisible, and all one-channel cases; only
bounded projection-singular divisible cases with \(q\geq2\) remain open.

## 5. Literature boundary and novelty caution

The ambient language of affine cone lifts and support certificates is
classical. Gouveia--Parrilo--Thomas,
[*Lifts of Convex Sets and Cone
Factorizations*](https://arxiv.org/abs/1111.3164), identify proper cone
lifts with factorizations of the slack operator. Fawzi--Gouveia--Parrilo--
Robinson--Thomas,
[*Positive Semidefinite Rank*](https://arxiv.org/abs/1407.4095), develop
real PSD rank and its geometric interpretations. Gribling--de Laat--
Laurent,
[*Lower Bounds on Matrix Factorization Ranks via Noncommutative Polynomial
Optimization*](https://doi.org/10.1007/s10208-018-09410-y), treat both real
PSD and complex Hermitian factorization rank. Dannemüller--Netzer,
[*Lifts of Operator Systems*](https://arxiv.org/abs/2508.15348), extend slack
operators and lift--factorization equivalence to matrix levels and free
spectrahedrops over complex Hermitian PSD cones. These theories optimize a
global factorization size or free-level lift. They do not, in the screened
statements, minimize the total rank inside the entire normalized certificate
fiber separately at each scalar support and then maximize over supports as
in (1).

The capped-block literature optimizes different resources. Fawzi--Parrilo,
[*Exponential Lower Bounds on Fixed-Size PSD Rank and Semidefinite Extension
Complexity*](https://arxiv.org/abs/1311.2571), count fixed-order real PSD
blocks for hard polytopes. Averkov,
[*Optimal Size of Linear Matrix Inequalities in Semidefinite Approaches to
Polynomial Optimization*](https://arxiv.org/abs/1806.08656), defines
semidefinite extension degree through the largest real LMI order.
Saunderson,
[*Limitations on the Expressive Power of Convex Cones without Long Chains
of Faces*](https://arxiv.org/abs/1902.06401), uses neighborliness and face
chains to obstruct product lifts, while Fawzi--Safey El Din,
[*A Lower Bound on the Positive Semidefinite Rank of Convex
Bodies*](https://arxiv.org/abs/1705.06996), uses algebraic-boundary degree
to lower-bound one PSD lift order. None of these screened sources retains
the objective-wise certificate rank, the cross-Peirce capacity
\(a p_iq_i\), or the minimax quantifier order in (1)--(2). In particular,
the real/complex sources do not state the all-field value
\(\lceil(s-1)/(a(R-1))\rceil\). Schmieta--Alizadeh,
[*Associative and Jordan Algebras, and Polynomial Time Interior-Point
Algorithms for Symmetric
Cones*](https://doi.org/10.1287/moor.26.3.543.10582), already extend PSD
interior-point analysis and Jordan-rank operations to complex and
quaternionic Hermitian cones; those all-field algebraic primitives are not
new here. Their paper does not study affine-lift certificate-rank minimax.
The quaternionic lift/factorization priority question still needs specialist
review.

The rotated Hermitian perspective in Section 2 is a classical
Schur-complement modelling device, not a new primitive. What was not
located is the exact selection-free lower bound matching it for every
finite relative-Slater affine product lift, nor the mixed-dictionary and
sequential-compression consequences. Searches for PSD rank of the
Euclidean-ball slack operator, minimum-rank dual certificates of ball
lifts, and exposed-rank curvature did not locate this formula.

For the movement corollary, Nesterov--Todd,
[*On the Riemannian Geometry Defined by Self-Concordant
Barriers*](https://doi.org/10.1023/A:1012446908930), gives the classical
conversion from bounded Dikin chords to barrier-metric distance.
Nesterov--Nemirovski,
[*Primal Central Paths and Riemannian Distances for Convex
Sets*](https://doi.org/10.1007/s10208-007-9019-4), compare central paths,
geodesics, and target sets, and Permenter,
[*A Geodesic Interior-Point Method for Linear Optimization over Symmetric
Cones*](https://arxiv.org/abs/2008.08047), develops a geodesic IPM. These
works do not give the support-principal-minor distance lower bound (16)
with coefficient equal to exposed certificate rank.

Quantum IPM papers such as Kerenidis--Prakash,
[*A Quantum Interior Point Method for LPs and
SDPs*](https://arxiv.org/abs/1808.09266), and Augustino--Nannicini--Terlaky--
Zuluaga,
[*Quantum Interior Point Methods for Semidefinite
Optimization*](https://arxiv.org/abs/2112.06025), establish algorithmic
upper bounds and analyze conditioning, feasibility, and quantum state
readout. They do not prove a formulation-universal hard-objective movement
lower bound. Thus (18)--(19b) should be advertised only as a lower bound
for the stated standard-logdet metric or bounded-chord model, not as a
quantum query or runtime lower bound.

The safe label after this targeted primary-source screen is **candidate
exact selection-free Hermitian support-certificate frontier and movement
synthesis**. It is not a new general PSD-rank, extension-degree,
self-concordant-distance, or unrestricted-QIPM lower-bound theorem. The
screen was targeted rather than exhaustive, and the quaternionic and
specialist factorization literatures remain the main priority checks.

## Audit checklist

1. Verify the factor \(a\) and the minimum-rank generic selection in (6).
2. Check quaternionic trace-pairing constants in (10)--(13).
3. Check exact projection/full Slater and all pole certificate cases.
4. Check that the nondivisible coordinate restriction preserves the
   all-support upper and dense-open lower.
5. Check the all-field compressed-range increment and the precise
   aggregate quantifier in (4).
6. Check the repeatable mixed-dictionary corollary.
7. Check the reference constant and bounded-round denominators in
   (15)--(19), and the perspective matching path (20).

## Independent hostile audit

The audit verified the real cross-Peirce factor
\(a p_iq_i\) and the use of a semialgebraic minimum-rank selector on a
common full-dimensional stratum.  In the rotated perspective construction,
the real trace pairing over \(\mathbb H\) counts the two conjugate
off-diagonal blocks once each, so the factor \(1/2\) in (10) gives exactly
\(-\operatorname{Re}\langle w_G,c_G\rangle\).  The rank-one Gram choice
has lower block
\(c_Gc_G^*/(4\alpha_G)\), whose real trace is
\((1-\eta)/2\); the zero-group, north-pole, and south-pole cases all have
the claimed rank.  The Schur inequalities project exactly to the ball,
and \(b=0,w=0,z_G>0\) supplies full Slater.

Restricting the last group to a nonzero real coordinate subspace changes
neither coefficient matching nor the dense-open condition
\(c_G\ne0\).  For the product theorem, whole-cylinder complementarity
preserves the pure-row slack after compression, and relative Slater
uniformly bounds the original certificate fibers.  The identity (14)
holds over all three division algebras via \(Y=CC^*\), while positivity
identifies the range of every positive aggregate with the span of the
individual ranges.  This proves exactly the additive-existence
quantifier in (4), not a minimum over the aggregate fiber.  The
mixed-dictionary lower and perspective upper both use the same maximal
capacity \(B_{\max}\).  The audit returned **PASS**.

The QIPM-facing extension (15)--(20) was audited separately.  The
support-minor constant in (15) has the correct determinant factors and
power \(1/Q\).  For \(0<\epsilon\leq1\),
\(\sqrt Q\geq\sqrt q\) gives (17) with exactly the stated positive-part
constant.  Triangle inequality gives (18).  A starting local displacement
\(\rho<1\) costs at most \(-\log(1-\rho)\), and each forward
\(\theta\)-Dikin chord costs at most \(-\log(1-\theta)\), which verifies
both denominators in (19).

At a generic support of the perspective lift, the trace and Schur
equalities force every \(\alpha_G\), \(Z_G\), and primal \(z_G\)
uniquely.  Each of the \(q\) primal blocks has one eigenvalue vanishing
linearly along the segment from a fixed Slater point, while objective
error is linear in the same segment parameter.  Hence its metric speed
has leading norm \(\sqrt q/t\), proving (20).  The audit returned
**PASS** and confirmed that no query-cost multiplication is implied.

The minimax extension (19b)--(24) was then hostile-audited.  For each
fixed pair \((\mathcal L,X_0)\), one hard support supplied by (2) works for
all \(\epsilon\); its formulation-dependent certificate scale and finite
start/reference distance vanish after division by
\(\log(1/\epsilon)\).  Hence the order
\(\inf_{\mathcal L,X_0}\liminf_{\epsilon\downarrow0}\sup_v\) in (19b) is
valid and does not permit a lift chosen as a function of accuracy.  The
inequality from that infimum-liminf to the corresponding infimum-limsup
in (24) follows pointwise.

For the upper bound, the grouped Schur construction has exact parameter
\(g=\lceil s/[a(R-1)]\rceil\), except in the stated direct rank-two spin
cases, and \(g\leq q+1\leq2q\).  The analytic-center local norm and the
standard \(O(g/t)\) centrality gap bound above are uniform over unit
supports.  Fixed-neighborhood Newton updates are feasible forward Dikin
chords after choosing the neighborhood for \(\theta\), or after a fixed
\(O_\theta(1)\) subdivision.  This proves the upper coefficient
\(C_\theta\sqrt q\), independent of \(R\), for fixed problem parameters.
The audit therefore found no change to (19b)--(24), but corrected the
construction label in the spin exceptions and made the chord and
uniformity hypotheses explicit.

The generic strengthening (2a)--(2b) received two independent re-audits.
The minimum-rank certificate incidence and a primal incidence admit a
common finite semialgebraic \(C^1\) stratification.  Every
full-dimensional stratum is open in the support sphere, so the mixed
Peirce rank inequality holds pointwise on their dense-open union; its
complement has surface measure zero.  For the perspective construction,
the Schur and trace equalities give minimum certificate rank \(q\) for
every support below the north pole.  This verifies both the dense-open
claim and the exact essential-infimum formula.  The same audits rechecked
the quantifier order in (19b)--(24): one lift-dependent hard support works
for all accuracies, while its fixed scale and start-distance constants
vanish after normalization by \(\log(1/\epsilon)\).  Both audits returned
**PASS**.
