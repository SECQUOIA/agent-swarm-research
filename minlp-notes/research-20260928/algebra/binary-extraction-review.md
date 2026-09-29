# Independent review of binary extraction at a known optimum

Date: 2026-09-28. Reviewer: `/root/frontier_algebra/binary_extraction_review`.
The [binary extraction proposition](binary-extraction-known-value.md)
passes this review. The full-Gram construction at the end was proposed
by this reviewer and independently rederived by the proposition's author.
I then checked its final written version. This is not presented as a
fresh noncontributor review of that extension.
Publication priority is unestablished.

## Scope and dependency checks

I read the complete
[coordinate-comparison theorem](../../research-20260927/rational-optimizer-posslp-coordinate-comparison.md),
the complete
[quaternion quartic realization](../../research-20260927/unit-quaternion-circuit-quartic-realization.md),
and its quantitative
[Hessian certificate dependency](../../research-20260927/sos-convex-quartic-realization.md).
I also inspected the sign compiler, its independent reduction review,
its literature comparison, and the statement and certificate interface
of the mixed-integer constraint-rank algorithm.

The source theorem supplies precisely the properties used here: an
explicit rational quartic F, a polynomial-size rational SOS expression,
a full rational positive definite Hessian Gram Q, a unique zero p in
the rational unit box, global curvature at least 3/2, and a designated
nonzero coordinate whose sign answers the original PosSLP instance.
The source constructs F without printing the expanded coordinates of p.
The short bridge introduces no operation requiring those coordinates.

This review independently checks the bridge and its certificate
interface. It does not present reading the source proofs as a new full
independent reconstruction of the quaternion compiler.

## Feasibility, value, uniqueness, and rank

For integral z with 0 <= z <= 1, the objective is F(x)+1/4.
Thus equality with the lower bound 1/4 holds exactly when x=p.
The two feasible intervals for the selected coordinate are [-1,0]
and [0,1]. The interval containing p_j is unique because p_j is
nonzero. This proves the stated optimizer and all three important
distinctions: the value is known, the optimizer exists, and the
optimizer is unique. The endpoints p_j=1 and p_j=-1 cause no issue.
If the nonzero promise were removed, p_j=0 would give two optimizers.

Both integer fibers are nonempty: x=0 is feasible for either binary
value. Every fiber is closed, and strong convexity makes its objective
coercive. The losing fiber therefore has an attained value strictly
above 1/4. No feasibility search over integer values is needed.

In standard form, the continuous rows are 0, 0, -e_j, and e_j.
Their rank is exactly one. The integer dimension is one. Bounds on
all coordinates of x must not be added when claiming this rank:
the assertion concerns a bounded optimizer, not a bounded feasible
region. In particular the unbounded remaining coordinates do not
prevent attainment because the objective is coercive.

Rationality of the winning optimizer is inherited. The losing fiber's
continuous optimizer need not be rational. No short expanded-fraction
bound is inherited or needed, since the requested output is one bit.

## The two convexity statements are distinct and correct

The ordinary Hessian is block diagonal with blocks Hessian(F) and 2.
It is therefore at least (3/2)I globally. The objective's rational SOS
expression gains the single linear square (z-1/2)^2.

For the additional strong SOS-convexity certificate, write

\[
 d=N+N^2,\qquad
 \rho=\frac{\det Q}{(\operatorname{tr}Q)^{d-1}},\qquad
 \eta=\min\{1,\rho/2\}.
\]

Every eigenvalue of Q is positive and no larger than its trace, so
Q is at least rho I and hence at least 2 eta I. Let E denote the
identity on the constant direction coordinates v in the Hessian basis
(v,x tensor v), and zero on its other coordinates. Then Q-eta E
is positive definite. Embed this Gram into the joint Hessian basis
and add the coefficient 2-eta for the new constant direction square.
The result is a rational positive semidefinite Gram for

\[
 (v,s)^{\mathsf T}
 [\nabla^2 H(x,z)-\eta I](v,s).
\]

This proves that H-(eta/2)||(x,z)||^2 is SOS-convex. Determinants,
traces, rational powers with exponent d-1, and the enlarged Gram all
have polynomial bit complexity in the explicit source input. Rational
positive semidefiniteness is exactly checkable. Rational weighted
squares can also be expanded into polynomially many rational squares
if that certificate format is desired.

The particular certificate modulus eta need not equal 3/2. Ordinary
strong convexity with modulus 3/2 does not by itself justify subtracting
3/2 from a supplied Hessian Gram. The current proposition correctly
keeps these assertions separate.

The joint full Gram cannot be positive definite for the stated H.
Set x=0, take a direction only in z, and let z vary. The Hessian
biform equals 2, whereas the full basis contains the monomial z s.
A positive definite Gram would bound this biform below by a positive
constant times 1+z^2, a contradiction. Consequently this construction
belongs to the global-curvature promise version of the rank theorem,
and has a checked strong SOS certificate, but does not belong to a
format that insists on a positive definite full joint Hessian Gram.

## Exact extraction, approximation, and significance

Mapping a PosSLP instance to this input and testing whether its unique
optimal binary block is one is a polynomial-time many-one decision
reduction. A polynomial-time exact search procedure returning the
optimal bit would put PosSLP in P. The statement does not prove that
PosSLP is outside P or that the problem is NP-hard.

