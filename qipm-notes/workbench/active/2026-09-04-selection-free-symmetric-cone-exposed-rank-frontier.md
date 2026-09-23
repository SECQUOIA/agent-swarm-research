# Exact selection-free exposed-rank frontier for symmetric cones

Status: Proved; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High for the theorem; targeted primary-source priority screen complete,
but specialist priority review remains necessary

## Result

Fix \(s\geq2\) and a finite repeatable dictionary of simple symmetric cones
and optional nonnegative rays.  For a non-ray factor \(K_i\), let \(V_i\) be
its Euclidean Jordan algebra, \(r_i\) its rank, and \(a_i\) its Peirce
constant.  Put

\[
 B=\max_i a_i(r_i-1)>0,
 \qquad q_B(s)=\left\lceil {s-1\over B}\right\rceil .       \tag{1}
\]

For a finite relative-Slater affine lift \(\mathcal L\) of the Euclidean ball
\(B_2^s\) by factors from the dictionary, let
\(\mathcal D_{\mathcal L}(v)\) be the full fiber of genuine normalized
positive certificates for the support slack \(1-v^Tx\).  Define

\[
 {\cal R}(\mathcal L)=
 \max_{v\in S^{s-1}}\ \min_{Y\in\mathcal D_{\mathcal L}(v)}
       \sum_i\operatorname{rank}_JY_i .                     \tag{2}
\]

Then

\[
 \boxed{\displaystyle
   \inf_{\mathcal L}{\cal R}(\mathcal L)=q_B(s).}           \tag{3}
\]

In fact, every fixed lift has a dense open semialgebraic subset of supports,
whose complement has surface measure zero, on which every certificate has
total Jordan rank at least \(q_B(s)\).  The construction below has minimum
certificate rank exactly \(q_B(s)\) at every support except one pole.  Hence
the corresponding essential-infimum frontier is, more explicitly,

\[
 \inf_{\mathcal L}\operatorname*{ess\,inf}_{v\in S^{s-1}}
 \min_{Y\in\mathcal D_{\mathcal L}(v)}
       \sum_i\operatorname{rank}_JY_i=q_B(s),              \tag{3a}
\]

where essential infimum is with respect to surface measure.  The assumption
\(s\geq2\) is necessary for the displayed definition (1): for \(B_2^1\),
every normalized support certificate is nonzero and the frontier is \(1\),
not \(q_B(1)=0\).

This includes every simple Euclidean Jordan algebra.  In particular, for the
Albert cone \(H_+^3(\mathbb O)\), \(r=3\), \(a=8\), and \(B=16\), so

\[
 \inf_{\mathcal L}{\cal R}(\mathcal L)
       =\left\lceil {s-1\over16}\right\rceil               \tag{4}
\]

when Albert factors may be repeated.  For a spin factor of dimension
\(m+2\), \(r=2\), \(a=m\), and \(B=m\).

## 1. Selection-free lower bound

Choose a primal boundary lift and a minimum-total-rank normalized certificate
semialgebraically.  A finite common stratification makes both selectors
\(C^1\), with locally constant Jordan ranks, on a dense open subset of the
support sphere.  Its complement is lower-dimensional semialgebraic and hence
surface-null.  Differentiating the
whole-slice identity

\[
        \sum_i\langle X_i(u),Y_i(v)\rangle=1-u^Tv           \tag{5}
\]

at a contact gives the full rank-\((s-1)\) mixed sphere metric.  If the
primal and dual support idempotents in block \(i\) have ranks \(p_i\) and
\(q_i\), complementarity gives \(p_i+q_i\leq r_i\).  The mixed Peirce space
between them has real dimension \(a_ip_iq_i\).  Therefore

\[
 s-1\leq\sum_i a_ip_iq_i
      \leq\sum_i a_i(r_i-1)q_i
      \leq B\sum_iq_i .                                    \tag{6}
\]

Ray blocks have no cross-Peirce channel and contribute zero to the first sum
in (6).  This argument uses only Peirce calculus and is valid for the Albert algebra.
It also remains valid after reduction to a proper face: every surviving
simple face has cross-Peirce capacity at most that of its parent.  Equation
(6) proves the lower bound in (3), generically for each lift and hence for the
maximum in (2), without a globally smooth certificate sheet.

