# Exposed Jordan rank forces bounded-Dikin iterations on symmetric-cone lifts

Status: Proved; independently hostile-audited
Started: 2026-09-04
Paper status: Not incorporated
Confidence: High on the theorem and constants; novelty pending specialist review

## Headline result

There is a path-independent iteration lower bound for the standard Jordan
log-determinant on **every** symmetric cone, including Lorentz, real,
complex and quaternionic PSD cones, and the exceptional cone
\(H_+^3(\mathbb O)\).  The invariant is the Jordan rank of an optimal dual
exposing slack, not the number of cone factors.

Let \(K=\prod_{i=1}^L K_i\), where \(K_i\) is the cone of squares of a
Euclidean Jordan algebra \(V_i\), and let

\[
 \Omega=\{x\in\operatorname{int}K:Ax=b\}.                         \tag{1}
\]

On \(\Omega\), use the restricted standard barrier and its Hessian metric

\[
 F(x)=-\sum_i\log\det_i x_i,
 \qquad \|h\|_x^2=\nabla^2F(x)[h,h].                               \tag{2}
\]

Write \(d_F\) for the intrinsic path distance obtained by integrating
this restricted Hessian norm over piecewise \(C^1\) curves in \(\Omega\).

Suppose a linear objective has finite optimum \(\ell_*\) and an attained
dual certificate

\[
             \ell_*-\ell(x)=\langle s,x\rangle
             \quad(x\in\Omega),\qquad s=(s_i)_i\in K.             \tag{3}
\]

Write \(q_i=\operatorname{rank}s_i\), \(Q=\sum_iq_i>0\), let \(c_i\)
be the support idempotent of \(s_i\).  Components with \(q_i=0\) are
omitted below.  For an interior reference point \(x^c\in\Omega\), set

\[
 \Delta_c
 =Q\left[\prod_{i:q_i>0}
       \det_{c_i}(s_i)\det_{c_i}\!\bigl(P(c_i)x_i^c\bigr)
        \right]^{1/Q}.                                               \tag{4}
\]

Here \(P(c_i)\) is the Peirce projection onto the rank-\(q_i\) algebra
\(V_i(c_i,1)\), and \(\det_{c_i}\) is its Jordan determinant.  Then every
\(y\in\Omega\) with objective gap at most \(\epsilon\) obeys

\[
 \boxed{
 d_F(x^c,y)\geq
       \left[\sqrt Q\log{\Delta_c\over\epsilon}\right]_+.}          \tag{5}
\]

This estimate permits arbitrary motion in the lifted variables and does
not require a central-path neighborhood, bounded fibers, strict
complementarity, or a bound on inactive eigenvalues.

More generally, suppose a sequence of outer iterates satisfies
\(d_F(x_j,x_{j+1})\leq B\) and \(d_F(x_0,x^c)\leq D_0\).  If \(x_T\) is
\(\epsilon\)-optimal, the triangle inequality in (5) gives

\[
              T\geq
              {\left[\sqrt Q\log(\Delta_c/\epsilon)-D_0\right]_+
               \over B}.                                             \tag{5a}
\]

Thus the obstruction applies to arbitrary geodesic, predictor, or
higher-order update arcs whenever each counted round has bounded intrinsic
barrier-metric displacement; straight Dikin chords are only one concrete
specialization.

Fix \(0\leq\rho<1\), \(0<R<1\), and an integer \(m\geq1\).  Start from
any \(x_0\in\Omega\) satisfying
\(\|x_0-x^c\|_{x^c}\leq\rho\).  If each of \(T\) rounds contains at most
\(m\) feasible chords, each having starting-point local norm at most
\(R\), and the last point is \(\epsilon\)-optimal, then

\[
 \boxed{
 T\geq
 {\left[
   \sqrt Q\log(\Delta_c/\epsilon)
       -\log(1/(1-\rho))\right]_+
  \over m\log(1/(1-R))}.}                                            \tag{6}
\]

The reference point need not be the analytic center.  Choosing it to be
the analytic center normally makes \(\Delta_c\) explicit.

For globally labelled bi-\(C^1\) lifts of a product
\(\prod_aB_2^{s_a}\) through arbitrary simple symmetric cones, Section 3
proves at every simultaneous contact

\[
 Q\geq\sum_a\left\lceil{s_a-1\over\kappa}\right\rceil,
 \qquad \kappa=\max_i a_i(r_i-1).
\]

This includes exceptional Albert factors.  Under a real factor-dimension
cap \(d\), replace \(\kappa\) by \(d-2\).  If some
\(s_a-1=t_a(d-2)\) with \(t_a\geq2\), sequential Peirce compression adds
the one-ball topological premium separately for every such source.  These
product statements convert (5) from a certificate-conditional theorem into
an explicit hard-objective movement lower bound.

## 1. A support-minor Busemann lemma

The mechanism behind (5) is stronger than a bound on total barrier height.
It tracks only the principal Jordan minor exposed by the dual slack, so an
algorithm cannot cancel the shrinking active eigenvalues by sending
unexposed lift variables to infinity.

Let \(V\) be any Euclidean Jordan algebra, \(x\in\operatorname{int}K\),
and let \(c\) be an idempotent of rank \(q\).  Put

\[
 a=P(c)x\in\operatorname{int}K(c,1),\qquad
 \phi_c(x)=-\log\det_c a.                                            \tag{7}
\]

For the Hessian metric of \(-\log\det x\),

\[
                  \|d\phi_c(x)\|_{x,*}^2=q.                          \tag{8}
\]

Indeed, \(\nabla^2(-\log\det x)=P(x^{-1})\), whose inverse is \(P(x)\),
and

\[
 d\phi_c(x)[h]=-
 \langle a^{-1},P(c)h\rangle=-\langle a^{-1},h\rangle.               \tag{9}
\]

The fundamental quadratic-representation identity gives, on
\(V(c,1)\),

\[
 P(c)P(x)P(c)=P(P(c)x)=P(a).                                        \tag{10}
\]

Consequently

\[
 \|d\phi_c(x)\|_{x,*}^2
 =\langle a^{-1},P(x)a^{-1}\rangle
 =\langle a^{-1},P(a)a^{-1}\rangle
 =\langle a^{-1},a\rangle
 =\operatorname{tr}_c c=q.                                          \tag{11}
\]

Affine restriction can only decrease a covector's dual norm.  Therefore,
for

\[
                \Phi_s(x)=\sum_{i:q_i>0}\phi_{c_i}(x_i),             \tag{12}
\]

on the slice (1),

\[
                         |d\Phi_s(x)[h]|
                         \leq\sqrt Q\,\|h\|_x.                       \tag{13}
\]

