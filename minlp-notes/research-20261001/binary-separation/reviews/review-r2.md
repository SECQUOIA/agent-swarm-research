# Review r2 of the binary-separation note (confirmation round)

Date: 2026-10-02. Reviewer: an independent research agent (adversarial review, not
journal peer review). Object: the revised [`note.md`](../note.md), `code/`, `logs/` and
`sources/`, after [review round 1](review-r1.md). My scripts and outputs are in
[`r2-work/`](r2-work/). My code does not import the author's code.

## Verdict

**Major problems: one issue, easy to repair. There are no other major or minor issues.**

All round-1 items are fixed correctly (table below), and the new Lemma 5 is proved
correctly. Corollaries 3–6 at `ε = 1/(8n + 2p + 1)` are correct, and so are the new
Corollary 8 and the new NP-membership argument for gap-1. All logs reproduce exactly,
apart from timing lines. My own exact checks confirm every revised claim.

The remaining issue concerns the status of Padberg's clique inequalities (10). The
note says in five places, including the paragraph written for a paper's discussion
section, that their separation complexity "remains open". The reason it gives is that
the violators have mixed signs. This is wrong. Switching the note's own hard points on
the single variable `g` turns the violated cut inequalities into violated clique
inequalities (10), and no other clique inequality is violated there. So separating
(10) is strongly NP-complete, with facet-defining violators at positive definite points
without repeated points (proof in R2-M1; exact check [G]). The same trick applied to
Corollary 5 settles the Barahona–Mahjoub clique inequalities (18) without switching,
but only at points with repeated points (exact check [H]). The task asked the author
to settle open cases that a reduction can settle, and to state the corrected status.
So this omission leaves a wrong statement in the main deliverable.

## Round-1 items

| Item | Status in revision | My check |
|---|---|---|
| M1 (strong hardness at the scaled points) | **Fixed.** Lemma 5 proves `max Mᵢᵢ ≤ s ≤ 4n + p + 1/(4(p−1)) < N/2`, and Corollary 3 uses `ε = 1/N`. | I checked the proof line by line. `uᵢᵀc* = 2 + |Sᵢ|/2 = Mᵢᵢ/2`, `u_gᵀc* = p/4 + (η² − p/4)/2 = M_gg/2`, `s = 4‖Πc*‖² ≤ 4‖c*‖²`, `4γ² = 1/(4(p−1))`. The lower bound is Cauchy–Schwarz in the `M` inner product. My check [A] covers 81 instances, including empty, duplicate and full-universe sets, singletons and `n = 61`, with 0 failures. The bound is nearly attained (12 singletons: `s = 60.012` against a bound of `60.023`), so it cannot be improved much in general. Corollary 3(c): `4N·X` is integral with entries `≤ 4N`, and `X − θe₀e₀ᵀ ≻ 0` for `θ ≤ 1/2` (Schur complement, `εs < 1/2 ≤ 1 − θ`). My check [B] covers 70 instances with 0 failures, with my own split enumeration and `θ = 1/2` tested exactly. |
| m1 (`Θ(1/(n+p))`) | **Fixed.** The claim is withdrawn. The violation is now exactly `1/(16n+4p+2)`, and the old bounds `1/(16n+4p+1) ≤ 1/(4s) ≤ 1/28` are stated. | Correct. Open question 5 still says `Θ(1/(n+p))` "for the chosen scaling", which is now true. |
| m2 (`εd ∈ [0,1]` for `q = 2`) | **Fixed** with the congruence `J − 2εD = L X Lᵀ`. | I verified the congruence entrywise by hand and exactly in [B], including 40 instances with a cover of at most 2 sets (where the triangle inequalities fail): 0 failures. |
| m3 (Letchford 2022; (11)/(12)) | **Fixed.** The sources are added, and Corollary 8 is new. | Quotations and locators checked: pp. 8–9, 11, 16, 18–20, and §7.2 begins on p. 17. Corollary 8 is correct (check [C], and [D] for facets). But see R2-M1: the new text on (10) and (18) is wrong. |
| m4 (BiqMac/BiqBin/MADAM) | **Fixed.** | BiqBin pp. 7–8 and MADAM pp. 3, 5–6, 15 say exactly this: BiqMac uses triangle inequalities only, triangles are enumerated, and pentagonal and heptagonal inequalities are separated by simulated annealing on a QAP formulation, because evaluating all of them is "prohibitive". |
| o1 (window `p/12`) | Adopted. | I checked the proof: the integer minimum `−⌊(m+1)²/4⌋` gives `(m+1)(mη² − p/4)` for odd `m` and `m((m+1)η² − p/4)` for even `m`. The sharpness examples are correct. My check [E] confirms Theorem 1 at `η² = p/12` on 80 instances, finds extra violators below `p/12` in 30 of 30, and confirms the no-instance example. |
| o2 (6-point gap runs) | Declined, with reasons. | **I agree with the author; my predecessor's item o2 was wrong.** At a no-instance, `εd` satisfies all gap-1 inequalities, and these include every switching of a hypermetric inequality. `CUT₆ = HYP₆` (Deza–Dutour Sikirić 2015, p. 1, quoted correctly). Every facet of the cut polytope is a switching of a facet of the cut cone (Letchford 2022, p. 16). So `εd` lies in the cut polytope for `|V| ≤ 6`. My LP check [I] (numerical) agrees: 30 of 30 no-instances with 4–6 points. |
| o3 (input domain; gap-1 in NP) | Adopted. | The switching argument is correct: `diag(s)Z diag(s) = J − 2D(d^S)` and `b′ᵀ(J − 2D)b′ = σ² − 4Q`. My check [F] confirms the identity on 300 random rational `d`. |
| o4 (manifest authors) | Fixed. | Confirmed. |

