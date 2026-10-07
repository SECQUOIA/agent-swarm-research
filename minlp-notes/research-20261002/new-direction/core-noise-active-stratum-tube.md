# Core noise avoids residual active-pattern boundaries

Date: 2026-10-02. Status: independently reviewed exact boundary and image
formulas, a uniform algebraic enclosure, and a finite-grid tube bound. A
separate primary-source audit supplied the singular-algebraic-set tube
theorem used in Section 5. This note does not assert a complete optimization
theorem.

Uniform strong residual convexity makes the residual optimizer unique.
Its bound-active pattern changes only on a lower-dimensional semialgebraic
set of core points. The corresponding stationary-noise vectors lie on an
algebraic hypersurface of uniformly bounded degree. This gives a finite-grid
tail for proximity to pattern changes. It does not give strict
complementarity.

## 1. Closed core faces and the unique residual selector

Let the core box be rational and compact, with \(k\) nonfixed coordinates.
Let \(Y=\prod_{i=1}^r[\ell_i,u_i]\) be a rational compact residual box,
with fixed coordinates substituted. Let \(F(v,y)\) be a rational
polynomial of degree at most \(d\). Assume the verified bound

\[
             \nabla^2_{yy}F(v,y)\succeq\mu I,
             \qquad\mu>0,
 \tag{1}
\]

throughout the original product box. The residual selector and value are

\[
 s(v)=\operatorname*{argmin}_{y\in Y}F(v,y),
 \qquad V(v)=F(v,s(v)).
 \tag{2}
\]

The argmin in (2) is a single point. Adding core-only noise
\(\gamma^Tv\) changes neither \(s\) nor its active-pattern sets.

Fix an original core face. Represent it as its **closed** box
\(K\subseteq\mathbb R^q\) in its free coordinates, substituting its
fixed coordinates in \(F\). All relative topologies below refer to this
closed \(K\). Its affine boundary \(\partial K\) is the ordinary box
boundary in \(\mathbb R^q\). First assume \(q\ge1\).

The selector is Lipschitz. Indeed, choose finite bounds

\[
 B\ge\sup\|F_{yv}\|_2,\qquad
 A\ge\sup\|F_{vv}\|_2.
\]

The two optimality variational inequalities, combined with strong
monotonicity of \(F_y(v,\cdot)\), give

\[
 \|s(v)-s(w)\|\le(B/\mu)\|v-w\|.
 \tag{3}
\]

The envelope derivative along the face is

\[
 \nabla V(v)=F_v(v,s(v)),\qquad
 \|\nabla V(v)-\nabla V(w)\|
       \le H\|v-w\|,\quad H=A+B^2/\mu.
 \tag{4}
\]

The derivatives in (4) extend continuously to the closed face. One may
also obtain a local differentiable extension around it: compactness and
(1) preserve a positive residual modulus on a sufficiently small open
neighborhood of the core box. No lower bound on that neighborhood's radius
is needed for this note.

## 2. Exact boundary sets and their dimension

For each residual coordinate define the closed subsets of \(K\)

\[
 A_i^\ell=\{v\in K:s_i(v)=\ell_i\},\qquad
 A_i^u=\{v\in K:s_i(v)=u_i\}.
\]

Define

\[
 S_K=\partial K\ \cup\!
       \bigcup_{i=1}^r\bigl(\operatorname{bd}_K A_i^\ell
                         \cup\operatorname{bd}_K A_i^u\bigr),
 \qquad E_K=-\nabla V(S_K)\subseteq\mathbb R^q.
 \tag{5}
\]

Here \(\operatorname{bd}_K\) denotes boundary in the relative topology
of the closed box \(K\). In particular the boundary of \(K\) as a
subset of itself is empty; the separate \(\partial K\) term in (5)
is necessary.

Every set in (5) is compact and semialgebraic. Each
\(\operatorname{bd}_K A_i\) has empty relative interior: an open subset
of that boundary lying in the closed set \(A_i\) would instead belong
to its relative interior. Since \(K\) is full-dimensional in its free
coordinates, a semialgebraic subset with empty relative interior has
dimension at most \(q-1\). The same is true of \(\partial K\). Thus

\[
        \dim S_K\le q-1,\qquad \dim E_K\le q-1.
 \tag{6}
\]

