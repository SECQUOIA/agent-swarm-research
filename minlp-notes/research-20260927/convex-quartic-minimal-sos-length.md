# A lower bound on the number of squares in a convex quartic

Date: 2026-09-28. Status: complete proof, with a
[fresh independent review](convex-quartic-minimal-sos-length-fresh-review.md)
and a [separate literature audit](convex-quartic-minimal-sos-length-literature-audit.md).
The argument uses standard Brouwer degree. No priority claim is made.

**Theorem.** Let $F\in\mathbb R[x_1,\ldots,x_n]$ be globally convex,
of degree exactly four, and suppose

\[
 F=\sum_{i=1}^m q_i^2,\qquad F(p)=0,\qquad
                       \nabla^2F(p)\succ0.
 \tag{1}
\]

Then $m\ge n+1$. The factors may have arbitrary real coefficients;
the conclusion therefore also applies to rational or integer squares.
Global strong convexity is sufficient, but is not needed.

The bound is attained for every $n\ge1$ by

\[
             (x_1^2+\cdots+x_n^2)^2+x_1^2+\cdots+x_n^2.
 \tag{2}
\]

More particularly, the
[compressed cyclic quartics](cyclic-quartic-square-compression.md)
have minimum SOS length exactly $n+1$, while their unique zeros have
joint field degree

\[
                    \frac{2^{n+1}-(-1)^{n+1}}3.
\]

The existence of a simple sharp example such as (2) is separate from
the cyclic family's arithmetic conclusion. This note supplies a
structural restriction on convex quadratic least-squares objectives;
it does not establish an optimization algorithm or a decision lower
bound.

## 1. Reduction to a square polynomial map

Every factor in a polynomial SOS representation of a quartic has degree
at most two. Indeed, the sum of the squares of the highest homogeneous
parts cannot vanish identically unless all those parts vanish.

Write $q=(q_1,\ldots,q_m)$. At a zero of $F=\|q\|^2$, all
components of $q$ vanish, so

\[
                     \nabla^2F(p)=2Dq(p)^{\mathsf T}Dq(p).
 \tag{3}
\]

Thus $m\ge n$. It remains to rule out $m=n$. Assume from now on
that $q:\mathbb R^n\to\mathbb R^n$.

The zero $p$ is the only real zero. Otherwise convexity and
nonnegativity would make $F$ identically zero on the segment between
$p$ and another zero. Its second derivative at $p$ in that segment's
nonzero direction would vanish, contrary to (1).

Equation (3) also says that $Dq(p)$ is nonsingular. A square map with
exactly one regular zero has odd topological degree when it is proper.
The obstacle is that the leading quadratic part of $q$ need not itself
be proper. The next two sections remove precisely this obstacle.

## 2. Directions where the leading quartic vanishes

Write $q=q_2+q_1+q_0$, with homogeneous parts of degrees two, one,
and zero, and put

\[
                 H(x)=\|q_2(x)\|^2,
             \qquad K=\{v:H(v)=0\}.
 \tag{4}
\]

The homogeneous quartic $H$ is convex: it is the pointwise limit of
the convex functions $t^{-4}F(tx)$ as $t\to+\infty$.
Its zero set $K$ is convex and invariant under every real scalar.
Consequently $K$ is a linear subspace.

For $v\in K$, $t\in\mathbb R$, and $0<\eta<1$, convexity and
homogeneity give

\[
 \begin{split}
 H(x+tv)
 &\le (1-\eta)H\left(\frac{x}{1-\eta}\right)
                +\eta H\left(\frac{tv}{\eta}\right)\\
 &= (1-\eta)^{-3}H(x).
 \end{split}
\]

Letting $\eta\downarrow0$ gives $H(x+tv)\le H(x)$. Applying the
same inequality to $x+tv$ and $-tv$ proves equality. Thus $H$
is constant along every affine translate of $K$.

Let $B_2$ be the symmetric vector-valued bilinear map associated to
$q_2$. For $v\in K$, $q_2(v)=0$, and

