# Moves from Section 5 (`sections/05-other.tex`) to the supplement

Key: m-other. Written 2026-10-04 during the main-text revision of Section 5.

Section 5 was cut from about 13 pages to about 8.6 pages. Almost everything
that was cut already exists in the supplement (B3, B5, B6, B7, B9, F, D).
This file lists the items that do not, and the supplement references that
the cut breaks. Items 1 and 2 are required: without them the supplement
has undefined references. Items 3 to 5 are recommended additions. Item 6
lists consistency fixes for supplement text that refers to Section 5.

All LaTeX below is ready to paste. Figures are in `figures/`, which both
documents find through `\graphicspath{{figures/}}` in `preamble.tex`.

---

## 1. REQUIRED: Figure `fig:eg-enclosures` to `sections/B7-eg.tex`

`B7-eg.tex` references `\cref{fig:eg-enclosures}` once (line ~347,
"(\cref{fig:eg-enclosures}a)"). The figure used to be in Section 5.5 and was removed from the main
text (it shows numerical evidence, not part of any proof). Paste it at the
end of the paragraph "Evidence about the method" in B7, after the sentence
that ends "... for the natural enclosure of \cref{lem:eg-natural} alone,
which sums term ranges." (just before `\subsubsection{Exactly feasible points}`):

```latex
\begin{figure}[t]
\centering
\includegraphics[width=\textwidth]{fig-eg-enclosures.pdf}
\caption{(a) Median gap between the sampled minimum of a row over a box and three lower bounds, against relative box width, over 64 boxes and 24 rows of \inst{eg_int_s} (numerical evidence). (b) Cancellation at the \inst{eg_int_s} optimum: sum of absolute values of the 97 kernel terms against the absolute value of their sum, for the active objective row e12 and the Gaussian part of the active side row e26.}
\label{fig:eg-enclosures}
\end{figure}
```

Caption text is unchanged from the previous main-text version. Source of the
numbers: B7 "Evidence about the method" (ratios 3.2/19/15/7.1/2.9 and
3.2/44/112/146/151) and B7 line ~65 (61.4 against 7.115; 78.4 against 0.0829).

---

## 2. REQUIRED: Box `box:kan-example` to `sections/B9-ann-kan.tex`

