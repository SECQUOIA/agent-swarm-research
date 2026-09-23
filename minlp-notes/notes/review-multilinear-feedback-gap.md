# Independent audit of the feedback-variable multilinear gap bound

Date: 2026-09-04. Reviewer: independent `review_extension` agent.

Reviewed result: [A feedback-variable gap bound, sharp for one deleted
variable](../results/positive-multilinear-feedback-gap.md), including the
later extension to finite boxes with nonnegative lower bounds.

Verdict: the bound `tbtgap<=2^f chgap` is correct. The common marginal-law
construction, residual repair, conditional forest gluing, general-box
extension, and sharp one-variable example all pass. Only a boundary wording
correction was requested: for `f=0`, the gaps coincide; their ratio is one
only where the common gap is positive.

## Universal domination

The construction uses one uniform variable and all `2^f` left/right choices
for the feedback-variable thresholds, with each remaining variable using
its left threshold. Every coordinate has its prescribed mean. For a fixed
feedback state and an outside-variable state, choose the feedback orientations
so that all the corresponding literal events share the same endpoint as
the outside literal. Their intersection then has probability equal to the
minimum of the individual literal probabilities. Since that orientation
has weight `2^-f`, its contribution proves the stated lower bound on the
master marginal law.

Every other joint law with the same singleton means assigns to that cell
at most this minimum. Thus the domination is simultaneous over all proposed
local laws and all outside variables; the master law is not chosen anew
for each factor. The analogous feedback-only inequality follows directly
by aligning feedback literals, without requiring an outside variable.
For an empty feedback set, its sole state has probability one and the
outside marginal domination is equality.

Endpoint means zero or one cause no problem. Zero-length literal events
give a zero comparison bound. Threshold endpoints have zero probability
under the continuous uniform variable.

## Residual repair

Set `lambda=2^-f`. For each local law `P_e` on all feedback variables and
the factor's outside variables, the residual mass at state `s` is
`h_s=Q_F(s)-lambda(P_e)_F(s)>=0`. Each prescribed residual pair marginal
`Q_i(s,b)-lambda(P_e)_(F,i)(s,b)` is nonnegative, and summing it over `b`
gives exactly `h_s`, independent of `i`. Therefore, conditional independence
of the outside variables realizes all these pair marginals simultaneously.

When `h_s=0`, both residual probabilities for every involved outside
variable are zero, and no residual mass is placed there. If the factor has
no outside variables, assigning just `h_s` to the feedback state is the
required construction. The total residual mass is `1-lambda`, including
the zero residual when `f=0`.

Adding the retained measure `lambda P_e` yields a probability measure
`P'_e` that dominates it pointwise and has master feedback and
feedback/outside marginals. In particular it preserves every singleton
mean, including feedback variables that were absent from the original
factor. The original local law can always be extended to those missing
feedback variables independently with their prescribed means.

## Forest gluing

Condition on a state with `Q_F(s)>0`. All conditional factor distributions
agree on every shared outside variable, because the common conditional
singleton law is `Q_i(s,b)/Q_F(s)`. In a factor-variable incidence tree,
traversal from a root factor introduces each new factor through exactly
one previously sampled variable. If it met a second sampled variable,
there would be an incidence cycle. Sampling its remaining coordinates
from the corresponding conditional factor law therefore preserves both
the old and the new factor marginal.

Zero-probability separator values are not reached under this construction,
so arbitrary choices on such null conditions do not affect a marginal.
Isolated outside variables are sampled from their master conditional
singleton distributions. Factors consisting only of feedback variables
add no outside variables. Feedback states of zero master probability are
omitted; domination forces every local repaired measure to assign them
zero mass as well.

After averaging over `Q_F`, every factor's full marginal is exactly its
repaired law. Hence the expectation of each nonnegative local function is
at least `lambda` times its expectation under the original local law.
There is only one loss factor; gluing does not multiply it along paths.

The acyclicity hypothesis concerns deletion of variable nodes only. The
proof does not extend it to deletion of an arbitrary mixture of factor
and variable nodes or to unrestricted incidence treewidth.

## Gap identities and nonnegative boxes

