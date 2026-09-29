# Exact comparison at strongly monotone polynomial zeros

Date: 2026-09-28. Status: proved and passed
[fresh independent adversarial review](strong-monotone-cubic-posslp-upper-independent-review.md).
This extends the separately reviewed
[strongly convex quartic theorem](strong-convex-quartic-posslp-upper.md)
to polynomial maps that need not be gradients. The root supplied the
cut-preservation warm-start outline. Publication priority is unestablished.

Let \(T:\mathbb R^n\to\mathbb R^n\) be an explicitly encoded rational
polynomial map of degree at most three. The input supplies a positive
rational \(\mu\), with the global promise
\[
 \langle T(x)-T(y),x-y\rangle\ge\mu\|x-y\|^2
 \qquad(x,y\in\mathbb R^n).                              \tag{1}
\]
All norms below are Euclidean or their induced operator norms.
The input also supplies a rational polynomial \(h\) of degree at most
four. Its coefficients and monomials count toward the input length.

**Theorem.** The map \(T\) has a unique real zero \(p\). Each predicate
\(h(p)>0\), \(h(p)\ge0\), \(h(p)<0\), \(h(p)\le0\), or
\(h(p)=0\) reduces in deterministic polynomial time to one PosSLP
instance. Construction of that instance makes no oracle calls.

In particular, the theorem gives exact rational-threshold comparison
of equilibrium coordinates and of polynomial observables. It assumes
global strong monotonicity, with a supplied modulus, and has no domain
constraints. It does not cover arbitrary polynomial variational
inequalities on a constrained domain.

A fully verifiable format supplies a rational symmetric positive definite matrix
\(M\) such that
\[
 v^{\mathsf T}J_T(x)v
   =(v,x\otimes v)^{\mathsf T}M(v,x\otimes v).            \tag{2}
\]
Here \(J_T\) is the Jacobian, which need not be symmetric. If \(m\)
is the dimension of \(M\), take
\(\mu=\det M/(\operatorname{tr}M)^{m-1}\).
This rational number has polynomial bit length, is at most the least
eigenvalue of \(M\), and certifies (1) by integration on line segments.
The identity and positive definiteness are checkable in polynomial
time. Thus invalid certificates can be rejected, giving an ordinary
language rather than only a promise problem.

The gradient examples in the reviewed
[coordinate reduction](posslp-certified-cubic-root-reduction.md) and
[unconstrained-value reduction](unconstrained-quartic-posslp-reduction.md)
belong to this format. Consequently the order-comparison problems are
PosSLP-complete in that format. Equality has the upper bound above;
no matching equality hardness claim is made.

## 1. Existence and explicit local bounds

Handle \(n=0\) by direct rational comparison. Let \(L\ge2\) bound
the total input length, including \(\mu\) and \(h\). In the
certificate format it is enough to enlarge the original length
polynomially after computing \(\mu\). We can assume
\[
 n\le L,\qquad 2^{-L}\le\mu\le2^L,\qquad
 \max\left\{\sum_{i,\alpha}|T_{i,\alpha}|,
                 \sum_\alpha|h_\alpha|\right\}\le2^{2L}.
                                                               \tag{3}
\]
For a continuously differentiable map, (1) implies
\[
 \frac{J_T(x)+J_T(x)^{\mathsf T}}2\succeq\mu I
 \qquad(x\in\mathbb R^n),                               \tag{4}
\]
by applying (1) to \(x+tv,x\), dividing by \(t^2\), and
taking a limit. Conversely, (4) implies (1) by integration.
In particular,
\[
          \|J_T(x)v\|\ge\mu\|v\|,
          \qquad \|J_T(x)^{-1}\|\le\mu^{-1}.             \tag{5}
\]

For completeness, existence does not need an extra promise. On the
boundary of a ball of radius \(s>\|T(0)\|/\mu\), (1) gives
\(\langle T(x),x\rangle\ge\mu s^2-\|T(0)\|s>0\).
The continuous map \(x\mapsto\Pi_{\overline B(0,s)}(x-T(x))\)
has a fixed point by Brouwer's theorem. The projection inequality at
that point is
\(\langle T(x),y-x\rangle\ge0\) for every point \(y\) of
the ball. The choice \(y=0\) excludes a boundary fixed point.
At an interior fixed point the same inequality in every direction
forces \(T(x)=0\). Strong monotonicity proves uniqueness.
Applying (1) to this zero \(p\) and to \(0\) gives
\[
                 \|p\|\le\frac{\|T(0)\|}{\mu}
                         \le2^{3L}.                     \tag{6}
\]