Thus \(\Phi_s\) is globally \(\sqrt Q\)-Lipschitz in barrier-metric
length.  Formula (8) is valid in the exceptional Jordan algebra as well;
it uses only the quadratic-representation identities.

## 2. Objective accuracy collapses the exposed minor

Put \(g_i=\langle s_i,y_i\rangle\) and
\(a_i=P(c_i)y_i\).  Positivity gives \(g_i\geq0\) and
\(\sum_i g_i\leq\epsilon\).  Take the square root of \(s_i\) inside the
rank-\(q_i\) Peirce algebra and set

\[
 z_i=P(s_i^{1/2})a_i.
 \quad\text{Then}\quad
 \operatorname{tr}_{c_i}z_i=g_i,qquad
 \det_{c_i}z_i=\det_{c_i}(s_i)\det_{c_i}(a_i).                       \tag{14}
\]

The trace identity uses self-adjointness of the quadratic representation
and \(P(s_i^{1/2})c_i=s_i\); the determinant identity is
\(\det(P(u)v)=\det(u)^2\det(v)\).  Jordan spectral AM--GM in this
rank-\(q_i\) algebra now yields the sharper invariant estimate

\[
 \det_{c_i}(P(c_i)y_i)
 \leq {1\over\det_{c_i}(s_i)}
      \left({g_i\over q_i}\right)^{q_i}.                            \tag{15}
\]

Weighted AM--GM, first over the factors with \(q_i>0\), gives

\[
 \prod_{i:q_i>0}\left({g_i\over q_i}\right)^{q_i}
 \leq\left({\epsilon\over Q}\right)^Q.                             \tag{16}
\]

Combining (15)--(16) with (4) gives

\[
             \Phi_s(y)-\Phi_s(x^c)
             \geq Q\log{\Delta_c\over\epsilon}.                    \tag{17}
\]

Integrating (13) along an arbitrary piecewise \(C^1\) path proves (5).
Notice that no determinant or trace bound is imposed on the complementary
Peirce algebra.  This is exactly what makes the result robust to unbounded
or densely coupled auxiliary fibers.

The coefficient \(\sqrt Q\) is sharp already in the unconstrained cone.
Apply the factorwise quadratic-representation isometry that sends the
reference point to the Jordan unit, and denote the transformed dual slack
again by \(s\).  In a Jordan frame diagonalizing \(s\), the curve

\[
 y_i(t)=P\!\left(\sqrt t\,c_i+(e_i-c_i)\right)e_i,
 \qquad y(t)=(y_i(t))_i,\qquad 0<t\leq1,                             \tag{17a}
\]

has \(\langle s,y(t)\rangle=t\langle s,e\rangle\) and length
\(\sqrt Q\,|\log t|\).  Hence the distance from the unit to the gap-
\(\epsilon\) halfspace is at most
\(\sqrt Q\log(\langle s,e\rangle/\epsilon)\), while (5) supplies the
same leading coefficient with the geometric-mean spectral scale.  Thus
\(\sqrt Q\) is the exact asymptotic \(\log(1/\epsilon)\) coefficient in
the full cone.  Affine constraints can only remove this explicit upper
path, not invalidate the lower bound.

For a feasible chord \(h\) with \(r=\|h\|_x<1\), self-concordant Hessian
comparison bounds its metric length by

\[
                         -\log(1-r).                                  \tag{18}
\]

The same bound applied to the initial center error, followed by the
triangle inequality and concatenation of at most \(mT\) chords, proves
(6).

## 3. Product balls force exposed rank through Peirce curvature

The exposed rank \(Q\) cannot be made arbitrarily small when bounded-size
symmetric cones lift a product of balls.  The following statement isolates
the exact regularity needed for that conclusion.

Let

\[
                 C=\prod_{a=1}^b B_2^{s_a},\qquad
                 n=\sum_{a=1}^b(s_a-1).                              \tag{19}
\]

Suppose the lift has globally labelled \(C^1\) primal factors
\(X_i(x_1,\ldots,x_b)\) on the product of boundary spheres and globally
labelled \(C^1\) dual row factors \(Y_i^a(z_a)\), with the full slack
identities

\[
 1-x_a^Tz_a=\sum_i\langle X_i(x),Y_i^a(z_a)\rangle.                  \tag{20}
\]

Assume, as part of the lift-factorization hypothesis, that each
\(Y^a(z_a)\) is a genuine affine-slice dual certificate: its pairing with
**every** feasible lifted point equals the corresponding projected slack,
not only its pairing with the selected boundary sheet in (20).  Therefore
the positive weighted sum in (21) satisfies the global certificate (3).

Choose positive objective weights \(\lambda_a\), fix a simultaneous
contact \(z_a=x_a\), and put

\[
 s_i=\sum_a\lambda_aY_i^a(x_a),\qquad
 p_i=\operatorname{rank}X_i(x),\qquad
 q_i=\operatorname{rank}s_i.                                        \tag{21}
\]

If \(K_i\) is simple of rank \(r_i\) and Peirce constant \(a_i\), then

\[
 \boxed{
 n\leq\sum_{i\,\mathrm{nonray}}a_ip_iq_i
   \leq\sum_{i\,\mathrm{nonray}}a_i(r_i-1)q_i.}                   \tag{22}
\]

To prove the first inequality, sum (20) with weights \(\lambda_a\).  Its
mixed derivative at simultaneous contact is the nondegenerate form

\[
              -(u,v)\longmapsto\sum_a\lambda_au_a^Tv_a               \tag{23}
\]

on an \(n\)-dimensional tangent space.  Positivity and zero pairing make
\(X_i(x)\) and \(s_i\) Jordan-complementary.  The differentiated
complementarity identity factors the \(i\)-th mixed form through the cross
Peirce space between their support idempotents, of real dimension
\(a_ip_iq_i\).  Rank subadditivity of the factorized mixed form proves the
first inequality.  Complementarity gives \(p_i+q_i\leq r_i\), proving the
second.  Ray factors have no cross-Peirce space.

Define the maximum exposed-rank capacity per dual rank unit

\[
                  \kappa=\max_{i\,\mathrm{nonray}}a_i(r_i-1).       \tag{24}
\]

Then (22) implies

\[
                         Q=\sum_iq_i\geq
                         \left\lceil{n\over\kappa}\right\rceil.     \tag{25}
\]

If every nonray factor has real dimension at most \(d\), the identity

\[
 \dim V_i=r_i+{a_i\over2}r_i(r_i-1),\qquad
 a_i(r_i-1)\leq\dim V_i-2,                                          \tag{26}
\]