## 2. A universal Peirce-perspective lemma

Let \(V\) be a simple EJA of rank \(r\geq2\), let \(c\) be primitive, and
write \(d=e-c\).  Give \(V(c,1/2)\) its trace-inner-product norm

\[
                 \|w\|_c^2=\langle w,w\rangle .             \tag{7}
\]

For \(w\in V(c,1/2)\), Peirce calculus gives

\[
 w^2={\|w\|_c^2\over2}(c+k_w),                             \tag{8}
\]

where \(k_w\in V(d,1)\) is primitive when \(w\ne0\).  Here and below the
Jordan rank of zero is \(0\).  The span of
\(c,k_w,w\) is a rank-two Jordan subalgebra, and \(d-k_w\) is orthogonal to
it.  It follows that

\[
 X(\delta,w,z):=\delta c+\sqrt2\,w+z d\succeq0
 \quad\Longleftrightarrow\quad
 \delta,z\geq0,
 \quad \delta z\geq\|w\|_c^2,                              \tag{9}
\]

and, with the standard normalization \(\det e=1\),

\[
 \det_VX(\delta,w,z)
       =z^{r-2}\bigl(\delta z-\|w\|_c^2\bigr).             \tag{10}
\]

The formulas follow by taking the two eigenvalues in the rank-two subalgebra
and the residual eigenvalue \(z\) with multiplicity \(r-2\).  In a spin
factor \(r=2\), so there is no residual eigenvalue and the factor \(z^{r-2}\)
is \(1\).  They also hold in the exceptional Albert algebra: there
\(V(c,1/2)\) has dimension \(16\), and the Peirce-square identity makes
\(k_w\) primitive in the rank-two face without using octonionic matrix
associativity.

There is also a rank-one completion identity.  For \(g\in V(c,1/2)\) and
\(A>0\),

\[
 A P\!\left(c-{g\over\sqrt2A}\right)c
   =Ac-{g\over\sqrt2}+{1\over2A}P(g)c\succeq0            \tag{11}
\]

has Jordan rank one, and its \(V(d,1)\)-part has trace
\(\|g\|_c^2/(4A)\).  This is the Jordan replacement for a rank-one Hermitian
Gram completion.

## 3. Peirce-perspective lift attaining the bound

Choose a dictionary factor attaining \(B\), fix a primitive idempotent \(c\),
and partition \(\mathbb R^{s-1}\) into
\(q=q_B(s)\) real coordinate groups of size at most \(B\).  Isometrically
embed each group into a copy of \(V(c,1/2)\).  For a projected point
\(x=(w_1,\ldots,w_q,b)\), introduce \(z_G\in\mathbb R\) and impose

\[
 X_G=(1-b)c+\sqrt2\,w_G+z_Gd\succeq0,
 \qquad \sum_{G=1}^qz_G=1+b.                               \tag{12}
\]

By (9), summing
\(\|w_G\|_c^2\leq(1-b)z_G\) proves
\(\sum_G\|w_G\|_c^2+b^2\leq1\).  Conversely, these scalar perspective
inequalities admit the required \(z_G\)'s at every ball point.  Thus (12) is
an exact full-Slater lift of \(B_2^s\).

Let a support be \(v=(g_1,\ldots,g_q,\eta)\in S^{s-1}\).  A dual block has
the coefficient form

\[
              Y_G=A_Gc-{g_G\over\sqrt2}+H_G,
              \qquad H_G\in V(d,1)_+,                      \tag{13}
\]

with

\[
 \operatorname{tr}H_G=\gamma={1-\eta\over2},
 \qquad \sum_GA_G={1+\eta\over2}.                          \tag{14}
\]

Indeed, (13)--(14) make
\(\sum_G\langle X_G,Y_G\rangle=1-v^Tx\) on the whole affine slice.
For \(\eta<1\), put

\[
 A_G={\|g_G\|_c^2\over2(1-\eta)}.                         \tag{15}
\]

