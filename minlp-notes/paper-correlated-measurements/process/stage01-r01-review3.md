# Stage 1 independent review 3

Scope: `sections/01-foundations.tex`, its statistical and algebraic claims, relevant original source passages, and source code. This review excludes the deliberately unwritten introduction, abstract, and later technical sections. I did not edit manuscript files or consult other Stage 1 reviews.

**Verdict: no major issue found. Three minor presentation/completeness corrections are identified below.** The stated model, marginal-information target, conditional-noise distinction, Loewner bounds, rank refinement, and global-certificate contract are mathematically sound under their explicit assumptions.

## Independent verification

The script `verification/stage01-review3/check.py` and its saved `results.txt` use exact SymPy arithmetic. I checked all 60 subsets across rational covariance examples of dimensions 2, 3, 4, and 5, with three parameter directions and a singular common prior. Checks include both sandwich inequalities, equality of kernels, diagonal observation-coordinate invariance, the exact Schur inflation identity, the decomposition of full information into actual-response conditional information and complement information, and the cross-covariance rank bound. Positive semidefiniteness was checked by every principal minor, not only numerical eigenvalues.

The exact two-response witness yields 16/7 gated singleton information, 8/7 full information, and 1/7 actual-response conditional information. The source covariance has the stated leading minors 1, 399/100, and 791/25; the SCM block of its inverse is exactly (4/3) C_0^{-1}.

For the kinetic example, symbolic substitution verifies the rate-swap identity. It also supplies a concrete full-local-rank example: at (A_0,k_1,k_2)=(1,1,2), using times (log 2, 2 log 2, 3 log 2), the sensitivity determinant with columns (A_0,k_1,k_2) is -(log 2)^2/2048. Thus the conceptual counterexample can be made completely explicit without further experiments.

I independently inspected the archived Wang accepted-manuscript text around Eqs. (6)–(13), Liu's Eq. (29)/Proposition 2 passage, and the actual `_split_sigma` and kinetic covariance construction in the immutable archived software. The manuscript accurately distinguishes the source's maximized trace criterion from conventional A-optimality, attributes the known selected-inverse mismatch and weak-correlation result, and does not infer that the final publisher version was inspected. The correction is appropriately scoped to one-modality witnesses and explicit source versions. The pattern repair correctly handles same-time cross-channel correlations by joint patterns, not independent modality chains.

## Findings

### R3-1 — MINOR: identify which extremum the sharpness example establishes

**Location:** `sections/01-foundations.tex:345`–348, Example `ex:gated-sharpness`.

**Issue:** Immediately after describing efficiency approaching its lower bound, the text says “the bound is sharp as a supremum.” The efficiency has an infimum, while the additive log loss (or inverse efficiency) has the corresponding supremum. The underlying result is correct, but the wording conflates the two quantities and is needlessly ambiguous.

**Fix:** State that “the infimum efficiency is 1/alpha (equivalently, the supremum additive log loss is log alpha for p=1), already for rational data and three candidates.” Alternatively say simply that the universal efficiency lower bound cannot be improved. No new theorem or experiment is needed.

### R3-2 — MINOR: explicitly finish the local-versus-global identifiability example

**Location:** `sections/01-foundations.tex:130`–143, paragraph and Eq. `eq:rate-swap`.

**Issue:** The paragraph introduces positive definite local information versus global identifiability, then proves only the global trajectory ambiguity. It does not explicitly establish that the displayed mean admits full-rank local information. The statement is correct, but supplying that last fact makes the intended example self-contained and avoids asking the reader to infer it.

**Fix:** Add the exact three-time local-rank witness above, or a short proof that the three sensitivity functions are linearly independent for positive distinct rates. A compact sentence giving the determinant at (1,1,2) and the three stated times suffices. This also makes clear that the phenomenon does not depend on regularization.

### R3-3 — MINOR: give the precise location of the covariance-table discrepancy

**Location:** `sections/01-foundations.tex:398`–400.

**Issue:** The manuscript refers to “an asymmetric entry” in “the inspected supplementary table,” but gives neither the table number nor the pair of entries. Since this is a concrete criticism of an external source that motivates using the public code's covariance, readers should be able to check it directly without navigating internal repository audit notes.

**Fix:** Name SI Table S-1 and the DCM-A/DCM-C transpose pair (0.01 versus 0.1) in the inspected accepted manuscript, with a page locator if useful. Keep the existing restriction to the inspected versions and the clear statement that calculations use the symmetric code covariance.

## Scope qualifications, not further defects

- The foundations correctly condition finite D certificates on an SPD feasible design, distinguish regularization from physical prior information, and exclude singular observation covariance and parameter-dependent covariance from the main model.
- The sharpness proof correctly needs only p=1 to rule out improving the universal constant; it does not claim every dimension or selection structure attains it.
- Rank-dependent improvement is correctly applied to the gated optimizer through a uniform feasible-schedule rank bound; no dimension-free trace-inverse assertion is made.
- The source-data numerical results and all later arithmetic algorithms are outside this stage. Their future certification cannot be inferred merely from the correct contract here.
- Exact finite-case checks complement, rather than replace, the elementary general proofs.

After these minor clarifications, I see no Stage 1 reason to prevent proceeding to the next stage.
