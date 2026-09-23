# Classical positioning of the structured bilevel results

Date: 2026-09-07. Status: bounded source audit and proposed paper language;
this is not a new mathematical result or proof of publication priority.
The audit read `literature/AGENTS.md` and did not change generated literature
files or paper packages. Local citations use extracted PDF-page markers.
The source-access record below distinguishes full text from abstracts.

## Main conclusion

The paper should lead with **a polynomial-size description of the global
follower reaction graph in fixed structural dimension**, despite a growing
number of follower variables and a possibly nonconvex aggregate cost.
Fixed leader dimension alone is insufficient. The shared-resource count,
aggregate dimension, and local block dimension supply the additional structure.

The appropriate classical comparison is with fixed **follower** dimension,
not fixed leader dimension. The positive linear-programming result predates
Deng (1998): Deng's own abstract credits Liu and Spencer (1995), and credits
Deng, Wang, and Wang (1995) for a simpler proof and an extension to independent
followers. The paper should cite that lineage rather than call Deng's result
a fixed-leader theorem. [Deng publisher abstract](https://doi.org/10.1007/978-1-4613-0307-7_6),
[Liu–Spencer publisher abstract](https://doi.org/10.1016/0377-2217(94)00005-W).

The contribution is a structural tractability result with a qualified
novelty assessment. It is not the invention of KKT elimination, clipping,
parametric response cells, exact real-algebraic optimization, or bounded
rational certificates. Those ingredients have established antecedents.

## Comparison with the closest complexity results

Here `r` is leader dimension, `N` is total follower dimension, `k` counts
shared resource rows, `s` counts aggregate coordinates, and `d` bounds local
block dimension. In the classical BLP/BQP sources, `m_f` is their follower
constraint count, with their separately stated nonnegativity convention.
Fixing `k` in a box/block model does not fix `m_f`: the number of local rows
and upper bounds grows with `N`.

| Result | Fixed quantities and growing dimensions | Follower structure | Semantics and output | Relation to this repository |
| --- | --- | --- | --- | --- |
| Liu–Spencer (1995), Deng (1998); modern proof in Ketkov–Prokopyev Theorem 1 | Fixed `N`; leader dimension and row counts may grow | Linear objective and polyhedral constraints | Optimistic exact polynomial solvability; rational LP-based output | Classical fixed-follower baseline. It does not allow an unbounded-dimensional nonconvex polynomial follower. |
| Ketkov–Prokopyev Theorem 1 | Fixed `m_f`; `N` and leader dimension may grow | Linear | Optimistic exact polynomial solvability | A different route to compression. Growing box bounds in the repository prevent identifying its fixed `k` with this fixed `m_f`. |
| Ketkov–Prokopyev Theorems 2–3 | Fixed `m_f` gives polynomial solvability; fixed `N` alone gives strong NP-hardness | Linear | Pessimistic objective and universal coupling-constraint feasibility | Tie handling and upper coupling constraints change the classification. Their hardness permits growing leader dimension. |
| Ketkov–Prokopyev Theorem 4 | Fixed `N`; leader dimension may grow | Convex quadratic follower; convex quadratic upper objective in their stated block-separable quadratic form | Optimistic polynomial solvability through convex QP subproblems | The repository fixes leader dimension but lets `N` grow and permits nonconvex aggregate follower cost and polynomial upper data. Neither result contains the other. |
| Ketkov–Prokopyev Theorems 5–6 | Pessimistic hardness with fixed `m_f`; optimistic hardness even with fixed `N,m_f` if follower quadratic is indefinite | Convex quadratic in Theorem 5; indefinite quadratic in Theorem 6 | Exact threshold NP-hardness, linear upper objectives | These results allow growing leader dimension. The repository does not resolve their open optimistic convex-QP case with fixed `m_f`. |
| Sugishita–Carvalho (2026), Theorem 1 | One leader variable; `N` and follower rows grow | Linear, coupled follower constraints, unit-bounded variables | Exact threshold NP-completeness; no extra upper constraints; reduction also has unique responses and gives pessimistic hardness | Shows that fixed leader dimension alone is inadequate. It does not establish hardness for a fixed-box well-conditioned SPD follower. |
| Repository exact quadratic-block compression | Fixed `r,s,k,d`; `N`, local row count, upper row count, and numerical polynomial degree may grow under the stated encoding | Positive-definite local quadratic blocks plus a possibly nonconvex polynomial of aggregate coordinates | Optimistic exact real-algebraic optimization; moving-normal extensions compute infimum and attainment separately and cover stated pessimistic semantics | Candidate main structural theorem. All competing stationary responses are compared globally in the compressed variables. |
| Repository polynomial-cost approximation | Fixed `r,s,k`; `N` and dense numerical degrees may grow | Strictly convex univariate polynomial locals, convex polynomial aggregate, fixed resource/aggregate matrices | Unique follower; global additive error `2^(-B)` in polynomial time in input bits and `B`; exactly feasible rational leader for the base model | An accuracy-bit theorem for the induced leader objective, not merely a high-precision follower solve. |
| Repository response-constraint extension | Same fixed dimensions; arbitrary explicitly encoded polynomial upper criteria | Same polynomial-cost follower | Bicriteria error without a margin; exactly upper-feasible rational approximation under an effective tightening modulus | Exact upper feasibility is conditional. It cannot be advertised as unrestricted exact feasibility or equality handling. |
| Repository near-optimal robustness | Fixed `r,s,k,d` and measurement count `h` per upper criterion; criterion count may grow | Same quadratic-block aggregate follower, possibly nonconvex | Exact robust feasibility, infimum, attainment, and algebraic witnesses against all cost-near-optimal followers | Extends an established robustness model by structured global complexity; does not assume near-optimal followers satisfy KKT conditions. |

Primary locators for the external rows: Ketkov–Prokopyev Table 1 and discussion,
[[ketkov2026-on-the-complexity-of-bilevel]] p.4; Table 2, p.5;
Assumption A1, p.7; Theorems 1–2, p.8, p.10; Theorem 3, p.15;
Theorems 4–6, p.18, p.21, p.23. Their standing A1 promises bounded nonempty
leader and follower feasible sets; verifying that promise is not included
in their algorithmic claims. Sugishita–Carvalho Theorem 1 and gap statement,
[[sugishita2026-complexity-of-bilevel-linear-programming]] p.3;
completion and pessimistic transfer, p.11. Their Theorem 2, p.13, concerns
polynomial-time *local* optimization; it should not be mistaken for global
tractability. Inspected versions:
[Ketkov–Prokopyev v2](https://arxiv.org/pdf/2511.15592v2) and
[Sugishita–Carvalho v2](https://arxiv.org/pdf/2510.21126v2).

Repository statements: [exact aggregate](../results/bilevel-fixed-aggregate-response-algorithm.md),
[quadratic blocks](../results/bilevel-fixed-block-response-algorithm.md),
[response semantics](../results/bilevel-compressed-response-infimum-semantics.md),
[convex polynomial aggregates](../results/bilevel-convex-aggregate-accuracy-bit-algorithm.md),
[upper response constraints](../results/bilevel-response-constraint-accuracy-bit-algorithm.md),
[near-optimal robustness](../results/bilevel-near-optimal-response-robustness.md).

## Proposed related-work prose

Bilevel optimization remains difficult even when both levels are linear.
Jeroslow (1985) established NP-hardness of value questions for two-level
linear games as part of a multilevel complexity analysis. Hansen, Jaumard,
and Savard (1992, Theorem 3.1 and Corollary 3.2) established strong hardness
for linear bilevel programming
and developed branch-and-bound rules. Vicente, Savard, and Júdice (1994)
studied descent methods with a strictly convex quadratic follower and
showed that recognizing local optimality can itself be NP-hard. These
results separate tractability of an individual follower problem from
tractability of the leader's induced optimization problem. General linear
bilevel models also have polynomial-size rational certificates:
Buchheim (2023, Theorems 1–2) proves NP membership under optimistic and
pessimistic semantics, and Theorem 4 gives polynomial-encoding-length valid
big-M values for the optimistic KKT reformulation. These results do not
provide a polynomial-time global optimizer. [Jeroslow abstract](https://doi.org/10.1007/BF01586088),
[Hansen–Jaumard–Savard inspected text, printed p.1197](https://www.researchgate.net/publication/233812576_New_Branch-and-Bound_Rules_for_Linear_Bilevel_Programming),
[Vicente–Savard–Júdice author-institution abstract](https://www.gerad.ca/en/papers/G-92-36),
[[buchheim2023-bilevel-linear-optimization-belongs-to]] p.3-7.

Classical polynomial algorithms instead restrict the follower dimension.
Liu and Spencer (1995) and Deng (1998) establish polynomial solvability for
linear bilevel optimization when the follower controls a fixed number of
variables. Ketkov and Prokopyev (2026) give a modern classification that
also separates fixed follower-variable and follower-constraint counts,
optimistic and pessimistic choices, and linear, convex quadratic, and
indefinite quadratic followers. In contrast, even a single leader variable
does not ensure global tractability: Sugishita and Carvalho (2026) prove
NP-completeness for a unit-bounded linear bilevel class with no additional
upper constraints. The parameterization here keeps the leader dimension
fixed while allowing arbitrarily many follower variables. Its additional
restrictions are fixed aggregate and shared-resource dimensions and
fixed-dimensional positive-definite quadratic local blocks. These
restrictions compress candidate responses into a fixed-dimensional
semialgebraic description, where global comparison removes nonglobal
stationary responses even when the aggregate cost is nonconvex.
[Liu–Spencer abstract](https://doi.org/10.1016/0377-2217(94)00005-W),
[Deng abstract](https://doi.org/10.1007/978-1-4613-0307-7_6),
[[ketkov2026-on-the-complexity-of-bilevel]] p.4-5, p.8, p.18,
[[sugishita2026-complexity-of-bilevel-linear-programming]] p.3, p.11.

The elimination ingredients have established precedents. Megiddo and
Tamir (1993) use low-dimensional multiplier cells for convex optimization
with local quadratic blocks and few shared constraints. Parametric QP
methods likewise exploit affine responses within active-set regions.
The contribution assessed here is the full global bilevel response
description and its bit-complexity consequences, rather than these local
formulas. For strictly convex polynomial local costs, the complementary
approximation results preserve a growing follower dimension and obtain
global leader-objective error `2^(-B)` with polynomial dependence on `B`.
They require explicit degree control and distinguish exact leader
feasibility from approximation of response-dependent upper constraints.
The earlier source audit compares the relevant approximation ingredients
with Hochbaum–Shanthikumar, Vigneron, and approximate multiparametric
optimization. [[megiddo1993-linear-time-algorithms-for-some]] p.6-10,
[existing source comparison](bilevel-resource-accuracy-bit-novelty.md),
[continuation source comparison](bilevel-reopened-literature-audit.md).

Uncertainty in a follower's decisions is a separate modeling choice.
Beck, Ljubić, and Schmidt (2023, Section 2.2) distinguish decision
uncertainty from uncertainty in model data. Besançon, Anjos, and Brotcorne
(2024) explicitly study robustness to cost-near-optimal lower-level
solutions. The present robust extension uses those established semantics
and compresses adversarial measurement fibers to obtain an exact
structural complexity result. It does not introduce the near-optimal
response model. For computational context, Kleinert, Labbé, Ljubić, and
Schmidt (2021) survey MIP reformulations, branch-and-bound, cuts, and
decomposition methods. Those methods are the appropriate practical
comparison class; polynomial solvability for fixed structural dimensions
does not imply a speed advantage over them.
[[beck2023-a-survey-on-bilevel-optimization]] p.8-10,
[[kleinert2021-a-survey-on-mixed-integer]] p.8-12, p.20-25,
[Besançon et al. open final paper, Section 2](https://publications.polymtl.ca/65063/1/2024_Besancon_Robust_Bilevel_Optimization_Near-optimal_Lower-level.pdf).

The first paragraph's historical references deliberately make only broad
claims supported by the source-access record. It must not acquire invented
theorem numbers or detailed restrictions attributed to an unread original.

## Corrections needed when stating the boundaries

### Fixed dimensions mean XP-type bounds, not a demonstrated FPT algorithm

The exact algorithms have input-length exponents depending on the structural
dimensions, for example `L^(f(r,s,k,d))`. Their decision versions therefore
have XP-type parameter dependence. Formal fixed-parameter tractability
requires a bound `f(r,s,k,d)*L^c` with an absolute exponent `c`; that is not
proved here. Use “polynomial time for fixed structural dimensions” in the
title, abstract, and theorem discussion. Avoid “fixed-parameter algorithm”
unless explicitly qualified as informal language.

Indeed, the [existing ReLU transfer](bilevel-diagonal-box-parameterized-hardness-source-audit.md)
already imports W[1]-hardness in growing leader dimension from the cited
Froese–Grillo–Hertrich–Stargalla construction, even with identity follower
Hessian and no shared resources. This is credited prior work, not a new
hardness result of this repository. It is a substantive reason not to
promise formal FPT dependence in the leader dimension.

### The accuracy-bit obstruction already follows from the existing gap

The [conditioned-box reduction](../results/bilevel-well-conditioned-box-exact-hardness.md)
has yes optimum at most `delta/8` and no optimum at least `15*delta/8`,
where `delta>0` has polynomial encoding length. Taking additive error
`delta/4` separates the two cases, while `log(1/delta)` is polynomial in
the SAT input size. Thus a global value approximation algorithm polynomial
in input length and accuracy bits would imply `P=NP`. Exponentially small
gaps suffice for this conclusion; strong NP-hardness is unnecessary.
The reduction's statement already includes this consequence.

Conversely, do not seek an inverse-polynomial **absolute** gap for that same
bounded-coefficient, bounded-conditioning scalar-leader class as if it were
an unconstrained improvement. Its upper coefficient one-norm `A` is at most
`2N`. The [additive algorithm](../results/bilevel-conditioned-box-additive-algorithm.md)
has running time polynomial in input length, `K<=N*kappa_2(Q)`, and `1/epsilon`
for error `epsilon*A`. An absolute gap at least `1/poly(L)` can therefore
be resolved in polynomial time by choosing `epsilon` below that gap divided
by a constant times `A`. Such gap hardness under all those same restrictions
would imply `P=NP`. This argument requires the polynomial numerical bound
on `A`; polynomial encoding length alone would not suffice. Strong
NP-hardness and normalized or absolute approximation gaps are distinct
notions and should not be interchanged.

Sugishita–Carvalho do supply a constant absolute `-1` versus `0` gap, but
their class has coupled linear follower constraints and their reduction
can use numerically exponential coefficients. Their gap cannot be imported
into the uniformly conditioned fixed-box class by simply citing it.
[[sugishita2026-complexity-of-bilevel-linear-programming]] p.3, p.6-11.

### Do not claim that every fixed parameter has a matching necessity theorem

The existing results exhibit several distinct obstructions: dense quadratic
coupling, growing leader dimension, weak path hardness, compressed binary
degrees, and growing measurement rank for near-optimal adversaries. These
do not automatically establish necessity of each parameter in every
positive theorem while all other assumptions are held fixed.

In particular, the robustness measurement-rank obstruction concerns
adversarial near-optimal responses; the exact optimistic quadratic theorem
allows arbitrary explicitly encoded polynomial upper criteria. The path
result is weak NP-completeness, and the exponential message example rules
out a small explicit piecewise-affine message representation for that
family, not every possible compressed algorithm. A sufficient-condition
theorem is not a complete complexity classification. A defensible sentence
is: “Complementary hardness and representation results identify several
limits of this structural approach.”

### Optimistic and pessimistic historical statements need explicit conventions

Ketkov–Prokopyev explicitly note that Deng's pessimistic statement lacks a
formal definition and that its interpretation with universal upper coupling
constraints is incompatible with their Theorem 3. Cite the classical
fixed-follower positive result in its optimistic form. Define separately
whether every follower optimum must satisfy the upper rows and whether
upper feasibility filters follower choices before the worst response is
taken. [[ketkov2026-on-the-complexity-of-bilevel]] p.4, p.7-8, p.15.

The paper's primary theorem should use the original fixed-normal optimistic
quadratic-block model. A table can then separate moving-normal infima,
pessimistic responses, and cost-near-optimal robustness. Exact algebraic
output and exactly feasible rational approximation are different guarantees.

## Source access and reading record

The following records what was actually inspected on 2026-09-07. “Full text”
means the relevant statement and surrounding argument were read; it does
not mean this audit re-proved every theorem in that source.

| Source | Access and precise locator used | Remaining limitation |
| --- | --- | --- |
| Deng (1998), *Complexity Issues in Bilevel Linear Programming*, pp.149–164 | Publisher abstract and bibliography at DOI `10.1007/978-1-4613-0307-7_6`; abstract explicitly identifies fixed follower variables and earlier Liu–Spencer and Deng–Wang–Wang work | Full chapter not retrieved. No internal theorem number claimed. |
| Liu–Spencer (1995), *Solving a bilevel linear program when the inner decision maker controls few variables*, EJOR 81:644–651 | Publisher abstract at DOI `10.1016/0377-2217(94)00005-W` states polynomial time for fixed inner dimension | Full article not retrieved. Modern proof is Ketkov–Prokopyev Theorem 1. |
| Jeroslow (1985), *The polynomial hierarchy and a simple model for competitive analysis*, Math. Programming 32:146–164 | Publisher abstract at DOI `10.1007/BF01586088` directly states NP-hardness of two-player value questions | Full article not retrieved. No approximation guarantee or detailed restriction is inferred from the abstract. |
| Hansen–Jaumard–Savard (1992), *New Branch-and-Bound Rules for Linear Bilevel Programming*, SIAM J. Sci. Stat. Comput. 13:1194–1217 | Public ResearchGate article-text extraction inspected: Section 3, printed p.1197, Theorem 3.1 (linear max-min strong NP-hardness) and Corollary 3.2 (general linear bilevel strong NP-hardness), including the KERNEL argument; GERAD report metadata cross-checked | Full PDF was not downloaded. Equation extraction is poor, so only the plainly legible theorem statement, corollary, and historical attribution are used, not a newly reconstructed reduction. |
| Vicente–Savard–Júdice (1994), *Descent approaches for quadratic bilevel programming*, JOTA 81:379–399 | Author-institution GERAD G-92-36 abstract explicitly identifies strictly convex quadratic follower methods and local-optimality hardness; author's publication list checked | Full article not retrieved. Abstract does not identify every restriction of its hardness reduction. |
| Buchheim (2023) | Local open arXiv v4 full text; Theorems 1–2, PDF pp.3–5; Theorem 4, pp.6–7 | NP membership and polynomial-bit big-M do not imply polynomial runtime or practical numerical bounds. |
| Kleinert–Labbé–Ljubić–Schmidt (2021) | Local open full text, Sections 2–4; PDF pp.8–12 and pp.20–25 | Survey, used for positioning and historical attribution rather than as a substitute for a new mathematical predecessor. |
| Beck–Ljubić–Schmidt (2023), *A survey on bilevel optimization under uncertainty* | Local open full text, Section 2.2, PDF pp.8–10, and robustness discussion | This is the uncertainty survey. It should not be confused with their later book on linear and mixed-integer bilevel optimization. |
| Ketkov–Prokopyev (2026), arXiv v2 | Local open full text; Tables 1–2 and Theorems 1–6 at locators above, with original PDF available | Classification is version-specific; assumptions and constraint-count conventions matter. |
| Sugishita–Carvalho (2026), arXiv v2 | Local open full text; Theorem 1 and reduction pp.3–11, Theorem 2 p.13 | First arXiv version was 2025; inspected revised package is 2026. No contradiction between these citation years. |

Searches included exact titles, author names plus `pdf`, DOI pages, GERAD
report pages, and Vicente's author publication list. Publisher paywall
previews were not treated as retrieved full articles. The public article-text
extraction provided the Hansen–Jaumard–Savard theorem after the initial
abstract search. Ketkov–Prokopyev Tables 1–2 and the pessimistic qualification
on printed pp.4–5 were additionally checked against images of the local
original PDF. No access controls
were bypassed. The missing historical originals limit fine-grained theorem
attribution, but not the main parameter comparison: it is directly proved
and tabulated in the inspected Ketkov–Prokopyev primary text and directly
described in Deng's and Liu–Spencer's own abstracts.

The [earlier continuation audit](bilevel-reopened-literature-audit.md) remains
the source for detailed comparisons with Megiddo–Tamir, the approximation
literature, near-optimal robustness, and safe screening. This note adds
classical positioning; it does not supersede that audit or assert that no
uninspected predecessor exists.
