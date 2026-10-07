# Prior-work review: constructive separator certificates

This report compares the paper's claims with primary sources and records a
bounded, claim-driven review completed on 2026-10-06. Four focused discovery
rounds covered separator consistency and cost shifting; adaptive regridding;
finite-domain AND/OR methods and spatial branch-and-bound; and inexact dynamic
programming, contracting dynamics, and adjoints. The review closed at
operational saturation in its narrow fourth-round citation-chain check. It is
not an exhaustive bibliography or publication-priority clearance.

## Consistency, cost shifting, and tree gluing

Several central ingredients are established. Wainwright, Jaakkola, and
Willsky formulate finite-state MAP inference using local marginal agreement
and reparameterization, and prove exactness on trees. Wald and Globerson
develop local-consistency relaxations for continuous pairwise MRFs: their weak
relaxation imposes agreement on selected test-function expectations, and the
dual uses cost shifts and sums of local minima. Their exactness result is for
the stated convex-decomposable pairwise class, not arbitrary continuous
tree-decomposed objectives. Sion's minimax theorem supplies the general
minimax step under its compactness and semicontinuity hypotheses. Lasserre's
sparse-moment result supplies a readable measure-gluing precedent; the paper's
tree-gluing argument is given directly. Vorob'ev is relevant historical
measure-extension work, but its full text was not retrieved. The paper should
not claim generic minimax duality, cost shifting, local consistency, or tree
gluing as new.

Primary locators: Wainwright et al. (2005), Theorem 1 and Corollary 1,
§§IV–V; Wald–Globerson (2014), Eqs. (6), (8), Lemmas 3.1–3.2, pp. 2–3, and
Theorem 4.1, p. 4; Sion (1958), Corollary 3.3 and Theorem 3.4, p. 174;
Lasserre (2006), Theorem 3.6 and its measure-gluing proof, pp. 6–10 and
13–16. Readable records: [[wainwright2005-map-estimation-via-agreement-on]]
p.5; [[wald2014-tightness-results-for-local-consistency]] p.3-4;
[[sion1958-on-general-minimax-theorems]] p.5;
[[lasserre2006-convergent-sdprelaxations-in-polynomial-optimization]] p.13-16.

## Separator-band identity and approximation

Factor-two approximation mechanisms and separator cost shifts also have
direct precedents. De Farias and Van Roy's approximate linear program bounds
value error by twice the best approximation error, scaled by the discount
factor when constants belong to the basis. Grimm, Netzer, and Schweighofer
prove positive-margin local splitting under running intersection by shifting
a separator-fiber minimum into the band. Korda, Magron, and Ríos-Zertuche give
a quantitative polynomial approximation version. Han, Jiao, and Weissman's
moment-matching identity is a zero-width, single-function analogue. Nie et
al. characterize tightness of a sparse moment-SOS hierarchy using local
polynomial shifts. These sources rule out novelty claims for cost shifting,
qualitative split existence, the general factor-two approximation mechanism,
and the zero-width case.

Ginchev and Hoffmann (2002) study Chebyshev approximation of set-valued maps
using Hausdorff excess and oriented distance. Their Proposition 2.2 gives
opposite shifts of these objectives under ball expansion (printed p. 37), and
their printed p. 35 identifies the scalar-valued case as earlier work from
1997. The 1997 publisher abstract confirms the scalar interval-valued
Chebyshev objective, but its chapter text remains inaccessible. This is close
prior art for the positive-width band objective. Neither inspected source
states the paper's restricted-DP gap identity, its clipping derivation, or the
tree extension.

The candidate contribution is narrowly the exact identity relating the
optimized one-separator DP gap to twice the (L_\infty) distance from the
permitted shift class to the separator band, together with the stated tree
lower bound by the largest edge distance and a jointly realizable split upper
bound. The independently optimized edge distances need not share one jointly
realizable separator shift. This is a specific theorem comparison, not a
claim that band approximation or the factor-two principle is new. The 2002
source is the primary comparison; the 1997 chapter is recorded as an
unretrieved historical predecessor and is not used for theorem-level claims.

