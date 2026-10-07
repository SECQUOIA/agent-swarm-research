# Review r2: stream `intersection-literature` (confirmation round 2)

Reviewer: independent research agent. I did not write the material or review r1.
Date: 2026-10-02. This file replaces a partial r2 review left by an interrupted
reviewer. I reused none of that reviewer's results without checking them myself.
My own independent script is `reviews/r2-code/r2b_independent.py`, with output in
`r2b_independent.log`. The earlier reviewer's `r2_exact_checks.py` and its log are
left in place but were not relied on.

Object: the revised `note.md` (Section 14 lists the changes), the new and changed
scripts in `code/`, the logs, and the two new sources.

**Verdict: minor fixes.** All three major and all four minor issues from r1 are
fixed correctly. Two minor issues remain: (n1) one inequality in the newly added
infinite case is wrong, and (n2) the note has no statement about background
processes, which the program rules require. There are also four optional items.

## Status of the r1 issues

| r1 issue | Status | What I checked |
|---|---|---|
| **M1** KY Ex. 4.2–4.5 missed; Prop. 2(b) = KY Ex. 4.3 | **Fixed** | I reread KY draft pp. 21–23 (`sources/kilinc-yang2015-sufficiency-draft.txt`, lines ~990–1120). The note describes Ex. 4.2 (`(1, −1/n)`; `c = (1,1)` generated), Ex. 4.3 (`(1 − 1/√n, −1/n)`; not generated), Ex. 4.4 (`(n, −1)`; `c = (0,1)` generated) and Ex. 4.5 (`(n, −1/n)`; not generated) correctly. The quoted sentence "The main difference in these examples is in the way the sequence of points in B_2 approach to a point in cone(A)" is on p. 21. The withdrawn priority claims are gone from the Summary, §4.4, §7 and §8. Thm 1(4) is now labelled "general sufficient condition; modest". The argument that Thm 1(4) cannot literally cover the discrete Ex. 4.2 is correct: a C^1 `q` with `{q ≤ 0}` locally discrete has a local minimum at the accumulation point, so `∇q(t*) = 0`. The Prop. 2(a)–KY Ex. 4.5 match is right: the boundary of `{(x+1)y + 1 ≤ 0}` is `y = −1/(x+1)`, the analogue of `(n, −1/n)` |
| **M2** KY Cor. 3.12 false as printed | **Fixed** | The printed statement in §4.4 matches the draft (pp. 17–18). Both counterexamples are valid. *Ex. 1* (KY Ex. 4.3, `D_2 = {(1/2,0)}`): `(1/2,0)` is a limit of rescaled `B_2` points and is not in `cl(B_2) = B_2 ∪ {(1,0)}`. The case bound (1/n ≥ 1/8 for n ≤ 8; 1/2 − 1/√n ≥ 1/6 for n ≥ 9) is correct; my exact distances for n < 200 have minimum 0.1879. The ray `e_2` is not a limit ray, because second coordinates stay ≤ 0. The inequality `x_1 + x_2 ≥ 1` is valid, since `S(A, R^2_+, B) = {e_1, e_2}`, and KY prove it is not generated. *Ex. 2* (Prop. 2(b), `D_2 = {(1/2,0),(0,1/2)}`): `q = 5/4, 1/4`. Both axes are limit rays: `q(T, −1/T) < 0` for large T (−8879/100 at T = 10), and `q(−s², 1−s) = −s⁴`. I re-derived `z_K = 1` (on the branch λ_1 ≥ 1, `f(x) = x + 1 − √(x²−x)` decreases from 2 to φ). The §4.1 step from "CGF generates c" to "an S-free set attains z_K" is correct. *Where the proof breaks*: KY's proof of Cor. 3.12 rescales to `2d/σ(d)`, and `(2,0)` puts `(1,0) ∈ cl(B_2)` on the segment, as the note says. Notably, in Ex. 4.2 KY themselves say that Cor. 3.12 "is not satisfied when c_1 = 1". That is the corrected reading, which supports the note's diagnosis. *Cor. 3.12'*: I read the proof of KY Prop. 3.11 (pp. 16–17). Its hypothesis (ii) is used exactly where the corrected `D_2` condition is needed. The rescaled points satisfy (ii), have σ = 2 > 1 and stay in `cl(R_{++}B_2) ∩ cone(A)`. The status "proved, given KY Prop. 3.11", with the caveat about unchecked steps, is appropriate. *Remark 4.4*: the choice of `D_1` and `D_2` gives (i) and (ii). (iii) holds on `D_1` because `d ∈ B ∩ cone(A)` puts every `μ` in `X`, and on `D_2` because `c > 0`. KY's standing assumption `0 ∉ conv S(A, R^n_+, B)` holds because `w^T λ ≥ z > 0` on `X`. *Theorem 14 inference*: correct under Cor. 3.12' (see the independent check below) |
| **M3** Prop. B general claim | **Fixed** | The general proof is correct. (1): I verified the trace and traceless-norm identities symbolically. (2): sympy solves `sym(AM) = 0` for a generic `A`: the solution set is one-dimensional and parallel to `A^{-1}J`. The lineality argument then forces `A = μ^{-1}G`, and `−G_t = G_{t+π}` makes "scalar" and "positive" multiples the same. (3): the 3×3 minors of `M ↦ sym(AM)` are `(−A_1, A_3, A_0, −A_2)·det(A)/2`, so the map is surjective and `int C'_A = {sym(AM) ≻ 0}`. Also `det(S + kJ) = det S + k²` and `‖(b+c, a−d)‖² − ‖(a+d, b−c)‖² = 4(bc − ad)`, so every nonempty (14b) set lies in `{ad ≤ bc}`. BCM v7 (14a)/(14b) are at lines 1005–1006 of the extracted text, and the containment argument is in the proof of Lemma 22. Example: `det sym(F^T M_1) = 7/16` (trace 5/2) and `det sym(F^T M_2) = −8` |
| **m1** OpenCitations DOI | **Fixed** | I reran `python3 code/opencitations.py 10.1007/s10107-021-01738-8`: 7 citers, the same identifiers as `logs/opencitations.log`. The superseded log is kept and labelled |
| **m2** Kılınç-Karzan–Steffy missing | **Fixed** | I checked page locators by counting form feeds in `sources/kilinc-steffy-sublinear-draft-web.txt`: Prop. 3 p. 8; Def. 3 and Prop. 4 p. 9; Cor. 2 p. 10; "without any further technical assumptions" p. 11; Prop. 5 p. 11; "recovers the main result, Theorem 1.1, of [14]" p. 12. Cor. 2 assumes only `0 ∉ conv(S(A, R^n_+, B))`, as described. The manifest sha256 matches the file. The KY introduction (p. 4) independently confirms the "no technical assumptions" description |
| **m3** solver baseline too strong | **Fixed** | The Summary, §6, §8 item 8 and §12 say "in the sources I could read" and name the unread sources. The slides' sha256 matches the manifest |
| **m4** Prop. A part (2) | **Fixed** | The halfspace argument is correct in all three cases (`a_w > 0`, `a_w < 0`, `a_w = 0`, the last using `a ≠ 0`), and so is the map `(x,y,w) ↦ (−x,y,−w)` from `{w ≥ xy}` onto `{w ≤ xy}` |
| o1 infinite case | Added, but with an error | See n1 |
| o2 "C^1 quadratic" | Fixed | §4.4 and §7 say "any `q ∈ C^1`" |