Set
\[
 R=2^{4L},\qquad Q=[-R,R]^n,\qquad B=2^{30L},
 \qquad \rho=\frac{\mu}{4B}.                            \tag{7}
\]
On the ball of radius \(nR\), the same number \(B\) bounds
\(\|T(x)\|\), \(\|J_T(x)\|\), a Lipschitz constant for
\(J_T\), and \(\|\nabla h(x)\|\). To check the exponents,
put \(C=2^{2L}\) and use \(nR\le2^{5L}\).
The respective bounds
\[
 \sqrt n C(1+nR)^3,\quad
 3nC(1+nR)^2,\quad
 6n^{3/2}C(1+nR),\quad
 4\sqrt n C(1+nR)^3                                  \tag{8}
\]
are all at most \(B\) for \(L\ge2\).
For the third bound, bound each second partial derivative of each
component and then its bilinear operator norm; integration gives the
Jacobian Lipschitz estimate. The fourth estimate uses \(\deg h\le4\).
The closed radius-\(\rho\) ball around \(p\) lies strictly inside
\(Q\), because \(\rho<1\) and (6) leaves a larger margin.

## 2. A polynomial-bit rational Newton starting point

We give the warm-start argument explicitly because ordinary projected
gradient iteration would have a condition-number dependence that need
not be polynomial in the binary input length.

At any rational query point \(x\), use the following procedure.
If \(x\notin Q\), return the coordinate halfspace through \(x\)
that contains \(Q\). Otherwise evaluate \(T(x)\) exactly and
accept \(x\) if
\[
                         \|T(x)\|\le\mu\rho.             \tag{9}
\]
This test uses squared rational quantities and does not require a
square root. Acceptance gives \(\|x-p\|\le\rho\), since
\(\mu\|x-p\|\le\|T(x)\|\) by (1).

At a point \(x\in Q\) failing (9), return the central halfspace
\[
                   H_x=\{y:T(x)^{\mathsf T}(y-x)\le0\}.
                                                               \tag{10}
\]
The normal is nonzero. The Lipschitz bound in (8) gives
\(\|T(x)\|\le B\|x-p\|\), so a failed test implies
\(\|x-p\|>\mu\rho/B\). By (1),
\[
 T(x)^{\mathsf T}(p-x)\le-\mu\|x-p\|^2
                         <-\frac{\mu^3\rho^2}{B^2}.
                                                               \tag{11}
\]
Let
\[
                 \delta=\frac{\mu^3\rho^2}{2B^3}
                         =\frac{\mu^5}{32B^5}.          \tag{12}
\]
For \(\|y-p\|\le\delta\), the change in (11) is at most
\(B\delta\). Thus every halfspace (10) contains the fixed ball
\(K_1=\overline B(p,\delta)\). Since
\(\delta/\rho=\mu^4/(8B^4)<1\), this ball lies in \(Q\),
so every coordinate cut also contains it. The quantities \(R\),
\(\rho\), \(\delta\), and
\[
                       \nu=\frac12(\delta/n)^n            \tag{13}
\]
have polynomial bit length. A translated cube of side \(\delta/n\)
lies in \(K_1\), so \(\operatorname{vol}(K_1)>\nu\).

Apply the rational rounded central-cut ellipsoid algorithm starting
with the radius-\(nR\) ball and volume target \(\nu\). The
needed consequence is the following cut-or-stop form of the usual
proof: if each returned halfspace contains a fixed set \(K_1\),
then either the query procedure accepts, or after polynomially many
steps an ellipsoid of volume at most \(\nu\) still contains
\(K_1\). The latter alternative is impossible here.

