# Independent review of exact continuous SOCP optimization

Date: 2026-09-28. Reviewed manuscript:
[continuous-socp-optimization.md](continuous-socp-optimization.md).
I read the full saved reduction and its principal theorem dependencies.
I found no gap in the reduction or its coefficient-sensitive running time.
All theorem inputs have completed independent review, including the
[minimum-norm optimizer theorem](nonconvex-attainment-and-optimizer.md)
and its [final review](nonconvex-attainment-review.md). I independently
read its full initial proof and its simpler two-limit replacement and
found no gap in the required dependency. The value, attainment decision,
and canonical optimizer recovery statements pass this review.

This is an independent proof and scope review, not formal verification
or a publication-priority assessment. No change to the SOCP optimization
algorithm was needed during this review.

## 1. Exact status and value do not require attainment

Each rational cone contributes its squared quadratic residual and its
affine right-side sign condition. The squared Hessians can be indefinite.
Keeping both parts gives precisely the original closed convex set, so the
[nonconvex finite-infimum bound](nonconvex-finite-infimum.md) applies
without assuming that the squared polynomials are convex.

For a nonempty input, the bound on every finite infimum supplies an
effective integer \(M\) with \(|\theta|<M\) whenever \(\theta\)
is finite. Feasibility at the rational objective threshold \(-M-1\)
therefore characterizes unboundedness below. This does not use an optimizer,
a recession ray, Slater's condition, or finite attainment for native PSD
quadratic systems. General SOC sets need not satisfy that last conclusion.

Every rational threshold adds only an affine row, so the squared-Hessian
span stays \(h\). The [SOCP feasibility theorem](socp-hessian-span-frontier.md)
is a deterministic decision oracle for these thresholds. If a bisection
midpoint equals an unattained infimum, the oracle answers no; retaining
that midpoint as the lower endpoint still encloses the infimum. No
strict-inequality oracle is required. The initial upper threshold is
strictly above the infimum and therefore feasible.

The interval approximations meet the reviewed
[Kannan–Lenstra–Lovász recognition input](algebraic-recognition-source-review.md).
Degree and logarithmic coefficient bounds are known before recognition.
Further approximation and univariate separation select the intended real
root. Passing from an annihilator to its minimal-polynomial factor
preserves the stated bounds. An empty domain is handled first.

This gives the exact finite infimum whether attained or unattained,
independently of the additional optimizer theorem.

## 2. The optimizer theorem must supply the correct box

The required dependency bounds some **global minimum-norm optimizer**,
not merely a feasible point or an optimizer in a previously chosen box.
In the SOCP application the nonempty optimal set is closed and convex.
Its minimum-norm point exists by compact restriction and is unique by
strict convexity. The dependency's algebraic point is therefore exactly
the canonical point used later by the algorithm.

The dependency regularizes by \(\varepsilon\|x\|^2\) in the original
coordinates, not by the norm of the auxiliary Hessian-basis lift.
Comparison with an original minimum-norm optimizer bounds all exact
regularized minimizers uniformly, including their uniquely determined
lifted coordinates. An unknown fixed box can therefore be chosen strictly
larger than all those points. At fixed \(\varepsilon\), every limit
of perturbed minimizers as the generic perturbation tends to zero is an
exact regularized minimizer. A sequence of boundary points would have a
boundary cluster point, contradicting strict containment. Thus all
selected box rows are eventually inactive.

Only original polyhedral rows enter the resulting affine charts and KKT
systems. The unknown radius therefore contributes no coefficient to the
algebraic calculation. Removing the generic perturbation first and norm
regularization second selects a global minimum-norm optimizer. Coherent
tuple subsequences justify every coordinate and rational-linear-form
annihilator at that same point. The primitive-element argument then gives
the required joint degree. This explains why the dependency supplies
more than an arbitrary feasible-point bound, without assuming a numerical
optimizer radius in its proof.

