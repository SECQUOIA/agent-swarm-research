# Boundaries for improving the product-sphere \(Q_3\) contact count

Status: Proved; independently audited
Started: 2026-09-04
Paper status: Not incorporated
Confidence: High on the stated subclasses; the unrestricted exact count remains open

## Executive result

Let

\[
 M=(S^q)^k,\qquad q\geq2,\qquad k\geq2,\qquad
 K(x,z)=\sum_{a=1}^k\lambda_a(1-x_a^Tz_a),                 \tag{1}
\]

where every \(\lambda_a>0\), \(\sum_a\lambda_a=1\), and put

\[
 n=kq,\qquad D=k(q+1)=n+k.
\]

The unrestricted globally labelled bi-\(C^1\) \(Q_3^L\) contact count is
currently known only within

\[
                 n+1\leq L\leq n+\lceil k/2\rceil.         \tag{2}
\]

This note establishes four rigorous boundaries around the remaining gap.

1. On every product of punctured-sphere charts, (1) has an exact smooth
   factorization with only \(n\) channels. Thus no obstruction based only
   on finitely many local germs or jets can prove an excess above \(n\).
2. If the channels separate according to a partition of the \(k\) sphere
   factors into \(m\) variable groups, then \(L\geq n+m\). A partition
   prescribed to consist of singletons and pairs attains equality. A
   maximally paired partition gives the known upper endpoint of (2).
3. If the factorization is a sum of common-scale squared-chord kernels,
   its functional inertia gives \(L\geq D-e\), where \(e\) counts the
   groups whose feature image is not contained in a Euclidean sphere. In
   particular, an \(n+1\)-channel construction of this kind needs at least
   \(k-1\) such groups.
4. A global stereographic factorization can be chosen so that an individual
   channel depends on all \(k\) sphere factors. Therefore a proposed
   unrestricted proof cannot assume that one Lorentz channel touches at
   most two coordinate blocks.

The first and fourth points rule out two natural proof strategies. The
second and third prove optimality in useful subclasses but do not establish
the conjectural unrestricted lower bound
\(L\geq n+\lceil k/2\rceil\).

## 1. Exact local saturation

Choose a pole \(p_a\in S^q\) for each factor and let

\[
 U_a=S^q\setminus\{p_a\},\qquad U=\prod_{a=1}^kU_a.
\]

For \(x_a\in U_a\), define

\[
 c_a(x_a)=1-p_a^Tx_a>0,
 \qquad
 F_a(x_a)=\frac{x_a-(p_a^Tx_a)p_a}{c_a(x_a)}
             \in p_a^\perp\cong\mathbb R^q.                \tag{3}
\]

The stereographic chord identity is

\[
 1-x_a^Tz_a
   =\frac{c_a(x_a)c_a(z_a)}2
      \|F_a(x_a)-F_a(z_a)\|_2^2.                           \tag{4}
\]

Use the null-paraboloid maps

\[
\begin{aligned}
 \mathcal U(t)&=\left(\frac{1+t^2}{2},
                       \frac{1-t^2}{2},t\right),\\
 \mathcal V(t)&=\left(\frac{1+t^2}{2},
                      -\frac{1-t^2}{2},-t\right),
\end{aligned}                                               \tag{5}
\]

which lie on the nonzero boundary of \(Q_3\) and satisfy

\[
                \langle\mathcal U(t),\mathcal V(u)\rangle
                       =\frac12(t-u)^2.                     \tag{6}
\]

Writing \(F_a=(f_{a1},\ldots,f_{aq})\), equations (4)--(6)
give the \(q\)-channel identity

\[
 \lambda_a(1-x_a^Tz_a)
 =\sum_{j=1}^q
   \left\langle
    \sqrt{\lambda_a}c_a(x_a)\mathcal U(f_{aj}(x_a)),
    \sqrt{\lambda_a}c_a(z_a)\mathcal V(f_{aj}(z_a))
   \right\rangle.                                          \tag{7}
\]

Concatenating (7) over \(a\) factorizes (1) on \(U\times U\) with
exactly \(kq=n\) smooth, nowhere-zero \(Q_3\) channels.

This is stronger than a formal jet construction: it is the exact two-point
identity on a neighborhood of every diagonal point after choosing poles
away from that point. Consequently every finite diagonal jet, including
all cross-block mixed derivatives, is compatible with local rank
saturation. The known \(+1\) lower bound and any possible further excess
must be global.

There is also a finite-sample strengthening. Given arbitrary finite primal
and dual sample sets in \(M\), choose each pole \(p_a\) outside the finite
union of their projections to the \(a\)-th sphere. One product chart then
contains every sample, and (7) factorizes the entire sampled submatrix with
\(n\) channels. Hence no finite submatrix, nor any finite collection of
off-diagonal derivative data contained in such charts, can witness the
global smooth excess above \(n\). The obstruction is genuinely an
infinite/global compatibility condition.

## 2. Exact count for partition-separated channels

Partition the coordinate indices and channel labels as

\[
 \{1,\ldots,k\}=G_1\sqcup\cdots\sqcup G_m,
 \qquad
 \{1,\ldots,L\}=I_1\sqcup\cdots\sqcup I_m.                 \tag{8}
\]

