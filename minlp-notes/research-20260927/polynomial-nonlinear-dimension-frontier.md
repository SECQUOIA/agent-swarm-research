# Exact convex polynomial feasibility with few nonlinear directions

Date: 2026-09-28. Status: proof and
[fresh full adversarial review](polynomial-nonlinear-dimension-review.md)
completed; no remaining gap was found after the lattice-map precision
repair in Section 6. A separate
[source-interface audit](polynomial-nonlinear-dimension-oracle-audit.md)
and independent oracle review checked that repair. Novelty is not established.

## 1. Model and result

Consider rational polynomial inequalities

\[
 C_i v+p_i(z,u)\le0\quad(i=1,\ldots,m),
 \qquad z\in\mathbb Z^k,\quad u\in\mathbb R^r,
 \quad v\in\mathbb R^n.                                  \tag{1}
\]

Every \(p_i\) is globally convex and has degree at most \(d\). The row
vectors \(C_i\) are constant and rational. Affine inequalities and affine
equalities are allowed; an equality is represented by its two affine weak
inequalities. Coefficients and monomials are explicitly encoded, with total
binary length \(N\ge2\). Put \(D=\max(2,d)\).

**Theorem.** Exact feasibility of (1) can be decided, and a feasible
original integer assignment returned when one exists, in

\[
                            f(k,r,d)N^C                    \tag{2}
\]

bit operations, where \(f\) is computable and \(C\) is an absolute
constant. Neither integer nor continuous bounds need be supplied. No Slater
condition or rational continuous feasible point is assumed. In particular,
continuous feasibility is fixed-parameter tractable in \((r,d)\).

The output here is a decision and, when applicable, the original integer
vector. The auxiliary grid coordinates used by the algorithm need not extend
to an exactly feasible continuous point of the original problem. An FPT
exact continuous algebraic witness or optimal-value algorithm is not asserted.

This extends the [quadratic common-range framework](common-range-fpt-frontier.md)
to convex polynomial inequalities. Unlike the quadratic and cone proof, the
algorithm does not require a compact polyhedral approximation of each
nonlinear row. Instead it uses a controlled relaxation, a grid only in the
\(r\) nonlinear continuous coordinates, and an implicit-polynomial version
of an established integer algorithm. The potential MINLP use is exact
feasibility certification for models with many linear continuous variables
but few nonlinear aggregate coordinates. Practical speedup and usable
precision constants remain unproved.

### 1.1 An intrinsic parameter on a supplied formulation

The form (1) can also be recognized from a convex polynomial formulation
\(g_i(z,x)\le0\). Define

\[
 K=\{a\in\mathbb R^n:
       \nabla^2 g_i(z,x)(0,a)=0
       \text{ identically in }(z,x)\text{ for every }i\},
 \qquad r=\operatorname{codim}K.                          \tag{3}
\]

Stacking the rational coefficient matrices of the polynomial Hessians
computes \(K\) by rational linear algebra. Its basis and a complement have
polynomial-bit coefficients. Write \(x=T_1u+T_0v\). The identity in (3)
says that every directional derivative along \((0,T_0v)\) is constant,
so

\[
 g_i(z,T_1u+T_0v)=p_i(z,u)+C_i v.
\]

Restriction preserves convexity. Compute \(p_i\) by substituting
\(x=T_1u\), and compute \(C_i\) from the gradient at zero. Expansion now
involves only \(k+r\) variables; its monomial count is at most
\(\binom{k+r+d}{d}\). Thus this recognition and conversion costs
\(f(k,r,d)N^{O(1)}\), not an uncontrolled expansion in the original
continuous dimension. For continuous models, take \(k=0\).

For globally convex inputs, the same space can be computed using only the
continuous Hessian blocks \(\nabla^2_{xx}g_i(z,x)\). Indeed, if such a
block annihilates \(a\) at every point, then the full positive-semidefinite
Hessian has zero quadratic form at \((0,a)\), and therefore annihilates
that vector as well. Thus a direction that is everywhere affine within
continuous fibers cannot have a hidden bilinear term \(z_jv_\ell\) in a
globally convex polynomial. Without global convexity this implication
fails, and a variable coefficient on \(v\) would invalidate the
constant-matrix projection below.
Convexity of the input polynomials is an assumption; checking convexity is
not needed by the feasibility algorithm described here.

## 2. Implicit projection and quantitative bounds

Let \(C\) collect the rows \(C_i\), and define

