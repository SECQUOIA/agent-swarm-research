# Independent audit of the original-instance envelope certificate pipeline

Date: 2026-09-06. Reviewer: `review_pipeline`. Verdict: **PASS for mathematical soundness and the implemented scope.** No implementation defect requiring a correction was found. This is an integration and verification result; the audit does not establish literature novelty or large-network performance.

Reviewed files: [`certified_envelope.py`](../code/potential_flow_mpd/certified_envelope.py), its benchmark and saved instances, the [pipeline note](potential-flow-certified-envelope-pipeline.md), and the existing envelope, finite-secant, rational-energy, and Bregman results and implementations. The independent executable audit is [`check_certified_envelope_review.py`](../code/potential_flow_mpd/check_certified_envelope_review.py).

## Why the certificate proves the stated original-instance claim

The input schema supplies only the graph, fixed balanced rational nominations, independent positive resistance intervals or explicitly listed finite sets, a target index, and the extremum direction. For a finite set, its minimum and maximum are actual allowed members, including when the list is unsorted or has repeated/interior values. Endpoint recovery therefore returns an allowed original scenario. Rejecting unknown instance fields avoids accepting a document with additional physical constraints while silently proving a different problem.

The graph checker validates simplicity, absence of loops, vertex types and ranges, and connectivity. Its degree-at-most-two elimination with neighbor fill correctly recognizes the implemented class. Each fill when the neighbors were not already adjacent is a minor operation: contract an edge incident to the degree-two vertex. Thus elimination preserves absence of a `K4` minor. A nonempty partial 2-tree has a vertex of degree at most two; conversely a successful elimination gives a width-two elimination ordering. Reversing that ordering contains the original graph in a partial 2-tree. This uses the classical equivalence of partial 2-trees and `K4`-minor-free graphs; no novelty is asserted for recognition.

The grounded all-unit Laplacian is nonsingular because the graph is connected. With the code's incidence convention (tail `+1`, head `-1`), its right-hand side is exactly the unit injection at the target tail and withdrawal at its head. Rational potential differences therefore give the exact adjacent-terminal adjoint signs. These signs are valid for arbitrary positive secant resistances by the reviewed graph-sign theorem. For target maximization the target receives the pointwise minimum law; other positive-sign edges receive the maximum law and negative-sign edges the minimum law. The code reverses these choices for minimization, and its asymmetric positive/negative coefficients match the actual pointwise orders for `beta*x*abs(x)`. Off-block zero-sign edges receive an arbitrary fixed allowed endpoint.

The finite secant identity is

```
r_a (y_a-x_a) = sum_{e != a} j_e d_e - (1-j_a)d_a.
```

For maximization every right-hand term is nonnegative. The target's special reversed rule is essential and is implemented correctly. Positive secants exist even when a physical current or derivative vanishes, so exact zero flows cause no gap in this proof. A bridge has `j_a=1` and all other adjoint currents zero, consistent with its conservation-determined flow. The envelope state attains the original optimum by independently selecting an agreeing endpoint law on every edge.

The pipeline first verifies the base energy certificate and only then calls Bregman sharpening. The exact base check establishes a conserved rational flow, an upper enclosure for every conjugate square root, the resulting nonnegative primal-dual gap, and the cubic error radius. Reverse Bregman divergence gives a per-edge enclosure of the unique physical flow. Each scalar term is nonnegative and its sum is the actual primal gap; keeping the outside endpoint at every bisection is correct. The fixed 48 bisections affect tightness, not validity.

The scenario's second certificate is checked under the actual selected *symmetric* endpoint coefficients. Its flow need only satisfy exact conservation; it need not be a separately optimized numerical state. Hence reuse of the envelope approximation cannot make the proof invalid. With the two physical target intervals, interval subtraction yields the stated nonnegative upper bound on maximization or minimization loss.

For the stronger zero-loss claim, the compatibility condition is sufficient edge by edge. Equal envelope coefficients need no sign information. Otherwise a certified weak sign and matching coefficient establish law equality at the true envelope flow. A singleton zero interval permits either endpoint. Law equality on every edge transfers the entire envelope physical state to the recovered original scenario, and uniqueness proves exact endpoint-scenario optimality. This certifies an exact scenario, not an exact rational value of its possibly irrational physical objective. Conversely, failure to certify signs does not prove a scenario suboptimal; the implementation correctly reports a safe potentially positive loss bound instead.

## Trust boundary and malformed inputs

The imported deterministic checker does not itself enforce the full original-instance graph class or schema. In particular its vertex test uses `isinstance(u, int)`, which alone admits Python Booleans. The pipeline's earlier `type(u) is int` check closes that boundary, and the strict top-level format similarly rejects Boolean targets and versions. The input parser rejects duplicate JSON keys. Rational fields must be strings, and malformed values, nonpositive resistances, dimension mismatches, nonconservation, and invalid certificate inequalities are rejected.

The imported producer contains some `assert` statements, but certificate acceptance uses unconditional `require` checks. The verification path imports no NumPy, NetworkX, CVXPY, or solver package and remains valid under `python -S -O`. The standalone older deterministic `verify_file` function has a looser JSON parser; the pipeline does not use it. These are distinct interfaces and should not be described as having identical input validation.

