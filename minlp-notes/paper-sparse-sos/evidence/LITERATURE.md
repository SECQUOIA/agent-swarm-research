# Literature and contribution audit

The final manuscript cites 40 distinct works. Literature research and primary
source reading used GPT Luna at max reasoning. Three read-only source lanes
verified the bibliography and checked the actual claims; one reusable Luna
lead owns all serialized `$lit` ingestion, promotion, index regeneration, and
integrity checks. The local skill is
`/workspace/local-home/repo/skills/literature/SKILL.md`. No independent source lane
mutated the shared literature folder.

The detailed source contracts, reading status, version distinctions, exact
locators, and initial local-package requests are in:

- `literature-lanes/kernels-ledger.md` and its bibliography/key map;
- `literature-lanes/recourse-ledger.md` and its bibliography/key map;
- `literature-lanes/standards-ledger.md` and its bibliography/key map.

`canonical-citation-map.json` records the final citation reconciliation.
The initial 45 assigned citation keys reduce to 40 retained works after
duplicate versions/aliases are collected and two unnecessary citations are
removed or replaced. The manuscript bibliography contains publication
metadata, not internal reading statuses or research paths. The source
checker confirms that every cited key is present. The separate
`citation-inventory.json` comparison confirms that there are no uncited
bibliography entries.

## Scope of the contributions

| Development | Prior work and precise boundary of the claim |
| --- | --- |
| Sparse full-box preordering at inverse-square order | Magron's July 2025 and February 2026 public slides already assert this sparse rate. The manuscript does not claim the rate as new. It gives a self-contained compatible-density proof, explicit coefficient budgets, and rounding. Published Korda–Magron–Ríos-Zertuche Theorem 6 states a slower rate; the discrepancy with the slides remains documented rather than dismissed as a typo. |
| Sparse ordinary box module | Gribling–de Klerk–Vera supplies the dense squared-kernel and logarithmic rate precedent. The manuscript constructs a normalized signed kernel and one common positivity correction with exact separator marginals. The gap has no additional bag-count or tree-size factor beyond its stated coefficient budgets; SDP size and those budgets can still grow with the bags. Priority is qualified. |
| Fixed quadratic obstruction and exact low orders | Moment matching versus best uniform approximation is established, including Han–Jiao–Weissman. Qualitative sparse zero-margin obstructions have precedents. The manuscript proves the quantitative inverse-square obstruction on one fixed quadratic instance and exact SDP values at orders one and two. Equality at all higher orders remains a conjecture. |
| Private-degree-two convex recourse | Partial lifting, parametric moment methods, and quadratic pseudomoment Jensen have precedents. Kahl–Henrion lifts a limited nonlinear subset; Guo–Wang instead fixes the SOS-convex decision-variable degree and increases the uncertainty degree. The manuscript proves finite-order source-feasibility and rounding estimates for its explicitly defined rectangular shared/private truncation. It does not identify that cone with a total-degree hierarchy. |
| Affine recourse and regularity | Hoffman repair and first-moment repair precedents are attributed separately. The manuscript proves a sharp inverse-order rate with a fixed private constraint matrix, and improved rates under explicitly stated projected-multiplier conditions. Arbitrary multivariate Lipschitz multipliers are not covered. Classical parametric QP sensitivity supplies a sufficient regime, not a novelty claim. |
| Polynomial constraints | Tran–Toh gives dense preordering bounds with the same global Hölder exponent. Heijmans et al. gives a polynomial lift; the displayed logarithmic composition is an inference for a dense formulation. The manuscript proves sparse compatible rounding and a sharper direct squared-displacement estimate for its ordinary-module extension, with a global geometric assumption. It also proves constrained certificate-supremum equality and strict-slack membership from the box order unit, without claiming boundary attainment. |
| Finite-state labels | Labels are retained exactly and continuous coordinates alone are smoothed. The development proves mass-scaled correction, zero-mass control, and the pruned-label dual statement. It does not cover label-dependent continuous domains. |
| Rational certificates | Peyrl–Parrilo and Davis–Papp establish rational recovery and bit-size precedents. The manuscript specializes these methods using explicit full-box interior directions and coefficient correction. Witness size is polynomial in expanded SDP dimensions and rational input length, including slack. No polynomial-time discovery of an unspecified real witness is claimed. |

The contribution descriptions in the introduction and discussion were
checked against the theorem statements and these source contracts by GPT
Sol. No publication-priority claim rests on an inaccessible theorem text.
The paper's proofs of its own results are complete; source access limits
are distinguished from unresolved mathematical gaps.

## Corrections made after source reading

