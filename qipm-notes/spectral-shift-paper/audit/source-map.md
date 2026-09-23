# Source map

The source notes are research records, not proof certificates. Every distinct
claim below must be verified, corrected, subsumed explicitly, or identified as
invalid with a mathematical explanation in the development audit.

All note paths below are relative to `../../workbench/active/`.

| Note (2026-09-04 prefix) | Stage and coverage |
|---|---|
| exact-two-cluster-shift.md | 1: exact two-point polynomial, robust cluster error, pairwise lower bound, interval construction, corrected condition-number inference |
| two-cluster-interval-shift-upper.md | 1: even-parity affine threshold, matching construction where valid, higher fixed-QSVT obstructions |
| adaptive-normalized-shift-hierarchy.md | 1: canonical oracle, globally nonnegative jet limit, arbitrary-coherent-circuit hierarchy, exact impossibility |
| normalized-shift-staircase.md | 1: exact Chebyshev thresholds and asymptotics, upper constructions including equality, coarse tier, GQSP and definite-parity separation |
| joint-accuracy-normalized-shift.md | 2: growing-order lower, contractive integrated-sign upper, high-accuracy matching, operational complement conversion |
| joint-accuracy-normalized-shift-lower.md | 2: Fejer--Riesz lower route, uniform finite-order control, unrestricted high accuracy |
| joint-accuracy-pinned-gate.md | 2: growing-degree endpoint-pinned upper, precise unresolved subpolynomial gap |
| sparse-lp-newton-access-separation.md | 3: genuine exact-central LP, normal-matrix versus rectangular-factor query cost, compiler transfers and sparse-value bypass |

## Context and overlap

- `../paper/sections/04-spectra.tex`, `05-beyond-kappa.tex`, and `12-preconditioning.tex`:
  access/normalization background. Existing conditioning or generic
  preconditioning claims are not contributions of this manuscript.
- `../conditioning-paper/sections/09-clustered-solves.tex`: two-cluster
  classical solve context, distinct from coherent reusable conversion.
- `../scalar-newton-paper/audit/source-map.md`: expressly excludes the
  normalized-shift project; its inverse-form bounds are not reproduced.
- `../conic-lift-complexity/audit/source-map.md`: expressly excludes spectral
  conversion. Cone geometry is outside the present paper.
- `2026-09-04-sparse-qipm-frontier.md` is a historical navigation ledger;
  its shift claims are routed through the eight theorem notes above.

The scalar-Newton directory was moved from the parent repository into `notes/`
by concurrent work during this task. Its content is left untouched here.
The broad paper's Theorem Q in Section 4 already distinguishes fixed-polynomial
inversion, full-query state preparation, dimension restrictions and factor
overlap. The new manuscript must preserve those distinctions: exact complement
conversion on a known two-point spectrum does not make all inverse-state tasks
constant-query. The plateau Schur-factor frontier archived on 2026-09-02 is
background about preprocessing and normalization, not a new shift theorem.

A second repository-wide search after Stage 2 checked unit-normalization,
plain-H, complement-compilation, and spectral-shift variants. The older broad
paper's Section 4 states the exact-subnormalization shift question and ties it
to Orsucci--Dunjko Section 4.3; this is the direct conceptual antecedent.
Section 13's implicit slack oracle, Section 5's effective spectral dimension,
the archived prefix-rigidified affine-correction separation, and the archived
winner-take-all trace family use normalization for different tasks. The
Hermitian-balance and one-cone SOCP notes concern cone encoding/scalar-output
problems covered elsewhere. None adds a missing spectral-shift theorem.
The concurrent scalar-Newton paper's coherent-access section now expressly
identifies normalized shifting as an additional access assumption, while
studying inverse forms. Its task and results remain distinct.

## Initial correction to investigate

The fixed-accuracy coarse logarithmic tier cannot include a degenerate high
band `[1,1]` without qualification. For K greater than (rho-1)/2, a bounded
quadratic can achieve O(delta) error on the low band and vanish at 1. The
high-band width and endpoint cases require explicit treatment.

## Final source-coverage ledger (Stage 4)

The labels below refer to the complete standalone manuscript. The source notes
were read and verified in their respective author stages; this ledger reconciles
their claim headings with those author audits and the final theorem statements.
No note is required to read the submission. The prefix for every note is
`2026-09-04-`.