The numerical producer's exact normalization is correct. If normalized coefficients and nominations are `c/C` and `b/B`, the certificate scales by `B` for flows/radii, `CB^2` for potentials, and `CB^3` for conjugate roots and gaps. In particular, the square-root conjugate expression scales by `CB^3`, not `CB^2`. All inequalities survive exact lifting. Normalizing before rational certificate construction avoids absolute dyadic precision loss at tiny supplies. Relative coefficient conditioning can still cause numerical failure; the program does not promise a requested output width.

## Integrated conservation-aware target witness

The later optional `goal_bounds` integration also passes focused review. The verifier reconstructs the target coordinate vector internally; the document cannot supply another goal while claiming the target's bound. Envelope and scenario witnesses are verified against their respective coefficients and base certificates. The nested schema is exact, every interval is checked, and the goal interval is centered on the corresponding conserved approximate target flow. Intersection with the prior Bregman interval requires a nonempty result. A non-null invalid witness is rejected rather than ignored; absence or an explicit null individual witness retains the original valid bound.

The imported Hessian argument uses the minimum scalar curvature on each verified interval. It bounds `sum h_e d_e^2` by twice the certified energy gap. Subtracting any potential-gradient functional from the goal preserves its value on the circulation error. Weighted Cauchy–Schwarz then proves the reported radius provided the residual vanishes on every zero-curvature edge. The verifier checks precisely those zero residuals and the factor/radius identities. Zero gap is separately exact. This focused audit agrees with the mathematical mechanism; the goal-certificate result also has its own independent review.

The producer constructs the goal witness in normalized units and lifts its intervals/radius by `B`, its potential witness unchanged, and its factor by `1/(CB)`. This follows from `h_original=CB*h_normalized`; multiplying the original energy gap and lifted factor scales their product by `B^2`. Thus the normalization also preserves the integrated final interval exactly across common supply/resistance units. The optional producer checks below were rerun after this integration and scaling change.

## Independent observable-behavior checks

The independent script uses only the standard library unless `--producer` is supplied. It constructs certificates directly from rational physical potentials or a zero dual potential; it does not call the author's certificate producer or reuse the author's numerical physical solver.

- All **771 connected labelled simple graphs on 2–5 vertices** are checked against an independent enumeration of four disjoint connected branch sets with every pair adjacent. This is the defining `K4` minor model, not another elimination algorithm. The checker agrees in every case, including **107 rejected graphs**. A separately constructed graph obtained by subdividing every edge of `K4` is also rejected.
- **24 exact rational physical fixtures** exercise maxima and minima, both potential polarities, mixed edge orientations, a target inside `K_{2,3}`, a target bridge, an attached cyclic block with exactly zero adjoint current, nonzero and zero physical flows, zero nominations, finite sets with interior/repeated/unsorted values, and supply scale `10^-70`. Their zero-gap certificates return exact singleton target intervals and exactly optimal allowed endpoint scenarios, including arbitrary endpoint choices on zero-flow edges.
- **Four independent closed-form triangle checks** exercise both objective directions and both nomination signs with intentionally loose certificates. The target flow formula follows by equating drops on a direct edge and its alternative two-edge path. Enumerating the eight endpoint scenarios gives an independent optimum reference. The verifier encloses both that optimum and a selected scenario and safely bounds their loss while declining to certify unresolved signs.
- **33 malformed JSON cases** are each rejected through the command-line entry point under `-S` and `-S -O`, for **66 rejection checks**. Controls include unsupported constraints, malformed schemas, duplicate keys, Booleans, nonstring and invalid rational data, inadmissible interior scenario resistance, loops, repeated edges, bad vertex ranges, invalid directions, nonconservation, and corrupt primal-dual data. A valid certificate is accepted in both modes. The audit script itself also uses unconditional checks.
- A further manually constructed **positive-gap bridge fixture with zero curvature on every edge** supplies a cut-potential goal witness. The integrated envelope and scenario intervals both become the exact conservation-determined singleton, despite loose base intervals. **Eleven malformed goal-witness cases** are rejected in both command-line modes, adding **22 rejections**; controls include an injected goal vector, wrong zero-curvature residuals on either state, bad interval data, invalid factors/radii, and unsupported nested fields. No author's goal-witness producer is used for this fixture.

Reproduce the standard-library audit with:

```sh
python -S code/potential_flow_mpd/check_certified_envelope_review.py
python -S -O code/potential_flow_mpd/check_certified_envelope_review.py
```

The optional producer audit additionally passed **six triangle solves**, in both directions at unit scales and at reciprocal supply/resistance scales `10^400` and `10^-400`. It compares the normalized *rational* final returned intervals for exact equality across units, including the integrated target improvement, independently checks the closed-form optimum, and re-verifies every emitted certificate. Run:

```sh
/home/sgusev/miniconda3/envs/minlp-notes/bin/python code/potential_flow_mpd/check_certified_envelope_review.py --producer
```

## Publication implications

The pipeline closes the earlier certificate-format gap: verification now starts from original uncertainty data and validates the envelope mapping and recovered original scenario. The bounded benchmark, including an explicitly synthetic quadratic model on a sourced water-network topology, supports a reproducible computational demonstration. It does not establish calibrated hydraulic prediction, performance on general infrastructure networks, requested-accuracy termination, or novelty of the classical envelope identity. A paper should state those boundaries and distinguish a verified endpoint scenario from a certified numerical objective interval.
