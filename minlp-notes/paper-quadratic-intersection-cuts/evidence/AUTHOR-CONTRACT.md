# Shared notation and file ownership

Read `BRIEF.md` before writing. Mathematical correctness takes precedence over
this provisional allocation. Explain any required change to the lead.

## Notation

- Work in the constraint space `s` with vertex `\sbar`, projected ray matrix
  `P=[p_1,...,p_N]`, and nonnegative ray coordinates `\lambda`.
- Reduced costs are `\rc=\omega`, with components `\omega_j`. This avoids
  confusing objective weights with the bilinear coordinate `w`.
- `X={\lambda\ge0:\sbar+P\lambda\in S}` and
  `\zK(\rc)=\inf_{\lambda\in X}\rc^T\lambda`.
- The corner-hull dominant is `\mathcal D=\cl(\conv X+\R_+^N)`.
  Reserve the letter `D` without a calligraphic font for scaled vertex depth.
- `\alpha_j(C)` is the ray step, `a_j(C)=1/\alpha_j(C)`, and
  `z_C(\rc)=\min_{j:a_j>0}\omega_j\alpha_j(C)`.
- Bilinear coordinates are `s=(x,y,w)`, `q(s)=w-xy`,
  `S={q\le0}`, `M(s)=\begin{pmatrix}w&x\\y&1\end{pmatrix}`,
  and `M_0(p)=\begin{pmatrix}p_w&p_x\\p_y&0\end{pmatrix}`.
- `C_F={s:\sym(F^TM(s))\succeq0}` for `\det F>0`.
  Family A contains these orbit sets; family B contains their closed upward
  completions along `e_w`. Do not assert every completion is maximal without
  treating the exceptional parameter. Family BP is the completed point-rule
  family under all relevant determinant-preserving transformations; it is not
  merely a permutation family.
- Family macros are `\famA`, `\famB`, `\famBP`; one-cut value macros are
  `\zA`, `\zB`, `\zBP`. Distinguish closure values explicitly as
  `z_{\mathrm{cl},\famA}` and analogous terms.
- `D=\sqrt{\max_j|\widetilde p_{jx}|\max_j|\widetilde p_{jy}|/q(\sbar)}`,
  with `\widetilde p_j=(\zK/\omega_j)p_j`.
  `\kappa` denotes the ray condition number only; SCIP's source constant is
  `\kappa_{\mathrm{SCIP}}`.
- Use the shared macros in `macros.tex`. Do not add packages or redefine macros
  locally; tell the lead about needed additions.

## File ownership

| Author | Main text | Proof appendices | Label prefix |
| --- | --- | --- | --- |
| foundations | `sections/02-corners.tex`, `sections/03-quadratic-geometry.tex` | `appendices/A-foundations.tex` | `fd:` |
| depth | `sections/04-depth.tex` | `appendices/B-depth.tex` | `dp:` |
| closures | `sections/05-closures.tex` | `appendices/C-closures.tex` | `cl:` |
| minors/convergence | `sections/06-minors.tex`, `sections/07-repeated-cuts.tex` | `appendices/D-minors.tex`, `appendices/E-convergence.tex` | `mi:`, `cv:` |
| computation | `sections/08-computation.tex` | `appendices/F-evidence.tex` | `exp:` |
| lead | abstract, introduction, discussion, integration and delivery | — | `intro:`, `disc:` |
| literature (GPT Luna max) | bibliography and literature audit | — | — |

Each author also owns its audit and author report in `evidence/`. No author
edits another author's files, the bibliography, or the existing research notes.

Use proof labels and semantic `\cref` references. State complete hypotheses.
Place the main conceptual proof steps near their statements and technical
certificate details in appendices. Every substantive source theorem needs a
final disposition in the author report. Cite established results normally;
the root will reconcile bibliography keys with the sole literature lead.

The paper is written for optimization researchers, not for the development
agents. Do not include session history, agent reviews, process-stage language,
repository-absolute paths, claim-inventory IDs, or claims that finite checks
prove an asymptotic theorem. Bibliographic and proof caveats should describe
the mathematics or evidence directly.
