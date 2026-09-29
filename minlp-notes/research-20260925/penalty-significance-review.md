# Independent significance review of the penalty results

Date: 2026-09-25. Scope: the one-binary construction in
[parametric-exploration.md](parametric-exploration.md), the binary-box and
unit-data constructions in [minimum-penalty-hardness.md](minimum-penalty-hardness.md),
their source interpretation, and their place in the research program.
This review did not edit the candidate notes.

**Verdict:** the two main constructions are correct within their stated
encoding and exactness conventions. They give precise negative answers to
questions in the inspected December 2025 Lefebvre–Schmidt manuscript. The
strongest defensible additions are an optimized-multiplier encoding obstruction
already for one binary convex QCQP, and polynomial-factor calibration hardness
already for a native binary box with a linear objective. These are credible
contributions to a focused theoretical note. They do not yet constitute a new
general penalty theory, a demonstrated solver advance, or an advance clearly
more consequential than the repository's strongest geometric and algorithmic
results. Resolving an explicitly stated question matters, but does not remove
the need to assess how much reasoning and useful capability are new.

## 1. What the source questions actually ask

I inspected the retained text of [Lefebvre and Schmidt's manuscript dated
15 December 2025](https://optimization-online.org/wp-content/uploads/2024/07/exact-penalty-for-minlp-1.pdf),
including Definition 1, Assumption 5, Theorem 14, and the conclusion on page 24.
The conclusion asks about computing the smallest gap-closing penalty and about
extending polynomial penalty encoding beyond MIQP to quadratically constrained
problems. The relevant exactness is the value of the augmented dual after
maximizing over multipliers. The convex MINLP theorem permits infeasible
fixed-integer slices; only feasible slices require the stated Slater property.

Accordingly, the candidates answer the two questions in the manuscript's
mixed-integer setting. The QCQP construction does not answer a different
question restricted to purely continuous convex QCQPs or fixed total dimension.
The finite-penalty existence theorem is not contradicted. Existence,
polynomial-size encoding, finding some sufficient value, and finding a nearly
smallest value are four distinct claims.

[Gu, Ahmed and Dey, Theorem 11](https://arxiv.org/html/1907.00920v1#S2)
provides the strongest direct encoding comparison: a rational positive
semidefinite quadratic objective over a rational mixed-integer polyhedron has
an exact norm penalty of polynomial binary encoding size. The statement covers
both optimized multipliers and a specified multiplier with its encoding included.
Its constraints are linear. [Bhardwaj, Narayanan and Pathapati](https://arxiv.org/abs/2209.13326)
extend the objective class over linearly constrained mixed-integer sets; their
title alone should not be read as covering arbitrary convex quadratic native
constraints. The independent literature review records the fuller theorem-level
comparison. I directly inspected the Gu theorem and model, and verified the
Bhardwaj source version and abstract, rather than independently rechecking its
complete proof.

## 2. Encoding obstruction: proof and assumption attack

I independently reduced the first construction to its two residual intervals.
For `delta=2^(-2^n)`, its native projection is

`q=0: y in [-1,1]`; `q=1: y in [delta,1]`, with objective `-q`.

The zero residual is feasible only in the first branch. A norm penalty exact
at some multiplier must satisfy, from the two points `y=-1,q=0` and
`y=delta,q=1`,

`rho-lambda >= 0`, and `(rho+lambda) delta >= 1`.

They imply `rho>=1/(2 delta)`. The displayed multiplier in the candidate
equalizes these two affine values and gives the claimed full dual envelope.
The proof therefore controls the supremum over every real multiplier, rather
than only the zero multiplier. There is no hidden multiplier-attainment issue.

The chain constraints are convex quadratics with coefficients from a fixed
finite set. The point `a_i=3/8,y=0,q=0` satisfies the original equality and
all continuous inequalities with slack at least `1/8`. The native `q=1`
slice also has a uniform strict point, while its equality-constrained slice
is empty. These checks match the source assumption. A feasible-slice Slater
condition cannot supply the missing separation of an infeasible slice.

The precise growth statement is `2^n` ordinary numerator bits for a sufficient
rational penalty, against sparse input size `O(n log n)`. It is
superpolynomial in input length and exponential in the chain length. Calling it
an exponential lower bound in the full input length without specifying the
encoding would overstate the displayed calculation. A power expression or an
arithmetic circuit is a different output model. Fixing the scalar norm also
matters: absorbing a huge scale into the norm does not avoid its encoding cost.

At the threshold, infeasible augmented minimizers tie with the true optimum.
Strictly larger penalties recover solution-set exactness, with the appropriate
multiplier, and preserve the encoding obstruction. The fixed additive-gap
formula is sound and useful: the phenomenon is not restricted to exact equality
of two symbolic values. Nevertheless the primal problem itself is easy. This
is a limitation of the prescribed relaxation and its numerical representation,
not a hardness theorem for solving the displayed optimization problems.

The important novelty limit is explicit. [Bienstock, Del Pia and Hildebrand,
Section 6](https://arxiv.org/html/2011.08347v5#S6) already discuss convex squaring
chains, large encodings, and bounded quadratic examples where minute
infeasibility causes constant superoptimality. [Beck et al.](https://optimization-online.org/wp-content/uploads/2022/02/nearly-feasible-bilevel-preprint.pdf)
give an especially close bounded convex-chain/Slater comparison in bilevel
optimization. The new mathematical step is placing that established mechanism
inside a mixed-integer augmented dual and preventing the free multiplier from
absorbing it. That step is short but necessary. It supports a crisp application
of an old precision mechanism, not invention of the mechanism.

## 3. Minimum-penalty hardness: correct stronger restrictions

For the binary-box construction, I independently checked that divisibility
forces the sole primal feasible point to be zero. The two nearest
objective-improving residuals are `-d_minus` and `d_plus`, both with objective
`-1`. Their balanced mixture gives the upper bound, while

`lambda=rho (d_minus-d_plus)/(d_minus+d_plus)`

makes every more distant point no better. Thus

`rho_star=(1/d_minus+1/d_plus)/2`

and the complete dual formula are correct. Appending `B+1` ensures the nearest
upper subset sum while preserving the original target decision. The `K=4`
construction has the asserted exact gap `D_(1/3)=-1/2` or zero. Exactness
recognition is coNP-complete on the specified family; computation of the
threshold is NP-hard. These directions of the reductions are correctly stated.

The approximation argument also survives scrutiny. With source length `ell`
and `K=2^ell`, the constructed length is polynomial in `ell`. YES thresholds
exceed `1/2`, whereas NO thresholds are `O(2^-ell)`. Any algorithm returning a
guaranteed sufficient penalty within a fixed polynomial factor of the optimum
would distinguish them. Positive thresholds in both cases avoid an artificial
zero-versus-positive approximation obstruction. This is a meaningful bit-model
result, but not strong hardness for binary boxes. Rescaling the equality
preserves the relative gap and moves, rather than removes, the fine arithmetic
spacing.

The unit-data graph construction is also correct, but its native optimization
already contains maximum stable set. It is a useful short supporting result.
Its significance is lower than the box construction, which isolates the
difficulty introduced by the residual penalty despite easy native *linear*
optimization. Easy native linear optimization does not mean that the augmented
absolute-residual subproblem is easy.

## 4. Prior penalty hardness is a material collision

[Alessandroni et al., version 4 dated 30 July 2025](https://arxiv.org/html/2307.10379v4#S4.SS1),
Observation 1 and Lemma 1, already prove hardness of finding an optimal QUBO
penalty and recognizing a supplied exact penalty. Their construction also has
a trivial constrained optimizer. Hence neither generic penalty-calibration
hardness nor hardness despite a known primal solution is a new claim here.

Their formulation uses a squared residual penalty with no optimized linear
multiplier and an explicit positive separation gap. Their particular reduction
cannot simply establish the present augmented-dual result: the residual
`x=0` has one sign in every binary coordinate, so free multipliers can enforce
it on a finite set without any norm penalty. The present opposite-residual
argument addresses that real difference. Generic symmetrization would already
make a broad optimized-dual hardness result plausible; the native binary box,
single scalar equality, single linear objective term, and polynomial-factor
inapproximability are the more informative additions.

I found no equivalent theorem with that complete combination in the sources
inspected. This is a qualified comparison, not a priority certificate. The
main note should lead with the restricted approximation obstruction and cite
the prior QUBO hardness prominently. A claim to the first proof that optimal
exact penalties are hard would be incorrect.

## 5. One consequential positive question, and a stopping rule for this lane

The most concrete positive question suggested by both results is:

> For compact convex integer slices with a bounded objective range, can
> polynomial-bit random perturbations of several linking right-hand sides
> yield a polynomial-bit computable sufficient norm penalty with high
> probability, without enumerating the integer slices, together with a
> certificate specifying when the perturbed solution or bound remains useful
> for the original problem?

This directly asks when the problematic infeasible-slice separation becomes
controllable. The scalar starting point is elementary: each convex slice
projects to an interval; being distance `d` from all endpoints controls both
infeasible-slice distance and feasible value-function slopes by objective
range divided by `d`. A union bound over at most `2^(k+1)` endpoints suggests
polynomial-bit high-probability penalties under scalar noise, even with `k`
binary variables. That scalar observation alone is unlikely to be substantial.
Several-row geometry, finite random grids, lower-dimensional images, and
useful certification are the actual next obligations. Classical smoothed
condition-number and convex error-bound literature must be checked before
claiming novelty.

There is a decisive application caveat. In the one-binary example, perturbing
`y=0` to `y=b` with `b>=delta` makes the better integer branch feasible and
changes the optimum from zero to minus one. A noise scale much larger than
`delta` can therefore remove the large penalty by changing the discrete
problem. Arbitrarily small perturbation does not guarantee a small objective
change. A theorem merely about the perturbed instance must say so. Conditioning
on feasibility also needs a quantitative argument; it is not free.

**Research allocation:** preserve and finish this focused negative milestone.
Allow a bounded investigation of the positive question now assigned to the
parametric research agent, but do not continue accumulating penalty variants
if it only yields the scalar union bound or a sufficient condition that assumes
the desired separation. The compact star-hull and other geometric tracks
already running have greater prospective impact. Returning to them would be
the right choice if the positive penalty work lacks a new mechanism or a
credible way to provide useful certificates.

## Review evidence

I read both current candidate notes, the supporting penalty geometry, the
retained dated Lefebvre–Schmidt text, the previous literature review, Gu's
primary model and Theorem 11, Alessandroni's full hardness reduction, and the
named precision examples. I reconstructed the key projected dual envelopes,
threshold inequalities, reduction directions, and input-size amplification
independently. I did not repeat the existing finite arithmetic campaigns;
their results establish their tested cases, not novelty or general hardness.
No solver tests, project-wide verification, or CI inspection were performed.
The document's local links and whitespace receive a separate targeted check.
