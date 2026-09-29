# Prior audit of adaptive PosSLP compilation

Date: 2026-09-28. Status: independent literature and significance audit.

The [adaptive compiler](adaptive-integer-sign-circuit-compilation.md) should
not yet be described either as established folklore or as a newly resolved
open problem. The sources examined establish the classical approximation
machinery, the oracle characterization of constant-free real computation,
and several individual many-one reductions. They do not establish the
general deterministic elimination of adaptive integer sign gates. A closely
matching model occurs explicitly in Balaji's 2016 thesis. The exact
many-one closure theorem was not located, but this search does not establish
novelty.

The proposed consequence is best written

\[
 \mathrm P^{\mathrm{PosSLP}}
 =\{L:L\le_m^p\mathrm{PosSLP}\},
\]

or as many-one completeness of PosSLP for its polynomial-time oracle class.
Writing the right side simply as `PosSLP` confuses a decision problem with
a class unless that convention is defined. This is a change in reduction
strength; it gives no ordinary polynomial-time algorithm for PosSLP and no
automatic practical improvement in an optimization solver.

## Closest source on the actual sign-gate model

[Nikhil Balaji, *Succinct Numbers, Skew Circuits and Bounded Treewidth*,
2016 thesis](https://libarchive.cmi.ac.in/theses/nikhilbalaji_cs2016.pdf),
Section 3.5.1, printed page 48, defines \(\mathrm{PosSLP}^{O}\) for a
straight-line program with basis \(\{+,-,\times,>\}\), where an internal
unary `>` gate tests whether its integer input is positive. Lemma 3.30 gives
a counting-hierarchy upper bound by guessing the comparison outputs and
checking their consistency with PosSLP queries. The surrounding text treats
this as an apparently stronger model. It does not give a deterministic
many-one reduction eliminating these gates.

This is a substantially closer antecedent than a generic reference to BSS
machines. The repository proposition would apply to this model after
appending one threshold gate to make the final output Boolean. Its
comparison to this source is therefore precise: it would replace the
oracle/guessing argument by a polynomial-time construction of one ordinary
integer arithmetic circuit with the same final positivity answer.

Access limitation: the indexed text of the primary PDF supplied the entire
subsection and lemma; a direct PDF fetch was unsuccessful. The subsection
was independently located and read by two agents. The rest of the thesis,
its surrounding chapter, and possible publications derived from it have
not been fully audited. This is a promising citation lead, not a complete
priority determination.

## What the foundational numerical-analysis paper establishes

Allender, Bürgisser, Kjeldgaard-Pedersen, and Miltersen,
[*On the Complexity of Numerical Analysis*](https://people.cs.rutgers.edu/~allender/papers/slp.pdf),
SIAM J. Comput. 38 (2009), 1987–2006, was checked in the
[local full text](../../literature/papers/allender2009-on-the-complexity-of-numerical/fulltext.md)
and author PDF.

- Proposition 1.1 proves
  \(\mathrm P^{\mathrm{PosSLP}}=\mathrm{BP}(\mathrm P^0_{\mathbb R})\).
  Its proof simulates branch decisions using the oracle. It does not combine
  the resulting adaptive calls into one SLP.
- Proposition 1.3 states a Turing equivalence for the generic numerical
  computation task, which is a function problem. A decision-language
  many-one closure theorem would not, by itself, turn the whole explicit
  floating-point output into one Boolean oracle answer.
- Remark 3.1 eliminates division by tracking numerator and denominator.
  This handles rational arithmetic, not internal sign gates.
- Section 3, before Theorem 3.9, discusses short rational approximation
  circuits for elementary functions and cites Newton iteration, Kung–Traub,
  Brent, Salamin, and the Borweins. Theorem 3.9 concerns approximable
  constants and advice. Neither that theorem nor the inspected approximation
  paragraph states adaptive sign-gate elimination.

Thus Section 3 is strong methodological prior, but citing it as if it
already proves the compiler would overstate the inspected result. The
[earlier audit](posslp-boolean-closure-audit.md) identifies the specific
map \(2x/(1+x^2)\) as classical inverse-Newton sign iteration and identifies
prior work on scaled and composed rational sign approximants. Those
numerical ingredients are not claimed as new here. What requires its own
argument is their uniform use with circuit-size magnitude bounds, integer
separation, propagated error, and an adaptive-query interpreter.

## The square-root-sum consequence is already supported by prior work

The 2009 source initially suggests a possible novelty test, but later work
resolves it. Etessami and Yannakakis,
[*Recursive Markov Chains, Stochastic Grammars, and Monotone Systems of
Nonlinear Equations*](https://homepages.inf.ed.ac.uk/kousha/final_rmc_jacm_version.pdf),
JACM 56(1), author manuscript page 6, explicitly says that the reduction
from SQRT-SUM to PosSLP was known under Turing reductions and
“not known to be harder via P-time many-one reductions.” This is historical
evidence only. Its Theorem 5.1 reduces SQRT-SUM to a threshold question for
a stochastic grammar, equivalently a probabilistic polynomial system (PPS).

Etessami, Stewart, and Yannakakis,
[*A Polynomial Time Algorithm for Computing Extinction Probabilities of
Multitype Branching Processes*](https://epubs.siam.org/doi/10.1137/16M105678X),
SIAM J. Comput. 46(5) (2017), 1515–1553,
[accepted manuscript](https://www.pure.ed.ac.uk/ws/portalfiles/portal/29051677/revised_sicomp_sub_after_rev_august16_v3_1.pdf),
Corollary 6.6 and its proof on manuscript pages 34–36, explicitly gives
many-one reductions of strict PPS threshold comparison to PosSLP. The
proof constructs a prescribed sequence of Newton iterations as a circuit,
uses determinant circuits for matrix inversion, and clears divisions. It
explicitly distinguishes this construction from the generic multiple-call
oracle simulation. Composing this with the 2009 SQRT-SUM construction,
and using complement where needed, gives the older many-one route.
For integer-output PosSLP, complement is immediate from
\(N\le0\iff1-N>0\).

This audit independently read Corollary 6.6 and its circuit construction
after another reviewer identified them. The Edinburgh cover sheet has
incorrect bibliographic metadata for the second author and journal; the
manuscript title page and SIAM publication page give Stewart and *SIAM
Journal on Computing*.

Bodirsky, Loho, and Skomra,
[*Reducing Stochastic Games to Semidefinite Programming*](https://drops.dagstuhl.de/storage/00lipics/lipics-vol334-icalp2025/LIPIcs.ICALP.2025.145/LIPIcs.ICALP.2025.145.pdf),
ICALP 2025, Figure 1 on page 145:3, also depicts SQRT-SUM to PosSLP with
a solid arrow; its caption defines solid arrows as polynomial-time many-one
reductions. Two agents independently inspected the figure visually. The
nearby paragraph cites Allender et al.; that citation alone would not
explain the strengthened reduction, but the PPS route above supplies a
concrete older source chain.

Accordingly, SQRT-SUM many-one reducibility must not be advertised as a
new consequence or as evidence that a current open problem has been solved.
It is also much weaker than eliminating all adaptive PosSLP queries.

## Recent use of the oracle formulation

The following primary texts were inspected for a later strengthening:

1. Bürgisser and Jindal,
   [*On the Hardness of PosSLP*, SODA 2024](https://goravjindal.github.io/assets/pdf/posslpsoda2024.pdf),
   Proposition 1.1 and the introductory numerical-computation discussion,
   retain the polynomial-time oracle characterization. Its individual
   many-one reductions do not state general adaptive closure.
2. Bläser, Dörfler, and Jindal,
   [*PosSLP and Sum of Squares*, FSTTCS 2024](https://drops.dagstuhl.de/storage/00lipics/lipics-vol323-fsttcs2024/LIPIcs.FSTTCS.2024.13/LIPIcs.FSTTCS.2024.13.pdf),
   Theorems 1.2 and 1.4, pages 13:2–13:3, distinguish the oracle
   characterization and Turing equivalence from particular many-one
   reductions. Its Figure 1 also distinguishes reduction types. It does not
   state adaptive sign-gate elimination in the inspected discussion.
3. Schaefer, Cardinal, and Miltzow,
   [*The Existential Theory of the Reals as a Complexity Class: A Compendium*,
   2024 version](https://arxiv.org/html/2407.18006v1), Section 1.2,
   explains the branch-by-branch oracle simulation and the resulting
   SQRT-SUM oracle algorithm. It does not assert a many-one closure theorem
   in that discussion.
4. Miltzow,
   [*Beyond Bits: An Introduction to Computation over the Reals*,
   arXiv:2603.29427v1](https://arxiv.org/html/2603.29427v1), Section 1.6,
   Theorem 2 and its proof, again use the oracle characterization and
   simulate comparisons by queries. The text is an introductory exposition,
   not a claim that stronger reductions remain open.

The continued use of Turing formulations is consistent with an unrecorded
strengthening, but it is not proof of one. Authors may state sufficient
weaker results, and equivalent statements may occur elsewhere.

## Assessment and remaining work

The defensible candidate contribution is the explicit uniform compiler
from finite integer arithmetic circuits with internal sign gates to one
ordinary PosSLP instance, together with a rigorous simulation showing
that it handles polynomial-time adaptive query descriptions. The closest
located model is Balaji's \(\mathrm{PosSLP}^{O}\). This audit found no
source contradicting the proposed theorem and no inspected source proving
its full statement. Neither finding certifies correctness or priority.

The original problem is still a mathematical reduction question, not a
claim that all real discontinuities can be removed. The integer separation
and circuit-size range bounds are essential. The transformation produces
compact representations of potentially enormous integers; it does not
make explicit evaluation efficient. Potential optimization uses require
separate algorithmic developments or a precise reduction target for which
many-one completeness matters.

Before any originality claim, inspect the full Balaji chapter and its
related publications, and trace sign-gate elimination under algebraic
decision-circuit terminology. The independent proof review remains
separate from this status audit. Novelty should remain qualified even if
all proof reviewers agree.

Searches combined `PosSLP` with `closed under`, `closure`, `adaptive`,
`one query`, `many-one`, `Turing`, `Karp`, `comparison gates`, `sign gates`,
`branching`, `absolute value`, `signum`, `rational approximation`, and
`rational functions`; related searches used `straight-line`, `elimination`,
`BSS`, and `circuit value`. Indexed snippets served to locate primary
sources. The Balaji access limitation is stated above rather than hidden.

Verification here consists of source reading, comparison of assumptions
and conclusions, and visual inspection of the 2025 reduction figure.
The targeted command
`git diff --no-index --check /dev/null research-20260928/algebra/posslp-prior-deep.md`
reported no whitespace diagnostics. No mathematical computation, Lean
verification, project-wide check, or CI inspection was used for this
literature audit.
