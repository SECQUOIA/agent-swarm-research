# Independent review of the classical bilevel positioning

Date: 2026-09-07. Reviewer: `classical_review`, independently assigned after
the author drafted [the positioning note](bilevel-classical-positioning.md).
Scope: source attribution, parameter comparisons, semantics, and the two
accuracy-gap arguments. This review does not repeat the full proof audits
of the repository's underlying theorems.

**Verdict: passed within the stated source-access limits.** I found no
material error requiring a change to the positioning note. The proposed
related-work prose supports the intended structural contribution without
claiming that classical elimination ingredients are new. It also corrects
three misleading readings of the earlier critique: Deng's fixed dimension
is the follower dimension; polynomial-bit exponentially small gaps already
exclude accuracy-bit algorithms; and the existing bounds are polynomial
for fixed dimensions, rather than formal FPT bounds.

## Sources independently checked

I read `literature/AGENTS.md`. I inspected the local extracted statements
and surrounding discussion for Ketkov–Prokopyev, Buchheim, and
Sugishita–Carvalho. I independently extracted the decisive theorem and
table pages from their original PDFs with `pdftotext`, rather than relying
only on the author's account. The following locators agree with the
positioning note:

| Source | Decisive checked material |
| --- | --- |
| [[ketkov2026-on-the-complexity-of-bilevel]] | Tables 1–2, p.4-5; A1 and response conventions, p.7-8; Theorem 1, p.8; Theorem 2, p.10; Theorem 3 and its role, p.15-17; Theorems 4–6, p.18, p.21, p.23. |
| [[buchheim2023-bilevel-linear-optimization-belongs-to]] | Optimistic and pessimistic NP-membership statements and their certificate arguments, p.3-5; Theorem 4 and the distinction between polynomial encoding length and exponential numerical magnitude, p.6-7. |
| [[sugishita2026-complexity-of-bilevel-linear-programming]] | Single-leader theorem and `-1` versus `0` gap, p.3; uniqueness, exponential coefficients, pessimistic transfer, and representation lower bound, p.11; polynomial local optimization, p.13. |
| [[kleinert2021-a-survey-on-mixed-integer]] | Historical strong-hardness attribution and computational-method context, p.8-12. |
| [[beck2023-a-survey-on-bilevel-optimization]] | The distinction between model-data uncertainty and decision uncertainty, including imperfect follower optimization, p.2-3 and p.8-10. |

