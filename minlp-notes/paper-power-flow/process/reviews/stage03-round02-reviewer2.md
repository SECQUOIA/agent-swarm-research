# Stage 3, round 2 — independent reviewer 2

**Verdict: mathematical PASS; one minor scope correction required. No major issue identified in the repaired draft.**

I reviewed the frozen round-2 inputs and correction report independently. I did not read other round-2 reports or edit manuscript inputs. My round-1 review incorrectly trusted the printed general rational-universality statement in the toolbox source. In this round I checked the replacement construction itself, both directions of every gate, the basic-closedness invariant, and the obstruction. The repair removes that dependence rather than merely narrowing a citation.

## Required minor correction

**Retain the coefficient-field restriction in the abstract and README.**

- `main.tex:35–36`: change “rational equivalence holds precisely for compact basic closed sets” to “rational equivalence holds precisely for compact basic closed sets defined over `Q`”.
- `README.md:7–8`: make the same qualification in “rational universality precisely for compact basic closed sets”.

The theorem itself has the correct restriction, but these summaries currently omit it directly beside the unrestricted topological statement. A compact basic closed set with arbitrary real coefficients need not be rationally equivalent over `Q` to a rational network feasible set; a singleton at a transcendental real number illustrates the distinction. This is a local statement-of-scope correction, not a flaw in the theorem or proof.

## Repaired arithmetic construction

I checked Appendix A as a self-contained proof, without using the source's general Boolean or quantitative-range claims.

1. **Polynomial evaluation.** Integer polynomial circuits with globally defined negation/zero/constants have a unique extension on a basic closed input set. Output equalities and nonnegativity impose exactly its conjunctive description. The circuit graph over a compact set is compact, supplying one finite bound for every coordinate. There are no inactive branches or sign-choice slack variables.
2. **Scaling.** Once `d=delta` and the halving chain fix nonzero `epsilon`, the replacement equations force `w_x=epsilon*x`; a multiplication's shared auxiliary obeys `q=epsilon^2*z`. All scaled variables are bounded by `delta` on solutions after choosing `epsilon M <= delta` and `delta <= 1`. Conversely, division by the fixed nonzero scale recovers all original circuit equations and inequalities. The argument uses existence of a finite halving chain and correctly makes no polynomial-size claim for arbitrary input descriptions.
3. **Shifted coordinates.** The two additions force `C_s=s+3/2`, `B_s=s+3/4`. The shifted addition and product rules eliminate to exactly `s+t=u` and `st=u`; the latter's remaining multiplication has inputs near one. The nonnegative auxiliary is `J_s=1/2+s`, so its lower bound enforces the intended sign. Its upper bound removes no source solution after scaling. The midpoint chain and `A_d+Delta=2` fix the dyadic constant uniquely using only allowed equations.
4. **Product from squares.** Direct substitution gives `r=(a+b)/2`, `d=(a^2+b^2+1)/4`, and final output `ab`. All fresh intermediate values are uniquely determined in the displayed order. At inputs `(1,1)` their values are strictly inside the common interval.
5. **Square from reciprocals.** The central denominator identity simplifies exactly to `h=1/(a(a+1/2))`, and the final output to `a^2`. Every reciprocal equation forces its value uniquely because the relevant operands in a bounded final solution are positive. Thus the reverse argument works for *every* bounded final solution, not only the near-one profiles used to prove existence. The stated center-value list and nonzero denominator claim are correct.
6. **Ranges and composition.** The fixed gate types have continuous rational coordinate functions with strictly interior center values. A common neighborhood therefore works for every occurrence, independent of circuit size. The actual multiplication inputs are the separately retained shifted small variables, so range errors do not accumulate through repeated gate composition. I also gave an independent exact interval certification at the explicit choice `delta=2^-16`; it verifies all 67 tracked coordinates of the composed shifted-product/square/reciprocal construction remain strictly within `(1/2,2)`. The sign auxiliary is treated separately at its allowed boundary.
7. **Uniqueness and recovery.** Fixed constants, every circuit coordinate, and every replacement auxiliary are forced. Recovery of original coordinate `t_i` is exactly `(A_{w_ti}-1)/epsilon`, giving the designated affine coordinate promised in the lemma. All rational denominators stay nonzero on the source set, so both maps are continuous. Empty sets can be represented by the stated inconsistent bounded equation.