Primary locators: de Farias–Van Roy (2003), Theorem 4.1, §4.1; Grimm et al.
(2007), Lemma 3, pp. 2–3; Han et al. (2018), Lemma 25 and Eq. (24); Korda et
al. (2025), Lemma 15 in the published version (Lemma 11 in arXiv v1), §3;
Nie et al. (2026), Theorems 3.1–3.2, arXiv v3, pp. 7–8; Ginchev–Hoffmann
(2002), Eqs. (1)–(2), printed pp. 34–35, and Proposition 2.2, printed p. 37;
Ginchev–Hoffmann (1997), publisher abstract only. Readable records:
[[farias2003-the-linear-programming-approach-to]] p.19;
[[ginchev2002-approximation-of-set-valued-functions]] p.5.

## Adaptive regridding under quadratic growth

Adaptive refinement and dynamic programming over discretized states are
established. Munos and Moore adaptively split state-space cells and rebuild a
discretized dynamic program. Zhang and Sun bound deterministic SDDP iteration
counts by a power of inverse accuracy under their covering and oracle
assumptions. Bienstock and Muñoz give compact bounded-treewidth LP
formulations with explicit polynomial dependence on inverse accuracy.
Nagarajan et al. combine piecewise relaxations, optimization-based bound
tightening, and selective spatial refinement. MUSE-BB combines decomposed
scenario subproblems in a single spatial branch-and-bound tree.

Munos (2011) proves logarithmic-accuracy bounds for DOO/SOO under its matched
near-optimality and growth assumptions; those bounds concern simple regret and
evaluations of the global objective, not a local certificate-solve count.
Bachoc et al. (2021) give instance-dependent Lipschitz value certificates
from value-oracle samples. Their theorem yields an \(\epsilon^{-d/2}\)-type
rate under a quadratic growth condition and fixed dimension; this exponent is
an inference from their covering formula. Local cluster results of Du and
Kearfott, Wechsung et al., and Kannan and Barton bound terminal or
near-optimal cluster counts under their own assumptions, not the full
separator-certificate construction or tree work considered here.

Among the results reviewed here, none gives the paper's combination of
quadratic growth, fresh regridding on an arbitrary supplied tree, aggregate
copy-drift accounting, and logarithmically many accuracy stages. The
candidate advance is that aggregate construction and its stated bound under
the paper's oracle, curvature, growth, width-error, and tree assumptions. It
is not adaptive grids or finite-tree dynamic programming in general. State
that cell counts can remain exponential in bag width, and do not infer
polynomial bit complexity from the exact-real oracle theorem. The separate
rational polynomial realization has fixed-degree and fixed-parameter
conditions and numerical-conditioning dependence; it is not uniformly
polynomial in the curvature-to-growth ratio.

Primary locators: Munos–Moore (2002), §§3 and 5; Munos (2011), Theorem 1,
Corollary 1, and Example 2, §§3 and 4.3; Bachoc et al. (2021), Theorems 1
and 3, pp. 6–9; Zhang–Sun (2022), §§4.1–4.2, Theorem 2 and Corollaries 1–2,
pp. 17–18; Bienstock–Muñoz (2018), Theorems 4, 7, 9, and 15, §§1–3 and
Appendix A; Nagarajan et al. (2019), Algorithms 1 and 4, pp. 9–15, and
Lemma 2, pp. 16–18; Langiu et al. (2025), Corollary 3, pp. 23–26; Du–Kearfott
(1994), Theorem 1, pp. 5–7 and Corollary 1, p. 8; Wechsung et al. (2014),
Theorem 1, §§2.2–3; Kannan–Barton (2017), Lemma 8, Theorem 3, and Remark 5,
pp. 20–24.

## Tree-decomposition optimization and spatial branch-and-bound

Finite-domain AND/OR search and weighted-CSP methods already use
separator-conditioned messages, cost shifting, caching, and search bounds
based on treewidth or pseudo-tree depth. These methods work with finite labels
and discrete cost tables. Bienstock–Muñoz provide treewidth-based polynomial
optimization formulations. For continuous nonconvex optimization,
Berenguel et al. give interval branch-and-bound rules for additively separable
functions with common variables. The official publisher page identifies the
article as open access. Although `lit.py` could not extract the PDF (the
publisher URL returned a redirect and the mirror returned 522), the full
primary PDF text was inspected in the publisher's browser PDF viewer. In §5.1,
Proposition 1 selects a retained subbox whose interval on the common variables
overlaps the query interval and uses its smallest lower bound; Theorem 2
combines this with the other interval subproblems to form a lower bound on the
expanded region (printed pp. 1107–1108). Section 6 uses the rule for interval
B&B pruning. This is an important shared-variable intersection comparator,
but it does not state an affine separator certificate or an aggregate
regridding bound.

