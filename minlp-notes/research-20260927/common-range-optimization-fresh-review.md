# Fresh adversarial review of common-range exact optimization

Date: 2026-09-28. This review checks the finished argument in
[common-range-optimization.md](common-range-optimization.md), including
its proposed exact-output extension. The reviewer did not develop the
original threshold, recession, or recovery arguments. The review read the
earlier investigation, then independently reconstructed the claims and
checked the subsequent Moore--Penrose chart simplification. No main
manuscript edits were made by this reviewer.

**Finding.** No substantive gap was found in the threshold, continuous
value and attainment, bounded-integer value and attainment, or exact
continuous optimizer arguments. The exact-output argument is valid with
the rational row normals in equation (11). This conclusion depends on the
stated exact one-quadratic algorithm and quantitative real-algebraic
imports. It does not establish publication priority, practical running
time, or unrestricted mixed-integer value computation.

## 1. Singular charts and their scope

After the common-kernel change of coordinates, the native rows have
constant matrix form \(Cv\le d(a)\). The objective Hessian restricted
to \(v\) is PSD. At a minimum-norm fiber optimizer, take an independent
basis of all active row normals. Small motions in either sign along
\(\ker C_I\) remain feasible, so the objective gradient belongs to
\(\operatorname{range}C_I^T\). Basis multipliers can have either sign.

For the symmetric KKT matrix

\[
 M_I=\begin{pmatrix}Q&C_I^T\\C_I&0\end{pmatrix},
 \qquad
 \ker M_I=(\ker Q\cap\ker C_I)\times\{0\}.
\]

Multiplication by the primal kernel vector proves this identity using
PSD and row independence. Motion along that primal kernel preserves the
objective; minimum norm makes the selected optimizer orthogonal to it.
The primal part of the Moore--Penrose solution is therefore the selected
optimizer. This handles a singular KKT matrix and zero active
multipliers. For example, minimizing \(v_1^2\) with \(v_2\ge1\)
requires the active row even though its objective multiplier is zero.

The pseudoinverse is rational with polynomial coefficient bits. One can
verify the manuscript's formula by splitting the space orthogonally into
the range and kernel of the symmetric matrix: \(M+ZZ^T\) acts as
\(M\) on the first and invertibly on the second. Rational minors then
bound its inverse without dependence on the retained parameter values.

The resulting map \(v_I(a)\) has degree at most two. Its feasibility
domain only checks the original rows after substitution. It is harmless
that a pseudoinverse may have been evaluated at an inconsistent KKT
right-hand side: every retained chart point is still genuinely feasible.
Conversely, at least one chart contains each finite fiber minimum.
These two facts give the exact union of threshold charts. Their values
are quartic, as required by the example \(v\ge u^2\), objective
\(v^2\).

This coverage argument needs finite fiber minima. The unbounded-fiber
repair is therefore essential. Global PSD of the objective annihilates
its cross blocks on \(\ker Q\), making recession descent independent
of the retained parameters. If a direction exists, all nonempty fibers
admit every threshold. Otherwise, elimination of the objective kernel
reduces each fiber to a positive definite quadratic plus a finite
polyhedral value function on a closed polyhedron. A dual feasible
vector supplies an affine lower bound, proving coercivity and attainment.
This reasoning is valid for irrational parameter values.

PSD only on the eliminated subspace would not give the same uniform
dichotomy. For instance, the objective \(uv\) on \(v\ge0\) has
zero \(vv\) Hessian, but its fiber is unbounded below for \(u<0\)
and has finite minimum for \(u\ge0\). The manuscript requires the
stronger assumption where it is needed.

## 2. Threshold radius, positive gap, and integer bounds

A nonempty chart is a basic closed quartic set in the retained
coordinates. Its meeting radius bounds one point; polynomial evaluation
of \(v_I\) bounds the original point without adding nonlinear
coordinates. In the recession case, the normalized rational direction
and a small native feasible point give the alternative threshold witness.

For the boxed residual problem, projection of the compact original
epigraph is compact. Each chart is closed and is a subset of that
projection, so each chart is compact too. If the minimum residual is
positive, imposing \(sy=1\) produces compact reciprocal charts.
The containing-radius theorem bounds their largest reciprocal
coordinate. This supplies the needed lower bound on the positive
residual. A meeting-radius argument alone would not suffice.

