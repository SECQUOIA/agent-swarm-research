# Shared-scale and chordal packing for products of spectral-norm balls

Status: Proved; targeted literature screen and independent hostile audit completed  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High within the stated barrier-model scope

## Result

For \(a=1,\ldots,k\), let
\[
       \mathbb B_a=\{X_a\in\mathbb R^{r_a\times c_a}:
                         \|X_a\|_{\rm op}\leq1\},
 \qquad \rho_a=\min\{r_a,c_a\}.                            \tag{1}
\]
Transpose blocks so that \(r_a=\rho_a\leq c_a\).  If a row group
\(G\subseteq[k]\) is represented by one shared-scale cone
\[
 \mathcal S_G=
 \{(t,(X_a)_{a\in G}):t\geq0,\ \|X_a\|_{\rm op}\leq t
                                      \text{ for all }a\in G\}, \tag{2}
\]
then
\[
                    \nu_{\rm opt}(\mathcal S_G)
                       =1+\sum_{a\in G}\rho_a.             \tag{3}
\]
Its exact maximum complementary-face dimension is
\[
  1+\sum_{a\in G}r_ac_a-\min_{a\in G}(r_a+c_a-1),
\]
so both the barrier cost and the exposed-face cost of matrix-row sharing
are explicit.
For a partition into \(g\) groups, arbitrary coupling between the cone
factors cannot lower the exact ambient value
\[
          \nu_{\rm opt}\!\left(\prod_{G\in\mathcal G}\mathcal S_G\right)
                    =g+\sum_{a=1}^k\rho_a.                \tag{4}
\]

The fixed-scale slice \(t_G=1\) has exact affine barrier parameter
\[
                              \sum_{a=1}^k\rho_a,          \tag{5}
\]
independent of the grouping.  Thus sharing \(k\) spectral-norm cones into
one reduces the exact ambient parameter from
\(\sum_a(\rho_a+1)\) to \(1+\sum_a\rho_a\), but leaves the reduced barrier
geometry unchanged.

There is a complementary chordal PSD-completion construction for matrices
with a common row size \(s\).  A star with an \(s\)-vertex hub and leaf
blocks of sizes \(p_a\) carries the same nuclear-polar slack rows.  Its
exact ambient parameter is
\[
                              s+\sum_a p_a,                \tag{6}
\]
while fixing all diagonal blocks to identities again gives the exact slice
parameter \(\sum_a\min\{s,p_a\}\).  This exposes a clean choice: the
nonsymmetric shared spectral cone is barrier-minimal for these natural
blocks, whereas the completion cone retains clique-tree sparse PSD
structure.

## 1. Exact barrier of a shared spectral cone

Put \(R_G=\sum_{a\in G}r_a\).  The block diagonal matrix
\(\operatorname{Diag}(X_a:a\in G)\) has spectral norm
\(\max_a\|X_a\|_{\rm op}\) and exactly \(R_G\) singular values, including
zeros.  The classical spectral-norm-cone barrier therefore restricts to
\[
 F_G(t,X)=
  -\sum_{a\in G}\log\det(t^2I_{r_a}-X_aX_a^T)
       +(R_G-1)\log t.                                    \tag{7}
\]
It is an \((R_G+1)\)-LHSCB.  Its homogeneity is explicit:
the determinant terms contribute \(2R_G\), and the positive
\(\log t\) correction returns \(R_G-1\).

For the lower bound, restrict every \(X_a\) to a rectangular diagonal
matrix with entries \(\xi_{a,1},\ldots,\xi_{a,r_a}\).  The section of (2)
is
\[
       \{(t,\xi):t\geq|\xi_{a,j}|\text{ for all }a,j\},
                                                               \tag{8}
\]
the \((R_G+1)\)-dimensional \(\ell_\infty\)-epigraph cone.  The sharp
polyhedral lower bound gives \(\nu\geq R_G+1\), proving (3).

