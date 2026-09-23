# Stage 5 corrections

Correction agent: `correction_agent`, distinct from the stage author and five
reviewers. Date: 2026-09-07. Authority:
`process/assessments/stage05-round01.md`, with the root's clarification about
affine upper constants. All three accepted minor issues are fixed; no accepted
issue remains unresolved. Root acceptance remains pending.

## Changes and verification

| Issue | Change | Verification |
| --- | --- | --- |
| S5-1 | The first Sugishita–Carvalho citation in `sections/05-boundaries.tex:23` now uses “Theorem 1 and Section 4.” | Visually checked the primary v2 PDF page 3, retained as `verification/reviewer02/stage05/sugishita-p3.png`. It explicitly labels the NP-completeness theorem “Theorem 1” and points to Section 4 for the proof. No bibliography or scientific attribution changed. |
| S5-2 | Added `cor:dense-multiplicative` and its full short proof immediately after the dense-gap proof. Added its Section 8 source and label to the stage 5 coverage table. | Independently checked nonnegativity on every exact response, both objective gaps, polynomial binary encoding after scaling, eventual domination of every fixed polynomial ratio, and the finite-small-size case. The argument below details these checks. The new prose explicitly treats the constant as affine upper data and retains the exact-feasibility, coefficient, and hardness qualifications. |
| S5-3 | Wrapped the complete `prop:single-power-output` statement in a local standard LaTeX `samepage` environment. | The unchanged statement, including both examples, strict-anchor qualification, and sparse-upper assertion, is together on PDF page 44. Its displayed number is now Proposition 5.13 because of the added corollary. No hard page break or mathematical wording changed. |

The following subsection's phrase “the last proof” now explicitly references
`thm:dense-hardness`, preserving its intended referent after insertion of the
new corollary. No existing proof was changed.

## Independent check of the multiplicative consequence

I read `notes/bilevel-dense-box-hardness-investigation.md`, Section 8, and
the actual manuscript's dense-gap proof. The identity
`H=2 sum_i min(y_i,1-y_i)+2 sum_a v_a` makes `H` nonnegative at every exact
response. Its optimum is zero for satisfiable formulas and at least two
otherwise. Thus `1+H` is strictly positive on the bilevel feasible set,
with optimum one versus at least three. A feasible minimization output with
ratio below three has value below three only in the satisfiable case.

For `s=n+m`, the scaled objective `1+2^s H` has optimum one versus at least
`1+2^(s+1)`. Each scaled nonzero upper coefficient has magnitude `2^(s+1)`,
requiring `s+2` binary magnitude bits and a sign bit; there are polynomially
many coefficients.
The follower construction is unchanged, so the full input length is bounded
by a fixed polynomial in `s`. For any fixed polynomial ratio bound `q`,
`q(L(s))` is therefore polynomially bounded in `s`, and hence eventually
smaller than `2^s`. Comparing the exactly feasible returned value with `2^s`
decides all sufficiently large source formulas. Exhaustive search for the
finitely many smaller values of `s` takes bounded time with respect to this
reduction and completes a polynomial 3SAT algorithm. No assumption about a
constant gap surviving coefficient normalization is used.

The additive constant is ordinary affine upper data. The corollary does not
claim to preserve the original exact coefficient alphabet; exponential
scaling also removes the bounded-upper-coefficient restriction. It preserves
polynomial binary encoding and requires exact follower optimality and
bilevel feasibility. The conclusion is an elementary gap consequence, not
strong hardness or a claim about approximate followers. These direct
inequality and encoding arguments need no broad repetition of the already
reviewed reduction diagnostics.

## Build, layout, and source integrity

Before editing, all thirteen live and frozen source files matched
`process/snapshots/stage05-round01/SHA256.json`. The manifest digest remains
`c25d5edb69e64647034e54fea863d4637e410b2a22461e8d3d378741d67fd6b5`,
and all frozen file hashes remain valid. I inspected the full diff: only
`sections/05-boundaries.tex` and `process/coverage.md` changed, as recorded
above. Every existing stage 5 proof block remains byte-identical. Earlier
accepted mathematical files, the path appendix, bibliography, main, and
README are unchanged.

All manifest-listed live files were copied to the isolated directory
`verification/correction-agent/stage05/source/` and built there with:

```sh
latexmk -gg -pdf -interaction=nonstopmode -halt-on-error -outdir=../build main.tex
```

After replacing the newly ambiguous “last proof” reference, I rebuilt the
isolated copy with the same command without `-gg`. The final isolated sources
match the corrected live sources. The resulting
`verification/correction-agent/stage05/build/main.pdf` has 63 pages and
207 unique labels. Its final log has no warnings, undefined citations or
references, overfull or underfull boxes, or fatal errors. I visually inspected
pages 35 and 44: the new corollary and proof, and the full output proposition,
are legible without clipping or overlap.

Evidence under `verification/correction-agent/stage05/` includes
`build-command.log`, `final-main.log`, `source.diff`, `checks.json`,
`rendered.txt`, `corollary-page35.png`, and `proposition-page44.png`.
The verified PDF is the isolated one; the main live build directory was not
rebuilt.

Remaining accepted issues: **none**. Root status, assessments, frozen
snapshots, and unrelated repository files were untouched. Stage 6 was not
started, and no work was delegated.
