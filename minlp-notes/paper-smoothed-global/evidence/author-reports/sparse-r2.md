# Author report: sparse and constrained sections, round 2 (Opus)

Author: Opus, sparse/constraint block. Date: 2026-10-06.

This report records what the interrupted Opus round-2 task did, the state
of the four owned files now, and a read-only check of the final text
against the round-2 requirements. It is not a review and claims no final
approval.

## 1. What happened

1. The round-2 task started from `sparse-r1.md`, the prewrite, early and
   complete Sol sparse/domain reviews, and the live integration contract.
   It made partial live edits to `sections/05-sparse.tex` and
   `sections/06-constraints.tex`: the all-fixed branch, the descriptor
   wording, the B10 proposition `prop:sp:conditional`, the companion
   comparison and moment paragraph (editorial P2), the gradient-rule
   wording, the hardness scope, the uniform-family premises, the actuator
   curvature `L=max{1,L_q+Lambda G_2}` with the rename `g_k -> chi_k`
   (also in Appendix D), and the simplex section text. It then stopped at
   the Claude rate limit (`evidence/provider-limit-handoff.md`).
2. Under the user's fallback instruction, Sol completed the same block
   (`sparse-sol-final.md`). The final review
   `reviews/final-sparse-domain-sol-r1.md` passed it, and the root
   finalized the submission (`snapshots/final-submission-r4/`).
3. When this session resumed after finalization, I made six more edits
   before I noticed the finalization: three in `06-constraints.tex` (order
   introduction, order fallback wording, TU companion attribution) and
   three in `C-sparse.tex` (a zero-dimensional remark and a point case
   inside `lem:sp:gls`). Two of them conflicted with the final Appendix C:
   the remark cited a `k=0` convention that the final `lem:sp:bezout` does
   not state, and the point case contradicted the final note that the
   lemma concerns positive tangent dimension.
4. At about 01:53 local time I restored both files byte for byte from
   `snapshots/final-submission-r4/`. At that point all four owned files
   matched that snapshot and `delivery/artifact-manifest.json`:

| File | SHA256 |
| --- | --- |
| `sections/05-sparse.tex` | `df3ef7c7f7c08d415044d9d93e3f9daa9b8a5d6c301954b950c3130c6718f047` |
| `sections/06-constraints.tex` | `9467eb72e20f355b3afb70d844bfedcf0a7fe52ba8f53d2483327162ad9db898` |
| `appendices/C-sparse.tex` | `af2f5b1e8d1c193a3c7bef41a7e6606cbba44ed698301d7c2ca3f10213cb72e3` |
| `appendices/D-constraints.tex` | `c0b90de5054e469a278c2d09f560ce39a746c5b1025c79ecf4aee75ca0f4e66b` |

The reverted edits are kept only as a temporary reference in
`/tmp/sp-r2-postfinal/`; nothing depends on them. No other file was
edited, apart from this report.

5. Afterwards, at 01:55 and 01:57, the companion attribution addendum
   (`STATUS.md`, `attribution-addendum-review-brief.md`) changed
   `05-sparse.tex` (attribution in `prop:sp:conditional`) and
   `06-constraints.tex` (TU scope paragraph). Those edits are not mine, and
   I left them untouched. The live hashes of these two files therefore
   differ from the R4 manifest; `C-sparse.tex` and `D-constraints.tex`
   still match it. Line numbers below refer to the R4 snapshot.

## 2. Round-2 requirements in the final text

Line numbers refer to the final snapshot (`05`, `06`, `C`, `D` are the four
owned files). Status means present in the final text; the final Sol review
verified these proofs, and the rows marked "checked" I also re-read now.

| Requirement | Final location | Status |
| --- | --- | --- |
| 1. B10 conditional-recourse count | `prop:sp:conditional`, `eq:sp:conditional` (`05:601`) | Present, checked: fixed outside domain, certified interval plus feasible completion, incumbent updated before pruning, witness bound `f*+2(e_j+eta_j)`, deterministic tolerance `2(1+a)e_j` for the count, `M>=2^J`. Stated as an oracle interface, not an algorithm. The boundary corollary `prop:lim:conditional` (`09:297`) now derives from it by cross-reference. |
| 2a. Coefficient length and production cost | `lem:con:uniform` (`06:72`, premises `P_1,P_2` at `06:81`) | Present, checked. |
| 2b. Actuator curvature | `eq:con:Lact` (`06:477`) | Present, checked: `L=max{1,L_q+Lambda G_2}`. |
| 2c. All-fixed inputs | `05:38` (`n>=1`), step (0) of `def:sp:algorithm` (`05:967`); graph and actuator branches in `06` and `D:347` | Present. |
| 2d. Singleton-hull descriptor | `05:116`; model clause owned by the model author | Present in both. |
| 2e. Gradient rule versus singleton rule | `05:825` | Present, checked. |
| 2f. Order transport replaces (P1) | `06:24`, `lem:con:transport` (`D:753`) | Present. |
| 2g. Hardness comparisons | `05:1105` (only the checked treewidth-two family, via `rem:lim:dk`) | Present. |
| 3. Equality-budget multipliers excluded | `06:643`; `lem:con:simplex-close` (`D:495`), success proof, `lem:con:simplex-tail` (`D:594`) | Present, checked: only zero coordinates and tight inequality budgets are margin variables; equality multipliers are free and cancel in derivative differences. |
| 4. Coarse simplex mesh | `06:613`; `D:388` | Present, checked: vertices for `h>=1`, indices `0,...,m-1` for `h<1`. |
| 5. Empty blocks before the center formula | `D:544`-`D:560` | Present, checked. |
| 6. Point patches before GLS | `C:218`; `D:301` (implicit charts still refine roots and objective), `D:520`, `D:908`, `D:1047` | Present. |
| 7. Sharper order count, binary-before-exposure, full-hull derivatives, weighted `D^T D` metric, chart-lift feasibility, pre-draw budgets | Unchanged from round 1 and verified in the final review | Present. |
| 8. Complete-review S5 items | `D:48` (`min{n,k^{D_g}}`), `06:188` (irrational constant roots stay in the chart), `D:173` (`U_{-1}=+infinity`, stored point), `D:240`, `D:617`, `D:993` (empty stationary tuple) | Present. |
| Editorial P2 | `05:694`-`05:746`, `05:1131` | Present, checked against the companion source (Section 3). |