gives the coarser universal form

\[
                         Q\geq\left\lceil{n\over d-2}\right\rceil. \tag{27}
\]

Useful exact capacities are

\[
\begin{array}{c|c}
\text{allowed simple factor}&\kappa\\ \hline
Q_m\text{ (Lorentz)}&m-2\\
H_+^R(\mathbb R)&R-1\\
H_+^R(\mathbb C)&2(R-1)\\
H_+^R(\mathbb H)&4(R-1)\\
H_+^3(\mathbb O)&16.
\end{array}                                                          \tag{28}
\]

Combining (6) and (25), every such product-ball lift has a simultaneous
support objective whose bounded-Dikin round count is controlled by its
actual exposed rank \(Q\), and in particular has asymptotic coefficient at
least

\[
               \sqrt{\left\lceil n/\kappa\right\rceil}
               \quad\text{in front of }\log(1/\epsilon),             \tag{29}
\]

for fixed formulation, objective and reference point.  The exact finite
bound remains (6), because \(\Delta_c\) depends on the positive eigenvalues
of the chosen dual certificate and on the reference point.

### A global one-ball divisibility premium

For one ball, global support topology sharpens the local numerator from
\(N-1\) to \(N\).  Suppose \(B_2^N\) has the globally labelled bi-\(C^1\)
factorization above, every nonray factor has dimension at most
\(3\leq d<N+1\), and the chosen dual certificate sheet is fixed globally.
Then there exists a unit support objective whose exposing slack satisfies

\[
                      \boxed{Q\geq
                      \left\lceil{N\over d-2}\right\rceil.}          \tag{29a}
\]

When \(d-2\nmid N-1\), this is already (27).  Otherwise write
\(N-1=L(d-2)\).  If every support objective had \(Q=L\), equality would
hold throughout (22) and (26) at every contact.  Lower semicontinuity of
the finitely many integer dual ranks, together with their constant sum,
makes every active label locally and hence globally constant.  Equality
forces each active factor to have

\[
                 q_i=1,\qquad p_i=r_i-1,
                 \qquad r_i=2,\qquad \dim V_i=d.                    \tag{29b}
\]

The joint dual-support map would therefore be a same-dimensional local
diffeomorphism, hence a finite covering,

\[
                         S^{L(d-2)}\longrightarrow
                         (S^{d-2})^L.                                \tag{29c}
\]

The cap \(d<N+1\) makes \(L>1\).  For \(d=3\), the target has infinite
fundamental group; for \(d>3\), it has nonzero intermediate cohomology.
Either contradicts a finite cover by a sphere.  Thus some support objective
has \(Q\geq L+1=\lceil N/(d-2)\rceil\), proving (29a).

This is an existential hard-objective statement; it does not assert the
extra unit for every boundary objective.  Combined with (5), it upgrades
the previously known standard-barrier parameter premium to an actual
bounded-metric movement obstruction for at least one objective, and
Section 5 below extends it to every self-scaled barrier on the same cone
product.  Its comparison with the sourcewise local theorem is exact:

\[
 \left\lceil{N\over d-2}\right\rceil>
 \left\lceil{N-1\over d-2}\right\rceil
 \quad\Longleftrightarrow\quad d-2\text{ divides }N-1.
\]

Thus the support-cover argument is genuinely stronger precisely in the
divisible equality regime that local Peirce-capacity counting leaves open.
The equality audit shows that any hypothetical failure of the premium
would force every active factor to be a dimension-\(d\) rank-two spin
factor, so the conclusion already covers the saturated Lorentz case rather
than assuming it away.

### A sourcewise heterogeneous bound

For real, complex, and quaternionic PSD factors, the cylindrical row
identities give a stronger source-by-source exposed-rank bound at **every**
simultaneous contact.  Let \(\mathbb F\in\{\mathbb R,\mathbb C,\mathbb H\}\),
put \(\beta=\dim_{\mathbb R}\mathbb F\in\{1,2,4\}\), and suppose every
factor has order at most \(R\).  At a simultaneous product contact define

\[
 U_{ia}=\operatorname{Ran}_{\mathbb F}Y_i^a(x_a),\qquad
 U_{i,-a}=\sum_{d\ne a}U_{id},\qquad
 d_{ia}=\dim_{\mathbb F}{U_{ia}\over U_{ia}\cap U_{i,-a}}.          \tag{29d}
\]

For positive objective weights, the summed dual slack has

\[
 q_i=\operatorname{rank}_{\mathbb F}
       \left(\sum_a\lambda_aY_i^a(x_a)\right)
     =\dim_{\mathbb F}\sum_aU_{ia}.                                 \tag{29e}
\]

The full row slack is cylindrical in every unrelated primal source.
Differentiating \(X_i(x)Y_i^d(x_d)=0\) in an \(x_a\)-direction,
\(d\ne a\), shows that the off-diagonal map of \(dX_i[u_a]\) annihilates
\(U_{i,-a}\).  Its pairing with \(dY_i^a[v_a]\) therefore factors through
the private quotient in (29d).  If
\(p_i=\operatorname{rank}_{\mathbb F}X_i(x)\), real-rank subadditivity of
the nondegenerate source contact metric gives

\[
 s_a-1\leq\sum_i\beta p_i d_{ia}
          \leq\beta(R-1)\sum_i d_{ia}.                              \tag{29f}
\]

For fixed \(i\), choose a complement to
\(U_{ia}\cap U_{i,-a}\) in each \(U_{ia}\).  These private complements
are jointly linearly independent, so

\[
                         \sum_a d_{ia}\leq q_i.                      \tag{29g}
\]

Taking ceilings in (29f), summing over sources, and using (29g) proves

\[
 \boxed{
 Q\geq\sum_{a=1}^b
       \left\lceil{s_a-1\over\beta(R-1)}\right\rceil.}              \tag{29h}
\]

Thus (5) gives an actual standard-barrier movement coefficient at least
the square root of the right side, and the same is true for every
self-scaled barrier because \(Q_\alpha\geq Q\).  This sourcewise theorem
matches grouped Hermitian constructions whenever no
\(s_a-1\) is divisible by \(\beta(R-1)\), and otherwise leaves precisely
the familiar per-source regularity premiums unresolved.

The same proof permits mixed Hermitian fields and varying orders.  Put

\[
                   \kappa_{\mathrm H}
                   =\max_i\beta_i(r_i-1),
                   \qquad \beta_i=\dim_{\mathbb R}\mathbb F_i.       \tag{29i}
\]

Private complements are formed separately inside each factor and then
summed, so no cross-field quotient is needed.  Equations (29f)--(29g) give

