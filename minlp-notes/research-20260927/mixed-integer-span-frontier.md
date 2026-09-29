# Exact integer projections from bounded continuous Hessian span

Date: 2026-09-27. Status: proved reduction using the value theorem in
[hessian-span-reduction.md](hessian-span-reduction.md), with an independent
adversarial review and a separate root review completed. It does not establish
priority. Statements marked conditional identify that theorem dependency.

The most useful consequence is stronger than fixed-integer-dimension
tractability: a bounded, jointly convex quadratic system whose continuous
Hessian blocks have fixed span dimension admits a polynomial-size rational
MILP with exactly the same feasible integer assignments and no new integer
variables. The continuous feasible sets need not agree. Compact polyhedral
approximations and exact integer preservation for certain purely integer
quadratic sets are established tools. The proposed addition is a uniform
precision bound for fibers with arbitrarily many existential continuous
variables and bounded continuous Hessian span.

This supplies a route to exact mixed-integer feasibility that does not require
exact separation over a projection, a Slater point in the original system, or
an exactly feasible continuous point from a numerical optimizer.

## Setting and conditional theorem

Write the variables as \(w=(z,x)\), with \(z\in\mathbb Z^k\) and
\(x\in\mathbb R^n\). Let

\[
 F=\{(z,x)\in B_z\times B_x:\ z\in\mathbb Z^k,
        Aw\le b,
        Ew=e,
        q_i(w)\le0\ (i=1,\ldots,m)\},
\]

where the boxes have explicit finite rational coordinate bounds and all data
have total explicit binary length \(N\ge2\). Assume each \(q_i\) is a
quadratic polynomial with rational coefficients and positive-semidefinite
**full** Hessian in \((z,x)\). Define

\[
 h=\dim_{\mathbb Q}\operatorname{span}
         \{\nabla^2_{xx}q_i:i=1,\ldots,m\}.
\]

Thus only the continuous Hessian blocks enter \(h\), although full joint
convexity is required for the polyhedral construction. There is no restriction
on the number, rank, or full-matrix span of the quadratic Hessians beyond
these assumptions. Empty boxes can be recognized first. Fixed coordinates
can be substituted out; this cannot increase \(h\).

**Conditional integer-projection theorem.** Assume the coefficient-height
and zero-separation theorem in the linked note. One can construct, in
\(N^{O(h+1)}\) time, a rational polyhedron
\(P\subseteq\mathbb R^k\times\mathbb R^n\times\mathbb R^s\), whose total
encoding length is \(N^{O(h+1)}\), such that

\[
 \{z\in\mathbb Z^k:\exists x,y\ (z,x,y)\in P\}
   =\{z\in\mathbb Z^k:\exists x\ (z,x)\in F\}.       \tag{1}
\]

The only integer variables in this MILP are the original \(z\). The result
holds for arbitrary \(k\); solving the MILP need not be polynomial when
\(k\) grows. For fixed \(k,h\), classical fixed-integer-dimension MILP
algorithms decide exact feasibility in polynomial Turing time and, when
feasible, produce an integer assignment having a nonempty exact original
continuous fiber.

The displayed asymptotic construction uses an effective sufficiently large
absolute constant in the linked separation theorem. A practical formulation
requires extracting a usable explicit bound; the result does not assert that
the worst-case lift is numerically attractive.

## Uniform gap over every integer assignment

Put every affine inequality, both signs of every affine equality, and every
quadratic inequality into the maximum violation function

\[
 v(z,x)=\max\{0,\ q_1(z,x),\ldots,q_m(z,x),
                    Aw-b,\ Ew-e,\ e-Ew\}.
\]

The vector entries inside the maximum are interpreted as individual scalar
functions. For each \(z\in B_z\cap\mathbb Z^k\), define

\[
 \alpha_z=\min_{x\in B_x}v(z,x).
\]

This minimum exists. It is zero exactly when the original fiber at \(z\)
is feasible. Every coordinate of every such \(z\) has polynomial binary
length in \(N\), because the input bounds are explicit. Substituting \(z\)
therefore gives rational continuous-slice coefficients of polynomial length,
uniformly over all assignments. This is a bound on substitution length, not
an enumeration of the assignments.

The epigraph problem for \(\alpha_z\) has a linear objective. Its native
continuous Hessians are the original \(xx\) blocks with one zero row and
column appended for the epigraph variable. Its affine rows add no Hessians.
A direct rational bound on the magnitudes of all rows over the input box
gives a polynomial-length upper bound for the epigraph variable. Thus the
linked value theorem gives a uniform effective number

