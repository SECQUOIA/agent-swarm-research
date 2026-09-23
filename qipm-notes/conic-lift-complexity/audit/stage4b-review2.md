# Stage 4B independent review 2

I read all five new sections (09a–09e), the Stage 4B author handoff, and the relevant universal-channel, joint-cover and proper-base-domain dependencies. I did not read other reviewers' reports or delegate this review. I reconstructed the local face proof, the exact-active-strata cup-product proof, all shared-square face cases, and the aggregate matrix contact calculation. The two issues below should be corrected. No counterexample to the intended integer-cap theorem statements or unresolved major proof gap was found. The first issue is a substantive strengthening and correction of an impossible-case discussion, rather than an invalidation of the currently displayed weak inequalities; root should determine whether the resulting mathematical revision merits a fresh five-review cycle.

## Issue 1: the total local channel rank has an extra annihilator; the proposed one-unit bonus is impossible

Locations: 09b-face-sharing.tex lines 35, 56–70, 84, 89–90, 104, 141–148, and especially 164–176; 09e-spectral-chordal.tex lines 62, 74, 81 and the corresponding direct-sum proof.

For a block with any active row a, fix its nonzero dual contact vector b=B_i^a(x_a). The scalar function x' -> <A_i(x'),b> is nonnegative on the whole primal source manifold and is zero at x. Therefore

    im DA_i(x) ⊂ b^perp,   A_i(x) ∈ b^perp.

The direct sum already constructed in the manuscript,

    R A_i(x) ⊕ ⊕_{a∈I_i} E_a,

lies in this (m_i−1)-dimensional hyperplane. Its dimension is 1+Σ_a t_i^a. Hence the actual bound is

    Σ_a t_i^a ≤ m_i−2 = r_i,

not merely m_i−1. This does not need C2 regularity or symmetry of the individual mixed forms. If there are no active rows it holds trivially. The identical argument applies to the spectral source manifolds in09e, including rectangular mixed pairings.

Consequences and suggested corrections:

* In09b replace the first local bound by m_i−2, and propagate R≥kp instead of R+L≥kp.
* Delete the suggestion that T_i=r_i+1 is a possible sharing bonus. It cannot occur under the hypotheses. Keep the valid complementary-face inequality (q_i−1)T_i≤q_i(f_i−1), so a shared block satisfies T_i≤min(r_i,2(f_i−1)).
* The consequence L≥ceil(kp/c) holds without the condition 2(f−1)≤c.
* In09e replace Σ_a t_i^a≤m_i−1 by ≤q_i and replace Σ_i(q_i+1)≥Σ_aκ_a by Σ_iq_i≥Σ_aκ_a. The displayed face-weighted capacity bound and its divided-by-f consequence are then redundant weaker bounds, although not false. Preserve the useful face-specific inequalities and incidence-count bound.

There is also an immediate global strengthening available from the already established joint-cover theorem. Define aggregate dual maps

    B_i(z_1,...,z_k)=Σ_a B_i^a(z_a).

These are C1 cone-valued maps and factor the kernel k−Σ_a<x_a,z_a>. Its contact pairing is nondegenerate on the product of spheres. If R=kp, Theorem general-joint-cover forces the positive capacities to be exactly k copies of p. Under c<p this is impossible. Thus

    R ≥ K := kp + 1_{c<p}.

For example, one can combine this with the manuscript's face budgets by setting

    R_* = max{ceil(kτ/f), K},
    L_* = max{ceil(kh/f), ceil(R_*/c)}.

Then L≥L_*, R≥R_*, D≥R_*+2L_* and every ambient barrier has parameter at least2L_*. It is also fine to state a less optimized but transparent consequence. The ray-exposed exact frontier remains unchanged. Do not infer an exact general f>1 frontier from these stronger necessary bounds.

## Issue 2: explicitly make the dimension cap an integer

Locations: 09b-face-sharing.tex line16; 09d-lp-power.tex line20 and the opening of Theorem lp-smooth-frontier. For consistency also clarify d in the spectral cap hypothesis if it is intended as the same integer cap.

The exact ceiling formulas and constructions require integer d. The earlier proper-smooth-frontier corollary explicitly says this, but these new sections introduce d afresh. For instance N=4,d=3.5 in lp-granularity would claim two factors, although every allowed integer-dimensional factor has dimension at most3 and three are necessary. In09b, divisibility c|p likewise presumes integer c. Add “an integer d≥3” at the relevant introductions (or establish a clearly scoped shared convention); do not alter the intended formulas.

## Checks with no issue found

* The global face-budget proof's activity loci are lower-semicontinuous rank loci; C_a=p is closed, and fixed exact-active-label pieces are clopen in that locus. Their compact projections admit normalized dual phase neighborhoods. Injectivity follows from the full row identity even though inactive derivatives need not vanish: their mixed forms have rank zero. The proper-open-domain lemma then kills the source top class. Disjoint neighborhoods of each finite family of compact pieces support the relative cup-product argument. No smooth cone boundary or differentiability of a polarity map is silently used.
* The shared-square cone includes the t=0 recession face. The dual formula, equality and strict dual cases, maximum exposed-face dimension2q−1, functional-span minimality2q+1, contact-face minimality2q−1, and q+1 completion barrier are consistent, including q=1. Product orthant sections justify coupled ambient barrier lower bounds.
* The09a whole-row rank and face proofs, polar extreme-row identification, minimum-dimensional cone rigidity, finite connected-cover dimension argument, 3-PARTITION reduction, recession-height criterion, and escaping-disk counterexample all check. Barrier transfer is stated with the necessary bounded-fiber/normalization conditions.
* The09c extreme-point classification and connectivity proof cover the disconnected real rank-two zero set by paths through another block. The Albert chart uses two octonions and Artin associativity legitimately. The original off-diagonal frame supplies the orthant/simplex sections, whereas the diagonalized height description is used only for connectivity. The two barrier optima follow from those sections and the restricted gradient calculation.
* The09d tree and Young constructions, genuine slice certificates, local projection splitting, half-cone counterexample, planar projective C2 obstruction, and weighted-variance curvature proof check under integer caps. The denominator-sensitive mediated-set statements are not overextended.
* The09e spectral mixed rank includes the δ−1 imaginary phase channels. The whole-row contact codimension δ(r+c−1), arbitrary-barrier recession certificate for the shared cone, fixed-scale gradient norm, completion duality, star ledger, phase-invariant rank-one polar certificate and equality of the reduced Hessians check. The claimed equality is only for identical retained data and barriers; no ambient oracle or running-time equivalence is inferred.

## Literature verification

The primary full text of Fawzi–Saunderson, https://arxiv.org/html/2205.04581v3, Section3.3 Theorem3.9, has exactly the recession-direction lower-bound hypotheses used in09e. The certificate there meets them and tensorizes by direct summands; logarithmic homogeneity of a competing barrier is unnecessary.

Read the local primary full text `literature/papers/andersen2013-logarithmic-barriers-for-sparse-matrix/fulltext.md`, introductory equations(3)–(6): signed Legendre duality and the inverse maximum-determinant completion agree with09e, including the additive −n constant. The manuscript appropriately calls this barrier classical.

Read the local primary Wang geometric-mean source around Theorems6 and16 (preprint numbering): the simple representation bound m−1 and arbitrary SOC count bound m/2 are distinct. The manuscript preserves that distinction and declines an unsupported scalar priority claim. Its separate self-contained curvature proof is valid.

No manuscript or literature files were edited by this review.
