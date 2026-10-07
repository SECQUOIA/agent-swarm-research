# Prewriting review: convex-quartic SOS length and rational descent

Date: 2026-10-05. This is an internal mathematical review. No literature
research, experiment, script rerun, project-wide check, or CI inspection
was performed.

The descent criterion is correct as stated. Its proof is complete once
the real SOS-length lower bound is supplied; the lower bound also passes
reconstruction. No mathematical repair or counterexample is needed.
The manuscript should include the proofs below, keep rational and real
vanishing spaces distinct, and avoid extending the cyclic stationary-space
calculations beyond their recorded dimensions.

The reviewed sources are
[the descent criterion](../../../research-20260927/convex-quartic-descent-criterion.md),
[the SOS-length theorem](../../../research-20260927/convex-quartic-minimal-sos-length.md),
[its earlier review](../../../research-20260927/convex-quartic-minimal-sos-length-fresh-review.md),
[the tower quadratic space](../../../research-20260927/tower-quadratic-vanishing-space.md),
[the tower stationary space](../../../research-20260927/tower-quartic-stationary-space.md),
[its earlier review](../../../research-20260927/tower-quartic-stationary-space-review.md),
[the cyclic construction](../../../research-20260927/cyclic-quartic-exponential-degree.md),
[the rational square compression](../../../research-20260927/cyclic-quartic-square-compression.md),
[its rank-one review](../../../research-20260927/cyclic-quartic-rank-one-compression-review.md),
[the second compression review](../../../research-20260927/cyclic-sos-compression-review.md),
[the cyclic quadratic-space draft](../../../research-20260927/cyclic-quadratic-vanishing-space.md),
and the retained
[cyclic stationary-space checker](../../../research-20260927/check_cyclic_quartic_stationary_space.py).
The earlier reviews were read as evidence; their conclusions were not
substituted for the arguments below.

For a real point \(p\in\mathbb R^n\), define
\[
\begin{aligned}
 I_2^{\mathbb Q}(p)
   &=\{q\in\mathbb Q[X]_{\leq2}:q(p)=0\},\\
 J_4^{\mathbb Q}(p)
   &=\{F\in\mathbb Q[X]_{\leq4}:F(p)=0,\ \nabla F(p)=0\},\\
 W^{\mathbb Q}(p)
   &=\operatorname{span}_{\mathbb Q}
       \{q r:q,r\in I_2^{\mathbb Q}(p)\}.
\end{aligned}
\]
The product rule gives \(W^{\mathbb Q}(p)\subseteq J_4^{\mathbb Q}(p)\).
Neither algebraicity of \(p\) nor a field representation of its coordinates
is required for the descent theorem.

These rational spaces cannot be replaced silently by the corresponding
real spaces. The full real quadratic vanishing space is
\[
 I_2^{\mathbb R}(p)=\{q\in\mathbb R[X]_{\leq2}:q(p)=0\},
 \qquad
 \dim_{\mathbb R}I_2^{\mathbb R}(p)=\binom{n+2}{2}-1.
\]
The real coefficient span of a rational basis of
\(I_2^{\mathbb Q}(p)\) can be much smaller. Likewise, the full real
stationary space has dimension \(\binom{n+4}{4}-(n+1)\): constants
and the affine polynomials \(X_j-p_j\) show that the value and gradient
conditions are independent over \(\mathbb R\). Their rational kernels
need not have these dimensions. The tower example below explicitly uses
this distinction.

**Theorem 1 (real SOS-length bound).** Let
\(F\in\mathbb R[X_1,\ldots,X_n]\), with \(n\geq1\), be globally
convex of degree exactly four. Suppose
\[
 F=\sum_{i=1}^m q_i^2,\qquad F(p)=0,\qquad
 \nabla^2F(p)\succ0,
\]
where the factors have arbitrary real coefficients. Then \(m\geq n+1\).
The bound is attained for every \(n\) by
\(\|X\|^4+\|X\|^2\).

**Proof.** Every factor has degree at most two. Otherwise, the sum of
the squares of the highest homogeneous parts of the factors of maximum
degree would be a nonzero homogeneous polynomial of degree greater than
four. Such a sum cannot vanish identically over \(\mathbb R\).

Let \(q=(q_1,\ldots,q_m)\). All its components vanish at \(p\), and
\[
 \nabla^2F(p)=2Dq(p)^{\mathsf T}Dq(p).
\]
Therefore \(m\geq n\). If another zero existed, convexity and
nonnegativity would force \(F\) to vanish on the segment joining that
zero to \(p\). The second directional derivative at \(p\) along
this nonzero segment would be zero, contradicting positive definiteness.
Thus \(p\) is the unique zero.

