# S4a adjudication

The lead read the entire authored section, its relevant repository developments and primary-source passages, and all six review reports. The five independent gate reports are `completion-s4a-r2.md` through `completion-s4a-r6.md`. Reviewer 1 inadvertently encountered author/lead report search hits after its mathematical pass; its report is supplementary, and reviewer 6 replaced it for the independence requirement. The replacement did not read excluded reports.

All five gate reviewers found no major issue. Their mathematical audits cover the rational quadratic certificate, nomination faces, fixed-global-rank algebraic optimization and recovery, discrete reductions, cactus flow regions, quantitative graph restoration, and convex-region classifications including the qualitative nonlinear-power extension. Existing numerical checks supplement these proof reviews; they do not establish the universal claims.

Two valid minor findings require correction:

1. Reviewers 3–6 (also supplementary reviewer 1) identify an ambiguity in the Brandenberg–Stursberg comparison. Each differential-flow polytope fixes its elasticity vector, but their universal cactus characterization quantifies over all positive elasticity vectors as well as nomination and capacity bounds. State both levels explicitly. The lead independently verified the original preprint's Theorem 18 on page 19. This changes attribution wording, not the present theorem.
2. Reviewer 2 identifies imprecise positivity wording in the hull and region theorem statements. Balanced nominations need not be positive. Specify rational nominations and, where applicable, objective coefficients, and strictly positive rational resistances. Preserve the polynomial encoding claim for quadratic witnesses and the qualitative existence-only claim for general powers.

No other requested correction was found in the five complete reports. A separate correction agent will implement both findings and rebuild Paper A. No repeat review round is required because no major issue was identified. Stage acceptance remains pending verification of these corrections and the build.

## Acceptance

The separate correction agent applied both findings. The lead read the corrections and correction report, verified all 13 build input hashes, and confirmed a successful Paper A build with no unresolved references/citations, duplicate labels, or overfull boxes. Section 6 SHA-256 is `20030371746b874b82e7704767b33e18e05216373d02dd755d79927a08d47904`. S4a is accepted. No major issue remains and all valid minor issues have been addressed.
