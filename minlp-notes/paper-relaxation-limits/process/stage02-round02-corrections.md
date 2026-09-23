# Stage 2, round 2: corrections

Accepted finding R15-M1 (MINOR) is addressed in `sections/appendix-cubic-certificates.tex`, immediately before the first checker minipage. The exact manuscript diff is:

```diff
@@ -114,7 +114,7 @@
 optimization or proprietary solver is involved. The same executable text
 is supplied as \texttt{verification/check\_stage02\_finite.py}.
 Concatenate the two code blocks in order to obtain that file.
-\par\noindent\begin{minipage}{\textwidth}\small
+\par\medskip\noindent\begin{minipage}{\textwidth}\small
 \begin{verbatim}
 from fractions import Fraction as Q
 from itertools import product
```

Before editing, the appendix was verified byte-for-byte against the frozen Stage 2, round 2 snapshot. Removing the single added `\medskip` from the corrected file reproduces that baseline exactly. All mathematics and both verbatim blocks are unchanged. Their byte counts and SHA-256 hashes are:

| Block | Bytes | SHA-256 |
| --- | ---: | --- |
| First | 776 | `f9d14e67f818dea34b32043279ac6fe4bad319f5062729518084a165cb447c09` |
| Second | 2107 | `4863f4ff62149eed91903459c117c7812ba6ee8b41d9a1fdac2ca57ae32180b7` |

Verification: `python verification/build_and_check.py`, run from `paper-relaxation-limits`, exited with status 0. Compilation produced 33 pages, no warnings, no duplicate labels, and confirmed that the concatenated printed checker exactly matches `verification/check_stage02_finite.py`. The live PDF SHA-256 is `fd7a4f7c9dce1e26547fdcefe78a9252255d7a80d22daab1dfba19e64da17118`. The script refreshed the live build output, report, and extracted manuscript text.

PDF page 31 was rendered with `pdftoppm -f 31 -l 31 -singlefile -scale-to 1800 -png` and visually inspected against the same page of the frozen round 2 PDF. The added space separates the final prose line from the first code line. The complete first code block remains on page 31 with no clipping or overlap. Inspection renders are `/tmp/stage02-round02-page31-before.png` and `/tmp/stage02-round02-page31-after.png`.

No other manuscript content, frozen snapshots, repository source code, or literature was edited. Root's final verification and Stage 2 acceptance decision remain pending.