Suppose \(m=n\). Then \(q:\mathbb R^n\to\mathbb R^n\) is a
quadratic polynomial map with a unique zero and nonsingular derivative
there. Write \(q=q_2+q_1+q_0\) by homogeneous degree, and put
\[
 H(x)=\|q_2(x)\|^2,\qquad K=\{v:H(v)=0\}.
\]
The function \(H\) is convex, as the pointwise limit of
\(t^{-4}F(tx)\) as \(t\to+\infty\). It is nonnegative and
homogeneous of even degree. Its zero set is convex and closed under
all real scalar multiples, hence is a linear subspace.

For \(v\in K\), \(s\in\mathbb R\), and \(0<\eta<1\),
convexity gives
\[
 H(x+sv)
 \leq(1-\eta)H\!\left(\frac{x}{1-\eta}\right)
       +\eta H\!\left(\frac{sv}{\eta}\right)
 =(1-\eta)^{-3}H(x).
\]
Letting \(\eta\downarrow0\), then applying the resulting inequality
to the displacement \(-sv\), proves \(H(x+sv)=H(x)\).
Let \(B_2\) be the symmetric vector-valued bilinear map with
\(q_2(x)=B_2(x,x)\). Since \(q_2(v)=0\),
\[
 q_2(x+sv)=q_2(x)+2sB_2(x,v).
\]
The coefficient of \(s^2\) in its constant squared norm is
\(4\|B_2(x,v)\|^2\). Therefore \(B_2(x,v)=0\): each
component of \(q_2\) is independent of the directions in \(K\).

Choose orthogonal coordinates \(x=(w,v)\), with \(v\in K\)
and \(w\in K^\perp\), and write \(\ell=\dim K\),
\(r=n-\ell\). Then
\[
 q(w,v)=q_2(w)+Aw+Bv+c.
\]
Nonsingularity of \(Dq(p)\) makes the \(n\)-by-\(\ell\)
matrix \(B\) have full column rank. Degree exactly four gives
\(q_2\ne0\), so \(r\geq1\). Moreover
\(\|q_2(w)\|^2>0\) for every nonzero \(w\in K^\perp\).

The \(ww\) block of the Hessian is
\[
 \nabla^2_{ww}F(w,v)
   =C(w)+2\sum_i(Bv)_i\nabla^2q_{2,i},
\]
where \(C(w)\) does not depend on \(v\). A symmetric matrix affine
in a freely signed real scalar can be positive semidefinite for every
scalar only if its linear coefficient is zero. Apply this observation
to each direction in \(v\). It shows that every component of
\(B^{\mathsf T}q_2(w)\) has zero Hessian. These components are
homogeneous quadratics, so
\[
 B^{\mathsf T}q_2(w)=0.
\]

Let \(T\) have orthonormal rows spanning
\((\operatorname{im}B)^\perp\), and define
\[
\begin{aligned}
 v_0(w)&=-(B^{\mathsf T}B)^{-1}B^{\mathsf T}(Aw+c),\\
 \bar q(w)&=T(q_2(w)+Aw+c).
\end{aligned}
\]
If \(\ell=0\), take \(T=I\) and omit \(v\) and \(v_0\).
The identity just proved makes \(v_0\) affine and gives
\[
 F(w,v)=\|B(v-v_0(w))\|^2+\|\bar q(w)\|^2.
\]
Hence \(\bar F(w)=F(w,v_0(w))=\|\bar q(w)\|^2\) is convex.
It has a unique zero \(w_*\), and the corresponding point on the
affine graph is \(p\). With
\(E=\begin{pmatrix}I_r\\Dv_0\end{pmatrix}\), its Hessian at that zero is
\(E^{\mathsf T}\nabla^2F(p)E\succ0\). The square map
\(\bar q:\mathbb R^r\to\mathbb R^r\) therefore has a unique
regular zero.

The leading part \(\bar q_2=Tq_2\) satisfies
\(\|\bar q_2(w)\|=\|q_2(w)\|\), because \(q_2(w)\) is
orthogonal to \(\operatorname{im}B\). Compactness of the unit sphere
gives a constant \(a>0\) with
\[
 \|\bar q_2(w)\|\geq a\|w\|^2.
\]
Consequently the homotopy
\(h_t=\bar q_2+t(\bar q_1+\bar q_0)\), \(0\leq t\leq1\),
satisfies a uniform bound
\[
 \|h_t(w)\|\geq a\|w\|^2-b\|w\|-c
\]
for constants \(b,c\geq0\). This bound proves properness of the
whole homotopy, rather than just properness of its individual maps.
It extends continuously to the one-point compactifications, so Brouwer
degree is constant along it.

The degree of \(\bar q\) is \(+1\) or \(-1\), by the local-degree
formula at its unique regular zero. The degree of \(\bar q_2\)
is even. To see this, choose a nonzero regular value; Sard's theorem
ensures that one exists, possibly outside the image. Its fiber is finite
by properness and regularity. Since \(\bar q_2\) is even, this fiber
is partitioned into pairs \(\{w,-w\}\), each contributing an even
sum of local signs. An empty fiber contributes zero. This contradicts
homotopy invariance of degree and excludes \(m=n\).