Deussen and Naumann define structural separability with a scalar separator and
a monotonicity condition over the current domain. Their theorem reduces the
optimization to separator extremization, with interval-adjoint checks and a
proof-of-concept B&B implementation. Schichl and Neumaier construct affine
underestimators on directed acyclic graphs per evaluation. MUSE-BB integrates
decomposition bounds into one spatial B&B tree. These works narrow any broad
claim that decomposition, separator use, or a single spatial search tree is
new. The distinct spatial-tree separation theorem is excluded from this
paper's scope.

Primary locators: Marinescu–Dechter (2009), Theorem 2 and §§4–5, pp. 12,
16–18; de Givry et al. (2006), pp. 2–4; Cooper et al. (2007), Theorem 4.2,
pp. 2–3; Berenguel et al. (2013), §5.1, Proposition 1 and Theorem 2,
pp. 1107–1108, and §6; Deussen–Naumann (2023), Definition 1 and Theorem 1,
pp. 3–4, §§3–4, pp. 9–13; Schichl–Neumaier (2005), §§1 and 8; Langiu et al.
(2025), §§2–3 and 5.2–5.3, Corollary 3, pp. 5–6 and 23–26.
[[deussen2023-subdomain-separability-in-global-optimization]] p.3-4;
[[schichl2005-interval-analysis-on-directed-acyclic]] p.14-17.

Robertson, Cheng, and Scott (2025) analyze convergence orders of value-function
relaxations used in decomposition-based global optimization of nonconvex
stochastic programs. The publisher abstract says their analysis concerns
Hausdorff convergence orders for reduced-space relaxations and regularity of
recourse value functions. The article's full text was not available in this
review, so it is cited only as a neighboring convergence-order study; no
theorem-level comparison is made.

## Inexact dynamic programming, nonlinear repair, and exact output

Approximation-error propagation and reliable bounds from inexact work are
classical in their respective models. Munos bounds policy loss for
approximate value iteration under a discounted Bellman contraction. Devolder,
Glineur, and Nesterov analyze inexact first-order value/gradient oracles.
Guigues (2017) constructs affine lower cuts from approximate primal/dual
solutions and proves deterministic IDDP error bounds; its Corollary 4.8 has a
quadratic horizon factor and linear dependence on bounded stage errors.
Guigues (2020) gives a stochastic SDDP counterpart. Raahauge's 2004 working
paper is directly adjacent on contraction-based value and derivative error
bounds, but only its official abstract and metadata could be inspected.
These works rule out novelty claims for inexact DP or contraction-based error
propagation generally.

Hager's discrete adjoint equations are standard backward costate machinery
for discretized nonlinear control. In the current result, adjoint separator
slopes cancel the first-order term from nonlinear forward-feasibility repair.
Steffy and Wolter repair approximate LP duals into exactly feasible duals;
Gleixner and Steffy obtain exact rational LP solutions from limited-precision
oracle calls. Exact arithmetic and reliable optimization certificates are
not new generally.

The candidate advance is the particular local contract and its integration:
a feasible local point, a valid lower bound, local solve error proportional
to squared cell width, controlled aggregate slope error, a certified upper
value at the reconstructed point, and propagation through arbitrary-tree
separator regridding. For dynamics, restrict the claim to the stated scalar
contracting recurrence, forward-feasible repair, and adjoint cancellation.
For the arithmetic result, restrict it to rational fixed-degree polynomial
box objectives and affine Taylor bag models: endpoint-only exact LP
subproblems and compact rational certificates are obtained with fixed degree,
bag/occurrence parameters, and the stated conditioning hypotheses. Do not
claim general duality, inexact DP, adjoints, rational LP certification, or
polynomial bit complexity uniform in numerical conditioning as new.

