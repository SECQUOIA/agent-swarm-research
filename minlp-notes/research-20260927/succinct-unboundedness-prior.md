# Prior audit: succinct polynomial escape certificates

Date: 2026-09-27. Scope: rational convex quadratic constraints and objective,
with every full Hessian positive semidefinite, and mixed-integer variables.
The proposed certificate lifts a decreasing ray from the terminal problem
in [the recession-elimination argument](mixed-integer-attainment-frontier.md).
This audit concerns literature comparisons, not an independent verification
of the proposed certificate theorem.

**Assessment.** The conditional equivalence between continuous and
mixed-integer objective unboundedness is an older qualitative consequence
of Bank–Mandel and has a direct later statement in Obuchowska (2008).
The latter also explicitly claims a polynomial-time LP algorithm for
boundedness, building on a 1995 continuous algorithm. These conclusions
should not be proposed as new. General curve
selection does not immediately supply the proposed
combination of polynomial coordinates, preserved integer samples, a short
arithmetic circuit, and a controlled algebraic coefficient field. I did not
find a primary source establishing that exact combination for the stated
class. This is a bounded search result, not a publication-priority finding.
The possible contribution should be stated through that combination and its
complexity guarantees, rather than through the broad idea of an escape curve.

## 1. Rational recession geometry and elimination are established ingredients