Finally,
\[
 F(x)=\left(\sum_jx_j^2\right)^2+\sum_jx_j^2
\]
has \(n+1\) displayed squares, zero only at the origin, and Hessian
\(8xx^{\mathsf T}+(4\|x\|^2+2)I\succeq2I\). This proves
sharpness. \(\square\)

The imported topological facts are the standard local-degree formula,
homotopy invariance of degree on spheres, and Sard's theorem. The proof
checks their noncompact-domain contract through the uniform properness
bound. It does not assume that the original leading quadratic map is
proper, nor that a homotopy of individually proper maps is automatically
proper. These are the potentially serious gaps that the flat-direction
reduction avoids.

Every principal hypothesis is needed. The positive-minimum quartic
\((1+\|x\|^2)^2\) has one square despite global strong convexity.
The quartic \(\|x\|^4\) has a degenerate zero and one square.
The nonconvex quartic \(x^2+(y-x^2)^2\) has two squares in two
variables and Hessian \(2I\) at its unique zero. A positive definite
quadratic centered at its zero has \(n\) squares. Degree six also fails:
\[
 (x_1+x_1^3)^2+\sum_{j=2}^n x_j^2
\]
has \(n\) squares, a unique zero at the origin, and Hessian
\(\operatorname{diag}(2+24x_1^2+30x_1^4,2,\ldots,2)\).
Thus the manuscript must retain degree exactly four and positive definite
Hessian at a zero, even when global strong convexity is available.

**Lemma 2 (rational Gram matrices and rational squares).** A polynomial
with a rational positive semidefinite Gram matrix on a rational polynomial
vector is a sum of squares of rational polynomials. Conversely, a sum of
rational polynomial squares gives such a matrix. For degree at most four,
all square factors have degree at most two. At a real zero, every square
factor vanishes there.

**Proof.** The converse and the zero statement follow directly from
summing squares. The degree statement was proved in Theorem 1. Rational
symmetric elimination gives a positive semidefinite rational matrix a
congruence decomposition into nonnegative rational weights and rational
linear forms; a zero diagonal entry in a positive semidefinite residual
has a zero row and column, so singular matrices cause no difficulty.
Every positive rational weight \(u/v\), with \(u,v\) positive
integers, is a sum of rational squares. Indeed, expand \(uv\) in
binary and divide by \(v^2\). A term \(2^{2h}/v^2\) is one
rational square, and a term \(2^{2h+1}/v^2\) is two equal rational
squares. Applying this to each weight gives the required polynomial
squares. \(\square\)

This lemma concerns existence of a rational SOS. It does not assert
that a rational matrix of rank \(r\) factors into exactly \(r\)
rational squares. Its real factorization does use \(r\) squares;
the rational conversion can use more. That distinction is needed when
discussing minimum length over different coefficient fields.

**Theorem 3 (rational descent from a small vanishing space).** Suppose
\[
 \dim_{\mathbb Q}I_2^{\mathbb Q}(p)=n+1,
 \qquad J_4^{\mathbb Q}(p)=W^{\mathbb Q}(p).
\]
Assume there is a rational SOS polynomial \(G\) of degree exactly
four that is globally convex and satisfies
\(G(p)=0\), \(\nabla^2G(p)\succ0\). Then every rational,
globally convex polynomial \(F\) of degree exactly four with
\[
 F(p)=0,\qquad \nabla F(p)=0,\qquad \nabla^2F(p)\succ0
\]
has a unique positive definite rational Gram matrix on any rational basis
of \(I_2^{\mathbb Q}(p)\). In particular, \(F\) is rational SOS.

**Proof.** Let \(q\) be a column vector listing a rational basis of
\(I_2^{\mathbb Q}(p)\). Each rational square factor of \(G\)
belongs to this space by Lemma 2. Therefore
\[
 G=q^{\mathsf T}S_0q,\qquad
 S_0\in\operatorname{Sym}_{n+1}(\mathbb Q),\quad S_0\succeq0.
\]
If \(S_0\) were singular, its real factorization would represent
\(G\) with at most \(n\) real quadratic squares, contradicting
Theorem 1. Hence \(S_0\succ0\).

Since \(F\in J_4^{\mathbb Q}(p)=W^{\mathbb Q}(p)\), there
is a rational symmetric matrix \(S\) with
\(F=q^{\mathsf T}Sq\). Suppose \(S\) is not positive definite.
The continuous segment
\[
 S_t=(1-t)S_0+tS,\qquad
 F_t=(1-t)G+tF=q^{\mathsf T}S_tq
\]
has a first parameter \(t_*\in(0,1]\) at which \(S_{t_*}\)
is positive semidefinite and singular. A real factorization then expresses
\(F_{t_*}\) as at most \(n\) real quadratic squares.

