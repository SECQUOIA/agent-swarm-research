# Stage 3 primary-agent mathematical audit

## Mode removal and coefficient algebra

Read the original arbitrary-block proof and the final seeded result, distinguishing the earlier clipped derivation retained in the reopened note from the final unclipped theorem. The maximum-mass step is valid only when the child coefficient is at least 1/(n−1); below that threshold the minimum-mass choice is essential. The manuscript must establish positivity of the remaining error allowance, not assume it from the old maximum-mass proof.

The recurrence transform telescopes exactly. For the elementary coefficient, the numerator of C_nk−1/(k+1), on the positive common denominator, factors as (k−n+1)(k²+k−2n). Thus the stated interval is an iff condition for k>=2, while k=1 has the isolated equality n=2. Sent this boundary distinction to the author.

Read the certificate-free four-block predecessor. It is the three-block seed propagated once, with the new minimum-mass branch also handling the smallest dimension n=5 uniformly. Its value remains useful because its proof is analytic, whereas the sharper exact four-block result uses certificates. The predecessor's old unresolved finite-n wording is superseded by accepted stage 2.

## Independent general-seed expansion

Let ell be a proved seed budget, d=k−ell, x=1/n and m=n−d. Expanding the exact transformed coefficient gives

    theta = 1−2k x+k(k−1)x²+(-ell³+ell+3k²−3k)x³/3+O(x⁴).

Substitution into C=x(1+theta)/(1−theta) yields

    C^(ell) = 1/k−(k+1)x/(2k)
              +(3k³−3k−2ell³+2ell)x²/(12k²)+O(x³).

The difference from the uniform lower coefficient is

    (k³−k−ell³+ell)/(6k² n²)+O(n^−3)
    = (k−ell)(ell²+ell*k+k²−1)/(6k² n²)+O(n^−3).

I derived these coefficients independently using exact symbolic expansion of the binomial expression. The ell=4 specialization already appears in the repository; this is not claimed as a new discovery. The general ell formulation makes its dependence on the seed transparent. Only ell<=4 is proved as an exact seed in the paper. At ell=1 it recovers the elementary coefficient, at ell=k<=4 the gap vanishes identically, and at ell=4,k=5 the second-order gap is2/5. Sent the general formula to the author for an independent derivation.

## Higher-block relaxation investigation

The original n=6 witness refutes only implication from a necessary partial-order relaxation. A coordinate decreases at later physical time, so it cannot be a cumulative allocation. Actual chronological coordinate monotonicity plus conservation is sufficient to interpolate event allocations, but it does not by itself establish the required reach/max identities. The author is testing a single chronological chamber and must state its restricted scope. No general higher-block reach theorem is approved by this note.

Full manuscript reading, verification audit and the required five independent reviews remain pending.

## New exact equal-terminal-mass band from all-light rounding

Read the full all-light greedy lemma in the three-switch-heavy source. At E=T/n for equal terminal masses, its k-block reach is at least T exactly when k(n−k+1)>=n(n−k), which reduces to k>=(n−k)^2. Therefore the full equal-terminal-mass minimax is T/n throughout that sufficient band: the lemma gives the upper bound, and uniform input with k<n omits a mode and gives the lower bound. This extends to arbitrary budgets; it is not a claim that the band is necessary or maximal. In terms of deficit d=n−k, it covers k>=d². Sent to the author for independent development and later five-reviewer scrutiny.

The same lemma at E=T/(k+1), combined with the heavy theorem, gives the unrestricted plateau k+1<=n<=2k. It explains the earlier certificate-free three-switch plateau n5..8 and the binary zero-switch equality; stronger general/seeded results can supersede it where their ranges extend further.

## Completed first manuscript reading

Read sections 06 and 07 in full before the author's handoff. The removal proof correctly treats C below, at, and above the reciprocal threshold; it verifies both prefix length and error allowance, and preserves distinctness and all original cumulative offsets. The initial draft's seed-domain omission and contradictory clipping sentence were corrected during writing. The elementary and seeded formulas, plateau signs, and formal series agree with independent algebra.

The all-light proof uses allocations at the target endpoint and bounds already selected masses, never resets cumulative history, and handles a truncated last block. Its equal-mass corollary is stated for every input, which is justified by the unavoidable omitted terminal mass. The dimension-free limit uses explicit finite-dimensional upper coefficients, so its strict inequality does not incorrectly exchange a pointwise strict bound with a supremum. The third-largest-mass proof is simplified validly using the accepted exact two-block reach lemma; its numerical mass example sums to one and improves the unconditional threshold.

The general exclusion argument is conditional on the missing weighted inequality and prior reach bound, with a positive substitution coefficient throughout n>=k+1. The n6 event relaxation explicitly fixes its maximizing pair/triple and minimum-root index; all printed rows match the bundled original builder. Its failure is confined to the relaxation and the text notes that S is not constrained to maximize a four-word. The interpolation lemma characterizes only a common trajectory, not inverse/max reach identities.

Read the new chronological checker and original matrix builder. The 64 event order is computed from exact witness times with deterministic original-index tie breaks;378 adjacent coordinate inequalities imply time ordering by conservation. The rational dual uses nonpositive inequality multipliers and nonnegative coordinate residuals, the correct signs for a minimization lower bound. The explicit uniform-event primal attains13104/125. The single-chamber and fixed-maximizer scope are explicit, and no general reach implication is claimed. The new checker’s initially ineffective assert-based optimized-Python guard was replaced by an explicit RuntimeError during writing. No outstanding defect found in this reading; the five independent reviews remain required.