The lower bound tensorizes against coupled barriers.  More explicitly,
the parameter-sharp Nesterov recession certificate for (8) uses only its
diagonal matrices, hence is also a certificate inside (2).  Placing these
certificates in separate direct summands gives value
\(\sum_G(R_G+1)\).  The sum of (7) attains that value, proving (4) for
arbitrary standard self-concordant barriers, not only separable LHSCBs.

### Exact complementary-face dimensions

The same cone has a closed face formula that quantifies the geometric cost
of sharing matrix rows.  Its dual is
\[
 \mathcal S_G^*=
 \left\{(\alpha,(Z_a)_{a\in G}):
             \alpha\geq\sum_{a\in G}\|Z_a\|_*\right\}.    \tag{8a}
\]
Take a nonzero dual boundary point, let
\(J=\{a:Z_a\ne0\}\), and put \(h_a=\operatorname{rank}Z_a\).
Equality in spectral/nuclear Hölder duality shows that its exposed
complementary face has dimension
\[
  1+\sum_{a\notin J}r_ac_a
     +\sum_{a\in J}(r_a-h_a)(c_a-h_a).                   \tag{8b}
\]
Indeed, in singular-vector coordinates for a supported block, equality
forces an \(h_a\times h_a\) corner of \(X_a/t\) to be \(-I\), forces both
cross rectangles to vanish, and leaves an arbitrary contraction of size
\((r_a-h_a)\times(c_a-h_a)\).  Unsupported blocks remain arbitrary
contractions, all with the same scale \(t\).

Consequently the maximum proper exposed complementary-face dimension is
\[
 f(\mathcal S_G)
   =1+\sum_{a\in G}r_ac_a
      -\min_{a\in G}(r_a+c_a-1).                         \tag{8c}
\]
The maximum uses one rank-one supported dual block whose
\(r_a+c_a-1\) loss is minimal.  For vector balls
\((r_a,c_a)=(1,s_a)\), this reduces to
\(1+\sum_as_a-\min_as_a\), exactly the heterogeneous
\(\mathcal H\)-cone formula.  Thus the spectral construction extends both
the barrier-sharing and face-sharing laws, rather than only embedding the
vector result.

## 2. Exact parameter on the matrix-ball slice

For \(X\in\mathbb R^{r\times c}\), \(r\leq c\), define
\[
                  \phi_{r,c}(X)=-\log\det(I_r-XX^T).      \tag{9}
\]
This is an \(r\)-self-concordant barrier for the open spectral-norm ball.
Ordinary self-concordance and boundary blow-up follow by restricting
\(-\log\det\left(\begin{smallmatrix}I_r&X\\X^T&I_c\end{smallmatrix}\right)\).
It remains to check the sharper gradient parameter.

Orthogonal invariance reduces to
\[
            X=\begin{pmatrix}\operatorname{Diag}(\sigma_1,\ldots,\sigma_r)&0
              \end{pmatrix},\qquad 0\leq\sigma_i<1.       \tag{10}
\]
The gradient is supported on the same rectangular diagonal subspace, and
that subspace is invariant under the Hessian.  On its \(i\)-th coordinate,
\[
 \phi_i'={2\sigma_i\over1-\sigma_i^2},
 \qquad
 \phi_i''={2(1+\sigma_i^2)\over(1-\sigma_i^2)^2}.         \tag{11}
\]
Consequently the squared local dual norm of the gradient is
\[
       \|\nabla\phi_{r,c}(X)\|_{X,*}^2
          =\sum_{i=1}^r{2\sigma_i^2\over1+\sigma_i^2}<r. \tag{12}
\]
Thus (9) has barrier parameter \(r\).  Conversely, its rectangular
diagonal section is the cube \((-1,1)^r\), so every self-concordant barrier
on the matrix ball has parameter at least \(r\).  Hence
\[
       \vartheta_{\rm opt}(\operatorname{int}\mathbb B_a)=\rho_a. \tag{13}
\]

