# Contact-curvature packing for products of spectral-norm balls

Status: Proved and independently hostile-audited over
\(\mathbb R,\mathbb C,\mathbb H\)  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the local theorem; novelty pending specialist review

## Result

Let

\[
 \mathcal E_a=\{X\in\mathbb R^{r_a\times c_a}:XX^T=I_{r_a}\},
 \qquad 1\leq r_a\leq c_a,                              \tag{1}
\]

be the extreme manifold of a rectangular spectral-norm ball, and let

\[
 \mathcal Z_a=\{uv^T:\|u\|=\|v\|=1\}                    \tag{2}
\]

be the extreme manifold of its nuclear-norm polar.  Suppose the full
extreme slack rows of a product of such balls have a globally \(C^1\)
factorization through proper cones:

\[
 1-\langle X_a,Z\rangle_F
   =\sum_{i=1}^L\langle A_i(X_1,\ldots,X_k),B_i^a(Z)\rangle,
 \quad X_b\in\mathcal E_b,\ Z\in\mathcal Z_a.            \tag{3}
\]

Write \(m_i=\dim K_i\geq3\), \(q_i=m_i-2\), and

\[
 f_i=\max_{0\ne y\in K_i^*}\dim(K_i\cap y^\perp),
 \qquad \bar f_i=\min(f_i,k).                            \tag{4}
\]

At a contact \(\langle X_a,Z_a\rangle_F=1\), define the mixed channel

\[
 M_i^a(H,\dot Z)
   =-\langle D_aA_i[H],DB_i^a[\dot Z]\rangle,
 \qquad t_i^a=\operatorname{rank}M_i^a.                 \tag{5}
\]

Then the total row curvature has the exact rank

\[
 \boxed{\operatorname{rank}
  \bigl((H,\dot Z)\mapsto-\langle H,\dot Z\rangle_F\bigr)
       =c_a-1.}                                         \tag{6}
\]

For \(I_i=\{a:t_i^a>0\}\), every cone block obeys

\[
 \boxed{
 \sum_{a\in I_i}t_i^a\leq m_i-1,\qquad
 1+\sum_{b\in I_i\setminus\{a\}}t_i^b
       \leq\dim(K_i\cap B_i^a(Z_a)^\perp)
       \quad(a\in I_i).}                                \tag{7}
\]

In particular,

\[
 t_i^a\leq q_i,\qquad |I_i|\leq\bar f_i,\qquad
 \sum_it_i^a\geq c_a-1.                                 \tag{8}
\]

These pointwise identities give, without any whole-row assignment,

\[
 \boxed{
 \begin{aligned}
 \sum_i\bar f_i
   &\geq\sum_{a=1}^k
       \left\lceil{c_a-1\over d-2}\right\rceil,\\
 \sum_i\bar f_iq_i&\geq\sum_{a=1}^k(c_a-1),\\
 \sum_i(q_i+1)&\geq\sum_{a=1}^k(c_a-1),
 \end{aligned}}                                        \tag{9}
\]

whenever \(m_i\leq d\).  If also \(f_i\leq f\), then

\[
 \boxed{
 L\geq\left\lceil{1\over f}
      \sum_a\left\lceil{c_a-1\over d-2}\right\rceil\right\rceil,
 \qquad
 \sum_iq_i\geq
      \left\lceil{\sum_a(c_a-1)\over f}\right\rceil.}    \tag{10}
\]

Unlike the whole-row dimension theorem, (6)--(10) allow the slack row of
one matrix ball to be split among many cone blocks.  They are local
curvature bounds: no topological divisibility premium or exact attainment
is claimed.

## 1. The spectral contact normal form

At contact, \(Z=uv^T\) and \(\langle X,Z\rangle_F=1\).  Since
\(\|X\|_{\rm op}=1\), equality in Cauchy--Schwarz gives

\[
                         Xv=u,\qquad X^Tu=v.             \tag{11}
\]

Choose orthogonal bases in which

\[
 X=\begin{pmatrix}I_r&0\end{pmatrix},\qquad u=e_1,\quad v=e_1.
                                                               \tag{12}
\]

A tangent vector to \(\mathcal E=\{X:XX^T=I_r\}\) has the form

