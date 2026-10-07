# Optimal sets and boundary output: continuation results

Date: 2026-10-02. These results extend topic 1 in three explicit classes.
They do not establish an efficient general unknown-growth theorem for
arbitrary optimal sets or the general finite exact polynomial boundary
certificate.

The second phase supplies [reusable optimal-set discovery and checking](../completion/optimal-sets.md)
and [automatic polynomial boundary search](../completion/polynomial-boundary.md).
These now run on user models, including actual unknown-growth trials and
implicit irrational optimizer descriptors. Their capped simplex and restart
implementations do not inherit every theoretical runtime guarantee. The
diagnostics below are retained as first-release evidence.

| Result | What is discovered and certified | Assumptions and cost |
| --- | --- | --- |
| [Unknown growth on the diagonal-certificate class](unknown-growth-diagonal-class.md) | One rational optimizer, exact value, and the full optimal set as a compact polynomial system; no supplied optimizer or growth constant | Continuous rational box QP admitting the established diagonal Lagrangian certificate at an optimum; \(f(p,\kappa)\operatorname{poly}(I)\) discovery |
| [Endpoint optimal-set certificate](endpoint-optimal-set.md) | All optimal faces through nonnegative Bellman residuals and endpoint-support constraints, including mixed integer boxes | Nonpositive quadratic diagonal; \(2^{O(p)}\operatorname{poly}(I)\), with no growth parameter |
| [Discovered active face and convex patch](boundary-active-face.md) | Selected exact implicit polynomial optimizer after certified endpoint substitutions; no full-Hessian premise | Unique point growth and strict complementarity; \(f_d(p,\kappa)\operatorname{poly}(I+B_\gamma)\), where \(B_\gamma\) measures active-gradient precision |

The first result supplies the missing **algorithmic discovery** step for an
existing independently checkable certificate class. Incorrect growth
guesses may produce nonglobal KKT points; acceptance requires a global PSD
certificate and cannot mistake a small promise-dependent interval for a
proof. Invariance of the diagonal certificate across all optimal components
makes the exact-recovery output acceptable regardless of the component it
approaches. It includes unknown tilted and disconnected continua.

The second result extends the familiar endpoint solver's output. Merely
collecting optimal coordinate labels is insufficient to describe the
continuous optimum set; the local residual-support equations preserve the
required correlations without enumerating the optimal components.

The third gives a complete automatic boundary-face search in a restricted
case. Its additional precision term is explicit and can be exponential in
input length even at fixed width and growth ratio. Bernstein signs sometimes
avoid that precision cost, but no completeness or cost bound is asserted for
those shortcuts outside the stated theorem.

## Independent review and exact diagnostics

A separate agent reviewed the actual saved notes and their prerequisite
proofs. The [review](reviews/review.md) found one runtime issue: an
arbitrarily small dyadic target would not support the claimed trial bound.
The algorithm now chooses the largest admissible dyadic. The reviewer found
no remaining mathematical gap in the three restricted theorems. This is
research-agent review, not journal peer review or an external novelty audit.

The targeted command

```sh
python3 -B research-20261002-decomposition/degeneracy/check_extensions.py
```

passed the following exact checks:

- 256 diagonal-certificate identities and full-set membership equivalences,
  including tilted disconnected segments and singular PSD matrices;
- rejection of the earlier false-growth example's nonglobal KKT point and
  acceptance at its true optimum;
- 135 endpoint-interpolation and full-set equivalences on a branching
  decomposition with overlapping bags, interior integer labels, and a
  strict negative diagonal;
- a complete proximal candidate/recovery fixture with two endpoint modes
  times a free continuous interval: 21 stages and 1,158 exact local objective
  evaluations, followed by an independently valid diagonal certificate;
- 34 boundary-elimination and precision-budget checks, including a negative
  full-Hessian entry removed by a verified weak derivative sign.

The first run exposed an overly restrictive assumption in the **diagnostic**:
it expected candidate generation always to select the lower optimal mode
and keep the free coordinate at its initial bound. The corrected check
accepts either recovered optimal mode and solves the free stationary equation,
matching the theorem. The mathematical algorithm requires neither mode
selection nor a stationary free-coordinate center.

The reviewer separately ran exact arithmetic checks of 18 diagonal identities
and 162 overlapping-bag endpoint identities. These finite diagnostics
support the explicit algebra and regression boundaries; they do not prove
the universal theorems or benchmark a general solver. The complete proximal
fixture is intentionally small and uses explicit bag enumeration and a
trivial stationary LP for that fixture. The general rational LP and the full
boundary search are mathematical algorithms, not production implementations
provided in this directory.

The other targeted commands actually run were
`git diff --check -- research-20261002-decomposition/degeneracy` and an
inline `python3 -B - <<'PY'` check of this directory's Markdown local links,
paired display delimiters, and trailing whitespace. Both passed. These are
local checks; no project-wide verification or CI inspection was performed.

## Remaining frontier

The general sparse QP problem with an unknown arbitrary optimal set still
needs an efficient discovery and representation guarantee outside the two
classes above. [General exact recovery](../completion/exact-output.md) is
now implemented without uniqueness, but its finite termination alone gives
no useful parameterized state bound for arbitrary sets. The
[earlier audit](../../research-20261002/new-direction/unknown-growth-certificate-audit.md)
continues to rule out direct fine-grid certification along flat directions
and explicit enumeration of all stationary optimal pieces at the desired
parameterized cost. Its oracle obstruction does not prove impossibility for
explicitly encoded quadratic programs.

For fixed-degree sparse polynomials, point growth alone still gives certified
arbitrary-precision enclosures, but a generally discoverable finite exact
descriptor remains unproved. Weak active derivatives, tiny strict margins,
and nearby nonglobal KKT minima cannot be dismissed by a restricted-Hessian
statement without an algorithm to identify and certify the face.
