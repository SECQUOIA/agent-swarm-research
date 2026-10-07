# Continuous certificates and constrained geometry: author record

Date: 2026-10-05. Owned submission files: `sections/certificates.tex`,
`sections/geometry.tex`, and `appendices/geometry-proofs.tex`.
The chapters are complete. `REVIEW-MANUSCRIPT-GEOMETRY-R1.md` records
the independent final review's finding of no remaining material
mathematical or exposition issue. Root owns standalone compilation and
integration.

## Scope and current evidence

I read `BRIEF.md`, `AUTHORING-CONVENTIONS.md`,
`ARCHITECTURE-DECISION.md`, the relevant architecture entries, the full
spatial audit and nonlinear-repair review, `INCOMING-AUDITS.md`,
`ISSUES.md`, and the current `LITERATURE-KEYS.md` and bibliography.
The final reread used the October 5 versions that include the compatible
original constraint tuple, all-owner tube accounting, augmented probing
events, fresh evaluation-cover count, and the restriction against treating
an owned event family as an ordinary valid closed-box cover.
`evidence/LITERATURE.md` did not yet exist at the final author reread;
the stable-key map supplies the literature scope used here.

Primary mathematical source families inspected:

- `research-20260928b/bb-complexity/spatial-constrained/instance-dependent-node-complexity.md`.
- `research-20260928b/bb-complexity/spatial-face-exact/face-exact-node-complexity.md`.
- `paper-bb-complexity/evidence/AUDIT-SPATIAL.md`.
- `paper-bb-complexity/evidence/REVIEW-GEOMETRY-REPAIR-R1.md`.

Read-only supporting proof review was delegated for regular KKT rates and
McCormick graph geometry. Its findings are incorporated below. No
supporting agent edited manuscript files. The independent final reviewer
also checked the saved submission proofs during writing; final review
and source hashes belong in the reviewer's separate report.

## Claim, hypothesis, source, and proof map

