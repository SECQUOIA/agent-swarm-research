# W3 report: coreB verifier

There were two verification passes over `sections/growth.tex`,
`sections/growth-sharp.tex` and `sections/appendix-growth.tex`. The details
are in "Verification (coreB verifier)" and "Verification (coreB verifier,
second pass)" at the end of `process/w3/reports/coreB.md`. This file gives
the six required parts for both passes. The assignment file
`assign/coreB-verify.json` does not exist, so the group file
`assign/core.json` (51 findings, shared with coreA) was used.

## (1) Adjudication (verifier verdict on the coreB rows)

"Confirmed" means the decision is justified and the fix is in the text.
"No coreB part" means no part of the finding touches the three coreB files.

| id | coreB status | verifier verdict |
|---|---|---|
| F10 | MODIFIED | Confirmed. Cor `cor:uniformgrid` is self-contained, and `constraints.tex`/`appendix-tu.tex` now cite it and `prop:sharp` instead of `prop:tu-tight`. Pass 2 adds "if that stage is run". |
| F11 | MODIFIED | Confirmed. `rem:cluster` deleted; a one-sentence pointer to Section 2 remains, and `related.tex` 98–108 holds the only comparison. |
| F12 | MODIFIED | Confirmed: 𝒢, Δ_𝒢, X', X^{(j)}, ĥ, ξ_t, ν, Q_k. No ℓ_i/l_i, B_i or σ clash remains. |
| F13 | ACCEPTED | Confirmed. No "Algorithm 1/2", "slope", "labels" or "geometric grid" remains. |
| F19 | MODIFIED (with F159) | Confirmed. TRIAL keeps an explicit incumbent x̂ = ℓ, U = F(ℓ), or a better known point. |
| F22 | no coreB part | Confirmed. |
| F26 | no coreB part | Confirmed by grep: no British spellings. |
| F28 | no coreB part | Confirmed. Section 5 uses k as the free parameter, κ̄ from the defining γ, and κ = max{1,L/g}. |
| F34 | ACCEPTED | Confirmed. The build has no overfull boxes. |
| F37 | no coreB part | Confirmed. |
| F38 | ACCEPTED | Confirmed. `rem:fpt` has the CONVENTIONS wording. |
| F41 | MODIFIED | Confirmed (as F12). |
| F47 | ACCEPTED | Confirmed: 12(2√(nκ)+1) is `thm:cells` with r=1, κ_S=κ. Pass 2 makes "polynomial for fixed p" precise. |
| F48 | ACCEPTED | Confirmed (as F11). |
| F51 | ACCEPTED | Confirmed. P≠NP, ETH and randomized ETH are attached to the right claims; no "must". |
| F57 | ACCEPTED | Confirmed. `lem:commonmesh` (G1)–(G5) is proved in App. A, and all consumers cite constants that it states. |
| F58 | no coreB part | Confirmed. |
| F59 | MODIFIED | Confirmed: chain states are ξ_t, and the objective is named Ψ_m as in `lim:prop:messages` (pass 2). |
| F61 | no coreB part | Confirmed. |
| F63 | no coreB part | Confirmed. |
| F65 | ACCEPTED | Confirmed. Numbered environments `alg:trial` and `alg:ct`. |
| F68 | MODIFIED | Confirmed. (c) Cor `cor:uniformgrid` is the single statement; (d) `ex:chain` is a pointer plus the proved rescaled κ bracket. |
| F70 | no coreB part | Confirmed. |
| F75 | ACCEPTED | Confirmed (as F47). |
| F83 | ACCEPTED | Confirmed. |
| F84 | ACCEPTED, no change | Confirmed. |
| F85 | ACCEPTED, no change | Confirmed. |
| F89 | MODIFIED | Confirmed. CONVENTIONS fixes the common mesh as h_j. |
| F91 | no coreB part | Confirmed. |
| F136 | no coreB part | Confirmed. |
| F139 | no coreB part | Confirmed. |
| F140 | ACCEPTED | Confirmed (resolved by the deletion). |
| F152 | no coreB part | Confirmed. |
| F155 | MODIFIED | Confirmed. Option 1 is correct, since R1's sentence would assert an unproved bound for TRIAL's θ=0 hull grids. Pass 2 adds "polynomial in I+q and κ for fixed p". |
| F156 | ACCEPTED | Confirmed, including +[i∈I_Z], the stage limit and the cap. |
| F157 | no coreB part | Confirmed. |
| F158 | no coreB part | Confirmed. |
| F159 | MODIFIED | Confirmed (as F19). |
| F160 | ACCEPTED | Confirmed. |
| F161 | ACCEPTED | Confirmed: φ(1)=16.21 > 15.85; the ceiling version holds for all m. |
| F162 | ACCEPTED | Confirmed. |
| F163 | ACCEPTED | Confirmed. |
| F164 | ACCEPTED | Confirmed. |
| F165 | ACCEPTED | Confirmed. Pass 2 adds m ≥ 2 for the grid-graph instance. |
| F166 | ACCEPTED | Confirmed. |
| F167 | ACCEPTED | Confirmed. |
| F168 | no coreB part | Confirmed. |
| F177 | no coreB part | Confirmed. |
| F181 | ACCEPTED | Confirmed. |
| F187 | no coreB part | Confirmed. |
| F204 | no coreB part | Confirmed. |

