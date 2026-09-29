# Calibration, perturbation and integrated-manuscript validation

The baseline is the accepted upper-bound commit `1d48cd06`. This stage adds
Sections 6–8, completes the abstract and introduction, updates the coverage
map and bibliography, and adds the exact calibration/perturbation checker.
The mathematical additions include a concrete infinite-threshold grid atom,
which resolves the earlier expected-encoding qualification.

The following targeted commands were run from `paper-exact-penalties/`:

```sh
python3 verification/check_lower_bound.py
python3 verification/check_upper_bound.py
python3 verification/check_calibration_perturbation.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
pdftotext -layout main.pdf verification/main-text.txt
git diff --check -- .
```

All three manuscript checkers passed. The new standard-library Fraction
checker independently evaluates balanced mixtures for 660 binary-box and
300 unit-data graph dual cases. It also checks 180 clipped-fiber cases,
240 centered/endpoint-grid configurations, 44 deterministic-margin cases,
167 tail/two-slice/adjacent-mixture cases, and 5 rational witnesses for the
infinite-threshold atom. The outputs are retained in `verification/`.
The earlier lower-bound and upper-bound checkers retain their documented
scopes and limitations; the upper-bound checker uses SymPy 1.14.0.

The new checker does not validate complexity reductions for all inputs,
all-dimensional convex geometry, Gaussian probabilities, or novelty. The
proofs supply those quantified arguments, relying explicitly on the cited
Gaussian tube lemma and the standard NP-complete starting problems.

The initial integrated manuscript built to 21 pages; the final localized
revision below builds to 22 pages. The final log has no unresolved
references or citations, TeX errors, or underfull/overfull boxes. Extracted
text was inspected for equation order and reading continuity in the new
sections and integrated abstract/introduction. A targeted source check
confirmed no trailing whitespace and no unresolved coverage rows or
missing explicitly named repository sources. The author field remains empty.
No project-wide checks, CI inspection, solver study or new Lean run was
performed. The lead will record the independent final review separately.

## Final localized revision

After the complete independent reviews, the writer applied the lead's
accepted local corrections: explicit equality-feasible refined Slater and
box assumptions, the linear-constraint antecedents of conservative output,
the fixed-zero-multiplier calibration consequence, precise Gibbs-sampling
wording, direct and contextual primary citations, notation/coverage fixes,
and the restricted finite-grid tail statement. No theorem or proof error
was reported by those reviews. The lead records their adjudication separately.

The affected checkers were rerun with output saved by these commands:

```sh
python3 verification/check_upper_bound.py > verification/upper-bound-results.txt
python3 verification/check_calibration_perturbation.py > verification/calibration-perturbation-results.txt
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex > verification/final-revision-build.log
pdftotext -layout main.pdf verification/main-text.txt
pdfinfo main.pdf
pdftoppm -f 14 -l 14 -scale-to 1400 -png -singlefile main.pdf evidence/reviews/final-writer-rendered/calibration
pdftoppm -f 18 -l 18 -scale-to 1400 -png -singlefile main.pdf evidence/reviews/final-writer-rendered/tails
git diff --check -- .
```

Both checkers pass. In addition to its previous determinant and singular
regularization checks, the upper-bound script tests 31 two-coordinate
reciprocal-graph candidates, including zero, negative values, reciprocals
of smaller residual coordinates, and a point with one zero coordinate.
It checks equivalence of the stated graph inequalities and saturation to
the reciprocal infinity norm, rather than merely substituting a correct
reciprocal.

The calibration/perturbation script passes 660 binary-box dual cases,
300 graph dual cases, 165 fixed-zero-multiplier threshold cases,
180 clipped-fiber cases, 240 original centered/endpoint-grid cases,
18 finer configurations with probability upper bounds below one,
3 exact atomic-correction cases computed using boundary distance,
44 deterministic-margin cases, 167 continuous-tail/two-slice/adjacent-mixture
cases, 24 finite-grid tail cases and 5 infinite-threshold witnesses.
The exceptional zero atom belongs to the concrete centered grid with
q=17, b0=0, sigma=1; the script checks q >= 4mK/epsilon for
m=1, K=2, epsilon=1/2, so the grid satisfies the theorem's resolution
requirement while its exceptional atom has probability 1/17.

The revised PDF has 22 pages. A direct log assertion found no LaTeX
warnings, undefined references/citations, or underfull/overfull boxes.
The extracted text was inspected around the changed equations and
assumptions, and rendered pages 14 and 18 were visually inspected for the
new calibration and finite-grid-tail paragraphs. A proposed PyMuPDF
text-boundary check could not run because that optional module is absent;
the available Poppler tools supplied the extraction and rendering instead.
The source-whitespace and git diff checks pass. The lower-bound checker
was unchanged and was not rerun during this final correction pass; its
earlier successful result above remains applicable. No project-wide
verification or CI inspection was performed.