Primary locators: Munos (2005), introduction, p. 1006; Guigues (2017),
Propositions 2.2 and 2.7, pp. 4 and 7, Theorem 4.7 and Corollary 4.8,
pp. 19 and 22; Guigues (2020), §2.2 and §§5.1–5.3; Devolder et al. (2014),
Definition 1 and §§2.1–2.2, pp. 3–5; Raahauge (2004), abstract only; Hager
(2000), §§3–4, pp. 255–259; Steffy–Wolter (2013), §§2–3, pp. 2–5;
Gleixner–Steffy (2020), Theorems 3 and 5, §§1.2–3. Cook et al. (2013) and
Eifler–Gleixner (2023) are exact rational MIP-certificate precedents, not
nonlinear-dynamics results.

## Internal companion drafts and overlap

Two unpublished local manuscripts share foundations with this paper. Their
author fields are blank and they have no public identifier or release URL, so
this review does not invent BibTeX entries or treat them as published priority
evidence.

The local draft `paper-bb-complexity/sections/decomposition.tex`, Theorem
`decomp:small-certificate`, proves an \(O(M\log(M/\epsilon))\) certificate
existence bound under quadratic growth. It centers partitions at the known
minimizer and fixes subtree-gradient slopes there. The current paper's
distinction is constructive recovery and regridding without knowing that
minimizer. It should not claim certificate form, growth-based existence, or
shared affine subtree slopes as wholly new.

The local draft `paper-decomposition-aware/sections/grids.tex` and
`sections/growth.tex` give a corrected coordinate-grid DP with coordinate
min-marginals, filtering, and graded grids. Certificate validity is
growth-independent; quadratic growth controls grid and running-time bounds.
The current paper instead uses continuous bag boxes, affine separator
minorants, aggregate copy-disagreement estimates, and a construction that
does not require the minimizer. These are important project-provenance
comparisons, but neither internal draft is a public scholarly citation.
Formal self-citation requires verified authors and a stable public or
submitted record.

## Candidate contribution wording

The manuscript should state only the specific results justified by its proofs:
the exact separator-band distance identity and the stated tree extension;
aggregate arbitrary-tree regridding under quadratic growth and its explicit
assumptions; the concrete inexact local-solve and slope budgets propagated
through that construction; the fixed-parameter rational polynomial
realization with endpoint-only exact LP subproblems and compact rational
certificates; and the stated scalar nonlinear-dynamics repair identity. The
novelty sentence is bounded to “the results reviewed above.” Do not claim
priority beyond the reviewed sources. Exclude the unproved \(C^{1,1}\)
insertion, multidimensional covering characterization, and spatial-tree
separation theorem.

## Round accounting and source status

Round 1 covered four lanes and deduplicated 28 candidates: 9 packages were
created, 1 candidate matched an existing package, 1 was a duplicate source
for an existing package, and 17 were rejected as outside the paper-specific
comparison or redundant. The nine created records comprised seven open/read
sources and two metadata-only packages (Berenguel et al. and Deussen–Naumann).
Munos–Moore was already in the KB; Han et al. was linked as a duplicate source.

Round 2 covered four discovery lanes and two source-promotion candidates,
with 18 deduplicated candidates: 3 packages were created (Ginchev–Hoffmann
2002 and Guigues 2017 open/read; Raahauge 2004 metadata-only), Deussen–Naumann
was promoted to an open/read package, Berenguel promotion returned an ingest
error, and 13 candidates were rejected. The ingest command exited 1 because
the Berenguel HTML response could not be extracted; this remains an explicit
retrieval/extraction failure, not a successful KB promotion. Its theorem
comparison above comes from the complete primary PDF displayed by the official
publisher viewer, not from the KB artifact.

Round 3 followed the direct citation chain for the band approximation result.
It created one metadata-only package for Ginchev–Hoffmann (1997); publisher
full text was subscription-only. Round 4 repeated the narrow citation-chain
check and yielded zero candidates. The direct chain review found no new
interval-band DP-gap or tree-extension result beyond the 1997 and 2002
sources already recorded. This empty fourth round establishes operational
saturation only for that focused chain and the recorded paper claims.