The image inequality uses that the gradient map in (4) is semialgebraic;
semialgebraic maps cannot increase dimension. Continuity makes its image
of the compact \(S_K\) compact. In particular \(E_K\) is closed, bounded,
and has empty interior. There is no hidden closure of a nonclosed image.

For a point \(a\in K\setminus S_K\), every sufficiently small relative
ball about \(a\) lies in the interior of \(K\), and each residual
coordinate has a constant bound-active status throughout the ball. More
precisely, this holds for every radius less than
\(\operatorname{dist}(a,S_K)\). Along any path in the ball, entering or
leaving one of the closed sets \(A_i^\ell,A_i^u\) would cross its
relative boundary.

## 3. Three quantified blocks describe the gradient image

Write \(\mathcal G(v,y)\) for the following quantifier-free box KKT
formula, including \(v\in K\):

\[
 \bigwedge_i\left[
 \begin{array}{l}
 (y_i=\ell_i\ \wedge\ F_{y_i}(v,y)\ge0)\ \vee\\
 (\ell_i\le y_i\le u_i\ \wedge\ F_{y_i}(v,y)=0)\ \vee\\
 (y_i=u_i\ \wedge\ F_{y_i}(v,y)\le0).
 \end{array}\right]
 \tag{7}
\]

Residual convexity makes (7) equivalent to \(y=s(v)\); strong convexity
makes this graph single-valued. No multipliers or quantified minimization
formula are needed.

For a lower-active set, its relative boundary has the exact description

\[
\begin{split}
 v\in\operatorname{bd}_K A_i^\ell
 \quad\Longleftrightarrow\quad
 \exists y\ \forall\varepsilon\ \exists w,z:\quad&
 \mathcal G(v,y)\ \wedge\ y_i=\ell_i\ \wedge\\
 &\left[\varepsilon\le0\ \vee\
 \left\{\mathcal G(w,z)\ \wedge\
        \|w-v\|^2<\varepsilon^2\ \wedge\ z_i>\ell_i\right\}\right].
\end{split}
 \tag{8}
\]

For \(\varepsilon>0\), the last condition says that every relative
neighborhood meets the complement of \(A_i^\ell\). Because \(A_i^\ell\)
is closed, membership in it and this condition are exactly boundary
membership. For nonpositive \(\varepsilon\) the disjunction is vacuous.
Upper-active boundaries use \(y_i=u_i\) and \(z_i<u_i\).

For the image of one lower-active boundary, take the noise vector
\(\beta\in\mathbb R^q\) as the free variable and use

\[
 \exists(v,y)\ \forall\varepsilon\ \exists(w,z):\quad
 \text{the matrix in (8)}\ \wedge\ \beta+F_v(v,y)=0.
 \tag{9}
\]

The affine-box-boundary image instead has the one-block formula

\[
 \exists(v,y):\quad \mathcal G(v,y)\ \wedge\ v\in\partial K
                              \ \wedge\ \beta+F_v(v,y)=0.
 \tag{10}
\]

Taking the union of (9), its upper-bound versions, and (10) describes
\(E_K\). Keeping these \(2r+1\) pieces separate avoids any issue about
moving the finite disjunction across quantified blocks.

