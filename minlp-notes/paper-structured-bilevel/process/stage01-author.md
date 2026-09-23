# Stage 1 author record

Date: 2026-09-07. Scope: foundations and manuscript scaffold, plus comprehensive
source-to-stage inventory. This record does not mark the stage accepted; five
independent reviews and root assessment follow.

## Files authored

- `main.tex`: standard article preamble, theorem environments, common notation,
  title without invented author identity, reviewed-stage input structure.
- `sections/01-foundations.tex`: six subsections covering motivation and related
  work; fixed-normal quadratic-block model; optimistic, universally feasible
  pessimistic and near-optimal semantics; input/degree/output conventions; and
  the real algebraic/Hoffman tools. One elementary substitution lemma is proved
  in full. No main exact or approximation theorem is asserted before its stage.
- `references.bib`: 13 actual primary/survey sources with verified metadata and
  version-specific arXiv entries; no internal repository notes used as authority.
- `README.md`, `.gitignore`, `build/.gitkeep`: build and process guidance.
- `process/coverage.md`: all 14 canonical bilevel results and note-only
  developments, dependencies, code families, historical reviews, scope exclusions,
  and concrete stage 6 development assignment.

Root's `process/STATUS.md` was preserved. All substantive changes are inside
this new folder. An initial build command accidentally ran at repository root,
created an empty `build/` directory, and failed for lack of `main.tex`; the empty
directory was removed. No repository source files or literature files changed.

## Research and mathematical decisions

The primary model keeps local row counts growing while fixing block, leader,
aggregate, and shared-row dimensions. It allows empty follower fibers but
assumes compact leader domain and polynomial coordinate bounds. It retains
nonconvex aggregate costs and arbitrary explicit polynomial upper criteria.
The approximation and robust measurement restrictions are expressly separate.

The upper minimization convention is uniform. Revenue maximization is explicitly
its sign-reversed version, so later pessimistic revenue is a minimum over
responses followed by a leader supremum. Upper constraints never filter the
follower problem. Algebraic attainment and exactly feasible rational approximation
are separate guarantees. The complexity convention is polynomial in actual
numerical degree and input bits for fixed structural dimensions, hence XP-type,
with no unsupported FPT claim.

The substitution lemma checks a key expanding-encoding step: after substituting
N rational follower functions into an explicit polynomial, the number of
variables is fixed even though N and numerical degree grow. A common positive
denominator preserves inequality directions. The proof counts dense monomials
in fixed dimension and coefficient growth; no arithmetic circuit shortcut is
assumed.

The inverse theorem, fixed-resource quantitative bounds, and rational recovery
are recognized as substantial stage 4 proof obligations. The Klee--Minty
follower-path theorem is separate from the growing-leader path theorem and
requires the telescoping/slab development. The fixed-core polyhedral theorem is
a related supporting elimination framework; its pooling corollaries are outside
the bilevel topic. The restricted affine-strip positive projection provides a
useful boundary to general path obstructions and should not imply arbitrary
path value-function compression.

No claim of complete novelty, production solver superiority, or mathematical
impossibility of future improvement is made. The final stage must produce a
complete paper with closed proof dependencies; it cannot responsibly promise
that all possible future research has been exhausted.

## Source checks

Read `literature/AGENTS.md`; did not edit generated literature files or copy
user-supplied originals. Read principal exact source proofs, compressed semantics,
classical positioning, scope map, bilevel closeouts and the relevant parts of
broad closeouts. Inspected theorem/header structure across every canonical
bilevel result and the specified proof dependencies to create the inventory;
full new audits of those future-stage proofs remain assigned work.

Direct primary text used for core foundations:

- Basu--Pollack--Roy (1996): local full text, statement and bit model in Section
  1.3, Theorem 1.3.1; univariate representation and sample points in Sections
  3.1.1 and 3.1.3. These support fixed-total-variable QE and common-field output.
- Hoffman (1952): local primary text pp.1--2, uniform-in-right-hand-side bound.
- Ketkov--Prokopyev: local primary text Theorem 1 and Table 2 plus online arXiv
  v2 record (June 10, 2026). Root initially questioned a historical note's
  Theorem 1 locator, then checked the theorem and withdrew the concern: it
  explicitly covers either fixed follower variable or fixed constraint count.
  No source correction is warranted.
- Sugishita--Carvalho: local primary statement/record and online arXiv v2
  abstract (March 20, 2026); global NP-completeness distinguished from local
  algorithm.
- Liu--Spencer: publisher abstract, author names, volume/issue/pages and DOI
  confirmed at https://www.sciencedirect.com/science/article/pii/037722179400005W.
- Deng: publisher chapter page at
  https://link.springer.com/chapter/10.1007/978-1-4613-0307-7_6;
  only broad fixed-follower complexity attribution used, not an unread theorem.
- Besançon--Anjos--Brotcorne: final publisher article/primary institutional
  record, DOI 10.1007/s10898-024-01422-z, JGO 90:813--842 (2024), Section 2
  near-optimal set. Distinguish its established upper-feasibility robustness
  model from the manuscript's additional worst-case objective.
- Other entries: local primary metadata and recorded relevant source passages;
  Kleinert and Beck volume/article/pages additionally checked against their
  publisher records. Megiddo--Tamir's role is local block/multiplier elimination;
  Hochbaum--Shanthikumar is high-accuracy follower resource allocation;
  Vigneron is algebraic-function approximation. No detailed uninspected
  external theorem is invoked as a missing proof dependency.

The bibliography is intentionally limited to citations used now. Later stages
must add and verify their own required primary sources (e.g. Adler--Beling,
Klee--Minty shadow authors, ReLU parameterized hardness, screening and envelopes).

## Validation

Built from `paper-structured-bilevel/` with:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

Result: `build/main.pdf`, 6 pages. Final LaTeX log has no undefined citations,
undefined references, overfull/underfull boxes, or other warnings. Build transcript
is `build/stage01-build.txt` (generated artifact). All backtick-delimited explicit
repository paths in the coverage map were checked for existence: no missing
paths. The author found and repaired one initial missing `\Z` macro during
compilation. No mathematical verification program was rerun merely to support
this foundations-only stage.

## Remaining work assigned, not omitted

Stages 2--6 own every main theorem proof and computation listed in coverage.
Stage 7 owns the final abstract, contribution map and paper-wide integration.
Commented future `\input` lines are only a development scaffold; there is no
visible placeholder theorem or invented result in the compiled manuscript.
The current draft is explicitly not a finished paper. This stage now awaits
five independent reviews of its model, conventions, source claims, coverage,
and readability before any subsequent authoring begins.
