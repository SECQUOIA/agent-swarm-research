# Stage 2, round 1 — reviewer 02

Primary lens: covariance, parity contacts, topology, volume, and unrestricted general integers.

Major findings: 0

Minor findings: 1

## Snapshot verification and coverage

All six file hashes were computed and match `reviews/stage2-round1/snapshot.json`:

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `04faf5b34942a13d79028d42728aeb6443b34c66a575f8293bc546a1ec8fb47e` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `92931390c89c837f079fa63121c50d7fd2ad9b5ff7b4cab8ff88276f2206e177` |
| `references.bib` | `3dcfb568784b51d38f1255ff6135ecefa8be1b9c17b1fef7e8927764022bc900` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `2d6d05e3f346561242f44ecab130c9b01016b101bb4843eaeb11724eef7a9d2d` |

I read the complete 1,546-line stage-2 section, its bibliography, process/protocol, and coverage material, with particular attention to all thirteen stage-2 canonical result rows and six substantive supporting rows. I revisited the stage-1 definitions, parity lemma, principal compression and shrinking lemmas, covariance identity and volume estimate, capacity lower bound, and shared-prefix construction. This builds on my complete stage-1 review; it is not a fresh whole-paper audit of the unrelated smooth material.

I compared relevant proofs and statements in the original finite covariance, correlated-budget, total-absolute-error, nonlinear-input-quotient, unconditional PSD-block, integer-feature, forest, and rational-construction results, together with the covariance certificate, commuting reduction, log-determinant oracle, and thin-domain supporting notes. I consulted selected original audits only after checking the manuscript arguments. I did not inspect every supporting note listed in the repository-wide inventory.

Primary-source checks used the supplied full-text cache: IQS Theorem 1.5 and Lemma 5.3; GGOW's rank and integral capacity statements; Zhang–Sra Corollary 8 and its one-step proof; Criscitiello–Boumal Proposition I.1 and its metric convention; GLS Definition (5) on printed page 172 and Theorem (3.1); and DPV Theorem B.5 with its ellipsoid convention. I checked the relevant imported interfaces, not the entirety of those external proofs. I did not conduct a new priority search, fully verify every bibliographic metadata field, compile the PDF, or implement the complete geodesic/ellipsoid algorithm.

## Assessment

I found no major mathematical defect in the reviewed stage. The finite covariance comparison, its grouped and absolute-error extensions, the rational feasibility repairs, and the domain-sensitive quotient arguments are coherent under their stated hypotheses. The rational noncommutative-rank preview now has the promised input-height proof. No new result is being accepted merely because an earlier audit called it correct.

The one finding below is a local wording defect; it does not invalidate the interior-ball argument or its algorithmic consequence. This review is bounded evidence, not a guarantee of correctness or novelty.

## Finding

1. **MINOR — identify the function whose variation is bounded.** Location: `sections/02-quadratic-finite.tex:1045–1048`, proof of `lem:block-logdet-oracle`. After bounding the norm of the independent-coordinate gradient by `8N/delta`, the text says, “Its variation is at most 1/4.” The nearest antecedent is the gradient, but the valid conclusion is that **the objective value** changes by at most `1/4` from its value at the center. A gradient variation bound of `1/4` is false: for one scalar block, `g(p)=log p`, `p0=delta/2`, and `sigma=delta/32`, the change in `g'` between `p0` and `p0+sigma` is `2/(17 delta)`, which can be arbitrarily large. In contrast, the required objective estimate follows by integrating the gradient bound along the segment: `|g(P)-g(P0)| <= (8N/delta) sigma <= 1/4`. Replace the sentence by that estimate or by “Thus g differs from its value at the center by at most 1/4.” The original supporting log-determinant-oracle note explicitly calls this an objective change. Classification: expository ambiguity, not a substantive proof gap.

## Mathematical checks and limits

- **Parity and measurability:** the lower proofs use closures of graph-input supports, not closures of the lifted feasible set. Continuity preserves each pairwise quadratic budget. Compact contacts are measurable and have attained coordinate extrema. Positive-volume contacts have positive definite covariance; zero-volume contacts are handled separately. None of these arguments bounds integer ranges or assumes that a parity class is convex.
- **Covariance constants:** the fourth-moment terms discarded in the scalar and grouped lower bounds are nonnegative after factoring a PSD budget for proof purposes. The unit-cube covariance cap is `nI/4`, and scaling by `max(4,n/4)` meets both cap and energy constraints. The general-domain comparison retains `log2 vol(Omega)`. The block proof correctly uses full contact covariance followed by the block determinant inequality, rather than assuming independence inside a contact.
- **Singular and correlated budgets:** the extension to a closed unbounded allowed-error set is stated explicitly. Its closure is sufficient for the parity step; compactness of the allowed-error set is not used there. Shared monomial errors produce a single symmetric error matrix, so correlated output budgets are controlled jointly. An identically zero measured energy gives an affine measured combination and can be omitted from logarithmic branches.
- **Rational construction:** the `2r` power in capacity scaling is correct. The rational-box volume bound uses a product of endpoint denominators. The Jacobi routine preserves exact orthogonality and reconstruction while controlling denominator growth. Near-active branch error and gradient error enter the recurrence at the actual stored iterate; projection and rounding are accounted for before telescoping. The final covariance repair and diagonal sandwich preserve feasibility by PSD-order monotonicity.
- **Oracle interfaces:** the cited GLS definition supplies distance to the original body and objective error relative to its full optimum, as the manuscript needs. The correlation repair has exact unit diagonal and PSD feasibility. The central-ball repair is an explicit convex combination of a feasible nearby point and a point in the known interior ball. DPV's alternative of a very small outer ellipsoid is excluded by the supplied inner radius; central symmetry removes its possibly nonrational center from both inclusions.
- **Domains and structured results:** the input quotient subtracts the affine output before projection, so affine variation along fibers causes no loss. Its zonotope normalization gives the claimed inner cube and volume penalty. Independent original blocks remain a product after separate quotients. The integer-feature minor estimate and forest face-image tiling give the stated volumes. The thin-domain example demonstrates why these restrictions matter.
- **Hardness:** the complement maximum-cut vertices force the zero-count threshold. Independent block choices give a pairwise incompatible packing of size `2^t`; appending the scalar square doubles it and makes the low-case optimum exactly one. Tolerance scaling and polynomial replication preserve the stated rational, convex, disjoint-block class. The conclusion properly excludes power-sublinear errors without claiming to exclude `N/log N`.

## Executed checks

An independent inline SymPy checker used exact rational arithmetic on 16 cases in dimensions 1–4 with 2–4 outputs and PSD budgets `W=C^T C`. It verified:

1. The grouped fourth-moment identity, including the two nonnegative discarded terms, for centered discrete distributions and independent copies.
2. The shared-grid correlated-error inequality `e^T W e <= E(P)/64` for rational scaled Hessians and symmetric normalized errors.

All 32 checks passed. The discrete distributions check the algebraic moment identity, not a positive-volume assertion. These computations supplement the proofs and do not test the complete rational optimization algorithm. No manuscript or research file was edited; only this report was written.
