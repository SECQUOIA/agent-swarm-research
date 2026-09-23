# Exact barriers and product-ball packing in PSD-completion cones

Status: Proved; targeted literature screen and independent hostile audit completed  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Summary

Let \(G=(V,E)\) be a graph on \(n\) vertices, with every diagonal specified,
and let \(\mathcal C_G\) be the cone of partial symmetric matrices on \(E\)
that admit a positive-semidefinite completion.  Then

\[
                         \nu_{\rm opt}(\mathcal C_G)=n.   \tag{1}
\]

The lower bound applies to every self-concordant barrier, including one
that couples several completion-cone factors.  The upper bound is the
Legendre-dual sparse-matrix barrier, equivalently the negative log
determinant of the maximum-determinant positive-definite completion.  For a
chordal graph it has the classical clique--separator formula and can be
evaluated by sparse clique-tree recursions.

A block-star specialization gives a useful product-ball formulation.  One
PSD-completion cone with an \(s\)-vertex hub and \(q\) scalar leaves carries
all \(q\) full slack rows of \((B_2^s)^q\).  It has

\[
 \begin{aligned}
 L&=1,\\
 D_{\rm amb}&={s(s+1)\over2}+q(s+1),\\
 \nu_{\rm ambient}&=s+q.                                 \tag{2}
 \end{aligned}
\]

Compared with a dense order-\((s+q)\) PSD factor, this removes all
\(q(q-1)/2\) leaf--leaf coordinates without changing the exact barrier
parameter.  Fixing the hub to \(I_s\) and every leaf diagonal to one
recovers exactly the ordinary product-ball barrier with parameter \(q\),
so the reduced central path, Hessian, Dikin geometry, and Newton equations
are unchanged.  This is a sparse representation theorem, not a new
maximum-determinant barrier.

## 1. The completion-cone barrier has exact parameter \(n\)

Let \(\mathbb S_G^n\) be the linear space of symmetric matrices supported on
the diagonals and edges of \(G\), with the trace inner product, and put

\[
 \mathcal K_G=\mathbb S_+^n\cap\mathbb S_G^n,
 \qquad
 \mathcal C_G=\mathcal K_G^*.                            \tag{3}
\]

The dual is naturally identified with partial matrices that have a PSD
completion.  The restriction

\[
                         X\longmapsto-\log\det X          \tag{4}
\]

is an \(n\)-LHSCB on \(\mathcal K_G\).  Legendre duality gives an
\(n\)-LHSCB \(F_G\) on \(\mathcal C_G\).  If \(Z(S)\) is the unique
maximum-determinant positive-definite completion of
\(S\in\operatorname{int}\mathcal C_G\), then, up to an additive constant,

\[
                         F_G(S)=-\log\det Z(S).            \tag{5}
\]

For completeness, the diagonal section obtained by setting every specified
off-diagonal entry to zero is exactly \(\mathbb R_+^n\).  Restricting any
self-concordant barrier on \(\mathcal C_G\) to this section and applying the
sharp orthant lower bound gives \(\nu\geq n\).  Together with (4)--(5), this
proves (1), in fact over the larger class of arbitrary standard
self-concordant barriers.

The same argument is exactly additive over products.  If \(G_j\) has
\(n_j\) vertices, the product has a diagonal section
\(\mathbb R_+^{\sum_j n_j}\), while the sum of (5) has parameter
\(\sum_jn_j\).  Hence

\[
        \nu_{\rm opt}\!\left(\prod_j\mathcal C_{G_j}\right)
                          =\sum_j n_j                     \tag{6}
\]

even when the competing barrier couples all factors.

When \(G\) is chordal, choose a clique tree with maximal cliques
\(\mathcal Q\) and edge separators \(\mathcal S\), counted with clique-tree
multiplicity.  Classical maximum-determinant completion gives

\[
 F_G(S)=-\sum_{C\in\mathcal Q}\log\det S_C
          +\sum_{R\in\mathcal S}\log\det S_R,            \tag{7}
\]

and the running-intersection identity
\(\sum_C|C|-\sum_R|R|=n\) makes its logarithmic-homogeneity degree explicit.
Thus a repeated separator receives an exact overlap credit: the naive sum
of clique-PSD barriers has parameter \(\sum_C|C|\), whereas the completion
barrier has parameter
\[
                    \sum_C|C|-\sum_R|R|=n.
\]
This is the precise chordal sharing law; clique count by itself overcharges
the intrinsic cone geometry.
The positive separator terms in (7) are not a license to subtract arbitrary
barriers; self-concordance follows from (4)--(5).

