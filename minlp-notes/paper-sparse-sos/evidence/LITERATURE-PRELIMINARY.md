# Preliminary literature map for the sparse SOS paper

**Status: early evidence for active drafting, not the completed literature audit.**
This note records source contracts already checked in the literature KB and
the project's retained primary-source audit. It does not establish priority.
The full `LITERATURE.md` will add the current citation-chain search, verified
source metadata, and all retrieval gaps.

## Safe attribution boundaries

### Sparse convergence and gluing are established

Lasserre's sparse moment/SOS hierarchy already uses local moment and
localizing matrices under running intersection. Theorem 3.6 gives convergence
of the sparse values under its boundedness and local-support assumptions; the
proof glues consistent local representing measures. The paper also gives a
sparse Putinar representation and a finite rank test. These are qualitative
convergence, measure-gluing, and finite-extraction precedents, not the
finite-order quantitative transfer proved in the present project.
[[lasserre2006-convergent-sdprelaxations-in-polynomial-optimization]]
p.6–12, p.13–16

The important gap is that a feasible finite-order moment functional need not
come from a measure. The new ordinary-module argument must explain how it
turns arbitrary feasible truncated functionals into compatible local laws
with controlled objective loss. It should not claim a new junction-tree
gluing theorem.

### Keep ordinary modules and preorderings separate

The ordinary box module has one SOS block for the constant and one for each
individual generator `1-x_i^2`. The full preordering also includes products
of distinct generators. Their degree bounds and block counts differ, and
products of univariate interval certificates naturally enter the
preordering. A result for one cone does not transfer to the other merely
because both are called sparse SOS. The hierarchy definitions in the current
setting section state this distinction explicitly.

Magron's Lorentz Center slides of 7 July 2025, slide 23/44 (PDF page 90),
explicitly assert an `O(R^-2)` sparse **preordering** gap and attribute it to
Korda, Magron, and Ríos-Zertuche (2024). The 16 February 2026 TENORS slides,
slide 35/90 (PDF page 121), repeat the inverse-square assertion. Both source
slides are retained and were visually checked in the research record:
[2025 slide PDF](../../research-20260928/solver/prior-sources/magron-lorentz-2025-07-07.pdf),
[2026 slide PDF](../../research-20260928/solver/prior-sources/magron-nlmoment-2026-02-16.pdf).
Therefore the inverse-square sparse-preordering rate must not be called new.
The slide assertion and the published theorem's different exponent should
both be reported; the evidence does not license silently treating the slide
as a typo or adding an unstated hypothesis.