Fixing \(t_G=1\) in (7) gives \(\sum_a\phi_{r_a,c_a}(X_a)\), with parameter
\(\sum_a\rho_a\).  A product of the diagonal cubes gives the matching lower
bound even for a custom coupled barrier on the full fixed-scale product,
proving (5).  The value, gradient, Hessian, Hessian-vector products, Dikin
metric, and reduced KKT/Newton equations are literally independent of the
row grouping.

## 3. Full-slack factorization

The polar of the spectral-norm ball is the nuclear-norm ball.  Its extreme
points are \(Z=uv^T\) with \(\|u\|=\|v\|=1\).  For a group \(G\), define
\[
       A_G(X)=(1,\operatorname{Diag}(X_a:a\in G))
                         \in\mathcal S_G.                 \tag{14}
\]
For the polar row indexed by \(a\in G\) and \(Z=uv^T\), let
\[
       B_G^a(Z)=(1,\operatorname{Diag}(0,\ldots,-Z,\ldots,0)).
                                                               \tag{15}
\]
The dual of the spectral-norm epigraph is the nuclear-norm epigraph, so
\(B_G^a(Z)\in\mathcal S_G^*\), and
\[
                   \langle A_G(X),B_G^a(Z)\rangle
                         =1-\langle X_a,Z\rangle_F.       \tag{16}
\]
Thus (2) gives globally polynomial selected factors for all labelled full
slack rows of a product of spectral-norm balls.  Vector Euclidean balls are
the special case \(\rho_a=1\), recovering the shared cone
\(\mathcal H\).

## 4. Chordal block-star alternative

Now take \(X_a\in\mathbb R^{s\times p_a}\).  Form a chordal graph with an
\(s\)-vertex hub clique and mutually nonadjacent leaf cliques of sizes
\(p_a\), each completely joined to the hub.  A partial matrix consists of
\[
       T\in\mathbb S^s,\quad
       U_a\in\mathbb R^{s\times p_a},\quad
       W_a\in\mathbb S^{p_a},                             \tag{17}
\]
and is PSD completable exactly when
\[
                    \begin{pmatrix}T&U_a\\U_a^T&W_a\end{pmatrix}
                                  \succeq0\quad\text{for every }a. \tag{18}
\]
The completion cone has
\[
 D_{\rm amb}={s(s+1)\over2}
    +\sum_a\left(sp_a+{p_a(p_a+1)\over2}\right)           \tag{19}
\]
specified coordinates and exact barrier parameter \(s+\sum_ap_a\).
The clique--separator barrier is
\[
 -\sum_a\log\det
       \begin{pmatrix}T&U_a\\U_a^T&W_a\end{pmatrix}
          +(k-1)\log\det T.                              \tag{20}
\]
The repeated hub receives exact overlap credit \((k-1)s\) relative to the
naive sum of clique barriers.

For completeness, exactness follows without assuming that a coupled barrier
separates over cliques.  Restrict the partial matrix to be diagonal.  The
resulting section is the positive orthant on the \(s+\sum_a p_a\) graph
vertices.  Its sharp orthant lower bound is \(s+\sum_a p_a\), while (20)
attains the same value.  Thus the claim is for arbitrary self-concordant
barriers on the completion cone, not only for the displayed
clique--separator barrier.

Fix \(T=I_s\), \(W_a=I_{p_a}\), and \(U_a=X_a\).  Then (18) is exactly
\(\|X_a\|_{\rm op}\leq1\), and (20) restricts to
\[
                  -\sum_a\log\det(I-X_aX_a^T),           \tag{21}
\]
where the smaller of \(X_aX_a^T\) and \(X_a^TX_a\) may be used.  Equation
(13) makes the exact slice parameter \(\sum_a\min\{s,p_a\}\).

