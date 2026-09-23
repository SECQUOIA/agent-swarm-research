# Research notes and archive guide

## Authority

The paper in [`paper/`](paper/) is the authoritative source for the current
theorem statements, proofs, qualifications, corrections, and open problems.
Use [`paper/main.pdf`](paper/main.pdf) as the reading copy and
[`paper/main.tex`](paper/main.tex) with [`paper/sections/`](paper/sections/) as
the source.

The archived Markdown files are research records. They preserve supporting
derivations, alternative constructions, literature searches, computational
checks, abandoned directions, and pre-repair statements. They are not
independent current authorities. If an archived note conflicts with the
paper, follow the paper.

This classification records the repository state after the paper corrections
committed as `8ebc9ef` on 2026-09-04.

## Repository layout

- [`paper/`](paper/) contains the current paper and bibliography.
- [`workbench/active/`](workbench/active/) is for research currently being
  developed and not yet incorporated into the paper.
- [`workbench/parked/`](workbench/parked/) is for unfinished work that may be
  resumed.
- [`research-archive/2026-09-research-cycle/supporting-results/`](research-archive/2026-09-research-cycle/supporting-results/)
  contains detailed, generally valid notes whose main results are mostly in
  the paper but which retain useful supporting material.
- [`research-archive/2026-09-research-cycle/superseded-corrected/`](research-archive/2026-09-research-cycle/superseded-corrected/)
  contains precursors or notes with statements, proofs, hypotheses, or
  normalizations corrected by the paper.
- [`research-archive/2026-09-research-cycle/research-logs/`](research-archive/2026-09-research-cycle/research-logs/)
  contains chronological ledgers, outlines, redirects, and exploratory work.
- [`scripts/`](scripts/) contains computational checks associated with results
  now presented in the paper.
- [`formal/`](formal/) contains Lean proofs and an axiom audit. The
  [fixed-preconditioner report](formal/PRECONDITIONER.md) verifies the signed
  path minimax theorem for every invertible congruence factor and the matching
  identity upper bound for all signed paths. Exact witness summation improves
  its lower bound to `(4m²−1)/3` for every positive dimension. The
  [coupling verification report](formal/COUPLING.md) records the exact-center
  Newton coupling law, its regularity boundary, and the sparse LP witnesses.
  It distinguishes the constant coordinate direction from its limiting
  slow-eigenspace amplitude and states the decoupled normalization range.
  The [QCPM verification report](formal/QCPM.md) records the verified norm
  correction, its correspondence to the original v2 algorithm, and its scope.
  The [mixture verification report](formal/MIXTURE.md) maps the sparse
  convex-mixture and scalar-centrality claims to Lean proofs, including
  stronger multibit and KKT bounds and the corrected counterexample scope.
  The [SDP mixture report](formal/SDP_MIXTURE.md) covers the noncommutative
  extension, actual symmetric-matrix coordinates, operator and Frobenius
  centrality under both centering conventions, and output soundness.
  The [refresh verification report](formal/REFRESH.md) maps the pathwise
  residual-certified refresh theorem to Lean proofs of its normalized
  residual estimate, exact scalar test, and sequential checkpoint count.
  It also corrects an acceptance-only assumption in the supporting OSS note.
  The [fractional SDP spectrum report](formal/FRACTIONAL_SDP.md) verifies
  the unique log-det center, actual Frobenius-metric Hessian, all four
  ordered eigenvalue asymptotics, and the restricted spectrum. It supplies
  the exact constant `2√2/7` behind the main paper's former numerical `0.40`.
  The singularity-degree, diameter, and arbitrary-barrier claims remain
  outside this formalization's scope.
- [`scripts/paper-audit/`](scripts/paper-audit/) preserves the numerical
  reproduction programs from the completed pre-repair paper audit.

## Useful material not stated fully in the paper

The paper contains or strengthens every mature headline theorem from the
archived cycle. The following material remains useful but is absent from the
paper or appears there only in a substantially compressed form.

