# Stage 3, round 1 — independent reviewer 3

## Verdict

**PASS subject to one minor wording correction. No major issue found.** The structural theorem, universality and designated-coordinate degree claims, residual estimates, tiny-infeasible family, general separation scale, promise certificates, and reactive stability have complete arguments under their stated assumptions.

Reviewed frozen snapshot: `process/snapshots/stage03-round01`, including all three new sections, updated abstract/bibliography, new checker, and accepted dependencies. I did not read other stage-3 reviews or edit manuscript sources.

## Required minor correction

**The description of the neighbors of D in the reverse residual estimate is inaccurate.** At `sections/06-numerical.tex:66–67`, “including its two weighted x copies and one y copy” suggests that D has two x-copy neighbors. It has one complemented x-copy neighbor with conductance 2, one complemented y-copy neighbor with conductance 1, and W. The other x-copy belongs to C_I. Replace this with “including the x-copy error weighted by 2 and the y-copy error weighted by 1”, or explicitly name the two complemented neighbors and their conductances. The displayed error bound `epsilon+3 delta` is correct; no constant or proof change is required.

## Structural construction

- The crossover equations force both wire equalities and uniquely determine the sum. All crossing sums lie in `[1,4]` while all transmitted source values stay in `[1/2,2]`. Explicit interval preservation correctly avoids using the cited bounded-witness promise as if it were a full solution-set statement.
- Replacing occurrence edges, including repeated occurrences, by separate wire corridors gives polynomially many crossings and local planar replacements. The crossover drawing has the required alternating exterior terminal order. I visually inspected Figure 2 in the compiled PDF.
- With complement constant `C=9/2`, I independently obtain copy injection `2-C=-5/2`, addition injection `3-C=-3/2`, and inversion linear-bus injection `5-3C=-17/2`. The inversion remains valid because `xy=1` and both variables at least `1/2` force both to be at most 2. The wider bound on I therefore creates no extra exact solution or lost valid solution through W.
- The variable paths can follow the incidence rotation order with a single break, while each requested bus has one external edge. Doubling the inversion x corridor preserves adjacency of the two strands; the three-leaf inversion tree admits either cyclic order. Repeated names are not identified physically. These observations justify simultaneous planarity, graph simplicity, degree three, and the original coordinate projection.
- A root remains a path endpoint with degree at most two and free injection. The connector path adds only fixed-voltage buses and changes old free injections within the same uniform bound. Choosing the outer face separately in each connected component makes the joining operation planar. The no-variable case is correctly handled by a singleton graph with its allowed zero injection.
- For subdivision, positive internal voltages turn zero powers into the linear second-difference equation. Its unique solution is affine interpolation. Endpoint powers scale by `1/(4L)` for both original conductances, so scaling the complete old injection intervals is correct, including pinned and free buses. Even path lengths give a bipartition. Every new simple cycle corresponds to an old simple cycle and has at least `6L` edges. The finite alphabet depends only on fixed L and hence fixed r.
- All these operations preserve entire solution sets, not merely feasibility. Applying the AC transfers only after electrical subdivision preserves the claimed simultaneous graph restrictions. The principal window uses the final number of buses, as required.

## Algebraic and primary-source audit

I verified the crossover attribution and source's bounded-witness qualification against [Dobbins et al., Theorem 2.1 and its proof](https://link.springer.com/article/10.1007/s00454-022-00381-0). The manuscript's explicit bounded construction is stronger than the source's promise in precisely the way its proof establishes.

I read Theorem 1, Definitions 4–5, and the bounded ETR-INV construction in the archived *Dynamic Toolbox for ETRINV*, including the original PDF for the linear-extension definition. It gives the rational equivalence and coordinate scaling/shifting used here. The source's auxiliary narrow intervals are accompanied by a promise that the formula's full solution set lies inside them, so taking the bounded `[1/2,2]` solution set does not discard an additional obligation.

For a singleton isolated algebraic root, rational equivalence gives a singleton arithmetic solution with every coordinate in `Q(alpha)`. The separate affine recovery property gives a designated coordinate generating exactly `Q(alpha)`; this does not follow merely from the field generated jointly by all coordinates. All electrical operations retain that coordinate. The rational case and Eisenstein degree-d examples are handled correctly. The manuscript avoids asserting a polynomial size bound for algebraic descriptions or deriving nonmembership in NP merely from irrationality.

