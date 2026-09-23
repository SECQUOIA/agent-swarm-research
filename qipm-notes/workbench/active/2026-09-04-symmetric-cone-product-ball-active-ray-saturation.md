# Active-ray saturation over all symmetric cones forces separate spin factors

Status: Proved; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Theorem

Let

\[
 C=\prod_{a=1}^hB_2^{s_a},\qquad
 M=\prod_{a=1}^hS^{p_a},\qquad p_a=s_a-1\geq1,
 \qquad n=\sum_ap_a.                                      \tag{1}
\]

Suppose the full extreme-row slack family has globally labelled \(C^1\)
factors over finitely many irreducible symmetric cones and scalar rays:

\[
 1-x_a^Tz
 =\sum_i\langle X_i(x),Y_i^a(z)\rangle_i
   +\sum_j\alpha_j(x)\beta_j^a(z).                       \tag{2}
\]

Here \(X_i,Y_i^a\) belong to the cone of squares of a simple Euclidean
Jordan algebra \(V_i\) of rank \(r_i\), dimension \(m_i\), and Peirce
constant \(a_i\); all scalar factors are nonnegative.  Put

\[
                  c_i=a_i\left\lfloor {r_i^2\over4}\right\rfloor.
                                                               \tag{3}
\]

Then

\[
                              n\leq\sum_i c_i.             \tag{4}
\]

If equality holds, every positive-capacity block is a rank-two spin
factor.  Moreover, after relabelling the blocks,

\[
                    \boxed{\ m_i=p_i+2=s_i+1\quad(i=1,\ldots,h)\ },
                                                               \tag{5}
\]

so there is exactly one positive block \(Q_{s_a+1}\) for each source
ball.  Each positive block serves only its assigned row:

\[
                        Y_i^d\equiv0\qquad(d\ne i).        \tag{6}
\]

Finite active ray factors may remain, but they carry no contact
mixed-curvature channel.  Thus no cross-source sharing is possible at
minimum total symmetric-cone curvature capacity.  Conversely, the
standard separate Lorentz factorization attains (4)--(6).  Ignoring
optional ray factors, its forced resource ledger is

\[
       L_+=h,\qquad M_+=\sum_a(s_a+1)=n+2h,\qquad
       \nu_{\rm normal}=2h.                              \tag{6a}
\]

Each appended ray adds one to all three ambient counts \(L,M,\nu\) but
does not change curvature capacity.  Consequently, if the profile (5)
fails, the integer gap is

\[
                              \sum_i c_i\geq n+1.           \tag{7}
\]

This extends the Hermitian active-ray classification to arbitrary spin
dimensions and the exceptional algebra \(H_3(\mathbb O)\).
In particular, under a uniform cone-dimension cap \(d\), equality is
impossible whenever some \(s_a+1>d\).

## 1. Equality produces a product-orbit covering

Fix a simultaneous contact \(z=x_a\) in every row.  Every term of (2) is
nonnegative and its row sum is zero.  A scalar ray term has zero mixed
derivative on the contact tangent spaces: if one factor is zero, its
tangential derivative is zero; if it is positive, the other factor and
its derivative are zero.  Put

\[
 Y_i(x)=\sum_aY_i^a(x_a),\qquad
 p_i'=\operatorname {rank}X_i(x),\qquad
 q_i'=\operatorname {rank}Y_i(x).                         \tag{8}
\]

Jordan complementarity and the Peirce mixed-channel bound give

\[
 n\leq\sum_i a_i p_i'q_i'
   \leq\sum_i a_i\left\lfloor {r_i^2\over4}\right\rfloor.
                                                               \tag{9}
\]

If (4) is an equality, every inequality in (9) is an equality at every
contact.  Each block has constant balanced complementary ranks.  Taking
the primal support idempotent, or its complement for the opposite odd-rank
convention, gives a \(C^1\) map

\[
 \Sigma:M\longrightarrow
   \prod_i\mathcal I_{\lfloor r_i/2\rfloor}(V_i).         \tag{10}
\]

The support differential is exactly the cross-Peirce component seen by
the mixed channel.  Hence \(d\Sigma\) is injective.  Its source and target
both have dimension \(n\), so (10) is a local diffeomorphism.  Compactness
of \(M\) makes it a finite covering.

This is the product-source version of
[Saturated symmetric-cone factors induce idempotent-orbit
coverings](2026-09-04-symmetric-cone-support-orbit-rigidity.md).  Active
rays do not affect the proof because their mixed rank is zero.

## 2. The only support-orbit factors that survive are spheres

Lift (10) to universal covers.  The lift is a diffeomorphism, and the
source universal cover is homotopy equivalent to the product of the
source spheres of dimension at least two, with one contractible real-line
factor for every source circle.

The classification of simple Euclidean Jordan algebras gives the target
orbits:

1. a spin factor \(Q_m\) has primitive-idempotent orbit \(S^{m-2}\);
2. real, complex, and quaternionic Hermitian factors have balanced
   Grassmannian orbits; and
3. \(H_3(\mathbb O)\) has orbit \(\mathbb OP^2\).