The appendix's source counterexample accurately follows the printed Boolean substitutions: an inactive branch leaves a nonnegative auxiliary free. Adding bounds on original variables does not constrain that free coordinate. The source statement therefore cannot support the old general rational-equivalence claim, and this appendix does not rely on it.

## Basic closedness, topology, and fields

- **`prop:basic-invariance`.** Every forward denominator and every numerator obtained from a composed inverse denominator is nonzero on compact `S`, so a common positive rational lower bound exists. Their squared lower bounds give weak polynomial constraints. On that domain, membership in `T` and the inverse identity can be cleared by positive even denominator powers. Every resulting point maps into `T` and returns to itself under `G`, hence belongs to `S`. Both inclusions are valid. The proposition does not assume the conclusion or confuse projection with rational inversion.
- **Three-quadrant obstruction.** Each lowest nonzero homogeneous part is nonnegative on the included open quadrants. Odd degree is impossible because two included quadrants are antipodal; even degree transfers nonnegativity to the omitted quadrant. A generic direction there avoids the finitely many zero sets, so all active defining polynomials become strictly positive on a short ray. Constant-positive and identically zero constraints cause no exception. This contradicts local exclusion. The proof covers equalities by replacing them with paired inequalities. It establishes the needed failure of local basic closedness directly.
- **`thm:universality`.** The self-contained bounded arithmetic lemma proves sufficiency for compact basic closed sets over `Q`; the invariant proves necessity. Both compose with the structural network construction. The rational-equivalence statement is now sharp in its stated domain.
- **`thm:topological-universality`.** Finite semialgebraic triangulation applies to compact semialgebraic sets with arbitrary real coefficients. The standard-simplex realization is compact basic closed over `Q`: support is a face if and only if every nonface monomial vanishes. Its barycentric map to a geometric realization is globally bijective because simplices meet in common faces, and is piecewise affine. Composing with the triangulation and rational network construction gives precisely a semialgebraic homeomorphism. No rational-map or size bound is incorrectly inferred.
- **`thm:algebraic-degree`.** The isolated algebraic singleton is compact basic closed over `Q`. The new lemma therefore supplies the required unique point and designated affine recovery without using the false general theorem. Forward rationality puts all coordinates in `Q(alpha)`; nonzero affine recovery gives `Q(x_j)=Q(alpha)`. The retained root, unique electrical auxiliaries, connectivity, and subdivisions preserve this. The rational case, all-degree Eisenstein example, and AC magnitude/reference-fixed conclusions remain sound.

I independently checked the newly cited primary triangulation source: [Ohmoto–Shiota, arXiv:1505.03970v2](https://arxiv.org/html/1505.03970v2), Theorem 1.1 and Section 1.2. It defines a semialgebraic triangulation by a homeomorphism and explicitly notes finiteness for compact sets. These are exactly the facts used here; no smoothness property is needed.

## Remaining stage-3 results

The structural section is unchanged from round 1. I rechecked the bounded crossover, widened electrical constants, incidence-port ordering including repeated inversion inputs, free-injection connectors, and even harmonic subdivision. Their composition still preserves unique rational extension and the original designated coordinates, which is the dependency needed by the repaired section.

The numerical section changes only the accurate description of `D`'s *one* weight-two `x` copy and *one* weight-one `y` copy. Its residual coefficient is therefore still `3 delta`. I rechecked the residual inequalities, recurrence family, connectedness/counts, compact epigraph and JPT substitution, rational promise rounding, and reactive energy/spectral bounds. None depends on general semialgebraic rational universality. All remain valid, including the distinction between small residuals, promise certificates, and exact algorithmic complexity.

## Verification and build evidence

Under `verification/reviewer2/stage03-round02/`:

- `check_intervals.py`, `independent.log`: independent exact rational interval certification of the composed gate ranges, symbolic reciprocal/square/product identities, and direct inactive-branch counterexample. The gate interval certificate concerns a whole input box, not sampled profiles. It supplements the manuscript's continuity proof.
- `arithmetic.log`: the new frozen checker passes all 1,681 multiplication/reciprocal profiles, the full disk circuit (valid, outside, and inconsistent assignments), constant chains, and simplex-support cases.
- `developments.log`: all previously supplied exact structural/numerical regressions pass again.
- `build.log`, `build/main.pdf`: successful independent 24-page LaTeX build. The final log has no unresolved-reference/citation or overfull/underfull warnings.

All eighteen frozen manifest hashes were verified before and after review. No additional major or minor issue was found. Correct the coefficient-field qualification before closing this stage.