\[
 \Lambda=\{\lambda\ge0:C^T\lambda=0,\ \mathbf1^T\lambda=1\}.
                                                               \tag{4}
\]

If this set is empty, the corresponding dual conditions are vacuous.
Otherwise it is a compact rational polytope. Farkas' lemma gives

\[
 \exists v\ Cv+p(z,u)\le0
 \quad\Longleftrightarrow\quad
 \lambda^Tp(z,u)\le0\quad
           \text{for every vertex }\lambda\text{ of }\Lambda.
                                                               \tag{5}
\]

Every vertex has support at most \(\operatorname{rank}C+1\); rational
minor bounds give polynomial coefficient bits. The implicit projected
polynomials therefore have degree at most \(d\), individual coefficient
bits \(N^{O(1)}\), and row count \(S\) with
\(\log(S+1)\le N^{O(1)}\). Nonnegative combinations preserve convexity.
The projection is exactly this basic closed set, so its closedness is proved
from the constant matrix, rather than assumed for an arbitrary projection.
No algorithm below lists its vertices or its projected inequalities.

If a rational number of bit length \(L\) is appended to the model, the
bounds on individual coefficients remain linear in \(L\), up to fixed
polynomial factors in structural input size. This follows from determinant
bounds and coefficient sums. This coefficient sensitivity prevents repeated
radius and gap steps from introducing an input exponent depending on the
parameters.

### 2.1 Small continuous witnesses