Call a factorization **partition-separated** if, for every \(i\in I_g\),

\[
 A_i(x)=A_i^g(x_{G_g}),\qquad B_i(z)=B_i^g(z_{G_g}).        \tag{9}
\]

Put

\[
 K_g(u,v)=\sum_{i\in I_g}
             \langle A_i^g(u),B_i^g(v)\rangle.             \tag{10}
\]

Every summand is nonnegative by self-duality of \(Q_3\). Since
\(K(x,x)=0\), every diagonal channel pairing vanishes. Hence
\(K_h(t,t)=0\) for every group \(h\) and every \(t\in(S^q)^{G_h}\).

Now freeze every group \(h\ne g\) at identical primal and dual arguments,
and vary only \(x_{G_g}=u\), \(z_{G_g}=v\). Equations (1) and (10) give

\[
 K_g(u,v)=\sum_{a\in G_g}\lambda_a(1-u_a^Tv_a).            \tag{11}
\]

Thus the channels in \(I_g\) form a global bi-\(C^1\) factorization of
the smaller product-sphere contact kernel. The compact simply connected
phase argument applies to \((S^q)^{|G_g|}\) and yields

\[
                |I_g|\geq q|G_g|+1.                        \tag{12}
\]

Summing (12) proves

\[
                         \boxed{L\geq n+m}.                 \tag{13}
\]

For every prescribed partition into singletons and pairs, this is exact. A
singleton has the standard \(q+1\)-coordinate-square factorization, and a
pair has the shared stereographic factorization with \(2q+1\) channels.
Choosing \(\lfloor k/2\rfloor\) pairs and, when necessary, one singleton
gives \(m=\lceil k/2\rceil\) and the count

\[
 n+m=n+\lceil k/2\rceil.                                   \tag{14}
\]

Any unrestricted improvement over (14) must violate separation with
respect to every maximally paired singleton/pair partition. No exact count
is asserted here for a partition having a group of three or more blocks;
the one-group case already contains the unrestricted open question.

## 3. A functional-inertia bound for multiscale chordal factors

Consider the symmetric subclass

\[
 K(x,z)=\sum_{g=1}^m
   \frac{r_g(x)r_g(z)}2
        \|F_g(x)-F_g(z)\|_2^2,
 \qquad F_g:M\to\mathbb R^{L_g},
 \qquad L=\sum_gL_g,                                       \tag{15}
\]

where \(r_g>0\) and all displayed maps are globally \(C^1\). Define

\[
 \alpha_g=\frac{r_g\|F_g\|^2}{2},\qquad
 \beta_g=r_g,\qquad h_{gj}=r_g(F_g)_j.                     \tag{16}
\]

The \(g\)-th kernel in (15) expands as

\[
 \alpha_g(x)\beta_g(z)+\beta_g(x)\alpha_g(z)
       -\sum_{j=1}^{L_g}h_{gj}(x)h_{gj}(z).                 \tag{17}
\]

On the formal feature space, its coefficient form has at most
\(L_g+1\) negative directions: one from the \((\alpha_g,\beta_g)\)
cross term and \(L_g\) from the \(h_{gj}\). If the image of \(F_g\) lies
on a Euclidean sphere, translate its center to the origin. Squared
distances do not change, and \(\|F_g(x)\|^2\) is then constant. Therefore
\(\alpha_g\) is a constant multiple of \(\beta_g\), so the cross term is
positive semidefinite and contributes no negative direction.

Let

\[
 e=\#\{g:F_g(M)\text{ is not contained in a Euclidean sphere}\}.       \tag{18}
\]

Pullback to the actual function span cannot increase negative index, so
the right side of (15) has at most \(L+e\) negative directions.

On the other hand, define

\[
 X(x)=(\sqrt{\lambda_1}x_1,\ldots,
       \sqrt{\lambda_k}x_k)\in S^{D-1}.                    \tag{19}
\]

Then \(K(x,z)=1-X(x)^TX(z)\). The constant function and all \(D\)
coordinate functions of \(X\) are linearly independent on \(M\), so this
kernel has functional inertia exactly \((1,D)\). Comparing negative
indices gives

\[
                          \boxed{L\geq D-e=n+k-e}.           \tag{20}
\]

In particular, since \(e\leq m\),

\[
                         L\geq n+k-m.                       \tag{21}
\]

An \(L=n+1\) representation within (15) therefore requires
\(e\geq k-1\): almost every missing channel must be paid for by a separate
noncospherical chordal summand. The functions \(r_g\) need not be distinct;
\(e\) counts summands in the displayed representation, not distinct radial
functions. For one common-scale summand, (20) recovers
\(L\geq D-1\).

The singleton/pair construction saturates (20). Each pair contributes one
noncospherical stereographic group, whereas an unpaired singleton uses
\(F(x)=x\), whose norm is constant. To see the first claim, inverse
stereographic projection sends a Euclidean sphere or hyperplane to a
hyperplane section of the ambient sphere, while the weighted product of
two full spheres affinely spans its entire \(\mathbb R^{2(q+1)}\) ambient
space. Thus
\(e=\lfloor k/2\rfloor\) and (20) becomes exactly

