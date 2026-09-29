# Prior-work and significance audit: ordinary sparse Putinar rounding

Date: 2026-09-28. Independent literature and significance review of
[sparse-putinar-kernel.md](sparse-putinar-kernel.md). This is not a replacement
for its separate proof reviews.

The ordinary-module result remains a plausible contribution: the inspected
sources do not establish its unconditional sparse box rate. Its ingredients
are substantially prior, including the dense `O(log^3(R)/R^2)` theorem.
The contribution to compare is the finite-order transfer to overlapping
bags using nearly normalized SOS kernels and quantitative separator repair.
No priority claim follows from this search.

The subsequently reviewed [exact-consistency strengthening](sparse-putinar-exact-consistency.md)
uses a common correction of signed densities instead of separator repair.
It proves the same rate per total local coefficient norm with no extra
bag-count or tree-topology factor. The [fresh final audit](signed-kernel-final-audit.md)
independently checks that argument and its source comparisons. References
below to a tree-size term concern the original approximate-consistency
theorem only; they do not apply to this stronger statement.

There is a material correction to the related preordering project. Magron's
July 2025 and February 2026 slides already publicly assert its `O(R^-2)`
sparse preordering rate. The earlier statement that no inspected source
asserted that rate is withdrawn. The slide and published-paper statements
differ; that discrepancy must remain explicit.

## Exact hierarchy being compared

The candidate minimizes `sum_b f_b(x_Bb)` over the continuous box, with a
running-intersection bag tree. At moment order `R`, each bag functional is
positive on

\[
 q^2\quad(\deg q\le R),\qquad
 (1-x_i^2)q^2\quad(\deg q\le R-1),
\]

and adjacent separator moments agree through total degree `2R`. The dual
uses only one SOS multiplier and one multiplier per coordinate in each
bag. There are no products of distinct box generators, added ball
constraints, representing-measure assumptions, or assumptions of attained
polynomial separator potentials.

The finite statement uses `R>=wD`, with
`D=2(s-1)(N+1)` and even `N`. Kernel densities use degree at most `R`,
leaving room to prove coefficient evaluations bounded through moment PSD.
Choosing `N=O(log s)` gives the stated rate for fixed objective and tree.
Constants include the local Chebyshev coefficient budget, objective degree,
width, and a tree-size contribution to separator repair. This is not a
uniform dimension-free guarantee for unnormalized growing objectives.

## A verified prior assertion that changes the preordering assessment

Victor Magron's **“Sparse polynomial optimization: Applications & solution
methods,” Lorentz Center, 7 July 2025**, logical slide 23/44, physical PDF
page 90, explicitly defines

\[
 Q_d(I)=\left\{\sum_{J\subseteq I}\sigma_J
              \prod_{j\in J}(1-x_j^2):\deg(\sigma_Jg_J)\le2d\right\},
\]

