# Exact SOCP feasibility from the span of the squared constraint Hessians

Date: 2026-09-27. Status: the complete proof and rational cone construction
have passed independent adversarial review after two statement clarifications.
The nonconvex quadratic certificate theorem used below has completed two
independent reviews. A subsequent coefficient-size refinement restores the
same exponent for inputs without boxes; its application here has passed a
separate independent review. The priority audit found important classical special
cases, and novelty has not been established.

Rational second-order cone systems with fixed squared-Hessian span admit
exact feasibility decisions in polynomial Turing time, even without an input
box or a constraint qualification. With bounded integer variables, the same
argument constructs a rational MILP with exactly the same feasible integer
assignments and no additional integer variables. The continuous feasible
sets need not agree. This extends the mechanism previously developed for
convex quadratic inequalities to cones whose natural squared inequalities
have indefinite Hessians.

The contribution being investigated is the span-dependent exact precision
bound and its consequences. Compact rational polyhedral approximations of
Lorentz cones, linear programming, and fixed-integer-dimension MILP
algorithms are established ingredients.

## 1. Model, parameter, and statements

Write \(w=(z,x)\), where \(z\in\mathbb Z^k\) and
\(x\in\mathbb R^n\). Consider rational data and the set

\[
 F=\{(z,x):z\in B_z\cap\mathbb Z^k,\ x\in B_x,\ Lw\le a,\ Ew=e,
       \ \|A_iw+b_i\|_2\le c_i^Tw+d_i\quad(1\le i\le m)\}. \tag{1}
\]

The integer box \(B_z\) has explicit finite rational bounds. An explicit
finite rational continuous box \(B_x\) may also be supplied. All matrices
and vectors are explicitly encoded; let \(N\ge2\) be their total binary
input length, including any supplied boxes. There is no integrality condition
when \(k=0\). When no continuous box is supplied, set
\(B_x=\mathbb R^n\) in (1).

Define

\[
 t_i(w)=c_i^Tw+d_i,\qquad
 q_i(w)=\|A_iw+b_i\|_2^2-t_i(w)^2,
\]
\[
 H_i=\nabla^2_{xx}q_i
      =2(A_{ix}^TA_{ix}-c_{ix}c_{ix}^T),\qquad
 h=\dim_{\mathbb Q}\operatorname{span}\{H_1,\ldots,H_m\}. \tag{2}
\]

Here \(A_{ix}\) and \(c_{ix}\) are the columns and entries corresponding
to the continuous variables. When \(k=0\), these are the full Hessians.
They need not be positive semidefinite. The equivalent quadratic description
of (1) uses **both** \(q_i\le0\) and \(t_i\ge0\).

The parameter concerns the given affine cone maps after squaring. It is not
the number or dimension of conic blocks introduced by a solver, the maximum
individual Hessian rank, or the dimension of a common Hessian kernel.
In particular \(h\le m\), but arbitrarily many distinct cone rows can
have fixed \(h\). Rational invertible changes of the continuous coordinates
preserve \(h\), by congruence of every \(H_i\). Arbitrary reformulations
and auxiliary variables can change it; no representation-invariant minimum
over formulations is claimed. One may first eliminate continuous coordinates
using rational affine equalities, retaining the original integer coordinates
and all induced affine compatibility rows; this can lower the span dimension.
No elimination of integer coordinates by an arbitrary rational transformation
is authorized by this observation.

**Theorem 1 (supplied continuous box).** If \(B_x\) is supplied, a rational
polyhedron \(P\) can be constructed in \(N^{O(h+1)}\) time and encoding
length, using original variables \((z,x)\) and continuous auxiliary variables
\(y\), such that

\[
 \{z\in\mathbb Z^k:\exists x,y\ (z,x,y)\in P\}
 =\{z\in\mathbb Z^k:\exists x\ (z,x)\in F\}.       \tag{3}
\]

The only integer variables in the resulting MILP are the original \(z\).
Moreover every original feasible \((z,x)\) in the supplied boxes lifts to
\(P\). A projected point of \(P\) can violate the original conic rows;
(3) states that its integer assignment has some exact original continuous
witness, which can be different from its displayed \(x\).

**Theorem 2 (no supplied continuous box).** Conclusion (3) still holds
without \(B_x\), with construction time and total encoding length
\(N^{O(h+1)}\). The construction first chooses a uniform continuous box
meeting every nonempty integer fiber, then applies the coefficient-sensitive
version of Theorem 1. It therefore preserves the original integer projection,
but need not contain every point of an unbounded original continuous feasible
set.