| Submission label | Main hypotheses and conclusion | Source and manuscript proof |
|---|---|---|
| `cert:def-classes`, `cert:eq-benchmarks` | Raw valid cover, interior-disjoint rectangular partition, and axis split-tree minima are distinct; cover <= rectangle <= tree | Constrained source §1.3 and face-exact source §1.2 used different N_opt conventions; definitions and explanation in certificates |
| `cert:lem-events` | Pointwise objective gap, permitted split/reduction model, recursively expanded successful probe partitions; disjoint convex rectangular owners give K_F <= ell_aug+2n R_rel | Constrained source Lemma 2.1 repaired by audit §2 and independent repair review; full direct ownership/removal proof in certificates |
| `cert:eq-work`, `cert:eq-eval` | Nodes, reduction rounds, virtual probes, and evaluations remain distinct; node lower consequence requires bounded rounds, solve consequence requires distinct evaluation charges and counted successful sources | Audit §§2.3–2.4 and repair review; direct construction/explanation in certificates |
| `geom:thm-cover-lower` | Uniform positive bound lower gap; every feasible near-optimal owned point is close to a test vertex | Constrained source Theorem 4.6; full proof in geometry |
| `geom:lem-arcsine`, `geom:thm-stratum` | Embedded C1 d-stratum, finite dominant-coordinate multiplicity; per-test arcsine bound and stratum integral lower bound | Constrained source Lemma 4.1/Theorem 4.5; full Cauchy–Binet/coordinate-area/arcsine proof, with degenerate-box treatment, in geometry |
| `app:geometry:lem-graphs` | C2 graph on convex tangent-domain, bounded graph Hessian; two-point inequality and dominant-coordinate injectivity on uniformly small patches | Constrained source Lemmas 4.2–4.3; full Taylor/singular-value proof in appendix |
| `geom:lem-localize` | Second-order pointwise upper relaxation error, error bound to full F for small original violation, Lipschitz objective, ideal optimal incumbent | Constrained source Lemma 6.1; full relaxed-witness-to-feasible-witness proof and grid charge in geometry |
| `geom:thm-profile`, `geom:eq-running` | Positive bound lower gap plus upper/localization assumptions; all raw benchmarks bracket running-supremum covering profile within O(log(1/eps)); direct comparison for owned K_F | Constrained source Theorems 6.2–6.3 and Remark 6.3a; full proofs in geometry; no N_cover <= K_F claim |
| `app:geometry:ex-wells` | Smooth one-dimensional family with uniform Hessian/relaxation constants; bounded single-scale profile but at least K/2 valid boxes | Constrained source Remark 6.3a; complete convexity, sublevel, and separated-well proof in appendix |
| `geom:prop-dimension`, `geom:prop-manifold` | Explicit global quadratic growth to optimal set; covering-dimension exponent p/2, positive-dimensional regular manifold exact rate eps^(-p/2), finite optimal set upper log only | Constrained source Theorem 6.4/Corollary 6.5 and Theorem 7.2; full tube/grid geometric-sum and chart-count proofs in geometry. Upper assertion expressly does not need objective lower gap |
| `geom:thm-integral` | Explicit parabolic proximity, stratum quadratic doubling, lower density, finite coordinate multiplicity, upper localization assumptions and positive bound gap | Constrained source Hypothesis R/Theorems 6.6–6.7; full separated-packing/Tonelli proof in geometry. Finite 0D strata add upper-only log terms |
| `geom:lem-tube-events`, `geom:eq-infeasible-cover` | Inner tube with alpha>=0,beta>0; all owners count, no original-feasibility propagation; dichotomy and infeasible near-optimal covering bound | Constrained source Lemma 5.1/Theorem 5.2 plus repaired ownership; full proofs in geometry |
| `geom:thm-tube-kkt` | f and compatible original exact/relaxed tuple C2 on open neighborhood, combined LICQ, same-tuple KKT multiplier on a relaxed constraint, active stratum d>=1 | Source Lemma 5.5/Proposition 5.6/Theorem 5.7, completed in audit §5 and REVIEW-GEOMETRY-REPAIR-R1; full new IFT curve, uniform graph inverse, multiplicity, relative-area and logarithm proof in `app:geometry:proof-tube-kkt` |
| `geom:cor-kkt-rates` | Finite global KKT minima, local full-feasible C2 description, LICQ, strict complementarity, SOSC, independent upper/error assumptions; log upper; matching objective/tube lower under their separate assumptions; unique 0D stratum exact grid under vertex-vanishing upper error | Constrained source Theorem 7.1 and Proposition 6.8; full direct normalized-sequence QG and sharp-growth/grid proof in `app:geometry:proof-kkt-rates`; equality-only 0D case handled explicitly |
| `geom:ex-flat-tube` | Exact linear objective, deliberately relaxed halfspace, isotropic versus directional constraint loosening | Constrained source Example 5.3; full raw eps^(-1/2) lower/upper and exact three-slab directional certificate in geometry. Isotropic upper invokes upper-only QG, not a nonexistent objective lower gap |
| `geom:lem-mcc-gap`, `geom:eq-mcc-upper` | Fixed convex g plus termwise bilinear decomposition, original-variable polyhedron kept exactly | Face-exact source Lemmas 2.1–2.2 and 2.5; full convex-combination envelope derivation, endpoint-product bounds, graph zero faces and upper-error proof in geometry. The minimum of the two products attains its maximum at the center; neither individual product is claimed to do so |
| McCormick ownership paragraph after `geom:eq-mcc-upper` | Explicit owned validity Gamma_C <= m+eps; envelope-domain monotonicity; same-relaxation/source-owner and distinct-cost transfer | Face-exact source Lemma 1.2 repaired by spatial audit; full short monotonicity/ownership proof in geometry, independently checked during final review |
| `geom:thm-flat-graph` | Selected coefficient subgraph H, bounded convex near-optimal subset of p-flat, tau(V,H); tau-positive power lower bound; graph transversality sufficient | Face-exact source Theorem 3.6/Lemma 3.7; full centroid/width proof in geometry; elementary tail-volume centroid proof in `app:geometry:lem-centroid` preserves half-open owners |
| `geom:prop-curved-graph` | Compact C1 p-stratum, all vertex-cover tangent projections injective, selected coefficient graph | Face-exact source Theorem 3.8/Lemma 3.9; full finite-chart slab measure and endpoint-cover proof in geometry |
| `geom:prop-fractional` | Near-optimal full-dimensional cube for lower; full relaxed graph for anisotropic gap-budget upper | Face-exact source Proposition 3.10/Corollary 3.11; full multiplicative-width LP proof and grid construction in geometry; half-integrality proved in `app:geometry:lem-half-integral`. Corrects source's upper claim when E had been introduced as a proper subgraph |
| `geom:prop-matching` | Matching k>=1 in termwise graph, explicitly feasible slice; selected concave chord directions | Face-exact source Theorem 3.4/Corollary 3.5; full preimage-rectangle/chord/AM–GM/arcsine proof in geometry; log consequence assumes nontrivial feasible chord and positive quadratic upper constant |
| `geom:prop-ray` | Nontrivial feasible one-sided ray, selected concave edge, liminf m(ray)/t=0 | Face-exact source Proposition 4.6(b), repaired in audit §6.1; full finite-interval compactness divergence proof in geometry, with constraints allowed |
| `geom:prop-aligned-two` | Convex continuous g+cxy, full optimal root-spanning vertical segment, no additional constraints | Face-exact source Theorem 4.4; complete transverse-slope proof using direct convex combinations in `app:geometry:proof-aligned-two`; at most two leaves, root exact at endpoint |
| `geom:ex-aligned-three` | Fixed decomposition phi=xy-xz of a convex quadratic; aligned optimal segment | Face-exact source Example 3.12(b); complete strip-center lower and direct O(1/s) active-dyadic-box upper in geometry; all raw benchmarks Theta(eps^(-1/2)) |

