# Latent treewidth of Lorentz Newton systems

Status: Proved; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the algebra and exact-arithmetic theorem; moderate on the
finite-precision and novelty claims

## Main point

A high-dimensional Lorentz block makes its barrier Hessian generically dense,
but this density has only two latent directions.  Replacing each dense block by
two scalar hub variables gives an equivalent sparse Newton system.  Treewidth
should therefore be measured on this **rank-expanded incidence graph**, not on
the graph of the materialized Hessian or normal equations.

This observation gives a new SOCP-specific extension of the bounded-treewidth
QIPM replacement principle.  If the rank-expanded graph has width \(\tau\), an
exact Newton system can be solved in

\[
 O\bigl((M+p+k)(\tau+1)^2\bigr)                           \tag{1}
\]

field operations from a supplied compact tree decomposition (or after the
one-time compaction cost stated below).  With the standard small
dual regularization, the expanded matrix is symmetric quasidefinite and a
width-\(\tau\) pivot-free \(LDL^T\) factorization costs

\[
 O\bigl((M+p+k)\tau^2\bigr)                               \tag{2}
\]

arithmetic and \(O((M+p+k)\tau)\) storage.  These bounds are independent of
the maximum Lorentz-block dimension.  They apply even when every materialized
barrier Hessian has scalar treewidth equal to that dimension minus one.

Consequently a hybrid QIPM that materializes every classical Newton direction
has no polynomial dimension advantage on constant-rank-expanded-treewidth
SOCP families under matched entry access.  In particular, splitting a large
Lorentz cone into a tree of three-dimensional cones can raise the generic
short-step count by the square root of the block dimension without improving
the linear-time structured Newton solve.  This cannot be evaded by coupling
the small-cone lifts across blocks: every joint exact lift of
\(Q_{s+1}^k\) by \(\prod_jQ_{m_j}\) obeys the additive curvature budget
\(\sum_j(m_j-2)\geq k(s-1)\).  Thus a pure-\(Q_3\) lift needs at least
\(k(s-1)\) factors, matching separate binary norm trees.

The low-rank Hessian identity and augmented-sparsity technique are classical.
The apparently new contribution is the exact rank-expanded-treewidth theorem,
its trajectory-level QIPM consequence, and the direct-versus-split cone
complexity comparison.  A literature search cannot establish priority.

## Model

Consider the equality-form SOCP

\[
 \min c^Tx,\qquad Ax=b,\qquad
 x=(x_1,\ldots,x_k)\in\prod_{i=1}^k Q_{m_i},              \tag{3}
\]

where \(A\in\mathbb R^{p\times M}\),
\(M=\sum_i m_i\), and

\[
 Q_m=\{(t,z)\in\mathbb R\times\mathbb R^{m-1}:
             t\geq\|z\|_2\}.
\]

At an interior point write \(x_i=(t_i,z_i)\),
\(r_i=\|z_i\|_2\), and \(q_i=t_i^2-r_i^2>0\).  Use the
standard barrier

\[
 F(x)=-\sum_{i=1}^k\log q_i,\qquad H=\nabla^2F(x).         \tag{4}
\]

The primal equality-form Newton matrix is

\[
 K_0=\begin{bmatrix}H&A^T\\A&0\end{bmatrix}.             \tag{5}
\]

The same construction applies to any primal, dual, or homogeneous-self-dual
Newton formulation in which a Lorentz barrier Hessian occurs as a diagonal
block: all other scalar variables and nonzeros are simply retained in the
expanded graph.

## Exact two-hub decomposition

### Lemma 1

For one noncentered block \(x=(t,z)\), put \(r=\|z\|>0\),
\(e=z/r\), and

\[
 D={2\over q}I,
 \quad
 a={\sqrt{2r(t+r)}\over q}\binom{1}{-e},
 \quad
 v={\sqrt{2r(t-r)}\over q}\binom{1}{e}.                  \tag{6}
\]

Then

\[
 \boxed{\nabla^2[-\log(t^2-\|z\|^2)]=D+aa^T-vv^T},       \tag{7}
\]

and \(D-vv^T\succ0\).  At \(z=0\), take \(a=v=0\).

#### Proof

Let \(J=\operatorname{diag}(1,-I)\) and \(u=Jx=(t,-z)\).
Direct differentiation gives