Both theorems use effective absolute constants from the linked algebraic
certificate bounds. Extracting practically usable constants is separate work.
They are polynomial bounds for each fixed \(h\), not fixed-parameter bounds
of the form \(f(h)N^C\) with an absolute exponent \(C\).

**Consequences.** For \(k=0\), exact rational SOCP feasibility is in P for
fixed \(h\), with arbitrary cone dimensions and affine rows and no supplied
box or Slater assumption. This includes a fixed number of native cones.
For arbitrary \(k\), the bounded-integer models reduce to MILP and hence are
in NP for fixed \(h\). For fixed \(k,h\), exact feasibility is in P by
the classical mixed-integer linear algorithm. The reduction can return an
integer assignment with a nonempty exact continuous fiber. It does not by
itself recover an exactly feasible continuous point.

## 2. Algebraic precision input

The proof uses two results from
[nonconvex-hessian-span-frontier.md](nonconvex-hessian-span-frontier.md):

1. A nonempty rational quadratic system with constraint Hessian span \(h\)
   and arbitrary affine rows has a feasible algebraic point with coordinates
   bounded in magnitude by \(2^{M^{O(h+1)}}\), where \(M\) is its input
   length. No input box or constraint qualification is required.
2. Over a supplied rational box, the minimum of an arbitrary rational
   quadratic objective on a nonempty rational quadratic system of Hessian
   span \(h\) has an integer annihilator of degree and coefficient bit
   lengths \(M^{O(h+1)}\). The objective Hessian is excluded from \(h\).

The second statement implies a separation from zero of the same form.
Indeed, if a positive value \(\alpha\) satisfies a nonzero integer polynomial
with coefficient magnitudes at most \(2^B\), remove any initial power of
the variable. The remaining constant coefficient has magnitude at least one.
For \(0<\alpha<1\), comparison with the other coefficients gives
\(1\le 2^B\alpha/(1-\alpha)\), so

\[
 \alpha\ge (2^B+1)^{-1}\ge2^{-B-1}.                 \tag{4}
\]

