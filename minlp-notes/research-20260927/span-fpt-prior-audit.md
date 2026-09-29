# Prior audit: FPT exact decision with a small Hessian matrix span

Date: 2026-09-28. Scope: exact feasibility over the reals for rational
continuous convex QCQP and rational SOCP, with running time
`g(h) N^C`, where `C` is absolute and `h` is the dimension of the span
of the native quadratic Hessian **matrices**. This audit found relevant
XP algorithms and an unrestricted SDP decision-hardness result, but no
inspected theorem that settles this FPT target. This is a limited source
comparison, not evidence of novelty or a claim that no such result exists.

The parameter must remain distinct from common range dimension, total
variable dimension, the number of quadratic constraints, and the span of
the complete quadratic polynomials. A single positive-definite matrix has
`h=1` and arbitrarily large common range. For SOCP, the squared native
polynomials can have indefinite Hessians even though the feasible region
is convex. An argument for globally convex quadratic polynomials cannot
silently be transferred to these squared SOC rows.

The strongest inspected comparisons are as follows.

| Primary source | Precise relevant result | Consequence for the FPT question |
| --- | --- | --- |
| Grigoriev–Pasechnik, [*Polynomial-time computing over quadratic maps I*](https://logic.pdmi.ras.ru/~grigorev/pub/quadric_cc.pdf), Theorem 1.2 and Corollary 1.6 | For a quadratic map with `k` components and an outer polynomial of degree `d`, exact sampling and emptiness testing use `(dn)^{O(k)}` operations; intermediate coefficient bitsizes have the corresponding bound. | This is XP in `k`, not `g(k) poly(N)`. The component count is not native Hessian span. Arbitrarily many affine rows cannot simply be added without changing the representation or supplying a separate convexity argument. |
| Porkolab–Khachiyan, [*On the Complexity of Semidefinite Programs*, DIMACS TR 96-18](https://dimacs.rutgers.edu/archive/TechnicalReports/abstracts/1996/96-18.html) | The primary report abstract states exact feasibility of `m` linear inequalities over PSD matrices of order `n` in `m n^{O(min(m,n^2))}` arithmetic operations over `l n^{O(min(m,n^2))}`-bit numbers. | A strong exact fixed-parameter-value precedent, but XP in the small constraint parameter. The parameter is not QCQP Hessian span. Only the primary abstract, not the complete report, was retrieved in this audit. |
| Henrion–Naldi–Safey El Din, [*Exact algorithms for linear matrix inequalities*](https://arxiv.org/abs/1508.03715), Theorem 3 and Section 1.3 in the [author manuscript](https://homepages.laas.fr/henrion/Papers/exactlmi.pdf) | Exact algebraic sampling/emptiness under stated genericity assumptions for an `m`-order pencil in `n` variables. Complexity is polynomial when either `m` or `n` is fixed; the displayed bounds depend on multilinear Bézout quantities. | The statements do not provide an input exponent independent of the pencil-variable parameter, and do not cover arbitrary degeneracies. Reducing a KKT system to an `O(h)`-variable determinant pencil still leaves degree growing with the matrix order; this route alone does not prove FPT. |
| Henrion–Naldi–Safey El Din, [*Exact algorithms for semidefinite programs with degenerate feasible set*](https://arxiv.org/pdf/1802.02834), Theorems 11–12 and the discussion after Theorem 12 in version 2 (2020) | Removes genericity assumptions on the feasible spectrahedron, retains a generic linear objective, and returns exact algebraic output. The authors prove polynomial arithmetic complexity when either the pencil-variable count or matrix order is fixed. | This follow-up closes the feasible-set degeneracy limitation of the preceding comparison. Its bounds remain XP in the small dimension and do not provide FPT bit complexity in native Hessian span. |
| Del Pia, [*Convex quadratic sets and the complexity of mixed integer convex quadratic programming*](https://arxiv.org/pdf/2311.00099v2), Proposition 4 | Exact feasibility of a rational polyhedron plus one convex quadratic inequality is FPT in the number of integer variables, with unbounded continuous dimension and quadratic rank. | Its continuous specialization is a genuine exact polynomial-time positive result. It does not address arbitrarily many nonproportional quadratic rows. The local source and detailed comparison are in [the common-range prior audit](common-range-fpt-prior.md). |

These comparisons explain the existing XP theory without settling whether
a different decision algorithm can avoid its algebraic expansion. For
example, expanding a degree-`n` determinant in `h` parameters can create
`binomial(n+h,h)` monomials. That is an obstruction to this representation
and enumeration strategy, not a lower bound on deciding feasibility from
the original matrix data. Likewise, a degree `n^{Omega(h)}` lower bound
for an optimum or a recovered coordinate rules out certain uniformly
small dense algebraic outputs; it does not rule out `g(h) N^C` yes/no
algorithms. Even the GP paper's exponentially many-component examples
concern a sampling task whose output includes every component.

There is a genuine nearby **decision** reduction, but its parameter and
target class must be retained. Tarasov–Vyalyi,
[*Semidefinite programming and arithmetic circuit evaluation*](https://arxiv.org/pdf/cs/0512035),
Theorems 3–4 and Section 2, reduce arithmetic-circuit comparison to exact
rational SDP feasibility in deterministic polynomial time. Strict PosSLP
reduces to their non-strict comparison because the circuit output is an
integer. Their first construction uses one variable per gate, addition
epigraphs, and `x_i >= x_j^2/2`; a second step uses Ramana's extended
semidefinite dual to compare two circuit outputs. The displayed final
reduction is to SDP. It does not itself establish the same hardness for
globally convex QCQP or for SOCP. Distinct squared registers in the first
construction have independent coordinate Hessians; a squaring chain has
span growing with its length. Consequently, this reduction supplies no
FPT lower bound in `h`. Establishing an SOCP specialization would require
a separate argument, and still would not control this parameter.

Square-Root Sum is an even clearer warning against interpreting ordinary
exact hardness as parameterized hardness. The familiar convex system

```text
0 <= x_i,   x_i^2 <= a_i,   sum_i x_i >= b
```

has `h=k` for `k` independent coordinate squares. The classical separation
bound quoted by Eisenbrand–Haeberle–Singer,
[*An Improved Bound on Sums of Square Roots via the Subspace Theorem*](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2024.54),
already gives a direct `2^{O(k)} poly(N)` decision algorithm: approximate
the radicals to `O(2^k poly(N))` bits, and compare against a nonzero-gap
threshold, treating the interval below that threshold as equality.
Here this algorithmic consequence is our elementary inference from the
stated effective classical bound, not the paper's ineffective improved
bound. Thus the reduction does not resist FPT in `h`. Unrestricted
polynomial-time solvability of Square-Root Sum remains a different issue.

The small-common-range result in this repository also remains a useful
positive comparison, but it is narrower: after a rational change of
coordinates its nonlinear part has dimension `r`, and fixed-degree
quantitative semialgebraic bounds can have a factor depending only on `r`.
Small matrix span does not give this coordinate reduction. Conversely,
hardness for nonconvex polynomial feasibility, convex **maximization**,
integer selection, or enumerating algebraic witnesses does not settle the
continuous convex decision question. Searches using those neighboring
terms produced apparent matches, but none inspected supplied an applicable
parameter-preserving reduction.

The defensible current conclusion is therefore an unresolved comparison:
the inspected few-quadratic and determinant-pencil algorithms give XP
precedents; the inspected decision-hardness reductions do not exclude FPT
in native Hessian span; and the known or locally developed positive
results control different parameters or narrower constraint families.
A valid negative result needs a reduction that keeps `h` bounded by a
function of the source parameter. A positive result needs a uniform input
exponent for the exact **decision** task, not merely polynomial time for
each fixed `h`.

Targeted verification: read the existing Hessian-span and common-range
audits and the few-quadratic supporting lemma; inspected GP's original
Theorem 1.2/Corollary 1.6, the exact-LMI primary statement and displayed
complexity, the degenerate-SDP follow-up's Theorems 11–12 and following
complexity discussion, the DIMACS primary abstract, and Tarasov–Vyalyi Section 2
using `pdftotext -layout` output. The latter matters because the web PDF
text misreads the non-strict inequality glyph as strict. Searches covered
fixed-parameter convex quadratic/semialgebraic feasibility, few quadratic
constraints, exact LMI feasibility, determinant pencils, and PosSLP.
Downloaded the exact-LMI author PDF with `urllib.request.urlretrieve`,
ran `pdftotext -layout`, and used `rg` and `sed` to inspect Theorem 3 and
Section 1.3. An inline `python3` check of this note's final newline,
trailing whitespace, control characters, and local Markdown links passed.
No project-wide verification or CI inspection was performed. These checks
verify the cited comparisons, not publication priority or the unproved
FPT claim.