\[
 H_x=-{2J\over q}+{4uu^T\over q^2}.                      \tag{8}
\]

Subtracting \(D=2I/q\), the result vanishes on the
subspace orthogonal to \(e_0=(1,0)\) and \((0,e)\).  In
that two-dimensional basis it is

\[
 {4\over q^2}
 \begin{bmatrix}r^2&-tr\\-tr&r^2\end{bmatrix}.          \tag{9}
\]

The normalized eigenvectors \((1,-1)/\sqrt2\) and
\((1,1)/\sqrt2\) have eigenvalues
\(4r(t+r)/q^2\) and \(-4r(t-r)/q^2\), respectively.  This
is exactly (7).  Relative to \(D\), the only negative update has
squared norm

\[
 v^TD^{-1}v={2r(t-r)\over q}={2r\over t+r}<1,             \tag{10}
\]

so the rank-one downdate criterion gives \(D-vv^T\succ0\).
At \(r=0\), (8) equals \(2I/q\).  \(\square\)

There is also a simpler one-hub identity that avoids block norms and square
roots.  Namely, (8) itself says

\[
 H_x=D_x+w_xw_x^T,
 \qquad D_x=-{2J\over q},\qquad w_x={2Jx\over q}.          \tag{10a}
\]

Here \(D_x\) is diagonal but indefinite.  This form is enough for exact
low-treewidth elimination.  The two-hub form (7) is needed only to expose a
quasidefinite regularization.

For all blocks, let \(D\) be block diagonal and let \(U,V\) have one
embedded column \(a_i,v_i\) per noncentered cone.  Zero columns may be
retained to keep a fixed symbolic graph.  Then

\[
 H=D+UU^T-VV^T,
 \qquad D-VV^T\succ0.                                    \tag{11}
\]

The augmented Hessian

\[
 H_{\rm aug}=
 \begin{bmatrix}
 D&V&U\\ V^T&I&0\\ U^T&0&-I
 \end{bmatrix}                                           \tag{12}
\]

has Schur complement \(H\) after the two hub groups are eliminated.  Its
positive principal block \(\left[\begin{smallmatrix}D&V\\V^T&I\end{smallmatrix}\right]\)
is positive definite by (11), while its remaining diagonal block is \(-I\).
Thus it is symmetric quasidefinite.

### Two hubs are generically necessary for a positive-diagonal star expansion

The two-hub count is not an artifact of (6).  Let \(m\geq3\), and suppose
every coordinate of \(Jx\) is nonzero.  There is no representation

\[
 H_x=D_0+\sigma ww^T,
 \qquad D_0\succ0\ \hbox{diagonal},\qquad \sigma\in\{+1,-1\}. \tag{12a}
\]

Indeed, put \(y=Jx\) and \(c=4/q^2\).  The off-diagonal entries of (8) are
\(c y_i y_j\).  If (12a) held and \(\alpha_i=w_i/y_i\), then

\[
 \sigma\alpha_i\alpha_j=c\qquad(i\ne j).                 \tag{12b}
\]

Using any three distinct indices shows that all \(\alpha_i\)'s are equal.
It follows that \(\sigma=+1\) and \(ww^T=cyy^T\).  Equation (8) then forces
\(D_0=-2J/q\), whose time entry is negative, a contradiction.  Thus a
positive diagonal base plus signed rank-one hubs needs at least two hubs on a
generic Lorentz block.  Formula (7) attains this minimum, with one hub of each
sign and the stronger property \(D-vv^T\succ0\).

This is only an optimality statement for diagonal-base star expansions.  A
more general sparse base or a nonsymmetric formulation can use a different
auxiliary representation.

## Rank-expanded incidence graph

Create vertices of four types:

1. one vertex for each scalar coordinate of \(x\);
2. one vertex for each equality row of \(A\);
3. two hub vertices \(u_i,v_i\) for every Lorentz block; and
4. any other scalar variables in the chosen KKT formulation.

Join a coordinate vertex to an equality-row vertex exactly when the
corresponding entry of \(A\) is structurally nonzero.  Join every coordinate
of block \(i\) to both hubs \(u_i,v_i\).  Retain all other structural KKT
edges.  Call the resulting graph \(G_{\rm L}\), and write

\[
 \tau_{\rm L}=\operatorname{tw}(G_{\rm L}).               \tag{13}
\]

