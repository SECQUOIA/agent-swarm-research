# Stage 4 corrections

Correction agent: `correction_agent`, distinct from the stage author and five
reviewers. Date: 2026-09-07. I read the root assessment and all five completed
stage 4 reports. All four accepted minor issues in
`process/assessments/stage04-round01.md` are fixed. No accepted issue remains
unresolved; root verification and acceptance remain pending.

## Changes

| Issue | Change and verification |
| --- | --- |
| S4-1 | In `sections/04-accuracy.tex`, subsection 4.6, introduced `d_h` for univariate inverse-branch degree and `d_a=max{1,max_i deg a_i}` for argument degree. The composed response degree is at most `d_h d_a`, so upper substitution has degree at most `D_up max{1,d_h d_a}`. The text supplies the aggregate-degree bound and handles constant or zero aggregate cost. The independent degree reasoning and exact example below verify the correction. |
| S4-2 | Added one paragraph immediately before `prop:accuracy-response-modulus` in `appendices/c-quantitative-bounds.tex`, citing Jeyakumar–Lasserre–Li–Phạm, Theorem 2.3. It specifies the compact, leader-independent feasible set and one-sided inclusion at a fixed reference leader. It distinguishes the present uniform pairwise exponent `1/P`, effective rational constant, and affine moving resource right-hand sides. The existing primary bibliography entry suffices. |
| S4-3 | Updated the README opening to identify accepted stages 1–3 and the included stage 4 accuracy draft and two appendices, pending completion of the correction gate. Replaced the obsolete stage 3 pending-review sentence in `process/coverage.md` with its accepted disposition. Stage 4's heading and closing paragraph now record completed reviews and pending root verification. The limitations of finite diagnostics and later-stage assignments are preserved. |
| S4-4 | Added the two-line gradient-splitting identity and bounds for its two gradient differences in `appendices/c-quantitative-bounds.tex`. The optimal-gradient difference annihilates `e-d`, producing the stated identity with the same active-row correction `d`. No theorem statement, constant, or subsequent inequality changed. |

## Independent mathematical and citation checks

For S4-1, composing a univariate polynomial of degree at most `d_h` with
an argument of degree at most `d_a` gives degree at most `d_h d_a`.
An upper monomial `x^alpha z^beta` therefore has substituted degree at most
`|alpha| + |beta| d_h d_a`, which is bounded by
`D_up max{1,d_h d_a}`. Differentiating the aggregate in an aggregate
coordinate lowers its total degree by at least one; the normalization of
aggregate variables is affine, and the incentive and multiplier terms are
affine. Hence `d_a <= max{1,deg phi-1}` for nonconstant aggregate cost,
with `d_a=1` for a constant or zero aggregate. Fixed compressed dimension
then preserves the polynomial monomial-count argument.

One narrow exact SymPy check confirms that the linear inverse branch `h(a)=a`
composed with `a(x,w)=x-w^3` has degree three, also after `w=2t-1`.
At `x=17/64` and `w=1/4`, its value is `1/4`, so the cited example is an
exact interior response candidate. The corrected bound gives three for
the linear upper objective. This finite calculation supports the local
correction; the preceding argument establishes the general bound.

For S4-4, write `A=grad F_x(z)`, `B=grad F_{x'}(z')`, and
`C=grad F_x(z')`. The common active-row span gives
`(A-B)'(e-d)=0`. Consequently `(A-C)'e=(A-B)'d+(B-C)'e`.
The triangle inequality bounds the first gradient difference by
`A_z ||e||_infinity + A_x Delta`; the second is bounded by `A_x Delta`.
Combining these with `||d||_infinity <= D_b Delta` gives exactly the two
existing terms, with the same factor `N`. No broader diagnostic rerun was
needed.

For S4-2, I followed `../literature/AGENTS.md` and read the primary text
`[[jeyakumar2016-convergent-semidefinite-programming-relaxations-for]] p.5-6`,
including Theorem 2.3 and its proof. I visually checked original PDF page 5:
its displayed inclusion is
`Y(x) subset Y(xbar) + c ||x-xbar||^tau B`, for a fixed reference `xbar`.
The constraints depend only on follower variables, and the feasible set
is compact. The exponent formula depends on polynomial degree, follower
dimension, and constraint count. The comparison does not attribute
two-sided set-valued continuity, a uniform pairwise constant, or a rational
bit bound to that theorem. The inspected local original is the revised
arXiv manuscript associated with the existing published bibliography entry;
no uninspected final-paper page locator was added. No literature file was
changed or copied into this paper.

## Build, layout, and integrity

Before editing, all eleven live and frozen source files matched
`process/snapshots/stage04-round01/SHA256.json`. The manifest digest remains
`4ef85d87d33a7c0860e735f7daa7311f1bc61f20b3ae6a36585f05ffe268befe`,
and every frozen file still matches its hash. I inspected the complete diff;
only README, coverage, section 4, and appendix C changed, as described above.
Earlier accepted sections, the inverse appendix, bibliography, and main file
remain unchanged.

I copied all manifest-listed live files to
`verification/correction-agent/stage04/source/` and built that isolated copy:

```sh
latexmk -gg -pdf -interaction=nonstopmode -halt-on-error -outdir=../build main.tex
```

The clean build succeeded and produced
`verification/correction-agent/stage04/build/main.pdf`, with 46 pages.
The final log has no warnings, undefined citations or references, overfull or
underfull boxes, or fatal errors. I confirmed the isolated sources match the
corrected live files and visually inspected pages 29, 42, and 43, containing
the degree correction, citation comparison, and gradient identity. These
passages are legible without clipping or overlapping content.

Evidence under `verification/correction-agent/stage04/` includes
`build-command.log`, `final-main.log`, `source.diff`, `checks.json`,
`rendered.txt`, `degree-page29.png`, `modulus-42.png`, and `modulus-43.png`.
The main live build directory was not rebuilt; the verified PDF is the isolated
one linked above.

Remaining accepted issues: **none**. Root status, assessments, and frozen
snapshots were not edited. No stage 5 work or delegation was started.
