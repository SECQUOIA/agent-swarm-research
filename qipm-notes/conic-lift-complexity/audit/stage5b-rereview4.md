# Independent Stage 5B rereview 4

No valid major or minor issues found.

I read all five requested sections end to end: `12a-resource-ledgers.tex`, `12b-work-contracts.tex`, `12c-newton-comparisons.tex`, `12d-query-output.tex`, and `12e-active-compilers.tex`. I followed the supplied global instructions and `/workspace/qipm/AGENTS.md`. I did not read earlier or current review reports, root checks, assessments, or correction-author reports. I made no manuscript edits and did not delegate.

## Fresh scale maintenance and static reuse

The additions in `12c-newton-comparisons.tex:382–563` are mathematically sound under their stated contracts.

- The quantum compile-and-commit contract at lines 382–400 requires fixed encoded value strings and exact restoration of the backing workspace, including retained correlations. This justifies extracting every committed value before continuing the maintainer. It does not assume that a consumable quantum state can be read without disturbance.
- In `newt:dynamic-scale`, the reset family has exact slacks `1/s` and `2/s`, which remain interior, including at `s=2`. Dividing by the public source column count preserves the relative-error decoder. The intervals are disjoint for every stated `0 <= delta < 1/3`.
- The Kronecker-sum adversary for the `Tb` independent presence bits has norm `Tb sqrt(s-1)` and filtered norm one. The finite-output adversary theorem applies directly. This covers superposed access to all epoch oracles and arbitrary persistent workspace.
- The randomized argument correctly conditions on the no-mark transcript and sums expected queries over independent pairs. The quantum upper bound uses exact search for the known one-mark case followed by verification, so zero-mark instances cause no error and joint success requires no amplification logarithm.
- The replicated-block family has `s/k-1 = Theta(s/k)` candidates throughout the stated range. Its update sparsity is `k`, and its smaller slack is `rho_* = k/s`; the claimed margin laws follow.
- In `newt:scale-service`, the distinct-basis-label client proves the lower bound for the universal service. Controlled exact search, deterministic-bit copying, and uncomputation implement a clean coherent invocation; a classical table supplies the other upper-bound branch. The `min(r_t,b)` transition, zero invocation budgets, and margin substitution are valid.
- In `newt:fixed-scale`, stationarity gives `rho + tau^2 rho^2/4 = 1` and the displayed solution, including zero objective blocks and zero multiplier. The Hessian ratio follows directly. Acquisition of fixed norms is charged once, while scalar precision and reversible arithmetic remain separate costs.
- The sparse-list alternative and the explicit exclusion of an unproved embedding into one fixed Newton trajectory are retained. None of these statements improperly multiplies a static query lower bound by an iteration count.

## Remaining mathematics and output distinctions

The exact auxiliary quotient and eliminated gradient in `12c-newton-comparisons.tex:141–291` check out. Feasible allocations give the crucial identity `sum tr(D0 E D E) = theta^T M0 theta`; positive trace pairing then yields the first-power comparison. Inversion gives the stated dual transfer. The two-column example attains both comparison endpoints and the condition ratio. The trace-distance calculations and the weaker approximate-allocation bounds are correct.

The resource ledgers, nullity envelopes, Holder constant, and continuous aspect ratio in section 12a are consistent with their integer and geometric hypotheses. The intrinsic grouped and packed parameters use a box section and bounded-fiber partial minimization, respectively; they are distinguished from ambient parameters and projected-body parameters. Section 12b retains the same aggregate certificate rank in curvature and movement, and its work multiplication has an explicit fresh per-round charge. The matching path has the stated speed, accuracy schedule, and serialization costs.

The Newton graph counts and signed-rank augmentations check out. The exact field-operation solver has the required supplied decomposition and nonsingularity assumptions. Its full-output replacement is appropriately limited by coefficient access, admitted trajectories, exact arithmetic, and finite-precision certification.

Section 12d's sign recovery, Boolean-mean rescalings, fixed scalar readouts, search diagnostics, state preparations, and movement estimates have the stated contracts. Hidden-dependent projected norms are not granted for free. The product-domain and direct-ball precision comparisons concern different bodies, as the text explicitly states.

For section 12e, I checked the consensus search reduction and KKT conditioning, both Pareto witness identities, the growing-dimensional decoder spacing and feasibility argument, and the entropy epigraph identity including its closed boundary. The natural and compiled path lengths use their specified barriers. The planar universal-barrier upper bound does not become an intrinsic lower bound from the natural barrier's large parameter. The entropy paths coincide at matched gaps, and their two lengths are measured in the correct full or marginal metrics. Compiler, readable-coordinate, objective-value, and amplitude-state output are kept distinct.

## Source and computational checks

I compared the substantive claims against the source notes `2026-09-04-dynamic-psd-fiber-scale-maintenance-lower-bound.md`, `2026-09-04-pareto-soc-barrier-compiler.md`, `2026-09-04-kblock-pareto-soc-compiler.md`, and `2026-09-04-blockwise-relative-entropy-source-compiler.md` in `notes/workbench/active`. The dynamic maintenance, universal invocation tradeoff, margin refinement, static caching, active-factor witnesses, readable-output decoders, and matched-gap comparisons are retained with their material scope restrictions.

Primary-source checks confirmed the finite-output adversary and direct sum in [Ambainis–Childs–Le Gall–Tani, Theorems 3–4](https://arxiv.org/html/0903.1291v2); exact known-success amplification and zero-versus-known-cardinality search in [Brassard–Hoyer–Mosca–Tapp, Theorems 4 and 16](https://arxiv.org/pdf/quant-ph/0005055); the dimension upper bound in [Lee–Yue](https://arxiv.org/abs/1809.03011); and the supplied-decomposition linear-system bound in [Furer–Hoppen–Trevisan, Corollary 3](https://drops.dagstuhl.de/storage/00lipics/lipics-vol351-esa2025/LIPIcs.ESA.2025.116/LIPIcs.ESA.2025.116.pdf).

Using `/workspace/local-home/miniconda3/envs/qipm/bin/python`, I checked the claimed integer `V_R` formula for `R=2,...,30`, `N=1,...,500`, and both explicit `F_4,F_5` formulas against dynamic programming. I also checked the allocation-aware matrix and quotient inequalities on 200 random feasible off-center packed instances. All checks passed. These computations supplement the algebraic review; they do not replace the proofs.
