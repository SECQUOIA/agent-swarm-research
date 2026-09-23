# Stage 1 primary-agent reading

## Scope

Read the source uniform-control and continuous one-switch proofs, current foundations draft, topic readiness and literature records, and the broader claim inventory. Final review-round adjudication will follow the five independent reports.

## Independent mathematical observations

- Uniform convergence preserves the monotone, 1-Lipschitz coordinate conditions and the identity that their sum is time. Absolute continuity then recovers a measurable simplex-valued derivative. Thus the cumulative input class is compact by Arzelà–Ascoli.
- For a fixed mode word, cumulative occupation depends continuously on ordered switch times, including collisions. Deleting zero blocks and merging equal neighbors represents exactly the intended budget class. Taking a finite union proves compactness.
- The error and its one-sided version are 1-Lipschitz in the cumulative input. Both inner optima and outer minimax extrema are therefore attained. This is a useful explicit foundation, not a new general compactness principle.
- Endpoint monotonicity means that averaging an arbitrary measurable input on the specified grid preserves the objective of every schedule on that grid. Consequently the grid minimax has the same value whether its adversary is restricted to cellwise constant controls or allowed all measurable controls.
- The last fact gives the comparison `F_cont <= F_grid` by applying schedule-class inclusion to every measurable input. This is not inferred by silently identifying different adversarial classes. It supplies the missing argument behind a conservative warning in the old grid-transfer note. Sent to the stage author for inclusion and independent review.
- The uniform-control lower recurrence counts service in the current block even when its label appeared previously. The matching construction uses distinct labels only where the number of available labels permits it. These are different logical roles and must remain explicit.

## Coverage decisions

The exact equal-total two-switch value is not subsumed by the unrestricted full-error theorem for all small mode counts. It remains assigned to stage 2. Historical claims that a subsequently solved case is still open must not be carried into the paper.

## Frozen draft checks

Read all of the eight-page stage01-round01 LaTeX text. Independently expanded the one-switch contradiction: summing the failed candidate inequalities gives `(2n-1)E < n-1-(n-2)m_q-m_r`; the largest/second-largest mass inequality gives the required contradiction for n>=3. Checked the heavy case at equality m_q=E, the n=3,4 transition, and the two exact discrete witnesses. Checked that the integer recurrence threshold lies in `[N,N(n-1)]`, including n=2 and N=1, and that its strict grid correction follows from the floor/ceiling identity with no floating tolerance.

Visually inspected the retained original manuscript p.27 image. Its displayed Conjecture 1 equation (7.6), both branches, and `1<=s<=N-2`, `n>2` assumptions match the quoted formula. Source scope will receive the separate reviewer check and final-source audit. Checked the inserted averaging comparison and confirmed the frozen snapshot manifest is unchanged (13 files). The current LaTeX log has no warning or over/underfull-box match.

No major issue identified in this primary reading. Independent reviewer reports are still pending; this is not stage acceptance.
