# Stage 3, round 1 — independent review 3

Reviewed frozen snapshot `process/snapshots/stage03-round01`, including all of
`sections/03-structured-oracles.tex`, its prior-stage dependencies, and the new
bibliography entries. No other current-round reports were consulted. No
manuscript edits or subagents were used.

## Verdict and enumerated findings

**Accept: no major or minor issues identified.**

1. **S03-R1-R3-01 — Verification finding; no correction required.** The
   transportation cut argument is sufficient, the original-coordinate affine
   branch extraction is globally valid, and the rational maximum-flow
   complexity statement distinguishes arithmetic counts from bit complexity.

The claims are properly limited to the specified block classes. In particular,
the manuscript neither extends the planar support argument to arbitrary
dimension nor equates parallel-path blocks with all series–parallel blocks.

## Mathematical checks

### Theta state domains, supports, and Minkowski sums

The sign convention for the third theta path is consistent: its core deviation
is `-s-t`, and negating the path sign permits a common coordinate form `h=s+t`.
Intersecting observations with both endpoint lists forces repeated observations
to agree and handles zero weights without division.

I checked the complete feasibility criterion by intersecting the rectangle's
attainable sum interval with the prescribed `h` interval. The six support
formulas follow by eliminating one coordinate, and their extrema are attained.
This includes point and segment domains.

The planar Minkowski-sum proof treats the relevant degeneracy correctly. An
exposed edge of a two-dimensional sum contains a nontrivial exposed segment
from at least one summand; all such segments must be parallel. A segment
summand has a permitted direction because one defining inequality is tight
through its relative interior. For a one-dimensional sum, the perpendicular
normal pair fixes its line, while another coordinate form fixes both endpoints.
Thus no extra facet direction is omitted by the six-support description.

### Globally valid branches and coefficient magnitudes

Every lower endpoint/support is a maximum of affine expressions and every
upper endpoint/support is a minimum. Each condition becomes a maximum of
affine branches bounded above by zero after rearrangement. An active branch is
therefore globally valid at hull points and has exactly the candidate's
violation; this is not merely a supporting local approximation.

Within a state, a support branch uses either one coordinate type or two
different types. The two aggregate flow representatives are different arcs.
Within a same-type local comparison, a repeated product cancels rather than
doubles. These facts support the unit `x,z` coefficient claim. The manuscript
retains the rational-scaling qualification from Stage 2.

### Theta recovery and compact storage

The reflected suffix sum in the recovery intersection has coordinate bounds
`r_eta - suffix_upper` and `r_eta - suffix_lower`; this sign order is correct.
The six-support lemma describes the suffix exactly. The stated point choice
lies in the intersection: its selected `s` is between the tight bounds, its
selected `t` obeys its own bounds, and the sum either equals the lower `h`
bound or remains below its upper bound by the tight upper restriction on `s`.
Subtraction therefore preserves feasible suffix membership inductively.

Positive-weight normalization, the unused default at zero merged weight, and
the default for an entirely unobserved block agree with the earlier refinement
proof. The number of scalar/vector entries per theta state is constant, so
suffix arrays, exceptions, and defaults fit the claimed linear arithmetic and
storage bounds. Dense expansion is explicitly charged separately. The
observation-grouping proviso and sorting cost prevent an unqualified linear
preprocessing claim.

I also recomputed the three-parallel-arc example. Both individual label hulls
admit the proposed decompositions, but their joint residual first-two-arc sum
would exceed its available weight by `1/3`. The displayed inequality has the
correct sign and violation.

### Transportation sufficiency and separation

For the shifted system, the local inequalities imply nonnegative capacities
and column targets. Applying the complementary subset bound gives the missing
nonnegativity of each row target. The original aggregate zero-sum equation
then yields equality of total row and column targets.

For a source-side row set `S`, assigning a column to the sink side costs
`sum_{i in S} C_ij`; assigning it to the source side costs `c_j`. Columns
choose sides independently. Thus the minimized cut formula is exact.
Adding the lower-bound shift converts its two alternatives into, respectively,
the upper-bound sum on `S` and minus the lower-bound sum on its complement.
This verifies the displayed subset inequality with no omitted capacity term.
All cuts have sufficient capacity exactly when the transportation system is
feasible. If the total target is zero, nonnegative row and column targets all
vanish and the zero shifted flow is valid.

The oracle checks negative row targets before constructing a flow network.
If a maximum flow is deficient, optimizing column sides of its minimum cut
cannot increase the capacity, so its row subset remains violated. The concave
subset right side is a minimum of affine expressions; an active affine
majorant gives a valid inequality and agrees at the candidate. Different paths
and states use different observation coordinates, preserving unit product
coefficients. The `k=3` comparison reproduces the six theta supports after
negating the third path coordinate.

The network size counts include the merged state and both terminals. The
construction bound counts all path/state entries. Edmonds–Karp uses a
capacity-independent polynomial number of shortest augmentations. Clearing
rational denominators gives integers of polynomial encoding length because
the number of capacities and their individual encoding lengths are polynomial.
Updates and flow values remain bounded by the total scaled capacity. Hence the
bit-complexity consequence is justified, without relying on an arbitrary
augmenting-path rule or unit-cost rational arithmetic.

## Independent finite checks and build

The script `verification/reviewer3/stage03-round01/check_domains.py` imports no
repository oracle implementation. It checked:

- All **3,375** theta interval triples with endpoints in `[-2,2]`, including
  **2,487 nonempty** domains, against explicit integer-point enumeration for
  feasibility, all six extrema, and the recovery point choice.
- **120** small transportation systems against exhaustive zero-sum column
  enumeration, testing all subsets on **5,674** aggregate targets, including
  **1,003** feasible targets. Every subset classification agreed.

These integer checks supplement the symbolic reasoning. They are not claimed
as exhaustive verification of rational or arbitrary-sized instances. The JSON
counts and script are retained in the verification directory.

A private build of the entire snapshot succeeded with the documented `latexmk`
command. The final 20-page log has no warnings, unresolved references, or
overfull/underfull boxes. Its log and private sources are retained alongside
the checks.

## Source overlap and limitations

I inspected [Kis–Horváth's open primary article](https://link.springer.com/article/10.1007/s10107-021-01652-z),
Section 5.7, especially Proposition 22 and equations (30)–(31). It explicitly
shifts lower bounds, uses a transportation network, and translates cut
inequalities back to original coordinates. The manuscript accurately calls
this a direct predecessor and the transportation feasibility mechanism
classical. It claims the graph-specific sparse-observation formulas and
oracles, not a new general max-flow projection principle. The planar
support-sum identity is likewise credited to classical polyhedral geometry.

The [primary Ford–Fulkerson transportation page](https://pubsonline.informs.org/doi/10.1287/mnsc.3.1.24)
supports the new bibliography entry. The Yale-hosted primary maximal-flow PDF
opens, but its browser text extraction is empty. The ACM Edmonds–Karp page
returned HTTP 403, and ordinary retrieval of the linked Michigan copy failed
certificate verification; those failures were not bypassed. I checked the
shortest-augmenting-path complexity argument mathematically rather than
claiming a fresh full-text audit of that source.

The foundational and compression section sources are unchanged from the
previous snapshot. This review did not re-run the numerical implementations,
establish exhaustive literature priority, or approve future coefficient and
computational sections not yet written.
