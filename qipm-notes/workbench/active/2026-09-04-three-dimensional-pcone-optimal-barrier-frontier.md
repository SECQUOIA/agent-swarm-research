# The optimal-barrier frontier for the three-dimensional \(p\)-order cone

Status: New obstruction proved, literature-screened, and independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the characteristic-barrier theorem, source ledger, and asymptotics

## Executive result

Let

\[
 K_p=\{(t,x_1,x_2):t\geq(|x_1|^p+|x_2|^p)^{1/p}\},
 \qquad 1<p<\infty,
\]

and let \(\nu_{\rm opt}(p)\) be the infimum of the parameters of its
logarithmically homogeneous self-concordant barriers. The currently proved
general interval is

\[
                         \boxed{h(p)\leq\nu_{\rm opt}(p)\leq3}. \tag{1}
\]

The lower endpoint is Hildebrand's explicit cross-ratio bound. The upper
endpoint is supplied by the three-dimensional canonical barrier. The exact
optimum is two at \(p=2\), and is three at the polyhedral endpoint cases
\(p=1,\infty\). No proof that \(\nu_{\rm opt}(p)\) equals either \(h(p)\) or
three was found for \(1<p<\infty\), \(p\ne2\).

This note adds a rigorous obstruction to the most prominent proposed way of
closing the gap.

> **Characteristic-barrier obstruction.** Let
> \[
>   \zeta_p(z)=\int_{K_p^*}e^{-\langle z,y\rangle}\,dy,
>   \qquad \Phi_{p,\kappa}=\kappa\log\zeta_p .       \tag{2}
> \]
> If \(p>2\) and \(\Phi_{p,\kappa}\) is self-concordant, then
> \[
>       \kappa\geq\frac{p}{p+1},\qquad
>       \nu(\Phi_{p,\kappa})=3\kappa
>                    \geq \frac{3p}{p+1}>h(p).       \tag{3}
> \]

Thus no scalar multiple of the characteristic-function barrier can match
Hildebrand's lower bound for \(p>2\). Chares conjectured, from randomized
numerical experiments, that the first inequality is also sufficient. The
argument below proves only its necessity, not that conjecture.

By Legendre duality, for \(1<p<2\) the analogous obstruction applies to
the dual-characteristic (entropic) family obtained from
\(K_q\), \(q=p/(p-1)>2\): its parameter cannot be below
\(3p/(2p-1)>h(p)\). This does not prove the same necessary scaling for the
characteristic barrier of \(K_p\) itself, because characteristic barriers
are not generally preserved by cone duality.

A second audited obstruction rules out the natural nested construction. Put

\[
 A=t^p-|x|^p,
 \qquad
 F_{\alpha,\beta}(t,x,y)
   =-\alpha\log A-\beta\log(A^{2/p}-y^2).             \tag{3a}
\]

The domain is \(\operatorname{int}K_p\), and the formal homogeneity
parameter is \(p\alpha+2\beta\). If this function is an LHSC barrier, a
generic boundary line for the second logarithm forces \(\beta\geq1\), while
the axial line \((t,x,y)=(1,1-\delta,0)\) forces

\[
                         \alpha+\frac{2\beta}{p}\geq1.
\]

Therefore

\[
                         \nu=p\alpha+2\beta\geq p>h(p) \tag{3b}
\]

for \(p>2\). For \(2<p\leq3\), the formula is additionally not \(C^3\) at
the interior axis \(x=0\); for \(p>3\), (3b) is the operative obstruction.
The corresponding dual nested construction cannot match \(h(p)\) for
\(1<p<2\).

The still simpler defining-function ansatz fails outright. For

\[
 F(t,x,y)=-a\log(t^p-|x|^p-|y|^p)-b\log t,
 \qquad a>0,                                         \tag{3c}
\]

the transverse Hessian on the central ray is zero when \(p>2\), while the
function is not \(C^2\) there when \(1<p<2\). Thus no choice of \(b\) makes
(3c) an LHSC barrier unless \(p=2\).