## 2. A star-completion factorization of all product-ball rows

Let the graph have a hub clique \(H\) of size \(s\) and leaves
\(a=1,\ldots,q\), each adjacent to every hub vertex and to no other leaf.
Write a partial matrix as

\[
       S=(T,(u_a,w_a)_{a=1}^q),\qquad
       T\in\mathbb S^s,\ u_a\in\mathbb R^s,\ w_a\in\mathbb R. \tag{8}
\]

Its maximal clique matrices are

\[
              S_a=\begin{pmatrix}T&u_a\\u_a^T&w_a\end{pmatrix}.
                                                               \tag{9}
\]

The graph is chordal, and \(S\in\mathcal C_G\) exactly when every \(S_a\)
is PSD.  Its specified-coordinate dimension is

\[
             {s(s+1)\over2}+qs+q.                         \tag{10}
\]

For \(x=(x_1,\ldots,x_q)\in(S^{s-1})^q\), define the primal factor

\[
                 A(x)=(I_s,(x_a,1)_{a=1}^q).             \tag{11}
\]

It is PSD completable: a completion is the Gram matrix of the \(s\)
standard basis vectors and the \(q\) vectors \(x_a\).  For
\(z\in S^{s-1}\), let \(b_a(z)\in\mathbb R^{s+q}\) equal \(-z\) on the hub,
one at leaf \(a\), and zero at every other leaf, and define the sparse dual
factor

\[
                         B^a(z)={1\over2}b_a(z)b_a(z)^T.   \tag{12}
\]

It lies in \(\mathcal K_G\), because its support is the clique
\(H\cup\{a\}\).  The trace pairing uses only specified entries and gives

\[
 \langle A(x),B^a(z)\rangle
     ={1\over2}\begin{pmatrix}-z\\1\end{pmatrix}^{\!T}
       \begin{pmatrix}I_s&x_a\\x_a^T&1\end{pmatrix}
       \begin{pmatrix}-z\\1\end{pmatrix}
     =1-\langle x_a,z\rangle.                             \tag{13}
\]

Thus one chordal completion cone carries all \(q\) labelled full slack
rows with polynomial factor maps.

## 3. Exact ambient and fixed-slice barrier ledgers

All \(q\) maximal cliques in the star meet in \(H\).  Formula (7) becomes

\[
 F_{s,q}(T,u,w)
   =-\sum_{a=1}^q\log\det
       \begin{pmatrix}T&u_a\\u_a^T&w_a\end{pmatrix}
       +(q-1)\log\det T.                                 \tag{14}
\]

Equivalently, with
\(\delta_a=w_a-u_a^TT^{-1}u_a\),

\[
                 F_{s,q}=-\log\det T-\sum_a\log\delta_a. \tag{15}
\]

The naive product of the \(q\) order-\((s+1)\) clique barriers has parameter
\(q(s+1)\).  The \(q-1\) repeated hub separators in (14) give exact credit
\((q-1)s\), leaving \(q+s\).  Treating \(\mathcal C_G\) as one primitive
cone therefore collapses the formal factor count, but its sparse
implementation still traverses the \(q\) cliques; the gain is the overlap
credit, not free membership evaluation.

Equations (1) and (10) prove the ambient ledger (2).  For a partition of
\(k\) source rows into \(g\) star blocks of sizes \(q_1,\ldots,q_g\), the
exact totals are

\[
 \begin{aligned}
 D_{\rm amb}&=k(s+1)+g{s(s+1)\over2},\\
 \nu_{\rm ambient}&=k+gs.                                \tag{16}
 \end{aligned}
\]

The second equality holds against arbitrary barriers coupled across the
\(g\) completion-cone factors, by (6).  It shows that sharing one PSD hub
across more rows lowers both factor count and the exact ambient parameter:
each additional group costs \(s\) barrier units.  In particular, one star
beats the \(2k\) parameter of \(k\) separate Lorentz factors exactly when
\(k>s\), although the nonhomogeneous shared-scale cone
\(\mathcal H_{k,s}\) remains better at \(k+1\).

On the affine slice

\[
                         T=I_s,\qquad w_a=1,               \tag{17}
\]

equation (14) restricts exactly to

\[
                  -\sum_{a=1}^q\log(1-\|u_a\|_2^2).      \tag{18}
\]

