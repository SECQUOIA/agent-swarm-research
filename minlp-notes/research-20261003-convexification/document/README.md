# Joint convexification: exact support and checked integration

The report joins exact support, positive-tolerance separation, safe
original-variable cuts, model-domain preservation, and prospective solver
evaluation. The first continuation's mathematical foundations are restated
with attribution; its experiments remain separate historical evidence.

Read the [completed report](main.pdf) or its [source](main.tex).
[COVERAGE.md](COVERAGE.md) maps each claim to its proof, implementation,
and independent evidence; [VERIFICATION.md](VERIFICATION.md) records the
targeted checks. The documented development program is complete: it includes
exact quadratic support on bounded rational polytopes, complete separation
to any positive rational tolerance for polynomial graphs, source-domain
preservation, original-variable cut integration, and evaluated implementations.

The new 30-model holdout produced the same 25 solves in all three modes,
with more aggregate time in both cut modes. Native SCIP remains the default.
A separate 75-job matched validation confirmed the discovery repair without
adding solves. Across the two new cohorts, 357 runs produced 165 recorded
cuts that all replayed and 338 returned incumbents that passed numerical
checks. Four original failed-worker cut logs remain unknown and are excluded
from the cut claims. The repair cohort does not replace the original holdout.

Build only this report from the repository root:

```sh
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error \
  research-20261003-convexification/document/main.tex
```

The bibliography includes the previous continuation's references and the
new primary-source audit. The complete separator has explicit, potentially
exponential cost; the solver callback uses bounded work and can return
incomplete. Joint graph closure need not equal the feasible-set hull, and
a cut certificate does not certify SCIP's complete solve. Exact support,
complete tolerance separation, and useful solver performance are separate
results. The reviews are internal checks, not external peer review or formal
verification.