The full slack factors are again partial Gram matrices.  For
\(Z=uv^T\), place \((-u,v)\) on the hub and leaf \(a\); one half of its
rank-one outer product is a sparse PSD dual factor, and its pairing with
\(\left(\begin{smallmatrix}I&X_a\\X_a^T&I\end{smallmatrix}\right)\)
is \(1-\langle X_a,Z\rangle_F\).  Thus the block-star construction carries
the same rows as (14)--(16).

## 5. Exact reduced-oracle equivalence

Put every shared spectral scale at one.  In the chordal formulation put
every hub block and leaf diagonal block at the corresponding identity.
After the harmless transpose used to orient each matrix with
\(\rho_a\) rows, both formulations have the same retained coordinates
\((X_a)_a\) and exactly the same barrier
\[
               \Phi(X)=-\sum_a\log\det(I-X_aX_a^T).      \tag{22}
\]
This is equality of functions, not merely equality of parameters.
Consequently their value, gradient, Hessian, Hessian-vector product, local
dual norm, and Dikin ellipsoid oracles are identical under a fixed
coordinate permutation.  Concretely, for one oriented block, with
\(M=I-XX^T\),
\[
 \nabla\phi(X)=2M^{-1}X,\qquad
 \nabla^2\phi(X)[H]
 =2M^{-1}H+
  2M^{-1}(HX^T+XH^T)M^{-1}X.
\]
Both formulations therefore use the same numerical primitive, not merely
two isospectral Hessians.

More generally, add the same affine equations
\(\mathcal A\operatorname{vec}X=b\) and objective \(c^T\operatorname{vec}X\)
to either fixed-scale formulation.  At every common interior point the
reduced Newton/KKT matrix and right-hand side are literally
\[
 \begin{pmatrix}
       \nabla^2\Phi(X)&\mathcal A^T\\
       \mathcal A&0
 \end{pmatrix},
 \qquad
 \begin{pmatrix}
       -\nabla\Phi(X)-\tau c-\mathcal A^Ty\\
       b-\mathcal A\operatorname{vec}X
 \end{pmatrix}.                                          \tag{23}
\]
Thus the central paths, reduced Newton directions, reduced Hessian
condition numbers, and exact normalized reduced Newton states coincide.
An exact classical or coherent oracle for any displayed reduced object in
one formulation implements the corresponding oracle in the other using
only a public index permutation and no source-data query.  The statement
also holds between any two shared-scale groupings, since (22) contains no
group label.

This equivalence is deliberately reduced.  It does not identify the
unfixed ambient primal--dual KKT systems: scale variables in (2) and
hub/leaf/completion variables in (17) are different, as are their conic
dual slacks.  It also does not make construction of a reduced oracle from a
given ambient input free.  Any computational separation between the
formulations must enter through that ambient-to-reduced compilation,
sparsity/materialization, preconditioning, or output contract, not through
the fixed-slice barrier metric itself.

### Complex Hermitian version

All statements above extend to complex matrices with the real Frobenius
pairing \(\operatorname{Re}\operatorname{tr}(X^*Z)\).  Replace transposes
by adjoints.  Singular-value counts, the exact parameters
\(R+g\) and \(R\), and the reduced-oracle equivalence are unchanged; the
rank-one slack is \(1-\operatorname{Re}(u^*X_av)\).  In the face formula
(8b), every free matrix dimension is doubled, so
\[
 f_{\mathbb C}(\mathcal S_G)
   =1+2\sum_a r_ac_a-2\min_a(r_a+c_a-1).
\]
The real ambient
dimension of one shared spectral cone is
\[
                       1+2\sum_a r_ac_a,
\]
while the Hermitian block-star completion cone has real dimension
\[
                       s^2+\sum_a(2sp_a+p_a^2).
\]
Its exact ambient parameter is still the graph order
\(s+\sum_ap_a\).  Thus complexification doubles off-diagonal storage but
does not change the intrinsic rank/grouping barrier ledger.

## 6. A grouping-independent bounded-move lower bound