For integer polynomials in \(s\) variables of degree at most \(D\),
coefficient bit length \(\tau\), and row count \(S\),
[Basu--Roy, Theorems 3 and 4](https://www.math.purdue.edu/~sbasu/jsc_final-06-05-10.pdf)
give radius bounds with

\[
 \log(2+R)\le(\tau+\log(S+1)+1)D^{O(s)}.                  \tag{6}
\]

Theorem 4 gives a ball meeting every nonempty connected component, including
unbounded ones. Theorem 3 gives a ball containing every bounded connected
component. Their distinct quantifiers are essential below. The explicit
formulas were inspected in the local final author manuscript, pages 3--5.

For any fixed rational \(z\), apply the meeting bound to (5) in the
\(r\) variables \(u\). It supplies a small feasible \(u\). Its fiber in
\(v\) is a nonempty polyhedron with rational matrix and algebraic or real
right-hand side. The minimum-norm point of that polyhedron satisfies the
active-normal formula

\[
 v=C_I^T(C_IC_I^T)^{-1}[-p_I(z,u)]                         \tag{7}
\]

for a linearly independent set of active row normals; if none is active,
that point is zero. Rational minors and direct polynomial evaluation bound
\(\|v\|\) in terms of \(\|z\|\), \(\|u\|\), and the input.
Consequently, on any integer box with endpoint bit length \(L\), every
nonempty fiber has a point with

\[
 \|(u,v)\|_\infty\le R,\qquad
 \log R\le (L+1)f(r,d)N^{C_0},\qquad R\ge2.             \tag{8}
\]

The bound is uniform and computable without enumerating integer assignments.
When \(r=0\), omit the radius theorem in zero dimensions and use (7)
directly.

### 2.2 A uniform positive infeasibility gap

Fix an integer box and a finite rational box \(B\) for \((u,v)\). For
fixed \(z\), let

\[
 \alpha_z=\min_{(u,v)\in B}
                  \max(0,C_1v+p_1(z,u),\ldots,C_mv+p_m(z,u)).
                                                               \tag{9}
\]

Choose a rational upper bound \(U\ge1\) for this maximum on the box.
Project \(v\) from the compact truncated residual epigraph

\[
 (u,v)\in B,\quad 0\le t\le U,\quad
                     C_i v+p_i(z,u)\le t.
\]

Its image \(E_z\) in \((u,t)\) is compact and has a Farkas description
with degree at most \(D\), individual coefficient bits polynomial in the
input and box bits, and logarithmic row count polynomial in the input.
If \(\alpha_z>0\), then

\[
 H_z=\{(u,t,y):(u,t)\in E_z,\ y\ge0,\ ty=1\}
                                                               \tag{10}
\]

is compact. Its maximum \(y\) equals \(1/\alpha_z\). Apply the
**containing** radius bound in \(r+2\) dimensions to obtain a computable
uniform \(\Delta>0\) such that

\[
                       \alpha_z=0\quad\text{or}\quad
                       \alpha_z\ge\Delta,                  \tag{11}
\]

with \(\log(1/\Delta)\) bounded by input and box bits times
\(f(r,d)\). The meeting radius alone would not imply this statement.
Taking the box \(B=[-2R,2R]^{r+n}\) after (8) preserves a bound of the
form \(f(k,r,d)N^{C_1}\) when the integer-box bits have that form.

### 2.3 A small integer assignment

The real projection of (1) onto \(z\) is convex. Formula (5) describes it
by a first-order formula with one existential block of \(r\) variables,
individual degree at most \(D\), and individual coefficient bits
\(N^{O(1)}\). The formula can have exponentially many predicates.

[Khachiyan--Porkolab, Theorem 1.1](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf)
bounds an integer witness independently of that predicate count. Its
feasibility reduction appends an integer coordinate fixed to zero. Therefore
there is an effectively computable integer \(B_z\ge1\) with

\[
 \log B_z\le N^{C_2}D^{O((k+1)^4(r+1))}                  \tag{12}
\]

such that, if feasible, (1) has a feasible integer vector in
\([-B_z,B_z]^k\). For \(r=0\), use the quantifier-free form or an unused
quantified variable. For \(k=0\), this step is unnecessary. Only the
witness bound is imported; the exponential formula is never constructed.

## 3. Continuous exact feasibility through a controlled relaxation

The continuous case already follows from a standard rational ellipsoid
feasibility algorithm, without integer programming. Take \(R\) from (8)
and the gap \(\Delta\) for the wider box \([-2R,2R]^{r+n}\). Set
\(\varepsilon=\Delta/4\). On that box, direct coefficient estimates
give a rational Lipschitz bound \(L\ge1\) for all original row functions,
with \(\log L\le f(r,d)N^{O(1)}\).

If the original system is feasible, one feasible point lies in
\([-R,R]^{r+n}\). The relaxed set

\[
 C_i v+p_i(u)\le\varepsilon\quad\forall i,
       \qquad (u,v)\in[-2R,2R]^{r+n}
                                                               \tag{13}
\]

then contains a ball of known radius at least
\(\min(1,\varepsilon/(2L))\), after defining \(L\) for Euclidean
changes. If the original system is infeasible, (11) makes (13) empty.
At a rational query point a violated convex polynomial supplies its rational
gradient as a separating hyperplane. If that gradient vanishes, convexity
certifies that the violated relaxed inequality is infeasible everywhere.
Box violations supply affine cuts.

The rational ellipsoid algorithm distinguishes an empty bounded convex set
from one containing a ball of the stated radius using a number of bit
operations polynomial in the ambient dimension, the input bits, and the
logarithm of the outer-to-inner radius ratio. These quantities have the form
\(f(r,d)N^{O(1)}\). Polynomial evaluation and gradients have that cost as
well. This proves the continuous instance of (2). Exact feasibility is
inferred from the gap; the rational relaxed point need not be an original
feasible point.

## 4. Reduce the mixed-integer case to a strict integer problem

Use (12) to impose \(|z_j|\le B_z\). Use (8) to find a uniform \(R\),
and (11) to find a uniform gap in \([-2R,2R]^{r+n}\). Set
\(\varepsilon=\Delta/4\). On
\(|z|\le B_z,\ |u|\le2R\), let \(L_u\ge1\) bound the sum of the
absolute \(u\)-partial derivatives of every \(p_i\). A coefficient
estimate gives \(\log L_u\le f(k,r,d)N^{O(1)}\).

Choose a positive dyadic mesh \(\delta\) satisfying

\[
                 \delta\le\tfrac12,\qquad
                 L_u\delta\le\varepsilon/4.              \tag{14}
\]

Introduce \(a\in\mathbb Z^r\), representing the grid coordinate
\(u=\delta a\). Consider the following **strict** system in
\((z,a)\in\mathbb Z^{k+r}\) and continuous \(v\):

\[
 \begin{split}
 C_i v+p_i(z,\delta a)&<\varepsilon &&(i\le m),\\
 |z_j|&<B_z+1,\\
 |\delta a_j|&<2R,\\
 |v_j|&<2R.
 \end{split}                                               \tag{15}
\]

All its numbers have bit length \(f(k,r,d)N^{O(1)}\).

If (1) is feasible, choose the small integer assignment and a continuous
point with \(|u|,|v|\le R\). Round each \(u\) coordinate to the nearest
multiple of \(\delta\), retaining \(z,v\). The change in each original
residual is at most \(L_u\delta\le\varepsilon/4\), and all wider box
inequalities are strict. Thus (15) has an integer point in its \((z,a)\)
projection.

Conversely, (15) implies \(|z|\le B_z\) because \(z\) is integral.
It supplies a point of the wider continuous box with maximum original
residual less than \(\varepsilon<\Delta\). By (11), the original fiber
at that same \(z\) is feasible. Hence

\[
 (1)\text{ is feasible}
 \quad\Longleftrightarrow\quad
 (15)\text{ has a point with }(z,a)\in\mathbb Z^{k+r}.      \tag{16}
\]

This grid is not enumerated. Its scaled coordinates become additional
integer variables in a fixed-dimension integer algorithm. The parameter
pays for exactly \(r\) additional integers, regardless of the number of
linear continuous variables.

## 5. An exact oracle for the implicit strict polynomial family

Write (15) as

\[
                         \widehat C v+b(z,a)<0,             \tag{17}
\]

including all its box rows. Normalize the associated dual cone by

\[
 \widehat\Lambda=
 \{\lambda\ge0:\widehat C^T\lambda=0,
                              \mathbf1^T\lambda=1\}.
\]

This polytope is nonempty because the opposite \(v\)-box rows or the
zero-\(v\)-coefficient \((z,a)\)-box rows supply a nonzero dual vector;
the empty-dimensional special case is handled directly. The fixed finite
strict polynomial family is

\[
 F_\lambda(z,a)=\lambda^Tb(z,a)<0
             \quad\text{for vertices }\lambda
                        \text{ of }\widehat\Lambda.        \tag{18}
\]

Its projection equals the projection of (17). To see this with strict
inequalities, solve at a fixed rational \((z,a)\) the LP

\[
 \min_{v,s} s\quad\text{subject to}\quad
                     \widehat C v+b(z,a)\le s\mathbf1.     \tag{19}
\]

It is feasible, has a finite attained optimum, and its dual is
\(\max_{\lambda\in\widehat\Lambda}\lambda^Tb(z,a)\).
The opposite box rows give finiteness, and ordinary linear programming
strong duality applies. Strict feasibility holds exactly when this optimum
is negative. If it is nonnegative, an optimal dual vertex supplies one
violated polynomial \(F_\lambda\ge0\).

Thus a rational LP gives exact membership in the fixed strict set, or returns
one violated convex polynomial from that set's fixed defining family. A
basic optimal dual solution can be obtained by standard exact LP algorithms
or rational linear postprocessing. Its coefficient bits are bounded by
minors of the constant matrix, independently of the rational query point.
Each \(F_\lambda\) has degree at most \(D\), at most
\(\binom{k+r+D}{D}\) monomials, and coefficient bit length
\(f(k,r,d)N^{O(1)}\). Clear denominators separately in each selected row
by a positive multiplier. This preserves strict signs and convexity. No
common denominator across all implicit rows is formed.

The strictness in (18) is deliberate. Replacing a weak integral row
\(F\le0\) by \(F-1<0\) preserves integer points but changes membership
at rational, noninteger oracle queries. The LP oracle must describe the
same fixed strict family that the integer algorithm uses. Equations
(17)--(19) ensure that requirement.

## 6. Adapt an established fixed-dimension integer algorithm

[Hildebrand--Köppe, *A new Lenstra-type Algorithm for Quasiconvex Polynomial
Integer Minimization*, Sections 4--6](https://arxiv.org/pdf/1006.4661)
provides the required algorithmic mechanism. The theorem as printed takes
an explicit family; the following is an adaptation of its proof, not a claim
that its displayed input already includes implicit families.

Let \(q=k+r\). Section 4 leaves membership and shallow-cut work as oracle
costs. In Theorem 5.7, the explicit row list is used to test a number of
rational points depending only on \(q\), and to obtain one violated
polynomial if a test point is outside the set. Subsequent work evaluates
that polynomial and its gradient. Replace the row scan by (19).

For convex polynomials, the shallow-cut argument has the following explicit
implementation. Suppose the current \(s\)-dimensional ellipsoid is
\(E(A,c)=\{c+A^{1/2}w:\|w\|_2\le1\}\), with rational positive
definite \(A\). Compute a rational decomposition
\(A=L\operatorname{diag}(d_i)L^T\). Choose positive dyadic numbers
\(t_i\) with \(\sqrt{d_i}/2\le t_i\le\sqrt{d_i}\), by exact rational
comparisons, and query the \(2s\) points

\[
                         c\pm\frac{t_iLe_i}{s+1}.         \tag{20}
\]

Their ellipsoidal norms are at most \(1/(s+1)\). If they all belong to
the strict convex set, their convex hull contains
\(E(A/\beta^2,c)\), where the rational choice
\(\beta=2s(s+1)\) suffices: in normalized coordinates the hull contains
the cross-polytope of radius \(1/[2(s+1)]\), and hence the Euclidean ball
of radius \(1/[2(s+1)\sqrt{s}]\).

Otherwise the oracle supplies a convex polynomial \(F\) with \(F(y)\ge0\)
at one tested point \(y\). If \(g=\nabla F(y)\ne0\), convexity gives
\(g^Tx<g^Ty\) for every point of the strict family, and

\[
            g^Ty\le g^Tc+\frac{\sqrt{g^TAg}}{s+1},        \tag{21}
\]

which is precisely the required shallow-cut offset. If \(g=0\), global
convexity implies \(F\ge F(y)\ge0\) everywhere, certifying emptiness.
The rational rounding construction and existing ellipsoid updates thus
need only \(2s\) LP membership queries and one selected-row gradient,
with a rounding factor depending only on dimension. The sharper rounding
factor in the source is unnecessary for the FPT conclusion.

Two other obligations of the proof remain valid for an implicit family:

1. **A volume bound at integer feasible points.** After positive denominator
   clearing, every strict row has integer coefficients with a uniform bit
   bound \(H\). At an integer feasible point its value is at most \(-1\).
   On a supplied bounding ball, a uniform coefficient bound gives a uniform
   gradient bound. For example, if the bounding ball has radius \(T\ge1\),
   and each row has at most \(M\) monomials, a radius smaller than
   \([4qMD2^H(T+1)^D]^{-1}\) suffices, with harmless enlargement for
   zero-degree rows. It lies inside every strict row simultaneously. The
   bit length of its radius is
   polynomial in \(H\), the bounding-radius bits, \(q\), and \(D\),
   independent of the number of rows. This is the content of Lemma 6.1;
   the elementary gradient argument also proves the needed version here.
2. **Recursive lattice sections.** Remarks 5.5--5.6 retain integer affine
   coordinate maps and evaluate an original polynomial at the lifted rational
   query point; gradients follow by the chain rule. The LP oracle can be
   called at exactly that lifted point. The returned original row remains
   convex and has the same degree after restriction. The transformed bounding
   quadratic can acquire linear terms; it remains an affine ellipsoid and
   need not be centered at the origin. Remark 5.5 assumes a short coordinate
   map, so it does not by itself prove the needed input exponent. The direct
   bound below supplies that hypothesis. No implicit row enumeration is
   introduced by recursion.

Here is the remaining lattice and coefficient accounting. For an ellipsoid
\(E(A,c)\) of coefficient bit length \(H\), minimize the rational positive
definite quadratic form \(a^TAa\) over nonzero integer \(a\). This is the
minimum of \(2s\) convex integer quadratic programs with constraints
\(a_j\ge1\) or \(a_j\le-1\). Each can be solved in FPT time in \(s\)
by [Del Pia, Theorem 3](https://arxiv.org/pdf/2311.00099v2). The same theorem
minimizes \((y-c)^TA^{-1}(y-c)\) over integer \(y\), deciding whether the
inner ellipsoid contains a lattice point and returning one if so. These
are rational quadratic forms; no irrational square-root lattice basis is
supplied to an algorithm.

A shortest nonzero direction \(a\) is primitive and satisfies
\(a^TAa\le A_{11}\). Rational determinant and eigenvalue bounds give
\(\lambda_{\min}(A)\ge2^{-\operatorname{poly}(s)(H+1)}\), hence
\(\operatorname{bitsize}(a)\le\operatorname{poly}(s)(H+1)\). If the
inner ellipsoid is lattice-free, the classical ellipsoidal flatness bound
limits the number of integer hyperplanes \(a^Ty=t\) meeting the outer
ellipsoid by a function of \(s\) and \(\beta\). Their integers \(t\)
have bit length \(\operatorname{poly}(s)(H+1)\).

Extended gcd operations construct a unimodular integer matrix \(U\) with
\(a^TU=e_s^T\), whose entries and inverse have the same type of linear
bit bound. The correct lattice section is \(y=U(w,t)\),
\(w\in\mathbb Z^{s-1}\). Merely choosing \(a\) as a column of a
unimodular matrix would not parameterize the required hyperplane. A fresh
strict bounding ball for \(w\) follows from the original radius and
\(\|U^{-1}\|\). Restricted row coefficients and that radius have bit
length at most \(f(s,D)\) times the old bit bound plus one.

Use the rational shallow-cut method with its controlled rounded ellipsoid
updates. Its output precision is linear in the row and volume-threshold bit
bounds, times dimension and degree factors, as in Hildebrand--Köppe
Corollary 5.8. Thus one recursive level has a bound
\(L_{\rm next}\le f(s,D)(L+1)\). At most \(q\) levels give
\(f(q,D)\) times the initial bit bound. Merely iterating an unspecified
polynomial precision bound would not prove FPT. The
[oracle audit](polynomial-nonlinear-dimension-oracle-audit.md) gives the
full derivation and records the independent correction to this point.

Append one explicit strict quadratic ball inequality containing all the
\((z,a)\) boxes in (15), to match the bounded input of their Theorem 6.3.
Its radius has bit length \(f(k,r,d)N^{O(1)}\). Empty or zero-dimensional
integer sections are handled directly by the membership LP. The modified
algorithm therefore has \(f(q,D)\) times a fixed polynomial in the LP
oracle's input length and coefficient bounds. Its bit cost has the form
(2). It returns a grid integer point \((z,a)\) when one exists; (16)
certifies that its \(z\) is a feasible original assignment.

The original continuous dimension affects only the polynomial size of the
LP oracle. It does not become the dimension of the lattice algorithm.

## 7. Prior work, limitations, and verification obligations

The polynomial radius bounds, Farkas projection, integer-witness theorem,
and Lenstra-type integer method are established. Hildebrand--Köppe already
gives true FPT dependence on total polynomial variable dimension and degree
for an explicit convex or quasiconvex polynomial family. Toledo's implicit
convex optimization results also predate this work. Its generic sequential
arithmetic bound has a dimension-dependent exponent, but the explicit-row
application of its parallel theorem has only dimension-dependent powers
of logarithms of the row count. Those powers are compatible with FPT
arithmetic complexity; exact Turing precision and the restricted evaluator
interface require a separate comparison. The proposed addition
is the exact fixed-parameter bit bound with an unrestricted linear
continuous lift, using an implicit family and a quantitatively certified
grid reduction. The [prior audit](polynomial-nonlinear-dimension-prior.md)
records the inspected sources and precise scope comparisons. Unsuccessful
searches do not establish novelty.

The proof requires constant coefficients on \(v\), globally convex
polynomial rows, explicit coefficient encoding, and the parameters
\((k,r,d)\). Convexity of the resulting feasible set alone does not supply
the convex separation polynomials used in Section 6. The separately reviewed
[quasiconvex extension](quasiconvex-polynomial-nonlinear-dimension-frontier.md)
uses the structure of extreme Farkas multipliers and a different separation
step to cover globally quasiconvex native polynomials. The latter step is
necessary because a zero gradient at a violated point need not certify
emptiness for a quasiconvex row. No general rational polyhedral
lift of polynomial epigraphs is asserted.

The positive gap, the grid, and the row-wise integer scaling can all have
large parameter-dependent bit lengths. The algorithm is a theoretical exact
decision procedure. Whether it yields a useful implementation or supports
practical speedups remains open. The separately reviewed
[full optimization theorem](polynomial-nonlinear-dimension-optimization.md)
now supplies exact optimal values and continuous witnesses in the same
parameterized bit bound when the objective uses the same nonlinear core.

The author directly inspected Basu--Roy's radius statements and
Hildebrand--Köppe Sections 4--6, including the sparse evaluation and recursive
map conventions. A separate investigator checked the same oracle interface
independently. The full adversarial review checked the radius and gap,
integer bounds, strict grid reduction, intrinsic parameter, and repaired
FPT bit accounting. The initial appeal to a source remark had not justified
short lattice maps; the revised proof derives their bounds and correct
unimodular sections directly. This correction was independently rechecked.
No project-wide verification or CI inspection was performed.

The targeted command
`python research-20260927/check_polynomial_nonlinear_dimension.py` passed
exact strict-quartic projection and boundary identities, 42 rational
ellipsoid test points in dimensions one through six, and the unimodular
lattice-section correction. These examples check the strictness convention,
the selected dual polynomial, rational ellipsoidal norm bounds, and the
failure of an incorrect column-completion rule. They do not verify the
general radius, gap, bit-recursion, or lattice algorithm arguments. A
targeted document check also passed for local links, paired math delimiters,
whitespace, control characters, and the final newline.
