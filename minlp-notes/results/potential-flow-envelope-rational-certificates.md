# Rational certificates for numerical envelope solves

Date: 2026-09-05. Status: support lemma and exact checker passed an independent mathematical and implementation audit, including a separately written verifier and optimized-mode tests. This uses established convex duality; no new duality theorem is claimed. Its purpose is to certify the actual accuracy of numerical SOCP output independently of solver status or stopping rules.

Formal verification follow-up (2026-09-20): [Lean topic 03](../formal/topics/03-potential-flow/COVERAGE.md) proves deterministic energy-certificate soundness, existence and uniqueness of the physical flow, the uniform flow radius, and the saved example. [Topic 16](../formal/topics/16-potential-flow-certificates/COVERAGE.md) adds the Bregman, support and curvature refinements and exact rational root constructions. These proofs do not verify the Python implementation, the original uncertainty-to-envelope mapping, or the bit-complexity claims below.

Let the deterministic envelope energy be

```
E(x)=sum_e c_e^+ (x_e^+)^3/3+c_e^- (x_e^-)^3/3,
A x=b,
```

with at least one edge, positive rational coefficients and feasible rational nominations. Feasibility requires balance on every connected component; the conserved trial flow below supplies a witness. Let `beta_L` be the smallest coefficient. Its unique physical flow is `x*`.

## Rational primal and dual data

Take any rational exactly conserved flow `y` and any rational potential vector `p`. No optimality or constitutive feasibility is assumed for these candidate vectors. Write `d=A^T p`. The scalar conjugate of the edge energy is

```
E_e^*(d_e)=(2/3) sqrt(|d_e|^3/c_e^sign(d_e)).
```

Here the positive coefficient is used when `d_e>=0`, and the negative coefficient when `d_e<0`; the zero case is independent of that choice. This follows by maximizing `d x-c|x|^3/3` separately on its positive and negative half-lines. Fenchel's inequality and conservation imply the valid lower bound

```
E(x*) >= b^T p - sum_e E_e^*(d_e).
```

Compute rational upward enclosures `u_e>=sqrt(|d_e|^3/c_e^sign(d_e))`. Define the rational dual lower bound and gap

```
LB=b^T p-(2/3)sum_e u_e,
delta=E(y)-LB>=0.
```

Then `E(y)-E(x*)<=delta`. The reviewed energy modulus gives the certified flow bound

```
||y-x*||_infinity <= eta,
eta^3 >=6delta/beta_L,
```

where `eta` is any rational satisfying the displayed inequality. Thus `[y_a-eta,y_a+eta]` encloses the exact target-flow extremum represented by this envelope network.

Select allowed resistance endpoints by the signs of `y` and the envelope rule. The [reviewed endpoint-recovery argument](../results/potential-flow-series-parallel-envelope-optimization.md) certifies that the physical target flow of this original scenario is within

```
C0 eta,   C0=1+2m beta_U/beta_L,
```

of the exact envelope extremum. This is a certified upper bound on suboptimality, which may be much larger than the observed numerical error.

## Exact rational implementation

A numerical flow vector is converted to an exactly conserved rational flow by rounding chord flows to dyadics and solving the tree conservation equations by leaf elimination. The tree-edge correction and all conservation checks use exact fractions. Numerical potentials may be rounded independently to dyadics; every rational potential vector gives a valid dual lower bound.

For a nonnegative rational `r=a/b` and precision `p`, an upward dyadic square-root enclosure is `k/2^p`, where `k` is the smallest nonnegative integer satisfying `k^2 b>=a 2^(2p)`. Integer square root plus one final exact comparison computes it. The analogous integer cube-root search gives an upward dyadic enclosure of `(6delta/beta_L)^(1/3)`. These operations have polynomial bit complexity in the certificate data and requested root precision.

A certificate verifier needs only rational conservation, coefficient positivity, the upward-root inequalities, the primal and dual expressions, and the cube inequality. It does not need to trust CVXPY, Clarabel, or any floating-point solver. It also does not require an exact algebraic physical state.

This is an a posteriori guarantee. It does not assert that an arbitrary numerical solver will reach a requested tolerance in polynomial time. The separate reviewed ellipsoid theorem supplies that theoretical existence guarantee; this checker certifies the tolerance actually achieved by one numerical output.