The retained exact objective cut does not enter the native approximation
error. A feasible point of the lifted polyhedron plus that cut violates
each approximated native row by less than the positive residual gap.
Thus its integer assignment has an original feasible completion. The
argument does not assert that the returned lifted continuous coordinates
themselves satisfy the original constraints.

For bounded integers, all fiber matrix and polynomial coefficient bounds
are uniform after substitution. Without integer bounds, the full-kernel
definition of \(\rho\) removes integer-continuous cross terms in the
eliminated variables. The threshold projection then has a formula with
only \(\rho\) existential variables, bounded degree, and polynomial
coefficient bits. Its convexity comes from the original convex problem;
individual quartic charts need not be convex. Applying the integer-witness
bound to the union is valid, even when that projection is not closed.

I inspected [Khachiyan--Porkolab, Theorem 1.1 and its preceding
feasibility reduction](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf),
pp. 207--208. Its witness bound omits predicate count; its algorithmic
bound in Theorem 1.2 does not. The manuscript uses only the former to
print an integer box. I also inspected [Del Pia, v2, Proposition
4](https://arxiv.org/html/2311.00099v2#S4.SS2): it supplies the stated
FPT feasibility algorithm for a rational polyhedron with one PSD
quadratic inequality and unrestricted continuous dimension.

## 3. Exact values and attainment

The primary coefficient statement was checked in [Basu's author survey,
Theorem 2.27](https://www.math.purdue.edu/~sbasu/raag_survey2011_final-sep4-2014.pdf),
also available in the repository text. Both the degree of each output
polynomial and its coefficient-bit bound depend on degree and variable
blocks, independently of predicate count. Output count and algorithmic
cost do depend on it. This distinction supports using the exponential
chart family for existence bounds without enumerating it.

The scalar sublevel projection has a finite boundary precisely at a
finite infimum. Some nonzero polynomial in a quantifier-free description
must vanish there; otherwise all signs are locally constant. This yields
the degree and height bounds for an unattained infimum as well. The
uniform root bound justifies the one very negative threshold query.
Rational bisection encloses an unattained endpoint even when an equality
query returns infeasible. Certified algebraic recognition then applies.

Conditional on attainment, append a polynomial and rational isolating
interval for the value to one optimal chart. A meeting radius and the
chart map give a uniform optimizer box. Enlarging by a feasible-point
box ensures that the boxed problem is nonempty. Its attained value equals
the original infimum exactly when the original infimum is attained.
The extra degree in this radius call is correctly absorbed into a generic
computable parameter function.

The finite integer box is indispensable in the stated mixed-integer value
proof: a finite minimum of fiber infima equals a single fiber infimum.
The uniform conditional optimizer box then supports attainment testing
and integer-coordinate bisection. No bound on all feasible continuous
points is being assumed. Infeasible restricted boxes must be treated as
negative optimal-set queries, as the construction requires.

For a simple nonattainment boundary, the cone
\(\|(2,x-y)\|\le x+y\) describes positive \(x,y\) with
\(xy\ge1\). Minimizing \(x\) has infimum zero, unattained.
This is within the SOC scope and confirms why a separate attainment
argument is necessary.

## 4. Exact optimizer output and its arithmetic

On the compact convex optimal set, the objective is constant on every
segment. PSD therefore gives \(Q_0(x-y)=0\), so every component of
\(g=Q_0x+a_0\) is constant. Bisection with a rational affine cut on
that expression uses only rational-data value queries and approximates
this one fixed vector. The ambient number of gradient coordinates affects
the number of queries polynomially.

The projected optimal set is compact and convex. Its minimum-norm
point \(u_*\) is unique. If \(u=Lx\), then \(\ker L\) is the
original common kernel; hence the added quadratic form \(L^TL\)
annihilates that kernel and does not increase the range parameter.
Minimum-norm value bisection, the projection inequality, and coordinate
bisection on a near-minimum slice give an approximation to the same
\(u_*\) at every accuracy. Restarting the coordinate box is necessary:
an earlier retained box need not contain \(u_*\) itself.

The joint-degree argument in Section 6 of
[the optimizer encoding note](common-range-optimizer-witness.md) survives
an independent reconstruction. The formula selecting \((u_*,\theta)\)
uses only parameter-controlled variable blocks. A product of coordinate
degree bounds has only \(r+1\) factors. Every gradient coordinate is
a rational polynomial evaluation at one small-field chart optimizer.
There is consequently no product of degrees over the ambient gradient
coordinates. Taking the compositum of these two fields still gives a
parameter-only degree bound. Coordinate heights and primitive-element
recovery have polynomial overhead in ambient dimension and those bounds.

After fixing \(u_*\), the completion system has rational normals and
algebraic right-hand sides. The objective equations are correctly written
as

\[
 Q_0x=b,\qquad
 a_0^Tx=\theta-c_0-\tfrac12x_0^TQ_0x_0,
 \qquad b=g-a_0,
\]

where rational-matrix elimination supplies \(Q_0x_0=b\). Their
equivalence to the selected objective value follows because
\(x-x_0\in\ker Q_0\). Replacing the second row by an expression
with \(g\) as a row normal would lose the rational-matrix property;
dropping it can admit nonoptimal points.

All right-hand sides are polynomial expressions of degree at most two in
the recognized tuple, with rational coefficients of polynomial length.
A common algebraic denominator must be squared for their quadratic
terms. Clearing denominators and bounding all conjugates in the already
bounded-degree field gives coefficient-bit bounds \(f(r)N^C\).
Minimum-norm fiber points use an active Gram matrix with rational
entries, so they remain in that field and have the same type of bound.

I checked the rational outward-approximation recovery in
[the feasible-witness note, Section 5](common-range-witness-recovery.md).
The exact fiber lies in every relaxed fiber, so their minimum norms do
not exceed its minimum norm. A uniform rational-matrix Hoffman bound
repairs each relaxed optimizer within \(O(\delta)\). The projection
inequality then bounds its distance to the fixed exact optimizer by
\(O(\sqrt{\delta})\), with explicitly bounded coefficients. Thus
only polynomially many precision bits are needed. Equalities represented
by both signs remain valid in this argument. No unsupported general
algebraic-matrix LP algorithm is used.

Repeated calls do not create hidden XP dependence. Added norm and affine
rows are only polynomially many; current interval endpoints replace old
ones. Appended precision and box bits enter all chart estimates with an
absolute polynomial exponent. The recognition precision is itself
\(f(r)N^C\). Composing the fixed number of polynomial overheads changes
the absolute exponent and parameter factor, rather than putting \(r\)
in the exponent of \(N\).

## 5. Targeted checks and remaining limits

The command

```text
python research-20260927/check_common_range_optimization_output_review.py
```

passed 36 exact optimal-set points and 12 checks that the scalar
objective equation cannot be omitted. The examples have native range
dimension one while the PSD objective rank ranges from one to twelve.
Two rational cones force \(u=\sqrt2\), affine rows impose
\(v_j\ge j u\) and \(w\ge0\), and a bounded free coordinate
makes the optimal set positive-dimensional. The objective is
\(\sum_jv_j^2+w\). Exact symbolic calculations confirm the constant
gradient, the rational-normal objective equations, and one common
quadratic field. These examples challenge the new output argument; they
do not prove its universal bounds or implement its recognition algorithm.

A separate nested reviewer was assigned the joint-field and affine-fiber
output argument without this review's conclusions and found no substantive
gap. That reviewer also obtained an independent nested check of the
Hoffman and Gram-matrix completion argument, including paired equality
rows. Two useful clarifications emerged: the right-hand-side height must
be bounded as well as the field degree, and final common-field recognition
can include the previously recovered primitive generator along with the
completion coordinates. This retains the field already used. The term
“optimal set” is more precise than “optimal face”: minimizing \(x^2\)
over \(\mathbb R\) has optimal set \(\{0\}\), which is not a face. Mathematical source imports, arithmetic
bounds, and oracle reductions remain mathematical proofs rather than
Lean formalizations. No project-wide checks or CI inspection were run.

A targeted inline `python -` document check passed for this review and its
exact-check script: four local links, Python syntax, paired mathematical
delimiters, whitespace, control characters, and final newlines. Those
checks establish document consistency rather than mathematical validity.

The closest inspected algorithmic comparator, Del Pia's one-quadratic
theorem, already permits arbitrary objective rank over a polyhedron.
The proposed additional capability concerns many nonlinear native rows
sharing a small common range. The chart and elimination methods are
classical, and the [separate prior audit](common-range-fpt-prior.md) does
not establish novelty. The exact FPT conclusion is materially stronger
than a fixed-parameter polynomial-time statement with a parameter-dependent
input exponent, but it provides no practical precision or speed guarantee.
