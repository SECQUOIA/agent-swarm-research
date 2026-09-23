# Independent review of the affine-branching proof barrier

Date: 2026-09-05. Reviewer: independent `spatial_sdp_review` agent.
Reviewed: `notes/spatial-bb-affine-branching-barrier.md`.

**Verdict: PASS for both mathematical obstructions.** This review checks
the stated proof-method limitation, not the separate literature comparison
or the complexity of constant-gap affine-branch certificates.

Under the uniform Boolean distribution, `E[S]=0` and `E[S^2]=n`.
An actual distribution supported on `S>=0` with zero mean must have
`S=0` almost surely, so those moments cannot belong to the half-cube
quadratic moment hull. The normalized affine coordinate `z=S/n` has
`E[z]=0`, `E[z^2]=1/n`; hence its moments violate the valid interval
inequality `z^2<=z`. These arguments hold for every positive integer `n`.
Symmetry of the Boolean distribution gives halfspace probability at
least `1/2`, including the mass on the boundary when `n` is even.

For the substitution lemma, suppose `t<r-1` and `t<ceil(n/2)`.
The second inequality implies `n-t>=t+1` for both even and odd `n`.
If the fixed-sign sum `a` is negative, the constant localizer fails.
Otherwise `a` is an integer in `[0,t]`, so choosing `a+1` unfixed
coordinates is possible. The negative-assignment indicator polynomial
has degree `a+1<=t+1<=r-1`; consequently

```
deg(S p^2) <= 1+2(r-1)=2r-1 <= 2r.
```

Its event has probability `2^(-(a+1))`. On that event, the fixed and
selected coordinates have sum `a-(a+1)=-1`, and every other unfixed
coordinate has conditional mean zero. Thus the exact localizer value
is `-2^(-(a+1))`, as stated. Boolean idempotence justifies replacing
`p^2` by its event indicator inside this actual expectation.

This proves the necessary bound `t>=min(r-1,ceil(n/2))`. For `r=1`
the conclusion is the trivial `t>=0`, with no missing boundary case.
At linear order the necessary substitution count is linear, although
the one-halfspace domain retains at least half the original witnesses.
Therefore the current substitution-cost-to-witness-loss implication
cannot extend unchanged to general affine inequalities.

The note correctly limits its conclusion to this construction. It
does not show that another node pseudoexpectation is impossible or
that affine branching gives a short fixed-gap certificate. Likewise,
refuting perfect satisfiability supplies only a `1/m` normalized
violation bound, which alone does not reach a fixed `1/16` target.