Its optimal affine barrier parameter is \(q\), by the scalar-cube section.
The value, gradient, Hessian, Hessian-vector products, Dikin metric, and
reduced KKT/Newton equations from (18) are independent of how the rows were
grouped.  Thus the ambient improvement in (16) is a representation and
barrier-ledger improvement, not a reduction in the fixed-slice Newton
geometry.

The star barrier is also explicitly sparse.  Factoring \(T\) once and
solving against the \(q\) leaf vectors evaluates (15) in
\(O(s^3+qs^2)\) dense arithmetic and stores
\(O(s^2+qs)\) scalars.  This should be compared with
\(O((s+q)^3)\) arithmetic and \(\Theta((s+q)^2)\) storage for treating the
same partial Gram construction as one dense PSD matrix.  These are barrier-
evaluation counts, not an end-to-end Newton-solve or quantum-query bound.

### Hermitian extension

The theorem is unchanged over complex Hermitian matrices.  Let
\(\beta=1\) in the real symmetric case and \(\beta=2\) in the complex
Hermitian case.  The star completion cone has real dimension

\[
 D_\beta(s,q)
   =s+\beta{s(s-1)\over2}+\beta sq+q,                    \tag{19}
\]

exact barrier parameter \(s+q\), and saves exactly
\(\beta q(q-1)/2\) real leaf--leaf coordinates relative to a dense
Hermitian PSD factor of order \(s+q\).  For complex unit vectors, use the
real trace pairing and replace transposes by adjoints in (8)--(15).  Then

\[
 {1\over2}
 \begin{pmatrix}-z\\1\end{pmatrix}^{\!*}
 \begin{pmatrix}I_s&x_a\\x_a^*&1\end{pmatrix}
 \begin{pmatrix}-z\\1\end{pmatrix}
       =1-\operatorname{Re}(z^*x_a),                     \tag{20}
\]

the natural real slack of the complex Euclidean ball.  The diagonal
orthant section and clique--separator proof remain literal, so products
again have exact parameter equal to their total number of graph vertices.
This extension changes real storage dimensions but not the barrier ledger.

## 4. What is and is not new

Ellipsoidal leaves give no new theorem: independent invertible coordinate
changes reduce them to (11)--(18).  For general SOC-representable norms,
the scalar-diameter section still gives useful lower certificates, but an
exact upper parameter depends on the chosen representation and does not
follow from SOC representability alone.

The completion theorem and barriers are classical.  Grone, Johnson, Sá,
and Wolkowicz characterize chordal positive-definite completion in
[*Positive Definite Completions of Partial Hermitian
Matrices*](https://doi.org/10.1016/0024-3795(84)90207-6).  Barrett, Johnson,
and Lundquist give the clique--separator determinant formula in
[*Determinantal Formulae for Matrix Completions Associated with Chordal
Graphs*](https://doi.org/10.1016/0024-3795(89)90706-4).  Andersen, Dahl, and
Vandenberghe develop the sparse log-determinant barrier, its conjugate on
the completion cone, and sparse derivative algorithms in
[*Logarithmic Barriers for Sparse Matrix
Cones*](https://arxiv.org/abs/1203.2742).

Accordingly, no novelty is claimed for (1), (5), or (7) as barrier
constructions.  A targeted local and web search found no source stating the
specific full product-ball slack factorization (11)--(13) together with the
exact coupled ledgers (16), the dense-PSD coordinate saving, and the exact
fixed-slice invariance (18).  That synthesis is the plausible contribution;
priority remains subject to specialist review.

## Independent hostile audit

The audit checked the dual identification for arbitrary graphs, including
closedness of the completion cone when all diagonals are specified.  It
rederived the Legendre sign: stationarity identifies the inverse of the
sparse primal optimizer with the maximum-determinant completion, giving
\(-\log\det Z(S)\) up to a constant.  The diagonal orthant section proves
the exact lower bound for arbitrary, possibly coupled self-concordant
barriers and gives (6).

For the star construction, the audit verified chordality, the specified
dimension, and the factor \(1/2\) in the sparse trace pairing.  Each of the
\(q-1\) clique-tree separators is the hub, yielding (14)--(16).  It also
checked the exact fixed-slice parameter \(q\), grouping-independent reduced
geometry, and the limited evaluation scope of
\(O(s^3+qs^2)\): this is a dense-arithmetic barrier-value/factorization
count, not a full Newton solve or end-to-end quantum bound.  No correction
was found.
