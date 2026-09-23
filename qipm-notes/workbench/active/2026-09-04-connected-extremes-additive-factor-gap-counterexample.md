# Connected extreme points do not force an additive factor-dimension tax

Status: Proved and independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High; exact all-dimensional counterexample families

## Refuted conjecture

Let \(C\subset\mathbb R^N\) be a full-dimensional convex body whose extreme
point set is connected. A plausible strengthening of the absolute
dimension rigidity theorem was

\[
          \sum_{i=1}^L\dim K_i\stackrel{?}{\geq}N+L       \tag{1}
\]

for every irredundant factorization of the full slack operator through a
product of \(L\) nonzero proper cones. The conjecture is false even for a
proper affine lift, compact lifted feasible set, full Slater, and
indecomposable cone factors.

## Counterexample

Write the three-dimensional Lorentz cone as

\[
 Q_3=\{(t,x,y):t\geq\sqrt{x^2+y^2}\}.
\]

Use

\[
 K=Q_3\times\mathbb R_+\times\mathbb R_+,\qquad
 (M,L)=(5,3),                                           \tag{2}
\]

with ray coordinates \(u,v\). Intersect \(K\) with the two affine
equations

\[
                    t+u+v=1,\qquad u-v=2x+\frac32,       \tag{3}
\]

and project to \((t,x,y)\). Eliminating \(u,v\) gives the body

\[
 C=\left\{(t,x,y):
 \sqrt{x^2+y^2}\leq t,\quad
 t+2x\leq-\frac12,\quad
 t-2x\leq\frac52\right\}.                               \tag{4}
\]

The point

\[
                    p_0=\left(\frac45,-\frac34,0\right) \tag{5}
\]

satisfies all three inequalities strictly, and the corresponding
\(u=v=1/10\) are positive. Thus the lift has full Slater and \(C\) is
three-dimensional. It is compact: the two linear inequalities imply
\(t\leq1\) after addition, while the Lorentz inequality bounds \(x,y\).
Translate by \(p_0\) if the usual slack-operator normalization
\(0\in\operatorname{int}C\) is desired; translation changes none of the
claims below.  It also preserves a linear projection description on the
lifted slice: replace the output map \((t,x,y)\) by
\((t,x,y)-p_0(t+u+v)\), which equals \((t,x,y)-p_0\) under (3).

## Exact extreme set

The origin is infeasible in (4), so every Lorentz-boundary point has a
unique representation

\[
             (t,x,y)=\lambda(1,\cos\theta,\sin\theta),
             \qquad\lambda>0.                            \tag{6}
\]

Put \(c=\cos\theta\). The two affine inequalities become

\[
 \lambda(1+2c)\leq-\frac12,\qquad
 \lambda(1-2c)\leq\frac52.                               \tag{7}
\]

They are feasible exactly when \(c\leq-3/4\), in which case

\[
 \lambda_-(c)=\frac{1}{2(-1-2c)}
       \leq\lambda\leq
 \lambda_+(c)=\frac{5}{2(1-2c)}.                         \tag{8}
\]

Every extreme point of \(C\) lies on the Lorentz boundary and at one
endpoint of (8). Indeed:

- a point in the Lorentz interior with fewer than two active affine
  inequalities lies in a nontrivial feasible segment;
- if both affine inequalities are active, then
  \(t=1,x=-3/4\) and the feasible points form the segment
  \(\{(1,-3/4,y):|y|\leq\sqrt7/4\}\), whose only extreme endpoints lie on
  the Lorentz boundary; and
- a Lorentz-boundary point lies on an extreme ray of \(Q_3\), so any
  convex decomposition inside \(C\) remains on that ray. It is extreme
  exactly at an endpoint of the feasible ray interval (8).

Consequently

\[
 \operatorname{ext}C=
 \{\lambda_-(\cos\theta)(1,\cos\theta,\sin\theta):
       \cos\theta\leq-3/4\}
 \ \cup\
 \{\lambda_+(\cos\theta)(1,\cos\theta,\sin\theta):
       \cos\theta\leq-3/4\}.                             \tag{9}
\]

The direction set \(\{\theta:\cos\theta\leq-3/4\}\) is a closed connected
arc. At each of its two endpoints, \(\lambda_-=\lambda_+=1\). Thus the
two continuous arcs in (9) meet at both endpoints; the extreme point set
is connected (in fact, a simple closed curve).

## Irredundancy and the violated bound

All three factors in (2) are indecomposable: \(Q_3\) is a rank-two simple
Lorentz cone and a ray has no nontrivial product decomposition. Each
factor constraint is essential:

- dropping the \(v\geq0\) constraint drops
  \(t+2x\leq-1/2\) and admits the origin;
- dropping the \(u\geq0\) constraint drops
  \(t-2x\leq5/2\) and leaves the ray
  \(\lambda(1,-1,0)\), \(\lambda\geq1/2\), unbounded; and
- dropping the \(Q_3\) constraint leaves an unbounded intersection of two
  halfspaces.

Here “dropping a factor constraint” means replacing that factor cone by
its linear span while retaining the lifted variables and affine equations.
Thus the lift is irredundant in the concrete constraint sense that relaxing
any one factor membership changes its projection. By the proper cone
lift--slack-factorization theorem, it supplies a factorization of the full
slack operator of the translated body through all three factors. The
curved Lorentz boundary and each of the two planar caps have exposed
points, so the associated dual certificates use respectively the
\(Q_3\), \(u\)-ray, and \(v\)-ray factors; none is slack-invisible.
Explicitly, the two cap slacks are

\[
       \frac52-t+2x=2u,\qquad
       -\frac12-t-2x=2v,
\]

while a supporting functional at a relative-interior point of the curved
sheet has a nonzero \(Q_3^*\) component.

Here

\[
                         N=3,\qquad L=3,\qquad M=5,       \tag{10}
\]

whereas (1) predicts \(M\geq6\). This refutes the additive
\(N+L\) law.

### All-dimensional sharp family

The example is not confined to dimension three. For every \(n\geq3\), let

\[
 Q_n=\{(t,x_1,\ldots,x_{n-1}):t\geq\|x\|_2\}
\]

and impose (3) on
\(Q_n\times\mathbb R_+\times\mathbb R_+\), with \(x\) in (3) replaced by
\(x_1\). Projection to \((t,x)\in\mathbb R^n\) gives

\[
 C_n=\left\{(t,x):
 \|x\|_2\leq t,\quad
 t+2x_1\leq-\frac12,\quad
 t-2x_1\leq\frac52\right\}.                            \tag{10a}
\]

The same point \((4/5,-3/4,0,\ldots,0)\) proves full Slater, and the same
addition of the cap inequalities gives compactness. Write a nonzero
Lorentz-boundary point as \(\lambda(1,z)\), where
\(z\in S^{n-2}\). Its feasible interval is still (8), with \(c=z_1\),
and is nonempty exactly on the spherical cap

\[
             D_n=\{z\in S^{n-2}:z_1\leq-3/4\}
                  \cong B^{n-2}.                       \tag{10b}
\]

The two endpoint maps
\(z\mapsto\lambda_\pm(z_1)(1,z)\) embed two copies of \(D_n\). They meet
exactly on \(\partial D_n=\{z_1=-3/4\}\), because
\(\lambda_-=\lambda_+\) exactly there. The interior-point and extreme-ray
argument used above is dimension-independent; when both cap inequalities
are active, the remaining feasible set is the Euclidean ball

