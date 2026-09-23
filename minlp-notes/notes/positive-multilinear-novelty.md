# Novelty audit: positive multilinear term-by-term gap

Date: 2026-09-04. Scope: primary-source assumptions, later gap results, and the relationship
to coverage functions and correlation gaps. This is a separate-agent literature review, not
external peer review or an exhaustive priority search. Mathematical proof audits are recorded
separately. The candidate result is
[positive-multilinear-gap.md](../results/positive-multilinear-gap.md).

**Assessment:** the sparse unit-coefficient construction fits the stated assumptions of
Luedtke–Namazifar–Linderoth's conjecture. No prior disproof or proof of its dimension-independent
positive-coefficient assertion was found in the targeted searches below. The nearest ordinary
correlation-gap results concern different ratios and do not imply or contradict the candidate.
Subject to the separate proof audits, this is a plausible new counterexample to an explicit
published conjecture. Publication priority remains unestablished.

## Exact source and assumptions

Luedtke, Namazifar, and Linderoth, *Some Results on the Strength of Relaxations of Multilinear
Functions*, Mathematical Programming 136 (2012), 325–351, DOI
[10.1007/s10107-012-0606-z](https://doi.org/10.1007/s10107-012-0606-z).
The [author-hosted technical report](https://jlinderoth.github.io/papers/Luedtke-Namazifar-Linderoth-12-TR.pdf)
has the conjecture on printed page 22, numbered Conjecture 1. The authors' uploaded
[published text](https://www.researchgate.net/publication/228577706_Some_results_on_the_strength_of_relaxations_of_multilinear_functions)
numbers the same statement Conjecture 4.1, on journal page 349. The local PDF is the
technical-report version.

The conjecture concerns a uniform constant upper bound on the ratio of term-by-term gap to
convex-hull gap for multilinear functions with positive coefficients on boxes `[ℓ,u]` where
`ℓ≥0`. It imposes no fixed polynomial degree, fixed term count, homogeneous-degree condition,
or lower bound on positive coefficients. The definition in Section 1 allows arbitrary sets
of included monomials. The constant is intended to be uniform over this class, extending the
positive bilinear constant bound; it is not merely a constant depending on each fixed
polynomial. The concluding discussion explicitly describes that intended generalization.

Section 4 defines the term-by-term relaxation using each monomial's *exact* convex and
concave envelopes, independently. It distinguishes this from recursive McCormick relaxation.
The candidate uses exactly this stronger term-by-term benchmark; shared-intermediate
recursive formulations and added interterm cuts are separate objects.

In the sparse candidate, every included coefficient is 1, the box is `[0,1]^n`, and
`n=2^L+L`. There are `2^(L+1)−2` included monomials. Its maximal degree is `2^(L−1)+1`.
All specified evaluation coordinates are interior. Thus the construction refutes a constant
uniform over dimensions if its divergent lower bound is correct. It does not refute a bound
that is allowed to depend on polynomial degree or on distance to the box boundary.

## Later optimization literature checked

- [Boland, Dey, Kalinowski, Molinaro, and Rigterink, Bounding the gap between the McCormick
  relaxation and the convex hull for bilinear functions](https://arxiv.org/abs/1507.08703),
  Mathematical Programming 162 (2017), 523–535. Its unbounded lower bound uses mixed signs
  in bilinear coefficients; it resolves the older mixed-sign bilinear question. It retains
  the positive-bilinear distinction and does not supply a positive multilinear counterexample.
- [On linear programming relaxations for solving polynomial programming problems](https://www.sciencedirect.com/science/article/abs/pii/S0305054818301643)
  discusses the 2012 numerical comparison and still describes nonnegative-domain,
  positive-coefficient termwise hull relaxations as strong. Its stated contributions compare
  RLT, J-set, and quadrification relaxations. The accessible introduction does not report a
  resolution of the positive-coefficient uniform-gap conjecture. This paper was screened,
  not completely proof-audited.
- [Schutte and Walter, Relaxation strength for multilinear optimization: McCormick strikes
  back](https://arxiv.org/abs/2311.08570), and the cited Khajavirad 2023 paper on recursive
  McCormick relaxations, concern the relation between recursive linearizations and extended
  flower relaxations. Their relevant local sections and conclusions were checked. They do
  not state the positive-coefficient width-ratio result being investigated here.
- [He and Tawarmalani, Tractable relaxations of composite functions](https://par.nsf.gov/servlets/purl/10382117)
  develops supermodular hypograph relaxations, optimal-transport descriptions, and a
  Section 3.2 characterization for termwise relaxation of bilinear functions. The downloaded
  manuscript's abstract and relevant section were checked. An exact hypograph theorem alone
  does not control the gap between hypograph and epigraph bounds.

These are concrete scope checks, not a claim that every citation or later version of each
paper has been exhaustively investigated. In particular, publication and repository upload
dates shown by search engines were not treated as theorem dates.

## Exact relation to coverage functions

This subsection is an elementary derivation used to distinguish the candidate from nearby
literature. Let

```
f(x) = Σ_{e∈E} a_e ∏_{i∈e} x_i,       a_e>0,
W = Σ_e a_e,
C(S) = Σ_e a_e 1[S∩e≠∅],            S⊆[n].
```

Then `C` is a weighted coverage function. Set `p=1−x`. For any random failure set `S`
with inclusion marginals `p`, the complementary binary vector satisfies
`f(1−1_S)=W−C(S)`. Write `C⁺(p)` and `C⁻(p)` for the largest and smallest possible
expected coverage under these marginals.

The minimum coverage is

```
C⁻(p) = L_C(p) := Σ_e a_e max_{i∈e} p_i.
```

The inequality `C⁻≥L_C` follows separately for each edge. A single common threshold with
`S={i:p_i≥U}`, `U` uniform on `[0,1]`, attains every edge bound simultaneously. This is the
coverage-function case of the standard Lovász-extension/convex-closure identity.

The sum of individual monomial convex envelopes transforms into the familiar edgewise
coverage upper bound

```
U_C(p) := Σ_e a_e min{1, Σ_{i∈e} p_i}.
```

Consequently the two widths in the positive multilinear conjecture are exactly

```
tbtgap_f(x) = U_C(p)−L_C(p),
chgap_f(x)  = C⁺(p)−L_C(p).
```

Hence the candidate asserts that the ratio
`[U_C−L_C]/[C⁺−L_C]` is unbounded even for unit-weight coverage functions with a sparse
explicit incidence representation. This is a useful alternative statement for a future
literature search. It is not the ordinary correlation gap.

## Why known correlation-gap bounds do not settle the conjecture

[Agrawal, Ding, Saberi, and Ye, Price of Correlations in Stochastic Optimization](https://web.stanford.edu/~yyye/priceofcorrelation.pdf)
compares the largest expected value at fixed marginals with the expectation under mutually
independent coordinates. Its Section 3 treats monotone submodular functions, while its
Section 5 gives the common-threshold extremizer for supermodular functions. Both facts are
consistent with the candidate.

For the coverage function above, independent sampling gives

```
F_C(p) = Σ_e a_e [1−∏_{i∈e}(1−p_i)].
```

The elementary union bound and product estimate imply
`C⁺(p)≥F_C(p)≥(1−1/e)U_C(p)`. This compares absolute values. Subtracting `L_C(p)`
from both sides gives only

```
C⁺−L_C ≥ (1−1/e)(U_C−L_C) − L_C/e,
```

which supplies no positive constant multiple of `U_C−L_C` when `L_C` is large. Thus neither
the usual coverage LP factor nor the standard submodular correlation-gap factor provides
the desired width comparison. The candidate exploits precisely this distinction.

Recent searches also retrieved [Ramachandra and Natarajan, Counterexample to a conjecture on
the pairwise independent correlation gap using AI](https://arxiv.org/html/2606.19663v1)
(June 2026). Its definitions compare `C⁺` to a maximum over pairwise-independent distributions.
It concerns a different 2025 conjecture and supplies a small counterexample to a `4/3` bound.
It does not address the ratio after subtracting `L_C`, and its pairwise moment constraints
are absent from the multilinear-envelope problem.

## Directed hypergraph cuts, Horn SAT, and nonmonotone correlation gaps

The candidate also has an exact directed-cut interpretation. Write `X` for the binary
success set, and for an anchor `a` and its block `B` put

```
D_(a,B)(X) = 1[a∈X] 1[B⊈X]
           = 1[a∈X] − 1[{a}∪B⊆X].
```

This is a nonnegative submodular function: the first summand is modular and the second
indicator is supermodular. It is the cut predicate for a directed hyperedge with singleton
tail `{a}` and head `B`, under the convention that some tail vertex lies in the set and
some head vertex lies outside it. The convention matters: directed hypergraph papers use
several inequivalent cut definitions. The submodular convention is stated explicitly, for
example, in the primary paper
[Submodular Hypergraph Partitioning: Metric Relaxations and Fast Algorithms via an Improved
Cut-Matching Game](https://arxiv.org/pdf/2301.08920)
(ICALP 2025; Section 4.1 of the full version). That paper studies minimum ratio cuts and metric relaxations, not the
prescribed-marginal maximization below.

Let `D=Σ_(a,B) D_(a,B)` and let `D⁺(x)` maximize `E D(X)` among distributions with
every inclusion marginal equal to `x_i`. The candidate's hull gap is exactly `D⁺(x)`:
the expectation of `Σ_(a,B)1[a∈X]` is fixed and equals the simultaneous concave-envelope
value of the positive polynomial. The sum of the separate cut concave closures is

```
U_D(x) = Σ_(a,B) min{x_a, Σ_(i∈B)(1−x_i)}.
```

The individual formula follows by making the leaf-failure union as large as possible,
then overlapping it maximally with the anchor event. In the candidate `U_D=L`. Thus the
result can equivalently be described as an unbounded gap between the sum of individual
cut concave closures and the concave closure of their sum, at prescribed marginals.

This distinction rules out a direct appeal to an unrestricted Max Cut integrality gap.
If anchor and head sets are disjoint and nonempty, independent fair coin choices cut each
singleton-tail edge with probability `(1/2)(1−2^(−|B|))≥1/4`. Any edgewise LP objective
is at most the total edge weight. Therefore the unrestricted maximization has a factor-4
comparison by this elementary argument. The candidate's prescribed marginals preclude
changing all probabilities to `1/2`. Fixing a single cardinality also does not fix every
marginal.

[Guruswami and Zhou, Tight Bounds on the Approximability of Almost-Satisfiable Horn SAT
and Exact Hitting Set](https://yuanz.web.illinois.edu/papers/Horn-1ink-UG.pdf)
(Theory of Computing 8, 2012) is the closest multiscale LP-gap construction located in this
extended search. Section 3.2 describes Horn implications that propagate geometrically
growing fractional deficits, while any integral assignment violates a clause. It then
constructs stronger SDP gaps. Its Horn violation predicate is
`(∏_(i∈T)x_i)(1−x_h)`: all tail variables must be true and the head false. This is not
the candidate's singleton-tail/some-head predicate. Moreover, its large gap concerns the
minimum unsatisfied deficit; maximizing satisfaction retains a large baseline. The paper
also proves logarithmic hardness for exact hitting set with mixed set sizes. Neither
result, as stated, gives the prescribed-marginal cut-closure ratio above. The shared use
of geometric scales should be acknowledged in any broader discussion of technique;
we have not established a reduction from those examples to the multilinear counterexample.

[Gallo, Gentile, Pretolani, and Rago, Max Horn SAT and the Minimum Cut Problem in Directed
Hypergraphs](https://iris.unimo.it/handle/11380/585403)
(Mathematical Programming 80, 1998) studies a hierarchy of LP formulations for Horn SAT
through directed hypergraph minimum cuts. The authors' institutional abstract was checked;
an open full text was not obtained in this audit. Its title should not be taken as evidence
that it studies the same cut convention or the same fixed-marginal maximum. This is an
explicit limitation of the search.

[Rubinstein and Singla, Combinatorial Prophet Inequalities](https://arxiv.org/pdf/1611.00665),
Section 4, Example 4.1, already shows that the ordinary correlation gap of a nonnegative
nonmonotone submodular function is unbounded on a single directed edge. At marginals
`(ε,1−ε)`, independent expected cut is `ε²`, whereas the cut concave closure is `ε`.
This example has `U_D=D⁺=ε`, so the ratio investigated here is exactly 1. It cannot
serve as a prior counterexample to the multilinear conjecture. Their constant-factor
replacement uses a monotone envelope or scaled marginals, which changes the benchmark.

[Chekuri and Livanos, On Submodular Prophet Inequalities and Correlation Gap](https://arxiv.org/pdf/2107.03662)
(2021 manuscript; Theoretical Computer Science 1019, 2024) gives a finer comparison
between independent expectation and concave closure in Theorem 1.1, depending on the
largest marginal, and in Theorem 1.2 allows a smaller marginal vector. These theorems
also do not compare `U_D` with `D⁺` at the same prescribed vector. In particular, known
nonmonotone correlation gaps are a genuine neighboring subject, not a resolution of
the sum-of-closures question.

No direct prior counterexample or theorem implying the present gap was found in this
extension. The Horn connection and differences above were checked against the primary
definitions and gap construction. This is still a bounded search, not a proof that no
appropriate CSP reduction or equivalent formulation exists.

## Search record and remaining uncertainty

The targeted searches included these exact phrases or their close combinations:

- `multilinear positive conjecture gap`
- `Luedtke Conjecture 4.1`
- `positive coefficients term-by-term gap`
- `multilinear term-by-term counterexample`
- `multilinear envelopes gap ratio`
- `termwise convex hull positive gap`
- `coverage concave closure Lovasz extension correlation gap difference`
- `correlation gap Lovasz coverage`
- `differential approximation coverage gap`
- `directed hypergraph integrality gap`
- `directed hypergraph cut linear programming`
- `directed hypergraph concave closure`
- `directed hypergraph marginals`
- `Max Horn integrality gap`
- `maximum directed hypergraph cut approximation`
- `non-monotone submodular correlation gap unbounded`

Targeted `rg` searches also screened the local papers citing Namazifar, especially their
conjecture, gap-ratio, positive-coefficient, and concluding passages. Some web searches were
repeated excluding secondary aggregation sites. Primary texts were used for substantive
claims; an unsuccessful search was not treated as proof of nonexistence.

No directly matching published counterexample, universal positive result, or reference
explicitly resolving Conjecture 4.1 was found. Potentially relevant older probability
literature on simultaneous Fréchet bounds and more specialized approximation results for
coverage *improvements above a correlated baseline* remain incompletely explored. The
responsible current status is therefore **candidate disproof with targeted novelty search
finding no match**, contingent on completed independent mathematical audits.
