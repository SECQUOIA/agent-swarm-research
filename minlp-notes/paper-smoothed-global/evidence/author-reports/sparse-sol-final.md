# Sparse and feasible-domain author report: final Sol revision

Sol completed the interrupted revision in the four owned submission files:
`sections/05-sparse.tex`, `sections/06-constraints.tex`,
`appendices/C-sparse.tex`, and `appendices/D-constraints.tex`. This report
is the only evidence file written. The mathematical repairs below are
complete in the live text. They require a final independent review of the
integrated source; this report does not certify the unseen changes of
other authors or final bibliography identities.

The revision used the complete brief, integration contract and decisions,
notation and inventory, the previous sparse author report, the prewriting,
early and complete sparse/domain Sol reviews, and the preserved Opus
editorial findings and root disposition. The later
`reviews/opus-math-partial-r1.md` was also read: it records partial proof
coverage but supplies no additional specific finding or final verdict.
The required preliminary literature note was read. Its bibliography subset
was empty when checked, and the live `references.bib` was absent; neither
was treated as a completed source audit.

The response table gives final live locations. `05`, `06`, `C` and `D`
mean the four owned files in the order listed above; line numbers refer to
this revision, and labels remain stable if integration moves the lines.

| Finding or obligation | Final response | Final locations |
| --- | --- | --- |
| Complete S1: equality-budget multipliers were wrongly included in the simplex margin event | Closure premises, success proof, multiplier lemma and margin event include only zero-coordinate inequalities and tight budgets of inequality blocks. Original equality-budget multipliers are unrestricted and excluded. The main text gives the positive-unequal-noise counterexample and explains cancellation in derivative differences. | `06:637`, `D:495`, `D:570`, `D:594`; `lem:con:simplex-close`, `lem:con:simplex-tail` |
| Complete S2: coarse simplex corners and exterior cubes | For every `h_j >= 1`, use the original simplex vertices as corners and grid. For `h_j=1/m<1`, use only cube indices `0,...,m-1`. The rounding lemma distinguishes coarse vertices from fine cube corners, and coarse counts use the direct vertex bound before face comparisons. | `06:609`, `D:388`, `D:398`, `D:448`; `lem:con:simplex-round`, `lem:con:simplex-count` |
| Complete S3: division by zero in a fully fixed inequality block | Drop empty free-coordinate blocks before computing width sums. Fix the sole remaining coordinate of an equality block to its residual budget. Remove forced lower/upper blocks, return a point at tangent dimension zero, and form the strict center only in remaining blocks with positive width sum. | `D:543`, `D:547`; patch construction in `lem:con:simplex-close` |
| Complete S4: point outputs before GLS | Box point evaluation was retained; Appendix C now states the positive-dimension interface explicitly. Explicit graph, implicit graph, simplex and order proofs branch before the positive-dimensional GLS lemma. Fixed retained graph coordinates still require dependent-root and objective refinement. | `05:1023`, `C:180`, `C:186`, `D:74`, `D:301`, `D:669`, `D:1047`; `prop:sp:eval`, `lem:sp:gls` |
| Complete S4: implicit fixed-point precision | A point patch evaluates its chart roots and objective in polynomial bit work. Coordinate brackets receive `q+O(log(n+m+1))` precision; the objective oracle receives its additional polynomial encoded allowance. Exact feasibility belongs to the lift; the separate rational ambient approximation can be infeasible. | `D:301`; proof of `thm:con:graph`(I) |
| Complete S5: parent-count bound | Explicit substitution depends on at most `min{n,k^{D_g}}` retained variables. The false comparison between ambient parent count and retained dimension is removed. | `D:48`; proof of `thm:con:graph`(E) |
| Complete S5: irrational constant implicit roots | Substitute only explicit rational constants or rational singleton brackets. Other constant implicit roots remain in the chart and original-domain rational fallback formula; empty ancestor sets do not affect decomposition connectivity. | `06:187`, `D:9`; `def:con:graph`, `lem:con:expand` |
| Complete S5: incumbent point association | Initialize `U_{-1}=+infinity` and store the point associated with the smallest certified upper value. Keep an earlier point when its bound remains better; update before pruning. The same convention is explicit for the exact sparse incumbent and conditional interface. | `05:384`, `05:608`, `06:354`, `D:173`; `lem:con:approx`, `prop:sp:conditional` |
| Complete S5: zero-dimensional stationary tuples | Simplex and order faces have one empty stationary tuple at dimension zero. The implicit KKT count has the same convention if its system has no unknowns. The positive-dimensional nonsingular-root lemma is not applied in these branches. | `D:240`, `D:617`, `D:993`; `lem:con:kkt`, `lem:con:simplex-tail`, `lem:con:order-tail` |
| Known actuator curvature finding | Retain the corrected positive enclosure `L=max{1,L_q+Lambda G_2}`. It also bounds the initial-state coordinate, since `Lambda G_2` is nonnegative. | `06:474`, `D:352`; `eq:con:Lact` |
| Known uniform-family coefficient-height finding | Retain the polynomial coefficient-length and production-cost premises `P_1(I+b)`, `P_2(I+b)`. Explicit substitution and actuator proofs now state both costs, with fixed-format exponents. | `06:72`, `D:44`, `D:358`; `lem:con:uniform` |
| Known all-fixed input finding | Mixed-box preprocessing returns its unique rational point before maxima or width divisions. Actuators substitute fixed free coordinates first and return the unique trajectory on the all-fixed branch. Graph point charts are evaluated directly. | `05:64`, `05:950`, `06:187`, `06:438`, `06:496`, `D:347`; `def:sp:algorithm`, `thm:con:actuator` |
| Known common-descriptor finding | Remove the obsolete assertion that sound continuous singleton-hull fixing is absent from the common model. Local soundness continues to use optimizer containment, separately from original-bound gradient forcing. The model owner was notified and owns its common clause. | `05:109`, `05:815`; patch output and `prop:sp:closure-sound` |
| Known order premise finding | Retain the corrected introduction: orders replace fixed outside feasibility by an attaining-point transport upper support. Neither the projection nor the transported fiber is asserted to equal a fixed box fiber. | `06:24`, `06:671`, `D:753`; `lem:con:transport` |
| Known quadratic-hardness scope finding | Retain the explicit Del Pia--Khajavirad NO-family gap and witness relation, with its finite-law threshold probability and narrow source attribution. This is a comparison with the sampled problem, not an original-threshold algorithm. | `05:1087`; `rem:lim:dk`, `prop:lim:threshold` are owned by the boundary author |
| Decision 10 / inventory B10 | Complete the certified conditional-recourse count, including sound pruning, incumbent upper bound and actual returned feasible-completion witnesses. The oracle is an assumption; no efficient outside solver or unconditional width-FPT algorithm is claimed. | `05:598`, `05:625`; `prop:sp:conditional`, `eq:sp:conditional` |
| Opus editorial P2 | Retain the conservative companion comparison: deterministic growth-conditioned graded grids, the supplied work/output bounds, graded versus uniform coordinate counts, and the stated rETH limitation on the condition-parameter exponent. The high inverse-growth moment argument is now an explicit truncated-moment bound including its finite atom term. It makes no impossibility claim about other algorithms. | `05:694`, `05:710`, `05:1100`; `sec:sp:width`, `sec:sp:prior`, citation `companion-decomposition-aware` |
| Shared fallback contract | All routes invoke the original-domain shared-root fallback and retain `B poly(I+b)` construction and `B poly(I+q)` evaluation factors under their polynomial-bit laws. Feasible point and objective-gap repairs for graph, simplex and order fallbacks are explicit. Shared-root construction itself remains owned by the foundations author. | `05:1004`, `C:212`, `D:320`, `D:688`, `D:1070`; `thm:count:fallback` |