This graph is independent of the current numerical iterate.  It is generally
much smaller in width than the graph of \(K_0\): when all coordinates of
\(z_i\) are nonzero, (8) makes the scalar Hessian graph on block \(i\) a
clique, whereas (12) replaces that clique by a \(K_{2,m_i}\)-type graph of
treewidth two.

## Treewidth theorem

### Theorem 2 (exact arithmetic)

Assume \(A\) has full row rank, so \(K_0\) is nonsingular.  Given the current
iterate and a tree decomposition of \(G_{\rm L}\) of width \(\tau_{\rm L}\),
put \(\bar\tau_{\rm L}=\tau_{\rm L}+1\).  After the standard compaction of
the supplied decomposition to linear size, one can solve (5) exactly using

\[
 O\bigl((M+p+k)\bar\tau_{\rm L}^2\bigr)                   \tag{14}
\]

field operations after \(O(M+\operatorname{nnz}A)\) work to form the
expanded coefficients.  The bound has no dependence on
\(\max_i m_i\) outside the linear input-size term.

#### Proof

For each cone use (10a), put the \(D_{x_i}\)'s on the diagonal of
\(D_x\), put the embedded \(w_i\)'s into \(W\), and form

\[
 \widetilde K_0=
 \begin{bmatrix}
 D_x&W&A^T\\
 W^T&-I&0\\
 A&0&0
 \end{bmatrix}.                                          \tag{15}
\]

For a right-hand side \((g_x,g_y)\) of (5), give (15) the right-hand side
\((g_x,0,g_y)\).  Eliminating the \(-I\) hub block gives (5), so
nonsingularity of one matrix is equivalent to nonsingularity of the other and
their solutions map by back substitution.  In particular, full row rank of
\(A\) and \(H\succ0\) make both matrices nonsingular, so the expanded system
is consistent for every right-hand side.  The scalar graph of (15) is a
subgraph of \(G_{\rm L}\), and
its order is at most \(M+p+k\).  Its entries use only field operations on the
current iterate; this exact branch does not need to extract \(r_i\) or any
square root.

The 2025 sharp low-treewidth Gaussian-elimination theorem solves a consistent
linear system whose row--column bipartite graph is supplied with a compact
width-\(\tau\) tree decomposition in \(O(n(\tau+1)^2)\) field operations,
without a no-cancellation assumption.  A
width-\(\tau_{\rm L}\) decomposition of the usual graph of a square symmetric
matrix gives a width-at-most-\(2\tau_{\rm L}+1\) bipartite decomposition by
replacing every vertex in every bag by its row and column copies.  Indeed, an
off-diagonal matrix nonzero is covered by a bag containing its two original
vertices, a diagonal nonzero is covered because both copies of that vertex
occur together, and each copy inherits the original connected bag subtree.
The number of bags is unchanged.  Thus, after nice-decomposition compaction,
the doubled decomposition has \(O(M+p+k)\) bags and satisfies the compactness
hypothesis of the Gaussian-elimination theorem.  Its width parameter plus one
is at most \(2\bar\tau_{\rm L}\); since (15) is square of order at most
\(M+p+k\), the theorem's \(O(k^2(m+n))\) bound is (14), with constants
absorbed.  Every coefficient in (10a) can be formed in linear work, giving the
coefficient-formation claim.  \(\square\)

If the original decomposition has \(|\mathcal T|\) bags, the usual nice-tree
compaction adds \(O(\tau_{\rm L}(|\mathcal T|+M+p+k))\) preprocessing.  The
resulting width-squared solve does not need an a priori zero-free scalar pivot
order: the cited algorithm permits arbitrary pivots and handles exact
algebraic cancellations.  This removes regularization and a no-cancellation
hypothesis only for the exact-arithmetic, one-right-hand-side solve.  It is not
a numerical-stability claim and does not supply the reusable symmetric factor
provided by the regularized formulation below.

### Theorem 3 (quasidefinite regularization)

For \(\rho>0\), replace the lower-right zero block of (5) by \(-\rho I\).
The corresponding expanded matrix is

\[
 \widehat K_\rho=
 \begin{bmatrix}
 D&V&U&A^T\\
 V^T&I&0&0\\
 U^T&0&-I&0\\
 A&0&0&-\rho I
 \end{bmatrix}.                                          \tag{16}
\]