This is the rational algorithm of Grötschel, Lovász and Schrijver,
[*Geometric Algorithms and Combinatorial Optimization*, Section 3.2](https://www.mpi-inf.mpg.de/fileadmin/inf/d1/ellipsoid-lovasz.pdf).
Theorem 3.2.1 and its proof, especially (3.2.8)–(3.2.10), give
polynomial bit length, containment, and volume decrease. Remark
3.2.33 explicitly allows cuts to retain a smaller fixed set than the
set associated with acceptance. Here acceptance is precisely (9);
we use only the containment and volume proof, without claiming that
acceptance tests membership in the unknown ball \(K_1\).
The separate [primary-source audit](monotone-warm-start-ellipsoid-source-audit.md)
checks this precise cut-or-stop consequence and the rounding requirements.

Normalize each nonzero normal to infinity norm one by exact rational
arithmetic. Polynomial evaluation at polynomial-bit rational centers
has polynomial bit cost because the degree is fixed. The rounded
ellipsoid therefore returns an explicit rational \(x_0\) of
polynomial bit length with \(\|x_0-p\|\le\rho\), in ordinary
polynomial time. For \(n=1\), interval bisection gives the same
cut-or-stop conclusion: each nonaccepting cut retains an interval of
length \(2\delta\), so the interval cannot keep halving past that
length. No PosSLP query is used in either case.

## 3. Exact rational Newton circuits

Starting at \(x_0\), define
\[
                   x_{k+1}=x_k-J_T(x_k)^{-1}T(x_k).       \tag{14}
\]
Let \(e_k=\|x_k-p\|\). The Jacobian Lipschitz bound, (5),
and the integral expression for \(T(x_k)-T(p)\) give
\[
                         e_{k+1}\le\frac{B}{2\mu}e_k^2.
                                                               \tag{15}
\]
No symmetry is used in this estimate. Since \(e_0\le\rho\),
the scaled errors \(Be_k/(2\mu)\) start at most \(1/8\)
and square at each step. Consequently all iterates remain in the
radius-\(\rho\) ball around \(p\), and
\[
              e_k\le\frac{2\mu}{B}2^{-3\cdot2^k}
                     \le2^{L+1-3\cdot2^k}.              \tag{16}
\]

To implement (14) by a fixed rational arithmetic circuit, compute
\(J=J_T(x_k)\) and solve
\[
                         J^{\mathsf T}Jd=J^{\mathsf T}T(x_k)
                                                               \tag{17}
\]
by rational \(LDL^{\mathsf T}\) elimination. The matrix in (17)
is symmetric positive definite, so all pivots are positive and no
pivot selection or sign queries are required. Its solution is exactly
\(d=J^{-1}T(x_k)\). We do not apply symmetric elimination to the
possibly nonsymmetric matrix \(J\) itself. Shared nodes give a
polynomial-size rational circuit for any polynomial number of Newton
steps; expanded coordinate fractions need not have polynomial length.

## 4. Separation and a single exact comparison

Let \(\alpha=h(p)\). The real formula
\[
      \exists x\in\mathbb R^n:\quad T(x)=0,\quad z=h(x)   \tag{18}
\]
defines precisely the singleton \(\{\alpha\}\). After clearing
denominators, its polynomials have degree at most four and coefficient
bit lengths polynomial in \(L\).

Basu's author survey,
[*Algorithms in Real Algebraic Geometry: A Survey*](https://www.math.purdue.edu/~sbasu/raag_survey2011.pdf),
Theorem 2.16, gives one-block quantifier-elimination degree and
coefficient-bit bounds. As in the
[quartic proof, Section 4](strong-convex-quartic-posslp-upper.md#4-a-uniform-algebraic-separation-bound),
there is a fixed effective polynomial \(a(L)\), enlarged to have
nonnegative integer coefficients and \(a(L)\ge60L+10\), such that
\(\alpha\) is a root of a nonzero integer polynomial of degree
at most \(2^{a(L)}\) and coefficient magnitudes at most
\(2^{2^{a(L)}}\). Indeed, a quantifier-free description of a
singleton must contain a nonzero polynomial vanishing at its point;
otherwise every sign test is locally constant. No assumption on the
dimension of the complex zero set of \(T\) is needed.

Removing any power of \(z\) from that polynomial and comparing
its nonzero integer constant term to the remaining terms proves
\[
              \alpha\ne0\quad\Longrightarrow\quad
              |\alpha|\ge g:=2^{-2^{a(L)+1}}.           \tag{19}
\]
Quantifier elimination is used only to prove this bound; it is not
executed by the reduction. The rational \(g\) has a circuit with
\(a(L)+1\) repeated squarings starting from \(1/2\).

Take \(k=a(L)+2\) Newton steps and put
\(\widehat\alpha=h(x_k)\). Equations (8) and (16) give
\[
 |\widehat\alpha-\alpha|
       \le Be_k\le2^{31L+1-12\cdot2^{a(L)}}\le g/8.      \tag{20}
\]
The last inequality follows from
\(31L+4\le10\cdot2^{a(L)}\).
The following rational circuit expressions are positive exactly for
the respective predicates:

| Predicate | Circuit expression |
| --- | --- |
| \(\alpha>0\) | \(\widehat\alpha-g/2\) |
| \(\alpha\ge0\) | \(\widehat\alpha+g/2\) |
| \(\alpha<0\) | \(-\widehat\alpha-g/2\) |
| \(\alpha\le0\) | \(-\widehat\alpha+g/2\) |
| \(\alpha=0\) | \(g^2/4-\widehat\alpha^2\) |

Each expression has a nonzero sign on the promised input class,
including when \(\alpha=0\).
Replace each rational gate by an integer numerator and positive
integer denominator. In particular, with positive \(D_a,D_b\),
division by a nonzero \(N_b/D_b\) uses
\[
 \frac{N_a/D_a}{N_b/D_b}
      =\frac{N_aD_bN_b}{D_aN_b^2}.                       \tag{21}
\]
Thus no denominator sign test is required. All divisions above are
by nonzero quantities. Binary constants and rational initial data
have polynomial-size integer circuits. The numerator of the selected
final expression is the single PosSLP instance.

## 5. Scope, degree frontier, and prior work

The extension includes nonpotential equilibrium maps. For example,
\[
 T(x)=(1+\|x\|^2)x+Ax-b,
 \qquad A^{\mathsf T}=-A,
\]
with rational \(A,b\), has symmetric Jacobian
\((1+\|x\|^2)I+2xx^{\mathsf T}\succeq I\).
It has a full positive definite Gram of the form (2), whereas a
nonzero skew matrix \(A\) prevents \(T\) from being a gradient.
The class also allows a nonconstant antisymmetric Jacobian. In two
variables, take
\[
 T(x,y)=(1+x^2+y^2)(x,y)+(x^2y/2,0).
\]
For \(z=(xv_1,xv_2,yv_1,yv_2)\), its certificate is
\[
 v^{\mathsf T}J_T(x,y)v=\|v\|^2+z^{\mathsf T}Q_0z,
 \qquad
 Q_0=\begin{pmatrix}
 3&1/4&1/2&2\\
 1/4&1&0&0\\
 1/2&0&1&0\\
 2&0&0&3
 \end{pmatrix}.
\]
The leading principal minors are
\(3,47/16,43/16,65/16\), all positive. Also
\((J_T)_{12}-(J_T)_{21}=x^2/2\), so this map cannot be
a gradient plus a fixed skew linear map. Adding a rational constant
vector changes neither certificate nor derivative identity.

The result can therefore describe exact comparisons in suitably
strongly monotone polynomial equilibrium models beyond potential
games. Whether natural application data admit such a supplied
certificate, and whether the circuit representations help practical
solvers, remain application-specific questions. No numerical speedup
is proved.

There is also an elementary degree frontier. If a globally strongly
monotone polynomial map has degree at most two, its symmetric
Jacobian is affine and positive definite on every real line. Each
linear coefficient must therefore vanish. Subtract its constant
symmetric part times \(x\); the remaining vector field \(U\)
satisfies \(\partial_iU_j+\partial_jU_i=0\).
Differentiating these identities for the pairs \((i,k),(j,k),(i,j)\)
in directions \(j,i,k\), respectively, and adding the first two
minus the third gives \(2\partial_i\partial_jU_k=0\).
Hence \(T\) is affine. Its zero and every fixed-degree rational
polynomial observable there are computable by polynomial-time
rational linear algebra. Cubic degree is the first possible degree
for the hardness construction. This does not separate P from PosSLP.

The precision-and-circuit method is established prior work.
Etessami, Stewart and Yannakakis,
[*Polynomial Time Algorithms for Multi-type Branching Processes and
Stochastic Context-Free Grammars*](https://arxiv.org/pdf/1201.2374v2),
Appendix C, Corollary C.8, already combine an algebraic gap, exact
Newton iterations, shared arithmetic circuits, and a single final
threshold to prove PosSLP equivalence for probabilistic polynomial
system coordinates. Their fixed-point assumptions differ from (1).
The present extension adds this target class and its matching
gradient-subclass lower bound; it does not introduce that architecture
or the classical ellipsoid warm-start method.

The [focused prior audit](strong-convex-quartic-posslp-upper-prior.md),
[monotone-system source supplement](strong-monotone-exact-prior-supplement.md),
and [independent broader audit](monotone-polynomial-posslp-prior-independent.md)
compare finite SOS methods, variational inequalities, real-computation
frameworks, and implicit fixed-point gates. The sources checked there
do not establish an equivalent theorem for this particular input
class. That observation is not evidence of priority, and publication
novelty remains unestablished.

## 6. Verification status

The fresh proof review independently reconstructed existence, the
retained-ball cuts, the rational ellipsoid argument, nonsymmetric
Newton iteration, algebraic separation, all five predicates,
certificate verification, lower-bound transfer, and the degree
frontier. It also checked both nonpotential examples. The separate
source audit verifies the precise GLS dependency; it does not by
itself verify the application inequalities.

The reviewer ran exact rational finite checks of derivative bounds,
retained radii, nonsymmetric linear solves, local Newton steps,
threshold margins, and division elimination. Their review records
the commands and limits of these checks. The author read that review
without rerunning its checks. Independently, an author inline
`python -` command using SymPy verified the variable-skew example's
polynomial Gram identity, four positive leading principal minors,
and nonconstant antisymmetric Jacobian.

Author targeted checks also passed:

- `git diff --check -- research-20260927/strong-monotone-cubic-posslp-upper.md research-20260927/monotone-warm-start-ellipsoid-source-audit.md`.
- An inline `python -` document check of this note, its source audit,
  and the preceding quartic theorem and proof review: four files,
  14 local links, paired math delimiters, whitespace, control
  characters, and unescaped math-mode spacing commands. An earlier
  run detected the missing backslash in (18), which was repaired.

No implementation of the ellipsoid algorithm or full reduction,
Lean verification, project-wide tests, or CI inspection is claimed.
