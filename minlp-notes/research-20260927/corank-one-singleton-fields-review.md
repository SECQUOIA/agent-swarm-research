# Independent check of the field of a corank-one singleton

Date: 2026-09-28. Scope: an independent proof audit of the following
proposition circulated by the root agent and the singleton-field prior
auditor. This review supplies its precise statement and checks the local
geometry and field argument. It does not establish novelty.

**Proposition.** Let

\[
 A(x)=A_0+\sum_{i=1}^n x_iA_i,
 \qquad A_i\in\mathbb S^m(\mathbb Q),
\]

and suppose $\{x\in\mathbb R^n:A(x)\succeq0\}=\{x^*\}$. If
$R=A(x^*)$ has corank one, then the coordinate field
$K=\mathbb Q(x_1^*,\ldots,x_n^*)$ has exactly one real embedding.

The proposed proof is correct. The two uses of the singleton assumption
are different and both are essential: it first rules out a positive
first-order change along the kernel, and then rules out a parameter
direction that preserves that kernel.

## Algebraicity and normalization

A singleton semialgebraic set defined over $\mathbb Q$ has algebraic
coordinates. For example, real closed field transfer gives a feasible
point over the real algebraic numbers, and uniqueness identifies that
point with $x^*$. Thus $K$ is a number field.

Since $R$ is a rank-$m-1$ matrix over $K$, its kernel has a generator
$v\in K^m$. Choose an index $j$ with $v_j\neq0$ and normalize so that
$v_j=1$. Write $F=\mathbb Q(v_1,\ldots,v_m)$. At this stage only
$F\subseteq K$ has been established.

## Why all coefficient quadratic forms vanish on the kernel

Suppose $v^{\mathsf T}A_i v\neq0$ for some $i$. Choose a real parameter
direction $\delta$ for which

\[
 v^{\mathsf T}\Bigl(\sum_i\delta_iA_i\Bigr)v>0.
\]

In an orthonormal basis adapted to $v^\perp$ and its one-dimensional
orthogonal complement, the matrix at $x^*+t\delta$ has the form

\[
 \begin{pmatrix}
   R_1+tE & tb\\
   tb^{\mathsf T} & t\beta
 \end{pmatrix},\qquad R_1\succ0,\quad\beta>0.
\]

For sufficiently small positive $t$, its upper block and its scalar
Schur complement $t\beta-t^2b^{\mathsf T}(R_1+tE)^{-1}b$ are positive.
This gives a positive definite feasible matrix at another parameter,
contradicting uniqueness. Therefore

\[
 v^{\mathsf T}A_i v=0\quad(1\leq i\leq n).
\]

Since $Rv=0$, it follows also that $v^{\mathsf T}A_0v=0$. This step
requires corank one: with a larger kernel, a nonzero directional
restriction can be indefinite and need not create a feasible side.

## Why the kernel coordinates determine the parameter field

Consider the affine linear system in $x$

\[
 A(x)v=0.                                             \tag{1}
\]

Its coefficients belong to $F$, and $x^*$ is a solution. Suppose that a
nonzero real parameter direction $\delta$ solves the corresponding
homogeneous system, so that $D=\sum_i\delta_iA_i$ satisfies $Dv=0$.
Symmetry then makes both cross blocks of $D$ between $v^\perp$ and
$\mathbb Rv$ zero. Consequently $R+tD$ preserves the kernel and is
positive definite on $v^\perp$ for every sufficiently small $|t|$.
It is positive semidefinite, contradicting singleton feasibility.

Thus (1) has a unique real solution. An injective linear system over
$F$ has its solution in $F$, by selecting a nonsingular coefficient
minor and applying Gaussian elimination. Hence $K\subseteq F$, and

\[
 K=F.                                                \tag{2}
\]

This also checks a useful dimension restriction: the vectors $A_iv$
are linearly independent and lie in $v^\perp$, so $n\leq m-1$.
No bound on $[K:\mathbb Q]$ follows from this dimension observation.

## Real embeddings

Let $\sigma:F\longrightarrow\mathbb R$ be any real embedding and set
$u=\sigma(v)$. Rationality of the coefficient matrices and the preceding
quadratic identities imply

\[
 u^{\mathsf T}A_i u=0\quad(0\leq i\leq n).
\]

The matrix $R$ itself uses the original parameter $x^*$; it is not
conjugated. Nevertheless the identities above give

\[
 u^{\mathsf T}Ru
 =u^{\mathsf T}A_0u+\sum_i x_i^*u^{\mathsf T}A_i u=0.
\]

Because $R\succeq0$, this forces $u\in\ker R=\mathbb Rv$. The
normalization $u_j=\sigma(1)=1=v_j$ gives $u=v$. Thus $\sigma$ fixes
every generator of $F$, and is its given real embedding. Together with
(2), this proves the proposition.

Every coordinate subfield also has exactly one real embedding. Indeed,
$[K:\mathbb Q]$ is odd, so the extension degree over any subfield is odd.
Each real embedding of that subfield extends to a real embedding of $K$:
apply the embedding to the coefficients of an odd-degree minimal
polynomial of a primitive element and choose a real root. Since $K$ has
only one real embedding, the subfield does as well.

## Converse and scope

The independently reviewed
[two-variable pencil construction](few-quadratic-unbounded-degree.md)
realizes $\{(\alpha,\alpha^2)\}$ with a unique corank-one feasible
matrix whenever the minimal polynomial of the nonrational number
$\alpha$ has exactly one real root. Every number field with one real
embedding has such a primitive element in its real realization. For
$K=\mathbb Q$, the rational pencil

\[
 \begin{pmatrix}1&x\\x&0\end{pmatrix}\succeq0
\]

has the singleton feasible set $\{0\}$ and corank one at that point.
Thus the proposition and the earlier construction classify the possible
coordinate fields for corank-one singleton rational spectrahedra.

Combining the proposition with the separate
[one-variable classification](one-parameter-spectrahedral-fields.md)
shows that a one-variable singleton with a corank-one feasible matrix
must be rational: its field is both totally real and has only one real
embedding. The size-$2d$ construction in that note has corank two, so
there is no conflict.

The proof does not apply to spectrahedral shadows, to a non-singleton
feasible set, or to higher corank. It does not imply that a conjugate
matrix of $R$ is positive semidefinite. Avoiding that invalid inference
is precisely the reason for using the rational quadratic identities at
the fixed original matrix $R$.

## Verification and prior status

This is an independent mathematical check of the proof steps. No
floating-point test, symbolic example, or formal proof assistant is used
as a substitute for the universal argument. Targeted Markdown checks
were run after writing the review; no project-wide verification or CI
inspection was performed.

The reviewed argument uses elementary positive semidefinite geometry,
real embeddings, and linear algebra. The
[prior audit](singleton-field-characterization-prior.md) and
[planar-pencil source comparison](planar-corank-one-singletons-prior.md)
record the literature status. An unsuccessful search for the exact
formulation does not establish novelty.