\[
 \{(1,-3/4,x_2,\ldots,x_{n-1}):
       x_2^2+\cdots+x_{n-1}^2\leq7/16\},
\]

whose only extreme points lie on the Lorentz boundary. Consequently

\[
              \operatorname{ext}C_n
                 \cong D_n\cup_{\partial D_n}D_n
                 \cong S^{n-2}.                        \tag{10c}
\]

All three factor constraints remain essential by the same witnesses
(free \(x_2,\ldots,x_{n-1}\) make the relaxation of \(Q_n\) unbounded).
Thus in every dimension \(n\geq3\) there is a full-Slater irredundant lift
with

\[
                    N=n,\qquad L=3,\qquad M=n+2=N+2,    \tag{10d}
\]

and a connected extreme-point manifold.

### Arbitrarily many factors

The separation also grows with the number of factors.  Fix \(s\geq2\),
\(p\geq2\), and \(a>0\), and use

\[
 K_{s,p}=Q_{s+1}\times\mathbb R_+^p,\qquad
 Q_{s+1}=\{(t,z):t\geq\|z\|_2\}.                       \tag{10e}
\]

Inside the normalized base impose one further equation,

\[
 t+\sum_{j=1}^p u_j=1,\qquad
 z_1+a\sum_{j=1}^p u_j=0.                              \tag{10f}
\]

Regard this compact slice itself, translated by a relative-interior point,
as a body \(C_{s,p}\) in its affine hull.  Its resource counts are

\[
 N=s+p-1,\qquad L=p+1,\qquad M=s+p+1=N+2.              \tag{10g}
\]

It has full relative Slater: choose
\(a/(a+1)<t_0<1\), set
\(z=(-a(1-t_0),0,\ldots,0)\), and distribute
\(1-t_0\) positively among the \(u_j\).  Compactness follows from the
first equation and cone nonnegativity.

The first equation cuts out the join of the Euclidean unit ball

\[
 D=\{(1,z,0):\|z\|_2\leq1\}
\]

and the \(p\) scalar vertices \(e_1,\ldots,e_p\).  Write
\(\omega\in S^{s-1}\), \(c=\omega_1\), and, for \(c<0\), put
\(\tau(c)=a/(a-c)\).  The exact extreme set of the second section is

\[
 \operatorname{ext}C_{s,p}
 =\{(1,\omega,0):\omega_1=0\}
 \ \cup\
 \bigcup_{j=1}^p
 \left\{\tau(c)(1,\omega,0)+(1-\tau(c))e_j:
                  \omega_1<0\right\}.                 \tag{10h}
\]

For completeness, let \(F\) be the minimal face of the normalized base
containing an extreme point of its hyperplane section.  Since
\(\operatorname{aff}F\) meets one hyperplane in a singleton,
\(\dim F\leq1\).  The base's vertices are the sphere
\(\{(1,\omega,0)\}\) and the \(e_j\).  Its relevant edges join a sphere
point to one \(e_j\); the section functional has value \(\omega_1\) on
the former and the common positive value \(a\) on the latter.  It
therefore meets exactly the edges displayed in (10h), together with the
sphere points where \(\omega_1=0\).

For each \(j\), the closure of its sheet in (10h) is a closed hemisphere,
and all \(p\) sheets meet along the common equator.  Their union is
connected.  Every factor is essential: relaxing the Lorentz constraint
makes \(z_2,\ldots,z_s\) unbounded, while relaxing the \(j\)-th ray
constraint permits the unbounded move
\((u_j,u_\ell)\mapsto(u_j-T,u_\ell+T)\) for any \(\ell\ne j\).
Each scalar inequality defines a genuine facet, and Lorentz supporting
rows expose the curved sheets, so all factors are slack-visible.

Consequently

\[
                 (N+L)-M=p-1=L-2,                     \tag{10i}
\]

which is unbounded.  Connected extreme points and factor irredundancy do
not yield any additive penalty beyond the sharp universal \(+2\).

### A ray-free arbitrary-factor family

The same unbounded separation needs no scalar cone factors. For every
\(s\geq2\) and \(L\geq2\), write the \(i\)-th copy of \(Q_{s+1}\) as

\[
 Q_{s+1}^{(i)}
   =\{(t_i,x_i,y_i):t_i\geq\sqrt{x_i^2+\|y_i\|_2^2}\},
 \qquad y_i\in\mathbb R^{s-1},
\]

and take the codimension-two slice

\[
 Z_{s,L}=\left\{z\in Q_{s+1}^L:
              \sum_{i=1}^Lt_i=1,\quad
              \sum_{i=1}^Lx_i=0\right\}.              \tag{10j}
\]

Identify its affine hull with \(\mathbb R^{(s+1)L-2}\). Then

\[
          N=(s+1)L-2,\qquad M=(s+1)L=N+2.             \tag{10k}
\]

The point \(t_i=1/L,\ x_i=0,\ y_i=0\) gives full relative Slater. The slice is
compact because \(0\leq t_i\leq1\) and
\(|x_i|,\|y_i\|_2\leq t_i\).

Here is an exact extreme-point description. Let
\(A(z)=(\sum_it_i,\sum_ix_i)\). For \(z\in Z_{s,L}\), let \(F(z)\) be the
minimal face of \(Q_{s+1}^L\) containing \(z\). Then

\[
 z\in\operatorname{ext}Z_{s,L}
 \quad\Longleftrightarrow\quad
 \ker A\cap\operatorname{span}F(z)=\{0\}.             \tag{10l}
\]

Indeed, a nonzero vector in the intersection gives a short feasible
two-sided segment through the relative-interior point \(z\) of \(F(z)\).
Conversely, the endpoints of any feasible segment with midpoint \(z\)
belong to \(F(z)\), and their difference lies in that intersection.

A nonzero Lorentz block is either interior, whose minimal-face span has
dimension \(s+1\), or lies on a boundary ray
\(t_i(1,c_i,w_i)\), where \(c_i^2+\|w_i\|_2^2=1\). An interior block
contributes a nonzero \(y_i\)-direction to the kernel in (10l).
Boundary-ray blocks
contribute the columns \((1,c_i)\) to \(A\). Thus an extreme point has
either

- one nonzero boundary-ray block with \(c_i=0\); or
- two nonzero boundary-ray blocks with \(c_ic_j<0\).

In the second case the positive weights are uniquely fixed by
\(t_i+t_j=1\) and \(t_ic_i+t_jc_j=0\). No point with three nonzero blocks
or an interior block is extreme.

This extreme set is path-connected. Denote its one-block points by
\(v_i^u\), where the \(i\)-th block is
\((1,0,u)\) for \(u\in S^{s-2}\). For any \(i\ne j\),
\(u,v\in S^{s-2}\), and \(0\leq r\leq1\), set all other blocks to zero and

\[
\begin{aligned}
 z_i(r)&=(1-r)\bigl(1,r,\sqrt{1-r^2}\,u\bigr),\\
 z_j(r)&=r\bigl(1,-(1-r),\sqrt{1-(1-r)^2}\,v\bigr).
\end{aligned}                                         \tag{10m}
\]

For \(0<r<1\) this is a two-block extreme point, and it joins
\(v_i^u\) to \(v_j^v\). Every two-block extreme point also joins
one of the \(v_i^u\): continuously move its positive cosine to zero
and use the unique positive weights above. Hence all extreme points lie in
one path component.

