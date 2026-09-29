# Review: exact moment solutions and arithmetic of the optimal Gram face

Date: 2026-09-28. Status: independent reconstruction of the proposed
moment uniqueness and rational rank bound, followed by a full reading
of the [integrated note](strict-hessian-moment-arithmetic.md); no
mathematical defect found. Sections 4–5 develop further consequences
during this review and therefore need a separate review before being
described as independently verified.

The full positive definite Hessian Gram assumption gives a unique
rank-one optimum of the order-two moment relaxation. It also gives
strict complementarity over the reals. If the minimizer is irrational,
every rational optimal Gram matrix has smaller rank, and no nonzero
rational PSD matrix exposes the real optimal Gram face. These are
arithmetic facts about an already exact relaxation.

## 1. Assumption and the existing Taylor lemma

Let $F\in\mathbb Q[x_1,\ldots,x_n]$ be a quartic with an identity

\[
 v^{\mathsf T}\nabla^2F(x)v
  =\begin{pmatrix}v\\x\otimes v\end{pmatrix}^{\mathsf T}
       M\begin{pmatrix}v\\x\otimes v\end{pmatrix},
                    \qquad M\in\mathbb Q^{n(n+1)\times n(n+1)},\
                    M\succ0.
 \tag{1}
\]

The complete basis in (1) is material. This assumption is stronger
than strong convexity together with SOS-convexity.

It implies uniform strong convexity, coercivity, and a unique minimizer
$a$. Put $m=F(a)$ and $K=\mathbb Q(a)$. The point $a$ is algebraic:
it is a nonsingular zero of the rational gradient equations because
its Hessian is positive definite.

Let $V(x)$ list all monomials of degree at most two, starting with 1;
put $N=\binom{n+2}{2}$ and $e=V(a)$. The
[previous Taylor lemma](rational-sos-convex-descent-prior.md)
already proves that $F-m$ has a positive definite Gram in the centered
basis

\[
                  z_a(x)=((x_i-a_i)_i,
                    ((x_i-a_i)(x_j-a_j))_{i\le j}).
\]

To check the lemma's rank conclusion directly, set $u=x-a$. Taylor's
formula integrates the Hessian at $a+tu$ against $1-t$. The map from
the centered coefficient vector $(b,c)$ to its Hessian coordinates is

\[
                  T_t(b,c)=(b,a\otimes b+tEc),
\]

where $E$ injectively duplicates symmetric quadratic coordinates into
ordered tensor coordinates. Thus $T_t$ is injective for $t>0$, and
$\int_0^1(1-t)T_t^{\mathsf T}MT_t\,dt$ is positive definite.
Translation to the full basis gives

\[
 F(x)-m=V(x)^{\mathsf T}Q_*V(x),\quad
 Q_*\succeq0,\quad \operatorname{rank}Q_*=N-1,\quad
                          \ker Q_*=\mathbb R e.
 \tag{2}
\]

Every entry of this particular $Q_*$ belongs to $K$, since the Taylor
integral has polynomial integrands over $K$. The local lemma and its
rank statement are verified here, not claimed as new prior-independent
results.

## 2. Unique optimal moments

Consider the unconstrained order-two moment problem

\[
             \inf\{L_y(F):y_0=1,\ M_2(y)\succeq0\},
 \tag{3}
\]

with moments through total degree four. Equation (2) proves the lower
bound $m$; the moments $y_\gamma=a^\gamma$ attain it. If $y$ is any
optimal solution, then

\[
                 \langle Q_*,M_2(y)\rangle=L_y(F-m)=0.
\]

For PSD matrices $P,R$, zero trace product implies $PR=0$: the PSD
matrix $P^{1/2}RP^{1/2}$ has trace zero, and is therefore zero.
Consequently the range of $M_2(y)$ lies in $\ker Q_*=\mathbb R e$.
Its $(0,0)$ entry is one, while $e_0=1$, so

\[
                       M_2(y)=ee^{\mathsf T}.
 \tag{4}
\]

Every monomial of degree at most four is a product of two monomials
of degree at most two. Thus (4) determines every component of $y$:
$y_\gamma=a^\gamma$. The moment optimizer is unique and rank one.
No representing-measure assumption, genericity, or limiting rank
argument was used. The pair $(ee^{\mathsf T},Q_*)$ is strictly
complementary, with ranks $1$ and $N-1$.