This is a direct obstruction to dropping exact arithmetic from integer
selection merely because the integer dimension and continuous rank are
fixed. There are only two feasible integer candidates and the global
value is supplied. Thus enumeration, infeasibility, and the size of the
requested output are not the source of the reduction's difficulty.
Calling this an unconditional barrier to polynomial-time algorithms,
or to the numerical behavior of practical solvers, would overstate it.

For clarity, the wrong-fiber objective gap Delta obeys the elementary
bounds

\[
 \frac34 p_j^2\ \leq\ \Delta\ \leq\ \frac M2 p_j^2,
 \qquad
 M=\max_{x\in[-1,1]^N}\|\nabla^2F(x)\|_2.
\]

The lower bound follows from strong convexity and distance to the
wrong halfspace. For the upper bound use p-p_j e_j, which is feasible
in both fibers, and apply Taylor's integral formula along the segment
from p. The source construction provides no inverse-polynomial
separation assumption on |p_j|. Hence this reduction does not assert
hardness of obtaining a fixed objective accuracy or of recovering a
binary decision under a positive margin promise. A quantitative family
of branch gaps is not required for the proposition and is not claimed
to have been fully verified in this review.

The bridge is elementary; its substantive input is the source
coordinate theorem. It is useful as an implication and a clean solver
interface distinction, rather than an independent main advance.
The original source's novelty qualifications remain necessary.

## Literature and verification record

I read the local source comparison cited above and opened the primary
[ECCC record and abstract for Allender et al., On the Complexity of
Numerical Analysis](https://eccc.weizmann.ac.il/report/2005/037/).
That abstract defines the integer straight-line-program sign problem
and gives its numerical-computation context. It does not announce the
restricted mixed-integer quartic theorem considered here; this abstract
check does not rule out a relevant result elsewhere in the paper.

Additional searches used the queries `"PosSLP" "mixed integer"
convex optimization`, `"PosSLP" "rational" "strongly convex"`,
and `"optimization" "known optimal value" "search" hardness
convex integer`. The retrieved material did not supply a relevant
primary theorem for this bridge. That unsuccessful search is not
evidence of novelty. No separate priority claim is supported.

The proof checks above are analytical. A numerical experiment would
not materially strengthen this elementary bridge, and none was run.
Targeted documentation checks were run for this review's local links,
final newline, whitespace, and display-math delimiters, followed by
`git diff --check -- research-20260928/algebra/binary-extraction-review.md`.
No project-wide verification, CI inspection, or Lean check was run.

## Separate extension: restoring a positive definite full joint Gram

The following extension is now recorded separately from the base
proposition. I proposed the polynomial correction and Gram arrangement;
the author independently rederived its full directional Hessian and
Schur complement. I read the final added section and found its formulas,
constant choices, size statements, and retained promises correct. It
preserves all feasible mixed-integer objective values, but the full list
of original certificate promises must not be imported without further
work.

Set t=z-1/2 and choose rational constants

\[
 \delta=\frac14,\qquad
 0<\varepsilon\leq\min\{\rho/4,1/(100N)\}.
\]

Define

\[
 \widetilde H(x,z)=F(x)+(z-1/2)^2
 +\varepsilon z(z-1)\|x\|^2
 +\delta z^2(z-1)^2.
\]

Both added terms vanish at z=0 and z=1. Thus every feasible objective
value, the unique mixed optimizer, rank one, and the known optimum 1/4
are unchanged.

In the centered full Hessian basis, group the coordinates as
(v,x tensor v), s, t v, x s, t s. The proposed rational Gram has
the following blocks:

- A=Q-(epsilon/2)E on (v,x tensor v).
- 7/4 on s, and 2 epsilon I on each of t v and x s.
- 3 on t s.
- The only additional cross block is b=4 epsilon d between
  (v,x tensor v) and t s, where d is zero on v and is the vectorized
  identity on x tensor v. Thus ||d||^2=N.

The cross term is 8 epsilon t s times the scalar product of x and v,
which is the required mixed Hessian term. Direct differentiation also
gives the two 2 epsilon blocks, the correction -(epsilon/2)E, and
the scalar coefficients 7/4 and 3.

Since A is at least (rho/2)I,

\[
 b^{\mathsf T}A^{-1}b
 \leq\frac{32\varepsilon^2N}{\rho}
 \leq8\varepsilon N\leq\frac{2}{25}<3.
\]

The Schur complement is positive and all other blocks are positive.
The full centered Gram is therefore positive definite. Replacing t
by z-1/2 is an invertible rational change of the full Hessian basis,
so it preserves positive definiteness and polynomial encoding length.
It supplies a positive rational strong-convexity bound, but the
particular bound 3/2 is not asserted by this calculation.

The objective remains globally positive under these constants. Indeed,
using ||p||^2<=N and F(x)>=(3/4)||x-p||^2 gives

\[
 \widetilde H(x,z)
 \geq (3/4-\varepsilon/2)\|x-p\|^2
       -\varepsilon N/2+t^2+\tfrac14(t^2-1/4)^2
 \geq\frac1{64}-\frac1{200}=\frac{17}{1600}>0.
\]

Global positivity and the displayed Hessian certificate are distinct
from an explicitly constructed short rational SOS expression for the
objective itself. The added term epsilon z(z-1)||x||^2 is not a square
or nonnegative term. A separate rational SOS construction would be
needed to add the base objective-certificate promise to this extension.
None was pursued or is part of the claimed refinement. The subsequent
[fresh noncontributor review](binary-joint-gram-fresh-review.md) independently
reconstructed the full joint Gram, its rational margins, positivity, and
the unchanged extraction reduction. It found no substantive defect and
completed separate exact symbolic checks.