When \(g_G\ne0\), (11) gives a rank-one \(Y_G\) whose tail trace is
\(\gamma\).  When \(g_G=0\),
take \(A_G=0\) and a rank-one tail \(\gamma k\), where \(k\) is a primitive
idempotent of \(V(d,1)\) and is also primitive in the parent algebra.  The sphere
identity makes (15) sum to \((1+\eta)/2\).  Hence there is a certificate of
total rank \(q\).  Conversely, \(\gamma>0\) forces the compressed tail of
every block to be nonzero, so every certificate has total rank at least
\(q\).  This includes the south pole \(\eta=-1\): all \(g_G=0\), all
\(A_G=0\), and every block has a nonzero primitive tail of trace one.  At the
north pole \(\eta=1\), positivity forces every tail and every half-Peirce
component to vanish; concentrating the top mass in one block gives minimum
rank one.  This proves the upper bound and the generic and essential-infimum
assertions.

For a non-full last coordinate group, (13) fixes only the projection of the
half-Peirce component onto the chosen group subspace.  Orthogonal components
may enlarge the full certificate fiber; the displayed favorable completion
sets them to zero, while the trace condition still makes every arbitrary
block nonzero when \(\eta<1\).  Likewise, zero support groups can have
higher-rank tail completions.  The theorem concerns the minimum rank in the
full fiber, not uniqueness or the rank of every certificate.

## 4. Heterogeneous products and QIPM movement

For an arbitrary affine lift of \(\prod_{a=1}^mB_2^{s_a}\), with every
\(s_a\geq2\), choose source
contacts and genuine pure-row certificates sequentially.  Compress the next
row fiber by \(P(e-c)\), where \(c\) is the join of previously selected
supports in each factor.  Whole-cylinder complementarity preserves the next
support-slack identity for the compression of every original genuine
pure-row certificate.  After reducing the restricted lift to its minimal
face, the lower bound (6) selects the next support so that every such
compressed certificate has rank at least \(q_B(s_a)\).  Thus one may choose
an original genuine certificate with that rank increment; no extension of a
certificate defined only on the restricted cylinder is being assumed.  The
identity

\[
 \operatorname{rank}_J(P(e-c)y)
   =\operatorname{rank}_J(c\vee\operatorname{supp}y)
       -\operatorname{rank}_Jc                              \tag{16}
\]

telescopes, including in Albert factors.  Thus there are simultaneous source
contacts and pure-row certificates \(Y^a\) such that every positive aggregate
has

\[
 \sum_i\operatorname{rank}_J\!\left(\sum_a\lambda_aY_i^a\right)
       \geq\sum_a q_B(s_a),\qquad \lambda_a>0.              \tag{17}
\]

Every primal tuple in the final simultaneous-contact fiber has at least the
same total Jordan nullity.  Separate copies of (12) attain (17) at the level
of favorable aggregate certificates.  This is an additive existence theorem;
it does not assert additivity of the minimum over the full certificate fiber
of an aggregate objective in a shared-factor lift.

For one ball, first pass to the minimal face containing the affine lift, and
use the standard Jordan barrier of that face.  Choose the hard support from
(3), any genuine certificate \(S=(S_i)\), and an interior feasible reference
\(X^c\) in the reduced affine slice.  If

\[
 Q=\sum_i\operatorname{rank}_JS_i\geq q_B(s),
\qquad
 \Delta_c=Q\left[
   \prod_{i:S_i\ne0}\det_{c_i}(S_i)
      \det_{c_i}\!\bigl(P(c_i)X_i^c\bigr)
                 \right]^{1/Q},                             \tag{18}
\]

then the support-principal-minor theorem gives the path-independent standard
Jordan metric lower bound

\[
 d_F\bigl(X^c,\{X:\operatorname{gap}(X)\leq\epsilon\}\bigr)
 \geq\left[\sqrt Q\log{\Delta_c\over\epsilon}\right]_+
 \geq\left[\sqrt{q_B(s)}\log{\Delta_c\over\epsilon}\right]_+ . \tag{19}
\]

For a trajectory starting within distance \(D_0\) of \(X^c\), with counted
rounds of standard-barrier distance at most \(D\), this implies

\[
 T\geq {\bigl[\sqrt{q_B(s)}\log(\Delta_c/\epsilon)-D_0\bigr]_+
             \over D}.                                      \tag{20}
\]

If a round consists of at most \(k\) forward Dikin chords of starting local
norm at most \(\theta<1\), one may take
\(D=k[-\log(1-\theta)]\).  The construction (12) shows that the
\(\sqrt{q_B(s)}\) exposed-rank coefficient is attainable at generic supports.
The reference scale \(\Delta_c\) depends on the selected lift, certificate,
and reference point, so (19) does not supply a formulation-uniform additive
constant.