It is symmetric quasidefinite.  A chordal elimination order obtained from the
supplied width-\(\tau_{\rm L}\) decomposition therefore gives a pivot-free
\(LDL^T\) factorization in

\[
 O\bigl((M+p+k)\tau_{\rm L}^2\bigr)                       \tag{17}
\]

arithmetic, \(O((M+p+k)\tau_{\rm L})\) storage, and
\(O((M+p+k)\tau_{\rm L})\) work for each subsequent right-hand side.

If \(w_0=K_0^{-1}g\neq0\) and \(w_\rho=K_\rho^{-1}g\), then whenever
\(\rho\|K_0^{-1}\|_2<1\),

\[
 {\|w_\rho-w_0\|_2\over\|w_0\|_2}
 \leq {\rho\|K_0^{-1}\|_2\over
                 1-\rho\|K_0^{-1}\|_2}.                 \tag{18}
\]

Thus a public inverse-norm bound permits regularization below any requested
relative direction tolerance. At sufficient working precision, residual
recomputation can test the original unregularized Newton contract; iterative
refinement can enforce it only under the usual backward-error and contraction
hypotheses. No unconditional finite-precision certification is asserted.

#### Proof

Order the positive group as \((x,V)\) and the negative group as \((U,y)\).
The positive diagonal block is positive definite because its Schur complement
is \(D-VV^T\succ0\); the negative diagonal block is
\(-\operatorname{diag}(I,\rho I)\prec0\).  Hence (16) is symmetric
quasidefinite.  Such matrices are strongly factorizable after a symmetric
permutation.  In a chordal order every eliminated column has at most
\(\tau_{\rm L}\) later neighbors, which gives the usual width-squared
factorization and width-linear triangular-solve counts.

Writing \(K_\rho=K_0-\rho E\) with \(\|E\|=1\), the resolvent identity and
Neumann bound give

\[
 \|w_\rho-w_0\|
 \leq \rho\|K_\rho^{-1}\|\,\|w_0\|
 \leq {\rho\|K_0^{-1}\|\over1-\rho\|K_0^{-1}\|}\|w_0\|,
\]

which is (18).  \(\square\)

Equation (17) is a real-arithmetic count. Forming (6) additionally uses one
norm and a constant number of square roots per noncentered block; unlike the
one-hub field-operation theorem, this branch is not asserted over an
arbitrary field. A finite-precision theorem still needs bounds on scaling,
element growth, working precision, and refinement. Quasidefiniteness removes
exact zero-pivot breakdown for every symmetric permutation, but does not by
itself rule out small pivots or imply backward stability or
dimension-free precision.

## From coarse cone incidence to latent treewidth

Let \(C\) be the bipartite graph whose vertices are the Lorentz blocks and
the equality rows, with an edge \(i\sim j\) when row \(j\) uses some scalar
coordinate of block \(i\).  Suppose every scalar column of \(A\) has at most
one nonzero.  If \(C\) has treewidth \(w\), then

\[
 \boxed{\tau_{\rm L}\leq\max\{2w+1,3\}.}                 \tag{18a}
\]

To prove this, start with a width-\(w\) decomposition of \(C\).  In every bag
replace each cone vertex by its two hub vertices and leave every row vertex
unchanged.  The new main bags have size at most \(2(w+1)\).  If coordinate
\(x_{i\ell}\) is used in row \(j\), attach a leaf bag
\(\{u_i,v_i,j,x_{i\ell}\}\) to any main bag that contained the coarse edge
\(i\sim j\).  If the coordinate is unused, attach
\(\{u_i,v_i,x_{i\ell}\}\) to a main bag containing cone \(i\).  These bags
cover every expanded edge.  Their running-intersection property follows from
the original decomposition and from the fact that each coordinate appears in
only one leaf.  The maximum bag size is
\(\max\{2(w+1),4\}\), proving (18a).

This gives a broad constant-width family hidden by dense cone blocks.  For
example, take any forest as the coarse cone--row incidence graph, allow rows
to couple arbitrarily many adjacent blocks subject to that forest, and use a
fresh scalar coordinate for every incidence edge.  Then \(w=1\) and
\(\tau_{\rm L}\leq3\), independently of the number and dimensions of the
Lorentz blocks.

Therefore every Newton system in the trajectory has

\[
 \tau_{\rm L}\leq3,                                      \tag{19}
\]

