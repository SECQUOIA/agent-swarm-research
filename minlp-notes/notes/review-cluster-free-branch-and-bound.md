# Review record: cluster-free branch-and-bound at nondegenerate constrained minima

Subject: [results/cluster-free-branch-and-bound-constrained-minima.md](../results/cluster-free-branch-and-bound-constrained-minima.md).

**Status after the ten-agent corrective audit (2026-09-22).** The earlier
verdict below missed an incorrect box orientation in the neighborhood
counterexample and several counting/scope errors. The result now repairs the
example analytically, restricts claims about domain reduction to proved
conditions, and distinguishes the local count from total-tree complexity.
The incumbent-sign and continuity-modulus corrections already existed before
this audit. See [the corrective audit](review-minlp-developments-20260922.md)
for the additional corrections and targeted checks. The historical numerical
claims below for the original counterexample are superseded.

## Independent adversarial review (2026-09-22, subagent, read-only)

**Later attribution correction.** The
[error-bound review](review-20260922-error-bound-transfer.md) identified
Anitescu's established off-feasible exact-penalty growth inequality as the
core principle behind the mixed bound. The earlier significance assessment
below is superseded: this is a useful spatial-search application, not a new
growth principle. Strict complementarity is not necessary under ordinary
SOSC and a linear feasibility error bound. The quartic example below fails
ordinary SOSC and does not prove that strict complementarity is necessary.

Re-derived every inequality of Theorem 1 (Steps 1–6) and the counting argument
of Theorem 2; confirmed that the proof holds for every point of the relaxed set
(no attainment needed), that an interior minimizer is not needed (active bounds
among the constraints), and that the Definition-14 neighborhood property of
Kannan–Barton can fail for standard αBB schemes even under LICQ, strict
complementarity and second-order sufficiency, so the mixed bound is the right
substitute rather than a weaker form of the same statement.

Adversarial numerics (reviewer's own scripts): `min -x_3 + 2x_1^2 + 2x_2^2`
s.t. `x_3 + x_1^2 - x_2^2 + x_1 x_2 <= 0` on `[-1,1]^3` with αBB
(`alpha = sqrt(5)/2`); about 800 boxes at distances `0.005–0.2` from `z*` with
width-to-distance ratios `0.02–0.3`, placed randomly, touching the constraint
surface, and on the infeasible side: `min (L(Z) - f*)/dist^2 = 0.85 > gamma/4 = 0.44`.
No counterexample. The initial review incorrectly claimed strict complementarity was shown necessary by
`min x_1^2 + x_2^4` s.t. `-x_2 <= 0`.

Verdict: mathematics correct; accept after wording and scope fixes.
Significance assessed as "in between, closer to the useful end": the
computation is Kannan–Barton's Theorem 5 carried out away from `z*`, with the
normal-component control and the positive-multiplier slack term as the
additions; conceptually it resolves the practical form of their open question
and shows the literal form is generally false for standard schemes.

Corrections requested and applied:

1. Incumbent remark: with `UBD = f* + eta` the effective tolerance is
   `eps - eta` (not `eps + eta`), and `eta < eps` is required.
2. Section 5 rewritten to describe the actual code (Examples A and B); the
   earlier Example 2 on `[-1,1] x [0,1]` fathoms at once because the bound
   `x_2 >= 0` makes the lower bounds exact.
3. The original `Theta(eps^{-1/4}/delta)` statement was hedged as a worst-case
   covering count. The later corrective audit found the exponent was still
   wrong; the result now uses the quartic tangential extent `eps^{1/4}`.
4. The claim that the Definition-14 gap can be of order `|z - z*| w(Z)` is now
   supported by the reviewer's verified example (`y_b = (b, -2b, 5b^2)`).
5. Step 3 rewritten with a modulus of continuity of the Hessian so the proof is
   valid under `C^2` data; condition (ii) of Step 6 adjusted accordingly.
6. Citation corrected to Definition 13 (pointwise convergence of schemes).
7. Remark added that LICQ is not used beyond injectivity on `C^perp`.
8. Summary wording: Kannan–Barton 2017 show neighborhood second order
   *suffices*; Theorem 1 stated in pointwise form for all `z in R(Z)`.

## Literature check (2026-09-22, subagent)

No published statement found; Kannan–Barton 2017/2018 and Kannan's 2018 thesis
(p. 304) list the neighborhood question as future work; Neumaier 2004 (Acta
Numerica, Section 15) has an unproved "reduced manifold, `n - a`" remark;
Kannan–Barton 2017 Remark 2 uses the fixed-multiplier Lagrangian only to
estimate the growth constant on the feasible set. Details in the note's
Section 6.

## Not done

No Lean formalization. The subsequent audit also covers the conditional
reduced-space theorem added after this first review; it does not establish a
general guarantee for FBBT, OBBT or interval Newton.