A coordinate coefficient bound \(H_*\) gives the rational box
\[
 B=[-R,R]^n,\qquad R=2^{H_*+2}.
\]
Cauchy's bound places the canonical optimizer in \(B\) whenever an
optimum exists. Constructing this conditional universal bound does not
presuppose an attainment decision.

For \(C=F\cap B\), emptiness excludes attainment by that implication.
Otherwise \(C\) is compact and its affine minimum \(\beta\) is
attained. Consequently
\[
 \theta\text{ is attained on }F
 \quad\Longleftrightarrow\quad\beta=\theta.
\]
The forward direction uses the optimizer bound; the reverse direction
uses compact attainment. A box preserving only nonempty feasibility would
not establish the forward implication.

Equality of the represented real algebraic values is decidable using
univariate polynomial gcd and root comparison, with polynomial bit
complexity in their degrees and heights. Their isolating intervals select
the intended roots. Numerical closeness is not used as an equality test.

## 3. The optimal-face oracle keeps the conic data rational

After attainment is established, the algorithm keeps
\(C^*=\{x\in C:f(x)=\theta\}\) implicit. For rational closed
affine restrictions \(K\), optionally with one squared-norm cap,
it checks \(C\cap K\) and computes
\(\beta_K=\min_{C\cap K}f\) when nonempty. Compactness gives
\[
 C^*\cap K\ne\varnothing
 \quad\Longleftrightarrow\quad
 C\cap K\ne\varnothing\ \text{and}\ \beta_K=\theta.
\]
The number \(\theta\) appears only in a comparison between recovered
algebraic outputs. It is never supplied as a coefficient to the rational
SOCP oracle or its rational LP lift. No LP algorithm over a number field
is silently assumed.

Compactness is essential even after the original optimum is attained.
For example, take
\[
 F=\{(x,y,z):x,y\ge0,\ \|(2z,x-y)\|_2\le x+y\},
 \qquad f(x,y,z)=x.
\]
The squared residual is \(4z^2-4xy\). The original minimum is
zero and is attained at \(x=z=0\). The rational affine restriction
\(K=\{z=1\}\) gives \(xy\ge1\), whose infimum for \(x\)
is still zero but is unattained. Equality of unboxed infima would
therefore give a false positive for optimal-face intersection. The
manuscript's compact \(C\cap K\) prevents this failure.

For rational \(r\ge0\), the norm cap has the rational cone form
\[
 \|(2x,r-1)\|_2\le r+1.
\]
Its squared residual is \(4\|x\|^2-4r\), with Hessian \(8I\).
Thus every such query increases the original span by at most one,
independently of accuracy and ambient dimension. The right side is
positive, so its sign condition is valid.

## 4. Every approximation targets the same optimizer

Norm bisection maintains an enclosing interval for
\(\nu=\|x^*\|^2\) with a feasible upper cap \(u\). The lower
endpoint need not be infeasible. At termination,
\(u-\nu\le2^{-2p}/16\). Convexity and norm optimality imply
\[
 \langle x^*,y-x^*\rangle\ge0,\qquad
 \|y-x^*\|^2\le\|y\|^2-\nu
 \quad(y\in C^*).
\]
Every retained point under the norm cap is within \(2^{-p}/4\)
of \(x^*\).

Coordinate bisections preserve a nonempty intersection with this capped
optimal set. Closed half intervals cover boundary-only feasibility.
When each coordinate interval has width at most \(2^{-p}\), its
midpoint is within \(3\cdot2^{-p}/4\) of the corresponding canonical
coordinate. The midpoint itself need not be feasible.

Restarting from the universal box at each accuracy is necessary:
a previous retained coordinate box need not contain \(x^*\), although
it contains a nearby point under its old norm cap. The manuscript
explicitly restarts. Its approximations target one fixed tuple at every
accuracy, as required by the
[common-field construction](constructive-common-field-recovery.md).
That theorem also receives a joint-field degree bound; separate coordinate
degree bounds alone would not justify the claimed common representation.

## 5. Coefficient-sensitive costs compose as claimed