\[
 H=\begin{pmatrix}A&B\end{pmatrix},
 \qquad A^T=-A,\quad B\in\mathbb R^{r\times(c-r)}.        \tag{13}
\]

Locally a tangent to \(\mathcal Z\) is represented uniquely by

\[
 \dot Z=\dot u\,e_1^T+e_1\dot v^T,\qquad
 \dot u\perp e_1,\quad\dot v\perp e_1.                  \tag{14}
\]

Put \(a_j=A_{j1}\) for \(j=2,\ldots,r\), and let
\(b\in\mathbb R^{c-r}\) be the first row of \(B\).  Then

\[
 \langle H,\dot Z\rangle_F
   =\sum_{j=2}^ra_j(\dot u_j-\dot v_j)
        +\sum_{j=r+1}^cb_j\dot v_j.                     \tag{15}
\]

The \(r-1\) variables \(a_j\) and \(c-r\) variables \(b_j\) are
independent.  Thus (15), and hence the full mixed slack curvature, has rank
\((r-1)+(c-r)=c-1\).  Orthogonal invariance proves (6) at every contact.
The missing \(r-1\) polar directions are genuine contact degeneracies:
moving \(u\) and the first \(r\) coordinates of \(v\) together is invisible
to first mixed order.

## 2. Factorwise quotient rank and cross-row annihilation

Every summand in (3) is nonnegative.  At contact their sum is zero, so
each summand vanishes.  If either \(A_i\) or \(B_i^a\) is a cone vertex,
its derivative is zero; an active mixed channel therefore has two nonzero
complementary values.  The standard tangent-ray quotient argument makes
the mixed pairing factor through spaces of dimension at most \(m_i-2\),
which proves \(t_i^a\leq q_i\).  Mixed differentiation of (3), followed by
rank subadditivity and (6), gives

\[
                         \sum_it_i^a\geq c_a-1.          \tag{16}
\]

Fix row \(a\) at contact and vary an unrelated primal source \(b\ne a\).
The \(i\)-th summand remains a nonnegative function equal to zero.
Differentiating first along the polar row and then along source \(b\)
gives

\[
 \langle D_bA_i[H_b],DB_i^a[\dot Z_a]\rangle=0
                         \qquad(b\ne a).                 \tag{17}
\]

For fixed \(i\), let \(\Lambda_a\) be pairing with
\(DB_i^a[T_{Z_a}\mathcal Z_a]\).  Choose
\(E_a\subseteq\operatorname{im}D_aA_i\) of dimension \(t_i^a\) on which
\(\Lambda_a\) is injective.  Equation (17) annihilates \(E_b\) for
\(b\ne a\), while contact differentiation annihilates the nonzero vector
\(A_i\).  Applying each \(\Lambda_a\) to a linear dependence proves that

\[
                     \mathbb RA_i\oplus\bigoplus_{a\in I_i}E_a
                                                               \tag{18}
\]

is a direct sum.  This proves the first inequality in (7).

For a fixed active row \(a\), the full unrelated-source cylinder lies in
the exposed face \(K_i\cap B_i^a(Z_a)^\perp\).  Hence
\(E_b\) lies in the span of that face for every \(b\ne a\).  The
corresponding subspace
\(\mathbb RA_i\oplus\bigoplus_{b\ne a}E_b\) proves the second inequality
in (7).  Since every active \(t_i^a\geq1\), it also gives
\(|I_i|\leq f_i\), and trivially \(|I_i|\leq k\).

## 3. Summed cap ledgers

Let \(N_a=|\{i:t_i^a>0\}|\).  Equations (8) and \(q_i\leq d-2\) give

\[
 N_a\geq\left\lceil{c_a-1\over d-2}\right\rceil.         \tag{19}
\]

Count block--row incidences and capacity-weighted incidences:

\[
 \sum_aN_a=\sum_i|I_i|\leq\sum_i\bar f_i,               \tag{20}
\]

\[
 \sum_a\sum_{i\in I_i}q_i
       =\sum_i|I_i|q_i\leq\sum_i\bar f_iq_i.             \tag{21}
\]

