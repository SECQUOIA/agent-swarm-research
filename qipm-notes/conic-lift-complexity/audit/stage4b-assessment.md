# Root assessment of Stage 4B, first review round

The author completed the five sections before five independent reviewers
were dispatched. Root has read all five reports and the manuscript additions.
Reviewers 1, 3, and 4 found only the integer-cap omission; reviewer 5 found
no issue. Reviewer 2 additionally found an unused annihilator that strengthens
the central sharing bounds. Both findings are accepted.

## Accepted substantive revision

In 09b and 09e, the direct sum consisting of the primal ray and all active
source derivative spaces lies in the hyperplane annihilated by any fixed
active dual contact vector. Nonnegativity of the fixed-dual pairing on the
entire primal manifold makes every first primal derivative lie in that
hyperplane. Its dimension is m_i-1, so the total mixed-channel rank is at
most m_i-2. Root independently verified this proof; no second derivatives
or symmetry of the individual mixed matrices are needed.

The existing weaker inequalities remain true, but the discussion of a
possible one-unit sharing bonus is misleading because that bonus is
impossible. The stronger bound materially changes the resource theorem.
For that reason, and to meet the user's requirement to develop identifiable
improvements, root treats this as a major scientific revision for workflow
purposes. A new five-reviewer pass is required after correction.

In 09b also aggregate the labelled dual maps. They factor
k-sum_a <x_a,z_a> on the product of spheres. At capacity equality R=kp,
the already proved joint-cover theorem forces the positive capacities to
be exactly k copies of p. Thus the strict cap c<p implies R>=kp+1.
The face-incidence and face-capacity budgets remain independently useful.
With a uniform face bound f>=1, one transparent combined consequence is

    K = kp + 1_{c<p},
    R_* = max(ceil(k tau/f), K),
    L_* = max(ceil(k h/f), ceil(R_*/c)),
    R >= R_*, L >= L_*, D >= R_*+2L_*, nu_ambient >= 2L_*.

Keep the exact ray-exposed frontier and the limitations for f>1. Retain
the shared-block face inequality, now T_i<=min(r_i,2(f_i-1)), but remove
the impossible bonus and any restrictions needed only for its weaker
consequences. In 09e propagate sum_i q_i>=sum_a kappa_a and the stronger
local total bound. Avoid retaining redundant divided-by-f capacity bounds
as if they were useful additional information. Verify all neighboring
formulas, source dispositions, and novelty descriptions after the change.

## Accepted minor correction

Declare dimension caps d>=3 to be integers in 09b and both exact-frontier
theorems of 09d; the capacity-excess proposition inherits that convention.
Make the 09e cap convention consistent. The concrete counterexamples in
the reports show why real d cannot be used literally in exact formulas.
The intended integer-cap proofs do not otherwise change.

No other requested correction was identified. A separate correction
author must implement all accepted changes, record them, and build the
manuscript. Stage 4B is not complete until five reviewers have checked the
revised mathematics and all remaining valid issues have been addressed.
