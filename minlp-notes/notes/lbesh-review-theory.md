# Independent review of the LB-ESH mathematical development

Date: 2026-09-19. Reviewer: fresh agent `/root/review_theory`, which did not
write the development note. Scope: mathematical claims in
[the theory note](lbesh-development-theory.md), consistency with
[the literature assessment](lbesh-development-literature.md), and limited
inspection of `lbesh/solver.py` for correspondence. This is not an independent
implementation or benchmark certification.

**Final verdict:** the derivations are sound under the stated exact
arithmetic, compactness, and oracle assumptions. Four precision corrections
concerning the empty-disjunct closure convention and the single-tree
termination and objective-gap contracts were incorporated and independently
rechecked. No unresolved mathematical defect was found. The results
establish a useful, carefully qualified
synthesis; they do not establish a new cut family or, by themselves, a strong
publication contribution.

## Independent mathematical checks

| Claim | Review result and essential qualification |
| --- | --- |
| Perspective tangent identity | Differentiating `lambda*g(nu/lambda)` gives coefficients `(grad g(z), g(z)-grad g(z)·z)`; the constant cancels. Correct. |
| Completeness | Convexity gives every tangent below `g`; selecting `z=p` attains equality. Scaled box bounds force `nu=0` at zero weight. Correct as the closed-perspective inequality formulation, with the empty-term convention discussed below. |
| Per-disjunction hull | Dividing each positive block by its weight and recombining proves both inclusions for bounded convex term sets. The note correctly distinguishes independent-disjunction hulls from the convex hull of their intersection. |
| ESH uniform separation | At the boundary, the supporting inequality at the anchor gives `a·(p-anchor) >= delta/s`. Lipschitz continuity gives `1-s >= g(p)/(LD)`, yielding the stated margin. No maximizing directional subgradient is required. |
| Subgradient extension | The same supporting inequality holds for every selected subgradient. A uniform bound on all selected subgradients supplies the Lipschitz and normal bounds. The open-neighborhood and gradient-bound assumptions avoid the lower-dimensional-box pitfall. |
| Integral finite separation | For a fixed row, any later candidate activating that same disjunct must satisfy its previous cut. Cauchy–Schwarz gives a positive minimum distance. Compactness and finitely many rows complete the packing argument. Activity of other disjuncts does not invalidate this subsequence argument. |
| Fractional finite separation | A residual above `epsilon_p` gives a transformed violation at least `epsilon_p` for ECP, or `epsilon_p*delta/(LD)` for ESH. The coefficient bound is independent of the weight. Compactness in `(nu,lambda)` supplies the same packing result. |
| Residual-derived weight threshold | Since `r <= lambda*U_r`, skipping when `lambda*U_r <= epsilon_p` is valid. Every genuinely violating block has denominator above `epsilon_p/U_r`. The upper bound must be valid, and tolerances remain representation-dependent. |
| Fixed weight cutoff | A completed checked-row pass gives `r <= max(epsilon,tau*U_r)`. No certificate follows merely from a stall or iteration limit. Correct. |
| Geometric repair | Substituting the convex combination in (6) bounds every nonlinear row by zero; affine rows and the box are preserved. Weighted triangle inequality gives (7). This needs nonempty terms and common strict margins for their nonlinear rows. |
| Intersection counterexample | For `x^2-y<=0`, `y<=0`, and `x,y>=0`, the exact point is `(0,0)`, while `(sqrt(epsilon),0)` has residual `epsilon` and objective error `sqrt(epsilon)`. It disproves a linear error rate from disjunct Slater margins alone. |
| Value convergence | Vanishing continuous residuals and compactness make every cluster point feasible. Valid master bounds and vanishing master optimality errors force objective convergence. This proves no rate and no finite exact termination. |
| Epigraph compactness | A tangent gives a finite lower bound. An upper bound on `f` preserves an optimal lift for every original feasible point when the artificial epigraph variable has no other role. The distinction between objective equivalence and preserving the entire unbounded epigraph is correct. |
| Single-tree conclusion | Conditional on a complete master solver, retained cuts, old-cut-feasible generating points, finite optional separation work, and original-point validation. These are substantive assumptions, not consequences of using a callback API. |
| Arithmetic allowance | Relaxing an approximate cut by its uniform error bound `E` preserves validity. The generating violation loses at most `2E`, and allowable stored-cut violation loses an additional `rho`. The stated positive-margin requirement is correct. |
| ESH/ECP non-dominance | Nonparallel halfspaces have witnesses on both sides. The literature note's explicit disk witnesses satisfy the claimed opposite inequalities. Setting the indicator to one preserves the example. |
| Representation invariance | At a common exact boundary point, the chain rule scales the normal by positive `phi'(0)`. The result needs the same anchor and exact root; it does not make stopping rules or interior-point computation invariant. |
| Exponential recurrence | Solving the tangent inequality gives (9). Its upper bound decreases and stays strictly above one, so previous cuts do not determine the next master optimum. A decrement below `1/a` proves `k>a(1-eta)`. This counts master separation steps, not function evaluations or time. |

