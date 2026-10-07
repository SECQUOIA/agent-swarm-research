# Handoff to the shared Luna-max literature lead

The box-hull literature agent is paused. It must not run `lit.py get`,
ingestion, a KB check, or any KB mutation until an explicit ownership transfer.
The shared lead owns serialized literature work. This is a handoff of later
needs, not authorization to interrupt the final sparse maintenance boundary.

Project: `/workspace/minlp-notes`.
KB: `/workspace/minlp-notes/literature`.
Paper: `/workspace/minlp-notes/paper-box-quadratic-hulls`.
Existing lookup evidence: `/tmp/literature-box-hulls-20261006` (18 metadata
responses and one extracted AB text). The reported lookup PIDs have exited.
All research and any additions must use GPT Luna with max reasoning and the
existing `$lit` lead. Execute the absolute `lit.py` script directly.

## Remaining deliverables

1. Finish the claim-driven literature/novelty audit in
   `paper-box-quadratic-hulls/evidence/literature-audit.md`, with pinned
   versions and precise source contracts. The manuscript and independently
   reviewed mathematical proofs are already written. Core novelty claims
   concern the missing family and its compact LMI, the rational separator
   against the two named systems, the strict edge-contact classification,
   and the box/sparse-graph applications of the known field-preservation
   obstruction. Do not claim a first exact three-variable hull.
2. Verify the nearby Nishijima symmetric-cone result and supply a short
   source-faithful comparison for the introduction. The current bib entry
   is `Nishijima2026`, arXiv `2602.23725v3`. The paper's box transfer must
   be distinguished from nonrepresentability over symmetric cones.
3. Complete the needed software/product/benchmark citations. Suggested keys:
   `McCormick1976`, `GoulartChen2024` (Clarabel), `ODonoghueEtAl2016` (SCS),
   `BurerBoxQPInstances2019` (already used in the numerical chapter but not
   yet in the bib), and a versioned Gurobi software reference if appropriate.
   Metadata responses for McCormick, Clarabel, and SCS are already in the
   temporary directory. Prefer existing KB packages. Add any missing needed
   papers through the shared `lit` workflow, without rerunning experiments.
   The original baseline lookup also left `crossref-shor1987.json` and
   `crossref-sa1990.json`. Please judge whether the named Shor and RLT
   constructions need their classical citations and supply verified entries
   if they do; this does not change any theorem input.
4. Finish the citation/read receipts and the serialized KB check required by
   `$lit`; report `KB_CHECK`, `UNREAD`, `READ_UNCITED`, the run record, and
   any unretrieved items. The box session has not performed a final KB check
   or written its final audit. Do not attribute another session's check
   to the box session without stating the scope.

## Core contracts already checked by the paused Luna agent

- **Anstreicher–Burer 2010**, Theorem 6: full two-variable box moment hull
  from augmented moment PSD and box RLT, including diagonal caps. Theorem 7:
  exact low-dimensional polytope/tetrahedral moment construction. These
  support Sections 5–6 and the exact numerical comparator.
- **Khajavirad**, arXiv `2601.18545v2`, equation (17): the 27 disjoint
  localizing blocks are the compared three-positive-variable system.
- **Anstreicher–Puges**, arXiv `2501.09150v1`, equations (14)–(16),
  Lemmas 4–5: trilinear RLT and the switched SOC/extended-triangle systems.
- **Burer–Natarajan–Willemsen**, arXiv `2504.03996v3`, Theorem 1:
  dimension **at most three**, arbitrary diagonal and linear terms,
  nonpositive mixed matrix entries, objective-value exactness under
  augmented PSD and ordered componentwise `Y <= m 1^T`. No full-hull claim.
- **Bodirsky–Kummer–Thom**, DOI `10.4171/JEMS/1509`, official full text:
  Lemma 2.3 (unital real-linear CP maps preserve finite LMI formulas),
  Theorem 2.13(1) (Hahn multiplier CP), Theorem 3.7 (strict positive-square
  separation over a real closed extension), Remark 3.2 and Example 3.4
  (Horn obstruction in the rational group algebra), Remark 3.17
  (closed-cone dual-shadow equivalence). The box embedding, lexicographic
  evaluation and graph transfers are manuscript proof steps.
- **Diananda / Maxfield–Minc**, classical order-four CP=DNN and dual
  COP=PSD+nonnegative identity. Complete authoritative read/citation receipts
  remain part of the final audit.

The original edge-contact theorem uses elementary calculus, perturbations
and cube-edge graph arguments. A subsequent facet-zero reduction now has a
complete argument and independent mathematical review at
`evidence/development-continuation.md` and
`evidence/reviews/facet-continuation-review.md`. It removes the pair-minor
assumptions; an independently checked BNW dual-attainment argument also
removes the mixed-product restriction. The final statement requires only
positive square coefficients and positive values at every cube vertex:
such an extreme ray is an affine square or a strict family copy. Only
vertex-zero rays remain outside the classification. Integration remains
gated on checking this precise source input:

**Hildebrand, Minimal zeros of copositive matrices**, arXiv `1401.0134v4`,
Lemma 4.3 and Definition 2.1. The paused Luna agent supplied the contract:
for copositive `B` and nonzero `w`, there is `epsilon>0` with
`B-epsilon*w*w^T` copositive iff `w^T u=0` for every nonnegative zero `u`
of `B`. Confirm exact hypotheses against the available original, including
boundary/support conditions, and provide the correct published citation
(`Hildebrand2014MinimalZeros` is the proposed key). The existing source
contract is sufficient for independent mathematical review but has not yet
received the final original-source receipt. This is now a useful required
source if the stronger theorem is included. No unverified source input or
unproved continuation claim may enter the final paper.

**Gate resolved:** the supplied original-source confirmation received on
6 October verifies the exact criterion without extra conditions. See
[hildebrand-source-receipt.md](hildebrand-source-receipt.md). Appendix F is
now included, and the manuscript bibliography has the published metadata
under `Hildebrand2014MinimalZeros`, with the verified arXiv v4 locator.
Any KB addition and final read/citation/check receipts still belong to the
sole shared lead.
