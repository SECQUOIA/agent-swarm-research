# Stage 7 synthesis: source and priority audit

Date: 2026-09-22. This author stage integrates the already reviewed primary
source comparisons in `literature.md` and `stage04-literature.md` through
`stage06b-literature.md`; it does not replace them with a search-based
absence claim. The current coverage table maps all included developments.

Freshly reopened the primary versioned pages:

- Blekherman–Dey–Sun, [arXiv:2210.01722v2](https://arxiv.org/html/2210.01722v2):
  checked the definition of good aggregation, the framework and standing
  dimensions, and the separation between the three conjectures. The HTML
  contains a generated date inconsistent with its fixed version metadata;
  the manuscript identifies the May 29, 2023 arXiv version rather than
  interpreting that generated date as a new scientific revision.
- Blekherman–Dunbar, [arXiv:2405.18282v1](https://arxiv.org/html/2405.18282v1):
  retained the exact qualified external input already checked in stage 6.
  The paper credits the existing four-bound and limiting-eigenvector
  antecedent. It claims the complete strict-system transfer, not invention
  of the number four or first removal of an infinity condition.

The introduction explicitly credits Dines, Yildiran, Polyak, DMS, BDS, BD,
Dunbar's dissertation, classical fidelity/rotation formulas, quadratic matrix
programming, and univariate approximation. The prior infinite example and
its failure of HHC remain in Section 7. The prior QMP convexification result
and its r≥3 scope remain distinguished from our direct r≥2 strict proof.
Rote's exponent is not claimed anew. The single-objective result is credited
to convex duality and is not an iteration lower bound. No new general
aggregation, semidefinite-lift, or inverse-square exponent claim is made.

Dunbar dissertation priority retains the exact previous access qualification:
a public reader extraction was available, the original PDF fetch failed,
and the stronger prior stated regular nonstrict result is acknowledged.
This stage makes no new assertion about the completeness of that dissertation
proof. The paper uses the qualified BD theorem instead.

The direct two-point construction was checked against actual
`Formal/InfiniteAggregation/HullCore.lean` and its root/weight lemma and
formal coverage. Its scientific content is written out in the main paper,
not offered merely as a claim that software verifies a missing proof.
The auxiliary direction is perpendicular to `b*u-a*v`, so r=2 suffices.
All other supplied formal coverage was reconciled against topic27–31 module
lists, declarations/coverage maps and existing audit records. The 2n+1 versus
signed-coordinate SDP tests and the sqrt(2)/2000 versus 1/2000 lower constants
are explicitly distinguished.

No literature PDFs, repository literature indexes, or other topics were
modified. The bibliographic audit found 26 entries, all cited, with no missing
keys. Versioned preprint and journal records remain distinct where numbered
locators depend on a specific version.
