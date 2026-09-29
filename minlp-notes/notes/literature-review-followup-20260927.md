# Research-note corrections after the September 26 literature review

The library review and five supplied journal papers support corrections to
attribution, source access, and novelty wording. Comparison with the current
research notes found no new source that refutes the repository's stated
theorems. This was a source comparison, not a fresh proof audit or exhaustive
publication-priority search. Many of the limits highlighted by the library
review were already recorded in the research notes.

| Topic | Finding and action |
|---|---|
| Ridge envelopes | Corrected the authors and arXiv identifier for *MIP Relaxations in Factorable Programming*: He and Tawarmalani, arXiv:2310.07168. He, Liu and Tawarmalani's arXiv:2310.08424 is the separate fractional-programming paper. The staircase proposition remains the same source result. |
| Iterated OBBT | Removed Proposition 3 from the introductory list of claims without a known counterpart. Its scalar threshold already has a cluster-analysis analogue, as the body of the theory note explains. Replaced universal assertions about unpublished combinations and stopping rules with statements limited to the sources inspected. Updated journal and thesis access records. |
| Concave row hulls | Corrected the blanket statement that Lim–Linderoth–Luedtke give no complete description or separation: they give local four-dimensional hulls and separation for tilted lot-sizing inequalities. Added the now-read Wolsey–Yaman upper-, lower-, and two-sided balance hulls. Novelty of inequality rows or setup indicators alone is unsupported; the arbitrary concave-cost mapping requires the comparison. |
| Shared-variable curves | Updated Ballerstein's library status: a metadata record now exists, but the original PDF remains unretrieved. The older note reports reading an institutional text extraction; the new access failure does not erase that earlier evidence or constitute a fresh PDF verification. |
| Three-variable quadratic cuts | The existing publication assessment already credits exact three-cube hull formulations and earlier separation. Its proposed contribution is the specific sparse-SDP counterexample and explicit family with compact enforcement. No additional downgrade was supported by this comparison. |
| Subset-parent star gaps | The existing priority review already credits the compatibility hierarchy, arbitrary-order incompatibility, and generic optimization advantage. Its remaining claim is the conditioned original-variable indicator-quadratic realization and quantitative gap. No new contradiction was found. |
| Penalty encoding and calibration | The existing significance review already distinguishes finite exactness, encoding size, and threshold computation, and credits the squaring-chain mechanism and earlier QUBO hardness. Its remaining claims concern optimized multipliers and the stated native constraints. No new contradiction was found. |

The main source checks were against local originals or extracted full texts:

- He–Tawarmalani's title page, Section 4.2.1, Proposition 4.4, and Remark 5.4
  in [the MIP source](../literature/papers/he2024-mip-relaxations-in-factorable-programming/fulltext.md),
  plus the [fractional source](../literature/papers/he2024-convexification-techniques-for-fractional-programs/fulltext.md).
- Lim–Linderoth–Luedtke, local hulls on PDF pp. 6–9 and tilted lot-sizing
  separation on pp. 14–15, in [the supplied source](../literature/papers/lim2018-valid-inequalities-for-separable-concave/fulltext.md).
- Wolsey–Yaman, flow-balance hulls on PDF pp. 6–11, in
  [the retained source](../literature/papers/wolsey2021-convex-hull-results-for-generalizations/fulltext.md).
- Wechsung–Schaber–Barton, prefactor thresholds on PDF pp. 8–9, in
  [the supplied source](../literature/papers/wechsung2014-the-cluster-problem-revisited/fulltext.md),
  compared with the existing OBBT Proposition 3 and its cluster follow-up.

The library files are local, ignored research state. Tracked research notes
retain the bibliographic identities and substantive comparison even when
those local links are unavailable in another checkout.

Verification: targeted `git diff --check` on the seven edited research notes
and this account; local Markdown link checks on the changed files; and
direct inspection of the changed passages against the sources above. No
project-wide verification or CI inspection was performed.
