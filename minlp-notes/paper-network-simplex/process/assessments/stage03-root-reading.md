# Stage 3: root source reading

The root independently checked the accepted cycle/theta and parallel-path source
proofs while preparing the manuscript stage. The following points need to remain
explicit in the paper.

- Theta state nonemptiness consists of three interval consistency conditions
  and intersection of the attainable sum interval with its specified bounds.
  The six tight coordinate supports are attained, including degenerate states.
- A planar Minkowski sum acquires no new edge directions. Segments and points
  require an explicit argument: the allowed segment directions have their affine
  equations and endpoint bounds among the same six normals. A full-dimensional
  polygon argument alone would leave a gap on zero-weight and degenerate strata.
- Selecting a branch gives a globally valid affine cut, not merely a local
  linear approximation. Lower endpoints are maxima, upper endpoints minima;
  nonnegative support combinations preserve the needed inequality direction.
- Unit product coefficients rely on selecting each observation at most once
  within a state, and disjoint product coordinates across states. All product
  consistency equations and local feasibility conditions must also be checked.
- Compact recovery can run in linear arithmetic time for theta blocks, but
  writing m+1 full flow vectors has a potentially quadratic output size. A
  default per block and exceptions per observed block/state pair resolves this.
- For parallel paths the shifted transportation row demand can initially be
  negative. Complement-of-singleton subset cuts imply its nonnegativity; an
  algorithm may return that violated lower bound before building max-flow.
- The minimum cut minimizes independently over column sides and gives the
  displayed minimum of two sums. Proving only necessity of subset inequalities
  would not justify exact membership or constructive recovery.
- The higher-path-count oracle is polynomial-time max-flow, not the earlier
  linear arithmetic method. Rational bit complexity needs a polynomial-time
  rational implementation rather than the arbitrary-capacity Ford–Fulkerson
  augmentation rule.

The previous joint-state theta example is useful: each one-state hull can hold
while the combined state allocations overfill a path. This is an illustration
of known disaggregation, not another novelty claim. The three-path coordinate
sum should not reuse the letter d already reserved for total state count.

No manuscript acceptance is implied before the completed five-reviewer round.

## Root draft reading

The root read the complete new section. The theta signs are consistent: the
third path uses minus its original traversal sign while the general parallel
formulation returns to the original signs. The nonemptiness conditions and
attained supports follow from interval intersection. The new proof explicitly
handles segment and point Minkowski sums; the suffix construction includes an
empty sum and a verified feasible-point selection rule.

The transportation proof supplies the missing nonnegative row targets before
invoking max-flow, handles total target zero, and converts every minimum-cut
expression back to the stated original subset inequality. Selected branches
are global affine majorants/minorants with equality at the candidate; their
validity is not inferred from a local derivative. The coefficient and rational
encoding arguments are correctly qualified. No mathematical defect was found
in this reading. Independent reviewer adjudication remains pending.
