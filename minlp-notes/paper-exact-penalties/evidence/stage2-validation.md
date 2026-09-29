# Encoding upper-bound validation

The stage adds the general continuous-dimension encoding bound, the fixed
nonlinear-count bound, and polynomial-time output of a conservative
sufficient coefficient for fixed continuous dimension or fixed nonlinear
count. Its baseline is the accepted geometry/lower-bound commit `fd646f01`.

Targeted commands run from `paper-exact-penalties/`:

```sh
python3 verification/check_upper_bound.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
pdftotext -layout main.pdf verification/main-text.txt
```

The symbolic script passed with SymPy 1.14.0. It checks a two-dimensional
singular-objective-Hessian example: adjugate stationarity, both constraint
numerators, the objective numerator and all displayed degree bounds. A
separate exact family has no unperturbed Slater point, a singular objective
Hessian and multipliers diverging as the regularization goes to zero; six
rational scales satisfy its KKT certificate, and symbolic limits verify the
objective and multiplier behavior. Three reciprocal-graph points provide a
small arithmetic check of that distinct construction. Results are in
`verification/upper-bound-results.txt`.

These are finite symbolic regression checks. They do not prove general
algebraic radius or height bounds, verify quantifier elimination, or test
unknown asymptotic constants. The manuscript supplies the general reduction
and cites the algebraic theorems explicitly. The source audit is recorded in
`evidence/stage2-sources.md`.

The cumulative manuscript builds to 13 pages with no undefined references,
undefined citations, TeX errors or overfull/underfull boxes. Targeted checks
also confirmed source whitespace and explicit coverage/source paths.
The new sections' extracted text was inspected for readable equation and
paragraph order. No project-wide verification, CI inspection, solver study
or new Lean run was performed.

After the full stage review, the modified upper-bound script was rerun. It
now computes the regularized objective from the proposed primal coordinates,
checks its signed value identity, and verifies the actual relaxed constraints,
multiplier signs and complementarity at all six rational scales. It derives
stationarity and the Hessian directly from the Lagrangian. The modified check
and rebuilt 13-page PDF passed. The final build log again has no unresolved
references/citations, TeX errors or underfull/overfull boxes.

The targeted commands for these localized corrections were:

```sh
python3 verification/check_upper_bound.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
pdftotext -layout main.pdf verification/main-text.txt
git diff --check -- .
```
