# Stage 1, round 1 — review 02

Reviewed `papers/pooling/sections/01-foundations.tex` in full. Focus: rational bit complexity, compactness, exact output, and NP/ETR certificates. I also read the canonical profitable-flow and facial-integrality results and the recirculation investigation, and checked the stage-1 entries in the coverage inventory. I did not inspect other reviewers' reports.

## Finding 1 — endpoint formulation needs the upper-only hypothesis

**Location:** lines 641–672, especially the claimed equivalence at 647–651 and the exact MILP assertion at 660–667.

**Severity:** major as written (a missing essential hypothesis makes an asserted equivalence false); repair is local and does not undermine the intended upper-only result.

This subsection starts at lines 520–523 with arbitrary rational polyhedral product regions. The general model also permits lower quality bounds. The endpoint paragraph subsequently imposes input attributes in `[0,1]` and product **upper** bounds in `{0,1}`, but never restricts the product regions to those upper bounds alone. Its support disjunctions ignore lower and cross-coordinate quality restrictions.

For a concrete counterexample, take one input of scalar quality 0, one pool, one product, unit arc/node capacities, and product quality interval `[1/2,1]`. Set all flow lower bounds to zero. This satisfies the paragraph's stated input-quality and upper-bound conditions, but `D = S = 0` for every flow. Its displayed disjunction therefore accepts unit delivery, whereas the original lower quality constraint requires `0 >= t/2` and forbids any positive delivery. Giving the feed cost `-1` also separates the alleged exact MILP optimum (`-1`) from the physical optimum (`0`).

**Proposed fix:** Start the paragraph with: “For the following special case, product quality restrictions consist only of coordinatewise upper bounds; there are no additional lower or cross-quality constraints. Assume all input attributes lie in `[0,1]` and each product upper bound lies in `{0,1}`.” Equivalently allow only redundant lower bounds at most zero. Retain the lower **flow** bounds permitted earlier; these cause no problem if removed arcs are checked against their bounds. Scope the ensuing MILP and NP claims to this expressly defined class.

## Finding 2 — finite capacities should be explicit where minima are introduced

**Location:** lines 187–190; also the bounded-lift sentence at lines 125–127.

**Severity:** minor assumption clarity.

The global model says arcs and totals “may have” finite bounds (49–50), whereas the profitable-flow subsection states only “nonnegative upper capacities.” Its displayed minima and finite approximation quantities require a globally bounded flow set; nonnegative finite bounds on every arc, as used in the canonical source, suffice. If an absent bound means an unbounded arc, the one-input/one-product arc of cost `-1` has infimum `-infinity` and no minimum, and bounding qualities alone does not make the lifted set bounded. The manuscript clearly intends the finite-capacity case, but it should state this before introducing `z*`.

**Proposed fix:** Say that all arc flows have finite rational upper bounds in this subsection, or that the specified finite capacities bound every arc flow. Move the finite-flow-bound qualification before the assertion that the lift is bounded at 125. The explicitly uncapacitated conic section remains unchanged.

## Checks that passed

- The standard/acyclic quality-box argument preserves the arc-flow projection and gives a compact projection once finite flow bounds are imposed. Zero-throughput pools can be reassigned without affecting any product. The cyclic compactness argument also works: source-reachable active blocks have uniquely determined source-average qualities, and isolated positive circulations can use zero.
- ETR membership follows from a polynomial number of quadratic equalities/inequalities with polynomial coefficient encoding. No unsupported inference of general NP membership appears.
- Affine-rank compression can be computed using rational elimination with polynomial bit length. Original product constraints remain present after substitution, so growing attribute count is not erased incorrectly.
- Rational single-product LP vertices have polynomial encoding; source-quality reconstruction is a nonsingular rational linear system on the active nonisolated pools. Clearing denominators rowwise and applying determinant bounds gives polynomial coordinate bit length, even for deep acyclic networks or ill-conditioned cyclic blocks. The absorption proof establishes invertibility without pretending that its probabilistic convergence rate is polynomial.
- The shortest-path witness has polynomially many path edges, a polynomial-size rational mixture vertex, and a positive scale obtainable from polynomially many rational capacity-to-used-throughput ratios. The `K+1` support argument is correct.
- Destination decomposition, single-product projection, conic-hull equalities, the capacitated-hull counterexample, cyclic circulation separation, and cyclic sign criterion withstand direct proof checking.
- Facial integrality follows from compatible support branches and integral network polytopes; the converse produces a rational strict improvement by a bounded rational LP. Face recognition uses polynomial-size LPs. Fixed-dimensional face enumeration has polynomially many rational hyperplanes, faces, and pool tuples, with polynomial bit sizes; it claims fixed-dimension polynomial time, not a uniform-exponent FPT bound.
- For the intended upper-only endpoint class, bounded branch vertices supply polynomial-size rational threshold certificates. With integer bounds, integral arc flows are enough; pool-quality coordinates need not be integer or included in the certificate.

## Verdict and limits

**Verdict: major findings present**, due to the unstated upper-only hypothesis for the endpoint equivalence. One additional minor assumption clarification is recommended.

This was a mathematical and bit-complexity review of stage 1 and its identified repository proofs. I did not re-audit publication priority or the final journal versions of cited sources, compile the manuscript, examine later stages, or claim exhaustive correctness. No computational experiments were needed to establish the explicit counterexample above.