The stronger hypothesis cannot be replaced without argument by
“strongly convex and SOS-convex.” For example

\[
                         F(x_1,x_2)=x_1^2+x_2^2+x_2^4
\]

has Hessian $\operatorname{diag}(2,2+12x_2^2)\succeq2I$ and is
SOS-convex. In the basis $(1,x_1,x_2,x_1^2,x_1x_2,x_2^2)$, the matrix

\[
                         \operatorname{diag}(1,0,0,t,0,0),
                                  \qquad t\ge0,
\]

is a consistent moment matrix: take $y_{(4,0)}=t$, $y_0=1$, and all
other nonconstant moments zero. Its objective value is zero. Hence
higher optimal moments are not unique in this example.

## 3. Rational rank loss

Now suppose $m\in\mathbb Q$, so the optimal Gram feasibility problem
has rational affine equations. Set

\[
       r=\dim_{\mathbb Q}
              \operatorname{span}_{\mathbb Q}\{a^\alpha:|\alpha|\le2\}.
 \tag{5}
\]

If $Q\succeq0$ is any rational Gram matrix of $F-m$, evaluation at $a$
gives $e^{\mathsf T}Qe=0$ and hence $Qe=0$. Every row of $Q$ is
therefore a rational linear relation among the coordinates of $e$.
The relation space has dimension $N-r$, so

\[
                         \operatorname{rank}Q\le N-r.
 \tag{6}
\]

This proves the proposed bound. If $a\notin\mathbb Q^n$, then $r\ge2$.
Thus no rational optimal $Q$ is strictly complementary to the unique
moment optimizer. This does not mean that strict complementarity fails
for the SDP: (2) proves that it holds over the reals.

The bound does not guarantee that a rational Gram exists or that its
maximum rank is $N-r$. For the separately constructed four-variable
degree-nine example, $N=15$ and $r=9$, so it would bound a rational
Gram's rank by six; the separate descent obstruction proves there is
no rational Gram at all. This numerical substitution is conditional
on that construction's independently verified field-span calculation.
If $m$ is irrational, a rational Gram of $F-m$ is already impossible
by its constant coefficient.

## 4. The exact coefficient field of maximal-rank certificates

Let $L\subseteq\mathbb R$ be any field containing $\mathbb Q$.
If an optimal Gram $Q$ has rank $N-1$ and entries in $L$, then its
one-dimensional kernel is defined over $L$. Normalize its generator
to have first coordinate one. By (2) and evaluation at $a$, that
generator is $e=V(a)$, so $a\in L^n$ and $K\subseteq L$.
Conversely, (2) constructs a maximal-rank optimal Gram over $K$.
Consequently

\[
 \text{a rank-}(N-1)\text{ optimal Gram exists over }L
                           \quad\Longleftrightarrow\quad K\subseteq L.
 \tag{7}
\]

In particular, the field of the minimizer is exactly the least
coefficient field needed for a maximal-rank optimal Gram. The analogous
statement for the unique optimal moment vector follows from its first
moments. This is stronger than saying that an irrational minimizer
prevents rational optimal moments.

## 5. A one-step real face with no rational exposing step

Let $\mathcal G$ be the real feasible set of optimal Grams of $F-m$.
Every element kills $e$, and (2) supplies one whose kernel is exactly
$\mathbb R e$. Thus its minimal PSD face is

\[
              \mathcal F_e=\{Q\succeq0:Qe=0\}.
 \tag{8}
\]

The matrix $Y=ee^{\mathsf T}$ exposes this face. It is an admissible
facial-reduction multiplier for the coefficient equations: if
$\mathcal A(Q)$ is the coefficient vector of $V^{\mathsf T}QV$,
then $Y=\mathcal A^*(y(a))$ and
$\langle y(a),\operatorname{coef}(F-m)\rangle=0$.
After this one reduction, $Q_*$ is positive definite on $e^\perp$.
The real singularity degree of this Gram feasibility problem is
therefore one.

Any PSD matrix $Y'$ with $\langle Y',Q\rangle=0$ for every
$Q\in\mathcal G$ must satisfy $\operatorname{range}Y'\subseteq\mathbb R e$,
by applying it to $Q_*$. Hence

\[
                            Y'=c\,ee^{\mathsf T},\qquad c\ge0.
 \tag{9}
\]