There is a robust bounded-correction version of this no-go. On the unit
base, write

\[
 f(x,y)=-a\log(1-|x|^p-|y|^p)+\psi(x,y).             \tag{3d}
\]

For \(p\leq3\), \(p\ne2\), a \(C^3\) correction \(\psi\) cannot repair the
interior-axis loss of \(C^2\) or \(C^3\). For \(p>3\), suppose only that
\(\psi_{yy}\) and \(\psi_{yyy}\) remain bounded along

\[
 x_\delta=(1-\delta)^{1/p},
 \qquad y_\delta=\delta^{1/(p-2)}.
\]

If \(L\) denotes the logarithmic term in (3d), direct differentiation gives

\[
 L_{yy}=ap(p-1)+o(1),\qquad
 L_{yyy}=ap(p-1)(p-2)\delta^{-1/(p-2)}(1+o(1)).       \tag{3e}
\]

The corrected Hessian is therefore bounded while its third derivative
diverges, contradicting self-concordance in the pure \(y\) direction (or
convexity fails first). The bounded-derivative hypothesis is essential:
an admissible barrier matching \(h(p)\), if one exists, must introduce a
singular transverse correction near the flat axial boundary.

## Proof of the characteristic-barrier obstruction

The dual cone of \(K_p\) is \(K_q\), where \(1/p+1/q=1\). Parameterize a
point of \(K_q\) as \(s(1,u,v)\), with \(s\geq0\) and
\((u,v)\in B_q^2\). The Jacobian is \(s^2\). Therefore, at

\[
                         z_\delta=(1+\delta,1,0),
                         \qquad \delta>0,
\]

integration in \(s\) gives

\[
 \begin{aligned}
 \zeta_p(z_\delta)
 &=2\int_{B_q^2}(1+\delta+u)^{-3}\,du\,dv\\
 &=4\int_0^2
   \frac{[1-|a-1|^q]^{1/q}}{(\delta+a)^3}\,da .      \tag{4}
 \end{aligned}
\]

As \(a\downarrow0\),

\[
 [1-(1-a)^q]^{1/q}=q^{1/q}a^{1/q}(1+O(a)).           \tag{5}
\]

Substitution \(a=\delta r\), followed by dominated convergence on a
small fixed interval and a bounded-tail estimate, yields

\[
 \zeta_p(z_\delta)=C_p\delta^{-\beta_p}(1+o(1)),
 \qquad
 \beta_p=2-\frac1q=1+\frac1p,                        \tag{6}
\]

where

\[
 C_p=4q^{1/q}\int_0^\infty
                \frac{r^{1/q}}{(1+r)^3}\,dr>0.
\]

Differentiating (4) under the integral and using the same rescaling proves
the differentiated regular-variation asymptotics through order three.
Consequently, for the univariate restriction
\(f_\kappa(\delta)=\Phi_{p,\kappa}(z_\delta)\),

\[
 f_\kappa''(\delta)=\frac{\kappa\beta_p}{\delta^2}(1+o(1)),
 \qquad
 f_\kappa'''(\delta)=-\frac{2\kappa\beta_p}{\delta^3}(1+o(1)). \tag{7}
\]

Restriction to an affine line preserves self-concordance. Hence
\(|f'''|\leq2(f'')^{3/2}\), followed by \(\delta\downarrow0\), forces

\[
                         \kappa\beta_p\geq1.         \tag{8}
\]

Since \(\zeta_p(\lambda z)=\lambda^{-3}\zeta_p(z)\), the logarithmic
homogeneity parameter of \(\kappa\log\zeta_p\) is \(3\kappa\). For
\(p>2\), (8) proves the first part of (3). The universal lower bound
\(\nu\geq2\) also gives \(\kappa\geq2/3\), but (8) is stronger precisely
when \(p>2\).