For the nonsmooth ESH claim, the critical inequality is immediate from
`g(anchor) >= g(z)+a·(anchor-z)` for any subgradient `a` at `z`.
Since `g(z)=0` and `g(anchor)<=-delta`, every such `a` has a strictly
positive radial component. A counterexample based on choosing a subgradient
with zero radial component cannot satisfy the strict-anchor premise.

## Corrections requested during review

1. **Empty terms and zero-weight closure.** If `g=1` on the box, the
   positive-weight feasible lift is empty. Its closure is also empty, but
   the closed-perspective row `lambda<=0` together with nonnegative weight
   admits `(nu,lambda)=(0,0)`. Thus the latter is the correct inactive-term
   convention, but it cannot unqualifiedly be called the closure of the
   positive-weight feasible lift. This is a terminology/assumption issue,
   not a failure of the all-tangents identity or the GDP formulation.
2. **Old lazy cuts.** A callback candidate can violate an earlier lazy cut.
   Re-enforcing it does not by itself justify packing newly generated cuts
   at that same candidate. Count fresh separation iterations only at
   old-cut-feasible points, and require old-cut repetitions to resolve in
   finite time.
3. **Optional fractional callbacks.** A finite bound on integer rejection
   cuts does not alone bound arbitrary fractional user-cut generation.
   Require a finite cap, the fractional uniform-separation contract, or
   state the termination theorem for the configuration without user cuts.
4. **Positive objective gaps.** A bound `U-B<=eta` for positive `eta`
   proves feasible `eta`-optimality. Exact optimality in exact arithmetic
   requires a zero gap. Contract 4 should preserve this distinction.

All four findings were communicated directly to the author and the lead
agent. They do not undermine the principal perspective identity or the
multi-tree separation theorems.

## Implementation correspondence and publication scope

The inspected solver uses ESH line search with the full affine tangent
constant and an ECP fallback. It checks original incumbents numerically and
records LP exits. It still uses fixed weight thresholds rather than the
residual-derived threshold theorem. No certified derivative/evaluation error
bound was observed. The development note appropriately separates its oracle
contracts from ordinary floating-point code. The theory cannot be used as a
blanket claim of exact numerical certification of that implementation.

The distinction between known synthesis and new contribution is essential.
The perspective coefficients are established; the boundary oracle is
established; compactness packing is a standard convergence mechanism. The
residual bounds, repair calculation, counterexample, and representation
diagnostic are useful derivations but no priority claim has been established.
The literature note's narrower framing is appropriate. Independent primary
source checks confirmed that [Serrano, Schwarz and Gleixner](https://arxiv.org/abs/1905.08157)
identify supporting-hyperplane separation with Kelley separation of a
reformulation, that [Bestuzheva, Gleixner and Vigerske](https://arxiv.org/abs/2103.09573)
study perspective cuts in a general branch-and-cut solver, and that
[Kronqvist and Misener](https://optimization-online.org/wp-content/uploads/2020/08/7957.pdf)
already combine ESH with disjunctive strengthening and discuss avoiding
perspective numerical difficulties. These sources support caution about
novelty; they do not prove identity of the complete implementations.

## Targeted verification record

The reviewer independently reconstructed the proofs above and ran one
`python -` arithmetic check using Python 3.13.11 and only the standard
library. It verified
the two explicit non-dominance witnesses, the exponential tangent equation,
strict monotonicity, and the iteration lower bound at `a=2,4,10,100`.
For geometric tolerance `eta=0.1`, the respective ECP counts were
`3,5,10,91`, versus one exact ESH cut. The intersection counterexample at
residuals `1e-2,1e-4,1e-6` gave objective-error/residual ratios
`10,100,1000`. These calculations corroborate the algebra; the proofs do
not depend on numerical tests. No solver runs, new dependencies,
project-wide checks, or CI inspection were used.

## Final revision check

The author's revision resolves all four requested corrections. Section 1
now explicitly distinguishes the inactive origin from the closure of an
empty positive-weight feasible lift and defines `S_ik subseteq P_ik
subseteq C`. Section 7 explicitly requires old-cut-feasible generating
points and finite resolution of old-cut repetitions. Its new contract 5
disables, caps, or places a uniform-separation contract on optional
fractional cuts. Contract 4 and the following conclusion distinguish
exactly feasible `eta`-optimality from zero-gap exact optimality.

The final independent reread covered each changed passage against the
proofs. SHA-256 of the reviewed theory note:
`7f1a0d0ee7c9d5719bcc58755dab9ba7961205730e61a2c070ecae8b1508909e`.
The finding is mathematical readiness for the qualified claims in that
note. It is not a claim that a distinctive strong-publication contribution
has been established, or that the floating-point implementation satisfies
the stated exact or certified-arithmetic contracts.