For $c>0$, the entry ratios $Y'_{0,\alpha}/Y'_{0,0}=a^\alpha$
recover $a$. Therefore every nonzero such exposing matrix has a
coefficient field containing $K$, and $ee^{\mathsf T}$ attains that
field. In particular, if $a$ is irrational, there is no nonzero rational
PSD exposing matrix that vanishes on the full real feasible Gram set.
Standard facial reduction restricted to such rational exposing
matrices cannot even take its first nontrivial step.

For comparison, define $U$ as the real orthogonal complement of the
rational relation space in (5). It has dimension $r$ and is spanned
by rational vectors. All rational optimal Grams, when they exist,
belong to the smaller face

\[
                      \{Q\succeq0:U\subseteq\ker Q\}.
 \tag{10}
\]

Thus a procedure allowed to discard real feasible Grams while
preserving rational feasibility faces a different problem. The
obstruction in (9) does not exclude that procedure, algebraic facial
reduction, or any other exact algorithm. Nor does it imply a numerical
conditioning bound or a decision-complexity lower bound.

## 6. Prior results and what this adds

The prior Taylor lemma in
[rational-sos-convex-descent-prior.md](rational-sos-convex-descent-prior.md)
is the main local input. Its proof was rechecked above.

[Lasserre, *Convexity in Semi-Algebraic Geometry and Polynomial
Optimization*, arXiv:0806.3784v3](https://arxiv.org/pdf/0806.3784),
Theorem 2.6 and Theorem 3.3, already gives Jensen's inequality for
normalized PSD moment functionals, exactness of the SOS-convex
relaxation, and recovery from first moments. Lemmas 2.4–2.5 credit the
SOS Taylor-integral argument to Helton and Nie. The present uniqueness
claim uses the stronger positive definite full Gram and identifies all
moments, not only the first moments. It is a direct complementary-rank
consequence, not a new general SDP exactness theorem.

The PSD-face description by common kernels and PSD exposing matrices is
standard; see, for example,
[Hu et al., *Facial reduction for symmetry reduced semidefinite and
doubly nonnegative programs*](https://pmc.ncbi.nlm.nih.gov/articles/PMC10195748/),
Section 3. The field recovery in (7) and (9) is elementary linear
algebra specialized to an evaluation vector with constant coordinate
one. The specific conjunction of a strict rational convexity
certificate, real singularity degree one, and a prescribed nontrivial
coefficient field is the potentially useful consequence.

[Laplagne, *Facial reduction for exact polynomial sum of squares
decompositions*, arXiv:1810.04215v1](https://arxiv.org/pdf/1810.04215),
Sections 3.1–3.2, is a particularly close antecedent. Proposition 3.2
uses real zeros as Gram-kernel vectors. Section 3.2 observes that a
rational Gram must also kill all algebraic conjugates of such a vector;
Proposition 3.4 uses their trace to obtain rational kernel relations.
Thus the rational-envelope mechanism behind (6) is established prior,
and its rank bound is an elementary dimension restatement. The
maximal-rank and exposing-field conclusions additionally use (2),
which identifies the complete real kernel as a single normalized
evaluation line. Laplagne's rational-candidate restriction is compatible
with the distinction made after (10).

[Kolmogorov, Naldi, and Zapata, *Certifying solutions of degenerate
semidefinite programs*, arXiv:2405.13625v3](https://arxiv.org/pdf/2405.13625),
introduction and main algorithmic setup, explicitly treats algebraic
feasible points and certification near a maximum-rank point. Thus
irrational feasible SDPs and algebraic certification are established
prior. The conclusions here should not be framed as their discovery.

The primary passages just identified were inspected on 2026-09-28.
The Lasserre, Laplagne, and Kolmogorov–Naldi–Zapata texts are saved
under moment-arithmetic-sources, with their arXiv identifiers in the
filenames.
Searches also combined “facial reduction,” “rational exposing vector,”
“irrational minimal face,” “strict complementarity,” and “SOS-convex
unique optimal moments.” No equivalent full statement was identified
in this limited search. Novelty is not established.

The proof uses exact identities and PSD linear algebra. The displayed
nonunique-moment counterexample was checked symbolically. No numerical
SDP computation or Lean proof is claimed. Only targeted document and
counterexample checks were run; no project-wide checks or CI logs were
used.
