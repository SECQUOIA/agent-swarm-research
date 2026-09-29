# Independent review of the inactive-box finite-infimum proof

Date: 2026-09-28. Reviewed text: Section 12 of
[nonconvex-finite-infimum.md](nonconvex-finite-infimum.md).
I independently read the saved addendum, the original radius-parameter
proof, Sections 2--6 of the
[attained-optimizer proof](nonconvex-attainment-and-optimizer.md), the full
genericity lemma in the
[nonconvex certificate note](nonconvex-hessian-span-frontier.md), and the
[finite-quotient elimination lemma](explicit-span-separation.md).
No gap was found in the shorter proof. No mathematical correction was needed.
The original, separately reviewed radius-parameter proof remains valid.

This review checks the new reduction and its use of those dependencies.
It is not a new literature audit, a Lean formalization, or a verification
of the whole research package. In particular, it makes no priority claim.

## 1. Finite infimum supplies a box at each fixed parameter

The original feasible set is closed because all its constraints are weak
polynomial inequalities or equalities. If its objective has finite infimum
\(\theta\), then
\[
 q_0(x)+\varepsilon\|x\|^2\ge\theta+\varepsilon\|x\|^2
 \qquad(x\in S,\ \varepsilon>0).
\]
Thus regularization is coercive on the original feasible set, even if the
objective is indefinite or not coercive elsewhere. A nonempty closed
sublevel set below the value at any fixed feasible anchor is compact, so a
global regularized minimizer exists.

Comparison with that anchor gives the addendum's bound (14) for **every**
regularized minimizer. Bounding original coordinates also bounds their
unique quadratic lifts. Consequently, at each fixed \(\varepsilon\),
one finite integer box strictly contains all exact regularized minimizers
and their lifts. This is stronger than enclosing just one selected point
and is the property needed to exclude boundary clusters later.

The box can depend arbitrarily on \(\varepsilon\). Its size need not
have a known encoding bound, and its choice need not be semialgebraic.
Neither quantity becomes an input coefficient. No uniform bound on the
regularized minimizers is inferred from a finite, possibly unattained,
infimum.

For each fixed feasible \(x\),
\[
 \theta\le v_\varepsilon
       \le q_0(x)+\varepsilon\|x\|^2.
\]
Taking the upper limit as \(\varepsilon\downarrow0\), then the
infimum over fixed feasible \(x\), proves
\(v_\varepsilon\to\theta\). This argument does not require
attainment of \(\theta\), convergence of the minimizers, or a bound
on the rate at which they may diverge.

## 2. The boxes do not enter the genericity argument

The family of affine charts uses subsets of the original polyhedron's
rows. There are finitely many charts, their rational coefficients have
the claimed bounds, and they do not depend on any box. On each chart,
the ambient quadratic perturbations restrict surjectively to arbitrary
objective and selected constraint quadratics whenever \(\eta\ne0\).
The fixed term \(\varepsilon\|x\|^2\) does not change that
surjectivity.

The genericity lemma separately excludes dependent active gradients,
singular multiplier Hessians, and singular bordered KKT matrices. Keeping
both nonsingularity conditions is necessary for indefinite quadratics;
gradient independence and an invertible Hessian alone would not suffice.
For a positive band width, at most one orientation of each equation can
be active, so at most \(h\) multiplier variables are needed.

The finite-grid choice works simultaneously on this fixed finite family
with both \(\varepsilon\) and \(\eta\) formal. Degree bounds for
the bad polynomials depend on structural size, not coefficient magnitudes.
Consequently the chosen perturbation coefficients need only
\(S_0^{O(1)}\) bits. For a nonzero bad polynomial in the two parameters,
only finitely many \(\varepsilon\) make it identically zero in
\(\eta\). After excluding those values, its nonzero \(\eta\)-roots
leave an admissible positive tail at each fixed \(\varepsilon\).
No common tail or box across all regularization parameters is needed.

## 3. Every small-perturbation minimizer is eventually box-interior

At a fixed admissible \(\varepsilon\), an exact regularized minimizer
is feasible for the perturbed bands for all sufficiently small
\(\eta\). The perturbed problem on the chosen box is therefore
nonempty and compact. The perturbations converge uniformly on this one
fixed box, and every cluster point of perturbed minimizers satisfies the
exact lift equations.

