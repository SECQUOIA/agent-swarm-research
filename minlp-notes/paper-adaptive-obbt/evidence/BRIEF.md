# Adaptive OBBT manuscript brief

## Deliverable and scope

Develop an anonymous, self-contained journal manuscript on adaptive and iterated
optimization-based bound tightening (OBBT). Main writing uses Claude Opus;
independent reviews use Opus and GPT Sol. Literature research uses GPT Luna at
maximum reasoning with the single reusable `$lit` lead. Do not rerun numerical
experiments. Existing results may be trusted; check their transcription and
interpretation. Analytic proof work and narrow exact-arithmetic checks are allowed.

The manuscript is rooted at `/workspace/minlp-notes/paper-adaptive-obbt/`.
Read `/workspace/minlp-notes/AGENTS.md`. Only targeted checks are permitted;
do not inspect CI. Preserve the existing research reports and evidence.

Primary inputs are the complete October study at
`/workspace/minlp-notes/research-20261003-adaptive-obbt/` and its September
antecedent at `/workspace/minlp-notes/research-20260922/iterated-obbt/`.
Cover their substantive mathematical developments coherently, not merely the
October report's selected summaries. State useful results fully, prove them,
repair errors, and develop any material missing steps. Remove claims that cannot
be justified. Ordinary research extensions need not be solved to make a complete
paper; do not list substantive missing proof obligations as future work.

## Shared mathematical language

Use the projected relaxed objective `\phi_B` of the existing reports. Let
`B=[\ell,u]`, `K_U(B)={x in B: \phi_B(x)<=U}`, and
`T_U(B)=\operatorname{box} K_U(B)`. Validity and monotonicity of the WHOLE
relaxation construction must be explicit. Assume compactness of the projected
sublevel sets when supports are attained. Distinguish frozen Jacobi rounds from
sequential coordinate updates. Set `w(B)=max_i(u_i-\ell_i)` and
`\epsilon=U-f^*`. Use `p=(-\ell,u)` for endpoint comparisons. A finite witness
pool uses `W`; its protected coordinate hull uses `P`. Lifted witnesses must
include every coordinate and satisfy the same lifted rows and objective.
Any result needing stronger assumptions must state them locally.

Use stable labels with prefixes `sec:`, `thm:`, `prop:`, `lem:`, `cor:`, `ex:`,
`eq:`, `tab:`. The lead establishes the shared preamble; section authors should
use standard amsmath/amsthm commands and specify any extra macros in their report.
Use `\R`, `\norm{...}`, `\hull`, `\dist`, `\diam`, `\supp`, `\conv` if needed.

## Planned structure and file ownership

1. `sections/introduction.tex`, `sections/related.tex`, `sections/foundations.tex`,
   `sections/local-rates.tex`, `sections/discussion.tex`, and `abstract.tex`:
   lead/front-and-rates Opus writer. Own `main.tex` initially. Explain the
   problem, contributions, uses, relationship between rates and certificates,
   and the significance of the empirical finding. Related work must follow the
   Luna source audit; do not invent priority claims.
2. `sections/certificates.tex`, `sections/cutoff.tex`,
   `sections/residual.tex`: certificate Opus writer. Include current-round and
   future-round distinctions, finite protected-box certificates, objective
   ceilings, cutoff adaptation/frontiers, integer-rounding scope, and matrix
   residual certificates. Supply constructive examples and all proofs.
3. `sections/constraints.tex`: constrained-theory Opus writer. Include fixed
   matrix dual information, exact parametric support regions, complete region
   coverage, sensitivity matrices, nonlinear feasible repair and fully worked
   example. Connect these results to the certificates and local rate analysis.
4. `sections/algorithms.tex`, `sections/effort.tex`, `sections/experiments.tex`:
   algorithms-and-evidence Opus writer. Include exact proof-backed workflow,
   numerical bound-validation formulas, practical policy, cost accounting and
   independent-baseline results. Describe archived experimental methods and
   results accurately, including the earlier preprocessing study when useful.

Independent Sol auditors own only their assigned files in `evidence/`. They may
propose corrected statements and full proofs there. Writers must not edit each
other's assigned files. The root integrates files and resolves review findings.

The sole Luna literature lead owns KB maintenance and writes
`evidence/literature-audit.md` and `evidence/literature-references.bib`; root
copies vetted entries to the paper bibliography. All newly needed sources must
be added to the repository's ignored `/workspace/minlp-notes/literature/`
via `$lit` at `/workspace/local-home/repo/skills/literature/SKILL.md`. Other agents should
write source requests in their author/audit reports, not run literature searches.

## Writing and scientific standards

Write for a MINLP/global-optimization expert who has not read the repository.
Use plain, direct prose, consistent established terms, focused sentences, and
complete reasoning. Each theorem needs motivation, precise assumptions, a proof,
and an explanation of use and scope. Define nonstandard terms before use.
Provide examples that distinguish otherwise easy-to-confuse claims. Avoid
promotional adjectives, boilerplate transitions, invented compound labels,
LLM filler, and repetitive warnings. A journal paper should not discuss agent
reviews, workstreams, task completion, repository process, or 'the continuation'.

Clearly separate established ingredients from the exact original formulation
supported by the source comparison. Do not portray classical weak duality,
feasibility filtering, fixed-point reasoning, contraction principles, or
parametric LP as new. Absence from a limited search is not proof of priority.
State qualified novelty only for an exact result with a supported comparison.

The empirical policy does NOT implement the stronger all-future protected-box
or matrix-tail machinery. The 120-run study found fewer LPs, no additional
solves, and no demonstrated total speedup. Explain why that finding matters.
Do not use short shared-machine timings to assert statistically established
slowdown. Numerical incumbents and SCIP output are not exact MINLP certificates.

Authors should leave no TODOs, placeholders, incomplete proofs, unsupported
citations, private-path links, or references to evidence files as substitutes for
mathematical explanations. State source and data availability only for artifacts
that are actually packaged. Submission sources must compile independently.

Write an author report in `evidence/author-<lane>.md` recording corrections,
developments beyond transcription, citation needs, and verification actually run.