Every factor is essential and slack-visible. If the \(i\)-th Lorentz
membership is relaxed to its linear span, choose \(j\ne i\), put
\((t_i,x_i,y_i)=(-1,0,0)\), \((t_j,x_j,y_j)=(2,0,0)\), and set the other
blocks to zero. This belongs to the relaxed affine slice but not to
\(Z_{s,L}\). A nonzero dual Lorentz ray orthogonal to \(v_i^u\) gives a
supporting slack row using the \(i\)-th factor. Since every \(Q_{s+1}\) is
indecomposable, (10j) disproves any factor-additive dimension penalty even
when all factors are nonpolyhedral and indecomposable. For \(L\geq3\),

\[
                       (N+L)-M=L-2.                   \tag{10n}
\]

It also identifies the sharp slice-codimension statement for injective
lifts. A compact full-Slater injective slice of a product with at least
two nonzero factors cannot have codimension one and connected extreme set:
a bounded codimension-one slice is, after scaling, a normalized base. To
see this, write its hyperplane as \(\ell(z)=\beta\) and orient it so that
\(\beta>0\). Full Slater and boundedness rule out every nonzero
\(k\in K\) with \(\ell(k)\leq0\): equality gives a recession ray directly,
while strict inequality lets a positive combination with the Slater point
produce a nonzero recession direction in \(K\cap\ker\ell\). Hence
\(\ell\in\operatorname{int}K^*\). The extreme points of this normalized
base are the disjoint clopen union of the normalized extreme rays of the
factors. Thus its slice codimension is at least two, and (10j) attains
equality for every \(s,L\geq2\).

The face argument used in (10l) has a general product-cone form.  If
\[
 S=\{z\in K:Az=b\},\qquad K=\prod_{i=1}^L K_i,
\]
where \(A\) has rank \(q\), and \(F_i(z_i)\) is the minimal face of
\(K_i\) containing \(z_i\), then

\[
 z\in\operatorname{ext}S
 \quad\Longleftrightarrow\quad
 \ker A\cap\bigoplus_i\operatorname{span}F_i(z_i)=\{0\}.
                                                               \tag{10o}
\]

Consequently every extreme point obeys the activation ledger

\[
             \sum_i\dim\operatorname{span}F_i(z_i)\leq q.      \tag{10p}
\]

In particular, at most \(q\) factor coordinates are nonzero.  For real
PSD factors this specializes to
\(\sum_i r_i(r_i+1)/2\leq q\), and for complex Hermitian PSD factors to
\(\sum_i r_i^2\leq q\), where \(r_i=\operatorname{rank}z_i\).
For a Lorentz factor, a nonzero boundary block costs one unit and an
interior block costs the full factor dimension.  This is the familiar
Pataki face-dimension mechanism in a general product-cone form; its role
here is to turn slice codimension into an exact factor-activation resource.

The standard product Lorentz barrier also has an exact parameter on this
slice. Namely, restrict

\[
       \Phi(z)=-\sum_{i=1}^L
          \log(t_i^2-x_i^2-\|y_i\|_2^2)               \tag{10q}
\]

to the relative interior of \(Z_{s,L}\). Its exact self-concordant barrier
parameter, in the Hessian-gradient convention, is

\[
                         \nu_{\rm std}=2L-1.           \tag{10r}
\]

For the upper bound, let \(H=\nabla^2\Phi\), \(g=\nabla\Phi\), and let
\(a(z)=\sum_it_i\). Logarithmic homogeneity gives
\(H^{-1}g=-z\) and \(g^\mathsf TH^{-1}g=2L\). A direct one-block
calculation gives

\[
 a^\mathsf TH^{-1}a
   =\frac12\sum_i(t_i^2+x_i^2+\|y_i\|_2^2)
   \leq\sum_it_i^2\leq1.                              \tag{10s}
\]

The squared dual norm of \(g\) after restriction to \(\ker a\) is the
minimum of
\((g-\lambda a)^\mathsf TH^{-1}(g-\lambda a)\) over \(\lambda\), hence
equals
\[
 2L-\frac{(a^\mathsf TH^{-1}g)^2}{a^\mathsf TH^{-1}a}
 =2L-\frac1{a^\mathsf TH^{-1}a}\leq2L-1.
\]
Restriction to the smaller tangent space that also satisfies
\(\sum_i dx_i=0\) can only decrease this norm. Affine restriction preserves
self-concordance and the barrier property, proving the upper bound.

For the matching lower bound, take the segment from the Slater point
\(z_i^0=(1/L,0,0)\) to any one-block extreme point \(v_i^u\).
As its parameter \(\theta\uparrow1\), the determinant of block \(i\)
vanishes to order one and each of the other \(L-1\) determinants vanishes
to order two. Therefore
\[
       \Phi((1-\theta)z^0+\theta v_i^u)
          =-(2L-1)\log(1-\theta)+O(1).
\]
The directional gradient/Hessian quotient tends to \(2L-1\), so no
smaller parameter satisfies the Hessian-gradient inequality. This exact
value concerns the standard restricted product barrier (10q); it is not a
lower bound for arbitrary coupled barriers on \(Z_{s,L}\).

In fact the same value is optimal even among arbitrary coupled barriers.
Fix a unit vector \(e\in\mathbb R^{s-1}\) and take the linear section

\[
                    x_i=0,\qquad y_i=u_i e
                    \quad (i=1,\ldots,L).
\]

The second equation in (10j) is then automatic, and the remaining domain
is \(\sum_i t_i=1,\ t_i>|u_i|\). Under
\[
                 p_i=t_i+u_i,\qquad q_i=t_i-u_i,
\]
it is the relative interior of the scaled simplex
\[
              p_i,q_i\geq0,\qquad
              \sum_i(p_i+q_i)=2,
\]
of dimension \(2L-1\). Every simplex facet \(p_i=0\) or \(q_i=0\)
satisfies \(t_i=|u_i|\), so the relative boundary of this section lies in
\(\partial Z_{s,L}\). Consequently the restriction of every barrier on
\(Z_{s,L}\) remains a barrier on the simplex. The
Nesterov--Nemirovskii simple-vertex lower bound and (10r) give the exact
coupled value

\[
       \boxed{\nu_{\rm opt}(Z_{s,L})=2L-1}
       \qquad(s,L\geq2).                              \tag{10t}
\]

Here \(\nu_{\rm opt}\) ranges over arbitrary ordinary self-concordant
barriers, including coupled ones. Thus no coupled barrier improves the
standard product value.

This intrinsic lower bound also transfers to bounded-fiber extended
formulations. Let \(\widehat Z\) be a convex affine lift of \(Z_{s,L}\)
whose nonempty projection fibers are bounded, and let \(\widehat\Phi\) be
any \(\nu\)-self-concordant barrier on its relative interior. Exact partial
minimization,
\[
       \phi(z)=\inf\{\widehat\Phi(\widehat z):
                         \pi(\widehat z)=z\},
\]
is a \(\nu\)-self-concordant barrier on \(Z_{s,L}\). Therefore (10t)
implies the formulation lower bound
\[
                  \boxed{\nu_{\rm lift}\geq2L-1}.      \tag{10t''}
\]
This permits arbitrary auxiliary variables, cone products, and coupling
inside the lifted barrier. Bounded fibers are essential to the stated
projection theorem; no claim is made here for lifts with unbounded
certificate fibers.