| Topic | Material retained outside the paper |
|---|---|
| Multibit KKT mixture frontier | The [multibit supplement](research-archive/2026-09-research-cycle/supporting-results/2026-09-02-single-flip-mixture-frontier-sparse-lps.md) includes the multibit primal--dual KKT extension with row- and column-input-degree accounting and an exact nonuniform-weight residual/centrality counterexample. The current paper and [Lean report](formal/MIXTURE.md) supersede its one-bit KKT constant, sharpen the multibit primal bound, and distinguish common-parameter from point-centered instability. The archived arbitrary-weight example and multibit KKT extension are outside that formalization's scope. |
| Bounded-scale parallel Newton construction | The [parallel initialization note](research-archive/2026-09-research-cycle/supporting-results/2026-09-02-robust-parallel-newton-initialization.md) combines a rational public centered start, one exact Newton correction to a true center, and a constant-relative-residual robust update contract in one bounded-scale family. Later paper results dominate individual parameters but not this exact conjunction. |
| SDP central mixtures | The [Kantorovich note](research-archive/2026-09-research-cycle/supporting-results/2026-09-02-sdp-central-mixture-kantorovich.md) retains detailed derivations and additional specializations. The current paper and [SDP Lean report](formal/SDP_MIXTURE.md) cover weighted residuals, the sharper signed KKT constant, multibit dependence, matrix and trace variance, and both centering conventions. The sharp worst-case Frobenius ratio criterion concerns common-parameter centering; for point centering it is sufficient. |
| Row-three winner-take-all formulation | The [early global-trace SDP note](research-archive/2026-09-research-cycle/superseded-corrected/2026-09-02-winner-take-all-global-trace-sdp.md) contains a distinct binary summation-tree formulation with maximum scalar row sparsity three, exact rank/nullity counts, and a treewidth-one scalar KKT graph. Its self-concordance argument is superseded, so only the structural construction should be reused. |
| Beyond-pair full-KKT obstruction | The [orthogonal-copy note](research-archive/2026-09-research-cycle/supporting-results/2026-09-02-beyond-pair-full-kkt-obstruction.md) retains the full cyclic-rotation LP realization, positivity and hard-mass calculations, saddle spectrum, coherent-codeword extension, and failed-construction ledger. |
| Block-angular module | The [block-angular note](research-archive/2026-09-research-cycle/supporting-results/2026-09-02-block-angular-qipm-frontier.md) gives the full inverse-decay/resolvent proof, dense-row LP arithmetic, partial-minimization Hessian calculation, collision map, and source audit compressed in paper Section 13. |
| Partition-free spectral construction | The [spectral face-repair note](research-archive/2026-09-research-cycle/supporting-results/2026-09-02-partition-free-spectral-face-repair.md) records the formulation-dependence of the coordinate selector and a conditional high-eigenvalue/Davis--Kahan construction for the dual range. It is not a selector-free end-to-end method. |
| Exact crossover details | The [tall-LP crossover note](research-archive/2026-09-research-cycle/supporting-results/2026-09-02-exact-quantum-crossover-tall-lp.md) retains the localization and bit-bound proofs, exact query/gate ledgers, sublinear regimes, and a direct-sum lower-bound construction. The paper correctly treats this only as a supporting module. |
| Conditioning evidence | The archived [barrier note](research-archive/2026-09-research-cycle/superseded-corrected/2026-09-02-barrier-independent-conditioning-dichotomy.md), [Netlib survey](research-archive/2026-09-research-cycle/supporting-results/2026-09-02-netlib-conditioning-survey.md), [RHS-alignment note](research-archive/2026-09-research-cycle/supporting-results/2026-09-02-newton-rhs-spectral-alignment.md), and [two-cluster audit](research-archive/2026-09-research-cycle/superseded-corrected/2026-09-02-two-cluster-central-hessian-benign-kappa.md) preserve explicit constants, fitting mechanics, failed approaches, correction history, and script mappings. Their interpretations are superseded by paper Sections 3--4. |
| LP and preconditioning proof details | The [bounded-data note](research-archive/2026-09-research-cycle/supporting-results/2026-09-02-bounded-range-exact-only-condition-one-hardness.md) retains exact-dimension padding; the [dual-homogeneity note](research-archive/2026-09-research-cycle/supporting-results/2026-09-02-dual-homogeneity-bounded-full-kkt-lower-bound.md) retains the full matrix and precision argument; and the [parity-preconditioner note](research-archive/2026-09-research-cycle/supporting-results/2026-09-02-parity-preconditioner-dichotomy.md) retains detailed central normal-matrix and amortization calculations. |
| Tree loading and SDP rank | The [tree-holonomy note](research-archive/2026-09-research-cycle/supporting-results/2026-09-02-block-treewidth-output-matching.md) includes per-coordinate and gate/workspace counts. The [rank-progress note](research-archive/2026-09-research-cycle/supporting-results/2026-09-02-sdp-newton-rank-progress-barrier.md) includes local cumulative-scalar encodings, initialization details, and the complete calculation ledger. |
| Condensation and state-conversion refinements | The [winner central-path note](research-archive/2026-09-research-cycle/supporting-results/2026-09-02-winner-central-path-condensation.md) retains arbitrary-schedule and physical-distance asymptotics and a separate `G=2` argument. The [collision note](research-archive/2026-09-research-cycle/supporting-results/2026-09-02-symmetric-block-resource-collision-lower-bound.md) states explicitly the nonconstant-gap consequence `q = Omega(L Delta^2)`, which is only implicit in the paper. |
| Structural and multiplier details | The [cut-resistance note](research-archive/2026-09-research-cycle/supporting-results/2026-09-02-cut-resistance-frontier-signed-parity-lps.md) retains full-row-rank/tree regularity. The [multiplier note](research-archive/2026-09-research-cycle/supporting-results/2026-09-02-signed-copy-cut-multiplier-conservation.md) retains the exact signed-path multiplier profile, redundant-row qualifications, and repeated-incidence design ledger. The [involution note](research-archive/2026-09-research-cycle/supporting-results/2026-09-02-involution-central-work-identity.md) retains compact-group Hessian and self-concordant bounds. |
| Unpromoted research leads | The [Hamiltonian research log](research-archive/2026-09-research-cycle/research-logs/2026-09-02-hamiltonian-qipm-research.md) is the only record of the pattern-only `2`-to-`1` value-lower-bound idea and connected diamond-flow output hierarchy. These are preliminary leads, not established results. |