\[
                 \boxed{Q\geq\sum_a
                 \left\lceil{s_a-1\over\kappa_{\mathrm H}}\right\rceil.} \tag{29j}
\]

If all Hermitian factors have real dimension at most \(d\), then
\(\beta_i(r_i-1)\leq\dim H_{r_i}(\mathbb F_i)-2\leq d-2\), and hence

\[
                 Q\geq\sum_a
                 \left\lceil{s_a-1\over d-2}\right\rceil.           \tag{29k}
\]

Arbitrary Lorentz factors can be mixed into the same theorem.  A productive
Lorentz block has nonzero primal boundary ray and aggregate dual slack on
the unique complementary ray.  If two distinct source rows are nonzero on
that ray, cylindrical complementarity in Jordan-product form gives

\[
          dX_i[u_a]\circ Y_i^d=0\qquad(d\ne a).                     \tag{29l}
\]

Multiplication by the complementary primitive idempotent is one half on
the Lorentz cross-Peirce space, so (29l) kills the row-\(a\) mixed channel.
Thus a productive Lorentz exposed-rank unit is private to at most one
source and carries at most \(m_i-2\) tangent dimensions.  Define

\[
 \kappa_{\mathrm{cl}}=\max\left\{
     \max_{i\,\mathrm{Hermitian}}\beta_i(r_i-1),
     \max_{j\,\mathrm{Lorentz}}(m_j-2)\right\}.                     \tag{29m}
\]

Adding the assigned Lorentz units to the Hermitian private quotient units
proves, for every product of classical irreducible symmetric cones,

\[
                 \boxed{Q\geq\sum_a
                 \left\lceil{s_a-1\over\kappa_{\mathrm{cl}}}\right\rceil.}
                                                                         \tag{29n}
\]

Under a common real-dimension cap \(d\), this again gives (29k).

It remains to control an exceptional Albert factor
\(H_+^3(\mathbb O)\).  Call a source row *productive in a factor* when
that factor's contribution to the row's mixed contact form is nonzero.
Let \(S=\sum_a\lambda_aY^a\) be the aggregate dual slack in an Albert
factor and put \(q=\operatorname{rank}S\).  Then

\[
 \boxed{\text{the number of productive source rows in the factor is at
 most }q.}                                                          \tag{29o}
\]

This is an incidence statement, not an assertion that every nonzero row
is productive.  Here is a proof using only Jordan products and Peirce
spaces.  If \(q=0\), positivity of the sum forces every \(Y^a=0\); the
derivative of a two-sided \(C^1\) cone-valued map at the cone vertex is
zero.  If \(q=3\), complementarity forces the primal value \(X=0\), so
the same vertex argument gives \(dX=0\).  Neither case has a productive
row.

If \(q=1\), every nonzero \(Y^a\) lies on the support ray
\(\mathbb R_+c\).  If rows \(a\) and \(d\) are both nonzero, cylindrical
complementarity differentiated in an \(x_a\)-direction gives
\(dX[u_a]\circ Y^d=0\).  On the relevant cross-Peirce space,
\(L_c=\tfrac12I\), so the cross component of \(dX[u_a]\) vanishes and
row \(a\)'s mixed channel is zero.  A row with \(Y^a=0\) has
\(dY^a=0\).  Hence at most one row is productive.

If \(q=2\), productivity requires the primal support to have rank one.
Write its idempotent as \(e\) and the complementary rank-two support of
\(S\) as \(c\).  The face \(V(c,1)\) is the rank-two spin factor
\(H_2(\mathbb O)\).  For a source \(a\), put
\(S_{-a}=\sum_{d\ne a}\lambda_dY^d\).  Cylindrical complementarity gives

\[
       L_{S_{-a}}B_a=0,
       \qquad B_a=\operatorname{proj}_{V(e,c)}dX[u_a].             \tag{29p}
\]

If \(S_{-a}\) has rank two, diagonalize it in the face as
\(\mu_1f_1+\mu_2f_2\), with \(\mu_1,\mu_2>0\).  The operator in (29p)
has eigenvalues \(\mu_1/2\) and \(\mu_2/2\) on
\(V(e,f_1)\oplus V(e,f_2)=V(e,c)\), so it is invertible and row \(a\)
is not productive.  Thus a productive row requires
\(\operatorname{rank}S_{-a}\leq1\).  Three productive rows are
impossible: for each of them, positivity and the rank-one condition force
all the other nonzero row slacks onto one ray; applying this to two of the
three rows forces all row slacks onto one ray, contradicting \(q=2\).
This proves (29o).

The Albert cross-Peirce space has dimension \(8pq\leq16\) in every
productive case.  Give one token to each source served productively by an
Albert factor.  Equation (29o) gives at most \(q_i\) such tokens in factor
\(i\), while each token carries at most 16 real mixed-contact dimensions.
Combine these tokens with the Hermitian private-quotient tokens and the
Lorentz complementary-ray tokens above.  More explicitly, let \(t_{ia}\)
equal \(d_{ia}\) for a Hermitian factor and equal one or zero according as
source \(a\) is productive or unproductive in a Lorentz or Albert factor.
The three factorwise arguments give

\[
       \sum_a t_{ia}\leq q_i,
       \qquad s_a-1\leq\kappa\sum_i t_{ia},
       \qquad \kappa=\max_i a_i(r_i-1).                            \tag{29q}
\]

Ray factors carry no mixed-contact rank and need no token.  Taking an
integer ceiling in the second inequality of (29q) and then summing the
first proves, for an arbitrary product of simple symmetric cones,
including any mixture containing Albert factors,

\[
                 \boxed{Q\geq\sum_a
                 \left\lceil{s_a-1\over\kappa}\right\rceil.}      \tag{29r}
\]

If every nonray factor has real dimension at most \(d\), then each
classical capacity is at most \(d-2\); an Albert factor can occur only when
\(d\geq27\), and its capacity \(16\leq25\leq d-2\).  Thus the fully
universal dimension-capped form is

\[
                 \boxed{Q\geq\sum_a
                 \left\lceil{s_a-1\over d-2}\right\rceil.}        \tag{29s}
\]

Equations (29r)--(29s) hold at every simultaneous contact under the global
bi-\(C^1\) row-factorization and affine-slice certificate hypotheses of
(20)--(21).  They are local exposed-rank statements; the separate
one-ball theorem (29a) is the global topological result that can add a
unit in its divisible equality case.

### Sequential compression makes all hard row ranks additive

There is a stronger product theorem than the simultaneous-contact ledger.
Define

