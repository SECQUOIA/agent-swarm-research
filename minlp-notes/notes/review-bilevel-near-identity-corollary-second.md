# Second audit: arbitrarily small coupling in the conditioned box hardness theorem

Date: 2026-09-05. Reviewer: `noncommutative_rank_review`.

**PASS.** Checked the proposed section 7 against [the complete base proof](../results/bilevel-well-conditioned-box-exact-hardness.md). No correction is required.

For `theta_new=min(theta,eta/(10C))`, the geometric row and column bounds remain valid and give `||B||_1,||B||_infinity<=eta/5`. The identity `Q-I=-B-B^T+B^TB` then bounds both induced norms by `2eta/5+eta^2/25`. Since `0<eta<=1`, this is at most `11eta/25<eta`. The spectral norm is bounded by the geometric mean of these induced norms. Thus all three strict inequalities follow.

Decreasing `theta` preserves every use of its original upper bound. In the relative-coordinate argument, `P,T,M,C` are unchanged, while the entries of `U` and the bounds involving `theta^2` decrease. Rebuilding `S` and `delta=s_N` therefore preserves the relative error bound and the yes/no gap relative to the new `delta`. The network point remains inside the unit box. The inequalities `delta/s_i<=1` and the original coefficient magnitude bounds also remain valid.

Strict diagonal dominance follows directly from

```
Q_ii-sum_(j!=i)|Q_ij| >= 1-||Q-I||_infinity > 0.
```

This remains strict at `eta=1`; it does not require an unmentioned strict upper bound on `eta`.

Rational minimum, matrix multiplication, and powers through order `N` preserve polynomial encoding length in the formula size and the binary encoding length of `eta`. This is the correct input-size qualification for arbitrary rational representations. The smaller rational threshold and precision remain polynomially encoded in those inputs. No constant-gap consequence follows.

The diagonal boundary is also correct under the same model restrictions. With positive diagonal `Q`, each follower coordinate is `clip(-(c_i+D_i x)/Q_ii)`. For fixed leader dimension, the threshold arrangement has polynomially many cells, including degenerate cells. The follower response and upper objective are affine on each closed cell, so exact LP and exact rational comparison solve the global problem in polynomial time. This comparison retains the absence of follower-dependent upper constraints.

This is a mathematical review of the corollary. The base theorem's source assessment and novelty qualifications remain unchanged.
