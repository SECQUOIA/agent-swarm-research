# Independent review of the analytic three-block reach theorem

Reviewed 2026-09-04 by a separate research agent. This is an independent agent review,
not external peer review. The reviewed proof is in
[the exact two-switch result](../results/cia-exact-two-switch-worst-case.md).

**Outcome: the analytic distinct-mode reach theorem is correct for every `n>=4`.**
The aggregate estimate, the treatment of flat portions, and the final contradiction
have no unresolved mathematical issue in this review. The argument supersedes the
computer-assisted four-mode proof as a proof of the positive result. The earlier exact
certificates remain useful independent checks.

## Reach endpoints and boundary cases

For continuous nondecreasing `F_i(t)=t-A_i(t)`, the feasible endpoint set on `[0,L]` is
closed. It contains the starting time `b`, because `F_i(b)<=b<=b+E`. Thus its maximum
exists. Under the contradiction assumption that no sequence of at most three distinct
modes reaches `L`, every first and second reach is strictly below `L`.

At an uncapped latest feasible endpoint, continuity gives equality with the threshold.
This remains true when `F_i` has flat portions: the endpoint is the rightmost point of
the feasible sublevel set. At any later time the threshold is strictly exceeded.
Consequently all pair bounds at `M` and `M_i` used in the proof are valid, and the final
inequality `F_i(L)>M_i+E` is strict. No differentiability, strictly positive mode weights,
or uniqueness of a threshold root is assumed.

The chosen horizon `L=min(T,B_3)` handles truncation. A first or second reach attaining
`L` already proves the desired conclusion, so the uncapped identities are used only in
the remaining case. Ties among first reaches or maximizing pairs cause no problem;
one can choose any maximizing indices.

## Sorted first reaches

Let `x>=y>=z` be the three largest first reaches. At time `y`, the largest-reach mode
has allocation at most `x-E` by monotonicity of its allocation; every other mode has
allocation at most `y-E` because its threshold was already reached. Summing gives
`x+(n-2)y>=nE`. The analogous argument at `z` gives
`x+y+(n-3)z>=nE`.

Both displayed linear identities converting these inequalities to (2) and (3) are
exact. Their remainder coefficients are respectively
`(n^2-3n+1)/(n-1)` and `(n^2-4n+1)/(n-1)`. The latter is positive starting at `n=4`;
the assumption `n>=4` is substantive. The exact three-mode counterexample in
[the earlier investigation](cia-distinct-reach-investigation.md) confirms that a
three-block reach theorem without this restriction would be false.

## Excluded-pair aggregate

For each excluded mode `i`, let `x_i,y_i` be the two largest remaining first reaches.
Summing the pair constraints at `M_i` uses the identity

```
sum_{k!=i} max_{j not in {i,k}} R_j = (n-2)*x_i+y_i.
```

This identity is valid with ties. Subtracting the resulting upper bounds for all
allocations except `A_i(M_i)` from the total allocation `M_i`, then using
`A_i(M_i)<=A_i(M)<=M-E-x_i`, gives exactly

```
(n-2)*M_i >= n*E+(n-1)*x_i+y_i-M.
```

For a distinct ordered pair `(p,q)` attaining the global maximum `M`, the same pair
is available after excluding any mode outside `{p,q}`. Hence all those `M_i` equal
`M`, and only two terms require individual lower bounds. The two elementary sorted
bounds used for those terms are valid:

* `x_p+x_q>=x+y`: if an excluded index attains the unique largest reach, the other
  excluded maximum is `x` and its own is `y`; otherwise both maxima are at least the
  required values. Ties only weaken this distinction.
* `y_p,y_q>=z`: deleting one index cannot make the second remaining order statistic
  smaller than the third original order statistic.

The coefficient of `M` after summing is `n-2-2/(n-2)>0` for `n>=4`. Substitution of
the independently derived two-block bound `M>=B_2` is therefore in the correct
direction. With `B_2=nE(2n-1)/(n-1)^2`, direct algebra gives

```
(n-2-2/(n-2))*B_2
  +(2*n*E+2*n^2*E/(n-1))/(n-2) = n*B_2.
```

I also checked this identity symbolically. Thus the central bound `sum_i M_i>=nB_2`
follows without an event-order assumption or a computational certificate.

## Final contradiction and CIA consequence

Appending `i` to a pair attaining `M_i` uses three distinct modes. If every such
sequence stops before `L`, summing its strict failure inequalities gives

```
(n-1)*L > sum_i M_i+n*E >= n*B_2+n*E = (n-1)*B_3,
```

contradicting `L<=B_3`. This completes the independent audit of the reach proof.

The logical combination with the separately reviewed heavy-mode lemma is also
valid. If every mode total is at most `E`, positive discrepancies are automatically
bounded by `E`; for a mode used once, its most negative discrepancy occurs at the end
of its block. Otherwise the heavy-mode lemma applies at threshold `T/4`. The four
pure-mode block lower bound and the uniform-control lower bound match the resulting
upper bound. This review does not replace the separate audit of the heavy-mode lemma.

The added one-sided minimax corollary follows as stated. For uniform controls, the
occupation of the currently used mode at a block endpoint is at least that block's
length, including when a mode is repeated. This gives
`t_j<=n/(n-1)*(t_{j-1}+E)` and the matching three-block lower bound.

The finite constructive procedure counts evaluations of monotone reach maps; it
does not assert a finite arithmetic complexity for arbitrary measurable functions
given without an evaluation representation. Novelty is a separate literature question;
this note establishes mathematical consistency, not priority.