For each oriented block choose the partial isometry
\[
                  C_a=\begin{pmatrix}I_{r_a}&0\end{pmatrix},
\]
and maximize
\[
                         \ell(X)=\sum_a\langle C_a,X_a\rangle_F. \tag{24}
\]
Its optimum over the product of spectral-norm balls is
\(R=\sum_ar_a\).  Let
\[
                  Q(X)=\prod_a\det(I-X_aX_a^T),
                  \qquad \Phi=-\log Q.                   \tag{25}
\]
If an interior point satisfies \(R-\ell(X)\leq\epsilon\), von Neumann's
trace inequality gives
\[
 \epsilon\geq\sum_{a,i}(1-\sigma_i(X_a)).
\]
Since \(1+\sigma_i\leq2\), AM--GM implies
\[
                         Q(X)^{1/R}\leq {2\epsilon\over R}. \tag{26}
\]

At the analytic center \(X=0\), \(Q=1\), and \(\Phi\) has exact parameter
\(R\).  With the convention
\(X(\tau)=\arg\max_X\{\tau\ell(X)-\Phi(X)\}\), the exact central path is
also rank- and grouping-transparent:
\[
 X_a(\tau)=r(\tau)C_a,\qquad
 r(\tau)={\tau\over\sqrt{1+\tau^2}+1},\qquad
 R-\ell(X(\tau))=R(1-r(\tau)).
\]
The standard barrier-height/distance inequality therefore puts
every \(\epsilon\)-accurate point at Dikin-geodesic distance at least
\[
                \left[\sqrt R\log{R\over2\epsilon}\right]_+
\]
from the center.  Suppose the feasible iterate starts at \(X=0\), each
counted outer round changes it through at most \(m\) successive chords in
the fixed slice, and every chord has starting-point \(\Phi\)-local norm at
most a fixed \(\eta<1\).  Since one such chord has metric length at most
\(\log(1/(1-\eta))\), the number of rounds obeys
\[
 T\geq
 {[\sqrt R\log(R/(2\epsilon))]_+
       \over m\log(1/(1-\eta))}.                          \tag{27}
\]

By Section 5, (27) is identical for every shared-spectral grouping and for
the fixed-identity chordal block-star formulation.  It permits arbitrary
classical or quantum computation to choose the bounded moves, provided
every change of the feasible iterate is included in those moves.  It is
not a query or runtime lower bound and does not cover algorithms that take
unbounded local-norm moves or leave the fixed slice.  Its role is to show
that factor-count collapse and chordal sparsification do not shorten the
fixed-slice determinant geometry even for matrix-valued balls.  The
standard short-step upper bound has the matching
\(O(\sqrt R\log(R/\epsilon))\) dependence, up to the usual
fixed neighborhood and accuracy conventions.

## 7. Resource comparison and scope

For \(g\) shared spectral-cone groups, with total matrix rank
\(R=\sum_a\rho_a\), the exact ambient and slice parameters are
\[
                         (R+g,\ R).                       \tag{28}
\]
For equal row size \(s\) and a partition of the block leaves among \(g\)
chordal stars, the corresponding values are
\[
                  \left(gs+\sum_ap_a,\ \sum_a\min\{s,p_a\}\right). \tag{29}
\]
The nonsymmetric cone wins the parameter comparison.  The chordal model
instead exposes PSD clique-tree structure and avoids materializing every
cross-leaf block of a dense PSD matrix.  Neither ledger includes the cost
of derivative evaluation, block encoding, a Newton solve, conditioning, or
solution readout.