Newly created packages: 13; promotion: 1; one accepted promotion remains an
explicit unresolved error. R1/R2 open additions were read and their notes
record primary-source locators; metadata-only records remain unread. Existing
packages were reused rather than duplicated for Munos (2011), Bachoc et al.
(2021), the interval-cluster papers, Schichl–Neumaier, and Guigues (2020).
The final serialized `lit.py check` exited 0 with `KB_CHECK=ok`,
`UNREAD=217`, and `READ_UNCITED=809`; these counts are also recorded in the
companion run account at `literature/runs/2026-10-06-separator-certificates/run.md`.

Three new notes were checked directly against extracted text and the primary
files: Wald–Globerson's continuous weak-LCR dual and exactness statement;
Ginchev–Hoffmann's ball-shift identity and oriented-distance result; and
Guigues's deterministic bounded-error theorem. Deussen–Naumann's separator
monotonicity statement was also spot-checked against its PDF. The key claims
and page markers matched the originals.

## Complete unresolved source-content list

These are all in-scope materials identified during this review whose primary
source content remains unretrieved as a local KB artifact or remains
unavailable in full. Abstract-only sources are explicitly labeled; no
theorem-level claim is taken from them.

1. N. N. Vorob'ev (1962), “Consistent Families of Measures and Their
   Extensions,” *Theory of Probability and Its Applications* 7(2):147–163,
   DOI [10.1137/1107014](https://doi.org/10.1137/1107014). Best lawful record:
   [MathNet article page](https://www.mathnet.ru/eng/tvp4710). The abstract and
   metadata are available, but attempts to retrieve the primary PDF timed out
   or returned a redirect without text. No theorem or page locator from this
   article is used.
2. Ivan Ginchev and Armin Hoffmann (1997), “On the Best Approximation of
   Set-Valued Functions,” in *Recent Advances in Optimization*, Lecture Notes
   in Economics and Mathematical Systems 452, pp. 61–74, DOI
   [10.1007/978-3-642-59073-3_5](https://doi.org/10.1007/978-3-642-59073-3_5).
   Best lawful record: [Springer chapter page](https://link.springer.com/chapter/10.1007/978-3-642-59073-3_5).
   The publisher abstract supports the historical scalar interval-band
   objective, but the chapter is subscription-only. A ResearchGate upload was
   not used because its version and authorization could not be verified.
3. José Luis Berenguel, Leocadio G. Casado, Inmaculada García, Eligius M. T.
   Hendrix, and Frédéric Messine (2013), “On interval branch-and-bound for
   additively separable functions with common variables,” *Journal of Global
   Optimization* 56(3):1101–1121, DOI
   [10.1007/s10898-012-9928-x](https://doi.org/10.1007/s10898-012-9928-x).
   Best lawful record: [official open-access publisher page](https://link.springer.com/article/10.1007/s10898-012-9928-x).
   The full PDF was inspected in the publisher browser viewer and supports the
   narrow §5.1/§6 comparison above, but the local KB fetch/extraction failed
   (publisher redirect; mirror 522), leaving the package `access:none` and
   `status:unread`.
4. Peter Raahauge (2004), “Upper Bounds on Numerical Approximation Errors,”
   Copenhagen Business School Department of Finance Working Paper 2004-4.
   Best lawful record: [CBS Research Portal item](https://research.cbs.dk/en/publications/upper-bounds-on-numerical-approximation-errors/); listed PDF:
   [7171.pdf](https://research.cbs.dk/files/59045083/7171.pdf). The official
   abstract/metadata supports only a neighboring contraction-based comparison;
   the institutional PDF endpoint returned HTTP 403. The package remains
   metadata-only and unread.
5. Dillard Robertson, Pengfei Cheng, and Joseph K. Scott (2025), “On the
   Convergence Order of Value Function Relaxations Used in Decomposition-Based
   Global Optimization of Nonconvex Stochastic Programs,” *Journal of Global
   Optimization* 91(4):701–742, DOI
   [10.1007/s10898-024-01458-1](https://doi.org/10.1007/s10898-024-01458-1).
   Best lawful record: [Springer article page](https://link.springer.com/article/10.1007/s10898-024-01458-1).
   The publisher abstract and metadata were verified, but the full article was
   unavailable. The manuscript cites only its abstract-supported subject and
   makes no theorem-level comparison.

## Run files

The complete round lane, deduplication, decision, and result files, plus the
source-locator and search account, are archived under
`literature/runs/2026-10-06-separator-certificates/`.