There is an exact criterion for when an unbounded lift can first be
normalized without increasing its barrier parameter. Let \(D\) be any
closed line-free convex affine lift of a compact body \(C\), let
\(\pi(D)=C\), and put \(R=\operatorname{rec}D\). Compactness gives
\(R\subseteq\ker\pi\). If \(R\ne\{0\}\), choose a linear functional \(a\)
strictly positive on \(R\setminus\{0\}\), and define
\[
            m_a(x)=\min\{a(z):z\in D,\ \pi z=x\}.       \tag{10t''a}
\]
The minimum is attained: otherwise a minimizing sequence with no bounded
subsequence would yield a nonzero recession direction \(r\in R\) with
\(a(r)\leq0\). For a scalar \(M\), the section
\[
                       D_M=D\cap\{a=M\}                \tag{10t''b}
\]
projects onto all of \(C\) if and only if \(M\geq\sup_Cm_a\). Indeed, from
any fiber minimizer one can add a fixed nonzero \(r_0\in R\) to reach every
larger \(a\)-value. Moreover
\(\operatorname{rec}D_M=R\cap\ker a=\{0\}\), so this closed section is
bounded. Choosing \(M>\sup_Cm_a\) so that the hyperplane meets
\(\operatorname{ri}D\) (for example, also take \(M>a(z^0)\) for one
\(z^0\in\operatorname{ri}D\)), restriction of a \(\nu\)-barrier to \(D_M\),
followed by bounded-fiber partial minimization, produces a
\(\nu\)-barrier on \(C\). If \(R=\{0\}\), \(D\) itself is bounded and no
normalization is needed.

In particular, every closed line-free lift of a compact polytope admits
this barrier-preserving normalization. Choose one lift \(z_v\) above each
of its finitely many vertices. If \(x=\sum_v\lambda_vv\), then
\(\sum_v\lambda_vz_v\in D_x\), and hence
\[
               m_a(x)\leq\sum_v\lambda_va(z_v)
                       \leq\max_v a(z_v).              \tag{10t''c}
\]
Thus any intrinsic barrier lower bound for a polytope transfers through
arbitrary closed line-free affine lifts, even when their original fibers
are unbounded. The finiteness of the extreme set, rather than compactness
alone, supplies the missing uniform bound. In particular, if \(C\) is an
\(n\)-dimensional polytope with a simple vertex, the
Nesterov--Nemirovskii lower bound gives
\[
                    \boxed{\nu(\widehat\Phi)\geq n}.    \tag{10t''d}
\]
This holds for every SCB \(\widehat\Phi\) on every closed full-Slater
conic lift of \(C\), regardless of fiber boundedness or barrier coupling.
It is intrinsically
sharp by the \(n\)-parameter universal barrier. No exact-\(n\) assertion
is made for polytopes without a simple vertex.

That last qualification cannot be removed merely by selecting \(n\)
independent active facet normals at an arbitrary vertex. Proposition 2.3.6
of Nesterov--Nemirovskii assumes that the boundary point belongs
**exactly** to the \(k\) stated facets. This makes a neighborhood of the
point an orthant times a free subspace and is used to construct \(k\)
simultaneous boundary comparison points. Extra active facets can destroy
those points.

For example, at \(v=e_1\) of the three-dimensional cross-polytope
\[
                  |x_1|+|x_2|+|x_3|\leq1,             \tag{10t''e}
\]
the four active facet normals are
\((1,\pm1,\pm1)\). The first three normals with sign pairs
\((+,+),(+,-),(-,+)\) are independent, but the tangent direction
\[
                         d=(-1,-1,-1)
\]
satisfies the three selected linearized inequalities and violates the
omitted \((-,-)\) inequality:
\[
 \langle(1,1,1),d\rangle=-3,\quad
 \langle(1,1,-1),d\rangle=-1,\quad
 \langle(1,-1,1),d\rangle=-1,\quad
 \langle(1,-1,-1),d\rangle=1.                          \tag{10t''f}
\]
Thus the selected normals define a strict simplicial supercone of the
true tangent cone, not the local model needed in the proof.

The other screened lower bounds do not close this gap. Hildebrand's conic
active-facet refinement retains the same exact-incidence hypothesis and
concerns logarithmically homogeneous barriers. Güler--Tunçel's general
Carathéodory bound for a cone is
\(\nu\geq\min_{x\in\operatorname{int}K}\kappa_K(x)\); this can be far below
dimension for a nonsimplicial polyhedral cone (the central ray of a
centrally symmetric polytope cone is already a sum of two opposite vertex
rays). Lee--Yue supplies the matching \(n\)-parameter universal-barrier
upper bound on the body, not a conewise lower bound. Therefore
\(\nu_{\rm opt}(C)=n\) for every \(n\)-polytope remains unproved by these
sources and arguments. The rigorous lift theorem here remains (10t''d)
for polytopes having a simple vertex; whether all nonsimple polytopes obey
the same lower bound is left open.

In contrast, not every compact-body lift can be repaired by an affine
normalization that removes its recession directions while preserving the
whole projection. The following closed one-ray example gives the sharp
obstruction.

Assume \(s\geq3\), choose distinct
\(u_n\in\mathbb S^{s-2}\) with \(u_n\to u_*\), and let
\[
 v_n=((1,0,u_n),0,\ldots,0),\qquad
 v_*=((1,0,u_*),0,\ldots,0)
\]
be one-block extreme points of \(Z_{s,L}\). On \(Z_{s,L}\), put
\[
 \delta_n=1-\langle u_n,u_*\rangle,\qquad
 \ell_n(z)=n-\frac{n}{\delta_n}
                    \bigl(1-\langle u_n,y_1\rangle\bigr),
 \qquad f(z)=\max\{0,\sup_n\ell_n(z)\}.              \tag{10t'''}
\]
Here \(\langle u_n,y_1\rangle\leq\|y_1\|\leq t_1\leq1\), with
equality only at \(v_n\). Hence \(\ell_n(v_n)=n\) and
\(\ell_n(v_*)=0\). For each fixed \(z\ne v_*\), uniqueness of the
maximizer of \(\langle u_*,y_1\rangle\) gives
\(\langle u_n,y_1\rangle\to\langle u_*,y_1\rangle<1\), so
\(\ell_n(z)\to-\infty\). Thus the supremum in (10t''') is finite at
every point, while \(f(v_n)\geq n\). As a pointwise supremum of affine
functions, \(f\) is closed and convex.

The same example can be chosen semialgebraic, so the phenomenon is not a
countable or nondefinable artifact. In two coordinates of
\(\mathbb R^{s-1}\), set
\[
 u(\tau)=\left(\frac{1-\tau^2}{1+\tau^2},
                \frac{2\tau}{1+\tau^2},0,\ldots,0\right),\quad
 u_*=e_1,\quad
 \delta(\tau)=\frac{2\tau^2}{1+\tau^2}
\]
for \(0<\tau\leq1\), and replace (10t''') by
\[
 f_{\rm sa}(z)=\max\left\{0,
   \sup_{0<\tau\leq1}\left[
    \frac1\tau-\frac{1-\langle u(\tau),y_1\rangle}
                         {\tau\delta(\tau)}\right]\right\}.       \tag{10t'''a}
\]
The bracket is zero at \(v_*\), equals \(1/\tau\) at the exposed point
\(v_1^{u(\tau)}\), and tends to \(-\infty\) for every fixed
\(z\ne v_*\) as \(\tau\downarrow0\). Hence the same finiteness and
unboundedness proof applies. Its epigraph is described by a universal
quantifier over rational polynomial inequalities in \(\tau\), and is
therefore semialgebraic by quantifier elimination. The closed
homogenization is semialgebraic as well.

