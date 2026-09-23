# Stage 3 correction pass

Implemented all four minor presentation improvements accepted in `stage3-round1-adjudication.md`. Only `sections/04-structural-algorithms.tex` and `sections/05-contract-algorithms.tex` were changed. The theorem statements and their scopes are unchanged. I read the adjudication, the relevant reviewer 2 and reviewer 4 findings, and the original statements and proof passages needed to check each edit. No delegation or literature modification was needed.

| Accepted item | Final source location and change |
| --- | --- |
| 1. Fixed-parameter wording | Section 4, line 437: replaced “fixed-parameter statements” with “polynomial-time results with fixed parameters.” The earlier explicit exclusion of a fixed-parameter runtime bound remains. |
| 2. Physical scope table | Section 5, lines 35–99: added Table 2 (`s5:scope-table`) with five physical classifications, precise contract and exception conditions, bypass degree, common pool bounds, objective scope, and common-field witnesses. The legend defines exact contracts, exceptions, bypass degree, economics, throughput, field degree, and the common-bound terminology. The supplementary paragraph distinguishes the fixed-rank exception corollary from the arbitrary-rank theorem and explains designated extra arc costs and the two-vector resource extension. |
| 3. Unary identity | Section 5, lines 1125–1141: defined the fixed membership indicators and minimizing binary labels, repeated the outgoing-minus-incoming divergence convention, and displayed the full directed-cut plus unary energy as equation (98), `s5:rank-energy`. The following sentence derives its node terms directly from the box rank. |
| 4. Projection orientation | Section 5, lines 105–108: explained that later polynomial physical results use additional conservation or strip structure, or the separate two-vector convex reduction. The general planar parameter result remains explicitly quasipolynomial. |

The scope table was checked against `s5:fixed-products`, `s5:quadratic-field`, the exception-model assumptions and `s5:fixed-rank` / `s5:arbitrary-exceptions`, `s5:restrictive-capacity` / `s5:throughput-optimization`, and `s5:two-vector-theorem` / `s5:two-vector-extensions`. The restrictive-common-bound row has a polynomial-degree field guarantee and explicitly has no constant field-degree assertion. The two-vector row retains exact product demand and quality, allows source intervals and arbitrary bypass topology, requires zero outlet and common pool lower bounds, and claims feasibility only. Polynomial time refers to bit complexity for fixed stated parameters. No dense arc-cost optimization claim was introduced.

For the new identity, write `d_v = div(ell)_v`. The box-rank node contribution before collecting terms is

`d_v t_v + beta_v s_v (1-t_v) - alpha_v t_v (1-s_v)`.

Collecting the coefficient of `t_v` gives the displayed expression exactly. Its values at `(s_v,t_v) = (0,0), (1,0), (0,1), (1,1)` are respectively `0`, `beta_v`, `d_v-alpha_v`, and `d_v`. The lower-bound shift of the cut function contributes `sum_v d_v t_v`; the remaining directed cut has edge contribution `(u_e-ell_e)t_v(1-t_w)` and nonnegative capacity. Thus the invocation of the binary path/cycle lemma preserves quadratic parameter degree. This direct algebraic check is sufficient for the presentation edit; no duplicate numerical suite was added.

Validation used an isolated source copy under `checks/stage3-corrections-build/`. `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` succeeded and produced a 97-page PDF. The final source copies match both edited manuscript files. The final TeX log has no errors, warnings, undefined references/citations, or overfull boxes. It has eight underfull boxes, all in the unchanged bibliography. BibTeX retains the two empty-year warnings for `s6:boveroux2026` and `s6:lrs-full`.

I rendered and inspected final Table 2 on PDF p.62 and equation (98) on p.76. The table fits within the text width on one page; its final larger font and ragged columns avoid the extra underfull warning in the first layout. The equation and its explanatory text are readable and fit without overflow. The table references, legend, and projection orientation remain consistent in the rendered output. The shared `papers/pooling/main.pdf` was not overwritten; its before/after SHA256 is `73b0c7a541309186c9ae4df671c5462d0e18d302ed3694c3480af859131746b1`.

Evidence is in `checks/stage3-corrections/`: pre-edit section copies, `correction.diff`, `validation.json`, extracted PDF text, `table-page62.png`, and `unary-page76.png`. The isolated build retains the PDF, source, logs, and final build console output. No accepted item remains unresolved.
