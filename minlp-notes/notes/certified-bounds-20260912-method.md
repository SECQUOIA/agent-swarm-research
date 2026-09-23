# Checkable bounds for convex MINLP

Updated 2026-09-13 after the correctness repair. This note supersedes its September 12 version. The original 269/289 acceptance result is historical evidence, not the current verification result. Current results and remaining limitations are collected in [the repair and replay record](certified-minlp-repair-and-replay.md). The manuscript directory is intentionally unchanged.

The method certifies a finite lower bound for a convex minimization problem, or a finite upper bound for a concave maximization problem with integer variables. It interprets each numeric leaf of the loaded Pyomo expression tree exactly and performs subsequent coefficient arithmetic rationally. Python calculations and Pyomo rewrites performed before that tree exists are part of input construction; their original decimal or algebraic intent cannot be recovered. Equivalence to another input format requires separate evidence.

A numerical outer-approximation solver proposes supporting points and slopes. The producer reconstructs the nonlinear rows from the exact model, evaluates function values and derivatives with rigorous intervals, and shifts rounded rational cuts far enough to ensure underestimation on the certified box. Exact linear propagation can tighten that box without excluding any original feasible integer point. One-sided and free coordinates require the residual-slope conditions proved in [the soundness note](certified-minlp-soundness.md).

The certificate consists of the source model, a JSON list of cut points and rational affine coefficients, a rational MILP master, and a complete VIPR proof. The checker:

1. Reconstructs exact expressions, domains, curvature, affine rows, bounds, integrality, and objective sense/constants.
2. Recomputes every cut's sufficient intercept bound and rejects unsupported points, derivatives, or intercepts.
3. Regenerates the master and checks its identity with the proof's mathematical problem, including a bijective variable mapping and positive row scaling.
4. Independently replays all discrete proof inferences using exact rational arithmetic. An external `viprchk` can corroborate the result, but its verdict is not the proof authority.
5. Returns a certified numerical bound only after all complete checks succeed. A requested partial check has `partial_ok` and `status="partial"`, while `ok` remains false and no certified bound is exposed.

The mathematical argument is feasible-set inclusion: every original feasible point extends to a feasible master point with the same normalized objective. Valid master lower bounds therefore transfer to the nonlinear problem. Neither attainment nor Slater conditions are needed for this conditional implication. It is not a completeness result or a guarantee that every convex model admits a certificate supported by this implementation.

The repair addresses a false-bound acceptance using an empty VIPR solution section, a second upstream rounding defect involving continuous variables, inconsistent floating-point coefficient aggregation, unsafe curvature/domain paths, and ambiguous partial-verification results. Original domains are checked before simplification. The former perspective shortcut is disabled because it checked curvature on the wrong potential ratio domain; valid models outside the remaining recognition rules are rejected conservatively. The exact proof checker has a documented supported syntax and checks branch assumptions, integrality, references, lifetimes, solution witnesses, and the final bound. See [the proof replay contract](certified-minlp-vipr-replay.md).

A checked master solution is not automatically a feasible nonlinear solution. Closeness to a MINLPLib reference value is therefore a bound-quality statistic, not an optimality certificate. The separately audited `clay0204m` case combines an exact feasible nonlinear witness with a checked matching lower bound; its precise result is in [the solver discrepancy audit](certified-minlp-solver-discrepancies.md).

The trusted software includes input loading, exact expression extraction and curvature rules, SymPy differentiation, mpmath interval arithmetic, rational master construction, the proof parser and replay kernel, Python, and python-flint/GMP. The numerical optimizer and external proof generator are outside the mathematical acceptance boundary. Independent agent review and adversarial tests are useful checks, not journal peer review or a mechanized proof of this implementation. No Lean verification of this pipeline is claimed.

Earlier literature searches missed direct prior work. Halbig et al. (2024) already compute and verify convex-MINLP optimality certificates; safe rounding, outer approximation, and MILP proof replay also have established foundations. The candidate contribution is the specific replayable integration and its audited computational evidence. [The refreshed primary-literature comparison](certified-minlp-literature-audit.md) records the distinction, including Wood et al., CakeML, SCIP, and related interval-based software. Publication priority remains qualified.

Implementation and reproduction commands: [certify/README.md](../code/minlp_solver_lab/certify/README.md). The small [quadratic example](../code/minlp_solver_lab/certify/examples/quadratic/README.md) can be checked without a numerical solver or the local MINLPLib collection.