## Other new or changed material checked and found correct

- **Corollary 8.** (12) is half the linearization of `(ℓ−s)(ℓ−s−1) ≥ 0`; I re-expanded
  it. The violators `(𝟙_C − e_g, 0)` and `(e_g − 𝟙_C, −1)` give the same inequality,
  violated by `1/(4N)`.
  - NP membership is correct: for fixed `(S,T)` the integer maximum is at
    `s = ⌊ℓ⌋`, and my check [C] asserts this on every `(S,T)`.
  - Facetness: Letchford's condition for (12) on p. 9 holds for the violators.
    Switching on `{g}` gives the clique inequality with `S′ = C ∪ {g}`, `s′ = 1`, and
    Padberg's condition holds for it.
  - My check [C] enumerates all ordered disjoint `(S,T)` and also runs a bounded
    Boros–Hammer box search (`v ∈ [−2,2]^{n+1}`, all `s`). It finds only
    `±(𝟙_C − e_g)`, with 0 failures on 40 instances.
  - My check [D] confirms facets by exact rank for `q = 2..6`, and also with unused
    variables.
- **The remark on Letchford's facet condition for (11).** The inconsistency is real.
  My check [D] finds that the printed (11) is a facet for `(|S|,|T|) = (2,1), (3,1),
  (2,2), (2,3), (3,2)` and not for `(1,2), (1,3), (1,4)`. The chapter's own remark on
  p. 8, that (11) with `|S| = 2`, `|T| = 1` is the triangle inequality (9), agrees with
  the printed formula. So the condition is the part that is off. See also optional
  item o4 below.
- **§9, §10 and the logs.** All numbers in the note match the logs:
  - the minimum `ε·Σλ` lies between 0.34 and 0.46 (0.3373–0.4590);
  - `s = 21.1, 24.7, 25.5`;
  - 19/21 digits at `q = 10`, `n = 22`;
  - 48 no-instances in total, of which 21 have 7–8 points.

  The diffs against `logs/r0/` are as the note describes.
- **Lemma 5 remark ("`s` stays bounded").** The statement is true. For `n` copies of
  `{0,1,2}` plus `{3,4,5}`, symmetry reduces `Mw = δ` to a 3×3 system, and I get
  `s(n) = 77(193n + 108)/(4(141n + 272)) → 14861/564 ≈ 26.35`. This reproduces the
  logged 21.142, 24.704 and 25.489. See optional item o3.