\[
 q_2(x+tv)=q_2(x)+2tB_2(x,v).
\]

Its squared norm is constant in $t$. The coefficient of $t^2$ is
$4\|B_2(x,v)\|^2$, so $B_2(x,v)=0$. Hence every component of
$q_2$ is independent of the directions in $K$, not merely their
squared norm.

Choose orthogonal input coordinates $x=(w,v)$, where
$v\in K\cong\mathbb R^k$ and
$w\in K^\perp\cong\mathbb R^r$, with $r=n-k$. Then

\[
                  q(w,v)=q_2(w)+Aw+Bv+c,
 \tag{5}
\]

where $B$ is an $n$-by-$k$ matrix. Since $Dq(p)$ is
nonsingular, $B$ has full column rank. As $F$ has degree four,
$q_2\ne0$, so $r\ge1$.

The restriction $H(w)=\|q_2(w)\|^2$ is positive for $w\ne0$.
This follows from the definition of $K$: a nonzero vector in
$K^\perp$ cannot also belong to $K$.

## 3. Convexity removes the quadratic coupling to the flat directions

For fixed $w$, the $ww$ block of the Hessian of $F(w,v)$ has
the form

\[
 \nabla^2_{ww}F(w,v)
       =C(w)+2\sum_{i=1}^n(Bv)_i\nabla^2 q_{2,i}.
 \tag{6}
\]

Here $C(w)$ does not depend on $v$: the $w$-derivative of (5)
is independent of $v$, and the remaining Hessian term is the second
term in (6). Global convexity makes (6) positive semidefinite for every
$v\in\mathbb R^k$. A symmetric matrix affine in a freely signed
real parameter is positive semidefinite for every parameter value
only if its linear coefficient vanishes. Therefore

\[
                    B^{\mathsf T}q_2(w)=0
                         \quad\text{for every }w.
 \tag{7}
\]

For clarity, first apply the matrix observation to each direction
$v=te_j$. It gives zero Hessian for the scalar homogeneous quadratic
$(Be_j)^{\mathsf T}q_2(w)$. Such a quadratic with zero Hessian is
identically zero, which proves (7).

Let $T$ be an $r$-by-$n$ matrix whose rows are an orthonormal
basis of $(\operatorname{im}B)^\perp$. For $k=0$, take $T=I$
and omit the expressions involving $B$. Define

\[
 \begin{split}
 v_0(w)&=-(B^{\mathsf T}B)^{-1}B^{\mathsf T}(Aw+c),\\
 \bar q(w)&=T(q_2(w)+Aw+c).
 \end{split}
 \tag{8}
\]

Equation (7) is what makes $v_0$ affine. Orthogonal decomposition in
the output space now gives the exact identity

\[
 F(w,v)=\|B(v-v_0(w))\|^2+\|\bar q(w)\|^2.
 \tag{9}
\]

In particular,

\[
                 \bar F(w):=\|\bar q(w)\|^2
                              =F(w,v_0(w))
 \tag{10}
\]

is convex, since it is the restriction of $F$ to an affine graph.
It has a unique zero $w_*=p_w$; a zero would otherwise lift through
$v_0$ to a second zero of $F$. At this zero,

\[
 \nabla^2\bar F(w_*)
   =E^{\mathsf T}\nabla^2F(p)E\succ0,
           \qquad E=\begin{pmatrix}I_r\\ Dv_0\end{pmatrix}.
 \tag{11}
\]

The matrix $E$ has full column rank. Since $\bar q$ has exactly
$r$ components, (3) applied to (11) proves that
$D\bar q(w_*)$ is nonsingular.

Finally, (7) says $q_2(w)\in(\operatorname{im}B)^\perp$. Hence the
leading homogeneous part $\bar q_2=Tq_2$ satisfies

\[
                       \|\bar q_2(w)\|=\|q_2(w)\|.
 \tag{12}
\]