even though a generic materialized Hessian has treewidth at least
\(\max_i(m_i-1)\).  The exact Newton solve costs \(O(M+p+k)\) field
operations, and the regularized quasidefinite solve has the same linear
arithmetic and storage scaling.

The product Lorentz barrier has parameter \(\nu=2k\). Suppressing the usual
initial-gap and neighborhood constants, a standard short-step method has the
generic trajectory bound

\[
 O\left(\sqrt{k}\log{1\over\epsilon}\right)              \tag{20}
\]

and total structured Newton arithmetic

\[
 O\left((M+p+k)\sqrt{k}\log{1\over\epsilon}\right).      \tag{21}
\]

This is a genuine many-cone, graph-coupled family, not the one-cone or
independent-block special case.

## Direct cones versus three-dimensional norm trees

Suppose for clarity that \(s\geq2\) and every block has dimension \(s+1\), so
\(M=k(s+1)\).  Keeping each Lorentz cone intact gives barrier parameter
\(2k\), constant latent width in the family above, and linear work per Newton
solve.

The small-cone barrier penalty below is unavoidable even if all \(k\) blocks
are reformulated jointly rather than by separate norm trees.

### Proposition 4 (additive Lorentz-curvature lower bound)

Every exact extended formulation of \(Q_{s+1}^k\) by
\(\prod_{j=1}^LQ_{m_j}\), with arbitrary affine slices, projections, and free
variables, satisfies

\[
 \boxed{\sum_{j=1}^L(m_j-2)\geq k(s-1).}               \tag{21a}
\]

In particular, if all factors are three-dimensional, then

\[
 \boxed{L\geq k(s-1).}                                  \tag{21b}
\]

Consequently every possibly coupled logarithmically homogeneous
self-concordant barrier on that ambient \(Q_3^L\) product has

\[
 \boxed{\nu\geq2k(s-1).}                               \tag{21c}
\]

#### Proof

Fixing every axial coordinate to one restricts an exact lift of the cone
product to an exact lift of

\[
 C=(B_2^s)^k.
\]

Its polar is

\[
 C^\circ=\left\{(y_1,\ldots,y_k):
                    \sum_i\|y_i\|_2\leq1\right\}.
\]

Choose positive \(\lambda_i\) with \(\sum_i\lambda_i=1\).  The local Lorentz
slack-curvature argument below applies even though the resulting contact set
is not a relatively open patch of the nonsmooth boundary of \(C\).
Because \(C\) is bounded, eliminate free variables and
pass to the minimal product face \(F=\prod_jF_j\) containing the feasible
slice, exactly as in the Lorentz curvature reduction.  The reduced lift is
proper.  Each \(F_j\) is the zero face, a ray, or the full \(Q_{m_j}\), so its
local curvature capacity is at most \(m_j-2\).  Slater duality for the reduced
lift, minimum-norm primal fibers, and minimum-norm attained dual multipliers
give semialgebraic factor maps \(A_j(x)\in F_j\),
\(B_j(y)\in F_j^*\) satisfying
\[
 1-\langle x,y\rangle=\sum_j\langle A_j(x),B_j(y)\rangle.
\]
More explicitly, identify both contact manifolds with
\(\mathcal M=(S^{s-1})^k\) through
\(X(n)=(n_i)_i\) and \(Y_\lambda(n)=(\lambda_i n_i)_i\).
The semialgebraic compositions \(A\circ X\) and \(B\circ Y_\lambda\) have a
common dense open \(C^1\) locus.  Choose \(n_0\) there and only then take the
independent local unit-vector charts
\(x_i(u_i),v_i(w_i)\in S^{s-1}\), centered at \(n_{0,i}\), and put
\(y_i(w_i)=\lambda_i v_i(w_i)\).  Their slack is
\[
 1-\sum_i\langle x_i(u_i),y_i(w_i)\rangle
 =\sum_i\lambda_i
        \bigl(1-\langle x_i(u_i),v_i(w_i)\rangle\bigr).  \tag{21d}
\]
At the diagonal complementary contact, its mixed \(u,w\) derivative is
block diagonal with nonsingular blocks \(-\lambda_i I_{s-1}\), and therefore
has rank \(k(s-1)\).  On the other hand,
differentiating one summand in the independent variables gives a
positive-semidefinite matrix of rank at most \(m_j-2\): for a nonzero
full-cone factor it is
\(\alpha_j\beta_j Dn_j^TDn_j\), while a zero or ray factor contributes zero.
Rank subadditivity proves (21a), and (21b) follows for \(m_j=3\).