The same conclusion holds for every classified self-scaled barrier on the
face-reduced product cone.  In the usual block normalization such a barrier
is, up to an additive constant and permutation of isomorphic factors,
\(F_{\boldsymbol\alpha}=-\sum_i\alpha_i\log\det_i\) with
\(\alpha_i\geq1\).  The weighted support-minor theorem replaces \(Q\) by

\[
 Q_{\boldsymbol\alpha}
      =\sum_i\alpha_i\operatorname{rank}_JS_i\geq q_B(s)    \tag{21}
\]

and \(\Delta_c\) by its weighted exposed-minor scale.  Thus the standard
barrier is already the weakest member of this self-scaled class for the
rank-based leading coefficient.  This statement does not cover arbitrary
coupled or custom self-concordant barriers.

Equations (19)--(21) are metric-movement obstructions for the standard Jordan
barrier and, with the displayed weighting, classified self-scaled barriers.
They are not quantum-query or runtime lower bounds for arbitrary
QIPMs, custom barriers, infeasible trajectories, or unbounded-movement rounds.

### Exact minimax asymptotic movement order

The lower order has a standard-barrier upper construction independent of the
rank of the symmetric-cone factor.  Put

\[
                    g_B(s)=\left\lceil {s\over B}\right\rceil . \tag{22}
\]

Partition all \(s\) ball coordinates into \(g=g_B(s)\) groups of size at most
\(B\), embed each group in \(V(c,1/2)\), and use the fixed-tail blocks

\[
       \widetilde X_G=t_Gc+\sqrt2\,w_G+d\succeq0,
       \qquad \sum_Gt_G=1.                                  \tag{23}
\]

Equations (9)--(10) reduce exactly to

\[
 \widetilde X_G\succeq0\iff t_G\geq\|w_G\|_c^2,
 \qquad \det\widetilde X_G=t_G-\|w_G\|_c^2.                 \tag{24}
\]

Thus (23) projects exactly onto \(B_2^s\), and the restricted standard
Jordan barrier is

\[
             \widetilde F=-\sum_G\log(t_G-\|w_G\|_c^2).     \tag{25}
\]

Each summand is one-self-concordant on its paraboloid domain.  This follows
by restricting the standard self-concordance inequality and checking the
gradient parameter directly.  If \(h=t-\|w\|^2\), then

\[
 \nabla f={1\over h}\binom{-1}{2w},\qquad
 \nabla^2f={1\over h^2}
 \begin{pmatrix}1&-2w^T\\-2w&2hI+4ww^T\end{pmatrix},
 \qquad
 \nabla f^T(\nabla^2f)^{-1}\nabla f=1.                       \tag{25a}
\]

Hence (25), after the affine
constraint in (23), has parameter at most \(g\).  If a matching spin factor
is actually present in the dictionary, it represents the whole ball as a
trace-one section and its direct standard barrier gives parameter one in the
exceptional case \(g=2,q_B(s)=1\).  This shortcut uses the absence of the
residual \(z^{r-2}\) determinant factor and does not arise merely because a
higher-rank factor, including Albert, contains rank-two faces.  In all cases

\[
                  q_B(s)\leq g\leq q_B(s)+1\leq2q_B(s).     \tag{26}
\]

Fix \(0<\theta<1\).  For a lift \(\mathcal L\), an interior start \(X_0\),
and support \(v\), let
\({\cal N}_{\mathcal L,X_0}^{\theta}(v,\epsilon)\) be the minimum number of
feasible forward chords, each of starting-point standard-barrier Dikin norm
at most \(\theta\), needed to reach support-objective gap at most
\(\epsilon\).  The lift and start are fixed before
\(\epsilon\downarrow0\).  Then

\[
 {\sqrt{q_B(s)}\over-\log(1-\theta)}
 \leq \inf_{\mathcal L,X_0}\liminf_{\epsilon\downarrow0}
       \sup_{v\in S^{s-1}}
       {{\cal N}_{\mathcal L,X_0}^{\theta}(v,\epsilon)
           \over\log(1/\epsilon)}
 \leq \inf_{\mathcal L,X_0}\limsup_{\epsilon\downarrow0}
       \sup_{v\in S^{s-1}}
       {{\cal N}_{\mathcal L,X_0}^{\theta}(v,\epsilon)
           \over\log(1/\epsilon)}
 \leq C_\theta\sqrt{q_B(s)}.                               \tag{27}
\]