## The characteristic threshold is strictly above \(h(p)\)

For \(p>2\), set \(c=1/p\), \(s=p-2>0\), and
\(A=\gamma_p^c\), with \(\gamma_p\) from Hildebrand's formula. Its defining
equation becomes

\[
                         A^s(sA+s+1)=1,              \tag{9}
\]

and

\[
 h(p)=2+\frac{s}{s+1}A,
 \qquad
 \frac{3p}{p+1}=2+\frac{s}{s+3}.                    \tag{10}
\]

The left side of (9) is strictly increasing in \(A\). Put
\(B=(s+1)/(s+3)\). At \(B\), its logarithm is

\[
 g(s)=\log(2s+3)+(s+1)\log\frac{s+1}{s+3}.          \tag{11}
\]

Here \(g(0)=0\). If \(b=(s+1)/(s+3)\), direct differentiation gives

\[
 g'(s)=\log b+\frac{2}{2s+3}+\frac{2}{s+3}.         \tag{12}
\]

To prove the sign without a loose logarithm bound, put
\(z=2/(s+3)=1-b\in(0,2/3)\). The right side of (12) becomes

\[
 H(z)=\log(1-z)+z+\frac{2z}{4-3z}.
\]

Now \(H(0)=0\), and

\[
 H'(z)=\frac{8-24z+24z^2-9z^3}
              {(1-z)(4-3z)^2}>0
 \qquad(0<z<2/3),
\]