## Minor issues

### n1. The infinite case of Remark 4.4 states a wrong inequality

Location: note.md §4.4, "Infinite case"; repeated in §14, row o1.

The note says: "The same argument with `c = Mw`, for any `M > 0`, gives
`z_V(w) ≥ M`." By the §4.1 dictionary, `ρ(p_j) ≤ c_j = M w_j` gives
`α_j ≥ 1/(M w_j)`, so `z_V(w) ≥ 1/M`. The finite case confirms the scaling:
there `c = w/((1−ε)z)` gives `z_V ≥ (1−ε)z`, so the bound is the reciprocal of
the factor in `c`. My script prints `min_j w_j α_j = 1/5` for `M = 5`. Since
`M > 0` is arbitrary, the conclusion `sup = ∞` still follows, but the displayed
inequality is false. (Review r1's wording of o1 was loose in the same way.)
Fix: use `c = w/M`, which gives `z_V(w) ≥ M`.

### n2. No statement about background processes

The program's process-hygiene rule says to make sure that every background
process has finished or been killed before returning, "and say so in the note".
`note.md` has no such statement. `grep -i "background\|process"` finds only the
unrelated word "background" in the novelty table. The stream ran only short
scripts and network queries, and `ps -ef` shows nothing from this stream running
now. So this is a missing sentence, not a hygiene failure. Fix: add one line,
for example in §11, saying that no background processes were started, or that
all have finished.

## Optional

- **o-a.** In §4.4 the note says that "Prop. 2(b) and KY Example 4.3 have
  `∇q(t*)^T(x̄ − t*) = 0`". For Prop. 2(b) this is a genuine tangency:
  `∇q(0,1) = (1,0)` and `x̄ − t* = (0,−1)`. For the discrete KY Ex. 4.3 it is
  only vacuous, because by the note's own argument `∇q(t*) = 0` for any C^1
  description. The same holds for the *attained* Ex. 4.2. I suggest saying it
  only for Prop. 2(b).
- **o-b.** `check_ky_cor312_counterexample.py`, Example 1, prints the bound
  "distance to every point of B_2 ≥ 1/8" from a hand case split, not from
  computed distances. The bound is a valid proof, but the log line reads as if it
  were computed. The proof should be cited, or the line reworded.
- **o-c.** In OpenCitations, Chmiela et al. (`10.1007/s10107-022-01808-5`)
  appears among its own 6 citers (a self-record). This has no effect on the
  conclusions.
- **o-d.** The program asks the note to end with "Checks actually run",
  "Limits" and "Open questions". Section 14 (the revision log) now comes after
  them. Moving it before §11, or into an appendix placed before those sections,
  would follow the required layout.

## Other material re-checked and found correct

- **Theorem 14 corner** (my own `Fraction` script; Cramer's rule rather than the
  stream's sympy solve):
  - `λ(t*) = (1/2, 1/2, 0)` with cost 1;
  - `n = (−18, −60, −18)` gives `n·p_1 = n·p_2 = 0` and `n·p_3 = −249`;
  - `q(t* + εn) = 18ε(−60ε − 11)` exactly at ε = 10^-1, 10^-4 and 10^-8, with
    λ_3 < 0 (for example −177/103750 at ε = 10^-4), so `t* − s̄ ∈ cl(B_2)`;
  - `q(s̄ + τ(t* − s̄)) = 3(1−τ)/2` at τ = 0, 0.1, …, 1;
  - `∇q(t*)·(s̄ − t*) = 3/2`.

  So under Cor. 3.12' the only admissible representative of that ray is the
  `D_1` point `t* − s̄`, with σ = 1. The sfree note's Theorem 1(4) hypotheses
  (`w > 0`, unique minimizer, transversality) hold, as the note says.
- **KY necessary conditions vacuous** for closed `S` and `c = w/z ≥ 0`: correct.
- **KY page locators**: Prop. 3.11 on p. 15 (between the "14" and "15" page
  footers), Cor. 3.12 on pp. 17–18, Ex. 4.2 on p. 21, Ex. 4.3 on p. 22, Ex. 4.4
  on pp. 22–23, Ex. 4.5 on p. 23.
- **Novelty framing**: now appropriately modest, and every "not found" is
  qualified as an unsuccessful search. Solver relevance is not overstated.
- **Script reproducibility**: all three changed scripts reproduce their logs
  byte for byte.
- **Background processes**: none from this stream are running (`ps -ef`).

## Checks actually run by this reviewer

All checks are targeted to this stream. I ran no project-wide verification and
did not consult CI.

| Command | Outcome |
|---|---|
| `OMP_NUM_THREADS=1 timeout 300 python3 code/{check_ky_cor312_counterexample,check_ky_gap_thm14,check_bcm_orbit}.py`, then `cmp` against `logs/` | All exit 0; all three outputs byte-identical to the logs |
| `OMP_NUM_THREADS=1 timeout 300 python3 reviews/r2-code/r2b_independent.py > reviews/r2-code/r2b_independent.log` (my own script) | Thm 14 facts as listed above; infinite-case scaling gives `1/M`; Prop. B: lineality parallel to `A^{-1}J`, det identity 0, (14a) identities 0, (14b) identity 0, minors `±A_i det(A)/2`, example dets 7/16 and −8; Prop. 2(b): `q = 5/4, 1/4`, `q(T, −1/T) < 0`, branch minimum φ; KY Ex. 4.3: minimum distance 0.1879 for n < 200 |
| `timeout 120 python3 code/opencitations.py 10.1007/s10107-021-01738-8` | 7 citers, identical to the log |
| `sha256sum` on the two new source PDFs | Both match the manifest addendum |
| `sed`/`awk` reads with form-feed page counting of the KY draft (§3 pp. 13–18, §4 pp. 21–23), the KS draft (pp. 8–12) and BCM v7 ((14a)/(14b), Lemma 22) | Locators and statements as listed above |
| `grep -n -i "background\|process" note.md`; `ps -ef \| grep` for stream scripts | No process statement in the note (n2); no running processes |
| Read of sfree note Theorem 1, Proposition 2, Lemma 10 and Theorem 14 (read only) | The note's descriptions match the hypotheses and data |
