# Stage 1, round 1 — independent review 02

Verdict: **accept after minor corrections**. I found no major issue in the stage 1 foundations or coverage plan. Two wording corrections are needed to keep the stated semantic and encoding scope precise. This verdict applies to stage 1; it does not certify the proofs assigned to later stages.

## Inspected version and independence

I read all five frozen inputs in `process/snapshots/stage01-round01`: `main.tex`, `sections/01-foundations.tex`, `references.bib`, `README.md`, and `process/coverage.md`. The SHA-256 digest of `SHA256.json` is `2230f1e9da9d015278c6bbf424d04167961f6c7911646ca287e899b9ccae36de`; every listed file matches its manifest hash. Locators below refer to this snapshot.

I did not read another current reviewer’s report, coordinate findings, delegate, or edit the manuscript. I read `literature/AGENTS.md` before using the literature collection and made no literature changes. All build and verification artifacts are under `verification/reviewer02/stage01-round01`.

## Findings requiring correction

### R02-01 — minor: specify the optimistic convention in the classical positive result

**Locator:** `sections/01-foundations.tex:24–27`, with the semantic comparison at lines 35–45.

The sentence attributes a polynomial algorithm to the fixed-follower-variable restriction without naming the optimistic convention. This matters because the paper subsequently treats both conventions, and its pessimistic definition uses universal upper feasibility. Under that convention, fixed follower dimension alone is not the positive result being cited.