- **Literature additions.** Dey et al. 2026: §4.1.2 starts on p. 15, and problem (18)
  with `Lᵢ = −2`, `Uᵢ = 2` and the Gurobi use are on p. 16. The sha256 values of all
  four new PDFs equal those in `r1-work/MANIFEST.md`. My own WebSearch queries
  (separation of clique inequalities for the Boolean quadric polytope; NP-hardness of
  hypermetric separation, 2025–2026) found no earlier resolution. The novelty caveat
  remains appropriate.
- **Processes.** No process of this stream was running when I started; `pgrep` and
  `/proc/PID/cwd` showed only split-practice, multiround, scip-set-selection and
  `research-20260929` jobs. My own runs were in the foreground or waited for, with
  `timeout` limits and at most two at a time, and all finished.

## Major issue

### R2-M1. Separation of Padberg's clique inequalities (10) is settled by the note's own construction, but the note says it is open

*Where.*
- Remarks after Corollary 8, first bullet: "Padberg's clique inequalities (10) remain
  open. Their vectors `v = 𝟙_S` have only positive entries, while the violators here
  have mixed signs. The same holds for their cut images, the Barahona–Mahjoub clique
  inequalities (18) without switching."
- §7, Letchford bullet: "Padberg's clique inequalities (10) remain open."
- §8 discussion paragraph: "The complexity of separating Padberg's clique
  inequalities ... remains open."
- Limits, fifth bullet.
- Open question 4.
- The author's results list (the "Still open" entry).

*Claim (proved here; checked exactly).* Take an X3C instance with `q ≥ 3`, let
`N = 8n + 2p + 1`, and let `P = X(1/N)` be the point of Corollary 3. Let `P′ = π_g(P)`
be its switching on `g`: `x′_g = 1 − x_g`, `y′_ig = xᵢ − y_ig`, and all other
coordinates unchanged. Then:

- `P′` violates a clique inequality (10) if and only if an exact cover exists;
- the violated ones are exactly `S′ = C ∪ {g}`, `s′ = 1`, for the exact covers `C`,
  each violated by `1/(4N)`;
- they are facet-defining, because `|S′| = q + 1 ≥ 3` and `1 ≤ s′ ≤ |S′| − 2`.

`P′` lies in `[0,1]` and has denominators dividing `4N`. For X3C,
`x′_g = 1 − (2p−1)/(4N)` and `y′_ig = 22/(4N)`. Its moment matrix `A P Aᵀ` (with `A`
invertible) is positive definite with `X′ᵢᵢ = X′₀ᵢ`, and `P′` satisfies all Boolean
quadric triangle inequalities, including McCormick. Hence separation of (10) is
strongly NP-complete. Membership in NP is trivial: the certificate is `S′`, with
`s′ = ⌊x(S′)⌋`.

*Proof.* `π_g` is an affine involution that maps the Boolean quadric polytope onto
itself. On 0/1 points it complements `x_g`, and it acts on the linearized monomials
consistently: `x_g xᵢ ↦ xᵢ − x_g xᵢ`. Hence for every Boros–Hammer datum `(v, s)`, the
slack of `(v, s)` at `π_g(P)` equals the slack of `(v′, s − v_g)` at `P`, where `v′` is
`v` with `v_g` negated. This map sends the family (12) (`v = 𝟙_S − 𝟙_T`) onto itself.

By Corollary 8, the members of (12) violated at `P` are exactly `(𝟙_C − e_g, 0)` and
its equivalent form `(e_g − 𝟙_C, −1)`. Their images are `(𝟙_C + e_g, 1)` and its
equivalent form, that is, the clique inequality (10) with `S′ = C ∪ {g}` and `s′ = 1`.
This `s′` lies in the admissible range `0..|S′|−1`. Every clique inequality (10) is a
member of (12) with `T = ∅`. So every violated (10) at `P′` is the image of a violated
(12) at `P`, and therefore comes from a cover. ∎