\[
 h_d(s)=
 \begin{cases}
  1,&d\geq s+1,\\[1mm]
  \left\lceil s/(d-2)\right\rceil,&d<s+1.
 \end{cases}                                                       \tag{29t}
\]

Under the same global factorization and certificate hypotheses, with
\(s_a\geq2\) and factor-dimension cap \(d\geq3\), there exists a
simultaneous support objective satisfying

\[
                         \boxed{Q\geq\sum_a h_d(s_a).}             \tag{29u}
\]

This is the exact minimax hard exposed rank over the stated class of lifts
together with fixed globally labelled certificate sheets.  A separate
grouped Lorentz construction uses one \(Q_{s_a+1}\) factor in the direct
regime and \(h_d(s_a)\) factors of dimension at most \(d\) in the strict
regime; its aggregate rank equals \(\sum_ah_d(s_a)\) at every simultaneous
contact.

The proof orders the rows and, before choosing row \(a\), compresses every
factor into the Peirce face orthogonal to the join \(c_i^{a-1}\) of the
previously chosen row supports.  If \(f_i^{a-1}=e_i-c_i^{a-1}\), prior-row
cylindrical complementarity puts the primal factor in that face for every
choice of all remaining source variables.  Hence

\[
  1-x_a^Tz_a=\sum_i\left\langle X_i(x),
       P(f_i^{a-1})Y_i^a(z_a)\right\rangle_i                       \tag{29v}
\]

is an exact globally \(C^1\) one-ball factorization through face cones of
dimension at most \(d\).  Apply the one-ball theorem to choose \(x_a\).
The compressed dual row need not be an affine-slice certificate; it is used
only for this factorization step.  The original uncompressed rows remain
the genuine final certificates.

The exact Jordan support identity behind the induction is

\[
 \operatorname{rank}\!\left(P(e-c)y\right)
   =\operatorname{rank}\!\left(c\vee\operatorname{supp}y\right)
      -\operatorname{rank}c,
      \qquad y\in K.                                                \tag{29w}
\]

Thus every compressed row rank is exactly the new rank added to the support
join.  These increments telescope, and the support of a positive weighted
sum is the join of its summands' supports, proving (29u).  Identity (29w)
and the sequential theorem hold for every Euclidean Jordan algebra.  In
particular, an Albert rank-two face is the spin factor
\(H_2(\mathbb O)\cong Q_{10}\), so exceptional nonassociativity creates no
gap.

The first branch in (29t) is essential: if \(d\geq s+1\), the direct
Lorentz lift through \(Q_{s+1}\) has rank one.  In the strict-cap regime,
if \(s_a-1=t_a(d-2)\), then \(h_d(s_a)=t_a+1\); (29u) therefore adds the
topological premium separately for **every** such source, even when other
sources are nondivisible.  In exact ledger form,

\[
 \sum_a h_d(s_a)=
 \sum_a\left\lceil{s_a-1\over d-2}\right\rceil
 +\#\{a:s_a-1\in\{2(d-2),3(d-2),\ldots\}\}.
\]

The resulting standard/self-scaled-barrier
distance coefficient is at least

\[
                         \sqrt{\sum_a h_d(s_a)}
                         \quad\text{in front of }\log(1/\epsilon). \tag{29x}
\]

