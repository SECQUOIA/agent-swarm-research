# Closing audit of the weighted path-sign corollary

Date: 2026-09-05. Independent review by the root agent of the previously
drafted [path-sign refinement](potential-flow-weighted-sign-path-decomposition.md).
Verdict: **PASS**, as a supporting corollary of the twice-reviewed
[global-rank theorem](../results/potential-flow-fixed-support-global-rank.md).

The additional proof obligation is replacing constant positive adjoint
sources by strictly positive or strictly negative sources on each path.
The displayed perturbation gives current increments `c_v+delta*sigma`,
all strictly of sign `sigma`. Positive differential resistances therefore
give one peak for positive sources and one valley for negative sources.
At most one edge current vanishes, so an extremal plateau has at most two
vertices. Every horizontal level meets at most two internal vertices.
Returning paths have equal endpoint potentials and obey the same argument.
Zero coefficients are covered by the nonzero perturbation; different paths
can choose different signs. The compensating coefficient is at a marked
reference vertex whose nomination is left free, preserving zero total
objective coefficient.

Suppression gives a connected multigraph, including loops, with
`P=k-1+r_actual<=k-1+r`. The note now distinguishes actual rank from its
upper bound. Paths with no internal vertices and a pure cycle marked at
one reference vertex satisfy this count. Pruning occurs before checking
the marked-set conditions. At most `k+2P` nominations remain free on each
face. For minimization apply the maximum argument to `-c`; the face family
can differ, but its size and dimension bounds are unchanged.

The finite closed face family is independent of perturbation parameters
and resistance values. Uniform convergence on the compact domain, the
fixed-face subsequence argument, and transfer through a fixed maximizing
resistance profile follow exactly as in the reviewed parent theorem.
Each face still has a fixed-dimensional nomination/circulation core.
Unbounded objective support changes only rational edge weights in the
objective, not the aggregate count. Thus the parent's fixed-core theorem,
polynomial encoding bounds, and algebraic witness recovery apply.

The corollary retains independent positive continuous resistance intervals,
balanced nomination boxes, no operating-constraint filter, fixed GLOBAL
rank, and possibly algebraic outputs. It does not establish bounded rank
per block or discrete resistance optimization. The
[parent source comparison](potential-flow-fixed-support-global-rank-novelty.md)
is the appropriate prior context. No new general adjoint method, separate
publication-priority assertion, or resolution of inaccessible older
circuit-tolerance literature is claimed.

The [exact checker](../code/potential_flow_mpd/check_signed_path_adjoint.py)
checks the additional signed-path argument using rational data, including
zeros before perturbation, exact plateaus, and returning paths. Finite
checks supplement the proof and do not implement the algebraic optimizer.