For a unit-box monomial, take an anchor whose prescribed mean is smallest.
The binary function `X_anchor-product_(i in e)X_i` is nonnegative on every
vertex. Its largest possible expectation is the concave monomial value
minus the convex monomial value, namely the exact local term gap. Positive
monomials share a comonotone maximizing distribution, so the sum of their
concave values is the concave envelope of the sum. These facts justify
the global deficiency identity and the desired gap bound.

The general-box extension preserves the original factor scopes. After
removing fixed coordinates and normalizing, each original monomial is a
positive linear combination of subproducts. Replacing each subproduct by
one of its minimum-mean coordinates produces an affine majorant that is
valid on every binary vertex. Its expectation equals the original
monomial's concave-envelope value because one comonotone law attains all
the subproduct upper bounds simultaneously.

Subtracting the original local monomial from that affine majorant gives
a nonnegative local function on the same original scope, whose largest
local expectation is exactly the original term gap. The previously
proved coupling theorem applies without turning the subproducts into
new factor nodes. This avoids an invalid change of incidence structure.
The expansion may be exponentially long; it is used for existence and
does not establish a polynomial-time construction in arbitrary degree.
Nonnegative lower bounds are essential to this positive-expansion proof.

## Sharpness with one feedback variable

For `p_n=a sum_i x_i+product_i x_i` at means `a=1/n` and `x_i=1-1/n`,
the sum of the bilinear term gaps is one, and the last monomial's gap is
`1-1/n`. Thus the term gap is `2-1/n`.

Let `R` count failed leaf variables. Its mean is one. The total deficiency
is `E[AR]+Pr(R>=1)-1/n`. The pointwise inequality
`AR+1[R>=1]<=R+A` is valid for both values of `A`; expectation therefore
bounds the hull gap by one. Selecting exactly one failed leaf uniformly
and sampling `A` independently attains that bound with every prescribed
mean. Hence the exact ratio is `2-1/n`.

Deleting the anchor-variable node leaves the stated incidence tree.
The displayed size-three bags form a valid tree decomposition: the anchor
and central factor occur along the entire bag path, each leaf variable
occurs in its path bag and attached factor bag, and each bilinear factor
occurs in its own leaf bag. All incidence edges are covered. A cycle
exists when `n>=2`, proving treewidth exactly two. The upper bound applies
to the one-variable deletion class; the example alone does not prove it
for all incidence-treewidth-two hypergraphs.

## Sharpness of the generic nonnegative-payoff lemma

The author's later scope example also checks out. Give the `f` feedback
variables and one outside variable mean `1/2`, and use one indicator payoff
for every full state `(s,b)`. Each payoff has local maximum expectation
`1/2`, while the sum of all `2^(f+1)` indicators is identically one. Thus
the sum of local maxima is `2^f` times the global maximum, showing that
the generic coupling guarantee cannot improve its factor.

If factors must have distinct genuine scopes, multiply each indicator by
its own private binary variable with prescribed mean one. All such variables
equal one almost surely, preserving both values; they make the formal
payoff scopes distinct and leave a subdivided star after feedback-variable
deletion. Indicators involving zero literals are not positive-coefficient
monomials. This example therefore does not settle the dependence on `f`
for the positive multilinear theorem itself.

## Verification and prior-art boundary

[audit-multilinear-feedback-law.py](../code/audit-multilinear-feedback-law.py)
independently checks the master law with exact rational arithmetic. For
`f=0,1,2,3`, it exhausts respectively `5,25,125,625` mean vectors on the
quarter grid, including endpoint means. Every law normalized correctly,
had all required singleton means, and satisfied every feedback and
feedback/outside domination inequality. These finite checks supplement
the proof; they do not replace it.

The classical zero-feedback case was verified in the primary manuscript
[Buchheim, Crama and Rodríguez-Heck, *Berge-acyclic multilinear 0–1
optimization problems*](https://orbi.uliege.be/bitstream/2268/204059/1/article_perfect_SL_version5.pdf).
It characterizes exact standard linearization by Berge acyclicity.
Conditioning and gluing on a forest are also established methods. This
review verifies the new quantitative argument but does not establish
publication priority for the feedback-dependent bound or its sharp case.