## Certified pressure intervals

Because the envelope target law is increasing, the exact target pressure drop belongs to the rational interval

```
[g_a^envelope(y_a-eta), g_a^envelope(y_a+eta)].
```

These endpoint evaluations use rational asymmetric quadratic arithmetic. They certify the envelope physical state's pressure drop, and should not be confused with the actual pressure under a selected original resistance scenario. The flow bound and endpoint-scenario suboptimality bound above remain separate guarantees.

## Checker and achieved tolerances

[`envelope_rational_certificates.py`](../code/potential_flow_mpd/envelope_rational_certificates.py) separates a numerical certificate producer from an exact verifier. The latter imports no scientific or optimization package. It checks conservation, coefficient positivity, every conjugate square-root enclosure, the claimed energy gap, and the cubic flow-radius inequality with exact rational arithmetic. A saved [example certificate](../code/potential_flow_mpd/envelope_certificate_example.json) can be checked with the system Python alone:

```
python code/potential_flow_mpd/envelope_rational_certificates.py --verify code/potential_flow_mpd/envelope_certificate_example.json
```

The numerical producer solved six envelopes on block ranks 2, 4, and 7 and produced valid rational certificates. Across these runs, the certified flow radius was less than `1.8e-4`, the certified envelope target-pressure interval width less than `4.8e-4`, and the certified original endpoint-scenario loss less than `1.8e-2`. The largest independently observed physical flow error was below `3.9e-7`. These quantities have different meanings: the certificates are rigorous upper bounds, while the observed errors are floating-point comparisons to separately solved physical equations. The cubic energy conversion and endpoint-recovery factor are conservative here.

The verifier rejected 24 deliberately corrupted certificates: violations of conservation, invalid upward root bounds, altered energy gaps, and undersized flow radii. The saved example's exact certified radius is

```
102885025499522195717 / 604462909807314587353088.
```

Run the six-case numerical producer with `/home/sgusev/miniconda3/envs/minlp-notes/bin/python code/potential_flow_mpd/envelope_rational_certificates.py`. The numerical solver happened to report `optimal` in these six certificate examples; certificate validity itself does not use or inspect that status.

## Verifier boundary and optimized-mode correction

The saved JSON certifies the deterministic asymmetric-quadratic energy instance specified in that file. It does not encode the original resistance intervals, the target edge, or the maximizing/minimizing envelope construction. Therefore the uncertainty-extremum interpretation also requires an independently correct mapping to the chosen envelope instance; the JSON verifier alone does not validate that mapping.

The first development version used Python assertions for certificate validation. Root review identified that `python -O` would remove those checks. Before promotion, the verifier was changed to unconditional checks raising `ValueError`; a regression now runs the verifier in optimized mode and confirms rejection of a corrupted energy gap. Valid saved certificates also verify under optimized mode. The numerical producer's internal test assertions are separate from the verifier's unconditional mathematical checks.

The numerical producer's `conserved_rounding` helper is explicitly restricted to simple, loopless, connected graphs; it validates those assumptions before constructing its spanning tree. The exact verifier's conservation/duality argument does not require simplicity, but that broader mathematical scope is not silently assigned to the rounding helper. Regression checks reject parallel-edge, self-loop, and disconnected helper inputs.

## Independent audit

The [full audit](../notes/review-potential-flow-envelope-rational-certificates.md) passed after the verifier and rounding-helper corrections documented above. The reviewer wrote an independent standard-library checker, [`check_envelope_certificate_review.py`](../code/potential_flow_mpd/check_envelope_certificate_review.py), which passed five exact known physical states, 800 integer-root minimality checks, 16 corrupted-file rejections across normal and optimized Python, valid-file checks in both modes, and rejection of floating-point gap/radius metadata. The reviewer also reproduced all six numerical producer cases.

The separately [reviewed Bregman refinement](potential-flow-envelope-bregman-certificates.md) supplies tighter posterior edge intervals and sign-based original-scenario guarantees. The later [original-instance pipeline](../notes/potential-flow-certified-envelope-pipeline.md) also verifies the graph, target, original resistance data, envelope mapping, and recovered scenario. These are separate reviewed components; the base JSON format described here still certifies only its deterministic energy instance.
