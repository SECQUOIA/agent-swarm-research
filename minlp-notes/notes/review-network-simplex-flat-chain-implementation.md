# Independent review of the flat-chain exact separator

Date: 2026-09-07. Reviewer: independent `review_separator` subagent.

**Verdict: pass after an observation-index validation correction.** The exact
implementation in [`flat_chain.py`](../code/network_simplex/flat_chain.py)
matches the [fixed-state flat-chain theorem](../results/network-simplex-flat-chain-fixed-states.md).
Reviewed SHA-256:
`48130c61af25f5a78b8395cbbc47fd29e20124a4858109a8eecc7579fce7cc98`.
This review establishes neither literature priority nor a speed advantage.

## Scope and correctness

The class constructs the stated canonical graph: `L>=1` consecutive gadgets,
each with two forward unit-capacity arcs, and a forward bypass, with unit total
flow. Arcs `2*l,2*l+1` are the two arcs of gadget `l`; arc `2*L` is the bypass.
It does not recognize or assert applicability to arbitrary graph inputs,
capacities, balances, or nested series-parallel graphs.

The preliminary conditions `x_a+x_b+x_h=1` for every gadget, together with
nonnegative unit-bounded flows, are equivalent to the original flow constraints
on this canonical graph. Simplex constraints and product nonnegativity are
checked explicitly. All observations on either gadget arc or the bypass are
included in the profile reduction.

The four observation categories correctly give the conditional arc-a interval:
fixed to `u_j` for A/T, fixed to `w_j-v_j` for B, and `[0,w_j]` for U. The
accumulated aggregate right side is
`R=x_a-sum_{A union T}u_j+sum_B v_j`. Both subset inequalities use the correct
sign and category sets. Bypass observations enforce `w_j=lambda_j-z_hj`.
The residual state is included in the same profile, always as an unobserved
state for the original observation model.

Grouping a row by its smallest right side is exact. If a positive circuit is
violated, its selected original rows remain valid regardless of which row
would minimize its group at another point. Their positive combination cancels
the entire profile and produces a globally valid original-variable inequality.
The implementation separately checks the zero normal. It returns a strictly
violated cut, not merely an active expression at the candidate.

The exact RREF circuit enumeration is complete: a one-dimensional kernel with
every entry positive defines a positive minimal dependence. Setting its free
entry to one cannot lose a positive ray. Denominator clearing and gcd reduction
produce primitive integer coefficients. Each support is visited once. Counts
for one, two, and three total states are 1, 5, and 41, as in the independently
verified theorem computation.

Recovery enumerates bases containing the always-valid profile-sum equality.
The profile polytope is bounded by `0<=w<=lambda`; if nonempty, it has a vertex.
At a vertex the sum equality can be extended to a basis using `d-1` other
present subset normals, including in degenerate lower-dimensional cases.
The enumerated exact inverse therefore finds a feasible profile. Checking it
against all tight grouped rows checks all original profile rows. Greedy filling
of the U intervals then exactly recovers each gadget aggregate. Zero-weight
coordinates have zero profile and zero state flows and are never divided by
the decomposition accessor.

## Correction found and retested

Initially, observation indices were range-checked but not type-checked. A
fractional index such as `(0.5,0)` could pass validation and then be silently
absent from all gadget categories. The author added integer checks for both
indices to `FlatChainSimplex` and to the existing `NetworkSimplex` constructor.
The independent suite now verifies rejection of fractional arc and state
indices. This was an input-contract error, not an error in the hull theorem.

## Independent executable verification

Added
[`verify_flat_chain_implementation.py`](../code/network_simplex_review/verify_flat_chain_implementation.py).
Run:

```sh
python code/network_simplex_review/verify_flat_chain_implementation.py
```

The suite does not use the author's profile builder, full-EF benchmark, or
existing tests to establish hull membership or global cut validity. It uses:

- A direct mixture LP over all directed-path/simplex vertices for chains with
  1, 2, 3, and 5 gadgets.
- An **exact** independent global cut maximization for every rejected point,
  including chains with 40 gadgets. At a fixed simplex vertex, collect the
  objective coefficient on each arc. The maximum over base-flow vertices is
  the larger of the bypass coefficient and the sum, over gadgets, of the
  larger of its two arc coefficients. This certifies the cut on the entire
  graph hull without enumerating exponentially many paths or using an LP.
- Exact verification of each positive-weight decomposition flow, including
  capacities, common branch flow, aggregate flow, and every observed product.

The final run checks 293 random in-domain candidates for `m=0,1,2` and
`L=1,2,3,5,40`. Among them are 186 accepted exact decompositions, 45 positive
circuit cuts, 16 zero-row cuts, and 46 product-nonnegativity cuts. There are
233 direct path-hull LP comparisons. Every one of these membership decisions
also has independent exact evidence: either the verified decomposition or a
strictly violated globally valid cut.

Additional checks cover 600 domain violations, a two-gadget example whose
individually feasible state observations force incompatible shared profiles,
six complete-observation cases with all flow on the bypass or all flow on the
chain, zero explicit and residual weights, and fractional-index rejection.
Every enumerated profile-basis inverse is checked exactly. All circuit supports
are distinct positive dependencies; their counts match the independently
established 1/5/41 totals. Every returned cut obeys the theorem's conservative
flow/product coefficient bound for its state count.

Recorded output:

```text
{'direct path-hull comparisons': 233,
 'domain: flat chain flow balance': 180, 'domain: flow bound': 180,
 'domain: simplex nonnegativity': 120, 'domain: simplex total weight': 120,
 'exact accepted decomposition': 186, 'extreme-profile exact decomposition': 6,
 'flat profile positive circuit': 45, 'flat profile zero row': 16,
 'product nonnegativity': 46, 'structured shared-profile contradiction': 1,
 'verified circuit count d=1': 1, 'verified circuit count d=2': 5,
 'verified circuit count d=3': 41}
PASS: independent path-hull membership, exact global cuts, exact state-flow reconstruction
```

## Complexity and practical interpretation

The implementation has linear dependence on chain length at fixed simplex
dimension. Dense tuple construction for every singleton row may contribute
`O(d^2 L)` work when treating `d` as variable; the code should not be described
as attaining a uniform `O(dL)` row-construction bound. Circuit and profile-basis
enumeration have exponential dependence on state count and are intended for
few-state models.

The circuit library is cached by `d` and is initialized by the first model
constructor using that dimension. The profile-basis cache is separate and is
initialized on the first call requesting decomposition. Thus a benchmark must
distinguish cold constructor, cold reconstruction, and warm online calls.
Observation sorting is another constructor cost. `decompose=False` avoids the
profile-recovery and flow-construction work.

The exact-rational interface still needs a separate numerical feasibility and
cut-rounding policy before use with floating-point solver iterates. Timings
against the full and compressed formulations are a separate benchmark task.
