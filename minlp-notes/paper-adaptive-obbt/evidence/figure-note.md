# Analytic rate figure

`figures/rates.pdf` is a vector figure sized 6.4 by 2.7 inches. The optional
`figures/rates.svg` contains the same figure. Regenerate both from the repository
root with:

```sh
python3 paper-adaptive-obbt/figures/rates.py
```

The self-contained script requires NumPy and Matplotlib, uses 10-point serif
text and mathtext, and needs no LaTeX installation. All curves use grayscale
line styles; the complete-graph curves also have distinct marker shapes.
The sampled values come directly from the displayed analytic formulas.
No solver, archived computational data, or computational experiment is used.

## Suggested exact caption

```tex
Analytic Jacobi factors at $U=f^*=0$ for termwise McCormick relaxations
with exact square terms. (a) For $f=x^2+y^2+axy$, the exact cube factor
$\rho(a)$ is below one for $0<a<2$
(Proposition~\ref{prop:two-variable-rate}). The scalar quadratic-growth
bound with $\mu=1-a^2/4$ and $\tau=a/4$ gives
$q(a)=\sqrt{a/(1-a^2/4)}$; its sufficient condition $q<1$ holds only for
$a<2\sqrt{2}-2$ (Proposition~\ref{prop:quadratic-growth}). The scalar curve
is shown through $q=1.6$. (b) For
$f=\sum_i x_i^2+a\sum_{i<j}x_ix_j$, $n\ge3$, the exact cube factor
$\min\{1,t_n(a)\}$ reaches one at $a=2/[(n-1)(n-2)]$
(Example~\ref{ex:many-term}). Markers identify the thresholds $1$, $1/3$,
and $1/10$ for $n=3,4,6$. All objectives are strongly convex for $0<a<2$;
the plateaus denote fixed cubes at every scale. Endpoints show continuous
limits.
```

The figure can be included as `\includegraphics[width=\linewidth]{figures/rates}`.
The manuscript integration and `graphicx` package are outside this figure task.

## Source support and analytic checks

- `sections/local-rates.tex`, `prop:two-variable-rate`, supplies
  `rho(a) = (sqrt(2*a^2 + 4*a) - a)/2` for positive `a`. Its exact per-round
  interpretation applies to centered cubes under Jacobi updates at zero cutoff
  slack. The plot makes no claim about successive ratios from arbitrary boxes.
- `prop:quadratic-growth` supplies `q^2 = 4*tau/mu`. The plotted general-`a`
  expression is a direct specialization, rather than a separately displayed
  formula in the source. Completing the square gives
  `f = (y+a*x/2)^2 + (1-a^2/4)*x^2`, and symmetry gives
  `f >= (1-a^2/4)*max(|x|,|y|)^2`. The bilinear McCormick gap is at most
  `a*w_x*w_y/4 <= (a/4)*w(B)^2`. Thus `mu=1-a^2/4` and `tau=a/4` are valid
  constants. Solving `q^2<1` gives `a^2+4*a-4<0`, hence the marked positive
  threshold `2*sqrt(2)-2`. Failure of this sufficient condition is not stalling.
- `ex:many-term` supplies
  `t_n(a) = (sqrt(a^2*(n-1)^2 + 2*a*n*(n-1)) - a*(n-1))/2`, and the exact
  centered-cube factor `min(1,t_n(a))`. Its positive-root polynomial at `t=1`
  is `1-a*(n-1)*(n-2)/2`, giving the three exact thresholds. The formula is
  used only for `n>=3`; the script rejects `n<3`.
- The same example supplies Hessian eigenvalues `2-a` and `2+a*(n-1)`, both
  positive on the open plotted parameter interval. The termwise relaxation
  remains essential: the figure does not describe a solver that keeps the
  original convex quadratic whole.

This figure visualizes existing manuscript results and their scalar-bound
specialization; it introduces no new scientific result.

## Targeted verification

The following local commands were run successfully:

```sh
python3 paper-adaptive-obbt/figures/rates.py
pdftoppm -singlefile -png -r 180 paper-adaptive-obbt/figures/rates.pdf /tmp/analytic-obbt-rates-review
pdfinfo paper-adaptive-obbt/figures/rates.pdf
pdffonts paper-adaptive-obbt/figures/rates.pdf
```

The script checks the endpoint limits, `q=1` threshold, displayed scalar cutoff,
and exact complete-graph threshold identities, including values on each side
of every threshold. The PDF has one page measuring 460.8 by 194.4 points and
contains embedded TrueType serif/math fonts. The rendered PDF was inspected:
axis labels, threshold labels, legends, and panel labels are readable and
unclipped. These are targeted local checks; no project-wide verification or
CI status/log inspection was performed.

With NumPy 2.5.1 and Matplotlib 3.11.1, a second generation produced
byte-identical PDF and SVG files. The comparison command was:

```sh
python3 - <<'PY'
from hashlib import sha256
from pathlib import Path
import subprocess

script = Path('paper-adaptive-obbt/figures/rates.py')
outputs = [script.with_suffix('.pdf'), script.with_suffix('.svg')]
before = [sha256(path.read_bytes()).hexdigest() for path in outputs]
result = subprocess.run(['python3', str(script)], check=True, capture_output=True, text=True)
after = [sha256(path.read_bytes()).hexdigest() for path in outputs]
assert before == after
print('PDF and SVG regeneration is byte-identical.')
print(result.stdout.strip())
PY
```