I also independently opened the primary
[Deng publisher abstract](https://link.springer.com/chapter/10.1007/978-1-4613-0307-7_6),
[Jeroslow publisher abstract](https://link.springer.com/article/10.1007/BF01586088),
[Hansen–Jaumard–Savard GERAD report page](https://www.gerad.ca/en/papers/G-89-09),
and [Vicente–Savard–Júdice GERAD report page](https://www.gerad.ca/en/papers/G-92-36).
Deng explicitly credits fixed follower-variable tractability to
Liu–Spencer and describes Deng–Wang–Wang's simpler proof and independent
followers extension. Jeroslow's abstract supports the broad two-player
value-hardness attribution. The Vicente report abstract supports the
descent-method and local-optimality-hardness descriptions.

The Liu–Spencer publisher page returned HTTP 403 in this independent
review. I did not retrieve the full historical articles or Deng chapter.
The Hansen report abstract supports its algorithmic contribution but does
not itself state strong NP-hardness; that historical attribution was
cross-checked in the inspected survey. These access limits match the
author's qualifications. No uninspected original theorem number or
fine-grained restriction is certified here.

## Parameter and semantics checks

Ketkov–Prokopyev Theorem 1 really covers either fixed follower-variable
count or fixed follower-row count, with a potentially growing leader
dimension. Their Theorem 4 assumes positive semidefinite follower and
upper quadratic matrices in the stated form. The repository's growing
follower dimension and nonconvex aggregate allowance are therefore a
substantive distinction; neither class contains the other.

The row-count caveat is necessary. Fixing the number of shared resource
rows in a model with growing local box or block constraints does not fix
the total follower constraint count in the classical formulation. A1 is
a promise of bounded, nonempty sets, and its verification is expressly
outside Ketkov–Prokopyev's computational problem. The note preserves both
qualifications.

The pessimistic interpretation in that source requires all optimal
follower responses to satisfy the upper coupling constraints. The stated
fixed-follower pessimistic hardness is consistent with optimistic
tractability because the universal feasibility condition is different.
The note correctly refrains from importing an unspecified historical
pessimistic convention. Its separation of exact algebraic output,
infimum/attainment, and conditional rational upper feasibility is also
consistent with the cited repository statements.

## Independent check of the precision arguments

Let `v` be the optimum in the conditioned-box reduction. Its promise is

```
YES: v <= delta/8,       NO: v >= 15*delta/8.
```

A two-sided additive estimate with error `delta/4` lies at most
`3*delta/8` in the yes case and at least `13*delta/8` in the no case.
Threshold `delta` separates them. A one-sided feasible-solution guarantee
also suffices if the response value can be evaluated, as it can in this
rational SPD quadratic setting. Since `delta` is positive rational with
polynomial encoding length, a dyadic tolerance below `delta/4` needs only
polynomially many accuracy bits. The exponentially small numerical gap
is no obstacle to this reduction.

For the opposite direction, the existing conditioned-box algorithm gives
error `epsilon*A`, where `A=||a||_1`. On the restricted hardness family,
`A<=2N` and `K<=N*kappa_2(Q)` is polynomially bounded. If a reduction within
all those same restrictions supplied a promised absolute gap
`g>=1/poly(L)`, choose `epsilon<=g/(4*A)` when `A>0`, capped at one if
necessary. Then `1/epsilon` is polynomial, and the additive algorithm
would resolve the gap in polynomial time. When `A=0`, the leader problem
is directly an LP. This validates the note's objection to seeking that
gap hardness without changing the subclass. Neither argument equates
strong NP-hardness with inverse-polynomial approximation-gap hardness.

## Limits of the verdict

The distinction between `L^(f(r,s,k,d))` and `f(r,s,k,d)*L^c` is correct.
The existing diagonal ReLU-transfer note supplies a concrete reason not
to promise formal FPT dependence on leader dimension; I checked that
transfer's stated identity-Hessian, no-shared-resource realization, but
did not independently re-prove the external network hardness theorem in
this bounded positioning review.

The warning against saying that every fixed parameter has a matching
necessity theorem is justified. The different hardness results concern
different models and semantics. A representation lower bound does not
exclude every implicit algorithm, and growing measurement-rank hardness
for near-optimal adversaries is not a restriction on arbitrary upper
polynomials in the exact optimistic theorem.

The note is suitable as a checked source for writing related work. It
does not establish publication priority or submission readiness by
itself. In the paper, retain the exact model restrictions next to the
main theorem and preserve the historical source-access qualifications
until original texts have actually been retrieved.

## Supplement: scalar convex-envelope antecedents

I independently checked the two principal attributions in
[the scalar source-positioning note](bilevel-nonconvex-source-positioning.md).
Both are supported. The
[Gardiner–Lucet publisher abstract](https://link.springer.com/article/10.1007/s11228-010-0157-5)
directly describes an easier quadratic-time algorithm and a more involved
linear-time algorithm for univariate piecewise linear-quadratic convex
envelopes. It also verifies the journal, year, and pages. This is a stronger
primary citation than the ResearchGate abstract link. Full original text
was not retrieved; no bit-complexity or detailed algorithmic claim is
certified from that abstract.

In [Moehle et al., arXiv v2](https://arxiv.org/pdf/2103.05455v2), Section 6.3
is on printed pp.13–14 and Appendix B on pp.21–24. The text gives recursive
convex-envelope construction, common supporting lines, and quadratic
equations for the interior contact cases. Section 6.3 explicitly credits
Gardiner–Lucet. Its recursion uses convex individual pieces; an
implementation applied to concave pieces must first account for that
condition. Thus this is an established construction antecedent, not a
ready-made exact bilevel or bit-complexity theorem. The note correctly
distinguishes the portfolio heuristic from its envelope subroutine.
[Boyd's publication page](https://stanford.edu/~boyd/papers/portf_constr_lcso.html)
confirms the final publication as Optimization and Engineering 24,
1667–1687 (2023).

This supplement audits attribution only. The contact-set identity and
solver correctness have separate mathematical reviews.