Bank and Mandel, *Nonlinear parametric integer programming* (1987),
pp. 16–48, is directly available in the
[publisher preview](https://api.pageplace.de/preview/DT0400.9783112720936_A50662169/preview-9783112720936_A50662169.pdf).
It also implies the stronger conditional unboundedness equivalence for
rational globally quasiconvex polynomial data, with any mixed-integer split.
Here is the inference from Theorems 3(iii), 4, and 7(i):

* Append the objective threshold row \(f_0\le b_0\). Continuous
  unboundedness makes every threshold feasible and keeps this row
  unbounded below on its own feasible sublevel.
* Hence the objective row is absent from the stable subsystem, which
  retains rows bounded below. Theorem 4 makes this index set independent
  of the feasible right-hand side.
* Any original mixed-integer feasible point satisfies every stable row,
  for every threshold. Rationality gives the stable recession cone the
  mixed-integer generation property by Theorem 3(iii).
* The paragraph after Theorem 7 then gives uniform distribution of the
  mixed-integer stable points; Theorem 7(i) yields a mixed-integer feasible
  point for every threshold.

Thus continuous unboundedness implies mixed-integer unboundedness whenever
the original mixed-integer set is nonempty. The converse is immediate.
No dimension parameter is fixed. This deduction gives no circuit-size
bound. Finite attainment is also older; see
[the existing prior audit](mixed-integer-attainment-prior.md).

Martínez-Legaz, Noll, and Sosa, *Minimization of Quadratic Functions on
Convex Sets without Asymptotes*, J. Convex Anal. 25 (2018), 623–641, provides
a second close methodological comparison in its
[author-hosted text](https://www.math.univ-toulouse.fr/~noll/PAPERS/frank_and_wolfe.pdf).
The proof of Theorem 1 takes a recession direction of an unbounded objective
sublevel, shows that the objective is constant along it, and projects to a
lower-dimensional problem. Theorem 1 concerns finite attainment, and Theorem
3 characterizes the Frank–Wolfe property using quadratic asymptotes. This is
qualitative convex geometry, without a mixed-integer circuit certificate.
The relevant terms are **f-asymptote** and **q-asymptote**; the latter means
quadratic asymptote, rather than a polynomial escape parametrization.

## 2. Exact ray certificates on polyhedra

Slot, Steurer, and Wiedmer, *Hesse's Redemption: Efficient Convex Polynomial
Programming* (2025),
[arXiv:2511.03440, Lemma 5.1](https://arxiv.org/html/2511.03440v1#S5),
prove that a rational convex polynomial is unbounded below on a nonempty
rational polyhedron exactly when a rational linear system has a solution
\(d\):

\[
                 Ad\le0,\qquad Ud=0,\qquad w^Td=1.
\]

Their decomposition gives \(f(a+td)=f(a)-t\). The matrices and vectors in
the system have polynomial encoding length, so linear programming supplies
a short rational ray. Their objective class is much broader than quadratic,
but the constraints are polyhedral. They therefore do not address repeated
lifts through quadratic inequalities. In the proposed class, even
\(\min\{-z:x\ge z^2\}\) has no decreasing feasible straight ray.

The affine decline of the objective along the terminal ray is thus familiar.
The comparison requiring justification is the representation and size of
its lift into the original quadratically constrained space.

## 3. General curve selection gives different representations

Basu and Roy, *Quantitative Curve Selection Lemma*,
[arXiv:1803.00505v3, Theorem 2](https://arxiv.org/pdf/1803.00505v3),
give explicit complexity bounds for a semialgebraic path entering a
semialgebraic set from a point in its closure. Their path is represented
through algebraic equations and a selected real branch. This is a
semialgebraic path description, not a claim that the coordinates themselves
are polynomials in the path parameter. Compactifying an unbounded problem
lets qualitative curve selection reach infinity, but does not automatically
preserve mixed-integer points, give rational coefficients, or produce a
polynomial-size arithmetic circuit in growing ambient dimension. More
precisely, its description degrees are \((2dN(N')^2,N)\), where
\(N=(2d+6)(2d+5)^{k-1}\) and
\(N'=5(k(2d+4)+2)N\). Here \(k\) is the ambient dimension and \(d\)
the maximum defining degree.

Jelonek and Kurdyka, *Reaching generalized critical values of a polynomial*,
[primary PDF](https://arxiv.org/pdf/1203.0539),
give an effective real curve-selection result in Theorem 6.7 of the second
version concatenated in that PDF. A finite
nonproperness value of a polynomial map of degree at most \(d\) can be
approached along a Laurent arc

\[
 x(t)=\sum_{i=-(d-1)D-1}^{D}a_it^i,\qquad
 D=(d+1)^n(d^n+2)^{n-1},\qquad a_i\in\mathbb R^n.
\]

Here “rational arc” means rational dependence on the parameter; it does not
mean rational coefficients. Negative powers are allowed. The displayed
bound grows exponentially with dimension and is not a short-circuit bound.
The theorem concerns finite limiting values of polynomial maps, so applying
it to an objective tending to minus infinity needs a separate reduction.
It is not, as stated, an exact feasible-curve theorem for a constrained
mixed-integer problem.

For clarity, a basic obstruction separates polynomial paths from general
semialgebraic paths. This is an elementary comparison example, not a claim
from either cited paper:

\[
                f(x,y)=x^2(xy-1)^2-x.
\]

It tends to minus infinity along \((t,1/t)\). On every polynomial path
\((p(t),q(t))\), it is bounded below as \(t\to+\infty\): if \(p\) is
nonconstant, \(pq-1\) is a nonzero polynomial and the nonnegative square
term has degree greater than \(p\); if \(p\) is constant, the conclusion
is immediate. Thus polynomial-coordinate escape is a substantive property
of the proposed convex quadratic class, not a general consequence of curve
selection.

## 4. Other polynomial unboundedness certificates

Nie and Yang, *The Multi-Objective Polynomial Optimization*, Math. Oper.
Res. 49 (2024), 2723–2748,
[full preprint, Appendix A](https://arxiv.org/pdf/2108.04336),
give a moment certificate supported on the homogenized feasible set at
infinity. Theorem A.1(ii) requires a negative top-degree objective value at
an infinity point approachable by homogenized feasible points. Closedness
at infinity is a sufficient global hypothesis for this approachability.
The paper explicitly states in Question 7.1 that its certificate is
sufficient and need not be necessary. It does not provide the proposed
mixed-integer polynomial curve or its circuit-size bound.

There is a concrete distinction even for native PSD data: for
\(q_0(u,v)=u^2-v\), the top homogeneous part \(u^2\) is nonnegative,
although the unconstrained objective is unbounded below. Thus a certificate
requiring strict negativity of the top homogeneous part can miss the
linear escape which the recession reduction detects.

Rele and Nedić, *A Certificate of Unboundedness for Polynomial Optimization
Problems* (May 2026),
[arXiv:2605.09162](https://arxiv.org/html/2605.09162v1),
propose directional sampling. The operational test evaluates homogeneous
components at a direction and requires the highest nonzero component of
the objective and of every constraint to be negative. Such a test proves
eventual strict feasibility and objective decrease along that ray. It is a
sufficient detection method, not a necessary-and-sufficient characterization
by curved paths. It can miss both constraints that remain constant along
an escape direction and problems whose escape requires a curve. This
comparison uses the operational ray test; it does not independently endorse
all the preprint's statements about asymptotic functions.

Nguyen Hong Duc and Vu Trung Hieu, *Deciding lower-boundedness of
polynomials* (2025),
[arXiv:2511.22807](https://arxiv.org/html/2511.22807v1),
give a lower-boundedness decision procedure for an unconstrained real
polynomial. Theorem 5.1 characterizes lower-boundedness through a Sturm
count for a non-critical tangency-value polynomial over a Puiseux-series
field, after choosing a suitable generic center. Proposition 3.7 uses
curve selection at infinity and Nash curves. This is another established
algebraic route to deciding unboundedness; it does not establish the
proposed mixed-integer polynomial-circuit representation or its fixed
Hessian-span bit bound.

## 5. Integer polynomial optimization already considers curved escape

Del Pia, *Towards a Geometric Characterization of Unbounded Integer Cubic
Optimization Problems via Thin Rays* (October 31, 2025),
[full preprint](https://optimization-online.org/wp-content/uploads/2025/11/ICP-thin-ray.pdf),
Theorem 1 recalls the ray characterization for rational linear or quadratic
objectives over integer points of a rational polyhedron. Proposition 1
shows that this fails for a rational cubic in dimension three. The
introduction explicitly identifies polynomial curves as a possible
alternative; the paper instead uses arbitrarily thin neighborhoods of
rays. Theorem 2 proves its thin-ray characterization for cubic objectives
in dimensions at most three.

This paper addresses polynomial objectives over polyhedra, including
nonconvex objectives, rather than convex quadratic constraint families.
It is nevertheless clear prior context for any claim about replacing rays
by curves in integer optimization. The proposed result should not be
advertised as introducing that broad idea.

## 6. Direct predecessors of the stronger conditional oracle

Obuchowska, *On boundedness of (quasi-)convex integer optimization
problems*, Math. Methods Oper. Res. 68 (2008), 445–467,
[full primary text](https://link.springer.com/content/pdf/10.1007/s00186-007-0196-3.pdf),
is a direct predecessor. Corollary 5.1, p. 465, states continuous–integer
unboundedness equivalence conditional on integer feasibility. Rationality
is a standing assumption. The faithfully convex branch requires the
decomposition \(f_i=F_i(c_i+B_ix)+a_i^Tx+d_i\) and condition (2.1):
recession directions belong to \(\ker B_i\). Rational PSD quadratics
satisfy this through rational \(LDL^T\) factorization; square roots are
unnecessary.

Algorithm A, pp. 461–462, tests objective descent in the common linear
recession system, then retains implicit-equality rows. Theorem 5.1 proves
correctness. Page 466 explicitly claims polynomial time using polynomially
many LPs and iterations. For native rational quadratics, the original
matrices suffice throughout, so no decomposition-size obstacle arises.
Page 447 states that the results extend to mixed-integer programming.
The formal corollary uses pure integers; its integer restoring displacements
preserve any selected subset of integral coordinates, supporting that
extension. Thus the proposed conditional oracle and equivalence should
be credited to this prior work, not presented as new conclusions.

Caron and Obuchowska, *An algorithm to determine boundedness of
quadratically constrained convex quadratic programmes*, European J.
Oper. Res. 80 (1995), 431–438,
[primary abstract](https://www.sciencedirect.com/science/article/pii/0377221793E0244R),
already treats a convex quadratic objective under convex quadratic
constraints. It gives at most \(\min\{m-1,n-1\}\) iterations, each
identifying implicit equalities in a homogeneous linear system using LPs,
and reduces both constraints and dimension. The full 1995 article was not
obtained here; the abstract suffices to establish this methodological
predecessor. The later full 2008 text supplies an explicit polynomial-time
claim and the integer extension.

Nguyen, Nguyen, and Sheu, *Extension of Eaves Theorem for Determining the
Boundedness of Convex Quadratic Programming Problems*, Taiwanese J. Math.
24 (2020), 1551–1563,
[published text](https://scispace.com/pdf/extension-of-eaves-theorem-for-determining-the-boundedness-2sx5x0yqwf.pdf),
Theorem 1.1 characterizes boundedness through a subset of rows whose common
recession directions annihilate their linear parts. Its introduction
explicitly connects this characterization to the 1995 algorithm and an
earlier dual LP approach. Example (1.5) is the parabola escape
\(\min\{-x_1:x_2\ge x_1^2,\ x_1,x_2\ge0\}\), illustrating that an
original decreasing ray need not exist.

The feasibility promise is material. These are boundedness tests on a
nonempty mixed-integer instance; they do not solve unrestricted
mixed-integer feasibility or supply a short feasible point. A short
conditional reduction trace must likewise be distinguished from a full
certificate that includes a feasibly encoded anchor.

## 7. The distinction the proposed theorem must establish

The meaningful proposed package is the following, subject to proof:

1. A feasible escape map has actual polynomial coordinates, objective
   \(q_0(a)-\beta T\) with \(\beta>0\), and mixed-integer samples at
   nonnegative integer \(T\).
2. Repeated lifting can be encoded by an arithmetic circuit of polynomial
   size, with polynomial-size rational instructions relative to the input
   and the encoded anchor bounds, without fixing the integer dimension.
   Expanded polynomial degree and coefficient length need not be polynomial.
3. A feasible algebraic anchor has a controlled exact representation when
   both integer dimension and continuous Hessian span are fixed. The
   nonconstant increments are integral, so irrationality is confined to the
   anchor rather than spread over new algebraic extensions.
4. A derivation certifies feasibility for the stated parameter range and integer
   preservation. A short arbitrary circuit alone is not a proof that its
   sign conditions can be verified in polynomial time.

Two technical qualifications matter when stating this package. A continuous
curve into \(\mathbb Z^k\) has constant integer coordinates, so an escaping
integer assignment must be required only at integer parameter values.
Also, when an eliminated coordinate is integral, substituting
\(C(1+\|y(T)\|^2)\) does not itself preserve integrality if \(y\) contains
algebraic continuous coordinates. An integer-coefficient polynomial
majorant, encoded without expansion, addresses that separate obligation.

Repeated squaring readily explains why circuit size and dense size differ.
For the chain \(x_{i+1}\ge x_i^2\), minimizing \(-x_1\) has a polynomial
escape whose coordinate degrees double at each stage. Any polynomial
escape with nonconstant \(x_1\) has the same successive degree lower
bounds. This elementary family motivates succinct encoding, but its
continuous Hessian span grows with the chain; it does not establish a
degree lower bound under fixed Hessian span.

## 8. Audit limits and checks

Searches covered polynomial paths and rays, effective curve selection at
infinity, Laurent arcs, convex-polynomial unboundedness, integer polynomial
optimization, and the related f-asymptote/q-asymptote literature. Primary
texts were inspected for the comparisons above. No source located in this
audit proves the complete proposed package, but absence from this search
does not establish novelty. The targeted command
`git diff --no-index --check /dev/null research-20260927/succinct-unboundedness-prior.md`
reported no whitespace errors; its exit status was 1 because the new file
differs from `/dev/null`. No project-wide tests or CI checks were run.
