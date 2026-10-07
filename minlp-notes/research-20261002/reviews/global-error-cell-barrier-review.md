# Independent review of the global-error cell barrier

Date: 2026-10-02. Verdict: passed. Read the full
[connected construction](../new-direction/global-error-cell-barrier.md)
against the actual retention and closure rules of the
[sparse polynomial theorem](../new-direction/smoothed-sparse-polynomial.md).

The nonzero clique-plus-path interactions give actual treewidth `p-1`.
The quartic's upper coordinate curvature is exactly two; the positive
bilinear couplings add no diagonal curvature. Since the quartic sum is
nonnegative and zero exactly at vertices, while the other terms are
multiaffine, every global minimizer is a vertex. Hence any complete dyadic
grid has exact optimum `f*`, uniformly over the whole noise box.

Completing any bag corner by a minimizing vertex outside that bag changes
the objective by at most `29p/400+1/200<=3p/40`. The global error allowance
is `nh^2/4`. Induction therefore retains every cell through the last dyadic
level with `h^2>=3p/(10n)`. The next dyadic level fails this inequality,
so this retained level has `h^2<6p/(5n)`. Its clique cell count is at
least `(5n/(6p))^(p/2)`. The full deduplicated row count is larger, and
all completions used in the induction are indeed allowed because every
preceding whitelist remains full.

The whole-hull closure tests cannot bypass that level. Every projection
hull remains `[0,1]`; the exact gradient takes both signs by evaluating
one coordinate at `1/4` and `3/4` with its neighbors zero. At the common
midpoint, the Hessian is `-I+eta A_G`, whose largest eigenvalue is below
zero by the maximum-degree bound. Thus the actual positive-Hessian test
cannot succeed. The stated cutoff inequality also forces refinement well
past the counted level. These conclusions apply to every supported noise
draw, so the same lower bound holds in expectation.

This is enough to exclude `f(p) poly(I)` retained-state work for the
specified rules: fix `p` larger than twice any proposed absolute input
exponent, then increase `n`, while the encoding is `O(n log n)` for that
fixed `p`. It does not contradict the existing dimension-dependent upper
bound. The construction is easy by endpoint DP, and it does not rule out
cellwise derivative tests, a different recourse representation, or a
different algorithm. Those scope qualifications are correct and essential.

The separate [local-error note](../new-direction/local-error-recourse-interface.md)
gives a complementary guardrail: simply replacing the global correction
by a bag-local correction is unsound even on a star quadratic. That
counterexample was independently recalculated by the coordinating
researcher and the connected-barrier author. Its sufficient conditional
recourse interface identifies a genuine additional oracle requirement,
not a completed FPT algorithm.

A scoped document check verified whitespace, paired mathematical
delimiters, equation numbering in the construction, and local links.
No optimization executable, external search, project-wide check, CI
inspection, or index change was used for this review.