The published Korda–Magron–Ríos-Zertuche article is a broader-domain
correlative-sparsity result. The prior source audit identifies its Theorem 6
as the sparse box-preordering rate `O(R^(-2/(w+3)))`; Theorem 8 treats
ordinary modules on general domains under normalized local Archimedean
certificates and local Łojasiewicz assumptions. The ordinary box theorem in
the current project therefore needs a cone-specific, assumption-by-assumption
comparison. [Published article](https://doi.org/10.1007/s10107-024-02071-6).
This source is not yet a read package in the KB; its article text and theorem
numbers will be verified and ingested in the full audit before citation in a
final source ledger.

### Dense rates are prior; the overlap transfer is the candidate addition

The dense ordinary box-module rate `O(log^3(R)/R^2)` from the squared-kernel
construction is prior. The project source audit attributes it to Gribling,
de Klerk, and Vera, Theorem 7 of the 2026 preprint
[*Squared polynomial approximation kernels for the hypercube*](https://arxiv.org/abs/2605.31496).
That theorem is dense. It does not by itself align laws on overlapping bags.
The candidate ordinary-module contribution is the finite-order transfer to
overlapping bags, using corrected signed densities and a common reference
law, with an error normalized by the sum of local nonconstant Chebyshev
coefficient norms and no extra bag-count or tree-shape factor at fixed width
and degree. The rate statement is not a runtime theorem.

Magron's 2026 product-set theorem supplies another important boundary. Its
Theorem 11 and Corollary 12 give inverse-square convergence for dense full
preorderings on stated product domains, including cubes; it does not prove
the current project's sparse ordinary-module overlap transfer.
[[magron2026-convergence-rates-for-polynomial-optimization]] p.2–4,
p.12–14, p.21

### Partial-degree convex hierarchies are established

Fixing a low degree in convex/private variables while increasing degree in
shared variables is not new. The current setting section already attributes
this design to Kahl's partial relaxations and to robust SOS-convex
hierarchies. The claim should be restricted to quantitative analysis of the
particular sparse private-degree-two hierarchy, including its stated
fixed-domain, affine-recourse, and regular-multiplier rates. Do not claim the
partial-degree construction itself as new. The Kahl entry and precise source
scope are still being checked; the current draft's provisional key is
`kahl2005-globally-optimal-estimates`.

The robust SOS-convex comparator is in the KB under the canonical key
`wang2025-a-moment-sum-of-squares` (Guo and Wang, 2025; DOI
`10.1287/moor.2023.0361`). It studies robust polynomial matrix inequalities
under SOS-convexity, compactness, and Slater-type assumptions; its hierarchy
and guarantees do not establish the current project's private-degree-two
sparse recourse rates. [[wang2025-a-moment-sum-of-squares]] p.2–5,
p.13–17, p.22–24

## Existing exact-certificate methods bound the rationalization claim

Peyrl and Parrilo give a numerical-symbolic procedure for turning an
approximate SDP Gram matrix into an exact rational SOS identity under strict
feasibility. Davis and Papp give quantitative rational dual-certificate
bit-size bounds and a rational-arithmetic Newton/rounding algorithm under
interior and conditioning assumptions. Thus rational SOS conversion is not
new as a general method. The project's narrower consequence is to derive a
quantitative slack from its sparse kernel theorem and then discharge the
finite cone's bit-size and feasibility conditions for the specified
expanded local Gram bases.
[[peyrl2008-computing-sum-of-squares-decompositions]] p.1–4, p.7–10;
[[davis2024-rational-dual-certificates-for-weighted]] p.9–15,
p.20–29

The rational-certificate note specifically assumes a real certificate with
quantitative slack at the chosen finite order. It does not infer strict Gram
feasibility from pointwise positivity at an arbitrary order. Its polynomial
construction bound is in the expanded SDP dimensions, including the local
preordering generator products. The exact unknown-center strong-feasibility
ellipsoid citation and theorem contract are under source verification; the
authors may omit the algorithmic time claim if that contract cannot be
confirmed. The accepted polynomial-size rational witness remains distinct
from that construction-time claim.

## Canonical keys in the shared setting section

These are identity checks for the citations currently in
`sections/02-setting.tex`; they are not a substitute for final source
locators.

| Current key | Status for drafting |
|---|---|
| `lasserre2006-convergent-sdprelaxations-in-polynomial-optimization` | Canonical KB key; read source. Use for sparse convergence and local-measure gluing, not the new finite-order quantitative transfer. |
| `wang2025-a-moment-sum-of-squares` | Canonical KB/BibTeX key for Guo–Wang. Replace provisional `guo2025-robust-pmi-sos-convex`. |
| `bental2001-lectures-modern-convex` | Draft key; exact edition/theorem and finite-SDP Slater statement are pending source verification. |
| `powers2000-univariate-interval` | Draft key; verify the exact Powers–Reznick source and the even/odd degree-preserving interval forms before final use. |
| `kallenberg2002-foundations` | Draft key; standard-Borel disintegration citation is pending edition and locator verification. |
| `vorobev1962-consistent-families` | Draft key; verify the exact bibliographic identity and relevance to finite-family extension. Lasserre 2006 already suffices for the sparse measure-gluing attribution. |
| `kahl2005-globally-optimal-estimates` | Draft key; verify source identity and state only the partial-degree convex-hierarchy overlap supported by the source. |

The final audit will resolve these entries against the shared bibliography and
KB, report unread and inaccessible sources, and supply page or theorem
locators only when the source text supports them.

## Contribution language that is currently defensible

- Do not claim the first sparse inverse-square rate: the slides already
  announce that rate for a full preordering, and dense ordinary-module
  squared-kernel rates are also prior.
- The clearest candidate distinction is the unconditional finite-order
  quantitative transfer to the ordinary sparse box module for arbitrary
  feasible truncated functionals, producing exactly compatible local laws
  and an `O(log^3(R)/R^2)` error under running intersection, without requiring
  an attained polynomial separator dual.
- For private recourse, claim only the theorem-specific rates under their
  stated domains, degree schedule, convexity, complete-recourse, and
  multiplier-regularity assumptions. The fixed-degree private block is
  established design precedent; the quantitative rate classification for
  this hierarchy is the candidate contribution.
- No general MINLP running-time improvement, practical speedup, or publication
  priority follows from these comparisons.