Finally, each \(Q_3\) contains a two-dimensional section linearly isomorphic
to \(\mathbb R_+^2\).  Restricting any ambient barrier to the product of
these sections gives a barrier on \(\mathbb R_+^{2L}\), whose parameter is at
least \(2L\).  Combine this with (21b) to obtain (21c).  \(\square\)

Replacing the epigraph \(t_i\geq\|z_i\|_2\) by an exact binary norm tree uses
\(s-1\) copies of \(Q_3\) per original cone.  The lifted formulation still
has linear size and constant ordinary KKT treewidth, so its structured solve
is still only linear.  But its standard product barrier has parameter

\[
 \nu_{\rm tree}=2k(s-1),                                  \tag{22}
\]

and hence generic short-step bound

\[
 O\left(\sqrt{ks}\log{1\over\epsilon}\right).            \tag{23}
\]

The binary tree attains the lower bound (21b), so this \(\Theta(\sqrt s)\)
ambient-product-barrier penalty is not an artifact of choosing separate
trees: holding the initialization and accuracy logarithm fixed, it applies
to every exact pure-\(Q_3\) reformulation whose conic-form complexity theorem
uses a logarithmically homogeneous barrier on the ambient product.  Such a
reformulation produces no
asymptotic per-step gain on the forest-incidence family.  A bit-complexity
statement can also place a barrier-dependent initial-gap factor inside the
logarithm.  This is not an intrinsic barrier lower bound for the projected
feasible set and not an iteration lower bound: a custom barrier on the affine
slice or a special path-following analysis might beat the generic ambient-cone
self-concordant guarantee.

## QIPM replacement consequence

Consider a hybrid SOCP QIPM which, at every outer iteration, materializes a
dense classical Newton direction or updated iterate before constructing the
next nonlinear system.  Assume:

- matched access: current entries, block norms, and right-hand sides are
  classically evaluable at the precision charged to the quantum oracle;
- a fixed rank-expanded supergraph and width-\(\tau_{\rm L}\) decomposition
  are supplied for every legal trajectory;
- the robust outer theorem accepts any direction meeting its stated Newton
  residual contract; and
- either exact arithmetic is the comparison model, or the regularization and
  finite-precision conditions following Theorem 3 hold.

Then replacing every quantum linear solve by Theorem 2 or 3 gives the same
outer guarantee with total classical work

\[
 \sum_t O\bigl((M_t+p_t+k_t)(\tau_{{\rm L},t}+1)^2\bigr)   \tag{24}
\]

in the unconditional exact-arithmetic branch, with the decomposition
compaction term charged once when needed.  The regularized branch has the
same width-squared order and a reusable symmetric factor.  Dense classical
materialization already costs
\(\Omega(M_t+p_t)\) word writes per round.  Hence for
\(p_t+k_t=O(M_t)\) and \(\tau_{{\rm L},t}=M_t^{o(1)}\), this architecture has
no polynomial total-work speedup in the ambient dimension.  Constant latent
width gives a linear classical replacement per round even if the displayed
Hessian is dense.

This does **not** exclude:

- a coherent QIPM that never materializes its iterate;
- scalar, observable, state, or sample output;
- quantum-only access to the instance or current iterate;
- a family with growing rank-expanded treewidth or unstable bit complexity;
- quantum speedup in Hessian/gradient formation for a tall implicit model; or
- parallel-depth improvements over sequential arithmetic.

## Literature screen and novelty boundary

The ingredients have clear antecedents:

- Goldfarb and Scheinberg's product-form Cholesky method and later SOCP
  implementations exploit one positive and one negative rank-one correction
  per Lorentz block.  The local companion note on
  [dimension-independent Lorentz Newton sampling](2026-09-04-lorentz-newton-sq-dequantization.md)
  already records this algebra for the inverse Hessian.