At every parameter the polynomial \(F_t\) is convex and vanishes
at \(p\), and its Hessian there is positive definite. It also has
degree exactly four at \(t_*\). Indeed, both endpoints are nonnegative:
\(G\) is SOS, and stationarity and convexity give \(F(x)\geq F(p)=0\).
Their fourth homogeneous parts are therefore nonnegative, by taking
limits along rays. For \(t_*<1\), the nonzero nonnegative fourth
part of \(G\) cannot be canceled by that of \(F\). For
\(t_*=1\), degree exactly four is an assumption on \(F\).
Theorem 1 gives a contradiction. Thus \(S\succ0\), and Lemma 2
gives rational squares.

To prove uniqueness, consider a nonzero real symmetric matrix \(K\)
with \(q^{\mathsf T}Kq=0\). After changing its sign if needed,
\(K\) has a negative eigenvalue. The ray \(S_0+tK\), \(t\geq0\),
reaches a first singular positive semidefinite matrix at a finite positive
parameter. This would represent the unchanged polynomial \(G\) by
at most \(n\) real squares, again contradicting Theorem 1. Therefore
the multiplication map has zero kernel, even over \(\mathbb R\).
This proves uniqueness. Changing rational basis applies an invertible
rational congruence to the matrix, which preserves positive definiteness.
\(\square\)

The boundary parameter \(t_*\) need not be rational. This creates
no gap: Theorem 1 allows real coefficients in the intermediate polynomial
and its square factors. The proof also does not infer convexity of the
individual quadratic factors or assume SOS-convexity.

**Corollary 4 (product independence).** The existence of the baseline
\(G\) and the dimension assumption alone imply
\[
 \operatorname{Sym}_{n+1}(\mathbb Q)\longrightarrow W^{\mathbb Q}(p),
 \qquad S\longmapsto q^{\mathsf T}Sq
\]
is injective and
\(\dim_{\mathbb Q}W^{\mathbb Q}(p)=(n+1)(n+2)/2\).
This conclusion does not require \(J_4^{\mathbb Q}(p)=W^{\mathbb Q}(p)\).
Under all hypotheses of Theorem 3, the real SOS length of \(F\) is
exactly \(n+1\). The theorem alone does not fix its rational SOS length.

The positive definite matrix in Theorem 3 is on the vanishing-quadratic
basis. A positive definite Gram matrix on the full monomial vector is
impossible, since that vector contains the constant monomial and is
nonzero at \(p\). In fact the full rational positive semidefinite Gram
matrix is unique and has rank \(n+1\). To verify this last assertion,
let \(m\) be the full degree-at-most-two monomial vector and write
\(q=B^{\mathsf T}m\), with \(B\) rational and of full column rank.
If \(F=m^{\mathsf T}Qm\) with rational \(Q\succeq0\), then
\(Qm(p)=0\). Each row of \(Q\) is a rational quadratic vanishing
at \(p\), so symmetry gives
\(\operatorname{range}Q\subseteq\operatorname{range}B\).
For a rational left inverse \(C\) of \(B\),
\[
 Q=B A B^{\mathsf T},\qquad A=CQC^{\mathsf T}\succeq0.
\]
Product independence determines \(A=S\), and hence \(Q\), uniquely.
This reasoning applies to rational positive semidefinite full Grams;
it makes no uniqueness claim about unrestricted real full Grams.

The two descent assumptions have separate roles. The dimension
\(n+1\) turns a singular restricted Gram into too few real squares.
The stationary-space equality supplies a restricted Gram for every
rational stationary \(F\). Without that equality, a stationary
quartic can lie outside the product span. Without the dimension bound,
a singular restricted Gram need not violate Theorem 1. Neither assumption
can be deleted on the basis of the present proof.

The tower stationary-space result is also valid uniformly. The following
reconstruction supplies its dependencies rather than treating the finite
rank calculations as a proof.