The [SOCP witness analysis](socp-exact-witness-recovery.md) and feasibility
proof give query cost
\[
 (\tau_q+1)^{O(1)}S_q^{O(s+1)},
\]
where the coefficient-size exponent is absolute. For affine value
recovery, each threshold adds one affine row. Structural size remains
polynomial in the original structural size and independent of precision.
Bisection increases coefficient bits, with query count and recognition
precision polynomial in the known degree and height. These factors
preserve the displayed cost form.

Appending the optimizer box adds \(2n\) rows with large rational
coefficients, not a precision-dependent number of structural positions.
Optimal-face queries store two endpoints per coordinate and at most one
norm cone, so their number of native rows remains independent of
accuracy. The additional span is at most one. Exact comparison of
\(\beta_K\) with the known \(\theta\) has absolute polynomial
cost in their degrees and coefficient bits, absorbed by the same bounds.

Common-field conversion has absolute polynomial overhead in the joint
degree, coordinate heights, and requested precision. Composing it with
the approximation oracle therefore gives
\[
 (\tau+1)^{O(1)}S^{O(h+1)}\le N^{O(h+1)}.
\]
No coefficient-size quantity is raised to an exponent depending on
\(h\). The precision-dependent LP lift is solved and discarded;
its auxiliary dimension is not input to another algebraic theorem.
These details justify the stated exponent without inferring a running
time merely from output size.

## 6. Scope, older methods, and verification

This is an algorithmic consequence of structural algebraic bounds and
exact rational SOCP decision. Value bisection, algebraic recognition,
radius-based attainment tests, minimum-norm selection, and common-field
recovery are established methods. The optimizer dependency's comparison
also gives a weaker certificate from classical Grigoriev–Pasechnik
sampling after the finite value is encoded. Qualitative fixed-span
complexity should not be described as a separate new recovery mechanism.
The [attainment prior audit](nonconvex-attainment-prior-audit.md)
further derives the sharper degree bound for some optimizer by sampling
over the optimal-value field. Its corresponding coefficient-height bound
needs additional accounting, and sampling alone does not select the
minimum-norm optimizer. These distinctions limit what can be claimed as
new about the present dependency.

The [SOCP prior audit](socp-hessian-span-prior.md) derives the span-one
feasibility and projection cases from older bounds. This review does not
establish that exact optimization at span one is new or resolve priority
for general fixed span. The substantive candidate input is the
parameter-dependent precision bound, including canonical optimizer
encoding and its coefficient-sensitive accounting. A broader literature
comparison remains necessary before a priority claim.

The result covers continuous variables and affine objectives. It does
not establish mixed-integer SOCP optimization. A general rational PSD
quadratic objective cannot be passed to this rational-map cone theorem
merely by invoking an irrational Cholesky factor. The norm cones
actually used in the proof have an explicit rational representation.

The returned point permits independent native-row sign checks, including
every cone right-side sign. Its objective can be checked against the
recovered value in its own field: evaluate the value's minimal polynomial
at that objective and check the isolating interval. No compositum is
needed. The point alone does not certify the global lower bound or
minimum-norm selection; those conclusions use the proved algorithm.
No practical speedup or usable numerical precision estimate is established.

I ran two targeted inline Python commands with exact SymPy arithmetic.
They checked the hyperbola cone residual \(4-4xy\), its Hessian,
the substitution \((x,y)=(1/R,R)\), the norm-cap residual, the
norm-gap expansion, and the affine-slice residual \(4z^2-4xy\).
The boxed hyperbola value \(1/R\) was independently checked from
\(xy\ge1\) and \(y\le R\), with that feasible point for
\(R\ge1\). These finite checks support identities and boundary
cases; they do not prove the general algorithms or complexity bounds.

A targeted inline Python document check passed for this review's local
Markdown links, paired inline and display math delimiters, control
characters, trailing whitespace, and final newline. These checks establish
document consistency only. No Lean formalization, project-wide verification,
or CI inspection was performed.