Compactness of the unit sphere and the strict positivity established
in Section 2 provide a constant $a>0$ such that

\[
                      \|\bar q_2(w)\|\ge a\|w\|^2.
 \tag{13}
\]

We have reduced to a square quadratic map in $r\ge1$ variables,
with one regular zero and a positive definite squared norm of its
leading part. No rationality of coordinates or transformations is
needed for this SOS-length statement.

## 4. The parity contradiction

For $0\le t\le1$, set

\[
            h_t(w)=\bar q_2(w)+t(\bar q_1(w)+\bar q_0).
 \tag{14}
\]

There are constants $b,c\ge0$ such that, uniformly in $t$,

\[
              \|h_t(w)\|\ge a\|w\|^2-b\|w\|-c.
 \tag{15}
\]

Thus (14) is a proper homotopy. Its extension to the one-point
compactifications is a continuous homotopy of maps $S^r\to S^r$.
Brouwer degree is therefore constant along it:

\[
                        \deg\bar q=\deg\bar q_2.
 \tag{16}
\]

The unique zero $w_*$ of $\bar q$ is regular. The local-degree
formula gives

\[
                   \deg\bar q=\operatorname{sign}
                                \det D\bar q(w_*)\in\{-1,1\}.
 \tag{17}
\]

On the other hand, choose a nonzero regular value $y$ of
$\bar q_2$; such values exist by Sard's theorem. Its inverse image
is finite, because it is both compact, by properness, and discrete,
by regularity. The map is even:
$\bar q_2(-w)=\bar q_2(w)$. Its inverse image therefore consists of
pairs $\{w,-w\}$, with no fixed point because $y\ne0$.

Each point contributes $+1$ or $-1$ to the degree. The sum over
each pair is even, so $\deg\bar q_2$ is even. More precisely,
$D\bar q_2(-w)=-D\bar q_2(w)$; the contributions cancel when $r$
is odd and agree when $r$ is even. An empty inverse image gives
degree zero and causes no exception. This also covers $r=1$.

Equations (16) and (17) are incompatible. Hence $m=n$ is impossible,
and the theorem follows.

The imported topological facts are classical. The local-degree sum and
homotopy invariance are in Hatcher, *Algebraic Topology*, Section 2.2,
especially Proposition 2.30. Sard's theorem and the regular-value
degree formulas are also in Milnor, *Topology from the Differentiable
Viewpoint*, Sections 2, 4, and 5. The uniform estimate (15) verifies the
properness condition needed when applying the compact-space statements.

## 5. Sharpness and necessary assumptions

For (2), direct differentiation gives

\[
 \nabla^2F(x)=8xx^{\mathsf T}+(4\|x\|^2+2)I\succeq2I.
\]

Its only zero is the origin, and it has $n+1$ displayed squares.
The theorem proves that this length cannot be shortened. Applying the
same theorem to the independently verified cyclic compression gives
its exact length $n+1$, even allowing arbitrary real coefficients in
a competing representation.

Each principal hypothesis has a concrete role.

- Without the zero-value assumption, $(1+\|x\|^2)^2$ is a globally
  strongly convex quartic with just one square. Its minimum is one.
- Without positive definite Hessian at the zero, $\|x\|^4$ is a
  globally convex quartic with a unique zero and just one square.
- Without global convexity, $x^2+(y-x^2)^2$ has two squares in two
  variables, a unique zero, and Hessian $2I$ at that zero. At
  $(0,1)$, its $xx$ Hessian entry is $-2$.
- Without degree exactly four, a positive definite quadratic centered
  at its zero has an $n$-square representation.

The unchanged lower bound also fails at degree six. The fresh reviewer
supplied

\[
       G(x)=(x_1+x_1^3)^2+\sum_{j=2}^n x_j^2,
\qquad
       \nabla^2G(x)=
       \operatorname{diag}(2+24x_1^2+30x_1^4,2,\ldots,2)\succeq2I.
\]