- ECOS exploits augmented sparsity for second-order cones under Nesterov--Todd
  scaling: Domahidi, Chu, and Boyd,
  [*ECOS: An SOCP solver for embedded systems*](https://doi.org/10.23919/ECC.2013.6669541)
  (2013).
- Chen and Goulart formalize sparse-plus-signed-low-rank Hessians and
  quasidefinite augmentation for nonsymmetric cones:
  [*An Efficient Implementation of Interior-Point Methods for a Class of
  Nonsymmetric Cones*](https://doi.org/10.1007/s10957-024-02573-5)
  (2025).
- Vanderbei proves that every symmetric permutation of a symmetric
  quasidefinite matrix admits a pivot-free \(LDL^T\) factorization:
  [*Symmetric Quasidefinite
  Matrices*](https://doi.org/10.1137/0805005) (1995). This is an
  exact-factorization statement, not a uniform finite-precision guarantee.
- Fomin, Lokshtanov, Pilipczuk, Saurabh, and Wrochna gave the earlier general
  \(O(n\tau^3)\) exact linear-system algorithm.  Fürer, Hoppen, and
  Trevisan sharpened Gaussian elimination and linear-system solution to
  \(O(n\tau^2)\) from a supplied compact bipartite tree decomposition:
  [*Fast Gaussian Elimination for Low Treewidth
  Matrices*](https://doi.org/10.4230/LIPIcs.ESA.2025.116) (ESA 2025).
- Existing QIPM-SOCP analyses charge a quantum linear solve and tomography but
  do not parameterize the classical comparator by this latent graph; see
  Kerenidis, Prakash, and Szilagyi,
  [*Quantum algorithms for Second-Order Cone Programming and Support Vector
  Machines*](https://doi.org/10.22331/q-2021-04-08-427), and Dalzell et al.,
  [*End-To-End Resource Analysis for Quantum Interior-Point Methods and
  Portfolio Optimization*](https://doi.org/10.1103/PRXQuantum.4.040325).
- [Gouveia, Parrilo, and
  Thomas](https://arxiv.org/abs/1111.3164) establish the general equivalence
  between cone lifts and slack factorizations.  The companion
  [Lorentz-curvature note](2026-09-04-exact-lorentz-curvature-budget.md)
  specializes the local factor geometry to one positively curved body.
  Proposition 4 above uses a different corner-contact manifold to make the
  capacity lower bound additive across a product of balls; it does not assume
  that this nonsmooth product boundary is a positive-curvature patch.
- [Fawzi](https://arxiv.org/abs/1610.04901) develops second-order-cone rank
  obstructions, and [Saunderson](https://doi.org/10.1137/19M1245670) develops
  face-chain obstructions to lifts by products of low-complexity cones.
  Neither source states the additive product-ball factor count used here.

A targeted search for `treewidth SOCP Newton`, `augmented sparsity SOCP
treewidth`, and `quantum interior point SOCP treewidth low rank` found no
paper stating Theorems 2--3, the coarse-incidence treewidth proposition, or the
direct-versus-norm-tree QIPM comparison.  This supports apparent novelty but
does not establish it.  A separate targeted search for product-ball
second-order-cone rank, joint Lorentz lifts, and additivity of SOC extension
complexity found no statement of Proposition 4.  The results should be
presented as apparently new synthesis theorems pending specialist priority
review.

## Audit record

The independent audit checked the Lorentz Hessian signs and eigenvalues,
the rank-one downdate criterion, both hub Schur complements, nonsingularity
of the one-hub augmentation, applicability of the general low-treewidth
linear-system theorem (including its arbitrary-field and consistent-system
hypotheses, its tolerance of accidental cancellation, nice-decomposition
compaction, and the width-\(2\tau_{\rm L}+1\) doubled row--column construction),
and the
quasidefinite pivot-free \(LDL^T\) count. It also verified the coarse
cone--row incidence bound and its forest width-three corollary, the
direct-versus-\(Q_3\)-tree barrier arithmetic, the weighted additive
curvature lower bound for arbitrary joint Lorentz lifts, the minimum
\(k(s-1)\) pure-\(Q_3\) factor count, and the coupled ambient-barrier lower,
Neumann regularization bound, and matched-materialization QIPM comparison.
The audit added the real-arithmetic/square-root distinction, the
zero-solution qualification in (18), the primary quasidefinite citation,
and the finite-precision caveats above. The exact branch's removal of
regularization and no-cancellation assumptions is limited to exact field
arithmetic and does not imply stable floating-point factorization. No
algebraic error or direct literature collision was found.