The supporting-results directory also preserves longer proofs, oracle
constructions, edge cases, numerical checks, and dated novelty searches for
results that the paper already states. These records may be useful when
preparing an appendix or responding to review, but they should not be cited in
place of the paper.

## Corrected or unsafe archived notes

The following notes are especially important not to treat as current:

- The [projective-lazy refresh note](research-archive/2026-09-research-cycle/superseded-corrected/2026-09-02-projective-lazy-quantum-newton-refresh.md)
  contains a false implication from leakage and forcing ledgers to bounded
  realized projective variation, an incorrect projected dual identity, and a
  superseded sharpness calculation. Paper Section 13 contains the repaired
  statements.
- The [holonomy winner-take-all note](research-archive/2026-09-research-cycle/superseded-corrected/2026-09-02-winner-take-all-global-trace-holonomy-sdp.md)
  and the early row-three formulation apply a standard self-concordant
  full-step estimate at barrier weight `1/G`. Paper Section 7 replaces that
  invalid argument with a direct decrement calculation.
- The [zero-versus-k note](research-archive/2026-09-research-cycle/superseded-corrected/2026-09-02-zero-versus-k-verified-sample-state-conversion.md)
  has an obsolete M-2 detuning proof when `epsilon << delta`. Paper Section 8
  supplies the corrected two-regime construction and logarithmic dependence.
- The archived beyond-condition-number notes use an overbroad intermediate-power
  claim or an unanchored shell definition. Paper Section 5 imposes the needed
  analyticity and bottom-anchored cumulative spectral law.
- The [compressed-dual note](research-archive/2026-09-research-cycle/superseded-corrected/2026-09-02-partition-free-compressed-dual-qipm.md)
  assumes the wrong outer error contract and omits a forcing factor and
  terminal solve. Paper Section 13 gives the corrected composition.
- The [Walsh note](research-archive/2026-09-research-cycle/superseded-corrected/2026-09-02-walsh-row-resistance-frontier.md)
  omits a capped-optimum or coefficient-floor hypothesis that the paper adds.
- The [prefix hostile audit](research-archive/2026-09-research-cycle/superseded-corrected/2026-09-02-prefix-rigidified-condition-one-audit.md)
  says the reduced right-hand side is hidden. Paper Section 9 shows that the
  complete reduced solve is public in the Moore--Penrose gauge and locates the
  hardness in the affine particular correction.
- Several archived notes use a legacy Hessian normalization containing an
  extra factor of the central parameter. The current paper distinguishes the
  barrier Hessian from its scaled Newton-system occurrence.

## Local literature

The literature corpus is stored locally in `literature/` and is intentionally
excluded from version control. It contains source papers, extracted text,
bibliographic data, and literature syntheses. The paper's committed
bibliography remains in [`paper/bibliography.bib`](paper/bibliography.bib).

Repository documentation does not link to individual files in `literature/`,
because the directory is optional and will not exist in a fresh clone.

## Audit history

The full 2026-09-03 pre-repair audit was removed from the working tree after
all 24 verified repairs were incorporated into the paper. It remains
recoverable from repository history, for example with
`git show 8ebc9ef:2026-09-03-paper-audit-findings.md`.

The small reproduction programs remain in [`scripts/paper-audit/`](scripts/paper-audit/):
`wta_newton.py` checks the winner-take-all decrement normalization;
`cyc.py` and `cyc2.py` check the projective-variation counterexample;
`sec11_hred.py` checks the Section 11 Hessian scaling;
`sec6_visibility.py` checks the condensation visibility calculation; and
`deg2.py` checks the four-window spectrum.

## Workflow for new research

Create new development notes in `workbench/active/` using a dated,
descriptive filename. Begin each note with at least:

```text
Status: Active exploration
Started: YYYY-MM-DD
Paper status: Not incorporated
Confidence: Preliminary
Question: ...
```

Move work according to its outcome:

- Keep ongoing work in `workbench/active/`.
- Move temporarily abandoned work to `workbench/parked/`.
- After incorporating a result into the paper, move its development record to
  `research-archive/.../superseded-corrected/`.
- Move a valid result intentionally omitted from the paper to
  `research-archive/.../supporting-results/` and add a concise entry above.
- Move failed or abandoned directions to
  `research-archive/.../research-logs/`.
- Place paper-review and correction records under
  `research-archive/audits/` with their reproduction scripts.

Update this file when a result becomes stable enough to preserve or when the
paper/archive authority boundary changes. Do not add every temporary
calculation to this index.
