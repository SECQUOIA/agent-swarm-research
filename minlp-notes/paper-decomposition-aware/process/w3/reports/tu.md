# W3 report: group tu (Section 8, Appendix "Coupling constraints")

Files edited: `sections/constraints.tex` (Section 8) and `sections/appendix-tu.tex`
(new appendix, `\label{app:tu}`, title "Coupling constraints: exact output and
deferred proofs"). No other file was touched. The check script is
`process/w3/checks/tu-checks.py`.

## Structure after revision

Main text, Section 8 (about 9 pages, previously 11):

- 8.1 Model (Def. `def:tu-model`, Rem. `rem:tu-curv`, Prop. `prop:tu-align`)
- 8.2 Feasible rounding (Def. `def:tu-domain`, Lemmas `lem:tu-round`,
  `lem:tu-allow`, Ex. `ex:tu-fullcurv`)
- 8.3 Filtering and certificates. TU-GRID is now `\begin{algorithm}` with
  `\label{alg:tugrid}`. Prop. `prop:tu-sound` follows it.
- 8.4 Node counts (Thm. `thm:tu-states`, Ex. `ex:tu-union`)
- 8.5 Complexity (Thm. `thm:tu-approx`), plus the claim paragraph in the
  wording of CONVENTIONS §5
- 8.6 Exact output, reduced to:
  - the scaled data;
  - the TU height constants `R_TU`, `Ω_TU`, `τ_TU` (`eq:tu-constants`);
  - the citation of `prop:accept` with `Ω'=Ω_TU`;
  - TU-EXACT as `\begin{algorithm}` with `\label{alg:tuexact}`; it absorbs the
    old procedure TU-REC as its steps (i)–(ii);
  - the statement of Thm. `thm:tu-exact`.
- 8.7 The uniform mesh: cost and non-uniform alternatives:
  - one paragraph citing `prop:sharp` and `cor:uniformgrid`, with the
    TU-GRID transfer in Lemma `lem:tu-uniform`;
  - Prop. `prop:tu-misaligned` (narrowed claim);
  - Ex. `ex:tu-sum`;
  - Rem. `rem:tu-bm` (Bienstock–Muñoz comparison only).

Appendix `app:tu`:

- D.1 Def. `def:tu-statpoly`, Lemma `lem:tu-statpoly`, Cor. `cor:tu-height`,
  with the Vavasis attribution.
- D.2 Lemma `lem:tu-snap`, and the remark on unrestricted multipliers with the
  `x_1-x_1^2` example.
- D.3 Proof of Thm. `thm:tu-exact` and Rem. `rem:tu-cf`.
- D.4 Lemma `lem:tu-uniform`, the node lists of the misaligned graded grids,
  and the verification of Ex. `ex:tu-sum`.

## (1) Adjudication of assigned findings

| id | verdict | reason | change made (tu files only) |
|---|---|---|---|
| F10 | MODIFIED | Duplicates removed where an existing result covers the TU case. The TU height lemma and TU snapping are not covered by Section 6, whose Lemma `lem:statpoly` uses principal minors and whose REC fixes coordinates; TU rows need a non-principal saddle-point system and row snapping. A common lemma for `{x: Mx<=d}` is the exact group's decision. `lem:cr-semiconcave` is not in my files. | `prop:tu-accept` deleted; Section 8.6 and the appendix cite `prop:accept` with `Ω'=Ω_TU`. `prop:tu-tight` deleted; Section 8.7 cites `prop:sharp`/`cor:uniformgrid`. The transfer to TU-GRID is the short Lemma `lem:tu-uniform`, derived from `prop:sharp` rather than reproved. The TU height and snapping lemmas moved to the appendix. |
| F11 | MODIFIED | Only `rem:tu-bm` is mine. | Kept only the technical Bienstock–Muñoz comparison (i)–(iv). Deleted the Hochbaum–Shanthikumar paragraph; that reference is still cited in `related.tex`. |
| F13 | ACCEPTED | Naming. | TU-GRID and TU-EXACT are numbered algorithm environments. TU-REC is no longer a separate name: it is now steps (i)–(ii) of TU-EXACT. "box algorithm" → "CT (Algorithm~\ref{alg:ct})". "states"/"points" for grid sizes → "nodes per coordinate". "labels" for the values of discrete coordinates → "values". Titles: "state counts" → "node counts". |
| F27 | ACCEPTED | Idioms. | "really incurred" → "is incurred"; "actually retained" removed in the rewrite of 8.7. |
| F30 | ACCEPTED | Undefined jargon. | "cell fiber" → "vertex decomposition of the polytope $\mathcal Q$" (after Lemma `lem:tu-round`) and "its intersection with the plane $x_1+x_2=x_3$" (Ex. `ex:tu-sum`). "XP factor" went with `rem:tu-hybrid`. |
| F32 | ACCEPTED | An unproved outline does not belong in the body. | `rem:tu-hybrid` deleted. `conclusion.tex` already states the open problem (front group). |
| F35 | MODIFIED | CONVENTIONS keep one paper. | All §8.6 proofs moved to the appendix. Algorithm boxes added. `prop:tu-tight` and `rem:tu-hybrid` removed. The misaligned-grid and `ex:tu-sum` verifications moved to D.4. |
| F36 | ACCEPTED (tu part) | The claim is false as stated. | Section 8 intro and the paragraph after Thm. `thm:tu-approx` follow CONVENTIONS §5 (details below). "Forced" no longer appears. The abstract and intro belong to the front group; both are already consistent. |
| F50 | ACCEPTED (tu part) | Same as F36. | Same as F36. |
| F58 | ACCEPTED | Symbol clash. | `P=ΔH` → `\hat H` (Sections 8.6 and D). The stacked matrix `M` → `\hat A`. |
| F59 | ACCEPTED | Symbol clash. | `S` → `\mathcal S`; projections `S_i` → `\mathcal S_i`. The scopes `S_a` are kept. |
| F62 | ACCEPTED | Nine letters had two meanings each. | Renames, all as R5 proposed except where noted: basis `N` → `\Xi_{\mathcal J}` (and `\Xi_0`, `\Xi_C`); `N_0` → `\mathcal I_0`; saddle matrix `K` → `\mathsf K`; stacked matrix `M` → `\hat A`; row set `E` → `\mathcal E` (its right side is written `(\hat b_z)_{\mathcal E}`, no `ε`); box width `W` → `s`; Lemma polytope `Q` → `\mathcal Q`; grid minimum `v_j` → `\mu_j`; fractions `θ` → `\vartheta`; step `τ` → `t`. In addition, the uncorrected min-marginals `M_i(t)` are removed: `m_i` is defined directly, so `M` no longer clashes with the messages. |
| F67 | MODIFIED | See F10. §8.6 now keeps only the TU constants, TU-EXACT and the theorem statement. | `prop:tu-accept` deleted. Theorem 7.18/7.46 are not mine. |
| F68 | MODIFIED (tu part) | R5 says "Corollary 5.6 applies verbatim with E_j". That is not literally true: the stage structure, mesh base η, union filter, constant allowance and the forced bag differ. | Replaced `prop:tu-tight` with a paragraph citing `cor:uniformgrid`. Lemma `lem:tu-uniform` (D.4) gives the transfer: the allowance `E_j` dominates the coordinate corrections, and the induction is that of the corollary. `computation.tex` already cites `cor:uniformgrid`. |
| F70 | ACCEPTED | Use Def. 3.2. | Set growth now refers to Def. `def:growth`, with constant `g_S`, and `κ_c=κ(\bar L,g_S)`. I kept the display `eq:tu-setgrowth`: it fixes the distance on `R^{n_c+n_d}`, and the label is cited six times. |
| F85 | ACCEPTED | Unify operation counts. | `O(p(|A|+n+N+m)K^p)` with `n=n_c+n_d`, in the DP paragraph and in Thm. `thm:tu-approx`. |
| F89 | MODIFIED | The finding allows η to stay the TU mesh unit. | `h_j=η2^{-j}` kept, with one sentence: "common to all continuous coordinates, with base η instead of s". No other η role occurs in my files. |
| F91 | ACCEPTED (no change in tu files) | The listed forward references are in `setting`, `grids` and `recourse` files. Section 8's only forward reference, to `lim:prop:constraints`, is required by the hardness claim. | None. |
| F96 | ACCEPTED | Overclaim. | Lines 12–15 rewritten: the full-Hessian price is necessary (Ex. `ex:tu-fullcurv`); the uniform-mesh price is incurred (8.7); two natural non-uniform alternatives give invalid bounds with curvature-only corrections. Lines 674–679 rewritten. Lines 729–730 → "Natural non-uniform alternatives fail, as follows." I also narrowed a further overclaim after Prop. `prop:tu-misaligned`. The old text said "no correction depending only on them and on the grids can absorb it". That is false: a rule that puts large corrections at the common nodes violates (8.5) and stays valid. The new text says "A correction that depends only on these and on the grids, and is small enough at the common nodes to satisfy (8.5), therefore cannot absorb it." |
| F99 | MODIFIED | Wrong part reference. The proposed clause "which holds for some g>0 when S={v*}" is not proved for TU feasible sets: Lemma `lem:unique-growth` covers box QPs only. | `rem:tu-cf` (now in D.3) assumes (8.3) with `\mathcal S=\{v^*\}` and cites Thm. `thm:tu-states`(c). Part (c) now states the hull localization explicitly; previously it appeared only in its proof. |
| F107 | ACCEPTED | Hardness reading. | "It is not fixed-parameter tractable. Its running time is not bounded by f(p,κ_c)poly(I+log(1/ε)): K^p contains the factor n_c^{p/2}, and Section 8.7 shows that this factor is incurred." The problem-level statement is kept separate: unless P=NP, via `lim:prop:constraints`. |
| F108 | MODIFIED | The width is renamed to `s` (reserved meaning), so `W` remains only the reduced denominator, as in `prop:accept`. A separate `W_F` is therefore unnecessary. | Row set → `\mathcal J`; saddle → `\mathsf K`; row basis → `\mathcal E`; Taylor variable → `t`; threshold → `τ_TU`. The right-side vector `ρ` is replaced by its expression, so `ρ` now means denominators only. `N` (basis) → `Ξ`; `d` (label bound) → `K_Z`; `d_z` → `\hat b_z`; `S` → `\mathcal S`. The `optsets`/`appendix-proximal` parts are not mine. |

Other changes made for consistency or correctness (not tied to one finding):

- **Symbol clashes with the notation table (`tab:notation`).**
  - Curvature subspace `\mathcal K` → `\mathcal W`; `\mathcal K` is reserved
    for retained coordinates.
  - TU domain `D` → `\mathcal D`; `D` is the correction sum.
  - Grid `N_j(D_i)` → `G_j(\mathcal D_i)`; `N` is the number of bags.
  - Basis `V` in `rem:tu-curv` → `\Xi_C`; `V` is the value function.
  - Projector `Π` → `Π_C`.
  - Gap `γ` in `prop:tu-misaligned` → `δ`; `γ` is weighted growth.
  - Denominator of η: `D_0` → `\Delta_\eta`.
  - In `ex:tu-union` and the snapping example, variables `(x,t,z)` →
    `(x_1,x_2,x_3)`; in Section 8, `z` denotes integer variables.
- **`thm:tu-states`(c)** now states the localization that `rem:tu-cf` needs.
- **TU-EXACT control flow.** The algorithm now says where to continue when
  the LP is empty or the test fails. It runs TU-GRID "without the stopping
  test of step (2)" instead of with ε = 0, which contradicts the input
  requirement ε > 0.
- **Claim paragraph after `thm:tu-approx`.** It states:
  - polynomial in I+log(1/ε) for fixed p when κ_c, s/η and r are polynomially
    bounded, under set growth with finitely many optimal values per
    coordinate;
  - `K_Z ≤ I`, because the sets `Z_k` are listed; this is why the label
    bound `d` of R9 is not a separate condition;
  - not FPT;
  - the level-0 grid has s/η+1 nodes per coordinate and, unless P=NP, cannot
    be removed: `lim:prop:constraints` gives instances with p=3, a unique
    minimizer and K_Z=2, with an affine objective, so that `\bar L ≤ g_S`
    gives κ_c=1.
- **Prop. `prop:tu-align` title:** "without enumerating $\mathcal Z$".

## (2) Labels deleted, moved or added

Deleted:

| label | references should become |
|---|---|
| `prop:tu-accept` | `prop:accept` with `Ω'=Ω_TU` (via `cor:tu-height`(b)). No reference remains in any file. |
| `prop:tu-tight` | `cor:uniformgrid` for the box phenomenon, or `lem:tu-uniform` for TU-GRID. No reference remains (`computation.tex` already cites `cor:uniformgrid`). |
| `rem:tu-hybrid` | Nothing; `conclusion.tex` states the open problem. No reference remains. |

Moved to `appendix-tu.tex`, labels unchanged: `def:tu-statpoly`,
`lem:tu-statpoly`, `cor:tu-height`, `lem:tu-snap`, `rem:tu-cf`.

New labels:

- `alg:tugrid`: TU-GRID, grids under TU coupling (Algorithm, Section 8.3).
- `alg:tuexact`: TU-EXACT, exact output with TU coupling; includes the
  former TU-REC as steps (i)–(ii).
- `eq:tu-constants`: the TU height constants `C_{\hat H}`, `R_TU`, `Ω_TU`,
  `τ_TU`.
- `lem:tu-uniform`: TU-GRID keeps at least √(2(n_c−2))+1 nodes per coordinate
  and builds a table with ≥ n_c^{p/2} entries for ε ≤ \bar L/64 on the box
  instance of `prop:sharp` with a redundant row; κ_c=2.
- `app:tu`: the appendix. Subsection labels: `app:tu-height`, `app:tu-snap`,
  `app:tu-exact-proof`, `app:tu-limits`.

Name change: the procedure "TU-REC" no longer exists. It is steps (i)–(ii)
of TU-EXACT. No other file uses the name.

## (3) Requests for other files

All current cross-references from other files to Section 8 resolve, and their
wording matches the revised statements. I checked `intro.tex` 235–253 and its
table row for `thm:tu-approx`; `conclusion.tex` 56–66; `limits.tex` 656–663;
`related.tex` 205–211; `exact.tex` 176–182; `grids.tex` 136–139; and
`computation.tex`. No change is required. Optional items:

1. **front (`related.tex`), optional.** The Hochbaum–Shanthikumar comparison
   was cut from `rem:tu-bm`. If wanted, add to the proximity-scaling sentence:
   "for totally unimodular matrices these methods also refine aligned grids
   inside windows around the previous scaled solution
   \cite{HochbaumShanthikumar1990}; in Section~\ref{sec:constraints} the
   window radius $\sqrt{n_c\kappa_c}\,h_j$ comes instead from growth and the
   rounding allowance."
2. **core (`setting.tex`, `tab:notation`), optional.** The row
   "$\bar L$ & directional curvature under coupling constraints" could read
   "$\bar L$, $\kappa_c$ & directional curvature under coupling constraints,
   $\kappa(\bar L,g_S)$".
3. **front (`intro.tex` table row for Thm. `thm:tu-approx`).** The row is
   correct as written: K = max{K_Z, s/η+1, r(5+2√(n_cκ_c))} bounds every
   level, including level 0. No change needed.

## (4) New BibTeX entries

None. All citations use existing keys: `Schrijver1986`, `HoffmanKruskal1956`,
`GrotschelLovaszSchrijver1988`, `BienstockMunoz2018`, `Vavasis1990`,
`DelPiaDeyMolinaro2017`.

## (5) Checks run

1. `cd process/w3/checks && python3 -B tu-checks.py`. Exact rational
   arithmetic; all PASS:
   - `ex:tu-fullcurv` for h ∈ {1/2, 1/3, 1/8};
   - `ex:tu-union`: growth ratio min 1/6 on a 61×61 rational sample; the
     largest absolute Hessian row sum is 12;
   - TU-GRID simulated exactly with the union filter on the instance of
     `prop:sharp`, η=1, \bar L=Λ+σ, for n_c ∈ {4, 6, 10, 18, 50, 100, 202},
     (Λ,σ) ∈ {(1,0), (3,1), (2,3/2)}, levels 0–13. At every level with
     (r+1)h_j ≤ 1 the next domain contains [−(r+1)h_j,(r+1)h_j] and has
     ≥ 4r+5 nodes, and the node count never exceeds the bound of
     Thm. `thm:tu-states`(b). Also checked: 4r+5 ≥ √(2(n_c−2))+1 and
     (√(2(n_c−2))+1)^2 ≥ n_c for even n_c < 2000;
   - `prop:tu-misaligned`, simple instance: δ=1/3, threshold 75/288 L,
     corrected minimum 743/9000 > 0 just above it;
   - `prop:tu-misaligned`, graded instance: the node lists printed in D.4, 11
     nodes each, common nodes {0,1}, gap at m=1/2, δ=27/1280, positive
     corrected minimum above the threshold;
   - aligned uniform grids violate (8.5) at the nearest common node;
   - `ex:tu-sum`: G={0,1,9/4,3}, corrections, the 7 feasible points with
     their values (min 31L/64), and the constant-allowance variant 53L/128;
   - snapping example: (1/2,1/2) with value 1/4;
   - Hadamard row bound ≤ (√2 n_c C)^{n_c} ≤ R_TU.
2. Hand re-derivations of every changed or moved proof:
   - Lemma `lem:tu-statpoly`(c) with `\mathsf K` and row norms;
   - `cor:tu-height`;
   - `lem:tu-snap`: slack ≤ 3τ/2, ψ ≤ 3/(8Δ_ηR_TU);
   - `thm:tu-exact`(a)–(c): the J_ex conditions h_j ≤ τ/(n_c√κ_c) and
     h_j ≤ 2/(Ω√(n_c\bar L));
   - `lem:tu-uniform`: the min-marginal comparison m_i^{TU}(a) ≤ m_i^{C_ρ}(a),
     the induction with ρ_j = min{1, 2(r+1)h_j}, and the ε ≤ \bar L/64
     reachability (4^J ≥ 8n_c ⇒ h_{J−1} ≤ (2n_c)^{-1/2} ≤ 1/(r+1));
   - the no-growth table size (s√(n_c\bar L/(2ε))+1)^p.
3. `latexmk -pdf -interaction=nonstopmode -outdir=build/tu main.tex`. The
   final run exits 0, with:
   - no `!` errors;
   - no undefined references to labels used in my files;
   - no overfull boxes in `constraints.tex` or `appendix-tu.tex`. The
     remaining overfull boxes are in `recourse-local`, `recourse-convex`,
     `optsets` and `appendix-moments`;
   - remaining undefined references only to `lim:prop:moments`, owned by
     limits;
   - multiply defined labels only `eq:setgrowth` and `rem:np`, which are not
     mine.

   Two intermediate runs failed in the bibtex step ("no \bibdata"). The cause
   was transient states of files being edited concurrently by other groups;
   the next run succeeded.

These are targeted checks only; no project-wide verification was run and no
CI status was inspected.

## (6) Unresolved

- **Section 6 still cites `lem:hadamard` as a separate lemma; Section 8
  does not depend on it.** If the exact group merges the height lemmas into
  one lemma for `{x: Mx<=d}`, Section 8.6 and Appendix D.1 could then cite
  that lemma with the TU constant instead of proving `lem:tu-statpoly`. I did
  not do this, because the current Section 6 statements are box-specific.
- **Hochbaum–Shanthikumar paragraph.** It was deleted from `rem:tu-bm`, as
  the task specified. The optional `related.tex` sentence is in request 1.
- **LP citation.** `\cite{GrotschelLovaszSchrijver1988}` for exact LP in
  TU-EXACT has no theorem number, as before. Section 6 cites Theorem 6.4.12
  of the same book; I did not verify that number, so I did not copy it.

## Verification (verifier for group tu)

Files verified and edited: `sections/constraints.tex` and
`sections/appendix-tu.tex`. No other file was touched. I checked every
assigned finding, re-derived every changed or moved statement and proof, ran
independent exact checks (`process/w3/checks/tu-verify-checks.py`), and
compiled the paper.

### (1) Adjudication review

| id | tu verdict | verification | change by verifier |
|---|---|---|---|
| F10 | MODIFIED | Confirmed. `prop:tu-accept` and `prop:tu-tight` are gone and nothing references them. Keeping the TU height and snapping lemmas is justified: `lem:statpoly`(c) uses principal minors and REC fixes coordinates, while the TU case needs a saddle-point matrix and row snapping. | none |
| F11 | MODIFIED | Confirmed. `rem:tu-bm` keeps only the Bienstock–Muñoz comparison; `HochbaumShanthikumar1990` is still cited in `related.tex`. | (iv) matched to the corrected size bound (see fix 4) |
| F13 | ACCEPTED | Confirmed: algorithm environments, names, "nodes per coordinate", "values". | first use in the appendix now reads "TU-GRID (Algorithm~\ref{alg:tugrid})" and "TU-EXACT (Algorithm~\ref{alg:tuexact})" |
| F27 | ACCEPTED | Confirmed. | none |
| F30 | ACCEPTED | Confirmed: "cell fiber" and "XP factor" are gone. | none |
| F32 | ACCEPTED | Confirmed; `conclusion.tex` states the open problem. | none |
| F35 | MODIFIED | Confirmed. | none |
| F36 | ACCEPTED (tu part) | Confirmed; the claim paragraph matches CONVENTIONS §5. The abstract and intro (front) are consistent. | paragraph tightened (fix 5) |
| F50 | ACCEPTED (tu part) | As F36. The no-growth size statement was not exact (fix 4). | fixes 4, 5 |
| F58 | ACCEPTED | Confirmed. | none |
| F59 | ACCEPTED | Confirmed. | none |
| F62 | ACCEPTED | Confirmed. Two clashes remained. | `δ` (determinant vs. grid gap) removed (fix 10); reserved `q` removed (fix 6) |
| F67 | MODIFIED | Confirmed: 8.6 keeps the constants, TU-EXACT and the theorem, and cites `prop:accept` (its current form takes the denominator bound `Ω'`). | none |
| F68 | MODIFIED | Confirmed that a separate TU-GRID proof is needed. The proof cited `prop:sharp` "with σ=0", but `prop:sharp` was changed concurrently and now has the parameter `g`. | fix 8 |
| F70 | ACCEPTED | Confirmed (`def:growth`, `κ_c=κ(\bar L,g_S)`). | none |
| F85 | ACCEPTED | Confirmed (matches `lem:dp` plus `m` row tables). | none |
| F89 | MODIFIED | Confirmed. | mesh sentence clarified (fix 2) |
| F91 | ACCEPTED (no change) | Confirmed. | none |
| F96 | ACCEPTED | Confirmed. The narrowed claim after `prop:tu-misaligned` is correct, and so is the claim that aligned uniform grids violate (8.5); both were checked exactly. | none |
| F99 | MODIFIED | Confirmed. Uniqueness implies growth is proved only for box QPs, so assuming growth is right. | feasibility check added to `rem:tu-cf` (fix 12) |
| F107 | ACCEPTED | Confirmed. The lemma gives at least `n_c^{p/2}` table entries with `κ_c=2`, `ε=\bar L/64` and `I=O(n_c log n_c)`, so no bound `f(p,κ_c)poly(I+log(1/ε))` holds. | wording (fix 5) |
| F108 | MODIFIED | Confirmed. | none |

### Fixes made

`sections/constraints.tex`:

1. **Opening sentence.** It said that the bound of `prop:cellwise` "rounds
   each coordinate". The proof of that proposition replaces coordinates by
   endpoints one at a time; the randomized rounding is the alternative proof
   that follows it. The sentence now says the bound "follows from rounding
   each coordinate independently to an endpoint of its grid interval".
2. **Mesh sentence.** It now reads "As in CT with a common mesh
   (Lemma~\ref{lem:commonmesh}), h_j is the same for all continuous
   coordinates; its base is the mesh unit η instead of s, so that every grid
   is aligned with the data."
3. **`ex:tu-union`.** "every coordinate x_3" is now "the coordinate x_3 of
   every block".
4. **Table size without growth (an error).** The old text said that the
   tables have at most `(s2^j/η+1)^p` entries, and
   `O((s√(n_c\bar L/(2ε))+1)^p)` at the last level. This is false in two
   cases:
   - `J=0`, where `ε≥E_0` and `s/η` can be large;
   - bags with discrete coordinates, where `K_Z` can exceed `s2^j/η+1`.

   The text now says:
   - a continuous coordinate has at most `s2^j/η+1` nodes at level `j`;
   - if `J≥1`, minimality of `J` gives `2^J<η√(n_c\bar L/(2ε))`;
   - so a bag of `p` continuous coordinates has fewer than
     `(s√(n_c\bar L/(2ε))+1)^p` table entries at the last level.

   `rem:tu-bm`(iv) now refers to a bag of `p` continuous coordinates.
5. **Claim paragraph after `thm:tu-approx`.** It is now a separate
   paragraph, with these changes:
   - "(s/η)" is written as a parenthetical, as in CONVENTIONS §5;
   - "It is not fixed-parameter tractable: its running time is not bounded
     by …, because …";
   - "NP-hard instances" is replaced by "instances … on which approximating
     OPT within 1/2 is NP-hard", which is what `lim:prop:constraints` proves.
6. **Section 8.6, linear coefficients.** They were written `q`, which
   `tab:notation` reserves for the accuracy `2^{-q}`; Section 8.7 also uses
   `poly(I+q)` in that sense. `F` is now written
   `\frac12v^THv+\nabla F(0)^Tv+F(0)`, and `c_z=\hat H_{xz}z+Δ\nabla_xF(0)`.
   No new symbol is introduced.
7. **`thm:tu-exact`(c), per-level cost.** Steps (i)–(iii) cost time
   polynomial in `I+j` at level `j`, not in `I`: they compare against
   `y^{(j)}` and `β_j`, whose bit lengths grow with `j`.

`sections/appendix-tu.tex`:

8. **Broken parameter in `lem:tu-uniform`.** The proof cited `prop:sharp`
   "with σ=0", but the current `prop:sharp` has the parameter `g` and the
   coupling `(Λ-2g)u_kv_k`. The proof now uses `g=\bar L/2`, for which the
   coupling vanishes and `κ=2`. I re-checked the proof against the current
   hypotheses of `prop:sharp`:
   - the subbox contains `[-ρ,ρ]^n`;
   - `w_i(0)≥h`;
   - `U≥0`;
   - the corrections are `Λw^2/8`.
9. **`lem:tu-uniform`, other changes.**
   - `r` is renamed `ν`. In Section 8, `r` is the number of optimal values
     per coordinate and a row index; `ν` matches `cor:uniformgrid`.
   - "point growth holds with g_S" is now "(8.3) holds with S={0} and
     g_S=\bar L/2".
   - The statement adds `n_d=0` and rational `\bar L`.
10. **`δ` with two meanings.** `δ=|det 𝖪|` (E.1–E.2) and the grid gap `δ`
    (`prop:tu-misaligned`, E.4) were the same letter. `lem:tu-statpoly`(c)
    now states the height as in `lem:statpoly`(c): "ρ^{-1}Z^{n_c} for an
    integer ρ with Δ_η | ρ and ρ ≤ Δ_η R_TU". The Hadamard step and the
    snapping proof were re-derived. The snapping proof needs Δ_η | ρ, so that
    `\hat b_z∈Δ_η^{-1}Z^{m'}⊆ρ^{-1}Z^{m'}`.
11. **Algorithm references.** The first uses of TU-EXACT and TU-GRID in the
    appendix now carry their algorithm references.
12. **`rem:tu-cf`.** `prop:accept` needs a feasible point, so the remark now
    says that a candidate is returned only if it is feasible and passes the
    test.

### Statements re-derived (no change needed)

These were checked line by line against the current text:

- `lem:tu-round`, `lem:tu-allow`, `ex:tu-fullcurv`;
- `prop:tu-sound`(a)–(e) and the checker claim;
- `thm:tu-states`(a)–(c), including the hull localization added for
  `rem:tu-cf`;
- `ex:tu-union`, `thm:tu-approx`, `prop:tu-align`, `rem:tu-curv`;
- `lem:tu-statpoly`(a)–(c), `cor:tu-height`, `lem:tu-snap` and the remark on
  unrestricted multipliers;
- `thm:tu-exact`(a)–(c), including the `J_ex` arithmetic;
- `rem:tu-cf`, `lem:tu-uniform`, `prop:tu-misaligned` and both of its
  instances, `ex:tu-sum`.

The hardness paragraph matches `lim:prop:constraints`. Its instances are
scaled by `a_0` (or use `η=1/a_0`), with:

- `s/η=a_0`;
- `p=3`, `K_Z=2`, `r=1`;
- the valid rational growth constant `g_S=1/((m+2)a_0^2+m+1)`, so
  `\bar L=g_S` gives `κ_c=1`.

The moved material keeps its labels and proofs: `def:tu-statpoly`,
`lem:tu-statpoly`, `cor:tu-height`, `lem:tu-snap`, `rem:tu-cf`, and the
proof of `thm:tu-exact`. Nothing proved was lost except the following, all
intended:

- `prop:tu-accept`, now `prop:accept` with `Ω'=Ω_TU`;
- `prop:tu-tight`, now `lem:tu-uniform`. Its constant `√(2(n_c-2))+1` is
  weaker than the old `2√n_c+1`, but no file quotes the old constant;
- `rem:tu-hybrid`, an unproved outline.

### (2) Labels deleted or renamed by the verifier

None.

### (3) Requests for other files

None required. The optional requests of the tu report stand.

### (4) New BibTeX entries

None.

### (5) Checks run

1. `cd process/w3/checks && python3 -B tu-verify-checks.py` (independent of
   `tu-checks.py`, exact arithmetic). ALL PASS:
   - the graded grids of Definition `def:graded` with centers 3/10 and
     7/10. The node list equals the printed one, and:
     - eleven nodes each;
     - the common nodes are {0,1};
     - the largest interval is 3831/20480;
     - (8.5) holds with m=1/2;
     - δ=27/1280;
     - the corrected minimum is positive above the threshold;
   - the simple misaligned instance: δ=1/3, threshold 75L/288, positive
     corrected minimum;
   - aligned uniform grids violate (8.5) at the nearest node (3 meshes × 3
     values of m);
   - `ex:tu-sum`: grid, corrections, the 7 feasible points, values, 31L/64,
     and the constant allowance 53L/128;
   - `ex:tu-fullcurv` for h ∈ {1/2, 1/3, 1/8};
   - `ex:tu-union`: growth ratio ≥ 1/6 on a 61×61 rational sample (minimum
     exactly 1/6), and row-sum bound 12;
   - exact TU-GRID simulation, union and hull variants, on the instance of
     `lem:tu-uniform`:
     - n_c ∈ {4, 6, 8, 10, 18, 50, 202}, p ∈ {1, 2, 3}, ε=\bar L/64;
     - the stated containment and ≥4ν+5 nodes hold at every qualifying level;
     - counts never exceed 5+⌊2√(2n_c)⌋;
     - level J−1 qualifies, and (nodes)^p ≥ n_c^{p/2};
     - the lemma's inequalities hold for even n_c < 2000;
   - Hadamard row bound |det 𝖪| ≤ (√2 n_c C)^{n_c} ≤ R_TU on 313 random
     nonsingular saddle matrices, with interval-matrix (TU) rows and exact
     determinants;
   - the snapping example returns (1/2,1/2) with value 1/4;
   - the counting in `thm:tu-states`(b), checked at random;
   - J ≥ 1 minimal ⇒ 2^J < η√(n_c\bar L/(2ε)), checked at random.
2. Every `\ref`/`\eqref` in the two files resolves to an existing label. No
   file references `prop:tu-accept`, `prop:tu-tight`, `rem:tu-hybrid` or
   `TU-REC`.
3. Build command:
   `latexmk -pdf -interaction=nonstopmode -outdir=build/tu-verify -jobname=tuverify main.tex`.
   - Result: exit 0; no `!` errors; no LaTeX warnings and no overfull boxes
     anywhere in the log.
   - I inspected the rendered pages of Section 8 and the appendix.
   - Note on the jobname: with the default jobname the build failed with
     "File ended while scanning use of \@@BOOKMARK". The cause was the
     repository-root `main.out`, which another process was rewriting at the
     time (`main.synctex(busy)`). pdflatex read that file. A separate
     jobname avoids it; it is not a source error.

These are targeted checks only; no project-wide verification and no CI
inspection.

### (6) Remaining

- **LP citation.** `\cite{GrotschelLovaszSchrijver1988}` in the remark
  after TU-EXACT has no theorem number (unchanged; not verified against the
  book).
- **Shared height lemma.** A single height lemma for `{x: Mx ≤ d}` shared
  with Section 6 remains the exact group's decision.
- **Local double meanings, kept on purpose.**
  - `ρ` is the height in E.1–E.3 and 8.6, and the cube radius in the proof
    of `lem:tu-uniform`. The radius matches `prop:sharp`/`cor:uniformgrid`.
  - `m` is the number of rows of `A`, and the minimizer coordinate inside
    the self-contained `prop:tu-misaligned`.

  Renaming would need symbols unused elsewhere in the paper and would read
  worse.
- **Appendix letter.** The current build letters the TU appendix "E";
  CONVENTIONS lists it as D. The order is set by the coordinator in
  `appendix.tex`.
- **`lem:tu-uniform` versus CONVENTIONS.** CONVENTIONS asks for
  `prop:tu-tight` to become a sentence. The main text has that sentence; the
  TU-GRID transfer needs its own proof (different filter, mesh base η,
  constant allowance), which `lem:tu-uniform` gives in the appendix. I
  consider this deviation necessary.

## Verification, second pass (verifier for group tu, 2026-10-03)

Files verified and edited: `sections/constraints.tex` and
`sections/appendix-tu.tex`. No other file was touched. The other sections
have not changed since the first verification pass (last modification 02:36),
so every cited statement was re-read in its current form: `prop:cellwise`
and the randomized-rounding paragraph, `def:corr`, `lem:dp`, `def:growth`,
`def:graded`, `prop:sharp` (parameter `g`, radius `h\sqrt{(n-2)\kappa/16}`),
`cor:uniformgrid`, `lem:statpoly`, `cor:height`, `prop:accept` (with `Ω'`),
`lem:snap`, `thm:transfer`, `lim:prop:constraints` and the paragraph after it.

### Adjudication review

I re-checked all 22 findings in `assign/tu.json` against the current text.
Every ACCEPTED fix is present and correct. The MODIFIED decisions (F10, F11,
F35, F67, F68, F89, F99, F108) and the no-change decision F91 are justified
for the reasons given in the table above. Points re-confirmed:

- **F36/F50.** The claim paragraph after `thm:tu-approx` matches CONVENTIONS
  §5. The NP-hardness instances fit Definition `def:tu-model` after scaling
  `y` by `a_0`, with:
  - `p=3`, `K_Z=2`, `r=1`, `s/η=a_0`;
  - growth constant `g_S=1/((m+2)a_0^2+m+1)`;
  - `κ_c=1` for `\bar L=g_S`.
- **F96.** No form of "forced" remains. The narrowed claim after
  `prop:tu-misaligned` is correct.
- **F107.** The text says that TU-GRID's running time is not bounded by
  `f(p,κ_c)poly(I+log(1/ε))`. Hardness is stated separately, via
  `lim:prop:constraints`.

| id | tu verdict | second-pass result | change |
|---|---|---|---|
| F10, F35, F67 | MODIFIED | confirmed | none |
| F11 | MODIFIED | confirmed | `rem:tu-bm`(iii)–(iv) made consistent with Section 8.5 (fix 3) |
| F13, F27, F30, F32, F58, F59, F62, F70, F85, F91, F96, F107 | ACCEPTED | confirmed | none |
| F36, F50 | ACCEPTED (tu part) | confirmed | none |
| F68 | MODIFIED | confirmed; `lem:tu-uniform` re-derived against the current `prop:sharp` | wording (fix 5) |
| F89, F99, F108 | MODIFIED | confirmed | none |

### Fixes made in this pass

1. **`rem:tu-curv`: the curvature bound must be positive.** The remark said
   that "the largest absolute row sum of `H_{xx}`" is a valid `\bar L`, and
   likewise for `Π_C H_{xx} Π_C`. Definition `def:tu-model` requires
   `\bar L>0`, and these row sums can be 0. Both sentences now read "every
   positive rational that is at least the largest absolute row sum of … is
   valid". The implication to coordinate curvature is now stated "for each
   `z∈𝒵`", since (8.2) is only assumed at integer `z`.
2. **Cost remark after TU-EXACT.** It said that steps (i) and (ii) take time
   polynomial in `I`. Step (i) compares against `y^{(j)}`, whose bit length
   grows with `j`, and `thm:tu-exact`(c) correctly says `I+j`. The remark now
   reads: "The large denominators of `y` enter only the comparisons that
   define `𝒥`. The rest of steps (i) and (ii) … takes time polynomial in
   `I`". The LP citation now carries the locator
   `\cite[Theorem~6.4.12]{GrotschelLovaszSchrijver1988}`, as in Section 6.
   R7 checked this locator against the full text ("All four locators
   correct"), which resolves the open item of the tu report.
3. **`rem:tu-bm` (iv) was false at `J=0`.** It said that a last-level table
   without growth has `O((s√(n_c\bar L/ε)+1)^p)` entries. When `J=0` the
   table has `(s/η+1)^p` entries, and `η` can be much smaller than
   `√(ε/(n_c\bar L))`. The item now says "if `J≥1`, … fewer than
   `(s√(n_c\bar L/(2ε))+1)^p` entries (Section 8.5)". This matches the
   corrected paragraph in 8.5.

   Items (iii)–(iv) wrote TU-GRID's accuracy as `\epsilon`, the glyph the
   remark uses for the Bienstock–Muñoz tolerance; Section 8 uses
   `\varepsilon`. TU-GRID's accuracy is now `\varepsilon`, and theirs stays
   `\epsilon`.
4. **Citations in `appendix-tu.tex`.**
   - `\cite[Section~2]{Vavasis1990}` becomes `\cite{Vavasis1990}`. As
     `reports/bib.md` notes, "Section 2" was checked only in the Cornell
     technical report, not in the IPL article. Section 6 also cites the
     paper without a locator.
   - Hadamard's inequality for rows now cites `\cite{HornJohnson2013}`
     without a locator, also as `reports/bib.md` suggests.
5. **`lem:tu-uniform`, precision.**
   - The statement now reads "at every level `j` with `(ν+1)h_j≤1` at which
     TU-GRID filters". Retention is claimed only at levels that end with
     step (3), as in `cor:uniformgrid`.
   - The proof called the uniform grid on `C_ρ` "a stage in the sense of
     Section 4". It now calls it "a grid for the subbox `C_ρ`", the object
     to which `prop:sharp` applies.

### Re-derivations (no change needed)

Each of the following was re-derived line by line:

- `lem:tu-round`, including the integrality of the right side, TU after
  appending unit rows, and part (c);
- `lem:tu-allow`, `ex:tu-fullcurv`, `prop:tu-align`;
- `prop:tu-sound`(a)–(e) and the checker claim;
- `thm:tu-states`(a)–(c), including `a_j^2=2E_j/g_S` and the lattice count;
- `ex:tu-union`, including the growth computation, the Hessian and
  `216n_b`;
- `thm:tu-approx`, including the bound on `J`, `K_0`, `K_j` and the
  denominators;
- `lem:tu-statpoly`(a)–(c), including the saddle matrix, Cramer's rule with
  `Δ_η|ρ` and the Hadamard chain `(2n_cC^2)^{n_c/2}n_c^{|ℰ|/2}≤(√2n_cC)^{n_c}`;
- `cor:tu-height`;
- `lem:tu-snap`, including `𝒥_0⊆𝒥`, slack `≤3τ/2`, and `ψ(x̃)≤3/(8Δ_ηR)`;
- the multiplier remark with `x_1-x_1^2`;
- `thm:tu-exact`(a)–(c), including both `J_ex` thresholds;
- `rem:tu-cf`;
- `lem:tu-uniform`: both induction cases, the comparison with
  `prop:sharp` at `g=\bar L/2`, `κ=2`, and the reachability bound
  `ν+1≤√(2n_c)`;
- `prop:tu-misaligned` and its two instances;
- `ex:tu-sum`: grid, corrections, seven points, `31L/64`, `53L/128`, and the
  triangle `(1,0,1),(0,1,1),(1,1,2)`.

CONVENTIONS compliance:

- algorithm names and environments are correct;
- the first uses of TU-GRID and TU-EXACT in the appendix carry algorithm
  references;
- the terminology is "nodes per coordinate", "table entries", "values";
- no filler words remain;
- the symbols agree with `tab:notation`.

### Checks run in this pass

1. **New end-to-end exact simulation.**
   - Command: `cd process/w3/checks && python3 -B tu-verify2-sim.py`.
     Exact Fractions, brute force over the grids. Result: ALL PASS.
   - *TU-GRID, union variant, on one block of `ex:tu-union`, levels 0–7.*
     It checks `β_j≤OPT≤U_j≤OPT+E_j` and `U_j-β_j=E_j`, that `𝒮⊆𝒟^{(j)}`,
     and that every retained point lies within `a_j+h_j` of `𝒮_i`. Node
     counts are at most 17, against the bound
     `2(5+⌊2√216⌋)=68`; the `x_3` domain splits into two intervals, as the
     example says.
   - *TU-GRID, union and hull variants, levels 0–10.* The instance has an
     order row and the unique minimizer `(1/3,1/3)`. The same checks pass,
     with at most 5 nodes, against the bound 9.
   - *TU-EXACT on a nonconvex QP.* The QP has one order row,
     `H=[[1,3],[3,1]]` (eigenvalues 4 and −2), `\bar L=4`, and `g_S=2`
     (proved by hand and checked on a sample). It was run with optimal
     values 0 (`Δ=18`) and 1/7 (`Δ=126`). Exact minimizers are returned at
     levels 18 and 26, before the threshold levels 36 and 50 of
     `thm:tu-exact`(c). `lem:tu-snap` holds at all 25 and 20 levels where
     its hypothesis `dist≤τ/(2√n_c)` holds. Those levels are not vacuous:
     the run continues past acceptance.
   - *TU-EXACT on a concave QP with `η=1/2` (`Δ_η=2`).* The QP has a sum
     row, and its unique minimizer `(1/2,1)` has a TU row and a bound row
     active. The exact minimizer is returned at level 12, and `lem:tu-snap`
     holds at all 41 levels that satisfy its hypothesis.
2. **Earlier checks, re-run.** `python3 -B tu-verify-checks.py` and
   `python3 -B tu-checks.py` both pass.
3. **Build.**
   - Command:
     `latexmk -pdf -interaction=nonstopmode -outdir=build/tu-verify2 -jobname=tuverify2 main.tex`.
   - Final result: exit 0; no `!` errors, no LaTeX warnings (including
     undefined references or citations) and no overfull boxes anywhere in
     the log.
   - The first invocation stopped with "pdflatex needed too many passes"
     while the labels settled after the edits. The second invocation
     finished cleanly, and so did a third after the last edits.
   - Rendered pages 51–53 (Sections 8.5–8.7) and 114 (E.3–E.4) were
     inspected.

These are targeted checks only. No project-wide verification was run and no
CI status was inspected.

### Labels, requests, BibTeX

- Labels deleted or renamed in this pass: none.
- Requests for other files: none required. The optional requests of the tu
  report stand.
- New BibTeX entries: none. The new citations use the existing keys
  `HornJohnson2013` and `GrotschelLovaszSchrijver1988`.

### Remaining

- **Appendix letter.** The build letters the TU appendix "E"; CONVENTIONS
  calls it D. The coordinator controls this through `appendix.tex`.
- **Shared height lemma.** One height lemma for `{x: Mx≤d}`, shared with
  Section 6, is still the exact group's decision; the current Section 6
  statements are box-specific.
- **Local double meanings, kept on purpose.**
  - `ρ`: height in E.1–E.3, cube radius in E.4. The radius matches
    `prop:sharp`.
  - `m`: number of rows, and the minimizer coordinate in
    `prop:tu-misaligned`.
  - `r`: number of optimal values per coordinate, and a bound row index.
  - `a_j`: a localization radius here; in `lem:inv` (Section 5) `a_j`
    means `n_Pη_j^2`.

  None of these is in `tab:notation`, and each is defined where it is used.
- **`lem:tu-uniform` instead of a one-sentence pointer.** CONVENTIONS asks
  for a sentence pointing to `prop:sharp`. That sentence is in the main text.
  The proof that the bound carries over to TU-GRID stays in the appendix,
  because TU-GRID differs from the setting of `prop:sharp` (different
  filter, mesh base η, constant allowance). I consider this deviation
  necessary.