The main bibliography uses the verified Baldi–Slot DOI
`10.1137/23M1555430`, Helfried Peyrl's correct first name, the plural title
of Kahl–Henrion's ICCV paper, and the 2026 publication metadata for
Miller–Wang–Guo. Tran–Toh's preprint and journal version are one work;
Baotić and Tøndel citation aliases are also collected. The wrong Kahl PDF
linked from one university metadata page was rejected in favor of the
verified LAAS author copy. Ben-Tal–Nemirovski's readable separation theorem
replaces an unread Rockafellar reference; the unnecessary Lauritzen
reference was removed because the dynamic program is proved in the paper.

The Catala convolution comparison is explicitly a torus-Fourier result
with a cosine-map inference. The exact Chebyshev-grid statement comes from
the manuscript's proof, while Bienstock–Muñoz supplies a bounded-treewidth
LP comparison. Zhang–Zhong is cited for repair precedent without
transferring its Wasserstein-radius convention into an unsupported rate.

A final retained-file handoff mislabeled the titles of the Heijmans and
Powers PDFs. This was caught before ingestion. The actual first pages match
the assigned works, and the Luna standards reader rechecked the original
lift, substitution, interval-positivity, Slater, and separation passages.
The error was confined to the handoff response; the bibliography and
source-contract ledger were correct. The Powers author copy has garbled
plain-text extraction, so its title and relevant page were checked visually.
This extraction issue is distinct from inability to retrieve the original.

## Retained source-content access limits

These are the four limits among the final cited works/versions. Their
identities are verified, and unverified page/theorem pinpoints are not used.

1. **Kallenberg, *Foundations of Modern Probability*, second edition
   (2002).** DOI `10.1007/978-1-4757-4015-8`; the publisher's
   [conditioning and disintegration chapter](https://link.springer.com/chapter/10.1007/978-1-4757-4015-8_6)
   was available as metadata, but its full text was not retrieved. The
   manuscript uses the standard regular-conditional-distribution result
   without an unverified pinpoint citation.
2. **Rudin, *Real and Complex Analysis*, third edition (1987).**
   Bibliographic identity is retained; no lawful full-text copy was
   verified. The standard signed Riesz representation step has no invented
   theorem or page locator.
3. **Vorob'ev, “Consistent Families of Measures and Their Extensions”
   (1962).** DOI `10.1137/1107014`; the
   [publisher abstract](https://epubs.siam.org/doi/abs/10.1137/1107014)
   supports broad historical attribution, but the full article was not
   retrieved. The finite-tree gluing proof is supplied in the manuscript
   and has a directly read Lasserre precedent.
4. **Tran–Toh, “Convergence of Truncated Moment Sequences with
   Applications to Polynomial Optimization” (published 2026).** DOI
   `10.1007/s10107-026-02394-6`; the
   [journal record](https://link.springer.com/article/10.1007/s10107-026-02394-6)
   was verified, but the final article text was unavailable. The complete
   [arXiv preprint](https://arxiv.org/abs/2507.00572v1) was read and supports
   the cited comparison; its theorem locators are not attributed to the
   unread journal version.

Lawful copies can later be added through the same serialized lead using
`literature/inbox/`; these access limits do not prevent the present proofs
or manuscript delivery. They are not silently promoted to full-text-read
status.

## Literature-folder maintenance

The reusable lead completed all 29 requested package additions: 10 recourse
works, 13 sparse-hierarchy works, and six standards works. Twenty-one
packages are read and eight remain metadata-only/unread. Kahl's later
promotion uses the verified author copy and does not count as another work.
The existing Peyrl record now identifies Helfried Peyrl correctly.

Five metadata-only packages have primary content read outside the KB:
Catala et al., Laurent–Slot, both Magron slide decks, and Nie et al. Their
imports returned HTML rather than a stored readable artifact. The remaining
three are Kallenberg, Rudin, and Vorob'ev. These local-package states are
distinct from the four retained source/version access limits above.
Tran–Toh's preprint is locally read; the final journal text remains unavailable.

The final direct `$lit` check completed at 05:59 UTC on 6 October 2026,
exit 0: `KB_CHECK=ok`, `UNREAD=197`, `READ_UNCITED=770`. Three existing
unrelated preview warnings remain. These counts describe the shared KB at
that check, not just this paper's references.

[`LITERATURE-KB.md`](LITERATURE-KB.md) gives every candidate outcome,
package slug, access state, and preserved run path. The supplied batches
stopped after processing the identified sources; they do not assert
discovery saturation or completeness of the literature. The source lanes'
initial absence counts are historical requests. The root's source check
and PDF build do not substitute for the lead's `$lit` integrity check.

The final GPT consistency review,
[`final-literature-receipt-gpt-r1.md`](reviews/final-literature-receipt-gpt-r1.md),
accepted the work mappings, actual package states, archived outcomes,
source-file hashes, and check chronology. Earlier raw search lanes and API
captures are preserved under `literature-discovery/` with an exact-copy hash
manifest; their incomplete status is explicit.