For the lower bound, the hard support and its certificate are fixed after the
lift is fixed; their exposed-minor scale and the finite start/reference
distance vanish after division by \(\log(1/\epsilon)\).  A forward
\(\theta\)-Dikin chord has metric length at most
\(-\log(1-\theta)\).  For the upper bound, start (23) at
\(t_G=1/g,w_G=0\).  The dual local norm of every unit support objective is
\(1/\sqrt{2g}\), uniformly in its direction.  A conventional fixed-neighborhood
short-step schedule for (25), subdivided into a fixed
\(O_\theta(1)\) number of forward chords if necessary, uses
\(O_\theta(\sqrt g\log(g/\epsilon))\) chords.  Equations (26)--(27) follow.

All metrics and local norms in (27) are those of the minimal face-reduced
standard Jordan barrier.  The infima range over finite relative-Slater affine
lifts through the fixed repeatable dictionary and over fixed interior starts
in their reduced affine slices.  The constant
\(C_\theta\) is independent of the ambient EJA rank and type, but (27) fixes
the dictionary and ball dimension before taking the accuracy limit.  It is a
bounded-Dikin movement frontier, not a quantum-query or runtime frontier.

### Exact standard-barrier value off the divisible seam

Let \(\nu_{\rm std,slice}(\mathcal L)\) be the parameter of the standard
product Jordan log-determinant after minimal-face reduction and restriction
to the effective affine lift (with null directions eliminated).  At the
hard support from (3), every certificate has rank at least \(q=q_B(s)\).
Complementarity therefore gives total primal nullity at least \(q\) at every
point in the exposed boundary fiber.  Along a segment from such a point to a
relative-Slater point, the product determinant has a zero of order at least
\(q\).  The standard boundary-order argument yields

\[
            \nu_{\rm std,slice}(\mathcal L)\geq q_B(s)       \tag{28}
\]

for every lift.  The fixed-tail construction has parameter at most \(g_B(s)\).
Consequently

\[
 \boxed{\displaystyle
 B\nmid(s-1)\quad\Longrightarrow\quad
 \inf_{\mathcal L}\nu_{\rm std,slice}(\mathcal L)
       =q_B(s)=g_B(s).}                                     \tag{29}
\]

In the one-channel divisible case \(s=B+1\), the companion
[one-channel rigidity theorem](2026-09-04-selection-free-symmetric-cone-one-channel-rigidity.md)
closes the seam: the exact value is one if the dictionary contains a matching
spin factor \(Q_{B+2}\), and two otherwise.  In the remaining divisible cases
\(q_B(s)\geq2\), the present theorem leaves the sharp value in the one-unit
interval \([q_B(s),q_B(s)+1]\).  This is the
all-symmetric-cone analogue of the previously proved Hermitian and Lorentz
nondivisible frontiers and includes nondivisible Albert capacities.

For a heterogeneous product of balls, the additive selected-certificate and
final-fiber-nullity theorem gives the standard-barrier lower
\(\sum_aq_B(s_a)\), while separate fixed-tail lifts give the upper
\(\sum_ag_B(s_a)\).  Hence the exact value is additive whenever every source
is off its divisible seam.  The companion one-channel theorem gives the
corresponding exact additive values for products of critical one-channel
sources as well.

## 5. Novelty and scope

### Targeted primary-source screen (2026-09-04)

