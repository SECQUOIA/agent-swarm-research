# W3 report: group coreA (Sections 3 and 4)

Files edited: `sections/setting.tex`, `sections/setting-growthcert.tex`,
`sections/grids.tex`. No other file was touched (check scripts are in
`process/w3/checks/coreA-*.py`).

## Summary of changes

- **Definition 3.2 (`def:growth`)** now defines point growth `(g, κ)`, weighted
  growth `(γ, κ̄)` and set growth `(g_S, κ_S)` (new `eq:setgrowth`), with the
  convention `κ(L',g') = max{1, L'/g'}`. Each condition number comes from some
  valid constant, and every statement holds for each valid constant. The text
  after the definition states how the three notions relate (point ⇒ set with
  `κ_S = κ`; point ⇒ weighted with `κ̄ ≤ κ`, including the case `L = 0`). A
  footnote separates our κ from the κ of Del Pia–Khajavirad Lemma 20.
- **"Unique minimizer" and "g exponentially small" (R1 m2, m3).** Both are
  replaced. The replacement is a proved two-variable example
  (`F = (x1−x2)² + 2^{-k}x1²` on `[0,1]²`, input length `O(k)`) with
  `κ ≥ 2^{k+2}` and `κ̄ > 2^{k+2}`.
- **Lemma `lem:growthcert`.**
  - It now holds on mixed boxes. Index sets are `J_0` (continuous coordinates
    strictly inside, the same meaning as `J_0(s)` in Section 6) and `J_∂`
    (coordinates at a bound).
  - In (a), the Euclidean growth constant is `g_0`, the proof uses `ζ^T d`
    (typo `ℓ^T d` fixed), and the integer-coordinate certificate
    `μ_i = −|ζ_i|`, which was previously only in the remark, is now part of
    the lemma and proved.
  - (b) now also covers weighted growth: `H_{J0J0} ⪰ 2γ diag(L_i)_{J0} ⪰ 0`.
    So the scope statement is proved for the hypothesis that the main bounds
    actually use.
- **Remark `rem:nonconvex`** now holds the growth-scope wording of CONVENTIONS
  §5, kept in one place. It says "positive definite" under point growth and
  "positive semidefinite" under weighted growth. The planted-instance sentences
  were removed; Section 11 already describes the family (see request C1).
- **New §3.4 "Notation" with Table `tab:notation`** (booktabs, `\small`, 22
  rows).
- **Section 4.**
  - Notation: subboxes `X'`, filtered subbox `X''`, stage boxes `X^{(j)}`;
    grid intervals `J`, effective width `w(J)` (was `Δ_i(I)`).
  - Terms defined: "nodes", "nodes per coordinate" and "table entries".
  - Degenerate subboxes are allowed, with the grid interval `[a,a]`.
  - `prop:cellwise` gains the node bound `F(x) ≥ m_i(v) + d_i(v)`. A new
    paragraph states the form for families of intervals, so Lemma `lem:cells`
    (Section 9) is an instance.
  - The randomized-rounding remark now carries its own short proof.
  - Lemma `lem:dp` states the total `O(p(|𝒜|+n+N)K^p)`.
  - Def `def:filter` requires `U ≥ β`. Prop `prop:filter` is restated and
    shows that `X''` is a subbox.
  - (C1) uses the interval hull and has a second alternative for unit integer
    intervals (label filter).
  - The checking cost is stated precisely.
  - Prior-work text is cut to the technical comparison. Credit to Bajaj–Hasan
    stays, and `prop:cellwise` is called an observation in prose.

## (1) Adjudication

"Not in coreA files" means that no part of the finding touches
`setting.tex`, `setting-growthcert.tex` or `grids.tex`. coreB, or the owner
named in the row, handles it.

