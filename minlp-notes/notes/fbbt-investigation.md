# FBBT investigation, 2026-09-04

The strongest current candidate is [constant-error hardness of bilinear FBBT limits](../results/fbbt-monotone-system-hardness.md). Its proof passed [independent review](review-fbbt.md). The key observation is that forward interval propagation on a nonnegative defining system computes its least fixed point in the limit; sound reverse propagation cannot remove that feasible point. Existing probabilistic-program verification hardness therefore transfers to MINLP presolve.

A companion [doubly exponential primitive-iteration lower bound](../results/fbbt-doubly-exponential-convergence.md) also passed independent mathematical review. The [verification script](../code/fbbt-hardness-check.py) passed 50 exact circuit/gap/SCC checks and 400 primitive-update invariant checks. The [separate source assessment](fbbt-novelty.md) is complete, with qualified priority and explicit antecedents.

Update, 2026-09-20: the companion iteration theorem now has a [completed Lean verification record dated 2026-09-11](../formal/topics/02-fbbt/VERIFICATION.md), including kernel replay of all eight FBBT modules. Its [coverage map](../formal/topics/02-fbbt/COVERAGE.md) includes exact `4n+4` variable and equation counts, the finite-prefix lower bound without fairness, nonattainment of the limiting lower endpoint in finite time, and convergence of both endpoint vectors under every fair schedule. The result note now supplies the separate upper-endpoint argument needed for the singleton limiting box; the general least-fixed-point lemma only establishes lower-endpoint convergence. The PosSLP-hardness reduction, binary encoding-length estimate, and publication novelty remain outside this formalization.

Useful qualifications and rejected directions:

- Irrational endpoints and non-finite convergence are easy to construct, and are much weaker than the constant-error hardness candidate.
- Slow linear FBBT iteration and its polynomial-time LP acceleration are already known (Belotti et al.); do not present these as discoveries.
- A first idea imposed `P(1)<=1` to keep all upper bounds fixed. This is unnecessary for the lower-bound identity: preservation of the least feasible point handles every reverse update. Dropping that assumption is essential for transferring constant-error hardness.
- The normalized case `P(1)<=1` is precisely the probabilistic polynomial-system subclass with a known polynomial-time additive approximation algorithm (Etessami–Stewart–Yannakakis). Exact threshold comparisons remain difficult. This is a useful tractable subclass, but Newton's method and its complexity theorem are established work.
- Bounded strongly connected component size in the directed defining graph does not rescue the unrestricted class. Acyclic circuits can encode extremely small values that feed a scalar quadratic fixed point and a scalar linear amplifier.

Primary references were downloaded to `literature/external-fbbt/` for audit. The exact external theorem underlying the reduction is Etessami–Yannakakis (2009), Theorem 5.2, with promised termination probability at most epsilon or equal to one. The completed source assessment supports only a qualified claim about the restricted FBBT transfer; it does not establish publication priority.
