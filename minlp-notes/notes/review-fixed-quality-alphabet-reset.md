# Independent review: fixed-quality-alphabet bypass reset

Date: 2026-09-05. Reviewer: `pooling_degree_two`. Verdict: **PASS** for
[the fixed-alphabet construction](degree-two-fixed-quality-alphabet-investigation.md),
including its uniform linear penalty and the stated nonlinear geometry
transfer. This is a structural realization of known exponential shadows;
no new hardness or general optimization classification follows.

The reset output has exact demand `s` and receives `t` from a quality-zero
input and `s-t'` from a quality-one input. Its redundant upper quality one
adds no restriction, and conservation gives `t'=t`. The following
quality-one to quality-zero mixing step has output upper capacity `S` and
upper quality `1/2`; these give `t'<=t_next<=S-t'`. Combining reset and
mixing steps with `S=4s` proves the claimed exact Klee–Minty projection.
Every source and output has degree at most two, and only input qualities
zero and one are needed.

The path price-difference formula is exact. Coefficients on reset right
flows are zero, so only the original free-coordinate coefficients remain.
The only varying physical price is the terminal price. Its contribution
to the constant offset is absent because the offset uses the preceding
output price at each source. All base arc coefficients lie in `[0,2]`.

For the upper-only linear network, the removed contracts include both
source supplies and reset-output demands. Adding `M` to all output
revenues rewards all source throughput by conservation. Adding another
`M` only to reset-output revenues rewards precisely the remaining reset
contracts. Their deficits are nonnegative. The reviewed error bound with
integer coefficient rows gives a repair of norm at most `N^N` times the
total deficit, independently of the rational right-hand sides. Thus
`M=2N^N+1` strictly rewards every nonzero deficit repair and forces all
contracts at optimality, uniformly over the stated price interval.

I inspected and reran
[the exact original-network checker](../code/parametric_path_lp/exact_fixed_alphabet_check.py).
All 252 certificates through dimensions two to seven passed. Its active
rows are actual physical source capacities, reset-output capacities,
nonnegativity, and mixing-output capacity or upper-quality rows. The
square active system has strictly positive exact rational dual
multipliers. All remaining physical rows are checked separately. Thus
these certificates prove unique optima in the actual upper-only network;
they do not assume extra signal-copy equations.

The nonlinear interface attaches to the final quality-zero input without
changing its algebra. The extra quality-two source expands the input
alphabet to three values. Exact reset steps give affine duplicate flows;
price differences vanish across equal consecutive supplies and equal
`3s_j` before the next descending step. Hence the previous physical
objective, vertex correspondence, perturbation, and convex-hull proof
transfer exactly. This extension retains its explicit exact contracts,
including the pool throughput contract. The linear penalty proof above
does not remove those nonlinear contracts.
