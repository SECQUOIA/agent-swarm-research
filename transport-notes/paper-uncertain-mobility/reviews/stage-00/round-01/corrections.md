# Corrections: Stage 00, round 01

Fixer: `paper_stage_fixer`, different from author `paper_stage0_author`. Date: 2026-09-07.

The input is the [reviewed manifest](snapshot.json), snapshot `1e46dddf69ca6d87bf8b3b56792a8e0181bb493a561d9ac29e4f4ba26b88bd5f`. The [coordinator adjudication](adjudication.md) accepts five groups of minor findings and no major issue. This correction record does not accept the stage.

| Accepted finding | Corrected locations | Correction and verification |
|---|---|---|
| R2-01; R3-02; ensemble part of R4-01 | `claims-map.md`, scope; `notation.md`, c and Δ entries | Defined the dimensionless circle of length 2π, squared cosine rate, uniform offset law with density 1/4, equal-bin endpoints and endpoint convention, observed bin index, and the unchanged per-bin budget. Checked compatibility with Δ=4/N and the existing dimensional conversion. |
| R2-02; R3-01; wall-drift part of R4-01 | `claims-map.md`, scope and M1; `notation.md`, velocity entry | Restricted reversibility to the transverse process, stated zero longitudinal wall advective drift, and distinguished axial molecular diffusion. The inventory now states the assumption needed for its mean-velocity expression without treating the Stage 1 derivation as completed. |
| R2-03; R3-03; R4-02 | `claims-map.md`, L4; `notation.md`, Gaussian entry | Replaced Gaussian A/B amplitudes by independent standard Gaussian ξ_1, ξ_2; updated the squared rate and lower-bound denominator. The area symbol A remains reserved. |
| R4-03 | `PLAN.md`, workflow step 2; `reviews/stage-00/author-handoff.md`, final paragraph | Required future manifests before dispatch, linked the existing round manifest, and distinguished the historical reviewed version from a future accepted corrected version. Preserved the present manifest and reviewer reports. |
| C00-01 | `claims-map.md`, prior-art paragraph | Replaced the broad exchange audit link by `../notes/singular-exchange-prior-art.md`; verified the target exists. |

The corrected document hashes are:

| File | SHA-256 |
|---|---|
| `PLAN.md` | `90d2262b58264d3c44bd68ed69897c787b7dddfde3594bdb4f445075db06c19e` |
| `claims-map.md` | `554c92b5cf919f03b1e5d7a43995e5437aad872f43213cc9f67fc0237a0c64c1` |
| `notation.md` | `a92d6a3d2e20f5e49e73a9441760f035cd4e7ecc322770e86dcee5d3dabe09d5` |
| `reviews/stage-00/author-handoff.md` | `2266e65545508bc559dc6c0c9169c26f35057021c23f5a54f8d7707e8aa14cdf` |

Verification: a Python check found all 43 local Markdown link targets in the four edited documents and confirmed that these are exactly the four source files differing from the reviewed manifest. Inline code was excluded from link parsing to avoid interpreting mathematical brackets as links. Running `latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex` in the manuscript folder exited successfully; the unchanged LaTeX scaffold was already up to date. No mathematical manuscript section or historical source note was changed.

New or clarified assumptions: the canonical ensemble and observation law, zero wall advective drift, transverse-only reversibility, and independent standard Gaussian amplitudes are now explicit. They identify the intended inherited problem; their mathematical consequences remain Stage 1 or Stage 2 obligations. No earlier substantive stage has been accepted.

Next action: coordinator verification of every minor correction and a separate acceptance record. The adjudication found no major issue, so it does not require a second five-reviewer round.