The spectral-norm cone and its barrier are classical: see
Nesterov--Nemirovskii, Proposition 5.4.6, and Coey, Kapelevich, and Vielma,
[*Performance Enhancements for a Generic Conic Interior Point
Algorithm*](https://optimization-online.org/wp-content/uploads/2020/05/7776.pdf),
Section 4.7.  Chordal completion and the max-determinant barrier are also
classical, as documented in
[the companion completion-cone note](2026-09-04-chordal-completion-ball-packing.md).

A targeted local and web search found no source packaging the block-diagonal
shared-scale construction, its exact product-coupled law (4), the sharp
matrix-ball slice calculation (9)--(13), the full slack factorization
(14)--(16), the chordal block-star comparison (17)--(21), and the exact
reduced-oracle equivalence, bounded-move theorem, and resource ledger
(22)--(29).  These are
short consequences of classical ingredients, so the plausible novelty is
their synthesis and exact sparse-QIPM resource frontier, not the primitive
barriers.  Priority remains subject to specialist review.

## Audit targets

1. Verify that block diagonalization gives exactly (7), including the
   parameter and the Nesterov-certificate tensorization.
2. Check Hessian invariance and the local gradient norm (12), and whether
   affine restriction supplies ordinary self-concordance of (9).
3. Check the nuclear-polar factorization and every trace normalization.
4. Recompute the block-star dimension, separator multiplicity, exact
   ambient parameter, fixed-slice barrier, and rank-one dual factor.
5. Ensure all comparisons distinguish classical barriers from the candidate
   new synthesis and make no runtime or query claim.

## Independent audit record

An independent hostile audit checked all five targets.  In particular:

- the block-diagonal embedding has \(R_G\) rows, and scaling (7) changes it
  by exactly \(-(R_G+1)\log\lambda\);
- the diagonal subspace is Hessian-invariant at an SVD representative, so
  (11) gives the full, rather than merely restricted, local dual norm in
  (12);
- the dual of (2) is
  \(\{(u,(Z_a)):u\geq\sum_a\|Z_a\|_*\}\), which makes (15)--(16) exact
  with no missing factor of two;
- the block-star has \(s+\sum_a p_a\) graph vertices, hub separator
  multiplicity \(k-1\), and the half rank-one dual factor pairs to
  \(1-\langle X_a,uv^T\rangle_F\); and
- the arbitrary-coupled lower bounds use genuine diagonal cube or orthant
  sections (and the direct-sum recession certificate for (4)), so no
  separability assumption is hidden.

A follow-up audit checked the reduced-oracle statement.  Sylvester's
determinant identity and the public transpose convention make (22) exactly
the same function in the shared spectral and chordal formulations.  With
common transformed affine data, (23), the central paths, condition numbers,
and normalized reduced Newton states coincide, and coherent oracle transfer
is a public basis permutation.  This does not identify either ambient KKT
system or the cost of compiling its reduced oracle.

The same audit checked the complex Hermitian corollary: the real storage
dimensions change as displayed, while the singular-value ranks, graph
order, barrier parameters, real-trace slack normalization, and reduced
oracles remain unchanged.

A separate hostile audit checked the face formulas (8a)--(8c).  Equality
in spectral/nuclear duality fixes the supported singular-vector corner and
annihilates both cross rectangles, leaving exactly the displayed free
complement contraction.  It also checked the maximization over support
ranks and blocks, all rectangular and rank-one edge cases, and the factor
of two in the complex real face dimension.

The bounded-move theorem in Section 6 was independently checked as well.
Von Neumann's inequality gives
\(R-\ell(X)\geq\sum_{a,i}(1-\sigma_i(X_a))\); applying
\(1-\sigma_i^2\leq2(1-\sigma_i)\) and AM--GM yields exactly (26).
Barrier height divided by \(\sqrt R\) gives the displayed distance, the
stationarity equation \(2r/(1-r^2)=\tau\) gives the stated central path,
and each starting-norm-\(\eta\) chord has length at most
\(-\log(1-\eta)\).  The transfer to shared and chordal formulations is
valid only on their fixed-scale or fixed-identity slices, where the
barrier and Hessian are literally the same.

No runtime, conditioning, or quantum-query conclusion follows from the
parameter identities alone; the exact oracle statement applies only under
the matched reduced interface just specified.
