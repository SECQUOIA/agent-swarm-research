# Result coverage and proof provenance

The source material is the revised
`research-20261001/binary-separation/note.md`, the general-integer precursor
`research-20260928b/side-results/split-separation-np-complete.md`, and the
mathematical developments in `research-20261001/split-practice/note.md`.
The submission is self-contained and does not cite these internal notes as
proof authorities.

| Result | Manuscript location | Development and scope |
|---|---|---|
| Cut, correlation, moment, and split equivalences | Section 2 | Direct identities replace references to a precursor note; switching and the factor-of-two convention are explicit. |
| Complete exact-cover encoding | Theorem `thm:exact-cover` | Every integer layer is analyzed, including parameter endpoints. Only covers give negative slack. |
| Polynomial rational scaling | Lemma `lem:scaling` | Sphere-center projection proves the common-denominator and strict-definiteness bounds without inverse-entry estimates. |
| Metric and strict elliptope promises; fixed gonality | Theorem `thm:relaxation-hardness`, Corollary `cor:hypermetric-hardness` | Complete rounded and split witness lists establish all promises on yes and no inputs; fixed-cutoff padding is quantified correctly. |
| Gap-one, rounded-psd, Boros–Hammer, and gonal union | Theorem `thm:binary-families` | Hardness uses controlled witnesses, not family containment alone. Gap-one NP certificates use switching signs. |
| Boolean quadric clique, cut, and signed families | Theorem `thm:finite-families` | Exact witnesses are stated up to duplicate polynomial data; the unbounded parameter in the signed family is handled by a best-offset verifier. |
| Required facets | Lemma `lem:clique-facets` and Section 4 | New manuscript supplies the full elementary face-dimension proof, including unused variables; no disputed historical facet condition is needed. |
| Pure hypermetric and odd clique families | Theorem `thm:pure-clique-hardness` | Orthogonal nearby points preserve positive definiteness. Unswitched all-positive odd cliques are treated separately. Maximum violations are conditional on a cover. |
| Polynomial certificates | Lemmas `lem:short-hypermetric-witness`, `lem:short-split-witness` | Rational quotients and integer linear systems prove polynomial witness length for singular as well as nonsingular inputs. |
| Rank algorithm | Theorem `thm:rank-separation` | Exact rational Gram input is converted to a rational Euclidean instance before applying Kannan's CVP theorem. Unsupported fixed-radius enumeration bounds are omitted. |
| Fixed support and gonality | Corollary `cor:bounded-support-separation` | Induced-support rank algorithms avoid facet-coefficient bounds. Polynomiality for fixed support is distinguished from rank FPT. |
| Normalized threshold | Theorem `thm:threshold-separation` | Strict rational comparisons and the exact ceiling-minus-one norm cutoff yield an XP bound, not FPT in the inverse threshold. |
| Primitive directions and raw maximum | Section 5 | The exact decomposition and rational discreteness arguments are stated in the general integer moment setting. |
| Raw-value approximation | Corollary `cor:raw-approximation` | The exact zero-or-positive maximum gives finite-factor and inverse-polynomial additive-error hardness. There is no fixed additive-tolerance claim. |
| Rational rank-one raw maximum and restricted coefficient hardness | Propositions `prop:rank-one-split-value`, `prop:restricted-rank-one-hardness` | Boolean rank-one moments are integral; these boundary examples concern general integer moments only. |
| Gap-zero separation | Theorem `thm:gap-zero-hardness` | Complete Laplacian reduction includes exact rational metric bounds, one negative eigenvalue, and a nearness statement. PARTITION reduction establishes NP-completeness without a strong-hardness claim. |
| Full gap scope | Section 7 and Remark `rem:general-gap-scope` | The non-PSD decision question is always positive; the tight gap of a given coefficient vector is a separate problem. Full gap separation on PSD points remains unresolved. |

The mathematical claims are analytic. Existing experiment records were accepted
as permitted by the user, but are not used as substitutes for proofs or reported
as new computational evidence. The paper makes no solver-performance claim.
Its approximation-hardness result concerns raw violation with a finite-factor
guarantee or the stated inverse-polynomial additive accuracy; it makes no
fixed-additive-tolerance claim.

Novelty is limited to the precise complete hardness proofs and relaxation
promises supported by the literature audit. Definitions, switching, covariance,
classical facet results, normal-form algorithms, and closest-vector algorithms
are prior work. The paper discloses secondary statements of hypermetric hardness
that do not provide a proof, rather than treating the primary open-problem
statements as an unconditional priority guarantee.
