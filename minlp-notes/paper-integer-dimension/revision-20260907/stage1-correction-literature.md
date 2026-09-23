# Stage 1 correction literature evidence

September 7, 2026. This supplements `stage1-literature.md`; no literature
package, index, or historical report was changed.

- Cevallos, Weltge, Zenklusen, *Lifting Linear Extension Complexity Bounds
  to the Mixed-Integer Setting*: inspected [arXiv:1712.02176v1](https://arxiv.org/html/1712.02176v1),
  Section 1, equations (2)–(3), and Theorem 1. Checked the model against the
  [primary PDF](https://arxiv.org/pdf/1712.02176), PDF page 3, and Theorem 1
  on PDF page 4. The model projects a polyhedron intersected with integrality
  conditions and takes the convex hull. Complexity counts facets and integer
  coordinates. Theorem 1 gives integer-count lower bounds with a linear-size
  restriction for matching, odd-cut, cut, and TSP polytopes. The introduction
  cites only this resource distinction, not proof details. Conference year
  and pages are confirmed by Schade et al.'s published reference 8: SODA
  2018, 788–807. The BibTeX URL fixes the inspected preprint version.

- Schade, Sinha, Weltge, *Lower bounds on the complexity of mixed-integer
  programs for stable set and knapsack*: inspected the [published article](https://link.springer.com/article/10.1007/s10107-025-02234-z),
  Section 1's model definition, Theorem 1.1, and Appendix A, Lemma A.1 and
  its proof. The model uses a polyhedron and affine integrality map, with
  affine objectives representing all weights. Lemma A.1 relates it to the
  projected mixed-integer-hull model, allowing an affine restriction.
  Theorem 1.1 strengthens the integer lower bound for stable set and
  knapsack families under a facet-count restriction. Publisher metadata:
  volume 216, 135–176 (2026), online May 19, 2025. The brief comparison
  distinguishes facet counts from rational bit length and convex-hull
  representations from containment of the projected graph approximation
  itself. No full proof audit or claim of applicability to this paper's
  arbitrary convex lifts is made.

- LinA: reread [[codsi2025-lina-a-faster-approach-to]] p.9-10 and p.12,
  and checked the original PDF using a fresh `pdftotext` extraction.
  Section 4.1 assumes continuously differentiable convex boundaries;
  Remark 3 explicitly provides continuity in this case. The logarithmic
  function/derivative oracle count is for Algorithm 2's maximal-segment
  computation. The revised introduction states each qualification.

- Vielma: checked [[vielma2018-embedding-formulations-and-complexity-for]]
  p.5-7 and the original PDF. Assumption 1 requires rational polyhedra,
  nonempty extreme-point sets, and a common recession cone. The bounded,
  nonempty case used in the introduction satisfies these conditions.
  The manuscript's elementary real-coefficient extension remains separately
  identified as Lemma `lem:disjunction`.

- IQS: the [publisher record](https://link.springer.com/article/10.1007/s00037-018-0165-7)
  confirms the published title's spelling “non-commutative.” The journal
  title is preserved while the URL now fixes the [v6 manuscript](https://arxiv.org/abs/1512.03531v6)
  used for theorem locators.

These are bounded source/model checks. They add context for integer count
and description resources and do not establish priority by absence of a
matching literature result.