| Source note | Final labels and retained content | Corrections, strengthening, or subsumption |
|---|---|---|
| `exact-two-cluster-shift.md` | `prop:two-point` (3.1), including exact quadratic and clustered error; `prop:pairwise` (3.3); `prop:no-exact` (3.2); `prop:even-upper` (4.9), `thm:staircase` (4.1) | The ratio-two sign-selector upper construction is subsumed by the general bounded constructions. A large condition number alone does not force expensive conversion. Pairwise constants include approximation error. Exact normalization-slack inequality is only a necessary formal bound: exact interval conversion is already impossible for every normalization below two. No approximate slack tradeoff is asserted. |
| `two-cluster-interval-shift-upper.md` | `eq:E1`, `prop:parity-lower` (4.8), `prop:even-upper` (4.9), `thm:even-staircase` (4.11), `prop:odd-optimal` (4.12) | Affine threshold and Fejer-kernel construction retained. Even lower bounds strengthened from unconstrained E_r to globally nonnegative F_r. Exact equality attained, F1=F2 plateau proved, exponent-3/4 lower improved to 5/6 below E1, and degree-six witness matches the concrete comparison. Odd order strengthened to include the logarithm. |
| `adaptive-normalized-shift-hierarchy.md` | `lem:scalar` (2.2), `thm:hierarchy` (4.4), `thm:thresholds` (4.2), `prop:threshold-asymptotics` (4.3), post-4.4 sublinear-error consequence; `prop:no-exact` (3.2) | Nonnegativity belongs to the limiting Taylor polynomial, not generally to a finite truncation. Complete coherent/adaptive scope and worst-case stopping assumption are explicit. Threshold characterization is replaced by exact formulas and unique stationary points. |
| `normalized-shift-staircase.md` | `thm:staircase` (4.1), `thm:thresholds` (4.2), `prop:threshold-asymptotics` (4.3), `lem:pinned` (4.5), `prop:threshold-upper` (4.6), `prop:coarse` (4.7), `lem:implementation` (2.1), parity results (4.11–4.12) | Strict-threshold unpinned construction is subsumed by the pinned equality-attaining construction. Global contractivity is proved in all regions. The integer threshold-index asymptotic has O(1), not o(1), rounding error. The coarse tier is logarithmic only for c<1; for c=1 it is nonzero constant in the general model. The GQSP comparison is against one definite-parity transform, and the concrete even comparison is strengthened to matched exponent 5/6. |
| `joint-accuracy-normalized-shift.md` | `eq:Hn`, `eq:H-asymptotic`, `thm:joint-exterior` (5.1), `prop:integrated-sign` (5.2), `thm:joint-matched` (5.3) | Exact sine target retained in the growing Taylor lower bound, so its error is uniform even when K is much smaller than delta squared. No upper spectral band is needed for the lower. Upper holds on the full [delta,1] interval. Complete complement law and arbitrarily fast log(1/K) growth included. |
| `joint-accuracy-normalized-shift-lower.md` | `lem:FR-remainder` (5.4), `thm:FR-margin` (5.5), `thm:FR-all` (5.6), `eq:FR-max`, `eq:FR-simple`, `thm:joint-matched` (5.3) | Independent Fejer–Riesz proof includes adaptive and fixed-radius branches. Finite-margin theorem states its index restriction; the half-threshold theorem removes an upper index restriction and covers arbitrarily high precision. Exact impossibility and operational access caveats retained. No dimension/sparsity-independent statement is made without the scalar continuum contract. |
| `joint-accuracy-pinned-gate.md` | `thm:joint-pinned` (5.7), `eq:uniform-pinned-gate`, `eq:uniform-tail`, `cor:joint-near-match` (5.8) | Exponential-in-index tail constants, including 2^(2r+4), retained explicitly. Both W and W delta P terms bounded on the high band. Global contractivity established separately. Regime r→infinity, r=o(log(1/delta)) retained. Original unspecified subpolynomial gap sharpened to O(r^2) away from upper tier boundaries, with an explicit margin factor near the boundary. No uniform multiplicative optimum is claimed. |
| `sparse-lp-newton-access-separation.md` | `prop:lp-center` (6.1), `thm:lp-state` (6.2), `thm:lp-compiler` (6.3), Section 6.5 | Genuine exact centrality, nontrivial feasible segment and objective, full normal/factor/right-side oracle unitaries proved. State target is explicitly dual; primal predictor is public. All right-side queries are counted and revealing exact norm data withheld. Direct amplitude estimation strengthens the source's suppressed-log factor upper to exact fixed-error Theta(delta^-1/2). Compiler is matrix-only. Public projectors make its coarse tier exactly zero, while all positive tiers transfer. Exact two-query factor complement, digital-entry bypass, and normalization-two bypass retained. No end-to-end LP/QIPM lower bound. |

The manuscript's new framing is in Section 1; its sources are primary
publications listed in `bibliography.bib`, not these notes. The proof roadmap
identifies the unitarity → nonnegative Taylor limit → extremal threshold →
pinned bounded construction chain. The conclusion explicitly records the
intermediate multiplicative gap, higher-even-threshold formulas, and
finite-precision synthesis as remaining questions.