and `f_cs^d=sup{lambda:f1+f2-lambda in Q_d(I1)+Q_d(I2)}`. The displayed
theorem asserts `f_min-f_cs^d=O(1/d^2)` and attributes it to Korda,
Ríos-Zertuche, and Magron (2024). The slide and immediate neighbors give
no disjointness condition. The assertion was independently rendered and
visually inspected, so no exponent was lost during text extraction.
[Primary 2025 slides](https://homepages.laas.fr/vmagron/slides/lorentz25.pdf).

The same statement appears in **“(Non)linear moment problems: theory and
practice,” TENORS Learning Week 2, The Arctic University of Norway,
16 February 2026**, logical slide 35/90, physical PDF page 121. This
rendering was separately inspected. The line mentioning a sparse Putinar
rate gives no exponent. These slides therefore directly affect preordering
priority; they do not state the ordinary-module rate of the present draft.
[Primary 2026 slides](https://homepages.laas.fr/vmagron/nlmoment.pdf).

Both slides cite the published work discussed next, whose explicit theorem
gives a different exponent. No stronger proof or additional assumption was
located in the inspected slides. It would be unjustified to dismiss their
claim as a typo, or to supply an unstated assumption. An earlier public
assertion and an earlier verified proof are different evidence; both facts
must be recorded. The explicit rounding proof and constants may still add
something, but the preordering rate itself cannot be described as newly
asserted here.

## Strongest directly relevant theorem comparisons

**Korda, Magron, Ríos-Zertuche, “Convergence rates for sums-of-squares
hierarchies with correlative sparsity,” Mathematical Programming 209
(2025), 435–473; online 25 March 2024.** The published Theorem 6 gives
the sparse box-preordering rate `O(R^(-2/(w+3)))`. Theorem 8 treats sparse
ordinary modules on general domains, assuming running intersection,
normalized local Archimedean certificates, and local Łojasiewicz bounds.
For local exponent `L=1`, its explicit equations (5)–(6) have dominant
degree requirement

\[
 R^2\ge C\varepsilon^{-(238+55w)/9},
\]

giving `O(R^(-18/(238+55w)))` for fixed data. This uses the displayed
theorem, rather than the slightly different simplified exponents in its
introduction or the older arXiv discussion. It uses coordinatewise degree;
converting to total degree costs width factors, not a new exponent.
The proof approximates separator value functions before constructing local
positive polynomials. The candidate avoids that intermediate approximation.
[Published primary article, Theorems 6 and 8](https://link.springer.com/article/10.1007/s10107-024-02071-6).

The general-domain normalization can be met for this box without changing
its ordinary generator cone. Here is the direct check: set `y=x/sqrt(w)`
and `g_i(y)=(1/w-y_i^2)/2`. On the ambient unit cube, `||g_i||_infty<=1/2`,
and on every bag of size `v<=w`,

\[
 1-\sum_{i\in B}y_i^2=1-v/w+2\sum_{i\in B}g_i(y).
\]

The scaled box has a linear distance bound in the largest constraint
violation, since `|y|-1/sqrt(w)` is bounded by a constant times
`y^2-1/w` outside the interval. This validates using `L=1`; constants
change under the scaling. It does not transfer the old general-domain
rate to hard constraints in the new candidate.

**Gribling, de Klerk, Vera, “Squared polynomial approximation kernels for
the hypercube,” arXiv:2605.31496v1, 29 May 2026.** Sections 3.1–3.5 supply
the squared Fejér kernel, reciprocal normalization by a finite geometric
series, and tensor approximation. Theorem 7 establishes the dense ordinary
box-module rate `O(log^3(r)/r^2)`. Its `Q(g)_r` truncates certificate
degree at `r`; the bound concerns `f_(2r)`. Thus the candidate's moment
order `R` corresponds to that total-degree cutoff `2R`, up to fixed
construction constants. The dense theorem is not new here. The potentially
new step is ordinary-module control of separator mismatch after local
normalization, followed by tree repair. The draft correctly rederives
degrees and enforces even normalization length: the source's Proposition
9 does not explicitly enforce evenness and its SOS wording for signed
`T_k` cannot be imported literally. Positivity holds for nonnegative
inputs, not arbitrary signed basis elements.
[Primary preprint](https://arxiv.org/html/2605.31496v1).

**Baldi and Slot, “Degree bounds for Putinar's Positivstellensatz on the
hypercube,” SIAM Journal on Applied Algebra and Geometry 8 (2024), 1–25.**
Theorem 11 controls degree for the ordinary dense box module; applying it
to `f-f_min+epsilon` gives the earlier `O(R^-1)` hierarchy rate. It does
not address overlapping bags. This remains historical context, not the
strongest dense comparison after May 2026.
[Primary revised preprint](https://arxiv.org/html/2302.12558v3).

**Gamertsfelder and Mourrain, “The Effective Countable Generalized Moment
Problem,” arXiv:2501.09385v4.** This is the closest general framework:
vectors of measures and countably many polynomial equalities include
separator moment agreement. Equation (3) uses finitely supported dual
multipliers. Assumption 9 requires an attained optimizer in that space;
Theorem 13 and Corollary 14 transfer effective positivity rates with
constants depending on it. Theorem 12 distinguishes ordinary box modules
(`theta=1` in its cited bound) from the full box preordering (`theta=2`).
With an attained polynomial separator dual, the newer dense kernel bound
can similarly transfer conditionally. The candidate's main distinction is
that it does not require this attainment. Strict feasibility of each
finite SDP, which the draft uses for finite dual attainment, is a different
claim and does not imply attainment of this countable moment dual.
[Primary text](https://arxiv.org/html/2501.09385v4).

**Nie, Qu, Tang, Zhang, “A characterization for tightness of the sparse
Moment-SOS hierarchy,” Mathematical Programming 215 (2026), 369–405;
online 2 May 2025.** This work characterizes finite tightness rather than
an unconditional numerical rate. Example 6.7 already supplies the rational
separator obstruction used in the repository's
[nonattainment example](prior-independent.md). Thus polynomial-dual
nonattainment is a real boundary, and its example mechanism is prior.
The new rate must not be advertised as proving finite convergence.
[Primary article](https://link.springer.com/article/10.1007/s10107-025-02223-2).

**Tran and Toh, “On the convergence rates of moment-SOS hierarchies
approximation of truncated moment sequences,” arXiv:2507.00572v1;
published July 2026.** An independent child reviewer read the primary PDF.
Theorem 3.5 gives second-order fixed-degree moment approximation on
products of unit balls and simplexes, including intervals, with a redundant
ball inequality. Its cone is `T(X)`, the full preordering. Even its reduced
cone `R(X)` retains all generator subset products; Table 1 does not give
the product theorem for ordinary `Q(X)`. For fixed even truncation `k`,
the threshold is `r>=2m(max_i n_i+1)k+m`. It concerns one dense truncated
moment vector. Independently applying it to bags does not ensure equal
separator laws or small separator TV: finite-moment agreement permits a
continuous law and matching atomic quadrature to be mutually singular.
[Primary preprint](https://arxiv.org/pdf/2507.00572),
[published abstract](https://link.springer.com/article/10.1007/s10107-026-02394-6).

**Schlosser, Tacchi-Bénard, Lazarev, “Convergence rates for the moment-SoS
hierarchy,” Numerical Algebra, Control and Optimization 16 (2026),
105–156.** Its primary text develops functional-LP convergence using
effective positivity, polynomial approximation, and an inward-pointing
condition equivalent to Slater. Sections 2–3 supply a broad transfer
framework; the inspected text does not provide the candidate's separator
TV estimate or its box-specific exponent. A claim of reduction to this
framework would need quantitative approximation of the separator
functions, including their regularity and norm bounds; the existence of a
general LP formulation alone does not supply that result.
[Primary text](https://arxiv.org/html/2402.00436),
[published article](https://www.aimsciences.org/article/doi/10.3934/naco.2025011).

**Magron, “Convergence Rates for Polynomial Optimization on Set
Products,” SIAM Journal on Optimization (2026), arXiv:2505.18580.** Theorem
11 and Corollary 12 give `O(R^-2)` for dense full preorderings on products
of spheres, balls, simplexes, and cubes. Equality-only sphere products are
a case where preordering and module coincide; that does not make the
same assertion valid for a product of intervals. The quantum generalized
moment result, Theorem 14, assumes bounded dual attainment. This establishes
kernel tensorization and product-domain rates, without the new draft's
overlap compatibility statement.
[Primary preprint](https://arxiv.org/abs/2505.18580),
[local primary text](../../literature/papers/magron2026-convergence-rates-for-polynomial-optimization/fulltext.md).

**Lasserre, “Convergent SDP-relaxations in polynomial optimization with
sparsity,” SIAM Journal on Optimization 17 (2006), 822–843.** Consistent
local measures already glue under running intersection; Appendix 6.2–6.3,
including Lemma 6.4, is directly relevant. The new question is finite-order
rounding of functionals which need not have representing measures. Neither
tree gluing nor qualitative sparse convergence is a new contribution.
[Primary DOI](https://doi.org/10.1137/05064504X),
[local primary text](../../literature/papers/lasserre2006-convergent-sdprelaxations-in-polynomial-optimization/fulltext.md).

A related gluing search also examined Tran–Nguyen–Soh, arXiv:2502.09102v3,
Lemma 5.2. The child reviewer found gluing of transport-plan variables
with fixed finite-distribution marginals and preordering constraints,
rather than completion of arbitrary overlapping coordinate
pseudo-moments. It is not an immediate equivalent theorem.
[Primary text](https://arxiv.org/html/2502.09102v3).

## Significance and practical limits

The candidate addresses an established sparse SDP cone with `v+1` PSD
blocks for a bag of size `v`. The full local preordering can require
`2^v` block types, although their sizes differ and high-degree products
are absent at low orders. Nearly retaining the dense exponent with fewer
generator products is a useful structural guarantee. The proof's
separation of smoothing error and exponentially smaller normalization
error also appears reusable.

That comparison does not imply a new fastest box-optimization algorithm.
Bos, De Marchi, Sommariva, and Vianello's Chebyshev-grid analysis already
gives second-order objective approximation: Proposition 2 uses
`md+1` nodes per coordinate for degree `d`, with error bounded by
`(sec(pi/(2m))-1)(f_max-f_min)`. On a bag tree, a common finite grid permits
ordinary finite-state dynamic programming. The earlier repository audit
read its primary manuscript; this pass's fresh retrieval timed out.
[Primary manuscript](https://www.math.unipd.it/~marcov/pdf/opticheb.pdf),
[DOI](https://doi.org/10.1007/s11590-017-1166-1).

Bienstock and Muñoz already obtain polynomial-size LP approximations for
bounded-treewidth mixed-integer polynomial problems, with scaled objective
and constraint tolerances. These handle a broader optimization setting
than an unconstrained continuous box, although they give a different
certificate and feasibility guarantee.
[Primary preprint](https://arxiv.org/abs/1501.00288),
[local primary text](../../literature/papers/bienstock2018-lp-formulations-for-polynomial-optimization/fulltext.md).

For the present theorem, reduced certificate degree and block count are
proved mathematical consequences once its proof is accepted. A useful
runtime reduction remains plausible, not established: it needs constants,
conditioning, extraction or sampling, and a comparison with grid dynamic
programming at matching accuracy. Exact rational certificate size and
bit complexity are unchecked. Additional hard constraints and integer
support are not preserved by this smoothing and repair construction.

The significance assessment is consequently specific: a potentially strong
convergence theorem for the ordinary sparse box hierarchy, built from a
recent dense result, rather than a demonstrated general MINLP solver
advance. General constrained support preservation, useful instance-wise
constants, or a new sharp obstruction would substantially strengthen it.
The slide discovery lowers the separate preordering rate's priority claim;
it does not by itself settle the ordinary-module transfer's priority.

## Search coverage, evidence, and checks

Searches on 2026-09-28 included sparse Putinar and quadratic-module rates,
correlative sparsity in 2025–2026, squared-kernel citations, product-domain
moment approximation, countable generalized moment problems, gluing, and
author lecture/publication pages. Primary papers were used for theorem
comparisons; search snippets and indexing pages only supplied leads.
One child reviewer independently scanned recent work and inspected the
2025 rendered slide, Tran–Toh, and transport gluing. This is bounded search
coverage, not a complete citation census.

Primary slide evidence retained in this repository:

| Source | Retained PDF | Rendered page | PDF SHA-256 |
|---|---|---|---|
| 7 July 2025, slide 23/44 | [PDF](prior-sources/magron-lorentz-2025-07-07.pdf) | [page 90](prior-sources/magron-lorentz-slide23-page90.png) | `2a5fd032a841c90bc0dbc079b47b35c2619c236b595fdfa50d02ce4d59f2ba58` |
| 16 February 2026, slide 35/90 | [PDF](prior-sources/magron-nlmoment-2026-02-16.pdf) | [page 121](prior-sources/magron-nlmoment-slide35-page121.png) | `320afc9dad8a7d094a4b8a75b0e783affd57dffbcd5ff5bf7c54b019e72aa3b9` |

Targeted evidence commands actually run included:

```text
pdfinfo /tmp/putinar-prior/nlmoment.pdf
pdfinfo /tmp/putinar-prior/lorentz25.pdf
pdftotext -layout -f 119 -l 121 /tmp/putinar-prior/nlmoment.pdf -
pdftotext -layout -f 112 -l 118 /tmp/putinar-prior/nlmoment.pdf -
pdftoppm -f 121 -l 121 -scale-to 1800 -png -singlefile /tmp/putinar-prior/nlmoment.pdf /tmp/putinar-prior/nlmoment-page121
sha256sum /tmp/putinar-prior/nlmoment.pdf /tmp/putinar-prior/nlmoment-page121.png
sha256sum /tmp/putinar-prior/lorentz25.pdf /tmp/lorentz25-sparse-rate.png
```

The temporary PDFs were copied without alteration to the retained paths
above. Both images were visually inspected; the child independently
rendered page 90. These checks establish what the downloaded primary
slides display and preserve exact source identity. They do not verify the
slide theorem or resolve its discrepancy with the published paper. No
project-wide checks or CI status inspection were run for this audit.