**Primary evidence:** Ketkov–Prokopyev, Table 1 and the discussion of Deng, [[ketkov2026-on-the-complexity-of-bilevel]] p.4, explicitly distinguish optimistic polynomial solvability from pessimistic hardness and explain the ambiguity in the historical pessimistic statement. I checked this page against the original PDF image. Their Theorem 1 explicitly states the optimistic positive result, p.8. The [Liu–Spencer publisher abstract](https://www.sciencedirect.com/science/article/pii/037722179400005W) and [Deng publisher abstract](https://link.springer.com/chapter/10.1007/978-1-4613-0307-7_6) support the fixed-follower-dimension attribution, but do not eliminate the need to specify the convention when comparing with this manuscript’s pessimistic model.

**Actionable fix:** Begin “Classical positive results for optimistic linear bilevel optimization fix the number of follower variables,” or explicitly attach “optimistic” to the following polynomial-algorithm statement. A short sentence explaining that universal pessimistic upper feasibility changes the classification would also make lines 43–45 more informative. No change to the manuscript’s definitions is needed.

**Severity rationale:** The surrounding discussion correctly emphasizes semantic distinctions, and this is a local qualification rather than a flaw in the proposed structural algorithm.

### R02-02 — minor: preserve numerical-degree dependence in the algebraic output guarantee

**Locator:** `sections/01-foundations.tex:211–213`, compared with lines 195–203.

The running-time paragraph carefully promises a polynomial bound in `(L, delta)` and distinguishes that from polynomial time in `L`. The following output paragraph instead says degree and combined encoding are “bounded polynomially in the input size,” without carrying over the degree condition. Read literally with the explicitly permitted sparse binary exponent encoding, this is too strong.

**Mathematical evidence:** Let `D=2^n`, choose one leader variable with compact domain `C={x:1<=x<=2, x^D=2}`, and take a trivial one-variable quadratic follower constrained to `z=0`, with `Q=1`, no aggregate, and upper objective `F=x`. This fits the primary model with fixed structural dimensions. Sparse binary input length is `O(n)`, while the unique leader has degree `D`, since `T^D-2` is irreducible by Eisenstein’s criterion at 2. Every common field containing that leader has degree at least `D`. This agrees with the earlier `(L, delta)` guarantee but contradicts an unconditional polynomial-in-`L` output-degree promise.

**Actionable fix:** Replace the sentence by “These quantities are bounded polynomially in `(L, delta)` for the stated fixed dimensions, and polynomially in `L` under the degree-encoding condition above.” Equivalent explicit wording is sufficient.

**Severity rationale:** The correct convention is already established immediately before this paragraph, and the inventory expressly retains the sparse-exponent obstruction. The intended claim is clear; the output statement should state it consistently.

## Literature and coverage assessment

The principal comparison is sound. The manuscript fixes leader, block, aggregate, and shared-resource dimensions while allowing follower dimension and local row counts to grow. Ketkov–Prokopyev’s fixed follower-variable count and fixed total follower-constraint count cannot simply be identified with these parameters. Their optimistic convex-quadratic theorem has its own upper quadratic assumptions and does not contain the nonconvex aggregate model. Sugishita–Carvalho’s scalar-leader hardness has coupled follower constraints; it is not incorrectly presented as hardness for a fixed-box, well-conditioned SPD follower. The version dates and titles match the [Ketkov–Prokopyev v2 record](https://arxiv.org/abs/2511.15592v2) and [Sugishita–Carvalho v2 record](https://arxiv.org/abs/2510.21126v2).

Megiddo–Tamir is appropriately credited for the local multiplier and quadratic-block elimination principle. Their general model fixes local row counts as well as block sizes and shared rows, [[megiddo1993-linear-time-algorithms-for-some]] p.6-8; I checked the model’s assumptions against the original PDF. The manuscript does not attribute its unrestricted local-row extension or global nonconvex bilevel comparison to that source.

Basu–Pollack–Roy’s cited Theorem 1.3.1 and Section 3.1.3 are real and relevant: the former provides quantifier elimination, while the latter constructs univariate representations meeting every cell, with degree and bit bounds for fixed dimension; [[basu1996-on-the-combinatorial-and-algebraic]] p.3-4, p.27-28. The manuscript correctly controls bound as well as free variables. Hoffman’s source supplies the fixed-matrix residual-to-distance bound, [[hoffman1952-on-approximate-solutions-of-systems]] p.1-2. The equality extension and norm equivalence are valid.

The separation of near-optimal feasibility robustness from a worst-case upper objective matches [Besançon–Anjos–Brotcorne, Section 2](https://link.springer.com/article/10.1007/s10898-024-01422-z). Buchheim’s NP certificates and polynomial-bit valid big-M values are not misrepresented as a polynomial global optimizer; see [[buchheim2023-bilevel-linear-optimization-belongs-to]] p.3-7.

I compared the inventory with `notes/bilevel-paper-scope.md`, `notes/bilevel-response-complexity-map.md`, `notes/bilevel-classical-positioning.md`, the reopened and nonconvex closeouts, the relevant broad closeout material, and the canonical block/response-semantics statements. I also checked the listed repository paths: all 72 distinct explicit `results/`, `notes/`, and `code/` paths exist. I found no missing substantive development in this stage’s assignment map. In particular, it preserves the signed inverse proof dependency, sharper one-resource result, both dense-box reductions, small-gap accuracy-bit boundary, conditioned approximation, both different path constructions, moving normals and nonattainment, common-field witness limitation, adverse screening evidence, and original-response contact reconstruction. The fixed-core and affine-strip dependencies have explicit scope limits. Path existence is not proof verification; each later stage must still discharge its assigned proofs.

An optional improvement, rather than an acceptance condition, is to make the approximation comparison at lines 59–65 more explicit. Hochbaum–Shanthikumar’s continuous resource-allocation result already has logarithmic accuracy dependence in its stated oracle/matrix setting, [[hochbaum1990-convex-separable-optimization-is-not]] p.2-4. Vigneron optimizes sums globally, but for nonnegative algebraic functions of constant description complexity and with FPTAS dependence on inverse relative error; [[vigneron2014-geometric-optimization-and-sums-of]] p.1-3. One sentence stating these distinctions would help readers understand why growing degree, signed upper objectives, and accuracy-bit dependence matter. The present broad statements are not false.

## Mathematical and presentation checks

- The fixed-normal compact model permits empty fibers and gives bounded unions from continuous coordinate endpoints on compact `C`. The definitions only use `v(x)` on feasible leaders and do not introduce vacuous robust feasibility at empty fibers.
- Optimistic feasibility, universal pessimistic feasibility, and near-optimal robustness are distinct and internally consistent. Fixed-leader worst responses are attained on compact sets; leader infima are correctly allowed to be unattained.
- The substitution lemma is correct: the denominator exponent is nonnegative for every input monomial; fixed dimension bounds the expanded support; rational coefficient growth is polynomial in the stated numerical degrees; positive denominators preserve signs.
- The common-field representation correctly permits a nonminimal square-free polynomial and does not promise a polynomial-degree compositum of unrelated witnesses. XP-type dependence is correctly distinguished from FPT.
- The foundations are readable and the notation is sufficiently introduced for this stage. I do not flag the deliberately deferred abstract, main theorem proofs, experiments, or synthesis as missing stage 1 work.

The isolated build used `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=../build main.tex` from the copied source directory. It completed successfully with no warning, undefined-reference, undefined-citation, overfull, or underfull diagnostics in the final log. Evidence: `verification/reviewer02/stage01-round01/build-command.log`, `build/main.log`, `hash-check.txt`, and `coverage-path-check.txt`. An attempted Python PDF renderer failed because `fitz` was unavailable; original-page inspection succeeded using `pdftoppm` instead. No manuscript source was changed.

## Access limits

The historical Liu–Spencer and Deng originals were not retrieved in full; I used their publisher abstracts for the broad attribution and the inspected modern primary theorem for the semantic distinction. The local Vigneron text is an author manuscript dated 2011 rather than the final typeset 2014 article; the checked scope comparison uses its explicit statements. I inspected relevant statements and surrounding text in the other primary sources, not every proof in every cited paper. The search was bounded and establishes neither exhaustive literature coverage nor publication priority. No result relies on a repository review’s approval label as theorem authority.
