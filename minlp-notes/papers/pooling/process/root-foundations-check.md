# Root's preliminary foundations checks

These checks precede the required 15-agent review of the completed stage.

## Mathematical reading

Read the profitable-flow, facial-integrality, and recirculation result notes and their main arguments. Checked the distinction between integral optima on a finite union of flow polytopes and tractable optimization over that union; the face-recognition LP; enumeration by active facets in fixed affine dimension; head-weighted destination decomposition; closed circulation classes; backward mixing-system invertibility when boundary flow enters; and the difference between an uncapacitated conic hull and a capacitated convex hull. No defect in these arguments was identified in this preliminary reading. Statements about an integral optimum require feasibility.

## Reproducible finite checks

Command: `python papers/pooling/verification/check_foundations.py`.

Result: PASS for 240 exact cyclic destination decompositions, 80 near-circulation conditioning instances and singular-cycle checks, and 406 nonfacial fractional-improvement witnesses. The script uses only Python standard-library rational arithmetic, with a fixed seed. These are finite supplemental checks, not proofs of the universal claims.

## Source defect found

The explanatory docstring of `code/pooling_degree_two/irrational_example.py` omits the concentration normalization denominator. For its proposed flow family the quality inequality is

`b(3/4+b/2)/(1+b) <= 1/4`,

equivalently `2b^2+2b-1 <= 0`, with positive root `(sqrt(3)-1)/2`. The file's stated root agrees with this corrected inequality, not with its displayed inequality. The manuscript author was notified. The original script is unchanged at this stage.

### Completing the global argument

Write the two intakes of the mixing pool as `a,b`, its throughput as `t=a+b`, its delivery to the strict output as `z`, and the clean anchor delivery to that output as `c`. The cost is `-3a-2b+z`. For fixed intakes the best feasible choice uses `z=max(0,t-1)` and may use `c=1-z`: decreasing `z` improves cost and only relaxes the quality condition, and clean intake and delivery costs cancel. The strict quality condition is `(3a+2b)z<=t`.

For `t<=1` the maximum profit is 3. For `t>1` it is `a+t+1`, with `a<=1` and `a<=h(t)=t/(t-1)-2t`. The function `h` is strictly decreasing. It equals 1 at `t0=(1+sqrt(3))/2`. Up to `t0`, the best profit is `t+2`, increasing; beyond `t0`, it is `2-t+1/(t-1)`, strictly decreasing. Feasibility ends at `t=3/2`. The global optimum cost is therefore `-(5+sqrt(3))/2`, attained at `a=1`, `b=z=t0-1`, `c=1-b`. These flows satisfy every original capacity. The zero-throughput case has cost zero and causes no division issue.

The original Gurobi script was also rerun in the existing `minlp-notes` environment after reading its physical model. Its result was `-3.366025404`, within approximately `6.8e-10` of the derived exact value. This floating-point agreement supplements the global analytic argument and is not an exact certificate.

## Proposed cyclic approximation completion

For at least one output, the cyclic destination decomposition can assign every isolated circulation component to one designated destination component. The circulation support is disjoint from the remaining positive-flow support, so the merged component remains physical and dominated by the original flow. The resulting destination components still sum to the original flow. Thus the output-count approximation and its shared-capacity LP argument extend to the stated algebraic cyclic model. With no outputs, the problem is a min-cost circulation problem instead. This was sent to the author for independent assessment and inclusion in the stage review.