The independently audited Hermitian theorem
[Active rays do not enlarge the Hermitian saturation
profiles](2026-09-04-hermitian-product-ball-active-ray-covering.md)
uses fundamental groups, Schubert squares, low homotopy, and integral
indecomposables to exclude every non-spin Hermitian orbit except the two
intermediate real possibilities

\[
             \mathbb{RP}^2,\qquad
             \operatorname {Gr}_2(\mathbb R^4).           \tag{11}
\]

That proof is unchanged when additional target factors are spheres: the
obstructing square or torsion class remains in the product by the Kunneth
theorem.  The exceptional plane is excluded even more directly:

\[
 H^*(\mathbb OP^2;\mathbb F_2)
       \cong\mathbb F_2[u]/(u^3),\qquad |u|=8,\qquad u^2\ne0.          \tag{12}
\]

Every positive-degree class in the mod-two cohomology of a product of
spheres has square zero.  Thus \(\mathbb OP^2\) cannot be a target factor.

Finally, the independently audited cylinder theorem
[Cylinder integrability excludes the last real low-order saturation
cases](2026-09-04-real-low-order-cylinder-exclusion-product-balls.md)
excludes both orbits in (11).  Its proof uses only the two assigned
\(S^2\) rulings, fixed-kernel cylinders, and the fact that all other target
factors have sphere universal covers.  Arbitrary spin factors therefore
do not alter it.

All target factors in (10) are now spin-factor spheres.  The free-abelian
rank of the fundamental group matches circle factors, and the graded
indecomposable quotient of mod-two cohomology matches the remaining sphere
dimensions with multiplicity.  Hence the target sphere dimensions are
exactly the multiset \(\{p_a:a\in[h]\}\), proving (5).  Within each fixed
dimension, the induced map on indecomposables is an invertible matrix.
Choose a nonzero determinant monomial; it bijectively matches target
spheres to source spheres so that every matched one-coordinate restriction
has nonzero degree.  Apply the same argument to the invertible rational
matrix on \(\pi_1\) for circle factors.  This is the assignment used below;
the covering itself need not split as a product map.

## 3. A cylinder also forbids cross-row service

Let spin block \(i\) be assigned to source \(a\).  Fix a different row
\(d\) at contact and vary \(x_a\), holding all other source coordinates
fixed.  Termwise complementarity gives

\[
                         X_i(x)\circ Y_i^d(x_d)=0          \tag{13}
\]

along the whole \(x_a\)-cylinder.  If \(Y_i^d(x_d)\ne0\), it has a
nonzero support idempotent orthogonal to the primitive support of
\(X_i(x)\).  A rank-two Jordan algebra has a unique primitive idempotent
orthogonal to a given nonzero primitive idempotent.  Equivalently, fixing
one nonzero complementary element fixes the opposite Lorentz boundary
ray.  Thus the normalized primal support is constant along the cylinder.

But the restriction of the support map to its assigned source sphere has
nonzero primitive degree (or nonzero winding for a circle), because it is
the corresponding factor of the universal-cover cohomology assignment.
This contradiction shows that \(Y_i^d(x_d)=0\).  Since the contact point
\(x_d\) was arbitrary, (6) follows.

## Scope and novelty boundary

The result assumes exact capacity equality, globally labelled \(C^1\)
full-row factors, finitely many irreducible symmetric-cone blocks, and
finitely many scalar rays.  It is not an unrestricted extension-complexity
lower bound and does not apply to unlabelled lifts without global factor
selections.  The theorem concerns curvature capacity, not the number of
rays or an arbitrary coupled barrier parameter.

The EJA classification, idempotent orbits, and their topology are
classical.  The Hermitian and low-order cylinder ingredients are proved in
the linked audited notes.  The apparently new synthesis is the exact
all-symmetric-cone product-ball saturation profile (5), including active
rays, the exceptional-octonionic exclusion, and the no-sharing conclusion
(6).  A targeted search found the recent paper Aubrun--La Piana--
Müller-Hermes,
[*Factorization through Lorentz cones*](https://arxiv.org/abs/2606.27825),
which classifies when **all positive maps** between a pair of cones factor
through direct sums of Lorentz cones.  Its Lorentz-factorization property
is different from equality in the contact-curvature capacity of one
globally \(C^1\) product-ball slack factorization, and it does not state
(5)--(6).  No source found in the targeted search states this saturation
or no-sharing theorem, but priority remains subject to specialist review.

## Independent hostile audit

The audit reconstructed the product-source EJA support covering with ray
terms invisible to mixed curvature.  It checked that the Hermitian
square, torsion, and low-order cylinder obstructions persist after
adjoining arbitrary sphere factors, and that \(u^2\ne0\) excludes the
octonionic plane from any product-sphere universal cover.

The audit also checked the potentially delicate assignment step.  The
degreewise map on indecomposables, and the rational map on \(\pi_1\) for
circles, admit a nonzero determinant matching; this supplies nonzero-degree
one-source restrictions without assuming that the covering splits.
Finally, the unique complementary primitive ray in every rank-two EJA
makes any unrelated nonzero dual row factor freeze the assigned support,
proving (6).  No correction was found.
