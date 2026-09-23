# An exact SOC-granularity versus ambient-barrier tradeoff

Status: Superseded by a sharp independently audited theorem  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the theorem; moderate on novelty (the lower-bound proof is elementary and may be folklore)

> **Sharp update.** The factor-three gap in this note has now been closed.
> [Exact Lorentz-block complexity of the Euclidean
> ball](2026-09-04-exact-lorentz-curvature-budget.md) proves
> \[
> \sum_i(m_i-2)\geq N-1,\qquad
> k_d(B_2^N)=\left\lceil\frac{N-1}{d-2}\right\rceil,
> \]
> for the same arbitrary-slice/projection/free-variable lift model. It also
> proves a local mixed-curvature version for general convex bodies. The
> weaker coordinate-count argument below is retained as provenance, but
> its statements that the exact minimum is open are superseded.

## Result

Let

\[
 B_2^N=\{x\in\mathbb R^N:\|x\|_2\leq1\},
 \qquad
 Q_m=\{(t,y)\in\mathbb R\times\mathbb R^{m-1}:t\geq\|y\|_2\}.
\]

Fix integers \(N\geq2\) and \(d\geq3\). Consider every exact extended
formulation of \(B_2^N\) whose inequality cone is

\[
 K=\prod_{i=1}^k Q_{m_i},\qquad 2\leq m_i\leq d,
 \qquad M:=\sum_{i=1}^k m_i,
\]

and which otherwise permits arbitrary affine equalities, projections, and
unrestricted free variables. Then

\[
 \boxed{M\geq N+1},
 \qquad
 \boxed{k\geq\left\lceil\frac{N+1}{d}\right\rceil}.       \tag{1}
\]

Conversely, there is an exact norm-tree formulation with

\[
 k\leq \left\lceil\frac{N-1}{d-2}\right\rceil             \tag{2}
\]

Lorentz blocks, each of dimension at most \(d\). Hence the minimum number
of bounded-size Lorentz blocks satisfies

\[
 \left\lceil\frac{N+1}{d}\right\rceil
 \leq k_d(B_2^N)
 \leq \left\lceil\frac{N-1}{d-2}\right\rceil,             \tag{3}
\]

with the evident one-block convention when \(d\geq N+1\). In particular,

\[
 k_d(B_2^N)=\Theta\!\left(\max\{1,N/d\}\right)             \tag{4}
\]

uniformly for \(d\geq3\); the displayed upper and lower bounds differ by
at most a factor three. For \(d=3\), every exact formulation uses
\(\Omega(N)\) Lorentz blocks of dimension at most three, while the binary
norm tree uses exactly \(N-1\) copies of \(Q_3\).

Each Lorentz cone has symmetric-cone rank and optimal ambient normal-barrier
parameter two, where a normal barrier is a logarithmically homogeneous
self-concordant barrier. The product cone therefore has

\[
 \nu(K)=2k.
\]

Combining this identity with (3) gives the tight-up-to-constants ambient
barrier law

\[
 \boxed{
 \nu_{\leq d}(B_2^N)
   =\Theta\!\left(\max\{1,N/d\}\right).}                  \tag{5}
\]

Here \(\nu_{\leq d}(B_2^N)\) means the minimum, over exact lifts in the
model above, of the optimal normal-barrier parameter of the ambient product
cone \(K\); it is not the minimum barrier parameter of the projected ball
itself.

Thus the direct one-cone formulation
\((1,x)\in Q_{N+1}\) has ambient parameter \(2\), whereas every exact
bounded-dimension product-cone formulation has ambient parameter
\(\Omega(N/d)\). For \(d=O(1)\), the \(\sqrt\nu\) multiplier in the standard
short-step guarantee changes from a constant to \(\Theta(\sqrt N)\). Holding
the other initialization and accuracy terms fixed, this gives
\(O(\sqrt N\log(1/\epsilon))\) rather than
\(O(\log(1/\epsilon))\) Newton steps at the level of that generic guarantee.

This last statement is **not** an unconditional iteration lower bound.
It applies to conic path-following analyses using a barrier for the ambient
product cone. Eliminating the lift and using the dense ball barrier, or
exploiting a special central path by another method, can evade that
representation-dependent accounting.

## Universal compact-body corollary

The dimension argument is not specific to Lorentz cones or balls. Let
\(C\subset\mathbb R^N\) be any full-dimensional compact convex body and let

\[
 K=\prod_{i=1}^k K_i,
\]

where every \(K_i\) is a nontrivial proper cone of dimension
\(m_i\leq d\). If \(C\) has an exact representation of the form (6), with
arbitrary affine slices, projections, and free variables, then