The [coefficient-size refinement](nonconvex-finite-infimum.md#8-separate-structural-size-from-coefficient-bit-length),
checked independently in its [review](nonconvex-finite-infimum-review.md#6-the-coefficient-sensitive-refinement-is-valid),
separates structural size \(S\ge2\) from maximum rational coefficient
bit length \(\tau\ge1\). Here \(S\) counts scalar coefficient positions,
rows, variables, and index lengths in a dense encoding; passage to dense
encoding costs only a polynomial factor. For the witness-coordinate and
bounded-value annihilators, it gives

\[
 D\le S^{C(h+1)},\qquad H\le(\tau+1)S^{C(h+1)}.    \tag{4a}
\]

The proof uses determinant and elimination norm bounds linear in the input
coefficient bits. In particular the dependence on \(\tau\) has an absolute
exponent independent of \(h\). This distinction permits repeated use after
appending a large radius.

This uses no convexity of the quadratic polynomials. Convexity of the original
conic set enters later through the availability of a polyhedral cone outer
approximation. A small algebraic certificate for an arbitrary nonconvex
quadratic system does not imply an efficient algorithm for finding it.

## 3. A uniform gap for every boxed integer fiber

First suppose both boxes are supplied and nonempty. Empty boxes can be
recognized directly. Regard the following as a finite list of scalar rows:
the \(q_i\), the original affine inequality residuals, both signs of each
affine equality residual, and the sign residuals \(-t_i\). For a fixed
integer \(z\in B_z\), put

\[
 \alpha_z=\min_{x\in B_x}
   \max\{0,\ q_1(z,x),\ldots,q_m(z,x),
          L(z,x)-a,\ E(z,x)-e,\ e-E(z,x),\ -t_i(z,x)\}. \tag{5}
\]

The maximum ranges over individual entries and all \(i\). It is continuous
on a compact nonempty box, so its minimum exists. Also \(\alpha_z=0\)
exactly when the original continuous fiber in the box is feasible.

Every boxed integer assignment has coordinate bit lengths polynomial in
\(N\). Expansion and substitution into the rational squared cone maps
therefore give coefficients of polynomial length, uniformly over all such
assignments. This observation bounds lengths without enumerating assignments.
The continuous Hessians remain exactly the \(H_i\) in (2).

The epigraph formulation of (5), with variable \(v\), minimizes \(v\)
subject to \(v\ge0\) and every displayed row being at most \(v\).
A direct absolute-coefficient bound over \(B_x\) supplies a rational
upper bound \(U\) of polynomial bit length for \(v\). Taking \(U\)
at least the largest absolute row bound ensures that this compact epigraph
system is nonempty. Its quadratic Hessians are the \(H_i\), each with
one zero row and column appended. Its Hessian span is at most \(h\).
Applying the bounded-value theorem and (4) gives one effective uniform number

\[
 \Delta=2^{-B}>0,\qquad B=(\tau+1)S^{C(h+1)}
                        \le N^{C'(h+1)},
 \qquad \alpha_z=0\ \text{or}\ \alpha_z\ge\Delta,  \tag{6}
\]

for sufficiently large absolute \(C,C'\). Here \(S,\tau\) are the
structural and coefficient bounds of the original model from (4a), rounded
up to integers. All polynomial expansion and substitution overhead is
absorbed in these constants. No convexity of the
epigraph system is asserted: each squared cone row can be indefinite.

## 4. Rational polyhedral cone approximation

For \(d\ge2\) and rational \(0<\epsilon\le1\), there is an explicitly
constructible homogeneous rational linear lift whose projection
\(C_{d,\epsilon}\) satisfies

\[
 \{(u,t):\|u\|_2\le t\}
 \subseteq C_{d,\epsilon}
 \subseteq\{(u,t):t\ge0,\ \|u\|_2\le(1+\epsilon)t\}. \tag{7}
\]

Its size and coefficient bit lengths are polynomial in
\(d+\log(1/\epsilon)\). The cases \(d=0,1\) are exactly polyhedral.
The [source and construction audit](socp-rational-lift-source.md) gives an
exact integer implementation of Kocuk's Pythagorean-triple construction and
its binary tree lift. It checks inclusion at the apex and avoids irrational
coefficient generation. This is established approximation machinery, not a
new lemma being claimed as original.

Let \(T\ge1\) be a rational upper bound for every \(|t_i(w)|\) on the
input boxes, obtained directly from absolute coefficients. Its bit length is
polynomial in \(N\). Choose

\[
 \epsilon=\frac{\Delta}{6T^2}.                    \tag{8}
\]

Substitute \(u=A_iw+b_i\), \(t=t_i(w)\) into an independent lift (7)
for each conic row. The resulting joint system is rational and linear in
the original and auxiliary variables. Retain the input boxes, original
affine constraints, and \(t_i(w)\ge0\) exactly. Although the last sign
rows already follow from the lift, keeping them makes the quadratic
equivalence explicit.

For any point in this lifted polyhedron,

\[
 q_i(w)\le [(1+\epsilon)^2-1]t_i(w)^2
          \le3\epsilon T^2=\Delta/2.              \tag{9}
\]

Here \(0<\epsilon\le1\). No approximation to a negative quadratic term
was used: (9) follows from approximating the actual norm cone. Replacing
each square independently in the indefinite \(q_i\) would not supply the
required outer approximation.

Every original feasible point has a lift by the first inclusion in (7).
Conversely, if a lifted point has integral \(z\), its exact affine rows and
(9) imply \(\alpha_z\le\Delta/2<\Delta\). The alternative (6) forces
\(\alpha_z=0\). Compactness in (5) then supplies an exact original
continuous witness for that same integer assignment. This proves (3).

The bit length of (8) is \(N^{O(h+1)}\); the total number of cone
coordinates in the explicit input is at most \(N\). The size of the lifts,
rational substitution, and exact construction time are therefore
\(N^{O(h+1)}\). This proves Theorem 1.

More precisely, (4a) and the same argument bound the tolerance bit length
by \((\tau+1)S^{O(h+1)}\). The right-side bound \(T\) has
\((\tau+1)S^{O(1)}\) bits on a supplied box. The rational lift has size
polynomial in its cone dimensions and tolerance bit length, with an absolute
polynomial exponent. Hence construction, and exact LP solution when \(k=0\),
have cost \((\tau+1)^{O(1)}S^{O(h+1)}\). Solving an MILP with unrestricted
integer dimension is not included in this polynomial bound. The exponent on
coefficient size here is independent of \(h\); the exponent on structural
size need not be.

## 5. Removing the continuous box

Fix any \(z\in B_z\cap\mathbb Z^k\). Squaring each cone row and retaining
its sign gives a rational quadratic system in \(x\) whose total description
length is polynomial in \(N\), uniformly over all assignments. Its constraint
Hessians span at most \(h\). By the small-point theorem, if this fiber is
nonempty, it contains a point satisfying

\[
 \|x\|_\infty\le R:=2^{(\tau+1)S^{C_0(h+1)}}
                         \le2^{N^{C'_0(h+1)}}.   \tag{10}
\]

Here \(S,\tau\) describe the original unboxed model, and
\(C_0,C'_0\) are effective absolute constants, uniformly over the boxed assignments.
Thus replacing the continuous domain by \([-R,R]^n\) preserves the entire
feasible integer projection. No enumeration or decision of the fibers is
needed to choose this box.

Using only total input length would give the valid but weaker composition
\(N^{O((h+1)^2)}\). To obtain the stated bound, use (4a) with the actual
choice (10). Integer substitution changes structural size \(S\) and
coefficient bit bound \(\tau\) by at most a fixed polynomial factor.
The radius satisfies

\[
 \log_2R\le(\tau+1)S^{O(h+1)}.
\]

Adding its \(2n\) affine bounds keeps structural size polynomial in \(S\)
and changes the maximum coefficient bit length to
\(\tau'\le(\tau+1)S^{O(h+1)}\). A second application of (4a) gives
gap bit length

\[
 (\tau'+1)S^{O(h+1)}=(\tau+1)S^{O(h+1)}.
\]

The right-side bound \(T\) obeys the same estimate. The preceding
coefficient-sensitive lift construction, and exact LP solution when \(k=0\),
therefore remain
\((\tau+1)^{O(1)}S^{O(h+1)}\), which is \(N^{O(h+1)}\). This proves
Theorem 2 without composing the exponent in \(h\) with itself. The
polyhedral lift is produced only at the last step; its precision-dependent
auxiliary dimension is never used as input to another algebraic theorem.

The box in (10) is a witness bound. It does not bound every feasible point.
For example, the system \(x\ge0\) is unbounded but has a witness in every
box containing zero. The unboxed conclusion is exact integer projection and,
when \(k=0\), exact feasibility equivalence; it is not a polyhedral outer
approximation containing the entire unbounded conic feasible set.

A bound on the affine cone right sides is essential for this approximation
argument. The rational cone system
\(\|(2,y)\|_2\le y\), \(y\ge0\), is infeasible. Yet for every
\(\epsilon>0\), its multiplicative relaxation
\(\|(2,y)\|_2\le(1+\epsilon)y\) is feasible for sufficiently large
\(y\). Its squared residual is the constant four. Thus a positive squared
gap alone does not justify an unrestricted relative cone approximation;
the witness box and the bound \(T\) in (9) supply the missing control.

For \(k=0\), solve the constructed rational LP exactly. For arbitrary \(k\),
the result is an MILP with exactly \(k\) integer variables. If \(k\) is
fixed, [Lenstra (1983), Section 5](https://pub.math.leidenuniv.nl/~lenstrahw/PUBLICATIONS/1983i/art.pdf)
allows any number of continuous variables and solves this rational MILP in
time polynomial in its encoding length. The consequences after Theorem 2
follow. Bounded integer coordinates are essential to the uniform substitution
argument; no unbounded-integer theorem is asserted here.

## 6. Interpretation, examples, and limits

The squared constraint Hessian is allowed to be indefinite even for one
ordinary Lorentz cone: \(\|x\|_2\le t\) has squared Hessian
\(2\operatorname{diag}(I,-1)\). Its row defines a convex cone only together
with \(t\ge0\). This example lies outside an argument requiring each native
quadratic inequality to be convex, while its squared-Hessian span equals one.

Many cones need not mean many Hessian directions. Constraints
\(\|x-a_i\|_2\le t+d_i\), with rational centers and offsets, all have
the same squared Hessian \(2\operatorname{diag}(I,-1)\). The number of
rows and their affine parts can grow independently of \(h=1\), and arbitrary
additional affine rows are permitted. This is a structural family included by
the parameter; no empirical solver advantage for this family is claimed.

A broader sufficient condition uses two directly computable spans. If
\[
 s=\dim\operatorname{span}\{A_{ix}^TA_{ix}\},\qquad
 r=\dim\operatorname{span}\{c_{ix}\},
\]
then
\[
                         h\le s+\frac{r(r+1)}2.             \tag{10a}
\]
Indeed the rank-one matrices \(c_{ix}c_{ix}^T\) lie in the symmetric
matrix space generated by a basis of the \(r\)-dimensional vector span,
whose dimension is at most \(r(r+1)/2\). The Gram matrices lie in a space
of dimension \(s\), so their differences lie in the sum of these two
spaces. For example, rational maps
\(A_i=\operatorname{diag}(a_i I_p,b_i I_q)\) and right-side vectors
\(c_i=\gamma_i c\) have \(h\le3\), while the cone count and both
block sizes can grow. Arbitrary affine shifts remain allowed. This is an
elementary modeling corollary, not an additional complexity theorem or a
claim about how often the structure occurs in applications.

The output is deliberately weaker than an exact linear description of the
continuous feasible set. A ball with a curved boundary has no finite exact
polyhedral lift, since every projection of a polyhedron is a polyhedron.
Also, a rational LP witness generally need not be an exact SOCP witness.
The exact conclusion comes from an existential zero-versus-positive gap, not
from rounding or repairing the LP solution. The separate
[exact witness theorem](socp-exact-witness-recovery.md) supplies the additional
arguments needed to recover a feasible algebraic continuous point in
\(N^{O(h+1)}\) time, after an integer assignment is fixed if present.

Irrational-only feasibility occurs already at \(h=1\), using two rational
cones:

\[
 \|(1,1)\|_2\le x,\qquad \|(x,x)\|_2\le2.          \tag{11}
\]

The unique feasible point is \(x=\sqrt2\). The squared residuals are
\(2-x^2\) and \(2x^2-4\), with Hessians \(-2\) and \(4\), whose span
has dimension one. The first sign row selects the positive root. Thus even
this small-span conic class does not always admit a rational exact witness.
This is a qualitative contrast with the one-native-cone rational-witness
argument in the prior audit, not a sharpness claim for the general bounds.
Minimizing \(x\) in (11) has value \(\sqrt2\), whereas a rational LP
with a finite optimum has a rational optimal value. Thus a rational LP
feasibility reduction cannot in general also preserve the continuous
objective value in one formulation.

An affine objective with a rational threshold can be included as another
affine row, without increasing \(h\). Thus exact rational-threshold feasibility
also follows. Moreover one fixed MILP preserves every objective depending only
on \(z\), because its feasible integer assignments agree exactly; for a
linear integer-only objective, it is therefore an exact MILP optimization
formulation. A continuous objective requires additional work, including an
attainment decision: a closed unbounded SOC set can have a finite
unattained linear infimum, as with minimizing \(x\) over
\(x,y\ge0\), \(xy\ge1\).

The subsequent [continuous optimization theorem](continuous-socp-optimization.md)
handles that distinction explicitly. For an affine objective, it classifies
infeasibility, unboundedness, finite nonattainment, and finite attainment in
\(N^{O(h+1)}\) time. It returns the exact algebraic finite value and,
when attained, a canonical algebraic optimizer. This uses additional
finite-infimum and optimizer-size theorems beyond the feasibility reduction.

## 7. Prior results and novelty boundary

- [Ben-Tal and Nemirovski (2001)](https://www2.isye.gatech.edu/~nemirovs/ApprLor_fin.pdf)
  developed compact lifted polyhedral approximations of Lorentz cones.
  [Kocuk (2021)](https://optimization-online.org/wp-content/uploads/2019/12/7501.pdf)
  supplies rational versions with controlled encoding lengths. These are
  ingredients, including their logarithmic dependence on inverse tolerance.
  Kocuk's Proposition 7 already preserves all integer points for intersections
  of integral balls, with an extension noted for integral ellipsoids. The
  proposed addition here is uniform preservation of integer assignments with
  arbitrarily many existential continuous coordinates, using a span-dependent
  algebraic gap; integer preservation itself is not new.
- The [separate prior audit](socp-hessian-span-prior.md#the-whole-hessian-span-one-case-follows-from-older-bounds)
  derives the entire \(h\le1\) decision and boxed-integer projection
  case from older bounds. If all nonzero squared Hessians have the same
  proportionality sign, an affine epigraph reduces the precision question to
  one quadratic over a polyhedron. If both signs occur, SOC inertia forces
  common Hessian rank at most two; low-dimensional radius and value bounds
  apply after polyhedral elimination. Thus neither the one-cone case nor the
  span-one case is positioned as the main advance. These are checked
  corollaries of earlier tools, not claims that those exact statements were
  found published verbatim.
- [Blanco, Magron and Martínez-Antón (2025)](https://arxiv.org/abs/2501.09828),
  *On the Complexity of p-Order Cone Programs*, gives exact feasibility,
  radius, and discrepancy bounds. Their Theorem 4.3 still has an exponent
  depending on the smaller of the variable and affine-row counts for a single
  cone. Theorem 5.2 extends the bound to several cones. The proposed result
  replaces that growing exponent on the present structural class by dependence
  on the squared-Hessian span. **This does not make one-cone tractability new:**
  a separate audit derived exact one-cone feasibility from classical polynomial
  convex quadratic programming by projective normalization. Its proof and
  primary-source comparison are recorded in
  [socp-hessian-span-prior.md](socp-hessian-span-prior.md). The scope still
  requiring a careful priority audit is fixed squared-Hessian span, including
  arbitrarily many cones and existential continuous fibers. An unsuccessful
  search does not establish priority.
- The general feasible-witness and radius bound also follows from
  [Grigoriev–Pasechnik sampling](https://arxiv.org/abs/cs/0403008) after
  restricting a Hessian-basis lift to a minimum-dimensional polyhedral face
  that meets its quadratic variety. The
  [independent source audit](socp-hessian-span-prior.md#fixed-cone-count-few-quadratics-and-degeneracy)
  proves this reduction. The potential advance therefore rests on the
  general larger-span value and positive-gap precision, and the conic
  consequences developed from it; the feasible-witness mechanism alone
  should not be claimed as new.
- [Hu (2026)](https://arxiv.org/abs/2609.06757) gives a polynomial-size exact
  SOCP dual and an alternative system, including weakly infeasible cases.
  The author explicitly separates formulation size over exact real data from
  rational certificate size and polynomial Turing complexity. Thus an exact
  conic alternative already exists; its stated formulation-size conclusion
  does not provide the precision bound or rational LP reduction claimed here.
- [Lenstra (1983)](https://doi.org/10.1287/moor.8.4.538) supplies the mixed
  integer linear algorithm after the reduction. No lattice algorithm is new.
- The repository's [convex quadratic projection theorem](mixed-integer-span-frontier.md)
  uses native positive-semidefinite quadratic rows and compact square
  approximations. Its proof does not apply directly to the indefinite squared
  SOC rows in (2). The current extension uses the separate nonconvex value and
  small-point theorems and approximates the actual SOC maps.

The main substantive claim is conditional only on those explicitly linked
algebraic theorems being correct. The resulting precision-to-LP step is short,
but it permits exact decisions for degenerate and unbounded rational conic
systems in the stated fixed-span class. Its practical value would require
usable separation bounds, an adaptive certified construction, and evidence
that small squared-Hessian span occurs in useful formulations. None of those
practical consequences has been established by this proof.

## 8. Verification record

The construction in [socp-rational-lift-source.md](socp-rational-lift-source.md)
is checked against the open Kocuk manuscript and proved using rational
Pythagorean rotations. The author of this note independently checked the
folding-angle inequalities, norm monotonicity with slack, coefficient bound,
tree accumulation, and apex behavior. That note records 789 exact finite
checks and four symbolic identities. The
[separate adversarial review](socp-hessian-span-review.md) checks the full
proof, the source construction, and additional independent exact arithmetic
cases. It identified two wording issues: the supplied continuous box must be
part of the stated feasible set, and optional affine elimination must preserve
the integer variables. Both were corrected and independently rechecked.
The irrational singleton (11) was also checked independently. These checks
include a separate verification of the Gram-span bound (10a) and its
two-block example. They do not constitute formal verification or prove
priority. Targeted commands
for this note were `git diff --check -- research-20260927/socp-hessian-span-frontier.md`
and an inline Python check of whitespace, control characters, final newline,
paired LaTeX delimiters, and local-link existence; both passed. The subsequent
[coefficient-sensitive review](socp-coefficient-sensitive-review.md) checked
the actual choices of \(\Delta\) and \(R\), the repeated height estimate,
and the construction and LP costs. It explicitly distinguishes polynomial
MILP construction from solving an MILP with unrestricted integer dimension.
No project-wide verification or CI inspection was performed.