**Theorem 5 (the quintic tower's rational spaces).** For \(k\geq1\),
let \(a_i=2^{1/5^i}\), use \(n=3k\) variables
\((x_i,y_i,z_i)_{i=1}^k\), and put
\(p_k=(a_i,a_i^2,a_i^3)_{i=1}^k\). Set \(b_1=2\) and
\(b_i=x_{i-1}\) for \(i>1\). Define
\[
\begin{aligned}
 q_{i,1}&=x_i^2-y_i,& q_{i,2}&=x_iy_i-z_i,\\
 q_{i,3}&=y_i^2-x_iz_i,&q_{i,4}&=y_iz_i-b_i,\\
 q_{i,5}&=z_i^2-b_ix_i.
\end{aligned}
\]
These \(5k\) relations form a basis of
\(I_2^{\mathbb Q}(p_k)\). Their unordered pairwise products are
independent over both \(\mathbb Q\) and \(\mathbb R\). With
\(q\) their column vector,
\[
 J_3^{\mathbb Q}(p_k)=0,\qquad
 J_4^{\mathbb Q}(p_k)
  =\{q^{\mathsf T}Aq:A\in\operatorname{Sym}_{5k}(\mathbb Q)\},
 \qquad \dim J_4^{\mathbb Q}(p_k)=\binom{5k+1}{2}.
\]
The matrix \(A\) is unique.

**Proof.** Eliminate the distinct pivot monomials
\(x_i^2,x_iy_i,y_i^2,y_iz_i,z_i^2\) using the displayed
relations. No right-hand side contains a pivot. The retained monomials
are \(1\), the four monomials \(x_i,y_i,z_i,x_iz_i\) for each
gate, and the nine products of a variable from each of two distinct gates.
In powers of \(a_k\), their exponents have distinct base-five patterns:
all digits zero, one digit in \(\{1,2,3,4\}\), or two digits in
\(\{1,2,3\}\). All exponents are less than \(5^k\).
Eisenstein irreducibility of \(T^{5^k}-2\) proves independence of
these evaluations. The reduction therefore proves completeness of the
relations, and their distinct pivots prove independence. It also proves
that no nonzero rational affine polynomial vanishes at \(p_k\).
Consequently \(J_2^{\mathbb Q}(p_k)=0\): the partial derivatives
of a stationary quadratic are affine vanishing polynomials and are zero;
its remaining constant is then zero.

For one gate the leading quadratics are
\(L=(x^2,xy,y^2-xz,yz,z^2)\). Their fifteen unordered products
span every ternary quartic. Ten monomials are direct products, and the
other five are given by
\[
\begin{aligned}
 x^3z&=L_2^2-L_1L_3,& xy^3&=L_2L_3+L_1L_4,\\
 y^3z&=L_3L_4+L_2L_5,&xz^3&=L_4^2-L_3L_5,\\
 y^4&=L_3^2+2L_2L_4-L_1L_5.
\end{aligned}
\]
They are thus independent, since the space has dimension fifteen.
In a dependence among relation products for several gates, the part of
degree four in the last triple contains only last-gate products. The
local independence kills their coefficients. The last-gate degree-two
part remaining is \(\sum_jL_jP_j\), where each \(P_j\) is a
linear combination of earlier relations. Independence of the five
\(L_j\), also over the polynomial ring in earlier variables, gives
\(P_j=0\). Independence of earlier relations kills the cross
coefficients. Induction kills the remaining earlier-gate dependence.
The argument works with real as well as rational scalar coefficients.

For the stationary assertions, first establish a local interpolation
lemma. Let \(L\) be a characteristic-zero field, let \(b\ne0\),
and suppose \(a^5=b\) has degree five over \(L\). Then
\[
 L[x,y,z]_{\leq3}\longrightarrow L(a)^4,
 \quad P\longmapsto(P,P_x,P_y,P_z)(a,a^2,a^3)
\]
is an isomorphism of twenty-dimensional \(L\)-spaces. To prove this,
multiply the derivative outputs by \(a,a^2,a^3\), respectively.
These are invertible \(L\)-linear transformations. A monomial
\(x^iy^jz^h\) of weight \(i+2j+3h=5t+r\) then contributes
to residue \(r\) a nonzero scalar \(b^t\) times the column
\((1,i,j,h)^{\mathsf T}\). The five residue blocks have the
following ordered monomials and determinants after these column scalings
are removed:

| Residue | Monomials | Determinant |
| ---: | --- | ---: |
| 0 | \(1,yz,x^2z,xy^2\) | \(5\) |
| 1 | \(x,z^2,xyz,y^3\) | \(5\) |
| 2 | \(y,x^2,xz^2,y^2z\) | \(-5\) |
| 3 | \(z,xy,x^3,yz^2\) | \(-5\) |
| 4 | \(xz,y^2,x^2y,z^3\) | \(-5\) |

All blocks are nonsingular. This also explains the shifted derivative
residues in the unscaled block matrices in the source note.

Use the lemma at the last gate over \(L=\mathbb Q(a_{k-1})\),
with \(b=a_{k-1}\) and \(a=a_k\); at the first gate use
\(L=\mathbb Q\), \(b=2\). The degree-five extension follows
from \([\mathbb Q(a_j):\mathbb Q]=5^j\).

For a stationary rational cubic, write \(U\) for earlier variables
and \(V\) for the last triple. The local lemma makes
\(F(p_{k-1},V)\) identically zero. Thus every coefficient in \(V\)
vanishes at the earlier point. Coefficients of \(V\)-degree at least
two are affine in \(U\), so they are identically zero. The remainder
is
\[
 h_0(U)+x_kh_1(U)+y_kh_2(U)+z_kh_3(U),
 \quad \deg h_0\leq3,\quad\deg h_j\leq2\ (j>0).
\]
All coefficient values vanish. Differentiating in any earlier variable
and using independence of \(1,a_k,a_k^2,a_k^3\) over \(L\)
makes every coefficient gradient vanish separately. The zero earlier
quadratic stationary space kills \(h_1,h_2,h_3\), and cubic induction
kills \(h_0\). The first-gate case is the local lemma itself.

For a stationary rational quartic, subtract products of last-gate
relations to eliminate its \(V\)-degree-four part, using the fifteen
leading products above. Its coefficients there are rational constants
by the total-degree bound. The remainder still has zero value and full
gradient. Local cubic interpolation makes every specialized coefficient
zero. Its \(V\)-degree-three coefficients are affine in \(U\),
so they are identically zero. Its quadratic \(V\)-coefficients lie
in the earlier rational quadratic vanishing space.

Let \(c_{y^2}\) and \(c_{xz}\) be the two indicated quadratic
coefficients. In a degree-at-most-two polynomial over \(L\), only
\(y_k^2\) and \(x_kz_k\) contribute to the field basis element
\(a_k^4\). Apply this observation to each earlier partial derivative
of the remainder after specializing \(U\). It proves that every
earlier partial derivative of \(c_{y^2}+c_{xz}\) vanishes at
\(p_{k-1}\). Its value also vanishes, and its degree is at most
two. The zero earlier quadratic stationary space therefore gives the
polynomial identity \(c_{y^2}+c_{xz}=0\).

The whole quadratic \(V\)-part can now be written
\(\sum_{j=1}^5L_j(V)P_j(U)\), with each \(P_j\) an earlier
quadratic relation. Subtract \(\sum_jq_{k,j}P_j\), a sum of
cross-gate relation products. These products preserve full stationarity
by the product rule. The remaining polynomial is last-linear, with
constant coefficient of degree at most four and other coefficients of
degree at most three. In particular, the term \(-x_{k-1}x_k\)
in \(q_{k,5}\) only contributes a last-linear coefficient of degree
at most three; no degree bound is lost.

Each remaining coefficient has zero value and gradient at the earlier
point, by the same independence argument as for cubics. The cubic result
kills the last-linear coefficients, and quartic induction expresses the
constant coefficient as earlier relation products. At the first gate,
subtract the fifteen local products and apply the local cubic lemma.
This proves the stationary-space equality. Product independence proves
uniqueness and the dimension formula. \(\square\)

It follows that a rational stationary quartic at this supplied tower
point is rational SOS exactly when its unique rational matrix \(A\)
is positive semidefinite. The implication from rational SOS restricts
the factors to the rational quadratic basis; the converse is Lemma 2.
The same full-monomial argument used after Corollary 4 proves uniqueness
of its rational positive semidefinite full Gram. Rational linear algebra
on \(O(k^4)\) coefficient positions and \(O(k^2)\) products,
whose entries are bounded integers, recovers \(A\) in polynomial
bit time in \(k\) and the explicit rational input length. Exact
symmetric elimination and the binary-weight proof of Lemma 2 give a
polynomial-length rational SOS when \(A\succeq0\). This recognizes
rational SOS for this supplied-point class; it does not find the point
or recognize arbitrary real SOS.

For every \(k\geq1\), the tower has
\(\dim I_2^{\mathbb Q}=5k>3k+1=n+1\). It therefore does not
satisfy the dimension hypothesis of the descent criterion. This preserves
the possibility of a strongly convex real-SOS rational quartic with an
indefinite matrix on the rational relation basis. Real square factors
can use the larger full real vanishing space. The tower stationary-space
proof itself neither constructs such a quartic nor establishes the
companion least-field claim; those remain separate dependencies.
An unconstrained differentiable minimum supplies ambient stationarity.
A constrained minimum need not, so the stationary identity cannot be
invoked at arbitrary constrained optima on that basis.

The cyclic SOS-length application is uniform and requires no stationary
dimension experiment. The construction supplies, for every \(n\geq2\),
a rational strongly convex quartic with its displayed zero and positive
definite Hessian there. Its residual vector has length \(m=n+1\).
For any nonzero rational vector \(g\), put \(R=g^{\mathsf T}g\).
Choose a rational \(0<r<\sqrt R\), and define
\[
 t=\frac{R-r^2}{2r},\qquad
 s=\frac{R+r^2}{2r},\qquad
 L=tI+\frac rRgg^{\mathsf T}.
\]
Then \(t>0\), \(s^2=t^2+R\), and
\[
 L^2=t^2I+gg^{\mathsf T},\qquad
 (g^{\mathsf T}q)^2+t^2\sum_iq_i^2=\sum_i(Lq)_i^2.
\]
Indeed \((gg^{\mathsf T})^2=Rgg^{\mathsf T}\), and the
rank-one coefficient in \(L^2\) is
\((2tr+r^2)/R=1\). The eigenvalues of \(L\) are \(t\)
on \(g^\perp\) and \(s\) on its complementary line. Thus \(L\)
is invertible, and the common zero set is preserved exactly.

The parameter must be chosen before taking this rational square root.
A previously fixed rational regularization \(t^2\) need not make
\(R+t^2\) a rational square. In the cyclic construction one can
choose rational \(r\) with \(M^{-1}\leq t\leq2M^{-1}\), where
\(M=10^6n^5\), using rational bisection. The weights give
inverse-polynomial lower and polynomial upper bounds on \(R\);
the interval has inverse-polynomial width, so numerators and denominators
of \(r\) can have polynomial magnitude. The resulting regularization
lies in \([M^{-2},4M^{-2}]\).

The universal curvature bounds remain valid over this whole interval.
With \(\mu=1/(16n^2)\), \(\nu=1/(8n)\), and
\(D\leq17n\), the required upper bounds are
\[
 t^2\leq1,\qquad t^2\leq\frac{\mu^2}{2(n+1)},\qquad
 t^2\leq\frac{\nu^2\mu^2}{36nD^2}.
\]
The middle right side is at least \(1/(768n^5)\), and the last
is at least \(1/(170459136n^9)\). Both exceed
\(4/(10^{12}n^{10})\) for every \(n\geq2\). The construction
therefore retains its positive global Hessian bound. Rational denominator
clearing and integer scaling preserve its zero and give \(n+1\)
integer quadratic square factors. Theorem 1 proves that no representation
by fewer real squares exists. Thus the compressed polynomial has minimum
SOS length exactly \(n+1\) over \(\mathbb R\), \(\mathbb Q\),
and \(\mathbb Z\), for every \(n\geq2\). No dimension table is
needed for this statement.

For the original regularization, real factorization of
\(gg^{\mathsf T}+\varepsilon I\) already gives at most \(n+1\)
real squares, so its real minimum is also \(n+1\). The original
display of \(n+2\) rational or integer squares does not by itself
establish a smaller rational or integer minimum. The compression gives
an alternative quartic with the same zero and a genuine \(n+1\)-square
integer display. These two assertions should remain distinct.

The cyclic zero's coordinate field degree
\[
 d_n=\frac{2^{n+1}-(-1)^{n+1}}3
\]
is uniform as well. With
\(s_i=((-2)^i-1)/3\), \(a^{d_n}=2\), and
\(p_i=a^{s_i}\), Eisenstein irreducibility of \(T^{d_n}-2\)
and \(p_1=a^{-1}\) give
\(\mathbb Q(p)=\mathbb Q(a)\), of degree \(d_n\).
The compression changes the objective, not this zero. Algebraic degree
is not a lower bound for all exact representations or decisions: these
coordinates retain short rational-power expressions.

The separate cyclic quadratic-space draft also has a valid uniform
proof. For \(n\geq4\), put \(m=n+1\), \(B=-2\), and
homogenize affine quadratics with \(X_0\), evaluated at \(p_0=1\).
Two monomials \(X_iX_j\) and \(X_uX_v\) have rationally
proportional evaluations exactly when
\[
 B^i+B^j\equiv B^u+B^v\pmod{B^m-1}.
\]
This modulus is correct: the difference of the exponent sums is the
displayed numerator divided by three, and
\(|B^m-1|=3d_n\). At most four cyclic indices occur. Since
\(m\geq5\), rotate an unused index to \(m-1\). Rotation
preserves the congruence because \(B\) is invertible modulo
\(B^m-1\). All used powers now have indices at most \(m-2\).
The absolute difference of the two pair sums is at most
\(3\cdot2^{m-2}<|B^m-1|\), so their congruence is ordinary
integer equality.

If both pairs have distinct indices, the 2-adic valuation of each sum
is its smaller index. The smaller indices agree, and cancellation gives
the same larger index. If both pairs are repeated indices, equality also
makes them identical. In the mixed case
\(2B^r=B^u+B^v\), \(u<v\), valuation gives \(u=r+1\),
and division by \(B^r\) gives \(B^{v-r}=4\), so \(v=r+2\).
After rotating back, the only nontrivial collision is
\(X_i^2\) with \(X_{i+1}X_{i+2}\). These \(m\) pairs
are disjoint. Their rational power-of-two coefficients are exactly the
displayed cyclic residual coefficients. They form a complete rational
quadratic basis, proving
\[
 \dim I_2^{\mathbb Q}(p)=n+1\qquad(n\geq4).
\]
Corollary 4 and the convex rational SOS baseline then prove product
independence and
\(\dim W^{\mathbb Q}(p)=(n+1)(n+2)/2\) uniformly for
\(n\geq4\). The rotation argument does not cover \(n=3\),
where \(\dim I_2^{\mathbb Q}=5\) and the descent hypothesis fails.

The remaining equality
\(J_4^{\mathbb Q}(p)=W^{\mathbb Q}(p)\) has only finite
recorded evidence for this cyclic family. The criterion note records:

| \(n\) | \(d_n\) | \(\dim I_2^{\mathbb Q}\) | \(\dim W^{\mathbb Q}\) | \(\dim J_4^{\mathbb Q}\) |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 3 | 3 | 6 | 6 |
| 3 | 5 | 5 | 15 | 15 |
| 4 | 11 | 5 | 15 | 15 |
| 5 | 21 | 6 | 21 | 21 |
| 6 | 43 | 7 | 28 | 28 |
| 7 | 85 | 8 | 36 | 36 |
| 8 | 171 | 9 | 45 | 45 |
| 9 | 341 | 10 | 55 | 55 |
| 10 | 683 | 11 | 66 | 66 |
| 11 | 1365 | 12 | 78 | 78 |
| 12 | 2731 | 13 | 91 | 91 |
| 13 | 5461 | 14 | 105 | 105 |
| 14 | 10923 | 15 | 120 | 120 |
| 15 | 21845 | 16 | 136 | 136 |
| 16 | 43691 | 17 | 153 | 153 |

The retained checker computes these spaces correctly over
\(\mathbb Q\). A monomial with exponent vector \(e\) evaluates
to \(2^h a^r\), where \(\sum_i e_i s_i=h d_n+r\),
\(0\leq r<d_n\); this reduction also handles negative exponents
of \(a\). Independence of \(1,a,\ldots,a^{d_n-1}\)
splits quadratic evaluation into residue classes. A class containing
\(t\) quadratic monomials supplies exactly \(t-1\) binomial
relations, which the program constructs with the correct rational
power-of-two coefficients.

For stationarity, each coordinate is nonzero, so multiplying the
\(j\)th derivative equation by \(p_j\) is invertible. A monomial
then contributes \(2^ha^r(1,e_1,\ldots,e_n)^{\mathsf T}\).
Each residue block is ranked separately, and the nonzero rational
column scale \(2^h\) can be discarded. The checker uses exact
\(\mathrm{Fraction}\) elimination for these ranks. It also forms
the actual relation products and computes their coefficient ranks;
each product stays in one residue block. Thus its reported kernel
dimensions have the stated interpretation. Inspection of the source
revealed no numerical, modular-rank, derivative-scaling, or field-basis
gap.

This review did not independently execute those computations. The table
is the existing recorded result, not a new run. For each listed dimension,
equality of its two final dimensions and the inclusion
\(W^{\mathbb Q}\subseteq J_4^{\mathbb Q}\) give equality of
spaces. The descent conclusion therefore applies to the listed cyclic
points for \(n=2\) and \(4\leq n\leq16\). It does not apply
at \(n=3\), despite equality of the two stationary/product dimensions,
because the required quadratic dimension is larger there. No argument
in the reviewed files establishes \(J_4^{\mathbb Q}=W^{\mathbb Q}\)
for all \(n\geq4\); no such claim should enter the paper.

The results preserved by this review are the universal real SOS-length
bound, the conditional rational descent theorem and product independence,
the uniform tower basis and stationary-space identities, the uniform
cyclic square compression and its exact minimum length, and the uniform
cyclic quadratic dimension for \(n\geq4\). The cyclic stationary-space
equality remains a finite computed application. The descent theorem is
an obstruction to rational SOS failure under its hypotheses; it supplies
no lower bound for arbitrary lifted certificates, solver runtime, or
exact-output formats.

Targeted work actually performed: read the listed notes and the retained
cyclic checker and rederive the displayed identities and universal proofs
analytically. The following local text check passed with twelve resolving
links; it performs no mathematical experiment:

```text
python - <<'PY'
from pathlib import Path
import re
p = Path('paper-exact-arithmetic/evidence/reviews/prewrite-descent-criterion.md')
s = p.read_text()
assert s.endswith('\n')
assert not any(line.rstrip() != line for line in s.splitlines())
assert all(ord(c) >= 32 or c in '\n\t' for c in s)
prose = re.sub(r'```.*?```', '', s, flags=re.S)
assert prose.count(r'\(') == prose.count(r'\)')
assert prose.count(r'\[') == prose.count(r'\]')
links = re.findall(r'\]\(([^)]+)\)', prose)
for target in links:
    assert (p.parent / target).resolve().is_file(), target
print(f'Review text checks passed; {len(links)} local links resolve.')
PY
```

No author experiment was rerun. These are local manuscript checks, not
CI results. No historical note or manuscript file was edited.