\[
 \sum_{i=1}^k m_i\geq N+1,
 \qquad
 k\geq\left\lceil\frac{N+1}{d}\right\rceil.              \tag{5a}
\]

Moreover, every self-concordant barrier on the **ambient product cone**
has parameter at least \(k\), including barriers that are not separable
across the factors. To see this, choose \(e_i\in\operatorname{int}K_i\)
and restrict the barrier to

\[
 E=\{(\alpha_1e_1,\ldots,\alpha_ke_k):\alpha\in\mathbb R^k\}.
\]

Because each \(K_i\) is pointed,
\(K\cap E\) is linearly isomorphic to \(\mathbb R_+^k\). Restriction
preserves the self-concordance and gradient inequalities and remains a
barrier, so its parameter cannot be smaller than the optimal parameter
\(k\) of the nonnegative orthant. Writing \(\nu_{\rm SC,ambient}\) for the
optimum over this general barrier class, therefore

\[
 \nu_{\rm SC,ambient}\geq k
 \geq\left\lceil\frac{N+1}{d}\right\rceil.                \tag{5b}
\]

For Lorentz products, the optimum over the narrower normal-barrier class is
\(\nu_{\rm normal,ambient}=2k\), which recovers (5). This does not assert
that the optimum over all self-concordant barriers is \(2k\). Neither (5a)
nor (5b) is an intrinsic barrier lower bound for
\(C\): both concern the chosen ambient product-cone representation.

## Lift model and elimination of free variables

The claimed lower bound allows the following general model:

\[
 B_2^N
 =\{Pz+Qu+p:\ z\in K,\ u\in\mathbb R^f,
                  \ Az+Bu=a\}.                            \tag{6}
\]

Here \(u\) is completely unrestricted, and all displayed maps and vectors
are arbitrary. This covers an affine slice followed by an affine
projection, as well as standard-form copies and consensus equalities.

The free variables cannot hide output dimension. Indeed, if \(v\in\ker B\)
and \((z,u)\) is feasible, then \((z,u+tv)\) is feasible for every real
\(t\). Boundedness of \(B_2^N\) forces \(Qv=0\). Thus

\[
 \ker B\subseteq\ker Q,
\]

so elementary linear algebra gives a map \(R\) with \(Q=RB\). On the
feasible set,

\[
 Pz+Qu+p=(P-RA)z+Ra+p.                                    \tag{7}
\]

Consequently (6) is an ordinary affine image of

\[
 K\cap L,
 \qquad
 L:=\{z\in\mathbb R^M:a-Az\in\operatorname{im}B\}.        \tag{8}
\]

## Proof of the \(N+1\) lower bound

Since the image in (7) has affine dimension \(N\), the set \(K\cap L\)
has affine dimension at least \(N\). Therefore \(M\geq N\).

Suppose for contradiction that \(M=N\). Then \(K\cap L\) has full affine
hull in \(\mathbb R^M\). Since it is contained in the affine subspace
\(L\), this forces \(L=\mathbb R^M\), and hence \(K\cap L=K\). The linear
part \(P-RA:\mathbb R^M\to\mathbb R^N\) in (7) has full rank and is
therefore invertible. But \(K\) contains a nonzero ray, whose invertible
image is unbounded, contradicting compactness of \(B_2^N\). Hence

\[
 M\geq N+1.
\]

Because \(M=\sum_i m_i\leq kd\), (1) follows. Notice that this proof did
not use curvature or rotational symmetry: every full-dimensional compact
convex body in \(\mathbb R^N\) obeys the same \(M\geq N+1\) cone-coordinate
bound for every nontrivial conic lift of the form (6).

For a conventional proper lift without free variables, the same number is
visible from slack rank: the ball slack kernel
\(S(x,y)=1-\langle x,y\rangle\) has ordinary function rank \(N+1\), while
factorization through a cone in \(\mathbb R^M\) has rank at most \(M\).

## Proof of the norm-tree upper bound

Put \(a=d-1\). Choose a rooted tree with \(N\) leaves, every internal node
having between two and \(a\) children, and

\[
 k=\left\lceil\frac{N-1}{a-1}\right\rceil
  =\left\lceil\frac{N-1}{d-2}\right\rceil
\]

internal nodes. Such a tree exists because the identity

\[
 N-1=\sum_{v\ {\rm internal}}(\deg(v)-1)
\]

can be realized by splitting \(N-1\) into \(k\) integers in
\(\{1,\ldots,a-1\}\). Explicitly, if the parts are
\(b_1,\ldots,b_k\), make the internal nodes a chain: node \(i<k\) has
\(b_i\) leaf children and the next internal node as one more child, while
the last node has \(b_k+1\) leaf children. This realizes all \(N\geq2\)
and \(d\geq3\), including the binary case \(d=3\).