Let \(N=q+r\), \(D_0=\max(2,d)\), and choose
\(s_0=50(N+1)\) as a safe atom-count bound for each displayed formula.
Formula (9) has three blocks of sizes \(N,1,N\), \(q\) free variables,
and degree at most \(D_0\), measured jointly in all variables. The
fixed-block quantifier-elimination bound already audited in the
[finite-noise tail note](polynomial-finite-noise-tails.md#2-two-quantified-blocks-give-a-uniform-scalar-section-bound)
therefore gives an effective universal constant \(a\) such that

\[
             Q=(s_0D_0)^{a(N+1)^4}
 \tag{11}
\]

bounds the number of output disjuncts, the number of polynomial atoms per
disjunct, and every output degree. The exponent in (11) is deliberately
coarse. It covers the smaller formula (10) as well. The relevant primary
result is Renegar's fixed-block elimination theorem, rather than an
unrestricted doubly exponential CAD estimate.

This is a format bound over real coefficients. Neither coefficient
heights, the noise values, nor \(\mu^{-1}\) enter it. The original core
noise does not occur in the formula at all. Fixed deterministic linear
terms may be included in \(F\), with the same bound.

## 4. A nonzero polynomial contains the whole exceptional image

For each quantifier-free output in Section 3, discard constant polynomial
atoms and identically zero polynomials. Multiply the remaining distinct
nonconstant polynomials, using the empty product one when needed. Call
this product \(P_j\).

Its zero set contains the corresponding image. Otherwise an image point
at which every atom polynomial is nonzero would have a neighborhood where
all their signs, and hence the entire output formula, are constant. That
neighborhood would lie in the image, contradicting (6). Constant and zero
atoms have fixed truth values and do not affect this argument. If no
nonconstant atoms remain, the image must be empty.

Each \(P_j\) is nonzero and has degree at most \(Q^3\): there are at
most \(Q^2\) atom occurrences, each of degree at most \(Q\). Their
product over the at most \(2r+1\) pieces gives a nonzero polynomial
\(P_K\) satisfying

\[
 E_K\subseteq Z(P_K),\qquad
 \deg P_K\le D_K:=(2r+1)Q^3.
 \tag{12}
\]

This proves a base-computable degree bound \(D_K=2^{\operatorname{poly}(I)}\).
The algorithm using a probability bound need not run elimination or
construct \(P_K\). The degree bound alone is enough. Nothing here bounds
\(E_K\)'s location or diameter by a coefficient-independent number;
neither is needed for a local tube estimate inside the noise cube.

## 5. Algebraic tube input and the finite-grid reduction

The primary input is Basu and Lerario, *Hausdorff approximations and volume
of tubes of singular algebraic sets*, Theorem 1.1, printed page 1 of the
[primary preprint](https://arxiv.org/pdf/2104.05053) (published in
*Mathematische Annalen* 387 (2023), 79--109). It applies to a real algebraic
set \(Z\subseteq\mathbb R^q\) defined by polynomials of degree at most
\(D\), with \(\dim Z\le m\), and a point \(X\) uniform in any
Euclidean ball of radius \(T\). For every \(\epsilon>0\),

\[
 \Pr\{\operatorname{dist}(X,Z)\le\epsilon\}
 \le 4\left(\frac{4qD\epsilon}{T}\right)^{q-m}
       \left(1+\frac{(4D+1)\epsilon}{T}\right)^m.
 \tag{13a}
\]

The hypotheses allow singular sets, an upper bound on real dimension,
and arbitrary real coefficients. The set need not be bounded. In
particular, a nonzero polynomial has a zero set of real dimension at most
\(q-1\), so we may take \(m=q-1\) even when the actual dimension is
smaller. An empty zero set is immediate.

For \(\epsilon\le T\), (13a) yields the ball-probability bound
\(16qD(4D+2)^{q-1}\epsilon/T\). To obtain a cube estimate, put
\(T=\sqrt q R\) and enclose \([-R,R]^q\) in the corresponding ball.
The ratio of ball volume to cube volume is at most \(q^{q/2}\), because
the ball lies in the cube \([-T,T]^q\). For \(\epsilon\le R\),
the normalized tube volume in the smaller cube is therefore at most

\[
 16qD(4D+2)^{q-1}q^{(q-1)/2}\frac\epsilon R.
\]

The following deliberately larger integer coefficient is convenient:

\[
 C(q,D)=16q^{q+1}D(4D+2)^{q-1},
 \qquad \log C(q,D)=O(q\log(q+1)+q\log(D+1)).
 \tag{13b}
\]

Thus every nonzero real polynomial \(P\) of degree at most \(D\ge1\)
satisfies, for \(R>0\) and \(0<\epsilon\le R\),

\[
 \frac{\operatorname{vol}_q\{x\in[-R,R]^q:
                \operatorname{dist}(x,Z(P))\le\epsilon\}}
      {(2R)^q}
       \le C(q,D)\frac\epsilon R.
 \tag{13}
\]

Since \(C\ge1\), the resulting probability bound
\(\min\{1,C\epsilon/R\}\) also handles \(\epsilon>R\) by the trivial
bound one. Constants depending only on dimension would not suffice here
without a size estimate; (13b) supplies the required explicit bound.

Now let \(M\ge2\), and sample each coordinate of \(\gamma\)
independently and uniformly from the \(M\) equally spaced points of
\([-\sigma,\sigma]\), including both endpoints. Put

\[
 h=\frac\sigma{M-1},\qquad R=\sigma+h.
\]

The cubes \(g+[-h,h]^q\), one centered at every grid point \(g\),
have disjoint interiors and tile \([-R,R]^q\). Thus adding an independent
uniform vector in \([-h,h]^q\) to a uniform grid point gives the uniform
distribution on \([-R,R]^q\).

If \(\operatorname{dist}(g,E_K)\le\delta\), every point in its cube
has distance at most \(\delta+\sqrt q h\) from \(E_K\), and hence from
\(Z(P_K)\). Applying (13), with the trivial bound one when necessary,
proves

\[
 \Pr\{\operatorname{dist}(\gamma,E_K)\le\delta\}
 \le\min\left\{1,\ C(q,D_K)
          \left(\frac\delta\sigma+\frac{\sqrt q}{M}\right)\right\}.
 \tag{14}
\]

The exact ratio before weakening it in (14) is

\[
 \frac{\delta+\sqrt q h}{R}
       =\frac{M-1}{M}\frac\delta\sigma+\frac{\sqrt q}{M}.
 \tag{15}
\]

In particular (14) includes the finite-grid atoms on \(E_K\) at
\(\delta=0\). The mesh term is necessary. The proof neither conditions
on a selected core face nor substitutes an almost-sure statement for a
finite-law estimate. Since \(\log D_K=\operatorname{poly}(I)\), the
coefficient in (14) has logarithm polynomial in the base input under
(13).

## 6. What this supplies to a local closure proof

Suppose \(a\in\operatorname{relint}K\) is any face-stationary point of
\(V(v)+\gamma^Tv\), so
\(\gamma_K=-\nabla V(a)\). By (4) and compactness of \(S_K\),

\[
 \operatorname{dist}(\gamma_K,E_K)
       \le H\operatorname{dist}(a,S_K).
 \tag{16}
\]

Consequently

\[
 \{\exists a\in\operatorname{relint}K:
   \nabla V(a)+\gamma_K=0,
   \ \operatorname{dist}(a,S_K)\le\rho\}
 \subseteq
 \{\operatorname{dist}(\gamma_K,E_K)\le H\rho\}.
 \tag{17}
\]

All original core faces are fixed before sampling, and there are at most
\(3^k\) of them. Apply (14) to their free-coordinate noise subvectors
and take a union bound. This is valid even when the optimizing face is
chosen after observing the noise. The other core-noise coordinates add
only a constant on a fixed face, so they do not change its \(E_K\).

For \(q=0\), a closed face is a point, every residual bound-active set
is either that point or empty, and all relative boundaries are empty.
There is no active-pattern transition to avoid and no free-core gradient.
Handle this case directly and omit it from the tube union. No assertion
about a hypersurface in \(\mathbb R^0\) is needed.

The conclusion is a relative ball on which residual bound status is
constant. It is **not** a positive lower bound on active residual
multipliers. For example,

\[
 F(v,y)=v^2+(y+v^2)^2,
 \quad v\in[-1,1],\quad y\in[0,1]
 \tag{18}
\]

has residual modulus two, selector \(s(v)=0\) everywhere, and active
multiplier \(F_y(v,0)=2v^2\), which vanishes at the interior point zero.
The core value \(v^2+v^4\) still has quadratic growth. Thus a proof
requiring strict complementarity cannot obtain it from (14). The separate
[small-multiplier curvature lemma](small-residual-multiplier-curvature.md)
is intended to handle weak residual multipliers on a stable active-pattern
ball. Its hypotheses and subsequent certificate construction remain
separate from the tube estimate proved here.

## Verification record

Independent actual-file review passed Sections 1--6, including the exact
boundary formula, fixed-block elimination, algebraic enclosure, explicit
ball-to-cube coefficient, grid atoms, and adaptive face union. A separate
literature reviewer checked Basu--Lerario Theorem 1.1 in the primary PDF;
local literature ingestion remains with the designated writer.

An inline `python3 - <<'PY'` command checked six exact symbolic identities,
including the jitter ratio and the weak-multiplier example. It also passed
600 exact finite-grid tube checks for the one-dimensional zero set
\(\{-2,0,2\}\), including zero-radius atoms and multiple grid spacings.
The same command checked this file's whitespace, math delimiters, and local
links. The scoped command
`git diff --check -- research-20261002/new-direction/core-noise-active-stratum-tube.md`
passed. These checks supplement the proof; they are not a computational
verification of its higher-dimensional claims.

No external search, literature ingestion, index modification, project-wide
checks, or CI inspection was performed by this task.