## Corrections and scope decisions incorporated

- GEO-1/2/3: retained boundaries belong to the continuing owner; raw cover,
  partition, and tree minima remain separate; actual nodes exclude probing
  only when no virtual stopping partitions are used. Repeated round work is
  never converted to node work without a round bound.
- GEO-4: the nonlinear IFT transfer keeps the original exact/relaxed
  assignment and violation function. All objective and constraint data
  used by the theorem are explicitly C2 on an open neighborhood. Uniform
  inverse-map/Hessian/coordinate-sheet/relative-area constants are proved.
- GEO-5: optimal-set dimension gives the power only under quadratic growth.
  A width-only upper error cannot support a finite exact certificate at a
  sharp minimum.
- FACE-2/3: graph lower bounds are separate from the generic box-face
  integral characterization; alignment alone is not enough in dimension
  three; the constrained concave-ray divergence proof includes its missing
  limiting argument. Fractional-cover upper constructions use the full
  relaxed graph.
- Exact original-constraint propagation is excluded substantively from
  tube lower bounds. The full all-owner count K_all and its fresh evaluation
  analogue are used; feasible-only filtering would lose the witnesses.
- Zero-dimensional KKT strata have bounded exact certificates only with
  vertex-vanishing upper error. Dyadic log lower statements require a
  middle-position condition, not merely nondyadic coordinates.

Editorially unselected material: product-integral matching bounds with
log^(2k) loss; generalized star-center aligned certificates; curved
row-slice example (its matching upper bound remains unknown); first-order
and arbitrary higher-order gap extensions. These are not used by any
selected proof and no claim about their unresolved generalizations is
made. The neighboring face-exact author owns the full C1,1 box-face
integral characterization and analytic/RLCT consequences. The decomposition
author owns the fixed-path exponential center-volume specialization.

## Literature use and integration

The chapter cites the stable scope-approved keys for Du–Kearfott,
Wechsung–Schaber–Barton, Kannan–Barton 2017,
Bachoc–Cesari–Gerchinovitz, and McCormick. Classical cluster results are
identified as upper-estimate precedents; the bilinear formula is credited
as classical. The chapter makes no blanket originality claim. The
coordinate area formula, Cauchy–Binet identity, implicit function theorem,
and elementary convex analysis are used as standard mathematical tools;
the certificate-specific arguments are supplied fully.
The final root/Luna correction marks the 2018 Kannan–Barton author-hosted
copy unread because no verified lawful full-text source was established.
The opening citation to that paper has been removed; no mathematical
claim here relies on that source.

Concrete integration requests:

1. Root should run the integrated standalone LaTeX build. No extra package
   or shared macro is needed by these files.
2. The literature lead/root should finish its existing primary-source
   scope/bibliography audit for the five cited keys. If a bibliographic
   citation for the standard coordinate area formula is desired, supply
   its verified key/locator; no external research was done by this author.
3. Root/coverage lead should record independent final review resolution
   and hashes after the reviewer's final pass. No mathematical blocker
   remains known to this author.

## Verification actually performed

Read-only targeted commands: `rg --files`, `rg -n`, `cat`, and `sed -n`
on the listed evidence and two source topics; `wc -l` and `sha256sum` on the three owned
submission files. A targeted Python scan of only those three files checked
balanced TeX groups, matched begin/end environments, unique labels, owned
cross-reference resolution, and citation-key presence in `references.bib`.
Result: all three files passed; 77 unique labels; all owned references and
the five used bibliography keys resolved after the literature correction.

No experiments were rerun, no project-wide verification was performed,
no CI status or logs were inspected, no literature was browsed, and no
other author's file was edited. The author scan is not a LaTeX build and
does not imply any CI result.