The left side of (21) is at least
\(\sum_{a,i}t_i^a\geq\sum_a(c_a-1)\).  Finally, summing the first
inequality of (7) gives

\[
 \sum_a(c_a-1)\leq\sum_{a,i}t_i^a
                    \leq\sum_i(m_i-1)=\sum_i(q_i+1).     \tag{22}
\]

Equations (19)--(22) prove (9).  Under \(f_i\leq f\),
\(\bar f_i\leq f\), so (10) follows.

## 4. Complex spectral balls

The theorem has a complex analogue under the real Frobenius pairing.  Let
\(X\in\mathbb C^{r\times c}\), \(XX^*=I_r\), and let
\(Z=uv^*\) be a nuclear-ball extreme point.  At contact, choose unitary
bases giving (12), now with

\[
 H=\begin{pmatrix}A&B\end{pmatrix},\qquad A^*=-A.        \tag{23}
\]

Use the phase gauge \(u^*\dot u=0\).  Then
\(\dot v_1=i\gamma\) for one real variable \(\gamma\), while
\(\dot u_j,\dot v_j\) are complex for \(j\geq2\).
The first column entries \(A_{j1}\) pair with the complex differences
\(\dot u_j-\dot v_j\); the first row of \(B\) pairs with the remaining
complex coordinates of \(\dot v\); and the imaginary diagonal entry
\(A_{11}\) pairs with \(\gamma\).  These directions are independent, so

\[
 \boxed{\operatorname{rank}_{\mathbb R}
   \bigl((H,\dot Z)\mapsto
           -\operatorname{Re}\operatorname{tr}(H^*\dot Z)\bigr)
       =2c-1.}                                           \tag{24}
\]

All cone-factor arguments are real linear and therefore unchanged.  Thus
(9)--(10) hold for complex spectral balls after replacing every
\(c_a-1\) by \(2c_a-1\).  The cone dimensions \(m_i\), face dimensions,
and cap \(d\) remain real dimensions.  In particular, the mixed-curvature
rank is not simply twice the real value: the relative phase contributes
the additional one-dimensional channel.

## 5. Quaternionic spectral balls and the division-algebra formula

The same calculation works over \(\mathbb H\), viewing the matrix space
as a real Euclidean space with pairing
\(\operatorname {Re}\operatorname {tr}(H^*\dot Z)\).  Write
\(\delta=\dim_{\mathbb R}\mathbb F\) for
\(\mathbb F\in\{\mathbb R,\mathbb C,\mathbb H\}\).  The representation
\(Z=uv^*\) is unchanged when \(u\) and \(v\) are multiplied on the right
by the same unit scalar.  Infinitesimally, this phase freedom has
dimension \(\delta-1\) and permits the gauge
\[
                             u^*\dot u=0.                \tag{25}
\]
The remaining diagonal coordinate \(v^*\dot v\) is imaginary and has
\(\delta-1\) real dimensions.  In the normal form (12), the first-column
entries \(A_{j1}\) give \(\delta(r-1)\) off-axis difference channels, the
first row of \(B\) gives \(\delta(c-r)\) rectangular-tail channels, and
the imaginary diagonal \(A_{11}\) pairs nondegenerately with the
\(\delta-1\) relative-phase directions.  Hence, uniformly over the three
real division algebras,
\[
 \boxed{\operatorname{rank}_{\mathbb R}
   \bigl((H,\dot Z)\mapsto
    -\operatorname {Re}\operatorname {tr}(H^*\dot Z)\bigr)
       =\delta c-1.}                                    \tag{26}
\]
For \(\mathbb H\), the last channel is the ordinary Euclidean pairing
between the three-dimensional spaces of imaginary diagonal quaternions;
noncommutativity causes no ambiguity because only the real part of the
trace is used.

All factor-cone arguments in Sections 2--3 are real linear.  They
therefore give the quaternionic and unified division-algebra versions of
(9)--(10) after replacing each real row budget \(c_a-1\) by
\(\delta_a c_a-1\), where different rows may use different division
algebras.  Cone dimensions and face dimensions are always counted over
\(\mathbb R\).

## Scope and novelty boundary