Consider the epigraph lift
\[
 D_f=\{(z,r):z\in Z_{s,L},\ r\geq f(z)\},
             \qquad \pi(z,r)=z.                     \tag{10t''''}
\]
It is closed, convex, has nonempty relative interior, and
\(\operatorname{rec}D_f=\{(0,r):r\geq0\}\). Let \(A\) be any affine
subspace such that \(D_f\cap A\) still projects onto all of \(Z_{s,L}\).
If the direction space of \(A\) omitted the vertical recession direction,
then the one-dimensional auxiliary coordinate and surjectivity would make
\(A\) the graph \(r=a+\langle b,z\rangle\) over
\(\operatorname{aff}Z_{s,L}\). This affine height is bounded on compact
\(Z_{s,L}\), contradicting \(a+\langle b,v_n\rangle\geq f(v_n)\geq n\).
Therefore every projection-preserving affine restriction retains the
vertical ray and has unbounded fibers.

This is genuinely a conic lift: homogenize \(D_f\) as
\[
 K_f=\operatorname{cl}\operatorname{cone}
       \{(1,z,r):(z,r)\in D_f\}.
\]
The cone is proper in its natural linear span, its slice at first coordinate
one is exactly \(D_f\), and that slice meets its relative interior. Thus
compactness of the projected body,
closedness, Slater regularity, properness of the lift cone, and even a
one-dimensional pointed recession cone do not imply the existence of a
bounded-fiber affine normalization. The elementary product lift
\(\operatorname{int}Z_{s,L}\times\mathbb R_{++}\) separately shows why
direct marginalization can fail: for the product barrier
\(\Phi(z)-\log r\), the fiber infimum is \(-\infty\). Neither example
disproves \(\nu_{\rm lift}\geq2L-1\) for all unbounded lifts; they rule out
the automatic-normalization and exact-marginalization routes, leaving that
broader lower bound open.

The corresponding ambient statement is exact as well. The homogenization
of \(Z_{s,L}\) is the balance cone

\[
 \widehat Z_{s,L}
   =\left\{z\in Q_{s+1}^L:\sum_i x_i=0\right\}.
\]

On the linear section \(x_i=0,\ y_i=u_i e\), the variables
\(p_i=t_i+u_i,\ q_i=t_i-u_i\) range independently over
\(\mathbb R_+^{2L}\). Its boundary is contained in the boundary of the
balance cone. Restriction therefore gives the orthant lower bound for
every ordinary, and hence every logarithmically homogeneous, coupled
barrier. The product Lorentz barrier attains it:

\[
       \boxed{\nu_{\rm opt}(\widehat Z_{s,L})=2L,\qquad
              \nu_{\rm opt}(Z_{s,L})=2L-1.}           \tag{10t'}
\]

Thus the balance equation that joins the projective extreme-ray components
reduces ambient dimension by one but does not reduce the optimal conic
barrier parameter; normalization removes exactly one unit.

A natural attempt to cancel one unit from (10t) fails already for
\(s=L=2\). Put
\[
 q_i=t_i^2-x_i^2-\|y_i\|_2^2
\]
and consider the boundary-order-canceling candidate
\[
             \Psi=-\log q_1-\log q_2+\log(q_1+q_2).    \tag{10u}
\]
At the interior point
\[
 t_1=\frac13,\quad t_2=\frac23,\quad x_1=x_2=0,\quad
 y_1=0,\quad y_2=\frac13,
\]
take the feasible direction that varies only \(y_2\). Direct
differentiation gives
\[
                    D^2\Psi[h,h]=\frac{13}{4},
       \qquad D^3\Psi[h,h,h]=25.
\]
Since \(25^2>4(13/4)^3\), the self-concordance inequality fails. Thus the
obvious coupled logarithmic cancellation cannot beat the exact optimum.

### Exact factor-cap hard instances

The construction closes an unrestricted factor-count frontier, not merely
the refuted additive conjecture. Fix integers \(d\geq3\) and \(L\geq2\),
take \(s=d-1\), and put

\[
                         N=dL-2.                       \tag{10v}
\]

For the full slack operator of \(Z_{d-1,L}\), among factorizations through
products of arbitrary nonzero proper cones of dimension at most \(d\),

\[
 L_{\min}=L=\frac{N+2}{d},\qquad
 M_{\min}=N+2=dL.                                     \tag{10w}
\]

Indeed, ordinary slack rank gives total dimension at least \(N+1\). A
single factor cannot attain it because \(d<N+1\). The
minimum-dimension rigidity and connected projective extreme-ray theorem
then exclude total dimension \(N+1\) for every multifactor
factorization, so \(M'\geq N+2\). Under the factor cap,
\(M'\leq dL'\), whence

\[
                 L'\geq\left\lceil\frac{N+2}{d}\right\rceil=L.
\]

The \(Q_d^L\) slice (10j) attains both equalities. This lower bound allows
arbitrary row splitting, arbitrary proper cone types under the dimension
cap, and discontinuous factor maps. For the attaining direct formulation,
the exact arbitrary coupled barrier parameters are \(2L\) on the balance
cone and \(2L-1\) on its normalized slice. The latter is an intrinsic
barrier statement for \(Z_{d-1,L}\); by (10t'') it also lower-bounds every
bounded-fiber extended formulation, but not lifts with unbounded fibers.

## What survives

The audited absolute-equality theorem remains sharp. Ordinary slack rank
always gives \(M\geq N+1\); if equality holds and
\(\operatorname{ext}C\) is connected, rigidity identifies the full product
cone with the homogenization cone of \(C\), and projective extreme-ray
connectivity forces \(L=1\). Thus for \(L\geq2\), \(M\geq N+2\).
The families above attain that surviving bound for every \(L\geq2\):

\[
                              M=N+2.                     \tag{11}
\]

The failure mechanism is an extra affine slice equation.  The following
restricted positive statement makes that precise.

**Proposition (one normalized base).**  Let
\(K=\prod_{i=1}^L K_i\), where every \(K_i\) is a nonzero proper cone of
dimension \(m_i\).  Choose \(\ell_i\in\operatorname{int}K_i^*\), put

\[
 B=\left\{z\in K:\sum_i\ell_i(z_i)=1\right\},
 \qquad C=\pi(B),                                      \tag{12}
\]

and suppose \(C\) has affine dimension \(N\).  If
\(\operatorname{ext}C\) is connected, then

\[
                         \sum_i m_i\geq N+L.            \tag{13}
\]

Indeed, the compact factor bases
\(B_i=\{z_i\in K_i:\ell_i(z_i)=1\}\) have images \(C_i\) satisfying

\[
 C=\operatorname{conv}\!\left(\bigcup_i C_i\right),
 \qquad \dim\operatorname{aff}C_i\leq m_i-1.           \tag{14}
\]

Every extreme point of this convex hull belongs to at least one \(C_i\).
The nonempty closed sets
\(E_i=\operatorname{ext}C\cap C_i\) therefore cover
\(\operatorname{ext}C\).  Their intersection graph is connected: a graph
separation would partition the connected extreme set into two disjoint
nonempty finite unions of relatively closed sets.  Along a spanning tree,
successive affine hulls intersect.  Hence, writing \(I\) for the indices
with \(E_i\ne\varnothing\),

\[
 N=\dim\operatorname{aff}(\operatorname{ext}C)
   \leq\sum_{i\in I}\dim\operatorname{aff}E_i
   \leq\sum_{i\in I}(m_i-1).                           \tag{15}
\]

Each unused nonzero cone has \(m_i\geq1\), and (13) follows.  Thus (1) is
valid for a linear image of one normalized product-cone base, without an
irredundancy assumption.  Equation (3) imposes a second coupling: its
section creates new extreme points with several factor coordinates active,
defeating the convex-hull cover argument.  Any broader additive theorem
therefore needs a restriction on slice codimension, factor activation, or
contact-sheet regularity; cone irredundancy and connected extreme points
alone do not suffice.

## Literature boundary

The implication from the proper lift (2)--(3) to a full slack
factorization is the classical theorem of Gouveia, Parrilo, and Thomas,
[*Lifts of Convex Sets and Cone
Factorizations*](https://optimization-online.org/2011/11/3249/).
Saunderson's
[*Limitations on the Expressive Power of Convex Cones without Long Chains
of Faces*](https://arxiv.org/abs/1902.06401) proves different product-cone
lift obstructions from neighborliness and face-chain length.
The real-PSD specialization of (10p) is the classical rank bound of
Pataki, [*On the Rank of Extreme Matrices in Semidefinite Programs and the
Multiplicity of Optimal
Eigenvalues*](https://doi.org/10.1287/moor.23.2.339); (10o)--(10p) only
records its elementary minimal-face proof for arbitrary product cones.
More directly, Henrion, Kružík, and Weis,
[*Extreme Points and Faces in the Moment
Problem*](https://arxiv.org/abs/2606.21391), Theorem 2.6, characterize
extreme points of an affinely constrained convex set by injectivity of the
constraint map on the smallest face containing the point.  In the present
finite-dimensional singleton-fiber setting this is the same general
principle as (10o); thus no novelty claim should be made for (10o) itself.
Their paper does not specialize the criterion to the product-Lorentz slice,
derive the exact one-/two-block classification or its topology, or combine
it with the barrier and factor-cap statements below.  Dubins,
[*On Extreme Points of Convex
Sets*](https://doi.org/10.1016/S0022-247X(62)80007-9), proves that an extreme
point of a codimension-\(m\) affine section of a linearly bounded, linearly
closed convex set is a convex combination of at most \(m+1\) extreme points.
Applied after normalization, his theorem already explains why an extreme
point of (10j) uses at most two normalized product-cone extreme rays.  It
does not give their exact balancing condition, the connected gluing, or the
sharp codimension-two obstruction.
The simplex lower bound in (10t) is Nesterov--Nemirovskii,
*Interior-Point Polynomial Algorithms in Convex Programming*,
Proposition 2.3.6; it is also quoted explicitly in Lee and Yue,
[*Universal Barrier is
\(n\)-Self-Concordant*](https://arxiv.org/abs/1809.03011), Remark 2.
The bounded-fiber projection step (10t'') is exact partial minimization as
proved in Robert Chares, *Cones and Interior-Point Algorithms for
Structured Convex Optimization Involving Powers and Exponentials*
(PhD thesis, UCLouvain, 2009), Theorem 5.2.1.  Chares explicitly assumes
bounded interior fibers and proves that the marginal retains the same
\(\nu\); his theorem extends the more special partial-minimization result
in Nesterov,
[*Parabolic Target Space and Primal--Dual Interior-Point
Methods*](https://doi.org/10.1016/j.dam.2007.05.002), Theorem 3.
Thus the transfer mechanism and the need for a fiber-attainment hypothesis
are prior art.  The targeted screen did not locate an earlier
extended-formulation lower bound obtained by combining this theorem with
an exact intrinsic barrier optimum for the projected body; (10t'') is best
labeled a new corollary for this family, not a new preservation theorem.
The normalization criterion (10t''a)--(10t''c) uses only elementary
recession geometry before invoking the same Chares theorem. Classical
polyhedral extension-complexity papers commonly define an extension of a
polytope to be another **polytope**, and slack-factorization constructions
can supply bounded extensions. That is nearby normalization practice, but
it does not transport a specified coupled self-concordant barrier from a
given unbounded conic lift. Gouveia--Parrilo--Thomas likewise characterize
proper cone lifts and slack factorizations without proving monotonicity of
the barrier parameter for an arbitrary barrier placed on the lifted slice.

The intrinsic endpoint is fully prior art. Nesterov--Nemirovskii,
Proposition 2.3.6, gives \(\nu\geq n\) at an \(n\)-dimensional simple
vertex. Lee and Yue,
[*Universal Barrier is
\(n\)-Self-Concordant*](https://arxiv.org/abs/1809.03011), Theorem 2 and
Remark 2, prove the matching universal-barrier upper bound on every proper
\(n\)-dimensional convex domain and explicitly restate the simple-vertex
lower bound. Thus neither endpoint of (10t''d) is new.

A targeted search of self-concordant-barrier projection, partial
minimization, and polyhedral/conic extended-formulation sources did not
locate the intervening lift-invariant statement: every SCB on every closed,
full-Slater, line-free conic lift of such a polytope has \(\nu\geq n\),
even with unbounded fibers and a coupled barrier. The safe label is
**candidate general lift-invariant corollary assembled from classical
recession geometry, known bounded-fiber marginalization, and the classical
simple-vertex lower bound**. It is not a new partial-minimization theorem,
and priority still requires specialist review.

The simple-vertex qualification cannot be removed by merely choosing
\(n\) independent normals from a nonsimple vertex. The primary wording of
Nesterov--Nemirovskii Proposition 2.3.6 requires the point to belong
**exactly** to the stated facets. Hildebrand's Theorem 6.1 retains exact
incidence and additionally concerns logarithmically homogeneous cone
barriers. Güler and Tunçel,
[*Characterization of the Barrier Parameter of Homogeneous Convex
Cones*](https://doi.org/10.1007/BF01584844), Proposition 4.1, give the
general cone bound
\(\nu\geq\min_{x\in\operatorname{int}K}\kappa_K(x)\). For a cone over a
centrally symmetric nonsimple polytope, the central interior ray is a sum
of two opposite vertex rays, so this bound can be only two. Their exact
rank theorem requires homogeneity. The cross-polytope calculation
(10t''e)--(10t''f) makes the local obstruction explicit. The screen found
no primary result proving \(\nu_{\rm opt}=n\) for every nonsimple
\(n\)-polytope, so that possible strengthening remains open.

The epigraph construction (10t''')--(10t'''') is elementary. It exploits
the fact that a finite closed convex function on a compact convex domain
need not be bounded above when it is allowed to lose continuity at the
domain boundary. It is not a counterexample to an abstract monotonicity
theorem for optimal barrier parameters under unbounded lifts. Rather, it
is a counterexample to the stronger geometric premise that closed compact
projections automatically possess a projection-preserving affine section
transverse to recession; it also shows why Chares's bounded-fiber
hypothesis cannot simply be manufactured by such a section.
The construction, its all-dimensional extension, and the
connected-extreme-set obstruction are elementary.
A targeted search of cone-lift, factorization, and product-cone obstruction
sources found no statement of either this \(M=N+2\) family or Proposition
(12)--(15). This is evidence rather than a proof of novelty. No novelty
claim is made for the primitive Lorentz or ray cones.
A separate targeted screen of SOCP barrier and affine-section sources found
the standard additive product-cone barrier theory and Hildebrand's
[*A Lower Bound on the Optimal Self-Concordance Parameter of Convex
Cones*](https://optimization-online.org/wp-content/uploads/2011/06/3068.pdf),
which develops projective cross-ratio lower bounds for logarithmically
homogeneous barriers and recovers the Nesterov--Nemirovskii polyhedral
bound.  It did not locate the exact arbitrary-barrier calculation for the
bounded slices (10j).  The lower-bound device in (10t) is classical; the
apparently unlocated part is the boundary-inheriting simplex section
together with the matching restricted product-Lorentz upper bound.

For the capped formulation claim, Fawzi and Parrilo,
[*Exponential Lower Bounds on Fixed-Size PSD Rank and Semidefinite Extension
Complexity*](https://arxiv.org/abs/1311.2571), prove factor-count lower
bounds for products of fixed-size PSD cones on a hard polytope family.
Averkov,
[*Optimal Size of Linear Matrix Inequalities in Semidefinite Approaches to
Polynomial Optimization*](https://arxiv.org/abs/1806.08656), studies the
minimum permitted PSD block order while allowing finitely many blocks, and
Saunderson's cited theorem treats arbitrary factor cones through bounded
face-chain length.  These are close in resource language but do not state
(10w): an exact simultaneous factor-count and total-dimension frontier for
one explicit family when every nonzero proper factor cone of dimension at
most \(d\) is allowed.  The safe label is therefore **candidate elementary
synthesis/counterexample, not a new extremality criterion or a new simplex
barrier lower bound**.  The targeted screen is evidence only and is not an
exhaustive priority determination.

## Audit targets

1. Re-eliminate \(u,v\), check Slater, boundedness, and full dimension.
2. Verify the feasible ray interval (8) and the complete extreme-point
   characterization (9), especially exclusion of Lorentz-interior points.
3. Check connectedness at both arc endpoints.
4. Verify each factor is genuinely essential and that proper-lift
   factorization uses all three factors.
5. Confirm that (10) refutes \(M\geq N+L\) but attains the surviving
   \(M\geq N+2\) bound.
6. Check the normalized-base proposition, especially the finite closed-cover
   intersection graph and the affine-span count in (15).
7. Check the all-dimensional extension (10a)--(10d), including the
   double-of-a-ball description of its extreme set.
8. Check the join-section family (10e)--(10i), including its exact sheets,
   factor essentiality, and unbounded deficit.
9. Check the ray-free family (10j)--(10n), especially criterion (10l),
   path-connectedness, and the sharp codimension-two statement.
10. Check the general activation criterion and face-dimension ledger
    (10o)--(10p), including the real and complex PSD specializations.
11. Check the exact restricted standard-barrier parameter (10q)--(10s),
    including the Hessian projection and determinant orders.
12. Check the arbitrary-barrier equality (10t), especially the simplex
    section, boundary inheritance, and simple-vertex lower-bound scope.
13. Check the exact arbitrary coupled ambient balance-cone parameter
    (10t'), including the orthant section.
14. Check the bounded-fiber partial-minimization transfer (10t'').
15. Check the exact normalization criterion (10t''a)--(10t''c),
    especially attainment, the relative-interior condition for barrier
    restriction, and the arbitrary-lift polytope corollary.
16. Check the nonsimple-vertex limitation (10t''e)--(10t''f), including
    the exact hypothesis of Nesterov--Nemirovskii Proposition 2.3.6 and
    the cross-polytope tangent arithmetic.
17. Check the unbounded-lift normalization obstruction
    (10t''')--(10t''''), especially pointwise finiteness of \(f\), the
    exact recession cone, the affine-graph argument, and properness of the
    homogenized cone.
18. Verify the exact derivative counterexample (10u) to the natural
    boundary-order-canceling barrier candidate.
19. Check the exact arbitrary-cone factor-cap frontier (10v)--(10w) and
    its separation from the intrinsic slice-barrier statement.

## Independent audit record

An independent hostile audit re-eliminated the ray coordinates, checked the
strict Slater point, boundedness, and the complete extreme-point
classification. In particular, a Lorentz-interior point with both affine
constraints active lies in the displayed cap-intersection segment, and a
Lorentz-boundary point is extreme precisely at an endpoint of its feasible
ray interval. The two endpoint arcs meet only at their two common endpoints,
so their union is a simple closed curve. The audit also checked each factor
constraint under the explicit relaxation convention above, the three
slack-visible exposing rows, and the connected-cover affine-dimension proof
of (13)--(15). No substantive defect was found.

An independent extension audit also checked (10a)--(10d). The same strict
Slater point works in every dimension; adding the two cap inequalities
gives \(t\leq1\), and the Lorentz inequality then bounds every output
coordinate. On each nonzero Lorentz ray, elimination gives exactly the
interval (8), nonempty precisely for \(z_1\leq-3/4\). Its two endpoint
maps are embeddings of the closed cap \(D_n\cong B^{n-2}\), and they meet
exactly at \(z_1=-3/4\), where the endpoints coincide. Lorentz-interior
points with both cap equations active form the displayed Euclidean ball,
whose extreme points are exactly its Lorentz-boundary sphere; points with
fewer active cap equations admit a feasible segment. Thus no extreme
points are omitted and the double is \(S^{n-2}\). Finally, the same
explicit relaxations prove all three factors essential: the extra
coordinates only strengthen the unboundedness witness when the Lorentz
constraint is removed. No defect was found.

A further hostile audit checked the arbitrary-factor join family
(10e)--(10i). The two independent equations give the displayed dimension,
the Slater interval is nonempty, and normalization makes the slice compact.
The normalized base is the join of a Euclidean ball and a simplex. The
minimal-face criterion leaves exactly the equatorial ball vertices and
the ball--simplex edges that cross the second hyperplane, yielding (10h).
Each sheet closes to a hemisphere and all sheets share their equator.
The constraint-relaxation witnesses preserve both equations, and each
factor has a genuine exposing slack row. Thus the unbounded deficit is
correct.

An independent audit also checked the stronger ray-free family
(10j)--(10n). The minimal faces of \(Q_{s+1}\) have span dimensions
\(0,1,s+1\);
the two slice equations act on a boundary ray through the column
\((1,c_i)\), while any full-cone face contains an invisible \(y_i\)
direction. This proves (10l) and the stated one- and two-block
classification. Formula (10m) is feasible and extreme in its open
parameter interval and connects all one-block points; varying one cosine
to zero connects every two-block point to them. Slater, compactness,
dimension, indecomposability, factor relaxation, and single-factor
supporting rows all pass. Finally, boundedness turns every codimension-one
full-Slater slice into a normalized base, whose factor-supported extreme
rays are disconnected for \(L\geq2\). Hence codimension two is sharp.

The general activation lemma (10o)--(10p) passed a separate hostile audit.
Every point lies in the relative interior of its minimal product face, so a
two-sided kernel direction is equivalent to nonextremality; conversely,
the endpoints of a midpoint decomposition lie in that face.  Thus \(A\)
is injective on the direct-sum face span and its rank bounds the sum of the
face dimensions.  The active-factor, real and complex PSD, and Lorentz
specializations all have the stated exact face costs.  No defect was found.

A separate independent audit checked the exact standard-barrier calculation
(10q)--(10s).  Direct inversion of one Lorentz Hessian gives
\((H_i^{-1})_{t_it_i}=(t_i^2+x_i^2+\|y_i\|_2^2)/2\);
logarithmic homogeneity and
inverse-metric projection therefore give the stated \(2L-1\) upper bound,
and the second slice equation can only decrease the norm.  On the chord to
\(v_i^u\), one determinant has first-order and the remaining
\(L-1\) determinants have second-order zeros, so the directional
gradient/Hessian quotient tends exactly to \(2L-1\).  The scope restriction
to the standard product barrier is necessary.  No defect was found.

The arbitrary-barrier equality (10t) also passed independent audit. Fixing
\(x_i=0\) and \(y_i=u_i e\), then setting
\(p_i=t_i+u_i,\ q_i=t_i-u_i\), identifies the section exactly with a
scaled \((2L-1)\)-simplex. Every simplex facet is a Lorentz-boundary point,
so restricting any barrier preserves the barrier property. A simplex
vertex is simple with exactly \(2L-1\) independent active facets; the
Nesterov--Nemirovskii simple-vertex lower bound applies. Together with the
audited standard-barrier upper, this proves (10t). No defect was found.

The ambient equality in (10t') passed independent audit. On
\(x_i=0,\ y_i=u_i e\), the balance equation is automatic and the
invertible coordinates \(p_i=t_i+u_i,\ q_i=t_i-u_i\) identify the cone
section with all of \(\mathbb R_+^{2L}\). Its relative boundary lies in
the balance-cone boundary, so every coupled barrier restricts to an
orthant barrier and has parameter at least \(2L\). The restricted product
Lorentz barrier supplies the matching upper bound. Normalizing
\(\sum_it_i=1\) then gives the separately audited \(2L-1\) body value.
No defect was found.

The bounded-fiber transfer (10t'') also passed independent audit against
Chares's exact partial-minimization theorem.  Bounded nonempty fibers give
an attained interior minimizer; stationarity, the Schur-complement Hessian,
and the envelope identity preserve ordinary self-concordance and the same
gradient parameter, while the theorem supplies barrier divergence.  Hence
the exact intrinsic lower transfers to arbitrary bounded-fiber affine
lifts.  For the trivial unbounded product lift, the displayed
\(-\log r\) term makes the fiber infimum \(-\infty\), so the note correctly
leaves arbitrary unbounded fibers open rather than reversing the
projection theorem.  No defect was found.

The normalization criterion (10t''a)--(10t''d) passed hostile audit.
Because the recession cone is closed and pointed, a functional strictly
positive on its nonzero part is coercive on every closed fiber; hence the
minimum in (10t''a) is finite and attained. A fixed nonzero recession
direction raises every fiber minimizer to any prescribed larger
\(a\)-level, proving the exact covering criterion. The level section has
zero recession cone and is therefore bounded. If its level lies above the
height of one relative-interior point, translating that point along the
same recession direction shows that the section meets \(\operatorname{ri}D\);
affine restriction and bounded-fiber partial minimization then preserve
the barrier parameter. For a polytope, convex combinations of finitely
many chosen vertex lifts uniformly bound every \(m_a(x)\), so the argument
applies to every closed line-free lift. The simple-vertex intrinsic lower
bound then transfers exactly as stated. No defect was found.

The automatic-normalization obstruction (10t''')--(10t'''') passed a
separate hostile audit.  For each fixed \(z\ne v_*\), the strict inequality
\(\langle u_*,y_1\rangle<1\), convergence \(u_n\to u_*\), and
\(\delta_n\downarrow0\) force \(\ell_n(z)\to-\infty\); at \(v_*\), every
\(\ell_n\) is zero.  Hence the supremum is finite pointwise, while its
affine-supremum epigraph is closed and convex and \(f(v_n)\ge n\).  Compactness
of the base forces every recession direction of \(D_f\) to be vertical,
and upward closure gives exactly the stated ray.  After intersecting an
arbitrary candidate affine section with
\(\operatorname{aff}Z_{s,L}\times\mathbb R\), omission of the vertical
direction makes its projection an affine isomorphism and therefore makes
the section the graph of a bounded affine function on \(Z_{s,L}\), which
cannot dominate \(f(v_n)\).  Finally, standard closed homogenization adds
precisely the recession ray at homogenizing coordinate zero; it is pointed,
full-dimensional in its natural span, and has the claimed unit slice and
relative Slater point.  No defect was found.

The semialgebraic strengthening (10t'''a) also passed audit. Since
\(\tau\delta(\tau)=2\tau^3/(1+\tau^2)>0\), the displayed bracket is affine
in \(z\) for fixed \(\tau\). It is continuous on every interval bounded
away from zero, while for fixed \(z\ne v_*\) its negative
order-\(\tau^{-3}\) term dominates the positive \(\tau^{-1}\) term near
zero; at \(v_*\) it is identically zero. Thus the supremum is finite
pointwise, convex and closed, but takes values at least \(1/\tau\) on the
corresponding exposed points. After multiplying only by the positive
rational denominators, membership in its epigraph is a first-order formula
over the reals with one universally quantified \(\tau\); quantifier
elimination makes the epigraph semialgebraic. Semialgebraic sets remain
semialgebraic under conic images and closure, so the closed homogenization
has the claimed definability. No defect was found.

The candidate-barrier counterexample (10u) also passed exact arithmetic
audit. At the displayed point \(q_1=1/9\), \(q_2=1/3\), and along the
displayed direction \(q_2'=-2/3,\ q_2''=-2\). Direct chain-rule evaluation
gives \(D^2\Psi=13/4\) and \(D^3\Psi=25\), while
\(4(13/4)^3=2197/16<625\). Hence the standard self-concordance inequality
fails, not merely its barrier-parameter condition.

The arbitrary-cone cap frontier (10v)--(10w) passed hostile audit. Slack
rank gives \(M'\geq N+1\); the strict cap rules out one factor of that
dimension, while connected-extreme minimum-dimension rigidity rules out
every multifactor equality realization. Thus \(M'\geq N+2=dL\), and
\(M'\leq dL'\) forces \(L'\geq L\). The displayed Lorentz product attains
both bounds. No row-integrity, continuity, or cone-regularity hypothesis
enters this argument. The direct-slice barrier statement is correctly
separated from barriers on arbitrary extended formulations.

A second independent audit checked the combined capped and intrinsic
statement, including the edge cases \(d=3\) and \(L=2\).  The full-slack
rank and equality-rigidity argument permits arbitrary splitting of every
slack row and uses no continuity of either factor map.  For the direct
formulation it rederived the ambient, restricted-standard, and intrinsic
barrier ledger
\[
                    2L,\qquad 2L-1,\qquad 2L-1.
\]
In particular, for \(s=d-1\geq2\), fixing \(x_i=0\) and one common unit
direction in the nonempty \(y_i\)-space gives a closed scaled
\((2L-1)\)-simplex section.  Each of its facets lies in the relative
boundary of \(Z_{d-1,L}\), so every barrier restricts to a simplex barrier
and the simple-vertex lower bound applies.  This closes the earlier
one-unit intrinsic gap; no qualification beyond direct-slice versus
fiber-extended barriers is needed.

The nonsimple-vertex scope (10t''e)--(10t''f) passed independent hostile
audit. At \(e_1\) of the three-dimensional cross-polytope, the four listed
facet normals are exactly the active ones, the selected three are
independent, and \(d=(-1,-1,-1)\) satisfies their tangent inequalities
strictly while violating the fourth. Thus independent-normal rank alone
does not reproduce the tangent cone required by
Nesterov--Nemirovskii Proposition 2.3.6. The audit also checked that the
quoted Hildebrand and Güler--Tunçel bounds do not close the arbitrary-SCB
nonsimple case. The note correctly records that extension as open rather
than false.
