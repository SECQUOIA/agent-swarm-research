# Stage 2 primary-agent proof audit

## Source arguments independently checked

- Read the universal heavy-mode proof. Integral prefix-flow feasibility and integer capacities give a rounding; maximizing the terminal flow of a heavy mode forces some repetition. In the prefix ending at the first repeated label, only that label occurs twice. Its terminal mass lies in [1,3], other selected masses are at most 2, and omitted masses at most 1. The deadline reordering preserves the prefix occupation multiset and thus every later discrepancy. The equality case where the repeated label has mass exactly 1 requires its latest level time to be the prefix end; the prescribed double slot still works. Extension to `(s+2)E` and restriction preserve the budget.
- The full/one-sided minimax identity uses attained inner minima (now proved in stage 1), and its omitted-mode lower witness requires exactly the stated `k<n`. It does not require repeated-mode competitors to be distinct.
- Read the complete analytic three-block reach proof and independently checked its two first-reach inequalities, excluded-mode inequality, and final aggregate algebra. Latest feasible endpoints ensure equality at uncapped roots and a strict inequality at a failed final horizon, including flat portions. The coefficient multiplying the global two-block reach is positive at n=4 and thereafter.
- Read the four-block verifier's quotient construction and symbolic-certificate checks alongside the result's necessary constraints. The ten `(maximizing pair, distinguished index)` types exhaust the membership classes under permutations preserving the selected triple. There are 179 finite cases because one type requires six modes. The objective counts excluded pairs meeting the selected triple twice when both excluded indices lie there.
- The four-block LP uses only necessary temporal orders. Coordinate monotonicity plus mass equalities forces equal event times when a global maximizing pair remains admissible after exclusion. Actual controls therefore map to feasible points; the relaxation need not represent every feasible LP point as a control.
- For a primal minimization with `Ax<=b`, the certificate sign `Y<=0` is correct: `Y Ax>=Y b`. Exact coefficient identities and a positive common denominator prove the lower bound. Polynomial shifts establish signs for every n>=23, not just tested dimensions. The text must explain why the symbolic matrices have fixed topology and known affine multiplicities before using evaluations at n=9,10.
- The exact equal-total full minimax follows from each proved one-sided reach bound and the terminal-mass positive bound. The uniform input supplies both lower terms. This preserves a stronger restricted-class statement rather than substituting the unrestricted minimax.
- Read the rational three-mode/three-distinct-block counterexample. Its allocation increments sum to time and every slope is between 0 and 3/4, so inverse functions are strictly increasing. All six distinct orders stop at 971/146, below 57/8. This refutes only the distinct-mode extension at k=n; repeated-mode/full-error conclusions do not follow.

## Manuscript checks still required

Read the completed author text, inspect actual supplement portability and source attribution, then adjudicate the five independent reports. No stage acceptance is implied by these source checks.

## New development: strengthen the three-mode boundary example

The root independently examined repeated-mode alternatives for the existing rational knot-table input on L=57/8. Its terminal masses are `(5281,3985,3217)/1752`. The first two exceed 2. At one-sided error E=1, a schedule with at most two used modes cannot omit either of those coordinates: summing the active coordinates' terminal constraints would give an omitted mass at most 2. Thus a repeated three-block word must use modes 0 and 1, in the form 010 or 101 (shorter schedules can be padded).

For a word p,q,p, let its first two endpoints be u,v. The first active endpoint implies u<=R_p, and the middle active endpoint implies v<=Phi_q(u)<=Phi_q(R_p)=M_2=290/73. Moreover, middle service `v-u <= A_q(v)+1 <= A_q(M_2)+1=M_2-R_p`. This avoids assuming a globally optimal greedy rule for repeated words. The terminal constraint of mode p requires middle service at least `L-m_p-1`.

For p=0, the maximum middle service is 162/73 while the requirement is 2725/876, a shortfall of 781/876. For p=1, the corresponding numbers are 193/73 and 3373/876, a shortfall of 1057/876. Hence neither repeated word can reach L at error one. The six distinct words already fail by the original inverse-composition calculation. Together these arguments appear to rule out every at-most-three-block schedule, strengthening the counterexample to the actual one-sided problem allowing repeats when k=n=3. Attainment from stage 1 turns infeasibility at E=1 into a strict instance lower bound. Sent to the author for a separate derivation and proof integration, and it will receive all five independent stage reviews. This note does not self-approve the new proposition.

## Completed draft reading before independent reviews

The primary agent read sections 03, 04, and 05 in full. The heavy-mode proof explicitly handles flat cumulative allocations, preserves the occupation multiset at the reordered prefix endpoint, and distinguishes floor/ceiling rounding from the weaker discrepancy bound after reordering. The analytic reach arguments use latest endpoints and allow arbitrary measurable controls.

The certificate section now states all necessary LP constraints, counts pair multiplicities correctly, explains exhaustive ten-type symmetry and orbit averaging without assuming an attained LP optimum, and proves that topology and affine counts stabilize before using dimensions 9 and 10 to reconstruct the known coefficient forms. The finite and polynomial dual signs have the correct direction for a minimization problem. The final aggregate inequality has a positive coefficient for every n>=5.

The small-budget section derives the unrestricted and equal-terminal-mass results with their separate parameter ranges. It includes the independently confirmed stronger three-mode proposition and a separate exact feasibility check over all padded words; no repeated-word greedy optimality is assumed. The uniform one-sided comparison at k=n is proved directly rather than applying the earlier full-error theorem outside its range. The two adjacent-pair counterexamples expressly concern fixed unit slots. The remaining largest-heavy-mode conjecture is stated separately and is unused.

No mathematical defect was found in this reading. The five independent stage reviews, including supplement portability and layout, remain required before acceptance.

## Additional primary-agent minor finding during frozen review

The sentence in `sections/04-four-block-certificates.tex` giving quotient sizes (57–162 variables, 151–826 inequalities, 10–19 equalities) needs its dimension scope stated. Those ranges are correct for the stable symbolic topology (n>=9). Direct exact quotient construction at n=5 gives as few as 148 inequality rows (and ranges 57–83 variables, 10–13 equalities). Thus the present unqualified sentence is ambiguous/inaccurate if read as covering every finite case. Minor correction: explicitly prefix the size statement with “For n>=9”. This is a descriptive count, not a defect in certificate coverage or a proof premise. No manuscript edit made during review.

## Exact-instance revision: primary-agent reading

Read the complete revised proposition and standard-library checker before freezing round 2. The capped inverse is defined for nonnegative arguments and is globally 4-Lipschitz because the allocation complements have slope at least 1/4. The proof compares the final horizon constraint directly, avoiding reliance on an uncapped final root. At the claimed threshold both optimal switching times lie in the stated slope-1/4 intervals, and all three active endpoint discrepancies equal E*. The repeated-word argument rules them out even at E*, with positive exact margins, and monotone feasibility covers lower thresholds. The distinct-word argument handles [1,E*) and its threshold-one failure handles E<1. Scaling yields a minimax lower bound only. No defect found in this independent reading.

The proof strengthening is substantively new, so five fresh reviews are required despite the absence of major criticism in round 1. Reviewers 01, 03, 04, 05, and a new reviewer 06 are assigned. Reviewer 02 helped derive/confirm the new result and is excluded from this round's five to maintain independence. The original frozen stage remains unchanged.
