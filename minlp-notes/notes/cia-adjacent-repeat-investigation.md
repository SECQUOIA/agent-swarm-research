# A possible integral-flow route to the general heavy-mode CIA lemma

Status: developed 2026-09-04. The existential adjacent-repeat property below is now proved analytically and independently reviewed in [the universal heavy-mode theorem](../results/cia-universal-heavy-mode-rounding.md). The largest-mode strengthening remains unproved, and two other stronger variants are false. The searches below record the investigation that led to the proof.

## Proposed finite-grid property

Let a_i,j≥0 for n modes and M unit-length intervals, with Σ_i a_i,j=1. Put A_i,k=Σ_{j≤k}a_i,j. Suppose some terminal mode mass A_i,M exceeds 1.

**Existential property, now proved.** There is a one-hot integer word w_1,...,w_M such that all cumulative errors have magnitude at most 1 and at least one adjacent pair of entries is equal.

A stronger surviving candidate is that an adjacent pair can always be chosen to use a mode of largest terminal mass. The hypothesis that the selected largest mass exceeds 1 remains necessary in this formulation. The existential property is now proved; the largest-mode strengthening is not.

The existential statement implies a general heavy-mode lemma. For T=(k+1)E, average an arbitrary measurable relaxed control over k+1 intervals of length E and apply the property. Cumulative error is bounded at their endpoints. Inside each interval every error component is monotone, so the same bound holds throughout. At least one equal adjacent pair merges, giving at most k activation blocks, hence at most k−1 switches. Thus any relaxed control with a mode mass greater than E has full CIA error at most E. Shorter horizons can be extended to (k+1)E and restricted after constructing the schedule.

This implication isolates the remaining exact-switching problem to one-sided discrepancy bounds. It would not by itself prove those reach bounds.

## Exact integral-flow feasibility test

`code/cia_tv_conjecture/adjacent_pair_flow.py` checks a specified adjacent pair without numerical optimization. A mode chain carries its cumulative occupation through successive prefix nodes, with lower and upper integer bounds

L_i,k=max{0,ceil(A_i,k−1)}, U_i,k=floor(A_i,k+1).

Each time slot supplies one unit of flow and can send it to a mode at that time. Forcing one mode at two consecutive slots removes the other assignment edges at those slots. Lower-bound circulation feasibility reduces to an ordinary integral maximum-flow problem. The implementation uses exact rational cumulative allocations and integer capacities, and directly verifies every returned word against all exact prefix errors.

For noninteger A_i,k these bounds coincide with ordinary floor/ceiling rounding. At integer prefixes they permit an additional unit of error on either side. Those boundary cases matter: pure alternating inputs may force all switches under exact prefix rounding even though error-one rounding permits merging adjacent choices.

A deterministic search checked 4,502 random rational profiles on M=3,...,12 unit intervals with n=3,...,12 modes, testing a largest-mass mode first. Every tested largest heavy mode admitted an adjacent equal pair. The search used 11,478 exact circulation feasibility tests. Earlier floating LP searches also passed all tested existential cases on M=3,...,9, but the exact tests are the stronger computational evidence. These are finite searches, not a proof of the conjecture.

## A false strengthening: an arbitrary heavy mode cannot always be repeated adjacently

Consider M=4, n=3, with interval-average rates

| mode | interval 1 | interval 2 | interval 3 | interval 4 | total |
|---|---|---|---|---|---|
| 0 | 7/15 | 0 | 0 | 0 | 7/15 |
| 1 | 2/15 | 1/2 | 0 | 4/5 | 43/30 |
| 2 | 2/5 | 1/2 | 1 | 1/5 | 21/10 |

Mode 1 is heavy, but no error-one rounding can select it at two adjacent slots.

If its pair occupies slots 1–2 or 2–3, its occupation at the end of the pair is at least 2 while its cumulative relaxed allocation there is only 19/30. Its negative error is at least 41/30>1.

If its pair occupies slots 3–4, mode 2 must receive at least two selections among slots 1–2, because its final mass is 21/10>2 and its final positive error must be at most 1. Yet selecting mode 2 twice by slot 2 produces negative error 2−9/10=11/10>1. This excludes the last possible pair.

The existential and largest-mode candidates survive this example. The words (0,2,2,1) and (0,1,2,2) both have error at most 1 and repeat the largest-mass mode 2. Exact flow checks recover these words.

This counterexample rules out a proof that simply fixes any heavy mode and then searches for its repeated adjacent activation. A valid general argument must select the mode using more information, such as its terminal mass rank.

## Exhaustive small searches and a second false shortcut

Additional exact searches tested every three-mode allocation matrix on four intervals with rates in thirds (10,000 matrices), five intervals with rates in halves (7,776 matrices), and six intervals with rates in halves (46,656 matrices). A largest-mass mode admitted an adjacent equal pair in every case. Since M>n in these searches, its mass is always greater than 1. These tests remain finite evidence.

It is also false that one can always force the largest mode's pair to end at the first integer-grid prefix where its cumulative mass reaches 1. A small counterexample has five intervals:

| mode | interval 1 | interval 2 | interval 3 | interval 4 | interval 5 | total |
|---|---|---|---|---|---|---|
| 0 | 3/5 | 0 | 1/10 | 2/5 | 1 | 21/10 |
| 1 | 3/10 | 3/5 | 11/20 | 3/5 | 0 | 41/20 |
| 2 | 1/10 | 2/5 | 7/20 | 0 | 0 | 17/20 |

Mode 0 is strictly largest. Its first prefix reaching 1 is prefix 4. Forcing it in slots 3–4 leaves mode 1 with no service in those slots. Mode 1 already has mass 41/20>2 at prefix 4, so it needs both slots 1–2. But its allocation at prefix 2 is only 9/10, making that assignment's negative error 11/10>1.

The largest-mode conjecture survives: (0,1,1,0,0) is a valid error-one rounding with the largest mode in slots 4–5. Exact flow tests find no largest-mode adjacent pair except those final two slots. A global argument must therefore choose the repeated pair's position with care, even if it chooses a largest-mass mode.


## Analytic resolution of the existential property

Integral prefix rounding can be chosen to repeat some mode by maximizing the terminal occupation of a heavy mode. If that rounding has no adjacent repeat, take the prefix ending at its first repeated mode. Its occupation multiset contains that mode twice and every other selected mode once. The existing prefix error bounds put its relaxed masses exactly in the regime of the one-double-block deadline construction. Reordering this prefix preserves all endpoint occupations, hence every suffix error, and introduces an adjacent repeat. The [complete proof](../results/cia-universal-heavy-mode-rounding.md) has a fresh independent audit and an independent exact dynamic-programming check on 1,415 cases. The proof does not force the repeated mode to be largest.

A final exploratory cutting-plane MILP checked the largest-mode property for three modes and five intervals over continuous relaxed rates. Its master enforced that mode 0 has largest terminal mass at least 1 and separated against every word containing an adjacent pair of mode 0. After 45 schedule cuts, the numerical master upper bound and a feasible lower witness both equaled 1. This was a floating solver result, not an exact rational certificate, and is not needed for the analytic existential theorem. It provides additional bounded evidence for the still-unproved largest-mode strengthening.