For B10, the outside domain is the fixed original product domain `X_O`.
With `e_j=pLh_j^2/8` and certified width `eta_j<=a e_j`, all level-j calls
are included before retention. Bag-only mean-preserving rounding gives
`min_corner W_beta <= f*+e_j`. Thus `f*<=U_j<=f*+e_j+eta_j`, and every
retained corner has its returned feasible completion of value at most
`f*+2(e_j+eta_j)`. For counting, dominate even draw-dependent errors by the
deterministic tolerance `2(1+a)e_j`. Comparison intervals are then
independent of all bag coefficients after conditioning on outside noise.
The expected tuple count is

`product_{i in beta}[4+(L w_i/(2 sigma))(1+(1+a)p/2)]`,

with `M>=2^J` paying for the grid atoms and corner incidence at most
`2^{|beta|}`. This is a count and an oracle contract; it leaves the cost of
outside conditional optimization unspecified. The deterministic filter
is attributed to the decomposition-aware companion.

The moment comparison uses `Z=L/g*`, `A_0=LW/sigma` and
`epsilon_M=2n C_tail/M`. For `r>1`, `K>=1`, the integrated tail bound is
`E min{K,Z^r} <= 1 + r A_0/(r-1)(K^{1-1/r}-1) + epsilon_M K`.
Only the linear small-growth tail's insufficiency is asserted. A different
expected-time algorithm is not ruled out.

