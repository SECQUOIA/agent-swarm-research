# Independent review: rational certificates for envelope flow solves

Date: 2026-09-05. Reviewer: `benders_review`.

**Verdict: the support lemma and corrected exact verifier pass this
independent audit.** I reviewed
[the note](potential-flow-envelope-rational-certificates.md),
[the implementation](../code/potential_flow_mpd/envelope_rational_certificates.py),
and the saved example. This certifies a deterministic rational energy
instance. Its interpretation as an original uncertainty extremum still
requires the separately proved and correctly instantiated envelope mapping.

## Mathematical certificate

For positive and negative cubic coefficients, optimizing
`d*x-c*|x|^3/3` on each half-line selects the sign of `d` and gives
the conjugate `(2/3)*sqrt(|d|^3/c_sign(d))`. This includes `d=0`,
where the choice of coefficient is irrelevant. With the incidence
orientation used by the code, `d_e=p_u-p_v`, and exact conservation
gives `sum_e d_e y_e=b^T p`. The Fenchel lower bound consequently
has the displayed sign and factor. Replacing each conjugate root by
an upward rational bound decreases the dual value and preserves a
valid lower bound on the optimum.

An exactly conserved primal candidate proves that the affine feasible
set is nonempty. Positive coefficients make the energy coercive and
strictly convex, so its minimizer exists and its flow is unique.
No constitutive feasibility or stationarity is required of the candidate
flow or rational potential vector.

The energy-to-flow factor is valid for asymmetric coefficients as well.
Writing each edge gradient as `beta_L*x*|x|` plus a monotone remainder
gives the scalar modulus
`(g(a)-g(b))*(a-b)>=(beta_L/2)*|a-b|^3`. Integrating along a segment
gives an edge Bregman bound `(beta_L/6)*|a-b|^3`. At the constrained
minimizer the linear gradient term vanishes on every conserved flow
difference. Thus the primal energy gap is at least
`(beta_L/6)*sum_e |y_e-x*_e|^3`, which implies the stated infinity-norm
bound. The computed dual gap is an upper bound on that primal gap;
a rational radius satisfying the cubic inequality is therefore valid.

The asymmetric quadratic law is increasing on the entire real line.
Evaluating it at the two rational flow-interval endpoints gives a valid
pressure-drop interval, even when the interval crosses zero. This is
the deterministic envelope's pressure interval, not a claim about the
pressure of an independently selected original resistance scenario.

## Conditional recovery of an original scenario

The separate endpoint-recovery theorem applies if the supplied asymmetric
coefficients really are the correct maximizing or minimizing envelope
for the original graph, target, nomination, and resistance intervals.
When signs of `y` and `x*` disagree, the affected true flow has magnitude
at most the certified radius `eta`. The selected original law's residual
at `x*` is therefore at most `beta_U*eta^2` on each edge. Monotonicity
and conservation give the reviewed flow-distance estimate
`sqrt(2m*beta_U/beta_L)*eta`, safely bounded by the stated rational
factor `(1+2m*beta_U/beta_L)*eta`. A zero approximate flow can use
either endpoint; the same residual bound covers the tie.

The JSON contains only deterministic edges, nominations, asymmetric
coefficients, and primal/dual certificate data. It does not contain or
verify the original resistance intervals, target, extremum direction,
series-parallel condition, or electrical sign calculation. Nor does
verifying a self-contained JSON authenticate it against an external
problem instance. The updated note explicitly states this boundary.
The JSON result by itself certifies the deterministic flow radius;
original-scenario and extremum conclusions remain conditional on the
independent model mapping.

## Exact implementation and corrected issues

The square-root routine first computes the integer floor root after
scaling, then increments exactly when the original rational inequality
is not yet satisfied. Taking the integer root of the floored quotient
does not lose information about that integer floor root. The analogous
integer cube-root search has a valid power-of-two bracket and the same
final exact comparison. Both return the smallest requested dyadic upper
bound. Their integer bit lengths and operation counts are polynomial
in the rational data and requested precision.

The conservation-rounding helper chooses chord values first and solves
tree flows by leaf elimination. Its orientation-dependent leaf flow and
parent residual update have the correct signs. I identified that its
original `networkx.Graph`/unordered-edge index implementation could not
silently cover parallel edges. The author added explicit simple,
loopless, connected-graph checks, matching the producer's intended
scope. Its final balance check is now unconditional as well. The exact
verifier itself remains mathematically valid for parallel edges.

Root review identified that the first verifier used Python assertions,
which disappear under `python -O`. The corrected verifier uses explicit
checks raising `ValueError` for every acceptance condition. It checks
all vector lengths, positive rational coefficients, rational primal,
dual, root, gap and radius values, valid edge indices, exact conservation,
upward conjugate roots, the exact gap identity and nonnegativity, and
the cubic radius inequality. Nonrational float gaps or radii are rejected
by its direct API. Numerical scientific packages are imported only by
the producer; the standalone file verifier uses the standard library.

The producer still uses ordinary numerical solves to propose candidates.
This is acceptable because successful certificate production ends in
the unconditional exact verifier. Solver status is neither an acceptance
condition nor evidence for the final radius. Internal demonstration
assertions are distinct from the verifier's mathematical checks.

## Independent validation

I wrote an independent
[standard-library checker](../code/potential_flow_mpd/check_envelope_certificate_review.py).
It passed:

- Five exact known-state cases, including positive, negative and zero
  flow, a parallel-edge graph, and a conserved perturbation with a known
  exact minimizer. Exact physical candidates have zero certified gap
  and radius; the perturbed candidate's interval contains the exact
  flow and pressure.
- 800 exact root-enclosure minimality checks, for square and cube roots
  at four dyadic precisions.
- Acceptance of the saved valid JSON under both normal and optimized
  Python; rejection of 16 independently corrupted file cases covering
  flow, nomination, coefficient, root, gap, radius, edge-index and
  dimension errors in both modes.
- Direct rejection of float-valued gap and radius fields.

I also reran the six numerical producer cases. All exact certificates
and its 24 corruption controls passed, together with optimized-mode
and unsupported-rounding-graph regressions. The largest reported
certified flow radius was `0.000178`, envelope pressure interval width
`0.000477`, and conditional endpoint-scenario loss bound `0.0173`.
The largest separately observed numerical flow error was `3.84e-7`.
The latter is an empirical comparison; it is not the certified radius.
The certificate bounds are deliberately more conservative.

This support work certifies achieved accuracy of a proposed numerical
candidate. It does not prove that the numerical solver attains a chosen
accuracy in polynomial time, implement the separate ellipsoid algorithm,
or establish new convex-duality theory. No outstanding correctness
issue remains within the stated deterministic-verifier scope.