the numerator decreasing to zero only at \(z=2/3\). Hence \(g'(s)>0\).

Thus the left side of (9) exceeds one at \(B\), so \(A<B\). Equation
(10) now proves the strict last inequality in (3). At two exact examples,

\[
 \begin{array}{c|c|c|c}
 p & \gamma_p & h(p) & 3p/(p+1)\\ \hline
 3 & (\sqrt2-1)^3 & (3+\sqrt2)/2 & 9/4\\
 4 & 1/16 & 7/3 & 12/5
 \end{array}                                             \tag{13}
\]

so the conjectured characteristic threshold does not equal the known lower
bound even at simple rational exponents.

## Exact asymptotics of Hildebrand's lower bound

Put

\[
 c=\min\{1/p,1-1/p\},\qquad
 d=1-2c=|1-2/p|,
\]

and let \(w=W(e^{-1})\approx0.2784645428\), where \(W\) is Lambert's
function. Then, as \(p\to2\),

\[
 h(p)=2+2wd+2w^2d^2+O(d^3).                         \tag{14}
\]

In particular,

\[
                         h(p)=2+w|p-2|+O((p-2)^2),   \tag{15}
\]

so the lower-bound curve has a genuine cusp at the Lorentz exponent. More
precisely, for \(\varepsilon=p-2\),

\[
 h(2+\varepsilon)=
 \begin{cases}
 2+w\varepsilon+\frac{w^2-w}{2}\varepsilon^2+O(\varepsilon^3),
       &\varepsilon\downarrow0,\\
 2+w|\varepsilon|+\frac{w+w^2}{2}\varepsilon^2
       +O(|\varepsilon|^3),&\varepsilon\uparrow0.
 \end{cases}                                           \tag{16}
\]

As \(p\to\infty\), with \(L=\log(2p)\),

\[
 h(p)=3-\frac{L+1}{p}
       +\frac{L^2-L+1}{2p^2}
       +O\!\left(\frac{L^3}{p^3}\right).             \tag{17}
\]

For \(p=1+\varepsilon\to1^+\), with
\(L=\log(2/\varepsilon)\),

\[
 h(p)=3-\varepsilon(L+1)
       +\frac{\varepsilon^2}{2}(L^2+L+1)
       +O(\varepsilon^3L^3).                         \tag{18}
\]

These expansions are Hölder-dual, as they must be. A compact derivation is
as follows. With \(a=\gamma_p^c\) and \(s=1/c-2\), the root equation is

\[
                         a^s(1+s(a+1))=1,            \tag{19}
\]

while

\[
 h(p)-2=\frac{1-2c}{1-c}\,a.                        \tag{20}
\]

The analytic implicit-function theorem at \(s=0\) gives

\[
 a=w+\frac{w(1+w)}2s+O(s^2),
\]

which yields (14)--(16). At the other endpoint, writing
\(\ell=\log(c/2)\), expansion of (19) gives

\[
 \gamma_p=\frac c2\left[1+\frac32c(\ell+1)
              +O(c^2|\ell|^2)\right],               \tag{21}
\]

and

\[
 h(p)=3+c(\ell-1)
       +\frac{c^2}{2}(\ell^2+\ell+1)
       +O(c^3|\ell|^3),                              \tag{22}
\]

from which (17)--(18) follow.

For comparison, Chares's conjectured characteristic-barrier parameter is

\[
 u(p)=\frac{3}{1+c}.
\]

Near \(p=2\), \(u(p)-h(p)=(1/3-w)|p-2|+O((p-2)^2)\);
near an endpoint the gap is of order
\(c\log(1/c)\). Thus even the conjectured improved barrier leaves a strict,
quantified gap above the cross-ratio lower bound throughout the open
non-Euclidean range.

## What is proved in the barrier literature

The following distinctions are essential.

- **Hildebrand lower bound.** Corollary 7.2 of
  [Hildebrand](https://doi.org/10.1007/s10107-012-0576-1) proves
  \(\nu\geq h(p)\). Remark 7.3 says the boundary contacts are optimal for
  that cross-ratio method. It does not construct a barrier and does not
  assert \(\nu_{\rm opt}=h(p)\).
- **Canonical upper bound.** Hildebrand's
  [canonical-barrier theorem](https://doi.org/10.1287/moor.2013.0640)
  supplies a \(3\)-LHSC barrier on every three-dimensional proper cone.
  This proves the upper side of (1), but the barrier is generally implicit.
  The unscaled characteristic function \(\log\zeta_p\) is another proven
  parameter-three intrinsic barrier by the universal-barrier theorem; its
  representation (2) is exact but integral-valued.
- **Chares's scaled characteristic function.** Section 3.2 of
  [Chares's thesis](https://perso.uclouvain.be/francois.glineur/files/theses/Chares-PhD-thesis-2007.pdf)
  derives an integral formula for \(\zeta_p\), tests self-concordance at
  finitely many randomized points, and conjectures the scaling
  \[
    \kappa=\begin{cases}p/(p+1),&p\geq2,\\
                         p/(2p-1),&1\leq p\leq2.
           \end{cases}
  \]
  The resulting proposed parameter is \(u(p)=3/(1+c)\). This is numerical
  evidence, not a proof. The obstruction (3) shows that the proposed scale
  for \(p>2\), if sufficient, is necessarily sharp within this scalar
  characteristic-function family.
- **Power-cone barriers are different.** Nesterov proved a parameter-four
  barrier for the three-dimensional power cone; Chares proved a
  parameter-three barrier and numerically conjectured a still smaller
  scaling. Roy and Xiao,
  [DOI 10.1007/s11590-021-01748-7](https://doi.org/10.1007/s11590-021-01748-7),
  proved a **different** Chares conjecture: the \((n+1)\)-parameter barrier
  for generalized power cones. It does not prove the smaller
  three-dimensional scaling. Likewise, recent exact formulas for the
  canonical barrier of a three-dimensional power cone do not apply to the
  \(p\)-norm epigraph. None of these results proves Chares's conjecture for
  \(K_p\).
  Modeling \(K_p\) by two three-dimensional power cones gives a valid but
  much weaker parameter-six ambient barrier.
- **Rational SOC lifts give only a large implicit intrinsic barrier.** For
  rational \(p=a/b\), \(K_p\) has a finite Lorentz-product lift. Under the
  bounded-fiber hypothesis satisfied by the standard construction,
  Chares's Theorem 5.2.1 shows that partial minimization of the product
  barrier along each lift fiber is a smooth self-concordant barrier with
  the same parameter. Homogeneous scaling of the fibers preserves
  logarithmic homogeneity. Thus this route does descend, but it retains the
  full parameter \(2s\) of its \(s\) Lorentz factors and requires solving a
  fiber analytic-center problem to evaluate it. It does not improve the
  canonical parameter-three upper bound.

The exact value of \(\nu_{\rm opt}(p)\) therefore remains open in the
non-Euclidean open range. The new result here is a sharp necessary boundary
scale for the characteristic ansatz, together with its strict separation
from Hildebrand's lower bound and exact endpoint asymptotics.

## Other lower-bound routes checked

The strict statement \(\nu_{\rm opt}(p)>2\) also has a short structural
proof, although Hildebrand's quantitative bound is stronger. In fact, every
proper cone admitting a \(2\)-LHSC barrier is linearly isomorphic to a
Lorentz cone. To see this directly, let \(F\) be such a barrier, fix
\(x\in\operatorname{int}K\), and take \(h\in\ker F'(x)\). Write
\(a=F''(x)[h,h]\) and \(b=F'''(x)[h,h,h]\). Logarithmic homogeneity gives

\[
 F''[h+tx,h+tx]=a+2t^2,
 \qquad
 F'''[h+tx,h+tx,h+tx]=b-6at-4t^3.                  \tag{23}
\]

Applying self-concordance at \(t=\pm\sqrt{a/2}\) forces \(b=0\).
Polarization shows that \(F'''\) vanishes on triples tangent to the level
set. For \(Q=e^{-F}\), which is two-homogeneous, one has \(D^3Q=0\) on
tangent triples, while homogeneity gives \(D^3Q[x,\cdot,\cdot]=0\).
Therefore \(Q\) is quadratic. Positive definiteness of \(F''\) gives its
signature \((1,n-1)\), and the barrier boundary condition identifies \(K\)
with a component of \(\{Q\geq0\}\). Thus \(K\) is Lorentz. Since
\(K_p\) is non-Lorentz for \(p\ne2\), parameter two is unattainable.

Two other natural routes do not improve \(h(p)\):

- Hildebrand's Remark 7.3 proves that his selected contacts optimize the
  cross-ratio method itself, so reoptimizing only those witnesses cannot
  strengthen the bound.
- The projective Dikin-ellipsoid sandwich gives
  \(\nu\geq1+2^{|1/p-1/2|}\) on the \(B_p^2\) base. This is strictly weaker
  than the known \(h(p)\) values in the tested non-Euclidean range; for
  example it is about \(2.12246\) at \(p=3\), versus
  \(h(3)\approx2.20711\).

## Audit checklist

- Verify the cone-coordinate Jacobian and factor two in (4).
- Justify differentiated regular variation in (6)--(7), including the
  contribution away from \(a=0\).
- Check that the one-dimensional restriction forces (8).
- Verify the exact comparison proof (9)--(12) and examples (13).
- Independently reproduce expansions (14)--(22).
- Screen later literature for a proof of Chares's \(p\)-norm-epigraph
  conjecture, without confusing it with the proved power-cone result.

The independent hostile audit verified (4) including its Jacobian and
constant, differentiated regular variation through order three, the
one-dimensional self-concordance limit, and the exact comparison
(9)--(12). It separately verified the nested-barrier obstruction (3a)--(3b),
including the nonsmooth range and both one-dimensional boundary limits.
Another audit verified the defining-function and bounded-correction no-go
(3c)--(3e), including its essential boundary-regularity qualification. A
second audit derived the asymptotic expansions and checked the literature
distinction between the \(p\)-norm epigraph and power cone. A third audit
checked the SOC partial-minimization boundary. No later proof of Chares's
conjecture or exact matching barrier was found.