Comparison with an exact regularized minimizer gives an upper bound
\(v_\varepsilon\) on the limiting objective. Feasibility of the
cluster gives the opposite inequality. Hence every cluster is a global
regularized minimizer of the original problem and lies strictly inside
the box. If there were boundary minimizers at arbitrarily small
\(\eta\), compactness would produce a cluster on the closed boundary,
contradicting this conclusion.

This proves eventual inactivity for **all** perturbed minimizers at each
fixed \(\varepsilon\). It justifies the original-row charts before
any KKT coefficient is formed. The argument is not circular: the boxes
are used only for compactness, and their rows disappear before the
algebraic bounds that will ultimately provide an explicit radius.

## 4. Only the scalar output needs an outer limit

At each fixed regularization parameter, finite pigeonhole selection gives
one original affine chart and one oriented active nonlinear subset on an
inner sequence. A second finite pigeonhole selection retains the same
choices along \(\varepsilon_\nu\downarrow0\). The number of
choices is independent of the varying boxes.

For a zero-dimensional chart, the fixed rational point gives the stated
rational limiting value directly. Otherwise the two nonsingularity
conditions give the reduced multiplier system and its nonsingular
Jacobian. The rational output is the perturbed objective. Its inner limit
is \(v_{\varepsilon_\nu}\), whose outer limit is \(\theta\).
There is no need for an outer primal or multiplier limit.

The finite-quotient lemma's lowest auxiliary-coefficient extractions work
over \(\mathbb Z[\varepsilon,\eta]\), since its norm estimates count
all formal variables. Extracting the lowest nonzero \(\eta\)-term
first gives a relation for every inner limiting value. Extracting the
lowest nonzero \(\varepsilon\)-term then gives a nonzero annihilator
of \(\theta\). A specialization making an intermediate relation
identically zero is permitted by the lemma's factor argument. It does
not invalidate the polynomial's nonzero formal coefficient or the final
limit argument.

At most \(h\) variables are eliminated, with multiplier degree
\(S_0^{O(1)}\) and coefficient-norm logarithm
\((\tau_0+1)S_0^{O(1)}\). Coefficient extraction does not increase
these bounds. Thus the resulting degree and coefficient bits have the
claimed forms \(S_0^{O(h+1)}\) and
\((\tau_0+1)S_0^{O(h+1)}\). The objective Hessian is correctly
excluded from \(h\): it enters the stationarity matrix but introduces
no additional active constraint multiplier.

## 5. Targeted checks and limits of verification

I ran `python -` with exact SymPy arithmetic for the addendum's example
\(xy=1\), \(x\ge0\), \(q_0=x^2\). Substituting \(y=1/x\)
gives the strictly convex positive-domain objective
\((1+\varepsilon)x^2+\varepsilon/x^2\). The command checked its
critical point, positive second derivative, value
\(2\sqrt{\varepsilon(1+\varepsilon)}\), annihilating relation,
zero value limit, divergent \(y\)-coordinate, and lowest-coefficient
extraction.

I also challenged a simultaneous-limit shortcut. Add the perturbation
\(-\eta y^2\) and use a box of radius
\(R_\varepsilon=\varepsilon^{-1/2}\) for sufficiently small
\(\varepsilon\). This box strictly contains the exact regularized
minimizer. At its feasible boundary point
\((1/R_\varepsilon,R_\varepsilon)\), choosing
\(\eta=\sqrt\varepsilon\) gives an objective tending to
\(-\infty\). The same exact command checked that limit. This does
not challenge the manuscript, which takes the inner limit first; it
confirms why an arbitrary simultaneous parameter choice is unjustified.

The command additionally checked the cone residual, continuous Hessian,
and boundary points in the boxed mixed-integer note's two-fiber example.
Its first run stopped on a SymPy structural-equality assertion comparing
expanded and unexpanded forms of the same polynomial. Replacing that
test with exact polynomial subtraction gave a passing rerun. This was
a check-script issue, not a failed mathematical identity.

A targeted inline Python document check passed for this review and the
scoped manuscript/status edits: local links, paired math delimiters,
control characters, trailing whitespace, and final newlines. A scoped
`git diff --check` also passed. These checks verify finite identities
and document consistency; they do not prove the universal algebraic
bounds. No project-wide checks or CI inspection were performed.