The globally bi-\(C^1\) sheet hypothesis is essential for the divisible
premium.  For arbitrary affine lifts of one \(B_2^s\) through Lorentz
cones of dimension at most \(d\), define the selection-free quantity using
the full genuine certificate fiber \(\mathcal D(v)\):
\[
 \inf_{\mathcal L}\max_{v\in S^{s-1}}
       \min_{Z\in\mathcal D_{\mathcal L}(v)}
       \sum_i\operatorname{rank}_JZ_i
       =\left\lceil{s-1\over d-2}\right\rceil.                  \tag{29x'}
\]
The lower bound follows from semialgebraic minimum-rank selectors on a
generic \(C^1\) stratum.  A grouped nested Lorentz chain attains it and has
a unique certificate at every support.  Hence (29x') is one below
\(h_d(s)\) exactly when \(d<s+1\) and \(d-2\mid s-1\).  The chain's
restricted standard log-determinant nevertheless has exact parameter
\(2\lceil(s-1)/(d-2)\rceil-1\): rank is born on its nonsmooth primal seam.
The complete calculation and scope boundary are in
[The exact selection-free Lorentz exposed-rank
frontier](2026-09-04-selection-free-exposed-rank-premium-counterexample.md).
For shared-factor Lorentz product lifts, the sequential argument gives the
exact favorable-certificate minimax
\[
 \inf_{\mathcal L}
  \sup_{\substack{u\in\prod_aS^{s_a-1}\\Y^a\in\mathcal D_a(u_a)}}
  \sum_i\operatorname{rank}_J\!\left(\sum_a\lambda_aY_i^a\right)
   =\sum_a\left\lceil{s_a-1\over d-2}\right\rceil
   \quad(\lambda_a>0).                                          \tag{29x''}
\]
This also forces that much nullity in every final primal fiber.  The
minimum rank over all certificates of the summed objective is not claimed
additive, because a certificate of a sum need not split positively into
certificates of its rows.

There is no additional selection-free “every completion” nullity premium.
A grouped rotated-Lorentz perspective lift has, for every boundary support,
a primal completion of total nullity exactly
\(\lceil(s-1)/(d-2)\rceil\), and every support-certificate fiber has
maximum rank exactly that value.  Its restricted standard barrier
nevertheless has exact parameter
\(2\lceil(s-1)/(d-2)\rceil-1\), witnessed by higher-nullity vertices
inside a non-singleton pole fiber.  The audited construction is in
[Rotated Lorentz perspectives refute the fiberwise nullity
premium](2026-09-04-rotated-lorentz-fiberwise-nullity-counterexample.md).

The complete proof and independent hostile audit are in
[Sequential Peirce compression makes product-ball hard ranks
additive](2026-09-04-sequential-peirce-compression-additive-exposed-rank.md).
That note also combines the induction with the exact finite-factor capacity
envelope below.  For at most \(L\) Peirce-\(a\), order-at-most-\(R\)
factors, if \(Q_{\min}(v)\) is the least rank budget whose balanced capacity
in (32) is at least \(v\), then the same selected objective obeys

\[
                 Q\geq\sum_a
                 \max\{h_d(s_a),Q_{\min}(s_a-1)\}.                \tag{29y}
\]

This is an additive row-by-row strengthening of applying the single global
capacity envelope only to \(n=\sum_a(s_a-1)\).

## 4. Exact joint factor-count/exposed-rank envelope

The coarser maximum \(\kappa\) in (24) hides a useful tradeoff.  Suppose
the nonray factors belong to one simple Jordan family with Peirce constant
\(a\), have order at most \(R\), and number at most \(L\).  For fixed total
dual exposed rank \(Q=\sum_iq_i\), (22) sharpens to

\[
 n\leq a\sum_{i=1}^Lp_iq_i
   \leq a\sum_{i=1}^Lq_i(R-q_i).                                    \tag{30}
\]

The exact integer upper envelope of the last rank budget is obtained by
balancing the \(q_i\)'s.  Write

\[
                 Q=uL+t,\qquad u=\lfloor Q/L\rfloor,\qquad 0\leq t<L.
                                                                         \tag{31}
\]

Then

\[
 \boxed{
 {\cal C}_{a,R}(L,Q)
 =a\bigl[(L-t)u(R-u)+t(u+1)(R-u-1)\bigr]}                            \tag{32}
\]

is the maximum of \(a\sum_iq_i(R-q_i)\) over integer
\(0\leq q_i\leq R\) with sum \(Q\).  Indeed, if
\(q_i\geq q_j+2\), transferring one unit from \(q_i\) to \(q_j\)
strictly decreases \(\sum_iq_i^2\), so every maximizer differs by at most
one; (32) follows.  This is an exact **rank-budget** envelope.  It does not
assert that every balanced rank tuple integrates to a product-ball lift.

Feasibility requires

\[
                        n\leq aL\left\lfloor{R^2\over4}\right\rfloor.
                                                                         \tag{33}
\]

On the increasing branch \(0\leq Q\leq L\lfloor R/2\rfloor\), define

\[
 Q_{\min}(n;L,a,R)
 =\min\left\{Q\in\mathbb Z_{\geq0}:
       {\cal C}_{a,R}(L,Q)\geq n\right\}.                            \tag{34}
\]

Every lift in this uniform family satisfies \(Q\geq Q_{\min}\).  Thus
the actual distance coefficient \(\sqrt Q\) in (5) is at least
\(\sqrt{Q_{\min}}\).  The finite logarithmic scale remains the
instance-specific \(\Delta_c\) from (4).

Dropping integrality gives the transparent closed form

\[
 n\leq a\left(RQ-{Q^2\over L}\right),                               \tag{35}
\]

and hence

\[
 \boxed{
 Q\geq {L\over2}\left(
      R-\sqrt{R^2-{4n\over aL}}\right).}                             \tag{36}
\]

Equation (36) shows two regimes.  At light loading,
\(Q\gtrsim n/(aR)\), recovering the per-rank capacity bound.  Near the
maximum curvature load (33), \(Q\) is of order \(LR/2\), so even only
\(L\) densely packed cone factors force a bounded-Dikin distance
coefficient of order \(\sqrt{LR}\), not merely \(\sqrt L\).  For
homogeneous product balls substitute \(n=b(s-1)\).

## 5. Extension from the standard barrier to every self-scaled barrier

The same proof covers the full classified family of self-scaled barriers
on a symmetric cone.  The Hauser--Güler classification states that, up
to an additive constant and the unique irreducible decomposition, every
self-scaled barrier is

\[
                  F_{\alpha}(x)
                  =-\sum_i\alpha_i\log\det_i x_i,
                  \qquad \alpha_i\geq1.                              \tag{37}
\]

An automorphism preserving one irreducible factor changes its Jordan
log-determinant only by an additive constant.  A global automorphism may
also permute isomorphic irreducible factors and hence permute unequal
weights.  Neither operation creates an additional metric case.  Put

\[
 Q_{\alpha}=\sum_i\alpha_iq_i,
 \qquad
 \Phi_{s,\alpha}(x)=
   -\sum_{i:q_i>0}\alpha_i
       \log\det_{c_i}(P(c_i)x_i).                                    \tag{38}
\]

Scaling the factor Hessian by \(\alpha_i\) and repeating (11) gives

\[
                 \|d\Phi_{s,\alpha}(x)\|_{x,\alpha,*}^2
                 =Q_{\alpha}                                       \tag{39}
\]

in the ambient product, and at most this value after affine restriction.
Weighted endpoint AM--GM, now optimized at
\(g_i=\alpha_iq_i\epsilon/Q_{\alpha}\), yields

\[
 \Phi_{s,\alpha}(y)-\Phi_{s,\alpha}(x^c)
 \geq Q_{\alpha}\log{\Delta_{c,\alpha}\over\epsilon},             \tag{40}
\]

where

\[
 \Delta_{c,\alpha}=Q_{\alpha}
 \left[
  \prod_{i:q_i>0}
   \left[
    \det_{c_i}(P(c_i)x_i^c)\det_{c_i}(s_i)
   \right]^{\alpha_i}
   \alpha_i^{-\alpha_iq_i}
 \right]^{1/Q_{\alpha}}.                                           \tag{41}
\]

Therefore (5)--(6) hold verbatim after replacing
\((Q,\Delta_c,F)\) by
\((Q_{\alpha},\Delta_{c,\alpha},F_{\alpha})\).  Since
\(\alpha_i\geq1\), the asymptotic coefficient satisfies
\(\sqrt{Q_{\alpha}}\geq\sqrt Q\): among self-scaled barriers on the
fixed cone decomposition, rescaling cannot beat the standard barrier's
exposed-rank coefficient.  This does **not** extend to arbitrary
self-concordant or coupled barriers on the affine slice.

The classification input is classical and not claimed as new:
[Hauser and Güler, *Self-scaled barrier functions on symmetric cones and
their classification*](https://arxiv.org/abs/math/0103196) and
[Hauser and Lim, *Self-scaled barriers for irreducible symmetric
cones*](https://arxiv.org/abs/math/0104020).  The weighted exposed-minor
distance and iteration consequence (38)--(41) were not found in the
targeted search and remain subject to specialist priority review.

## 6. What packing can and cannot improve

The theorem separates three quantities that should not be conflated:

1. the number of cone factors;
2. the parameter of the restricted standard barrier;
3. the exposed Jordan rank \(Q\) of the optimization objective.

Factor sharing may reduce the first quantity without reducing \(Q\).  In
that case (5) proves directly that the standard-barrier metric still has a
\(\sqrt Q\log(1/\epsilon)\) distance-to-accuracy obstruction.  This is the
abstract reason that PSD column packing does not shorten the already proved
packed-PSD lower bound: one dense block can contain all source columns, but
the summed optimal dual slack still has rank equal to the number of tight
columns.

For bounded-size arbitrary symmetric cones, (22) says that lowering \(Q\)
requires spending more cross-Peirce curvature capacity per exposed rank
unit.  Thus packing can improve the square-root coefficient only by a
genuine increase in cone rank/Peirce capacity, not merely by placing many
rows in one factor or adding unexposed auxiliary directions.

The result is deliberately about the Hessian metric of the standard
product Jordan barrier or, by Section 5, a classified self-scaled barrier.
It does not cover a general custom coupled barrier,
rounds with unbounded intrinsic metric displacement, infeasible iterates,
or quantum procedures that do not generate a sequence of classical
feasible points.  The explicit conversion (6) additionally requires local
norm below one and a bounded number of counted chords per round.  This is
an actual movement lower bound under the stated model, not an iteration
lower bound inferred from a barrier parameter.

Strict complementarity is **not** required for (5): only the rank of one
available dual exposing slack appears.  Strict complementarity is useful
only if one wants to identify \(Q\) with the primal boundary nullity or
with a separately computed restricted-barrier parameter.

## Literature and priority boundary

The Jordan spectral theorem, quadratic-representation formula for the
log-determinant Hessian, generalized principal minors, and Peirce
decomposition are classical.  Generalized Hadamard--Fischer inequalities
in Euclidean Jordan algebras are also known, although the proof above does
not need the full inequality.  Standard IPM analyses use bounded Dikin
steps to obtain upper iteration bounds.

A targeted search of the local corpus and open literature did not locate
the explicit exposed-rank distance formula (5), its exact joint
factor-count envelope (30)--(36), or its product-ball Peirce-capacity
application.  The constant-norm principal-minor identity (8) is best
viewed as classical symmetric-space/generalized-power geometry; novelty is
not claimed for that identity alone.  Nor is the generic conversion from
bounded Dikin movement to a distance lower bound new.  The potentially new
content is the objective-dependent closed form in terms of one exposing
slack's rank and, especially, its immunity to arbitrary inactive-fiber
motion.  Priority remains subject to specialist review.

The direct precedent for converting bounded local moves to an iteration
bound is
[Nesterov and Todd, *On the Riemannian Geometry Defined by
Self-Concordant Barriers and Interior-Point Methods*](https://people.orie.cornell.edu/miketodd/NTRiemann.pdf),
Definition 3.1, Lemma 3.2, and Corollary 3.2.  For a sequence whose chords
have starting-point local norm at most \(\kappa<1\), they prove
\(\rho(x_0,x_N)\leq-N\log(1-\kappa)\), hence
\(N\geq\rho(x_0,x_N)/[-\log(1-\kappa)]\).  Lemma 2.2 gives the generic
barrier-height lower bound, and Lemma 4.1 gives the product-metric
\(\ell_2\) rule.  Their Theorem 5.2 and Corollary 5.1 additionally prove
that primal--dual central-path segments are within a factor \(\sqrt2\) of
geodesic and give an optimality statement for short-step primal--dual
path-following; they explicitly do not obtain the analogous pure-primal
claim.

The target-set viewpoint is also explicit in
[Nesterov and Nemirovski, *Primal Central Paths and Riemannian Distances
for Convex Sets*](https://doi.org/10.1007/s10208-007-9019-4).  Their
Example 1.1 shows on the orthant that a central-path endpoint can be much
farther from the start than another point in the same target hyperplane.
Writing \(\sigma\) for Riemannian distance, Theorem 4.1 gives

\[
 \rho[x(\cdot),t_0,t_1]
 \leq \log2+\nu^{1/4}
 \sqrt{\sigma(x(t_0),x(t_1))
       [\sigma(x(t_0),x(t_1))+\log12]},
\]

with the sharper \(\nu^{1/4}\sqrt{\sigma(\sigma+\log3)}\) form when the
starting Newton decrement is at least \(1/2\).  Corollary 5.1 gives, under
its bounded-feasibility assumptions,
\(\rho[x(\cdot),0,1]\leq O(1)\nu^{1/4}[\sigma(0,F)+\log\nu]\).
Therefore neither distance to the whole target set nor its use as a
short-step benchmark is a priority claim here.

The present result is narrower: it calculates that target-set distance
from below by the exposed-rank quantity in (5), for the standard Jordan
barrier, without a central-path assumption and despite unbounded inactive
fibers.  Also nearby is
[Permenter, *A geodesic interior-point method for linear optimization over
symmetric cones*](https://arxiv.org/abs/2008.08047), which constructs and
analyzes geodesic-update algorithms rather than proving the obstruction
(5).

A modern geometric neighbor is
[Lemmens, *Horofunction Compactifications of Symmetric Cones under Finsler
Distances*](https://doi.org/10.54330/afm.141190).  It describes
horofunction boundaries using Jordan faces and support idempotents, but for
the Thompson and Hilbert Finsler metrics.  It does not use the Hessian
Riemannian metric of the Jordan log-determinant or give an
objective-accuracy theorem.  This reinforces the conservative view that
support-idempotent/Busemann geometry is classical while the optimization
formula (5) is the candidate synthesis.

The Peirce-capacity statement (22)--(27) has a different scope from
[Aubrun--La Piana--Müller-Hermes, *Factorization Through Lorentz
Cones*](https://arxiv.org/abs/2606.27825).  That paper classifies when
positive linear maps between proper cones factor through direct sums of
Lorentz cones.  It does not treat nonlinear primal and dual factors of a
product-ball slack operator, mixed contact derivatives, or curvature per
rank of the summed exposing slack.  Likewise, general lift/factorization
theory and semidefinite extension degree do not retain the exposed-rank
ledger in (22).  No direct antecedent for
\(\sum_a(s_a-1)\leq\sum_i a_ip_iq_i\leq\kappa Q\) was located.

The one-ball premium (29a)--(29c) was screened separately.  Sparse SOCP
formulation work such as
[Kobayashi--Kim--Kojima, *Sparse Second Order Cone Programming
Formulations for Convex Optimization
Problems*](https://doi.org/10.15807/jorsj.51.241) studies auxiliary-variable
choices, Schur-complement sparsity, and the computational benefit of larger
cones, but proves no dimension-capped factor lower bound or smooth-support
topology.  Fawzi's SOC nonrepresentability theorem and the Lorentz
factorization work above address other source/target cones and do not use a
sphere-to-product covering obstruction.  No source was located for the
claim that, when \(N-1=L(d-2)\), a globally labelled bi-\(C^1\) fixed
certificate sheet forces **some** objective to have \(Q\geq L+1\).
Topology of static finite-matrix PSD factorization spaces was studied by
[Fawzi--Gouveia--Parrilo--Robinson--Thomas](https://arxiv.org/abs/1407.4095),
and fixed-block PSD-lift lower bounds were proved by
[Fawzi--Parrilo](https://arxiv.org/abs/1311.2571) and
[Fawzi--Safey El Din](https://arxiv.org/abs/1705.06996).  Those are important
precedents, but they do not use a globally \(C^1\) factor field over a ball
contact sphere, primitive-support finite covers, or objectivewise aggregate
Jordan rank.  Accordingly (29a) and the sequential theorem (29u) are
plausible candidate results only in their stated selected-factor model.
They are existential in the objective and are not unconditional lower
bounds for arbitrary affine lifts, nonsmooth norm-tree formulations, every
objective, arbitrary barriers, or arbitrary QIPMs.

Useful background sources include Faraut and Kor\'anyi, *Analysis on
Symmetric Cones*, for quadratic representations, Peirce algebras and
generalized power functions;
[Gowda and Tao, *Some inequalities involving determinants, eigenvalues,
and Schur complements in Euclidean Jordan
algebras*](https://userpages.umbc.edu/~gowda/papers/trGOW10-02.pdf);
and standard self-concordance texts for (18).
Precise bibliographic attribution should be checked before paper use.

## Audit checklist

- Verify the compression identity (10) and the exact norm \(q\) in (11)
  for reducible algebras and the exceptional factor.
- Check the normalization of primitive idempotents and support determinants in
  (14)--(17).
- Re-derive the summed-slack Peirce rank bound (22), including factors in
  which the individual row supports overlap.
- Check the approximate-start subtraction and every constant in (6).
- Search specifically for prior Busemann/principal-minor formulations of
  (5), distinguishing a classical metric identity from the new
  distance-to-accuracy and iteration application.
- Verify that the fixed global certificate sheet in (29a)--(29c) follows
  from every intended lift hypothesis; otherwise state the theorem only
  for selected factorizations that explicitly supply it.

## Independent audit

Two independent hostile audits rederived the compression identity
\(P(c)P(x)P(c)=P(P(c)x)\) and the exact squared dual norm \(q\), including
for reducible products and the exceptional Jordan algebra.  They checked the
normalization of support idempotents, every power and constant in
(14)--(17), and the approximate-start and bounded-chord conversion in (6).
They also rederived the summed-row slack argument when individual dual
supports overlap and confirmed that the mixed form uses only the
\(a_ip_iq_i\)-dimensional cross-Peirce channel.  One audit requested that
the global affine-slice certificate implicit in the phrase “dual row
factor” be made explicit before combining (5) with (22); that presentation
gap was repaired above.  No mathematical constant or conclusion changed.

A further hostile audit checked the exact discrete envelope (32) both
symbolically and by exhaustive small-rank enumeration.  It verified
monotonicity on the lower branch, the odd-order plateau, the feasibility
threshold (33), and the continuous root (36).  The same audit checked the
Hauser--Güler classification normalization in (37), rederived the weighted
dual norm \(Q_\alpha\), and independently optimized all endpoint gap
allocations in (40)--(41).  It noted only that a global cone automorphism
can permute isomorphic irreducible factors; the prose above now states this
explicitly.  The weighted theorem and constants passed unchanged.

The same auditor then checked the invariant strengthening from a minimum
positive eigenvalue to the full support determinant.  It verified in every
Euclidean Jordan algebra that
\(\det_c(P(s^{1/2})a)=\det_c(s)\det_c(a)\) and
\(\operatorname{tr}_c(P(s^{1/2})a)=\langle s,a\rangle\), and rechecked
both the standard and \(\alpha\)-weighted gap allocations.  Equations
(4), (14)--(17), and (40)--(41) passed with the stronger constants.

Finally, the one-ball divisibility premium (29a)--(29c) was hostile-audited
with its essential existential quantifier.  The audit checked rank
semicontinuity and fixed active labels, every equality in the Peirce
capacity chain, the rank-two spin-orbit identification, and both the
fundamental-group and cohomology exclusions.  It confirmed that zero-rank,
ray, lower-dimensional, and unequal-factor cases cannot survive equality.
The conclusion is that at least one support objective has the extra exposed
rank unit; no claim is made for every prescribed objective.

The heterogeneous Hermitian private-support theorem (29d)--(29h) also
passed an independent audit.  It checked the range of a positive weighted
sum over all three division algebras, the cylindrical annihilation and
quotient factorization, and joint independence of private complements.  In
particular, a quaternionic Hermitian cross block has real dimension
\(4p_id_{ia}\), not twice that value, because its conjugate block carries no
independent degrees of freedom.  The sourcewise ceiling and its
standard/self-scaled movement consequence passed unchanged.

A follow-up audit verified the mixed-field/varying-order Hermitian form
(29i)--(29k) and the Lorentz mixture (29l)--(29n).  It checked that
cylindrical complementarity must be differentiated in Jordan-product form:
on a Lorentz cross-Peirce space, multiplication by the complementary
primitive idempotent is one half, so a second nonzero row on the same ray
kills the first row's mixed channel.  Hence every productive Lorentz rank
unit is source-private, and blockwise private counts add across mixed
classical factors exactly as stated.

Two further hostile audits independently checked the Albert incidence
lemma (29o)--(29p), including the nonassociative case directly in
Jordan-product and Peirce language.  They verified the vertex cases, the
one-half Peirce action for rank-one support, invertibility of
\(L_{S_{-a}}\) for an interior slack in the complementary rank-two spin
face, and the argument excluding three productive rows at aggregate rank
two.  They also checked the token ledger: an Albert block serves at most
\(q_i\) productive sources, each through at most 16 real cross-Peirce
dimensions, while nonzero curvature-flat rows need no token.  Thus the
universal mixed-factor sourcewise bounds (29r)--(29s), including the
dimension-cap corollary, passed unchanged.

An additional hostile audit rederived the support-join compression identity
(29w) in an arbitrary Euclidean Jordan algebra.  It checked that prior-row
complementarity holds on the whole remaining product cylinder, Peirce
compression preserves the exact next-row factorization, all remaining face
cones obey the dimension cap, and future-coordinate changes do not disturb
earlier support choices.  It also checked the Albert rank-two face and the
distinction between compressed factors, which need not be global dual
certificates, and the final uncompressed exposing slack, which is.  The
telescoping additive hard-rank theorem (29u) and its movement consequence
(29x) passed unchanged.  A follow-up audit rederived the stagewise Peirce
capacity program and confirmed (29y), with the important qualification that
the actual remaining-face rank program is bounded below by, but need not
equal, the padded balanced envelope \(Q_{\min}\).