The geometry of Stiefel manifolds, equality in spectral/nuclear duality,
and tangent-ray quotient bounds are classical.  The companion
[whole-row grouping theorem](2026-09-04-spectral-norm-face-capped-grouping-frontier.md)
uses ordinary function rank to obtain a much stronger \(rc+1\) dimension
bound when each complete row family is assigned to one cone.  The present
result has a different scope: it allows arbitrary row splitting and
extracts the exact nonzero mixed-curvature rank
\(\delta c-1\), where \(\delta=\dim_{\mathbb R}\mathbb F\).

The direct-sum face-packing proof extends the audited Euclidean-ball theorem
in
[Bounded complementary faces interpolate between no-sharing and packed
cone blocks](2026-09-04-bounded-face-sharing-product-ball-factors.md).
A targeted literature search found no prior use of the degenerate
spectral-ball contact pairing to prove cone-factor dimension/face packing
bounds.  No priority claim is made pending specialist review.

The result assumes globally labelled \(C^1\) factors on all primal and
polar extreme manifolds.  It does not apply to merely pointwise,
unlabelled, or nonsmooth factorizations.  It gives no lower bound on the
cost of evaluating a barrier or on quantum queries.

## Audit targets

1. Verify the extreme-manifold descriptions and the contact normal form
   (11)--(14), including \(r=1\), \(r=c\), and rectangular cases.
2. Recompute the mixed rank in (15) and confirm that it is \(c-1\), not
   \(r+c-2\).
3. Check the tangent-ray quotient bound and every use of \(C^1\) mixed
   differentiation.
4. Check the direct-sum and exposed-face proof of (7).
5. Recompute all incidence, capacity, and floor/ceiling bounds in
   (9)--(10).
6. Check the complex phase gauge and the extra relative-phase channel in
   (23)--(24).
7. Check the quaternionic phase quotient, noncommutative pairing, and
   unified rank \(\delta c-1\) in (25)--(26).

## Independent hostile audit

The audit recomputed the contact geometry in the normal form (12).
For \(H=(A,B)\), only the \(r-1\) entries \(A_{j1}\) and the \(c-r\)
entries in the first row of \(B\) pair with a polar tangent, and the
corresponding polar combinations are independent.  The mixed rank is
therefore exactly \(c-1\), including the edge cases \(r=1\) and \(r=c\).

For each cone factor, nonnegativity on the unrelated-source cylinder
first kills the polar derivative and then gives (17) using only the
separate \(C^1\) regularity of the two factors.  Applying the row
pairing maps to a putative dependence verifies the direct sum (18).
The same subspaces lie in the appropriate exposed-face spans, proving
both inequalities in (7).  The tangent-ray quotient gives the remaining
\(m_i-2\) bound.  Finally, independent incidence counting reproduces
every inequality and ceiling in (9)--(10).  No correction was required.

For the complex extension, quotienting the simultaneous phase of
\((u,v)\) permits the gauge \(u^*\dot u=0\), while
\(\dot v_1=i\gamma\) retains the relative phase.  The complex
off-axis difference channels contribute \(2(r-1)\), the rectangular
tail contributes \(2(c-r)\), and the imaginary diagonal of \(A\) pairs
nontrivially with \(\gamma\).  Their total real rank is therefore
\(2c-1\), including \(r=1\) and the square case.

A further hostile audit checked the quaternionic extension.  With right
\(\mathbb H\)-modules, the simultaneous transformation
\((u,v)\mapsto(uq,vq)\) leaves \(uv^*\) fixed.  Its three-dimensional
infinitesimal phase removes the imaginary quaternion \(u^*\dot u\), while
the imaginary value \(v^*\dot v\) remains as the relative phase.
Quaternionic skew-Hermiticity gives \(A_{1j}=-\overline{A_{j1}}\), so the
real-trace pairing is the ordinary nondegenerate real inner product on
each four-dimensional off-axis channel and on the three-dimensional
imaginary diagonal channel.  The count is
\(4(r-1)+4(c-r)+3=4c-1\).  Since the rest of the proof is real linear,
mixed real, complex, and quaternionic source rows obey the unified
\(\delta_ac_a-1\) ledgers.  No correction was required.