Associate a scalar \(t_v\) with each internal node. If its children carry
values \(z_{v,1},\ldots,z_{v,j}\), impose

\[
 (t_v,z_{v,1},\ldots,z_{v,j})\in Q_{j+1},\qquad j+1\leq d. \tag{9}
\]

Leaf values are the coordinates of \(x\), internal child values are copies
of the corresponding \(t\)'s joined by affine consensus equalities, and
the root value is fixed to one. Recursing through (9) shows feasibility
implies \(\|x\|_2\leq1\). Conversely, set every nonroot \(t_v\) equal to
the Euclidean norm of the leaves below \(v\), and keep the root value fixed
at one. Every nonroot constraint then holds at equality, and the root
constraint holds because \(\|x\|_2\leq1\). This proves (2).

## Barrier and QIPM consequence

The canonical Lorentz barrier

\[
 F_m(t,y)=-\log(t^2-\|y\|_2^2)
\]

has parameter two, independently of \(m\), and parameters add over
Cartesian products. More strongly, Güler and Tunçel identify the optimal
normal-barrier parameter of a homogeneous cone with its cone rank. The
product of \(k\) Lorentz cones is a homogeneous self-dual cone of rank
\(2k\), so changing the normal barrier on the **ambient product cone**
cannot improve its parameter below \(2k\). Equations (3)--(5) follow.

This gives a precise granularity tradeoff for sparse SOCP/QIPM design:
breaking one dense \(Q_{N+1}\) block into bounded-size blocks can make every
cone-local operation and every consensus row sparse, but it necessarily
introduces \(\Theta(N/d)\) ambient cone blocks and hence
\(\Theta(N/d)\) ambient barrier parameter. The binary \(Q_3\) norm-tree
lift in the parameterized scalar-frontier construction is therefore
asymptotically optimal in both block count and product-barrier parameter,
even though the present lower bound leaves a factor-three gap in its exact
number of blocks.

This barrier accounting alone is not a QIPM runtime theorem. The dimension,
sparsity, fill, and conditioning of the Newton system, as well as data-access,
precision, and output costs, remain separate; eliminating the tree
equalities can also destroy the row sparsity visible in the lifted model.

## What is and is not known from this argument

- The total-coordinate lower bound \(M\geq N+1\) is sharp: the single
  \(Q_{N+1}\) lift attains it.
- For bounded \(d\), the block count and ambient parameter are pinned to
  the correct order, but the exact minimum number of blocks is open here.
  The dimension/slack-rank argument cannot improve
  \(\lceil(N+1)/d\rceil\).
- A tempting stronger estimate
  \(k\geq\lceil(N-1)/(d-2)\rceil\), which would make norm trees exactly
  optimal, appears to require a new curvature, topology, or Lorentz-slack
  factorization invariant. It is not asserted.
- For \(d=2\), finite products are polyhedral, and affine slices and
  projections remain polyhedral. They cannot represent \(B_2^N\) exactly
  when \(N\geq2\).
- Equation (5) concerns normal barriers on the ambient product cone. It does
  not exclude a small-parameter barrier on the affine slice or projected
  body, nor does it lower-bound the number of iterations of every classical
  or quantum algorithm.

## Literature boundary

[Gouveia, Parrilo, and Thomas](https://arxiv.org/abs/1111.3164) establish
the general equivalence between cone lifts and slack-operator
factorizations. [Fawzi](https://arxiv.org/abs/1610.04901) defines
second-order-cone rank and notes that higher-dimensional Lorentz cones have
finite lifts by products of three-dimensional Lorentz cones.
[Güler and Tunçel](https://doi.org/10.1007/BF01584844) identify the optimal
normal-barrier parameter of a homogeneous cone with its rank; this supplies
the intrinsic logarithmically homogeneous ambient-product statement used
above. The standard orthant lower bound supplies the parameter \(k\) of
\(\mathbb R_+^k\) used in the universal restriction argument. The standard
norm-tree construction is classical and is not claimed as new.

A targeted search of these sources and of work on SOC rank, bounded-block
semidefinite extension degree, and limitations of products of cones found
no explicit quantitative theorem combining (i) arbitrary free-variable
SOC lifts of the Euclidean ball, (ii) the \(N+1\) coordinate lower bound,
and (iii) the resulting bounded-cone-dimension ambient-barrier law (5).
The ingredients are elementary enough that priority should not be claimed
without a broader specialist review. The useful new point for this project
is the rigorous QIPM granularity consequence and the proof that free
variables or consensus formulations do not evade it.