It has only $n$ displayed squares and a unique zero at the origin.
The identity $x_1+x_1^3=x_1(1+x_1^2)$ proves uniqueness over the reals.
Thus global strong convexity and a nondegenerate zero do not rescue
the same conclusion in arbitrary higher degree.

SOS-convexity is neither assumed nor inferred here. The conclusion
applies when an SOS-convex polynomial also has a polynomial SOS
representation and satisfies (1), as the cyclic family does. It does
not assert that rational SOS-convex polynomials are SOS over the
rationals.

## 6. Literature comparison, verification, and open scope

The standard *SOS length* of a polynomial is the minimum number of
polynomial squares in a representation. Scheiderer's *Sum of squares
length of real forms* studies worst-case and typical lengths, gives
general bounds, and includes upper bounds using a real zero's
multiplicity. Those statements have different quantifiers and do not
immediately give the lower bound here for each globally convex quartic
with a nondegenerate zero. His Theorem 1.12 and Corollary 1.13 are
particularly relevant comparisons after homogenization. This limited
comparison does not establish novelty.

Sources examined on 2026-09-28:

1. [Hatcher, Chapter 2](https://pi.math.cornell.edu/~hatcher/AT/ATch2.pdf),
   Section 2.2, printed pages 134–136; local copy in
   `quartic-square-length-sources/hatcher-chapter2.pdf`.
2. [Milnor, *Topology from the Differentiable Viewpoint*](https://www.ux1.eiu.edu/~cidelman/Classes/4855%20and%205220/Supplementary%20Texts/MilnorTopDiffVpt.pdf),
   Sections 2, 4, and 5; local copy in
   `quartic-square-length-sources/milnor-differentiable-viewpoint.pdf`.
3. [Scheiderer, *Sum of squares length of real forms*, arXiv:1603.05430v1](https://staff.math.su.se/shapiro/ProblemSolving/Scheiderer!.pdf),
   introduction and Section 1, especially Theorem 1.12; local copy in
   `quartic-square-length-sources/scheiderer-sos-length-2016.pdf`.
4. [Harrison, *Quadratic Convexity and Sums of Squares*, 2013](https://web.math.ucsb.edu/~martin/dissertation.pdf):
   abstract, Theorems 3.2.10–3.2.11, and Section 3.3 were examined.
   The convexity there concerns the image of a quadratic map, with
   applications to coefficient-space parameterizations of all sums
   of a given number of squares. It differs from convexity of the
   scalar function $x\mapsto\|q(x)\|^2$ here. The examined statements
   do not imply the present individual-polynomial lower bound.
   Local copy: quartic-square-length-sources/harrison-dissertation-2013.pdf.

Searches combined “convex quartic,” “SOS length,” “number of squares,”
“nondegenerate zero,” “Pythagoras number,” and “proper quadratic map.”
No matching theorem was located in that search; this is not evidence
of priority. The reduction in Sections 2–3 and its combination with
degree parity are the specific proof to compare against further work.

No numerical experiment verifies the topological step. Its verification
is the explicit properness bound and the standard degree theorems.
The boundary examples and sharpness Hessian are checked by exact
symbolic calculation in `check_convex_quartic_minimal_sos_length.py`.
That check does not prove the universal theorem. No Lean proof or
project-wide verification is claimed.

Targeted command run, with exit status zero:

~~~text
python research-20260927/check_convex_quartic_minimal_sos_length.py
~~~

It verified the displayed sharpness and positive-minimum Hessian
identities in dimensions one through five, the nonconvex boundary
example, and an exact flat-direction completion whose two regular zeros
have opposite Jacobian signs. Targeted Markdown, control-character,
math-delimiter, and local-link checks also passed. No CI results were
inspected.

A higher-degree extension would need new restrictions, as the sextic
example shows. The affine reduction in Section 3 specifically uses the
quadratic degree of the residuals. Weaker local nondegeneracy is another
possible question, but the one-square quartic boundary above rules out
simply dropping that hypothesis.
