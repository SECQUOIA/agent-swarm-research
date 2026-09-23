# Weighted potential optimization on cacti at fixed objective support

Date: 2026-09-06. Status: theorem obtained by composing the reopened structural and approximation results; independent review records are linked below. The [completed focused source comparison](../notes/potential-flow-reopened-weighted-literature.md) found no inspected matching combined theorem; priority remains provisional. No novelty is claimed for the individual approximation or real-algebraic tools.

## Theorem

Fix an integer `p`. Let `G` be a connected cactus with fixed positive rational asymmetric quadratic edge laws

```
g_e(x)=beta_e^+ x^2  (x>=0),
g_e(x)=-beta_e^- x^2 (x<=0).
```

Let nominations range over a nonempty rational box intersected with exact total balance. Let `c` be a rational vector with `sum c=0` and at most `p` nonzero entries. Given a positive rational tolerance `epsilon`, the maximum and minimum of `c^T pi` can be enclosed in rational intervals of width at most `epsilon`, and a rational feasible nomination with objective within `epsilon` of the respective optimum can be computed in time polynomial in input bit length and requested accuracy bits, for fixed `p`.

The number and length of cycle blocks, and thus the total cycle rank, are unbounded. The polynomial exponent may depend on `p`; no fixed-parameter tractable running time or practical implementation of the full exact algorithm is claimed. Resistances are fixed. Additional operating constraints do not filter the uncertainty set. Exact equality-sensitive comparison of the optimum with a rational threshold is not claimed.

This result closes the fixed-law cactus part of [the previously unresolved weighted bounded-block direction](../notes/potential-flow-bounded-block-weighted-obstruction.md). The [earlier weighted theorem](potential-flow-fixed-support-global-rank.md) allowed joint resistance intervals but required bounded global cycle rank. The present theorem trades that resistance freedom for unbounded total cycle rank on cacti; neither theorem contains the other in full.

## Why the proof works

The [weighted nomination-face reduction](../notes/potential-flow-reopened-weighted-face-reduction.md) constructs a polynomial family of reduced nomination faces, each with `O(p)` free coordinates, containing a global maximizer on at least one face. The reduction first removes objective-free pendant subnetworks and contracts a block when every induced objective coefficient sum at its ports is zero. Both operations preserve attainable objective values and allow rational nomination disaggregation.

In the remaining support-spanning block tree there are `O(p)` special blocks and ordinary chains. The electrical adjoint sends a fixed nonzero current along every ordinary chain. Strict terminal ordering and the single balance multiplier restrict free nominations to at most one block per chain. After fixing this coarse face, the positive-source potential perturbation inside the selected blocks leaves at most two free nominations per suppressed path. This two-stage construction avoids disturbing the chain argument and gives only `O(p)` free coordinates on a cactus. Uniform smoothing and perturbation limits preserve a maximum on one of the closed faces.

Each retained face is a compact rational polytope of fixed dimension, and the nominations are rational affine functions of its coordinates. The [affine-load cactus optimizer](../notes/potential-flow-reopened-weighted-investigation.md) optimizes an arbitrary weighted potential objective over precisely this kind of parameter family. Its local cycle equations are quadratic after fixing flow signs. Local drops are polynomial plus affine-times-square-root terms, or rational functions on a nonsingular branch; an all-zero-flow branch handles the remaining degeneracy explicitly.

Uniform rational piecewise-polynomial approximations of the square root have polynomial size in the requested accuracy bits. Their discriminant-panel boundaries, together with exact local branch domains and bridge sign boundaries, produce a polynomial common semialgebraic partition in fixed parameter dimension. On each cell the sum is a rational function of polynomial degree and coefficient encoding. Fixed-dimensional real-algebraic optimization then computes a certified approximate global value without exact comparison of sums of independent radicals. An explicit global nomination-to-potential Lipschitz bound permits rational linear-programming recovery inside the original face, even if rounding crosses a local branch boundary.

Optimize every face to a suitable fraction of the requested tolerance, retain the best certified candidate, and disaggregate all reduced nominations rationally. Objective preservation gives the original-network guarantee. Replacing `c` by `-c` gives the minimum.

## Practical interpretation and remaining boundaries

The theorem handles a small number of pressure measurements or pressure-difference terms over a large cactus network with independent uncertain nominations. It establishes accuracy-bit tractability for their weighted aggregate despite arbitrarily many interacting uncertain block loads. The main algorithm is theoretical; implementing fixed-dimensional semialgebraic optimization at useful scale remains a separate engineering problem.

The underlying affine-load theorem also handles any number of objective terms when the load uncertainty itself depends on a fixed number of affine factors. That theorem has an exact local-capacity extension with algebraic feasible output. Those capacity constraints cannot simply be added here: they invalidate the objective-preserving block contraction and the nomination-face argument. The separate [joint weighted cactus theorem](potential-flow-joint-weighted-cactus-accuracy-bits.md) now handles independent resistance intervals for symmetric quadratic laws. General bounded-rank blocks remain an open algorithmic extension. That joint theorem and the present fixed asymmetric-law result have distinct assumptions.

## Verification

The structural proof has a [second independent mathematical audit](../notes/review-potential-flow-reopened-weighted-faces-second.md). The affine-load proof and local-capacity corollary passed a [separate independent full mathematical audit](../notes/review-potential-flow-reopened-weighted.md). The composition itself only uses the structural lemma's rational fixed-dimensional face output as input to the affine-load theorem; no new approximation assumption is added.

[`reopened_weighted_checks.py`](../code/potential_flow_mpd/reopened_weighted_checks.py) verified 360 square-root sample bounds using exact rational arithmetic, including all panel endpoints and zero regions at four precision levels. It also compared 1,200 local asymmetric-cycle formulas against independent monotone root finding, covering positive, negative, and zero quadratic coefficient cases, with maximum circulation discrepancy `2.84e-14`. These checks support the new approximation and local representation mechanisms; they do not implement the global optimizer or replace the proofs.