The general lift language is established by Gouveia--Parrilo--Thomas,
[*Lifts of Convex Sets and Cone
Factorizations*](https://arxiv.org/abs/1111.3164): a proper-cone lift is
equivalent, under the usual hypotheses, to a factorization of the slack
operator.  Soh--Varvitsiotis,
[*Multiplicative Updates for Symmetric-Cone
Factorizations*](https://arxiv.org/abs/2108.00740), explicitly formulate cone
factorizations over arbitrary symmetric cones and review the full simple-EJA
classification, including the octonionic (3\times3) cone.  These papers
optimize or compute a global cone factorization.  They do not optimize, for
each support slack, the minimum Jordan rank in its **entire** normalized dual
fiber and then take a maximum or essential infimum over supports.

The closest 2026 positive-map result is Aubrun--La
Piana--Müller-Hermes,
[*Factorization through Lorentz
cones*](https://arxiv.org/abs/2606.27825).  Their Theorem 3 says that every
positive map from the square-based cone to a symmetric cone factors through a
direct sum of Lorentz cones.  Their symmetric-cone list expressly includes
real, complex, and quaternionic PSD cones, spin factors, and the Albert cone;
they also note that the Albert cone is not a retract of any real PSD cone.
This is a useful boundary: the exceptional case here is genuinely an
all-symmetric-cone statement rather than a disguised real-PSD corollary.
Their invariant is nevertheless positive-map Lorentz factorizability, not
support-fiber Jordan rank, Peirce capacity (a(r-1)), or an affine ball-lift
minimax.  Aubrun--Müller-Hermes,
[*Annihilating Entanglement Between
Cones*](https://arxiv.org/abs/2110.11825), Appendix D, likewise proves
positive-map and tensor-cone statements uniformly for all symmetric cones
using EJA spectral calculus; it does not contain the rank frontier (3).

The Jordan ingredients are classical.  Faraut--Korányi, *Analysis on
Symmetric Cones*, supplies the Peirce decomposition, determinant, quadratic
representation, and classification used in Sections 1--3.  Cardoso--Vieira,
[*On the Optimal Parameter of a Self-Concordant Barrier over a Symmetric
Cone*](https://optimization-online.org/2003/11/774/), prove that the
Carathéodory number equals the EJA rank and hence that rank is the optimal
ambient barrier parameter.  Hauser--Güler,
[*Self-Scaled Barrier Functions on Symmetric Cones and Their
Classification*](https://optimization-online.org/2001/03/307/), prove the
irreducible decomposition and algebraic classification that yields the block
weights in (21).  Schmieta--Alizadeh,
[*Associative and Jordan Algebras, and Polynomial Time Interior-Point
Algorithms for Symmetric
Cones*](https://doi.org/10.1287/moor.26.3.543.10582), and Permenter,
[*A Geodesic Interior-Point Method for Linear Optimization over Symmetric
Cones*](https://arxiv.org/abs/2008.08047), supply nearby all-symmetric-cone
IPM machinery and square-root-rank iteration bounds.  None determines the
parameter of the standard product determinant after an arbitrary affine ball
lift, or ties the iteration coefficient to a minimum-rank support
certificate.

The targeted search did not locate any primary source stating any of the
following: the exact minimax
(\lceil(s-1)/\max_i a_i(r_i-1)\rceil); its dense-open/full-measure and
essential-infimum strengthening; the Peirce-perspective lift attaining it;
the Albert value (\lceil(s-1)/16\rceil); the additive sequential-compression
theorem; the off-divisible exact restricted-standard-barrier value; or the
formulation minimax (\Theta(\sqrt q)) bounded-Dikin movement order.

The conservative label is **candidate exact selection-free all-EJA
support-certificate frontier and restricted-standard-barrier/movement
synthesis**.  It is not a claim of new Peirce calculus, EJA classification,
cone-factorization theory, positive-map theory, self-scaled-barrier
classification, ambient symmetric-cone barrier optimality, or general
square-root-rank IPM complexity.  The result concerns genuine affine-slice
support certificates and standard product Jordan barriers (plus classified
self-scaled weights); it does not cover arbitrary coupled self-concordant
barriers or unrestricted quantum query/runtime lower bounds.  This was a
targeted screen through 2026, not an exhaustive priority determination, and
the exceptional Albert and quaternionic cases still merit specialist review.

## Audit record

An independent agent derived (9)--(11) from the rank-two Peirce subalgebra,
including the Albert case, and checked the ball projection and favorable
rank-one dual completions.  It also identified and resolved two scope traps:
zero support groups admit higher-rank dual completions, and a non-full last
group does not fix the orthogonal half-Peirce component.  Neither affects the
minimum-rank frontier.

### Hostile audit verdict (2026-09-04)

**PASS after the stated \(s\geq2\) correction and scope clarifications.**
Without that restriction, (1)--(3) have the counterexample \(B_2^1\):
\(q_B(1)=0\), while a normalized support slack cannot have the zero
certificate, so its frontier is \(1\).

The lower bound survives arbitrary finite simple-EJA dictionaries.  On a
common full-dimensional semialgebraic \(C^1\) stratum, locally constant rank
puts the two selector derivatives in their support-tangent Peirce spaces; the
only paired channel is the \(p_i\)-by-\(q_i\) cross space of real dimension
\(a_ip_iq_i\).  Complementarity and \(p_i+q_i\leq r_i\) give (6).  Rays
contribute no channel.  Proper faces do not increase capacity: classical
faces retain the same Peirce constant at smaller rank, spin faces are rays,
and the rank-two proper face of Albert is the \(10\)-dimensional spin factor
with capacity \(8\leq16\).  Thus neither facial reduction nor exceptional
rank conventions furnish a counterexample.  Semialgebraic definable choice
of a minimum realized integer rank, followed by common stratification, gives
the claimed dense open set; its lower-dimensional complement is
surface-null, which verifies the quantifiers in (3a).

The upper construction was checked at every certificate branch.  For
\(\eta<1\), including the south pole and groups with \(g_G=0\), each block
has a rank-one completion and every certificate has a nonzero tail.  At the
north pole positivity kills the tail and half-Peirce parts and the minimum is
one.  Restricting the last coordinate group only frees orthogonal
half-Peirce coefficients and does not change either the favorable completion
or the per-block nonzero lower bound.  Formulae (8)--(11) remain valid for
rank-two spin factors and Albert: in the former \(z^{r-2}=1\); in the latter
the Peirce square lands on a primitive idempotent of the rank-two
\(H_2(\mathbb O)\) face, so no associative matrix argument is needed.

For products, whole-cylinder complementarity makes the compression of every
original pure-row certificate a certificate of the restricted lift.  Applying
the generic lower bound after further minimal-face reduction therefore
selects a hard next support without assuming that an arbitrary restricted
certificate extends globally.  The Jordan compression identity (16) then
telescopes support-join ranks, including in Albert, and positivity identifies
the support of every strictly positive aggregate with that join.  This proves
exactly the additive existence statement (17), not additivity of the minimum
over an aggregate fiber.

Finally, the support-minor movement bound has the correct
\(\sqrt Q\), determinant scale, positive parts, and bounded-chord denominator
when interpreted in the minimal face-reduced standard Jordan metric.  In the
fixed-tail upper, (10) gives
\(\det\widetilde X_G=t_G-\|w_G\|_c^2\) for every EJA type.  Affine
restriction supplies standard self-concordance, while (25a) supplies the
sharper parameter \(1\); hence the grouped parameter is at most
\(g=\lceil s/B\rceil\), with \(q_B(s)\leq g\leq q_B(s)+1\leq2q_B(s)\).
The parameter-one trace-section shortcut in the \(g=2,q_B(s)=1\) case
requires an actually available matching spin factor and does not follow from
an Albert embedding.  The analytic-center dual norm and conventional
short-step schedule are uniform in the support, rank, and EJA type.  In
(27), the lift and start lie outside and before the accuracy limit, whereas
the hard support may depend on that fixed lift; the exposed-minor constants
then vanish after division by \(\log(1/\epsilon)\).  The displayed
\(\inf\)-\(\liminf/\limsup\)-\(\sup\) order is therefore sound.

The parameter corollary (28)--(29) also passes.  Fixing any one hard
certificate suffices to force nullity at least \(q_B(s)\) at every point of
its exposed primal fiber.  A segment from such a boundary point to a
relative-Slater point has determinant vanishing order equal to that total
nullity; restricting the parameter inequality to this one-dimensional
segment gives limiting squared gradient norm equal to the order, and hence
\(\nu_{\rm std,slice}\geq q_B(s)\).  The fixed-tail upper has parameter at
most \(g_B(s)\), and the integer ceiling identity gives \(g_B(s)=q_B(s)\)
exactly off the divisible seam.  At a simultaneous product contact, the
support-join/nullity increments add, so the same boundary-order proof and
separate fixed-tail uppers establish the stated additive exactness whenever
each source is nondivisible, as well as when a divisible \(q=1\) source has
the available matching-spin trace-section exception.