## Residual and numerical claims

- The forward residual extension holds throughout the source box. Its only nonzero possible fixed-injection errors are the addition residual and the inversion linear-bus residual `|y-1/x| <= 2|xy-1|`.
- In the reverse estimate, every path extension contributes at most one injection-error unit to the propagated complement error; the global `6m epsilon` bound suffices. The I division is safe, and `|h'| <= 2` on `[1/2,2]` is correct. Including the coefficient 2 at D yields `10(epsilon+delta)` for inversion, which dominates addition. Empty instances are handled.
- The tiny-infeasible family has the claimed counts. Its recurrence follows from the actual addition/inversion equations, remains within all source intervals, and has strictly positive error at every step. The denominator recurrence and final electrical residual `1/(d_k+1)` are exact. All other physical injection constraints are satisfied by the canonical extension. Compactness supplies the strictly positive minimum independently of the exhibited upper bound. The connectedness argument includes k=0.
- The input-length and accuracy conclusions follow from linear graph size and doubly exponential denominator growth. The text correctly separates a limitation of universal residual thresholds from a lower bound on decision algorithms.
- For the general separation estimate, the epigraph cap `B_0=1+U^2D+A` is valid. The capped epigraph is nonempty, compact, and connected even when the voltage box has singleton coordinates, so it is a compact connected component to which the polynomial-minimum theorem applies. There are exactly `4n+2` inequalities in dimension `n+1>=2`. Positive denominator clearing has polynomial coefficient bit length. Substitution of d=2 in the source bound gives the displayed exponent and a base with logarithm at most `tau+q+4`.
- I verified that bound and all its conditions against [Jeronimo, Perrucci, and Tsigaridas, Theorem 1 in the archived/arXiv version](https://arxiv.org/pdf/1112.0544), page 2. The manuscript cites the journal numbering, Theorem 1.1; I verified the mathematical statement in the available preprint. For fixed data and bounded degree, H is constant and the remaining logarithmic factor is absorbed into `2^{O(n)}`. The tiny family has linearly many buses in k, establishing the matching exponential scale for logarithmic residual minima.
- Rational rounding followed by clamping moves coordinates by at most one mesh width while preserving exact bounds and singleton pins. The `4UD` Lipschitz bound is sufficient. The certificate argument is complete on its stated promise and does not claim an unpromised approximate decision result or a search algorithm.
- The reactive energy argument gives the stated angle norm and active discrepancy constants, including the factor `lambda_2^{-1}` rather than its square in the active estimate. The weaker sine bound gives rational constants 2 and 2. The path/Cauchy–Schwarz argument proves the displayed graph-only spectral lower bound. Substituting ell=1/2, U=4, g_min>=1 yields exactly `256 n(n-1)^2 eta^2`. Components and singleton buses are treated correctly.

## Verification artifacts

The supplied new exact suite passes: 49 generalized crossover profiles, 8 generalized inversions, component joining, three subdivision scales including original-power scaling, 360 perturbed original-network profiles, 11 tiny-residual instances, and 100 rational Poincare/Lipschitz checks.

I added an independent supplementary numerical check of reactive stability using the physical line reactive powers and active corrections on uniformly weighted paths, whose spectral gap has a closed form. It passes 180 profiles including zero angles, small angles, and the `pi/2` edge boundary. This smoke check uses an explicit floating-point tolerance; it supports the analytical check and is not an exact certificate. It lives in `verification/reviewer3/stage03-round01/check_reactive_stability.py` with saved output.

A separate LaTeX build succeeds in `verification/reviewer3/stage03-round01/build/`. The final log has no warnings or overfull/underfull reports. Figure 2 has the asserted crossing order and no hidden intersection. Source-definition and minimum-theorem PDF text extractions and the rendered page are retained in the same verification directory.

## Optional suggestions

No further mathematical development is needed to validate this stage. A citation could additionally identify JPT's arXiv theorem number for readers following the supplied URL; I do not treat the journal-number citation as an error.