The note already uses exactly this switching in its facet proof (Corollary 8, "the
violator `(𝟙_C − e_g, 0)` is the switching of the clique inequality (10) with
`S′ = C ∪ {g}` and `s′ = 1`"). So the stated reason for openness, the sign pattern of
`v`, does not apply: the input point can be switched.

*Check [G]* (`r2-work/independent_check_r2.py`). On 40 instances (30 X3C with
`q ∈ {3,4}` and 10 general exact-cover instances), I enumerated all `S` and every
admissible `s` at `P′`, in exact arithmetic. The violated clique inequalities were
exactly `{(C ∪ {g}, 1)}`, with violation `1/(4N)`. `P′` was positive definite and in
`[0,1]`, and the Boolean quadric triangle family held if and only if no cover uses at
most 2 sets. There were 0 failures.

*The same trick for (18).* Take Corollary 5's point `εd′`, with `q − 2` copies of
`0`, and switch it in cut form on `U = {g} ∪ {copies}`. Cut switching maps odd clique
inequalities to odd clique inequalities, `b ↦ diag(s_U)b`, and preserves the
violation. Among the pure violators at `εd′`, `(b₀, b_copies, 𝟙_C, −1)` with
`b₀ + Σb_copies = 2 − q`, exactly one per cover becomes a 0/1 vector:
`b = 𝟙_C + e_g + Σe_copies`, which has odd support `2q − 1`. Hence separation of the
Barahona–Mahjoub clique inequalities (18) without switching is strongly NP-complete,
at points in the metric polytope and the elliptope. For `q ≥ 4` these points still
have repeated points, because the copies stay at mutual distance 0.

*Check [H].* On 30 X3C instances with `q ∈ {3,4,5}`, I enumerated all odd 0/1 vectors.
The violated (18) were exactly `{𝟙_C + e_g + Σe_copies}`, the switched points lay in
the metric polytope, and there were 0 failures.

So what remains open is (18) and the cut-form odd clique family at points without
repeated points (the note's open question 3), not (10).

The first remark also says that (18) are "the cut images" of (10). This is
inaccurate. Letchford (2022, p. 11) obtains (18) only from the subfamily of (10) with
`|S|` odd and `s = (|S|−1)/2`. The cut image of a general (10) is a rounded psd
inequality whose root coefficient is in general not in `{0, ±1}`.

*Fix.*
1. Add a short corollary, for example Corollary 9, with the claim and proof above:
   (10) is strongly NP-complete at `π_g(X(1/N))`. Optionally add the (18) statement
   for repeated points.
2. Rewrite the remarks after Corollary 8, the Letchford bullet in §7, the §8
   paragraph (Letchford's whole list (10)–(13) is now settled), the Limits bullet,
   open question 4 and the results list. What remains open is (18) and the cut-form
   odd clique family at points without repeated points.
3. Correct the "cut images" sentence.
4. Add the clique family to the solver-relevance list in §9 and the Summary.

## Optional

- **o1.** Corollary 8 attributes the switching rule `(v, s) ↦ (v′, s − v_g)` to
  Letchford (2022, p. 9). That page states only the sign change of `vᵢ`. The shift of
  `s` is a one-line computation (`vᵀπ(x) = v′ᵀx + v_g`), which the note could give
  itself.
- **o2.** §2 table and §7 say that Dey et al. (2026) "make no complexity statement".
  On p. 4 they recall that Boros and Hammer gave polynomial-time separation for
  certain subclasses (by minimum spanning trees). "No complexity statement about the
  full class" would be exact.
- **o3.** §9 and the Lemma 5 remark say that `s` stays bounded for some families,
  citing "Lemma 5 and §10". Lemma 5 gives only an upper bound that grows with `n`.
  The closed form `s(n) = 77(193n + 108)/(4(141n + 272)) → 14861/564` for the family
  of `n` copies of `{0,1,2}` plus `{3,4,5}` would make the statement proved. The note
  could also say that the bound of Lemma 5 is nearly attained, for example by
  singleton families.
- **o4.** In the remark on Letchford's condition for (11), add that the chapter's
  own remark (p. 8: `|S| = 2`, `|T| = 1` gives the triangle inequality (9)) agrees
  with the printed formula. Padberg's orientation of the cut inequalities, with
  `x(S)` on the right, is commonly cited, and the printed condition fits that
  orientation; my check [D] confirms that this form is a facet for
  `(|S|,|T|) = (1,2), (1,3), (2,2)`. So either the formula or the condition was
  transposed in the chapter. "Apparently" already hedges this.
- **o5.** Summary item 3, last bullet: "odd clique inequalities in cut form, that is,
  pure hypermetric inequalities". The odd clique family is larger than the pure
  hypermetric family. Corollary 5 proves hardness for both, so "and pure hypermetric
  inequalities" would be accurate.

## Checks run by the reviewer

All commands were run from `research-20261001/binary-separation/` with a `timeout`
limit, at most two at a time. Outputs are in `reviews/r2-work/`.

1. `timeout 900 python3 code/check_binary_separation.py` → `ALL CHECKS PASSED`
   (13.5 s). The output is identical to `logs/check_binary_separation.log` apart from
   timing.
2. `timeout 600 python3 code/probe_gap.py 3`, `timeout 900 python3 code/probe_gap.py 3 5 5 30`
   and `timeout 900 python3 code/probe_gap.py 2 6 6 20` → 27, 12 and 9 no-instances,
   0 violations. All three outputs are identical to the logs apart from timing.
3. `timeout 600 python3 code/probe_cutcone.py` → 24 of 24 in the cut polytope.
   `timeout 300 python3 code/scip_crosscheck.py` → 24 instances, 0 disagreements.
   Both are identical to the logs apart from timing.
4. `timeout 600 python3 code/check_gap0.py` → identical to `logs/check_gap0.log`
   apart from timing (23.5 s).
5. `timeout 1200 python3 reviews/r2-work/independent_check_r2.py` →
   `reviews/r2-work/independent_check_r2.log`, `REVIEWER R2 CHECKS PASSED`, 16.5 s.
   This is my own exact code, with a top-down `LDLᵀ` Fincke–Pohst enumeration
   different from the author's:
   - [A] Lemma 5 on 81 instances, 0 failures; maximum ratio of `s` to the bound
     0.9998;
   - [B] Corollary 3(c)–(e) on 70 instances, 0 failures;
   - [C] Corollary 8 and a bounded Boros–Hammer box search on 40 instances, 0
     failures;
   - [D] facets by exact rank, all as expected;
   - [E] Theorem 1 at `η² = p/12` on 80 instances, 0 failures; the controls below
     `p/12` behave as expected;
   - [F] the switching identity of Corollary 4(ii), 300 trials, 0 failures;
   - [G] switched points: violated (10) are exactly `(C ∪ {g}, 1)`, 40 instances, 0
     failures;
   - [H] switched Corollary 5 points: violated (18) are exactly
     `𝟙_C + e_g + copies`, 30 instances, 0 failures;
   - [I] floating-point LP: `εd` is in the cut polytope for 30 of 30 no-instances with
     4–6 points.
6. An exact computation of `s` on degenerate families (singletons, empty sets, full
   sets, pairs of [7]), and a sympy closed form of `s(n)` for the bounded family.
7. Literature:
   - `sha256sum` of the four new PDFs and of arXiv:1503.04554, all matching their
     manifests;
   - page-split reads of `letchford2022-qubo-chapter.txt` (pp. 6, 8–12, 16, 18–20 and
     the section headings), the BiqBin and MADAM texts, Dey et al. (pp. 4, 15–17) and
     arXiv:1503.04554 (p. 1);
   - WebSearch: "separation problem clique inequalities Boolean quadric polytope
     NP-hard" and "hypermetric inequalities separation NP-hard proof exact cover 2025
     OR 2026". Neither found an earlier resolution.
8. `pgrep -af python3` with `readlink /proc/PID/cwd`: no process of this stream was
   running. All my jobs finished before I wrote this review.

## Required change for a clean verdict

R2-M1: add the switching corollary for (10), with the optional (18) statement for
repeated points. Then correct the six places listed above, and the "cut images"
sentence. My check [G] can serve as the exact check, or the author can add an
equivalent check to `code/check_binary_separation.py`.