`B9-ann-kan.tex` line ~241 references `\cref{box:kan-example}`. The box was
in Section 5.5 and was moved out to meet the page target. Section 5 now
points to `\cref{app:annkan-kan-infeasible}` for this worked example.
Paste the box in B9 directly after the proof of `prop:kan-infeasible`
(after `\end{proof}`, before the paragraph "For \inst{kan_r5_h1_n3} and
edge \texttt{x776}, \cref{box:kan-example} works out ..."):

```latex
\begin{infobox}[label={box:kan-example}]{Exact infeasibility of \inst{kan_r5_h1_n3}}
Take the edge with argument $z=x_{776}$ and its knot interval that allows $z\in[-0.5857759315175706,-0.0040155389917946]$.
With the binary of that interval equal to 1, the Cox--de Boor rows e48 and e49 give $x_{221}=-0.006902393224744528-1.718920732397047\,z$ and $x_{222}=1.0069023932247445+1.718920732397047\,z$, and the other degree-1 basis variables of the edge vanish.
The partition row e77 requires $x_{221}+x_{222}=1$, but the sum is $1.0069023932247445-0.006902393224744528=1-2.8\cdot10^{-17}$ for every $z$.
On three further admissible intervals the degree-1 residual is again a nonzero constant; on the remaining two, the degree-3 residual has no root in the interval (Sturm count), or the degree-2 and degree-3 residuals have no common root.
\end{infobox}
```

Text unchanged from the previous main-text version (dossier: ann-kan.md;
B9 line ~241 gives the same residual $-2.8\cdot10^{-17}$ and the interval
\texttt{b6}). If the supplement editor prefers no box in the supplement, the
alternative is to delete "`\cref{box:kan-example}` works out the interval of
\texttt{b6}, where" in B9 line ~241 and keep the paragraph as prose; then the
box text above is not needed, because B9 already states the residual.

---

## 3. RECOMMENDED: Figure `fig:camshape-profiles` to `sections/B3-camshape.tex`

The camshape profile figure was removed from Section 5.1. No reference to
it remains in either document, and B3's `tab:camshape-values` already holds
every number in the caption (contact phases 1--64 and 1--513; $E_j=2$ for
the last 6 and 51 radii). Paste after `tab:camshape-values` (after the
paragraph that starts "For $0 < c < 2$, $S_j = A\cos(j\varphi)+\dots$"):

```latex
\begin{figure}[t]
\centering
\includegraphics[width=\textwidth]{fig-camshape-profiles.pdf}
\caption{Optimal radii $E_j$ of \inst{camshape100} and \inst{camshape800} against the angle $j\,\Delta\theta$, with the comparison line $R_j=1/S_j$ (dashed) and the cap $r=2$ (dotted). Phases: contact ($E_j=R_j$; $j\le64$ and $j\le513$), maximal slope (shaded) and $r=2$ (the last 6 and 51 radii). Drawn from the OSIL constants; the certified values are those of \cref{thm:camshape-opt}.}
\label{fig:camshape-profiles}
\end{figure}
```

and add "(\cref{fig:camshape-profiles})" at the end of the sentence "The
exact computation shows the three phases of \cref{tab:camshape-values}: ...".

---

## 4. RECOMMENDED: Lavaei remark to `sections/B6-powerflow.tex`

Cut from the Section 5.3 literature paragraph; it is not in B6 or D.
No claim depends on it (it is a remark on prior work). Paste in B6,
paragraph "Relation to prior work", after its first sentence:

```latex
\citet{lavaei2012-zero-duality-gap-in-optimal} note that zero-resistance transformers violate their exactness condition; the branch 2--30 at which the 39-bus certificates need the leaf cut is such a transformer.
```

Source: previous Section 5.3 text ("Lavaei and Low note that zero-resistance
transformers violate their exactness condition; the defect here sits on such
a branch"); B6 "Leaf data" (branch 2--30 has $r=0$).

---

## 5. RECOMMENDED: hvycrash tolerance remark to `sections/B5-small.tex`

Section 5.4 keeps only the explanation of the listed points p1 and p2. The
general statement below was cut. Paste in B5, `rem:hvycrash-tolerance`,
before "In the other direction, the COCONUT record ...":

```latex
Conversely, under a positive tolerance a stage can be dropped by letting $r_k\to\infty$: then $\text{alg}_k$ and $\text{dyn}_k$ hold approximately and the increment of $s$ vanishes, so tolerance-feasible points can reach values near $-0.2185+jh$ for $j=1,\dots,50$.
```

Source: previous Section 5.4 text; numbers.json / small dossier (p1, p2 with
$r_{50}$ of order $10^7$ and $10^9$ and objective $-0.21413=-0.2185+h$).

---

## 6. Consistency notes for supplement text that refers to Section 5

- **Certificate boxes for class E.** Section 5.5 no longer has certificate
  boxes for `thm:eg-bounds`, `thm:ann-bound`, `prop:kan-infeasible` and
  `thm:kan-enclosure`; it points to the supplement's boxes in
  `app:egrounding-trust` (F), `app:annkan-ann-verif` and
  `app:annkan-kan-enclosure` (B9). These boxes must stay complete (inputs
  with SHA-256 prefixes, computation and arithmetic, implementations,
  evidence level, replay).
- **ANN replay time (numbers-check item 14).** B9 lines ~155 and ~170 say the
  re-certification takes "about 2.6 CPU-hours". The recorded reproduction
  run (`R/publication/reproduction/network/logs/ann.verify_*.time`) took
  1,159 + 5,234 + 924 s = 7,317 s user time, that is 2.0 CPU-hours (1.2 h on
  two processes); Section 10 and Section 5.5 now use 2.0 CPU-hours. The
  2.6 CPU-hours is the critique's estimate for an earlier run on 4--5
  processes. B9 should use 2.0 CPU-hours or say which run each figure belongs to.
- **eg trust wording (decision 7).** Section 5.5 now states
  `thm:eg-bounds` under the review's trust-base wording (exact rationals;
  IEEE binary64 round-to-nearest-even with gradual underflow; correctness of
  the model reader, enclosure code, auditor, exact arithmetic and coverage
  checker; faithful execution and retention of the recorded run; no accuracy
  guarantee for NumPy, libm or Intel SVML). The TODO at the end of
  `F-eg-rounding.tex` (line ~439) and the one in `02-semantics.tex` should be
  resolved the same way.
- **pricing050 multiplier count.** Unchanged ("two nonzero 20-digit
  multipliers"; B5: $\mu_{e5}$, $\mu_{e6}$).
- **Box merges.** Section 5.2 has one box for `thm:ex62-bounds` and
  `thm:pricing-bound`, and Section 5.3 one box for `thm:etamac-bound` and
  `thm:pindyck-bound`. B5 line ~625 ("The certificate boxes of
  \cref{sec:other} give the arithmetic, the evidence level and the replay
  times") remains true.
- **Box format.** Section 5 boxes use four fields (Inputs, with how the
  data are read; Computation; Implementations; Level and replay). Section 4
  uses six. Harmonize if desired.
