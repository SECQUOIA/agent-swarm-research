# Independent review: arbitrary switching budgets and many modes

Date: 2026-09-04. Target:
[`notes/cia-many-mode-switching-investigation.md`](cia-many-mode-switching-investigation.md).
This is an independent agent review, not external peer review.

**Verdict:** The dimension-free continuous value `sup_n F_{n,s}(T)=T/(s+1)` is
correct for every integer `s≥0`. The explicit integral-flow proof is valid. Its stronger
finite-mode comparison follows directly from a verified published CIA result. The note's
assessment as a useful consequence of established rounding theory, without a major
novelty claim, is appropriate.

## Upper bound

Set `m=s+1` and `h=T/m`, and form the relaxed allocation averages over these `m` equal
blocks. They are simplex columns even for arbitrary measurable original controls.
For each mode, let `S_{i,k}` be its cumulative average allocation through block `k`.

The proposed flow network is correctly oriented: a supply of one enters from block
node `j` into the chosen mode node `(i,j)`; mode-chain arcs run forward in time and
therefore carry cumulative, not future, assignments. Bounds
`floor(S_{i,k})≤flow≤ceil(S_{i,k})` on the outgoing chain arc are integral. Fractional
assignment values and chain flows `S_{i,k}` provide a feasible fractional flow. The
sink's demand is the integer `m`. Network-flow integrality then gives an integral
feasible flow; each block's assignment is exactly one binary selection.

This proves all prefix floor/ceiling bounds simultaneously. If a target prefix is
integral, its error is zero; otherwise either permitted integer differs from it by
strictly less than one. Since there are finitely many modes and block endpoints, the
maximum endpoint discrepancy is strictly less than `h` for each fixed input.

The construction assigns a constant mode to each block and therefore makes at most
`m−1=s` switches. On a block, the selected mode's cumulative discrepancy has derivative
`α_i−1≤0` almost everywhere, and every other mode's discrepancy has derivative
`α_i≥0`. These absolutely continuous functions are monotone. Their absolute values
cannot exceed the maximum of their two endpoint values. Consequently the endpoint
bound controls the entire horizon even when the relaxed data vary arbitrarily inside
blocks. This monotonicity is essential; endpoint approximation alone would not suffice
for a general time-dependent coefficient multiplying the control discrepancy.

No arbitrary-precision integration or oracle complexity is hidden in the existence
argument. An implementation needs the block integrals to be available. The finite flow
network itself has `O(n(s+1))` nodes and arcs.

## Lower bound and exact supremum

For uniform input `α_i=1/n`, any competitor with at most `s` switches has at most
`s+1` constant blocks. One block has length at least `h`. At its endpoint `t`, the
selected component's cumulative occupation is at least that block's length, including
any occupation on earlier blocks. Its negative discrepancy is therefore at least
`h−t/n≥h−T/n`. This gives

```
h−T/n ≤ F_{n,s}(T) ≤ h.
```

Letting `n→∞` proves the exact supremum over all finite mode counts. The lower bound
may be negative for small `n`; that does not affect the argument. The degenerate case
`n=1` has error zero and also satisfies the upper bound. The proof works for `s=0`.
It does not claim that a fixed finite `n` attains the dimension-free supremum.

## Verified published stronger bound

The precise direct source is Zeile, Robuschi, and Sager, *Mixed-integer optimal control
under minimum dwell time constraints*, [Corollary 1, Section 5.2](https://link.springer.com/article/10.1007/s10107-020-01533-x).
It states the unrestricted CIA upper bound

```
θ* ≤ [(2n−3)/(2n−2)] Δbar.
```

I checked both the publisher's full text and text extracted directly from the local
original PDF. The source is at
[[zeile2020-mixed-integer-optimal-control-under]] p.17, printed page 669. The upper
bound applies to any grid and relaxed input. Its following condition `N≥n−1` concerns
sharpness of the bound, not its validity. This distinction matters when the coarse grid
has only `m=s+1<n−1` blocks.

Apply Corollary 1 to the coarse block averages, with spacing `h=T/(s+1)`. The resulting
integer control uses at most `s` switches and has endpoint error at most
`[(2n−3)/(2n−2)]h`. The same within-block monotonicity transfers that error bound to
the original measurable relaxed control. Hence the stronger comparison

```
F_{n,s}(T) ≤ [(2n−3)/(2n−2)] T/(s+1),  n≥3,
```

is a valid direct consequence of the literature. No limit through increasingly fine
grids is needed. The note should cite Corollary 1 directly rather than only its
antecedent Theorem 2 and Proposition 1; this source refinement was sent to its author.
The flow argument remains useful as a self-contained proof of the weaker dimension-free
bound and does not establish a new sharp finite-mode upper constant.

Finally, with fixed `s`, expansion of the previously verified uniform expression gives
`[T/(s+1)] [1−(s+2)/(2n)+O(n^−2)]`; expansion of the published coefficient gives
`[T/(s+1)] [1−1/(2n)+O(n^−2)]`. Both asymptotic expressions in the note are correct.
Determining the sharp finite-mode correction for budgets at least two remains a separate
research question.