No dependent issue outside my files remains open for this block. The
shared-root fallback (`03`, `A`), the common descriptor clause (`02`), the
discussion's width question (`10:104`) and the boundary corollary (`09`)
were resolved by their owners, as the final reviews record.

## 3. Companion source check for the P2 paragraph

Sol's final author report left one item for the root and Luna: the exact
statements of `companion-decomposition-aware` used at `05:694`-`05:721`. The
root's final passage was later reconciled with Luna's evidence. I read the
repository's own companion manuscript (`paper-decomposition-aware/`, not
external literature) and found that the final passage matches it:

- `sections/abstract.tex`: `f(p,bar kappa)(I+q+1)^5` certified
  approximation, exact output in `f_1(p,kappa)I^{O(1)}` under point growth
  at a unique minimizer, `kappa >= bar kappa`, and the rETH limitation on
  an exponent `o(p)`.
- `sections/intro.tex`, `thm:intro-main` (lines 77-113): the formula
  `f(p,t)=c_0(c_1 p sqrt t)^p t(1+log_2 t)^2` and graded grids with
  `O(sqrt(bar kappa) log(n+2))` nodes per coordinate;
  `thm:intro-lower` (lines 215-249), including the companion's remark
  that its own exponent is `p/2+O(1)`.
- `sections/growth-sharp.tex`, `cor:uniformgrid` (line 33): at least
  `4k_0+5 >= sqrt((n-2)kappa)+1` nodes per coordinate for filtered uniform
  grids in the specified stages.
- `sections/recourse-local.tex`, `thm:cr-filter` (line 41): the
  deterministic filter that `prop:sp:conditional`(a),(b) reproduces.
- `sections/constraints.tex` (`sec:tu-rounding`, `thm:tu-states`): aligned
  totally unimodular rounding with deterministic node counts. The R4
  introduction attributes this overlap (`01:498`-`01:502`, pointing to
  `sec:con:scope`), and the attribution addendum is now adding a local
  statement to the TU scope paragraph (`06:789`).

## 4. Editorial notes not applied

The submission is frozen, so I did not apply these. None is a
mathematical defect.

1. `05:601`-`05:673`: the oracle error factor `a` appears next to the
   comparison spacing `a_i` in the same inequality (`05:673`). A different
   symbol for the error factor would read more easily.
2. `05:719`: "or rule out every smaller linear exponent in `kappa`" is
   unclear. A suggested reading: "or exclude exponents `cp` of `kappa`
   with `c<1/2`".
3. `D:411`: `rho=m-sum_i k_i` reuses `rho`, which is `1/(4B)` in the same
   appendix's schedules.
4. `D:544`-`D:557`: `beta_b` for a residual budget reuses the bag symbol.
5. `D:674`-`D:676`: `sigma_s` for slacks reuses the noise half-width.
6. `D:770`-`D:776`: interior groups are indexed by increasing value
   (`r_1<...<r_k`), but the next sentence gives the `l`th group the value
   `sum_{i>=l} lambda_i`, which decreases in `l`. The conclusion holds
   because each edge direction `d_l` is the indicator of one group; the
   simplest repair is to say exactly that.
7. `D:989`-`D:997`: `B` for a face basis reuses the fallback factor `B`.
8. `05:334`: `C_0` names a cell in `lem:sp:round`, while `05:155` uses
   `C_0` for the absolute constant of `thm:sp:main`. The Opus editorial
   review (`reviews/opus-editorial-r1.md`, notation table, lines 554-563)
   lists this and other overloads in these files (`b` for blocks, `k` as a
   time index, `Z`, `I_k`), and its item 11 (line 601) suggests folding
   `ex:con:actuator` into one sentence. I found no disposition of these
   items in the review-disposition files.

None of the six new findings of `reviews/opus-math-r1.md` (NEW-1 to
NEW-6) concerns this block. Its confirmed sparse/domain items are the
repairs listed in Section 2, all present in R4.

## 5. Checks actually run

- Read the four owned files, the final snapshot copies, Sol's final author
  report, the final sparse/domain review, the status, handoff, addendum
  brief and manifest files, the sparse-related parts of
  `reviews/opus-math-r1.md` and `reviews/opus-editorial-r1.md`, and the
  relevant companion source files with `cat`, `sed -n`, `grep`, `awk` and
  `diff`.
- Compared each owned file with `snapshots/final-submission-r4/` using
  `cmp`, and computed SHA256 values, which match the snapshot manifest and
  `delivery/artifact-manifest.json`.
- Re-derived the inequalities of `prop:sp:conditional` and the repaired
  simplex closure and margin statements by hand.

Not run in this session: any TeX build of the final files, project-wide
verification, CI inspection, experiments, literature search, commits or
delegation. These are targeted local checks and are distinct from the
root's final verification record.