\[
 L\geq n+\lceil k/2\rceil.                                 \tag{22}
\]

This optimality statement applies to the multiscale chordal subclass (15),
not to arbitrary asymmetric Lorentz factors.

### 3.1 Positive block-group chordal decompositions

There is a broader exact optimality statement that allows overlapping
groups and splitting each block weight among several groups. Suppose

\[
 K=\sum_gK_g,\qquad
 K_g(x,z)=\sum_{a\in G_g}\mu_{ga}(1-x_a^Tz_a),             \tag{23}
\]

where \(\mu_{ga}>0\) and
\(\sum_{g:a\in G_g}\mu_{ga}=\lambda_a\). Assume each positive
block-additive kernel \(K_g\) has one common-scale chordal representation
of the form (15), using \(L_g\) scalar channels.

If \(|G_g|\geq2\), the functional inertia of \(K_g\) is
\((1,|G_g|(q+1))\), while one chordal summand has at most
\(L_g+1\) negative directions. Hence

\[
                  L_g\geq |G_g|(q+1)-1.                    \tag{24}
\]

If \(|G_g|=1\), the compact phase obstruction for the sphere gives the
stronger bound

\[
                  L_g\geq q+1.                             \tag{25}
\]

Let \(I=\sum_g|G_g|\) be the total block incidence and let \(t\) be the
number of nonsingleton groups. Every block is covered, so \(I\geq k\), and
\(t\leq\lfloor I/2\rfloor\). Summing (24)--(25) gives

\[
\begin{aligned}
 L&\geq(q+1)I-t\\
  &\geq(q+1)I-\lfloor I/2\rfloor\\
  &\geq(q+1)k-\lfloor k/2\rfloor
   =n+\lceil k/2\rceil.                                    \tag{26}
\end{aligned}
\]

Disjoint pairs and, for odd \(k\), one singleton attain (26). Thus the
paired construction is exactly optimal in this positive block-group
chordal class even when groups may overlap and weights may split. The
assumption that each chordal summand itself equals a positive
block-additive subkernel is essential; arbitrary chordal summands can have
cross-block terms that cancel only after summation.

## 4. One channel can depend on every coordinate block

The all-block stereographic construction also supplies a useful
counterexample to a tempting structural claim. In (19), choose a pole
\(p\in S^{D-1}\) such that every block \(p_a\) is nonzero and

\[
             (\|p_1\|,\ldots,\|p_k\|)
                 \ne(\sqrt{\lambda_1},\ldots,
                      \sqrt{\lambda_k}).                   \tag{27}
\]

Cauchy--Schwarz is then strict:

\[
 \max_{x\in M}p^TX(x)
   =\sum_a\sqrt{\lambda_a}\|p_a\|<1.                      \tag{28}
\]

Hence \(c(x)=1-p^TX(x)>0\) globally. Choose a generic orthonormal basis
of \(p^\perp\) and let

\[
 F(x)=\frac{X(x)-(p^TX(x))p}{c(x)}\in p^\perp.              \tag{29}
\]

The usual stereographic identity and (5)--(6) give a global
\(D-1\)-channel factorization. Because the denominator in (29) depends on
every block and a generic coordinate numerator has a nonzero projection
on every block, individual channel maps can depend nontrivially on all
\(k\) blocks.

Thus exact positivity and the absence of mixed terms in (1) do not force a
channel to be block-local or pair-local. What remains plausible is a
quantitative theorem charging additional channels for such global mixing,
but none is proved here.

## 5. Research boundary

The results above leave the unrestricted interval (2) intact. They show
precisely why several direct approaches cannot close it:

- diagonal rank and all finite jets are already saturated locally;
- phase topology sees only the sharp Euclidean embedding dimension
  \(n+1\);
- ordinary rank and inertia are strong only after controlling the number
  of chordal summands or their block-additive structure; and
- a single global channel can mix arbitrarily many coordinate blocks.

A stronger universal lower bound must therefore extract a global invariant
from the full two-point identity that controls arbitrary channel-dependent
amplitudes, or else a new construction must exploit those amplitudes to
beat the singleton/pair upper bound.

## Relation to the workbench

The global \(+1\) phase theorem and the paired construction are proved in
[*Joint smooth \(Q_3\) contact factorizations for products of balls*](2026-09-04-joint-product-ball-q3-contact-factorizations.md).
The present note supplies local no-go results and exact optimality theorems
for two structured subclasses; it does not change the full-lift caveats in
that note.

## Audit record

Three independent hostile audits checked the local stereographic constants,
the finite-sample strengthening, diagonal cone-positivity in the freezing
argument, the scope of the singleton/pair exact statement, functional
inertia and its cospherical refinement, the overlapping block-group count,
strict Cauchy--Schwarz in the generic-pole construction, and the distinction
between these subclasses and unrestricted asymmetric Lorentz factors. The
audits caught and corrected a missing weight normalization, an omitted
\(k\geq2\) hypothesis, and two initially overbroad subclass claims.