| id | status | reason | change made (coreA files) |
|---|---|---|---|
| F10 | MODIFIED (coreA part) | The height, snap and accept lemmas belong to exact/tu/recourse. The coreA part is the "three Jensen proofs". | Section 4 keeps one short, self-contained rounding proof. A new "Families of intervals" paragraph makes `prop:cellwise` apply to unions of cells, so `lem:cells` and `lem:cr-cell` can cite it instead of reproving it (requests O1, R1). |
| F11 | ACCEPTED (coreA part) | grids.tex 225–230 repeated related.tex "Filtering and certificates". | Removed the edge-concave citations and the OBBT/VIPR citations from grids.tex. Kept the technical comparison: credit to Bajaj–Hasan, the αBB constant, the attribution of Lemma dp, and one sentence that points to §2 and says what is specific (one pair of message passes per stage). `rem:cluster` belongs to coreB. |
| F12 | ACCEPTED (coreA part) | Notation table and `\ell_i` are coreA's. | Notation table added (§3.4). My files use only `\ell_i`. `γ` in growthcert → `g_0`, `ℓ^T d` → `ζ^T d`. Renames in other sections belong to their owners. |
| F13 | ACCEPTED (coreA part) | Section 4 is where the grid terms are defined. | Defines "nodes", "number of nodes per coordinate" (`|G_i|`) and "table entries" (bag tables). "Graded grid" and "grading θ" belong to coreB (§5). |
| F19 | NOT IN coreA FILES | Concerns `U ≥ F(ℓ)` in TRIAL (growth.tex). | None. coreB. |
| F22 | ACCEPTED (coreA part) | Typo. | `ℓ^T d` → `ζ^T d` in the proof of `lem:growthcert`. The exact-localized part belongs to the exact agent. |
| F26 | ACCEPTED (coreA part) | | grids.tex: neighbours → neighbors, towards → toward, outwards → outward. related.tex belongs to front; recourse-local and computation to their owners. |
| F28 | MODIFIED | Convention changed as F70 and CONVENTIONS require, instead of "largest constant". The largest weighted constant need not exist: if `P = ∅`, every `γ > 0` is valid. Statements hold for every valid constant anyway. | Def 3.2 defines κ, κ̄, κ_S from some valid constant and states that every statement holds for each valid constant and that a larger constant never gives a larger condition number. κ and κ̄ now follow the same convention. |
| F34 | ACCEPTED (coreA part) | | No overfull box in coreA files. The new (C1) overfull box (53 pt) was fixed with a display. |
| F37 | ACCEPTED (coreA part) | | `rem:nonconvex` now carries the scope statement. `lem:growthcert`(b) was extended to weighted growth so that the statement covers the hypothesis of the main theorem. Section 3 shows κ (and κ̄) can be exponential in I. The intro sentence belongs to front; see request F1 on PD vs PSD. |
| F38 | NOT IN coreA FILES | No FPT wording in Sections 3–4. | None. |
| F41 | ACCEPTED (coreA part) | | Notation table added; `\ell_i` everywhere in coreA files; `P = {i: L_i>0}` kept. |
| F47 | NOT IN coreA FILES | growth-sharp.tex. | None. coreB. |
| F48 | NOT IN coreA FILES | rem:cluster (growth.tex). | None. coreB. |
| F51 | NOT IN coreA FILES | No such wording in coreA files. | None. |
| F57 | NOT IN coreA FILES | Common-mesh lemma (growth.tex). | None. coreB. |
| F58 | ACCEPTED (coreA part) | | `P = {i: L_i>0}` kept in Def 3.1 and listed in the table. Renaming ΔH → Ĥ belongs to the exact and tu agents. |
| F59 | ACCEPTED (coreA part) | | Defined `𝒮` and `𝒮_i = {x_i : x ∈ 𝒮}` in §3.1. Lemma growthcert uses `J_0`, `J_∂`, with `J_0` meaning the same as `J_0(s)` in Section 6. Renames elsewhere belong to their owners. |
| F61 | ACCEPTED (coreA part) | | Lemma growthcert and Remark: `γ` → `g_0`. λ_A/B_λ and the other γ's belong to their owners. |
| F63 | ACCEPTED (coreA part) | | `ℓ^T d` → `ζ^T d`. Subboxes `B, B_i, B^{(j)}` → `X', X'_i, X^{(j)}` with filtered subbox `X''`. `Δ_i(I)` → `w(J)`, so Δ is now free for denominators. |
| F65 | NOT IN coreA FILES | No algorithm names occur in coreA files. | None. |
| F68 | MODIFIED (coreA part) | coreA part: "State Proposition 4.2 for products of families of intervals". | Added the "Families of intervals" paragraph. The proof of `prop:cellwise` uses only two properties, which the paragraph states. Checked exactly (see §5). `lem:cr-cell` needs no families: it is `prop:cellwise`(a) applied to `W_B` (request R1). Deleting Lemma 7.2 and the 8.19/5.6 and 5.11/10.8 items belongs to other owners. |
| F70 | ACCEPTED (coreA part) | | Def 3.2 now has (a) point, (b) weighted, (c) set growth (`eq:setgrowth`), the term "point growth" and `κ(L',g')`. Deleting the local definitions in Sections 6, 8 and 9 is requested (E3, T1, O1). |
| F75 | NOT IN coreA FILES | growth-sharp.tex. | None. coreB. |
| F83 | ACCEPTED (coreA part) | | coreA files use "minimizer", "nodes" and American spelling. "integer labels" → "integer values" in §3.2. |
| F84 | NOT IN coreA FILES | Uses of `f` are outside Sections 3–4. | None. |
| F85 | ACCEPTED (coreA part) | | Lemma dp states the total `O(p(|𝒜|+n+N)K^p)`, which includes the `n` unary terms. Thm 9.3 and Thm 8.11 must match (requests O2, T2). |
| F89 | NOT IN coreA FILES | Meshes `h_j` and `η` are not used in Sections 3–4. The table lists `θ, h_ij, η_j` as §5 symbols. | None. |
| F91 | ACCEPTED (coreA part) | | The rounding inequality is now proved in Section 4 (Jensen, coordinate by coordinate); Lemma 8.5 is cited only for the correlated version. The planted-instance sentences of Remark 3.4 were removed (request C1). The remaining forward references in §3 (Lemma `lem:intcurv`, Lemma `lem:unique-growth`, Remark `rem:setgrowth`, Example `ex:family`) only point to where facts are proved; no proof in §3 depends on them. |
| F136 | ACCEPTED (coreA part) | The intro text belongs to front. | grids.tex now credits the classical parts precisely. Lemma dp is classical; two-pass min-marginals are classical; filtering is OBBT and the record follows checkable B&B certificates (pointer to §2). The only new elements named are the corrected input `Q` and one pair of message passes per stage. This is consistent with the F136 rewrite of contribution (i). |
| F139 | MODIFIED | The full text of Bajaj–Hasan 2020 is paywalled. Searches found only the abstract (AIChE and Springer pages). The theorem number and the constant convention cannot be verified. | Removed "Theorem 1". The text says what the abstract supports: they build an edge-concave underestimator from an upper bound on the diagonal Hessian entries and evaluate it at the vertices. The per-coordinate form is proved in `prop:cellwise`(a) itself. |
| F152 | ACCEPTED | Verified in the local full text of Del Pia–Khajavirad (`literature/papers/pia2026-treewidth-and-the-complexity-of/fulltext.md`, Lemma 20, attributed there to [22] = Khajavirad2026PolyBox). | Footnote at Def 3.2. |
| F155 | NOT IN coreA FILES | growth-sharp.tex. | None. coreB. |
| F156 | NOT IN coreA FILES | Common mesh. | None. coreB. |
| F157 | ACCEPTED (coreA part) | | setting.tex: "uses a growth condition at a minimizer or at the set of minimizers". The abstract belongs to front. |
| F158 | MODIFIED | "κ can be exponential in I (Example 5.11 unit-box; Prop 10.1)" is not proved by those citations. The unit-box chain gives `κ = 2^{Θ(√I)}`, and Prop 10.1 gives only an upper bound on κ. | Replaced by a proved two-variable example with `κ ≥ 2^{k+2}`, `κ̄ > 2^{k+2}` and `I = O(k)` (checked exactly). exact.tex line 290 belongs to the exact agent (request E5). |
| F159 | NOT IN coreA FILES | growth.tex TRIAL. | None. coreB. |
| F160 | NOT IN coreA FILES | growth.tex. Def 3.2 now attaches κ̄ to a valid γ, which supports a clean statement of Lemma 5.3. | None. coreB. |
| F161–F167 | NOT IN coreA FILES | growth.tex, growth-sharp.tex, appendix-growth.tex. | None. coreB. |
| F168 | MODIFIED | Accepted the typo fix. The renaming uses `J_0`, `J_∂` (CONVENTIONS §4) instead of `I_int`, `I_act`. `J_0` matches `J_0(s)` of Section 6 exactly: continuous coordinates strictly inside. | `ζ^T d`; `S, A` → `J_0, J_∂`. |
| F177 | MODIFIED | Forbidding degenerate subboxes (R1's first fix) would break the label filter (App. boundary, lem:labelfilter(ii) fixes integer coordinates to one value) and the localized rule `B'_i = {x*_i}`. The alternative fix was used instead. | Subboxes allow `ℓ'_i ≤ u'_i`; a single node `a` forms the grid interval `[a,a]` (effective width 0). The clause "(w_i(v)=0 if there is none)" was deleted because every node is now an endpoint. (C1) uses `[ℓ_i^{(j+1)}, u_i^{(j+1)}]`. The rounding remark is now self-contained (see F91). Filtering on nondegenerate boxes still gives nondegenerate boxes, and `prop:filter` shows `X''` is a subbox. |
| F181 | NOT IN coreA FILES | | None. |
| F187 | ACCEPTED | Correct. A retained boundary label next to a deleted label violates the old (C1). | (C1) gains a second alternative: `w(J) = 0` and `m_i^{(j)}(v) ≥ β` for each endpoint `v` outside the next hull. `prop:cellwise`(c) gains the node bound `F(x) ≥ m_i(v)+d_i(v)` for `x_i = v`, which proves it. The proof of `thm:certificate` handles both cases. A sentence after Def `def:cert` names the label filter. |
| F204 | ACCEPTED (coreA part) | | grids.tex: "A checker runs the dynamic program once per recorded stage, the same table work as the filtering steps that produced the certificate; in the runs of Section 11 the replay took 0.9 to 2.5 times the solve time." The solver hot-loop fix and the §11 sentence belong to computation. |

## (2) Labels deleted or renamed

None deleted or renamed. New labels:

- `eq:setgrowth`: set-growth inequality in Def 3.2(c). **The same label is still
  defined in `optsets.tex:13`.** The optsets agent must delete that local
  definition (request O1); until then LaTeX reports a multiply defined label.
  References in `appendix-proximal.tex:36` and `limits.tex:502,521` should
  then resolve to Def 3.2(c).
- `sec:grids-dp`: §4.2 (dynamic programming and min-marginals).
- `tab:notation`: notation table (§3.4).

Other new symbols:

- Local proof symbols (unused elsewhere in the same meaning): `W = {i : w(J_i) > 0}`
  in the proof of `prop:cellwise`, `𝒥_i(v)` / `𝒥_i` for interval sets and
  families, `𝒲_{t→u}` (was `V_{t→u}`, because `V` is reserved) in the proof of
  `lem:dp`.
- Filtered subbox: `X''` (was `B'`).

## (3) Requests for other files

**coreB (growth.tex, growth-sharp.tex, appendix-growth.tex)**

- B1. Use `X'`, `X'_i`, `X^{(j)}`, `[ℓ_i^{(j)}, u_i^{(j)}]` and "filter with threshold U to obtain
  `X^{(j+1)}`" (Def 5.1 already uses `X'_i`). Def `def:filter` now requires
  `U ≥ β`. TRIAL satisfies this because `U ≥ OPT ≥ β_j`, by Prop `prop:filter`
  and Prop `prop:cellwise`(b).
- B2. Lemma `lem:inv` should take "a weighted-growth constant γ with
  minimizer x*" and `κ̄ = max{1,1/γ}`, or a free `k` as in F160. Def 3.2 now
  defines `κ̄` from any valid γ.
- B3. Effective widths are now `w(J)`. The grid-interval symbol is `J`, and
  `Δ` is no longer used in Section 4 (Example `ex:family` may write
  `Δ_Γ`).

**exact agent (exact.tex, exact-localized.tex, appendix-localized.tex, appendix-boundary.tex)**

- E1. `lem:node` (exact-localized): its first claim is the new last claim of
  Prop `prop:cellwise`(c). Replace the proof's first part by "By
  Proposition~\ref{prop:cellwise}(c), $F(x)\ge m_i(v)+d_i(v)\ge m_i(v)$."
  Also, `\Delta_k(C_k)` no longer exists (it is now `w(J_k)`).
- E2. `lem:labelfilter`(i) (appendix-boundary). Replace "the filtering-history
  argument of Proposition~\ref{prop:filter} remains valid" with "the recorded
  stages satisfy (C1) of Definition~\ref{def:cert} through its second
  alternative". The proof of (i) can use "By
  Proposition~\ref{prop:cellwise}(c), $F(x)\ge m_i(v)+d_i(v)=m_i(v)$"
  instead of rounding. `l_i` → `\ell_i` (line 60).
- E3. Theorem `thm:transfer`(a): write "If $F$ has set growth with constant
  $g_S$ (Definition~\ref{def:growth}(c))". Use `𝒮` for `S`.
- E4. appendix-localized and Cor `cor:local`: `S, A` → `J_0, J_∂`.
  Lemma `lem:growthcert`(b) now holds on mixed boxes (`J_0 ⊆ I_C`), so
  "Lemma growthcert(b)" at appendix-localized lines 20 and 62 is now literally
  correct; write `H_{J_0J_0}`.
  - Subboxes may now be degenerate in Section 4, so the localized boxes with
    `B'_i = {a}` are subboxes in the sense of §4.1. Rename `B, B^∘, B'` to
    `X'`-style names (e.g. `X^∘`, `X'`, `X''`).
- E5. exact.tex line 290 ("The constant g can be exponentially small in I"):
  delete it, or write "The condition number can be exponential in $I$
  (Section~\ref{sec:setting})."

**optsets agent (optsets.tex, appendix-proximal.tex)**

- O1. Delete the local set-growth definition and `\label{eq:setgrowth}` at
  optsets.tex 12–16. Cite Definition~\ref{def:growth}(c) and use `κ_S` from
  there. Use `𝒮`, `𝒮_i` instead of `S`, `π_i(S)`. Proof of `lem:cells`, suggested text:
  "The bounds $\beta_j\le\min_{X_j}F$ and $\min\{m_i(a),m_i(b')\}\le F(x)$ are
  Proposition~\ref{prop:cellwise}(b),(c) in the form for families of
  intervals (Section~\ref{sec:grids}), with $\mathcal J_i$ the stage cells of
  coordinate $i$, whose endpoints are exactly the nodes of $G_i$." Keep the
  filtering induction. The random-`Y` claim can cite the randomized-rounding
  paragraph of §4.1, or be dropped if unused.
- O2. Thm `thm:cells` operation count: `O(p(|𝒜|+n+N)K_S^p)` (F85).
- O3. appendix-proximal: `B_i` → `X'_i`; `g` in `eq:setgrowth` → `g_S`.

**recourse agent**

- R1. Lemma `lem:cr-cell` is Proposition `prop:cellwise`(a) applied to the
  problem $\min_{X_B}W_B$ with the single cell $C$. `W_B` is continuous on
  $\bar X_B$ and has upper coordinate curvature `L` by
  Lemma~\ref{lem:valuefunction}(a), and $F(x)\ge W_B(x_B)$. The proof can be
  replaced by this sentence, and $e_B(C)$ can use $L_i$.
- R2. `κ_V` → `κ(L^V, g)` (Def 3.2 convention).

**tu agent (constraints.tex)**

- T1. Set growth: `g` → `g_S`, `κ_c := κ(\bar L, g_S)`. Cite
  Definition~\ref{def:growth}(c) and do not restate it. `S_i` → `𝒮_i`.
- T2. Thm 8.11 operation count must include the `n` unary terms (F85).

**computation agent**

- C1. Add the planted-instance construction removed from Remark
  `rem:nonconvex` to the planted-family paragraph. Suggested text: "Each
  instance is certified by Lemma~\ref{lem:growthcert}(a): $\mu$ is chosen so
  that $H+2M\succeq2g_0I$ is verified exactly; then
  $g_0\le g\le\frac12v^{\T}H_{J_0J_0}v/\norm v^2$ for rational $v$ supported
  on $J_0$ (Lemma~\ref{lem:growthcert}(b)), which brackets $\kappa$."
- C2. Keep the sentence "replay took 0.9 to 2.5 times the solve time in all
  runs reported here" in §11. grids.tex quotes these numbers ("in the runs of
  Section~\ref{sec:computation} the replay took 0.9 to 2.5 times the solve
  time"). If the numbers change after the checker fix, the coordinator should
  update that sentence in grids.tex.

**front agent (intro.tex, related.tex, abstract.tex, conclusion.tex)**

- F1. Scope paragraph (Rewrite 5 / CONVENTIONS §5). The main bounds assume
  *weighted* growth, which forces the Hessian block of the interior continuous
  coordinates to be only positive *semi*definite. It is positive definite
  under point growth (Lemma `lem:growthcert`(b)). The negative-curvature
  conclusion holds in both cases. Suggested wording: "For a box QP, point
  growth forces the Hessian block of the continuous coordinates strictly inside
  their bounds to be positive definite, and weighted growth forces it to be
  positive semidefinite (Lemma~\ref{lem:growthcert})." The rest of the
  CONVENTIONS sentence can stay.
- F2. Table 1 (`tab:results`, intro.tex 283ff) is currently deferred to the
  last pages. Because floats keep their order, this also pushes
  `tab:notation` and the Section 11 tables to the end. Use `[p]` or make it
  smaller, or the coordinator should adjust placement.
- F3. related.tex line 17: neighbours → neighbors (F26). If any text cites
  "Theorem 1" of Bajaj–Hasan, remove the theorem number (F139; unverifiable).
- F4. Abstract: "If the objective grows quadratically away from a minimizer
  in the coordinate-curvature metric" (F157).

## (4) New BibTeX entries

None.

## (5) Checks run (local, targeted; not CI)

- `python3 process/w3/checks/coreA-cellwise.py 1 300` and `... 7 300`: both
  passed (600 grid/family checks each).
  - Instances: random nonconvex mixed-integer box QPs with `n ≤ 3`, exact
    `Fraction` arithmetic, and subboxes that may have single-node coordinates.
  - What is asserted:
    - `prop:cellwise`(b): equality.
    - (c): the `β_i(J)` formula and its inequality.
    - The new node bound `F(x) ≥ m_i(v)+d_i(v)`.
    - (a) at random points.
    - The family form: random families covering all nodes, for (a), (b), (c)
      and the node bound.
    - Randomized rounding `E Q(Y) ≤ F(x)` with the exact expectation.
    - `prop:filter`: removed points have `F > U`, and the minimizer of `Q` is
      kept when `U ≥ β`.
- `python3 process/w3/checks/coreA-growthcert.py 1 400` and `... 5 400`: both
  passed.
  - Lemma `lem:growthcert`(a) on mixed boxes: the minorant
    `F(x)−F(x*) ≥ ½dᵀ(H+2M)d` holds at all integer combinations and sampled
    continuous values.
  - Its growth conclusion holds when `H+2M−2g_0I ⪰ 0` (exact elimination
    test; 105 and 116 instances).
  - The two-variable example of §3.3: unique minimizer, `g ≤ 2^{-k-1}`,
    `κ ≥ 2^{k+2}` and `κ̄ > 2^{k+2}` for `k ≤ 11`.
- Compile:
  `latexmk -pdf -interaction=nonstopmode -outdir=build/coreA main.tex` exits 0.
  The log was scanned per input file (`/tmp/coreA_logscan.py`):
  - No errors, no overfull boxes and no undefined references from coreA files.
  - Every `\ref`/`\eqref` and `\cite` key in coreA files resolves. The labels
    `alg:*` and `lem:cr-cell` used by other files are currently undefined,
    which is expected.
  - One warning involves coreA: `eq:setgrowth` is multiply defined (see (2)).
  - The pages of Sections 3–4 and the table were visually inspected.

## (6) Unresolved

- `eq:setgrowth` stays duplicated until optsets removes its local definition
  (O1).
- Bajaj–Hasan Theorem 1 and its constant convention could not be checked
  (paywalled). The text no longer depends on them.
- The quoted replay ratio (0.9–2.5) depends on Section 11 (C2).
- `tab:notation` currently floats to the end because of the deferred intro
  Table 1 (F2).
- The CONVENTIONS growth-scope wording ("growth forces … positive definite")
  is exact only for point growth. coreA uses the precise form, and front
  should do the same (F1).

## Verification (coreA-verify)

Verifier pass over `sections/setting.tex`, `sections/setting-growthcert.tex`
and `sections/grids.tex`, against `process/w3/sections-before-w3/`, the 51
findings in `assign/core.json` and `CONVENTIONS.md`.

### What was checked

- **Adjudication coverage.** All ids in `core.json` have a row, except
  **F140**. Its row is added here:

  | id | status | reason | change made (coreA files) |
  |---|---|---|---|
  | F140 | NOT IN coreA FILES | It concerns the cluster-count sentence of Remark `rem:cluster` (growth.tex), which belongs to coreB and is deleted by CONVENTIONS §1. | None. |

- **ACCEPTED/MODIFIED fixes.** Every fix that touches these files is in the
  text: F12, F22, F26, F28, F37, F41, F58, F59, F61, F63, F68, F70, F83, F85,
  F91, F136, F139, F152, F157, F158, F168, F177, F187, F204.
  - Each MODIFIED decision (F10, F28, F68, F139, F158, F168, F177) has a
    concrete and correct reason. Two examples: no largest weighted constant
    exists when `P = ∅`, and forbidding degenerate subboxes would break
    `lem:labelfilter` and the localized rule.
  - All old labels survive. The new labels `eq:setgrowth`, `tab:notation` and
    `sec:grids-dp` are each defined once; the optsets copy of `eq:setgrowth`
    is gone.
- **Mathematics re-derived line by line.**
  - Section 3:
    - Def 3.2(a)–(c) and the relations between the three notions: point
      growth implies set growth with `κ_S = κ`, and weighted growth with
      `κ̄ = κ` if `L > 0` and with any constant if `L = 0`.
    - Scaling invariance of `κ̄`, and the separable example (`κ̄ = 2`,
      `κ = 2 max L_i / min L_i`).
    - The two-variable example: `L_1 ≥ 2+2^{1-k}`, `L_2 ≥ 2` and
      `F(t,t) = 2^{-k}t²` give `g ≤ 2^{-k-1}`, `γ < 2^{-k-2}`,
      `κ ≥ 2^{k+2}` and `κ̄ > 2^{k+2}`.
    - The footnote against the local full text of Del Pia–Khajavirad,
      Lemma 20 (`[22]` = Khajavirad2026PolyBox).
  - Lemma `lem:growthcert`(a) on mixed boxes, including the claim that the
    remaining coordinates are integer coordinates, and `μ_i = −|ζ_i|`.
  - Lemma `lem:growthcert`(b) with point and weighted growth.
  - Prop `prop:cellwise`(a)–(c), including degenerate intervals and the new
    node bound `F(x) ≥ m_i(v)+d_i(v)`, which runs (a) with `W∖{i}`.
  - The "families of intervals" form. The proof uses only "endpoints in
    `G_i ⊆ X_i`" and "every node is an endpoint"; the stage cells of UC
    satisfy both, so `lem:cells` is an instance.
  - The randomized-rounding proof: Jensen coordinate by coordinate,
    `Var(Y_i) ≤ w(J_i)²/4`, and `Y_i = x_i` when `w(J_i) = 0`.
  - The operation count of Lemma `lem:dp`.
  - Def `def:filter` and Prop `prop:filter`, including that `X''` is a
    subbox.
  - Def `def:cert`, (C1) with its second alternative, and the proof of
    `thm:certificate`.
  - The paragraph showing that filtering records are valid certificates.

### Problems found and fixed

1. **Remark `rem:nonconvex` and Lemma `lem:growthcert`(b) misattributed the
   PSD property to growth.** At any minimizer of a box QP,
   `H_{J0J0} ⪰ 0` holds by second-order necessity, with or without growth.
   - The old text said "weighted growth forces it to be positive
     semidefinite" and "If `J_0 = [n]`, … weighted growth makes it convex".
     Both are true but credit growth with what minimality gives.
   - The lead "Growth restricts where nonconvexity can occur" had the same
     defect.
   - (b) now states `ζ_{J0} = 0` and `H_{J0J0} ⪰ 0` for every minimizer, then
     `⪰ 2gI` under point growth and `⪰ 2γ diag(L_i)_{J0}` under weighted
     growth. The `J_0 = [n]` case reads "F is convex, and strongly convex under
     point growth". The proof now derives all three inequalities.
   - The remark states the same facts in this order. The deviation from the
     CONVENTIONS §5 lead sentence is deliberate; the substance (positive
     definite under point growth, negative curvature only in directions that
     involve active bounds or integer coordinates, Example `ex:family`) is
     kept.
2. **Remark `rem:nonconvex`, last sentence, was false for integer
   coordinates.** It said that integrality of `d_i` at integer coordinates
   "supplies the growth that the Hessian lacks" in part (a). In (a),
   integrality only gives the weaker term `μ_i = −|ζ_i| ≤ 0`. A certificate
   `H+2M ⪰ 2g_0I` therefore still needs `H_ii ≥ 2g_0+2|ζ_i|` at such `i`.
   The sentence now says this.
3. **Two-variable example (setting.tex).** `γ < 2^{-k-2}` needs
   `L_1+L_2 > 4`, which was not justified. The text only gave
   `L ≥ L_2 ≥ 2`. The example now states `L_1 ≥ 2+2^{1-k}`, `L_2 ≥ 2` and
   `F(t,t) = 2^{-k}t²`, and is split into short sentences.
4. **Cell-bound lead-in (grids.tex).** "β(C) is a lower bound for F on C" is
   false when some `J_i` is a unit integer interval (`w = 0`). F can be lower
   at fractional points, which are infeasible. The lead-in now subtracts the
   quadratic only in coordinates with `w(J_i) > 0` and claims the bound on
   `C ∩ X`, as Prop `prop:cellwise`(a) does.
5. **Replay figures (grids.tex).** "In the runs of Section 11 the replay took
   0.9 to 2.5 times the solve time" quoted numbers that Section 11 does not
   contain: computation.tex line 72 has placeholders `@@ to @@`, and the
   QPLIB_3852 certificate was not replayed. The sentence now ends with
   "Section~\ref{sec:computation} reports measured replay times." Request C2
   is obsolete.
6. **Filtering record ⇒ valid certificate (grids.tex).** The paragraph did
   not show that each threshold satisfies the new hypothesis `U_j ≥ β_j` of
   Def `def:filter`. It now derives `β_j ≤ OPT ≤ U_j` from the induction. It
   also says that a grid interval not contained in
   `[ℓ_i^{(j+1)},u_i^{(j+1)}]` was not retained.
7. **Smaller precision and wording fixes.**
   - Def `def:cert` defines `ℓ_i^{(j)} = min G_i^{(j)}` and
     `u_i^{(j)} = max G_i^{(j)}`.
   - The proof of `thm:certificate` writes the chain `F(x) ≥ m+d ≥ m ≥ β`.
   - "label filter of Appendix" became "integer-label filter of
     Lemma~\ref{lem:labelfilter}".
   - "interpolation bounds of Lemma cells" became "bounds of Lemma cells for
     unions of uniform cells".
   - "The proof uses" became "The proof of Proposition~\ref{prop:cellwise}
     uses".
   - The ambiguous "It has two further advantages" became "The weighted
     condition number has …".
   - "by an amount proportional to its squared distance" became "by at least
     a fixed multiple of …".
8. **Notation table.** Added rows for `S_{tu}` (separators, §4.2) and `K_S`
   (Thm `thm:cells`), as CONVENTIONS §4 lists them.

### Corrected requests

- **F1 (front, intro.tex "Scope of the growth hypothesis") replaces the
  wording suggested above.** The current intro sentence "For a continuous box
  QP, growth forces the Hessian block of the coordinates strictly inside their
  bounds to be positive definite" is false for weighted growth. With
  `i ∈ J_0∖P`, the row `i` of `H_{J0J0}` is zero. Suggested text: "For a box
  QP, the Hessian block of the continuous coordinates strictly inside their
  bounds at a minimizer is positive semidefinite, and point growth makes it
  positive definite (Lemma~\ref{lem:growthcert}). The nonconvex instances
  covered by our bounds therefore have their negative curvature in directions
  that involve active bounds or integer coordinates; such instances can have
  exponentially many strict local minima (Example~\ref{ex:family})." Do not
  write "weighted growth forces it to be positive semidefinite"; that holds at
  every minimizer.
- **C1 (computation)** is already done: computation.tex lines 98–103 contain
  the planted-instance construction. **C2** is obsolete (item 5).
- **E2** (`lem:labelfilter`(i)) and **O1** (`eq:setgrowth`, `lem:cells` via
  families) are already done in the current files.

### Checks run (local, targeted; not CI)

- `python3 process/w3/checks/coreA-verify-cert.py 3 200` and
  `... 11 200` (new). Both passed: 200 instances, 600 random certificates and
  200 filtering records each; 77 and 78 of the records used the integer-label
  filter.
  - Exact OPT is computed by enumerating integer values and faces of the
    continuous box.
  - For random nested subboxes with random grids (degenerate coordinates
    allowed), the script takes the largest β for which Def `def:cert` holds,
    using both (C1) alternatives, and asserts β ≤ OPT.
  - Filtering records (with the label filter) are checked to be valid
    certificates with β = β_k, with `U_j ≥ β_j` at every stage and every
    exact minimizer kept.
  - The node bound is checked at exact minimizers.
- Mutation test: the same script with the second alternative of (C1) allowed
  for every interval (`w(J) > 0` too) fails at once (β = 1/2 > OPT = −1). So
  the check can detect an unsound (C1).
- Re-ran the coreA scripts on new seeds:
  - `coreA-cellwise.py 5 200`: passed (400 grid/family checks).
  - `coreA-growthcert.py 9 300`: passed (300 minorant checks, 87 with the
    growth certificate, plus the two-variable example).
- `latexmk -pdf -interaction=nonstopmode -outdir=build/coreA-verify main.tex`
  exits 0. Scanning the final log by input file found no errors, no overfull
  boxes, no undefined references or citations and no multiply defined labels
  in the whole build at the time of the run. The notation table page (p. 13)
  was inspected visually.

### Remaining

- The intro scope sentence (front's file) is incorrect for weighted growth
  until F1 is applied.
- The CONVENTIONS §5 lead sentence "Growth restricts where nonconvexity can
  occur" is not used in Remark `rem:nonconvex` (reason in item 1). The
  coordinator may want to align the intro in the same way.
- Bajaj–Hasan's theorem number and constant convention remain unverifiable
  (paywalled). The text no longer depends on them.

## Verification (coreA-verify, second pass)

This is an independent second pass over `sections/setting.tex`,
`sections/setting-growthcert.tex` and `sections/grids.tex` as left by the
first verifier. The files had not changed since 02:22. The pass checked them
against `process/w3/sections-before-w3/`, all 51 findings in
`assign/core.json`, `CONVENTIONS.md`, and the other sections as they stand
now.

### What was checked

- **Adjudications.** Every id in `core.json` has a row; F140 was added by the
  first pass. Every ACCEPTED or MODIFIED fix that touches these files is in
  the text. Each MODIFIED or NOT-IN-coreA decision has a correct concrete
  reason:
  - F28: there is no largest weighted constant when `P = ∅`.
  - F158: the proposed citations do not prove that κ can be exponential in I.
  - F168: `J_0`, `J_∂` follow CONVENTIONS §4.
  - F177: degenerate subboxes are needed by `lem:labelfilter` and
    `prop:local`.
  - F139: the theorem number cannot be verified.
- **Mathematics, re-derived line by line:**
  - Section 3:
    - Def 3.2(a)–(c) and the relations between the three notions.
    - Scaling invariance of κ̄.
    - The separable example: largest constants `γ = 1/2` and
      `g = min L_i/2`.
    - The two-variable example: `∂11F = 2+2^{1-k}`, `∂22F = 2`,
      `F(t,t) = 2^{-k}t²`, hence `g ≤ 2^{-k-1}`,
      `γ ≤ 2^{-k}/(L_1+L_2) < 2^{-k-2}`, `κ ≥ L_2/g ≥ 2^{k+2}`, and the
      Hessian determinant `2^{2-k} > 0`.
    - Lemma `lem:growthcert`(a), (b) on mixed boxes, including that the
      "remaining" coordinates of (a) are integer coordinates.
    - Remark `rem:nonconvex`.
  - Section 4:
    - Prop `prop:cellwise`(a)–(c), including degenerate intervals and the
      node bound.
    - The families-of-intervals form. The UC stage cells of
      `optsets.tex` satisfy its two properties and `G_i ⊆ X_i`, so Lemma
      `lem:cells` is a genuine instance.
    - The rounding paragraph, Lemma `lem:dp` and its operation count.
    - Def `def:filter` and Prop `prop:filter`, Def `def:cert` with both
      (C1) alternatives, the proof of `thm:certificate`, and the paragraph
      on filtering records.
- **Uses of coreA statements in other files.** Each was checked against the
  current wording; all are consistent:
  - `prop:cellwise`(c) node bound: exact-localized `lem:node`,
    appendix-boundary `lem:labelfilter`(i), appendix-localized,
    limits.tex 526.
  - The second alternative of (C1): limits (c), appendix-boundary.
  - Def `def:filter` with `U ≥ β`: TRIAL filters only when
    `U−β_j > ε > 0`; limits (b) uses `U ≥ OPT ≥ β`.
  - The families form: optsets `lem:cells`.
  - Def 3.2(c): optsets, constraints, exact `thm:transfer`, limits.
  - The planted-instance text and `eq:minorant`: computation.tex.
- **Sources.** The footnote at Def 3.2 matches Lemma 20 and reference `[22]`
  of the local Del Pia–Khajavirad full text. The Bajaj–Hasan description
  matches the published abstract (AIChE 2018 abstract: "a global upper bound
  on the diagonal Hessian elements … edge-concave underestimator … evaluating
  this underestimator at the vertices").
- **CONVENTIONS.** Checked:
  - The notation table: every row was compared with its defining section
    (`h_ij`, `η_j` in growth.tex; `Δ, R, Ω, τ` in exact.tex; `𝒦, ℛ, V` in
    recourse-valuefn; `L̄` in constraints; `K_S` in `thm:cells`).
  - Terminology ("nodes per coordinate", "table entries", "point/weighted/set
    growth", "observation").
  - `\ell_i`, `g_0`, `J_0`/`J_∂`, `w(J)` and `X'`.
  - No banned phrases or British spellings.
  - All 21 labels of the original files survive, and all 24 current labels
    (21 old plus `eq:setgrowth`, `tab:notation`, `sec:grids-dp`) are each
    defined once in the whole paper.

### Problems found and fixed

1. **The convention after Def 3.2 was false as written.** It said that "every
   statement that involves κ, κ̄ or κ_S holds for each valid constant". Many
   statements are existential, and read this way they become false because a
   smaller valid constant gives a larger condition number. Examples:
   - "κ ≤ 2" (limits.tex 19, 303; intro.tex 173, 193, 354);
   - "κ_S ≤ 40" (optsets.tex 37, 61);
   - "κ_S ≤ 2n(n−1)" (limits.tex 481).

   The text now reads: "The constants are not unique, and a larger constant
   never gives a larger condition number. Each condition number is defined
   from a valid constant: a result that assumes growth holds for every valid
   constant, and a statement that an instance has, for example, κ ≤ c means
   that some valid constant gives this bound." Statements of the form κ ≥ c
   in Section 3 (Lemma growthcert(b) and the two-variable example) are proved
   for every valid constant, so they remain correct.
2. **Bajaj–Hasan (F139, R7's per-coordinate point).** "this is the bound of
   Bajaj and Hasan" became "this is the vertex bound of Bajaj and Hasan, who
   build …; we use one bound L_i per coordinate". This addresses R7's remark
   that they use a single bound on the diagonal. It no longer claims that
   their constant convention coincides with ours.
3. **Lead-in to Lemma `lem:growthcert`.** It said the lemma "shows what growth
   implies for the Hessian". Part (b) first states what minimality alone
   implies (`ζ_{J0} = 0`, `H_{J0J0} ⪰ 0`). The lead-in now says "what
   minimality and growth imply".
4. **Wording.** In the paragraph after Def 3.2, a sentence with two
   consecutive "so" clauses was split.

### Checks run (local, targeted; not CI)

- `python3 process/w3/checks/coreA-verify-dp.py 1 300` and `… 7 300` (new):
  both passed (906 and 875 bags).
  - Exact check of Lemma `lem:dp` on random tree decompositions with random
    grids and unary corrections.
  - Messages are computed as in the text: upward by `eq:messages`, downward
    from `A_t − M_{u→t}`.
  - Asserted: `A_t = min{Q(z): z_B = y_B}` for every bag, `β = min A_t`,
    `m_i(v) = min_{y_i=v} A_t` for every bag containing `i`, and that the
    root-outward minimizer attains β.
  - A mutation (downward messages taken from `A_t` without subtracting
    `M_{u→t}`) fails at once.
- Reruns on new seeds; all passed:
  - `coreA-cellwise.py 13 200`: 400 grid and family checks.
  - `coreA-growthcert.py 17 300`: 300 minorant checks (79 with a growth
    certificate) and the two-variable example.
  - `coreA-verify-cert.py 23 200`: 600 random certificates and 200 filtering
    records (83 used the label filter).
- `latexmk -pdf -interaction=nonstopmode -outdir=build/coreA-verify main.tex`:
  - From an empty build directory, latexmk reported two transient
    `\@@BOOKMARK` errors. They came from the bookmark file of an intermediate
    pass that had unresolved `??` titles in the appendices. One more
    `pdflatex` pass exited 0 with no errors.
  - The final log, scanned per input file with `max_print_line=10000`, has no
    errors, no overfull or underfull boxes, no undefined references and no
    multiply defined labels in the whole build.
  - Page 10 (Def 3.2 and its paragraph) was inspected visually.

### Remaining

- **front, intro.tex 136–138: request F1 is still not applied.** The sentence
  "and weighted growth forces it to be positive semidefinite" credits growth
  with what minimality gives. Replace "Growth restricts where nonconvexity
  can occur. For a box QP, point growth forces the Hessian block of the
  continuous coordinates strictly inside their bounds to be positive
  definite, and weighted growth forces it to be positive semidefinite
  (Lemma~\ref{lem:growthcert})." with "For a box QP, the Hessian block of the
  continuous coordinates strictly inside their bounds at a minimizer is
  positive semidefinite, and point growth makes it positive definite
  (Lemma~\ref{lem:growthcert})."
- Bajaj–Hasan's theorem number and constant convention remain unverifiable
  (paywalled). The text depends on neither.
