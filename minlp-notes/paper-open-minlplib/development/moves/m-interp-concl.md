# Moves from Sections 9, 10 and 11 to the supplement

Key: m-interp-concl. Files revised: `sections/09-interpretation.tex`,
`sections/10-reproducibility.tex`, `sections/11-conclusion.tex`.

## Result: no block needs to be pasted

None of the cut material needs to be pasted into the supplement. Every cut
fact that a claim depends on is still in the main text or already in a
supplement file. The table below lists where each one is. The supplement
editors only need to keep these passages when they condense their own files.

| cut from | material | still present in |
|---|---|---|
| §9 (old 9.4) | band theory: Theorem 9.1 (band identity), Proposition 9.2 (constant cells), Figure 7, the TODO on unread antecedents | **Deleted, not moved** (revision decision 2, D1). Appendix G no longer contains the proofs, and no file references the band labels. |
| §9.1 | prose descriptions of classes B to E | `tab:structure` (§9) and §5 |
| §9.1 | which validity result each staged certificate uses (Lemma 4.1, Lemma 4.2, Proposition 4.4) | `tab:staged` (§4) |
| §9.1 | affine split versus richer split class and windows (numbers-check item 5) | §4 (`04-split.tex`, opening of the section) and the introduction (C8). The wording fix of item 5 belongs to §4 (see the open issues). |
| §9.3 | interpretation of the `ann_cumene_tanh` gap (constrained cluster effect) | `B9-ann-kan.tex`, `app:annkan-ann-verif` (line 162); §5.5 |
| §9.3 | Chachuat et al. (2005): global dynamic optimization relaxes over state enclosures | Not claim-bearing. Still cited in `B4-chain-catmix.tex`. |
| §9.3 | Basu et al. (2023): branch-and-bound proofs versus cutting-plane proofs | Not claim-bearing. Dropped; the key is now cited nowhere. |
| §9.3 | "dtoc5 needs no state enclosures, because each stage term becomes a strictly convex quadratic once the multipliers are fixed" | §4 (`prop:dtoc5-identity` and its discussion) |
| §10 | per-result replay times of the old 21-row tier table | `tab:repro-register` (`I-reproduction.tex`; time and tier columns). Times outside the register are kept in the new three-row `tab:repro-tiers` (eg searches 3 to 8 min per part and step, eg_disc2_s search 3.4 h, ann verification 2.0 CPU-hours). Also in the supplement: powerflow0039 regeneration 316 s and 463 s (`app:repro-regen`), waterno2_06 "20 to 30 CPU-hours unloaded" (`B8-waterno2.tex`, line 301), eg "37 minutes with eight parallel jobs" (certificate box in `F-eg-rounding.tex`). |
| §10 | regeneration reproduces waterno2_06/09/12 exactly | `app:repro-regen` (`I-reproduction.tex`, line 212) and `B8-waterno2.tex` |
| §10 | 1,564 replayed waterno2_06 cell-slope tasks with identical status, bound and node count | `B8-waterno2.tex`, line 300 |
| §10 | topopt regeneration leaves the class, the margin and the display unchanged | `app:repro-regen`, "Audit" paragraph |
| §10 | the waterno2_06 path check and the pair-bound check can be run separately | `tab:repro-tiers` (path in Tier 2, pair bounds in Tier 3); `tab:repro-register` ("2 (path), 3 (pairs)") |
| §10 | MINLPLib and QPLIB models redistributed under CC BY 4.0 | "Statements and declarations" at the end of §11 |
| §11.1 | details of the SCIP mechanism (exact intersection of the propagated activity with the row bounds) | `obs:scip-propagation` (§8) and `app:solvers` |
| §11.1 | count of invalid bounds (19 listed per-solver bounds on 15 instances) | §7, abstract, introduction |
| §11.2 | per-family list of where mpmath is trusted | `tab:trust` (§2) and §2.5 |
| §11.2 | the camshape and hvycrash exact optima are decimal-model statements; the audit rerun with binary64 data (computed, one implementation) | `rem:sem-readings` (§2.1); `E-audit.tex`, line 554 |
| §11.2 | full list of unread sources (Floudas handbook 1999, the 2022 waterno2_04 paper, Arrow and Kurz, Murtagh and Saunders) | `app:literature-unread` (`D-literature.tex`) |
| §11.2 | campaign caveats (overloaded first batch, memory stops, no ranking) | §8.3 and `tab:solvers` |
| §11.2 | level-S certificates store no tree, so checking them means rerunning the searches | §10 |
| §11.1 | which shunts and taps the powerflow models omit | `app:semantics-provenance` (Appendix A) |

## Labels

- Removed, with no remaining references in any file: `sec:interpretation-band`,
  `thm:band-identity`, `prop:band-cells` and `fig:band-schematic`.
- Kept: `sec:interpretation`, `sec:interpretation-structure`,
  `sec:interpretation-evidence`, `sec:interpretation-reading`, `sec:repro`,
  `tab:repro-tiers` (cited by `I-reproduction.tex`, line 17), `sec:conclusion`,
  `sec:conclusion-recs`, `sec:conclusion-limits` and `sec:conclusion-open`.
- §11 now cites `tab:claims`, `prop:qplib-copies` and `prop:kan-scip` across
  documents. They resolve once the m-solvers moves are pasted into
  `H-solvers.tex`.
- §11 newly cites `app:egrounding-trust` (in the supplement) and
  `rem:sem-readings` (§2).
