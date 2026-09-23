# Stage 2, round 1 — independent reviewer 4

Reviewed frozen snapshot: `process/snapshots/stage02-round01`, including the
whole compression section, its dependencies and integration in `main.tex`.

## Verdict and enumerated findings

**Accept the stage: no major or minor defects identified.**

1. **R4-S02-01 — No actionable finding.** The variable, row, nonzero, and
   coefficient claims follow from the constructions as written. I found no
   unsupported minimum-dimension assertion or missing essential proof step.

## Detailed audit

**Fixed arcs.** The affine graph correspondence remains valid when fixed
coordinates include positive flows or self-loops: adjoining `c` changes the
balances by exactly `A_F c`, and the product coordinates adjoined are affine
in the simplex vector. For the affine-hull assertion, every nonconstant
coordinate admits a midpoint strictly between its two bounds. Averaging all
these midpoints makes every remaining bound strict, which supplies a relative
neighborhood in the balance affine space. The empty-coordinate case is
handled. Fixed-coordinate detection is explicitly not claimed as part of this
lemma.

**Suppression and counts.** Internal degrees are correctly taken within the
block, so attachments at articulation vertices do not invalidate path
suppression. The signed intervals for both orientations follow from solving
`0 <= v_e + epsilon_e delta_p <= u_e`. A rank-one block needs a separate
loop representation and is given one. For the other cyclic blocks, suppression
gives minimum degree three; `2k >= 3n` and `r=k-n+1` imply the displayed
`n <= 2r-2` and `k <= 3r-3`. The chord identity rows ensure boundedness of
cycle coordinates even if the feasible domain has smaller affine dimension.

**Initial extended hull.** Each observed label uses exactly `r_B` variables.
The residual is a circulation because it is the difference of the aggregate
circulation and explicit state circulations; no omitted residual balance
equation is needed. The bound rows number `2k_B(a_B+1)`, and every original
observation retains its own equation, including repeated observations on a
single path. Using one representative original arc for each residual path
expression is essential to the unit `x` coefficient claim and is done
explicitly. Zero weights force all path coordinates and then all chord
coordinates to zero.

**Total unimodularity and elimination.** The minor identity for
`N_T^{-1}N_Q` follows by replacing selected tree columns and expanding the
unchanged identity columns after multiplication by `N_T^{-1}`. Its determinant
is an incidence minor divided by a unimodular tree determinant. Appending
identity rows preserves total unimodularity. Both the row-replacement formula
for `W` and the bordered determinant formula for `R` are correct; repeated
rows give zero determinants, and empty pivot/free cases are valid. The
substitution for `t_I` is reversible, and all nonselected observation equations
remain. Thus no compatibility equation is lost.

**Coefficient collection.** Selected independent path rows use distinct
original products. A nonselected observation has a different product variable
from every selected observation, even when it observes the same path. Different
labels have disjoint product and auxiliary columns. Therefore collecting
state, observation, and residual rows cannot turn a unit coefficient into
magnitude two. Only the `y` coefficients collect network offsets and interval
data. The normalization warning correctly avoids transferring this assertion
to primitive integer rows after denominators are cleared.

**Observation rank and size.** Restriction to observed original arcs has
kernel exactly the circulations supported on unobserved arcs, yielding
`r-d=|U|-|V_B|+c(V_B,U)`. This uses all isolated vertices and counts loops
correctly. Observing any original arc on a suppressed path fixes that path
value, so its restriction rank is exactly the rank of the observed core rows.
Elimination adds no rows. Each reconstructed path uses at most `O(r_B)`
selected-product and retained-variable entries per label, and each observation
uses at most `O(r_B)` entries. With `O(r_B)` paths, this gives the displayed
nonzero bound, including residual rows whose length grows with the number of
active labels. Rational offsets and their finite sums have polynomial bit
length. No claim of linear bit complexity or whole-matrix total unimodularity
is made.

**Completion and recovery.** Each extra coordinate removes at most one
dimension of the restriction kernel. The nonforest unobserved edges remove
exactly all its cycles and attain the count. Treating their added product
coordinates as auxiliary variables is legitimate because coordinate projection
commutes with convexification. This adds at most `sum r_B a_B` observation
rows and no new observed labels, so the stated row bound is preserved. The
forest cut explanation correctly permits known observed edges to cross cuts
and includes component consistency conditions. The interpretation is carefully
restricted to ambient linear reconstruction; fixed capacities and zero weights
are not mistakenly included in its lower bound. Recovery reduces explicitly
to the previously proved proportional refinement.

**Concrete example and integration.** I recalculated the three missing `K_4`
deviations from node balance and obtained the displayed formulas. The equally
weighted four-path flow has `x_12=x_34=1/2` and the other entries `1/4`.
The chosen three products `1/5` satisfy all their McCormick rows at `y=1/2`,
but their sum `3/5` violates the reconstructed nonnegativity cut. This example
does not purport to be a complete one-inequality hull. Stage 1 notation and
labels remain compatible with this section, and later coefficient results
are not needed for any present proof.

## Checks actually performed

I compared the section with `notes/network-simplex-reopened-compressed-hull.md`
and `notes/network-simplex-observed-rank-elimination.md`; the scoped results
and their material caveats are covered, with additional proof detail.

I wrote an independent exact SymPy check in
`verification/reviewer4/stage02-round01/check_elimination.py`. It constructs
fundamental-cycle matrices directly from incidence matrices, examines every
observation pattern in six graphs, and tries every nonsingular pivot-column
choice for its independent observed rows. The graphs include a loop, parallel
arcs with mixed orientations, a reversed triangle, `K_4`, two triangles sharing
an articulation vertex, and `K_{2,4}`. The checks passed:

- 410 observation patterns: exact restriction-rank/unobserved-cycle identity;
- 459 pivot choices: unimodular determinants;
- 3,262 path rows: exact reconstruction identity and unit entries of `W` and
  `R`.

The summary is retained in `check_elimination.json`. These finite checks
supplement the proof audit; they are not the basis for the general theorems.

A private snapshot copy built successfully with `latexmk` under
`verification/reviewer4/stage02-round01/build`. The final log has no warning,
undefined reference, overfull, or underfull matches.

## Limitations

I did not benchmark model construction or independently repeat the prior
literature search. Neither is needed to substantiate this stage's purely
structural claims. The small exact experiments do not exhaust all graphs or
reprove arbitrary-size total unimodularity. I read no other current-round
report, edited no manuscript source, and spawned no agents.