\[
 \Delta=2^{-N^{C(h+1)}}>0
 \quad\text{such that}\quad
 \alpha_z=0\ \text{or}\ \alpha_z\ge\Delta             \tag{2}
\]

for one sufficiently large absolute \(C\), after absorbing polynomial
substitution overhead. Neither the feasible fibers nor the infeasible fibers
need satisfy a constraint qualification.

Choose a rational \(0<\varepsilon<\Delta\), for instance
\(\varepsilon=\Delta/2\). It now suffices to construct a rational lifted
outer approximation whose projected points satisfy every native quadratic
row to additive error at most \(\varepsilon\), while retaining all affine
rows exactly.

## A compact rational square approximation

This is an established approximation ingredient, included with a proof so
that the arithmetic and the absence of extra integer variables are explicit.
Beach, Burlacu, Bärmann, Hager, and Hildebrand's
[2024 paper](https://link.springer.com/article/10.1007/s10589-023-00543-7),
Definition 6 and Proposition 2, provides a stronger sawtooth epigraph
relaxation using continuous auxiliary variables only. Its construction builds
on the earlier square interpolants and compact formulations cited there.
The following slightly weaker version is enough here.

For \(s\in[0,1]\), define the tent function

\[
 T(s)=\min\{2s,2(1-s)\},\qquad
 f_r(s)=s-\sum_{j=1}^r4^{-j}T^j(s).
\]

The function \(f_r\) is the linear interpolant of \(s^2\) at the dyadic
grid \(j2^{-r}\). To prove this inductively, start with \(f_0(s)=s\).
At the next refinement, \(T^r\) vanishes at the preceding grid points and
equals one at their interval midpoints. Subtracting \(4^{-r}T^r\) corrects
the previous midpoint interpolation error, which is exactly \(4^{-r}\).
The functions are affine on each refined interval, proving the claim.
On an interval with endpoints \(a,b\), the interpolation error is
\((s-a)(b-s)\). Consequently

\[
 0\le f_r(s)-s^2\le\eta_r:=4^{-(r+1)}.               \tag{3}
\]

Consider the entirely continuous linear system

\[
 g_0=s,\qquad 0\le g_j,\quad
 g_j\le2g_{j-1},\quad g_j\le2(1-g_{j-1})
                   \quad(j=1,\ldots,r),
\]
\[
 t\ge s-\sum_{j=1}^r4^{-j}g_j-\eta_r.                \tag{4}
\]

Its projection onto \((s,t)\), with \(s\in[0,1]\), is exactly
\(t\ge f_r(s)-\eta_r\). Here is the point requiring proof: relaxing the
tent equalities to upper bounds does not let the weighted sum exceed its
value on the iterated tents.

Let \(V_r(s)\) be the maximum of \(\sum_{j=1}^r4^{-j}g_j\) over the
chain with \(g_0=s\). Inductively,

\[
 V_r(s)=\sum_{j=1}^r4^{-j}T^j(s),\qquad
 \operatorname{Lip}(V_r)\le\sum_{j=1}^r2^{-j}=1-2^{-r}.
\]

For the induction step, the optimal tail after choosing \(g_1=u\) has
value \(\frac14 V_{r-1}(u)\). The objective for this choice is therefore
\(\frac14(u+V_{r-1}(u))\). Since \(V_{r-1}\) has Lipschitz constant
strictly below one, this expression is strictly increasing in \(u\).
Its maximum on \([0,T(s)]\) is at \(u=T(s)\). The stated expression and
Lipschitz bound follow, establishing the projection claim.

By (3), the lower approximation \(f_r-\eta_r\) is everywhere at most
\(s^2\), and differs from it by at most \(\eta_r\). System (4) has
\(O(r)\) continuous variables and rows with coefficient bit lengths
\(O(r)\). Its total binary encoding length is polynomial in \(r\).

## From squares to every convex quadratic row

Exact rational elimination of a rational PSD matrix gives a decomposition

\[
 q_i(w)=\ell_i(w)+\sum_{a=1}^{r_i}d_{ia}(u_{ia}^{T}w)^2,
 \qquad d_{ia}>0,
\]

with rational \(d_{ia},u_{ia}\), affine rational \(\ell_i\), and at most
\(k+n\) square terms. The conventional factor \(1/2\) can be absorbed in
\(d_{ia}\). A pivoted rational \(LDL^T\) elimination suffices. If the
remaining PSD matrix has all diagonal entries zero, then it is zero; a
positive diagonal pivot can otherwise be used. Schur complements remain PSD.
Determinant bounds for rational elimination give polynomial coefficient bit
length and polynomial construction time. No square roots are needed.

Compute exact interval bounds \([L_{ia},U_{ia}]\) for each linear form
over the input box. A form with \(L_{ia}=U_{ia}\) contributes a constant.
For every other form, put

\[
 s_{ia}=\frac{u_{ia}^{T}w-L_{ia}}{U_{ia}-L_{ia}}\in[0,1],
 \qquad \beta_{ia}=d_{ia}(U_{ia}-L_{ia})^2>0.
\]

Expanding the square expresses the row as

\[
 q_i(w)=\widetilde\ell_i(w)+\sum_a\beta_{ia}s_{ia}^2. \tag{5}
\]

All these coefficients have polynomial bit length. Let
\(S\ge1\) be a rational upper bound on every sum \(\sum_a\beta_{ia}\).
Its bit length is polynomial in \(N\). Choose one depth \(r\ge0\) with

\[
 S4^{-(r+1)}\le\varepsilon.
\]

This requires \(r=O(\operatorname{size}(S)+\log(1/\varepsilon)+1)\).
Introduce an independent copy of (4) for each term in (5), and impose

\[
 \widetilde\ell_i(w)+\sum_a\beta_{ia}t_{ia}\le0.       \tag{6}
\]

The projection of these rows onto \(w\) is exactly the inequality
\(\underline q_i(w)\le0\), where

\[
 \underline q_i(w)=\widetilde\ell_i(w)+
                \sum_a\beta_{ia}(f_r(s_{ia})-\eta_r).
\]

Positive weights are essential for this equivalence. Equations (3) and (5)
give the pointwise estimates

\[
 q_i(w)-\varepsilon\le\underline q_i(w)\le q_i(w).    \tag{7}
\]

The number of terms is polynomial in the explicit input size, and every
lift has size polynomial in \(N+\log(1/\varepsilon)\). With the choice
following (2), the total size and construction time are \(N^{O(h+1)}\).

## Proof of exact integer projection

Define \(P\) by the input box, the exact affine rows, and all the lifts
(4)--(6). A point of \(F\) satisfies every \(\underline q_i\le0\), so
it has a lift to \(P\). This proves one inclusion in (1).

Conversely, take \((z,x,y)\in P\) with \(z\) integer. By (7),
\(q_i(z,x)\le\varepsilon\) for every native quadratic row. The affine
rows hold exactly, so

\[
 \alpha_z\le v(z,x)\le\varepsilon<\Delta.
\]

The uniform alternative (2) forces \(\alpha_z=0\). Compactness of the
continuous box then gives some \(x'\) with \((z,x')\in F\). The point
\(x'\) need not equal the continuous part \(x\) of the MILP solution.
This proves (1) and the conditional theorem.

For fixed \(k\), apply the mixed-integer extension in
[Lenstra's original paper](https://doi.org/10.1287/moor.8.4.538), Section 5.
Its running time is polynomial in the MILP encoding length when only the
number of integer variables is fixed; the number of continuous auxiliary
variables is permitted to grow. This supplies the fixed-\(k,h\) Turing
decision consequence without an approximate nonlinear oracle.

## What follows for optimization

An objective that is rational linear in \(z\) alone can be optimized
exactly over the constructed MILP. Equality of the integer projections gives
the same original optimum and optimal integer assignments.

For a jointly convex quadratic objective \(q_0(z,x)\), adding a rational
threshold row \(q_0(z,x)\le\tau\) increases the continuous Hessian span
by at most one. The theorem therefore gives exact rational-threshold decision
in polynomial time for fixed \(k,h\), including equality at the optimum.
It also returns an integer assignment with a nonempty exact original fiber
below the threshold. The continuous output of the MILP is not asserted to
meet that threshold exactly in the original problem.

One can additionally identify an optimal integer assignment in polynomial
time for fixed \(k,h\). For every feasible integer assignment, let
\(\theta_z\) be its continuous-slice optimum. The value theorem gives
uniform integer annihilators of degree at most \(D=N^{O(h+1)}\) and
coefficient bit lengths at most \(H=N^{O(h+1)}\). These imply a uniform
gap \(\sigma=2^{-N^{O(h+1)}}\) between distinct slice optimum values.
Indeed, if \(P,Q\) are two such nonzero annihilators, then

\[
 R(t)=\operatorname{Res}_u(P(u),Q(u-t))
\]

is a nonzero integer polynomial vanishing at their root differences. Its
degree is at most \(D^2\); the Sylvester determinant gives coefficient
bit lengths \(O(DH+D^2+D\log D)\). It remains nonzero even if \(P,Q\)
share factors, since each pair of their roots gives only one difference.
For a nonzero difference, remove powers of \(t\) and apply a Cauchy bound
to the reciprocal polynomial. This proves the asserted separation.

First check feasibility. Bound the absolute objective over the box by a
rational number \(M\) of polynomial bit length and start with the strict
lower endpoint \(a=-M-1\) and feasible upper endpoint \(b=M\).
Rational-threshold bisection then produces
\(a<\theta^*\le b\) with \(b-a<\sigma\). Any integer assignment
returned by the threshold MILP at \(b\) has \(\theta_z\le b\), and
therefore \(\theta_z=\theta^*\); otherwise the gap would be at least
\(\sigma\). The number of bisections and the bits of its thresholds are
polynomial for fixed \(h\). A conservative complexity bound obtained by
substitution is polynomial for fixed \(k,h\); a sharp joint parameter
exponent is not asserted here.

This argument does **not** yet construct an exact algebraic continuous
optimizer or the explicit minimal polynomial of \(\theta^*\). Those
output problems require additional recovery arguments. Rational-threshold
decision, rational approximations to any prescribed accuracy, and exact
identification of an optimal integer assignment are the established outputs
of this conditional reduction.

## Literature comparison and limits

- **Lenstra (1983).** The fixed-number-of-integer-variables MILP algorithm is
  an ingredient. Section 5 was checked directly in the
  [open author copy](https://pub.math.leidenuniv.nl/~lenstrahw/PUBLICATIONS/1983i/art.pdf).
  No new lattice algorithm is claimed.
- **Khachiyan--Porkolab (2000), Theorem 1.2.** Their exact algorithm handles
  convex sets defined by first-order real formulas. The complexity exponent
  depends on the dimensions of the quantified blocks. Applying it directly
  to a projection \(\exists x\ F(z,x)\) does not yield polynomial time
  when \(n\) grows. The repository's
  [local full text](../literature/papers/khachiyan2000-integer-optimization-on-convex-semialgebraic/fulltext.md)
  was examined, especially pages 207--210.
- **Heinz (2005); Hildebrand--Köppe (2013).** These are stronger algorithmic
  precedents for pure integer quasiconvex polynomial optimization. The
  [Hildebrand--Köppe paper](https://arxiv.org/abs/1006.4661) fixes the
  dimension of the integer polynomial problem. It does not by itself
  remove an arbitrarily large existential continuous block.
- **Del Pia (2025).**
  [Convex Quadratic Sets and the Complexity of Mixed Integer Convex
  Quadratic Programming](https://doi.org/10.1137/24M1636782), Proposition 4
  and Theorem 3, gives an FPT algorithm parameterized by integer dimension
  for feasibility with one convex quadratic inequality and for convex
  quadratic optimization over a polyhedron. This is stronger than our
  fixed-parameter polynomial claim in that special case and does not need
  our explicit input box. The proposed additional class has arbitrarily
  many convex quadratic inequalities with bounded continuous Hessian span.
- **Compact polyhedral approximation.**
  [Ben-Tal--Nemirovski](https://www2.isye.gatech.edu/~nemirovs/ApprLor_fin.pdf)
  gives compact polyhedral approximations for second-order cones. Beach
  et al. (2024), cited above, gives the more directly usable rational
  sawtooth square epigraph construction. Approximation lifts and their
  logarithmic dependence on accuracy are not new contributions here.
- **Kocuk (2021), Proposition 7.**
  [Rational Polyhedral Outer-Approximations of the Second-Order Cone](https://optimization-online.org/wp-content/uploads/2019/12/7501.pdf),
  pp. 20--21, already constructs rational outer approximations preserving
  exactly the integer points of intersections of balls with integral data;
  the text also discusses integral ellipsoids. Its compact lifts add
  continuous auxiliary variables. It chooses accuracy below the arithmetic
  gap in integer squared distances. Thus using accurate rational lifts to
  preserve integer assignments is an established mechanism. The proposed
  extension here is the uniform gap after minimizing over continuous
  fibers, supplied by bounded Hessian span. The root and independent
  reviewers inspected the proposition directly.
- **Bredereck et al. (2017 version).**
  [Mixed Integer Programming with Convex/Concave Constraints](https://arxiv.org/abs/1709.02850)
  reduces models with explicitly piecewise-linear convex/concave functions
  to MILP. Its abstract and Section 1.1.1 were inspected. The nonlinear
  functions treated there are piecewise linear in their input descriptions;
  it is not a quadratic fiber-separation theorem. It reinforces that
  conversion of known polyhedral epigraphs into MILP is established work.
- **Basu (2022 version), Theorems 5.7--5.8.**
  [Complexity of optimizing over the integers](https://arxiv.org/abs/2110.06172)
  states weak mixed-integer convex algorithms whose dependence on continuous
  dimension is polynomial when integer dimension is fixed. Applied to
  maximum violation over a box, this is an alternate route. The theorem
  needs an ambient interior ball in the optimal integer fiber. Padding
  each rounded integer interval by one half and rescaling nonfixed
  continuous box coordinates provides such a ball. The source refers
  finite-precision rounding details to Grötschel--Lovász--Schrijver and
  warns that sharper projection-based bounds need more delicate analysis.
  The explicit MILP reduction above avoids relying on that route.

Joint convexity cannot be replaced in this proof by convexity only after
fixing \(z\). For example, \(q(z,x)=x^2-z^2\) has continuous Hessian
\(2\), but is not jointly convex: \((-1,1)\) and \((1,1)\) satisfy
\(q\le0\), whereas their midpoint \((0,1)\) does not. The PSD square
decomposition of the full quadratic is unavailable in general.

A decision oracle for a continuous fiber is not a separation oracle for its
projection. Conversely, approximation alone cannot exclude a false integer
fiber: its violation may be positive but smaller than the chosen tolerance.
The explicit uniform alternative (2) for existential continuous fibers is
the bridge that the present reduction adds. Without a bound on \(h\),
the linked theorem does not give a
polynomial-size lift through this argument.

Equality (1) concerns the discrete projection, not a MILP representation of
the whole curved feasible set or its mixed-integer convex hull. It does not
imply a strong LP bound, good numerical conditioning, or an observed solver
speedup. The size bound is polynomial for fixed \(h\), not an FPT bound in
\(h\).

Searches on 2026-09-27 covered fixed-integer-dimension convex quadratic
feasibility, few quadratic constraints, Hessian span, compact square
epigraphs, and equivalent convex semialgebraic formulations. They located
the precedents above but not an equivalent stated exact-integer-projection
theorem with bounded continuous Hessian span. This limited search does not
establish novelty. The proposed significance depends first on correctness
of the value theorem and then on a broader comparison with exact conic and
mixed-integer formulation literature.

## Verification record

The linked value theorem is an explicit dependency, not reproved here.
The square interpolation identity, the continuous-chain projection argument,
rational PSD decomposition, the integer-fiber transfer, and the pairwise
algebraic-value separation are mathematical proof arguments. The root
independently obtained the same discounted-tent proof and reviewed the full
note. A separate adversarial reviewer identified the direct Beach et al.
precedent and reviewed the reduction and resultant argument without finding
a substantive gap. Both reviewers requested the explicit strict initial
bisection endpoint, now supplied above. These checks are evidence rather
than a correctness guarantee.

Targeted source commands actually run include `pdftotext -layout` on the
downloaded Basu and Beach PDFs and `rg`/`sed` over those texts and the local
Khachiyan--Porkolab and Del Pia papers. Source files are in
[sources-mixed-integer-span](sources-mixed-integer-span/).

An exact SymPy vertex-enumeration check, saved as
[check_mixed_integer_span_vertices.py](check_mixed_integer_span_vertices.py),
maximizes the relaxed chain objective over every vertex basis at depths one
through four for 22 rational inputs per depth. All 88 instances agree with
the iterated-tent value. This checks the relaxed LP, not just the interpolation
identity. It does not establish the arbitrary-depth theorem or any bit
complexity claim. The command run is
`python research-20260927/check_mixed_integer_span_vertices.py`.

No project-wide verification, CI inspection, or Lean proof was performed for
this note.