Changes made by the verifier:

* Pass 1 (8 items, listed in coreB.md):
  - CT with P = ∅ via Lemma `lem:dp`;
  - effective widths in the stage-J gap of `thm:approx`(a) and
    `lem:commonmesh`;
  - "at least of order √(nκ)" in growth-sharp;
  - Cor `cor:uniformgrid` without a cap and for stages "that end by
    filtering";
  - UC under point growth;
  - the centering paragraph;
  - `ex:family` grid graph m_1×m_2 and the 9/8 sentence;
  - `ex:chain` wording.
* Pass 2 (6 items, listed in coreB.md):
  - "if that stage is run" in Cor `cor:uniformgrid` and its proof;
  - "polynomial in I+q and κ for fixed p" for UC;
  - m = m_1m_2 ≥ 2 in `ex:family`;
  - the reason for the smaller constants of `lem:commonmesh` ((G2) is
    Euclidean, at the price κ ≥ κ̄);
  - Ψ_m and ς_t in the `ex:chain` proof;
  - "need to be close" in the centering paragraph.

## (2) Labels deleted or renamed

| label | status | references should become |
|---|---|---|
| `rem:cluster` | deleted (coreB, per CONVENTIONS) | none exist; `Section~\ref{sec:related}` |

New labels: `alg:trial`, `alg:ct`, `lem:commonmesh`. The verifier added,
deleted and renamed no labels.

## (3) Requests for other files

* **coreA (`setting.tex`, Table `tab:notation`).** In the row
  "$J$, $w(J)$, $w_i(v)$", add the second meaning of J:
  "grid interval (in Sections~\ref{sec:growth}, \ref{sec:constraints}
  and~\ref{sec:optsets} $J$ is also the stage limit), its effective width,
  largest width at node $v$". This repeats coreB's open request.
* The other coreB requests have been applied by their owners. The verifier
  confirmed this for `computation.tex`, `optsets.tex` (`alg:uc`,
  "TRIAL"/"CT"), `appendix-boundary.tex`, `exact-localized.tex`,
  `constraints.tex`/`appendix-tu.tex` and `limits.tex`.

## (4) New BibTeX entries

None.

## (5) Checks run (targeted, local; not CI)

* Pass 1: `coreB-verify-growth.py` (seeds 5, 11 and 29) and
  `coreB-commonmesh.py 101 15 40`; all held (details in coreB.md).
* Pass 2:
  - `python3 process/w3/checks/coreB-verify-ct.py 41 300` and `… 97 300`
    (logs `coreB-verify-ct-seed{41,97}.log`). These run the full CT
    schedule in exact arithmetic and check `thm:approx`(a)/(b), Definition
    `def:cert` (C1)/(C2) on the returned record, the termination trial, the
    denominators Γ_X2^α, the scalar facts, eq:logabsorb, the node formula,
    and an exhaustive integer check of `lem:graded`. A stress mode with
    reduced caps went through 556 aborted or failed trials. All assertions
    held.
  - `coreB-verify-growth.py 13 10` and `coreB-commonmesh.py 77 10 40` (logs
    `coreB-verify2-*.log`): all held.
* `latexmk -pdf -interaction=nonstopmode -outdir=build/coreB-verify main.tex`
  exited 0, with no LaTeX errors, no overfull boxes, and no undefined or
  multiply defined references.

## (6) Unresolved

* The J notation-table clash, which belongs to coreA (part 3).
* Local radii R and R_ij in Section 5 coincide in letter with the reserved
  R of Section 6. CONVENTIONS does not require a rename, so they are left
  unchanged.