The development map of `sparse-r1.md` still applies to inventory B1--B9,
F7/F9/F11 and the graph, actuator, simplex, order and TU supporting proofs.
This revision adds substantive B10 coverage at `prop:sp:conditional` and
keeps the width and local-error barriers scoped to their specified rules.
The TU paragraph still proves aligned continuous rounding only; it supplies
no general expected-time TU optimizer. The preserved Opus mathematical
record does not identify its unspecified minor gaps, so they cannot be
marked resolved from that record alone.

Targeted verification actually run:

- Read the four live source files and the required evidence files with
  `cat`, `sed -n`, `rg` and `wc -l`; re-derived the rounding, witness,
  comparison, multiplier and evaluation inequalities stated above.
- Compiled only the four owned TeX files in
  `/tmp/sparse-sol-final-check/wrap.tex`, with the manuscript preamble and
  live macros, using `pdflatex -interaction=nonstopmode -halt-on-error wrap.tex`.
  The initial two passes succeeded; two later passes verified the final
  source after the last changes and stabilized references. The final
  wrapper has 43 pages, zero TeX errors, zero overfull boxes and no
  oversized-float warning. External labels and citations are deliberately
  unresolved because the wrapper omits other chapters and bibliography.
- Ran `python3 /tmp/sparse-sol-final-check/check_owned.py`: owned-file
  final newlines, trailing whitespace, balanced environments, label
  uniqueness at the owned interface, reference resolution against the live
  chapter label catalog, report format and final source fingerprints.
  The chapter catalog is read only to resolve this block's references; it
  is not a project-wide verification run.

No full-manuscript build, project-wide check, CI inspection, optimization
experiment, saved proof-diagnostic rerun, literature search, delegation,
commit or publication was performed. Historical evidence was not edited.

One source-contract item remains for the root and Luna: verify the exact
condition-parameter normalization, growth hypotheses, work/output theorem
locators, graded/uniform grid comparison and rETH statement of
`companion-decomposition-aware`. The final submission text deliberately
uses a conservative single-parameter comparison based on the supplied
editorial finding; it does not retain the interrupted draft's unverified
`bar-kappa` versus Euclidean `kappa` distinction or its asserted companion
upper exponent `p/2+O(1)`. The root should reconcile this passage with the
final source audit before submission. Existing classical citation identities
and exact locators, including GLS and refined Bezout, remain with Luna's
bibliography audit. This pending source check does not change the proved
conditional count or domain repairs.

Final submission-file SHA256 fingerprints:

| File | Lines | SHA256 |
| --- | ---: | --- |
| `sections/05-sparse.tex` | 1132 | `9f1d5eb4404dda9c5943cedff0d640784a3458e57a138b776366976eb97ceffe` |
| `sections/06-constraints.tex` | 818 | `9467eb72e20f355b3afb70d844bfedcf0a7fe52ba8f53d2483327162ad9db898` |
| `appendices/C-sparse.tex` | 278 | `a93e0493bd253e24e72b5fa1d903f360f8422a84222ec04d80eed069ca9b2974` |
| `appendices/D-constraints.tex` | 1080 | `c0b90de5054e469a278c2d09f560ce39a746c5b1025c79ecf4aee75ca0f4e66b` |
