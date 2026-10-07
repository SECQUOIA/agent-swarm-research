# Moves from Sections 6 and 7 to the supplement (key: m-points-audit)

Material cut from `sections/06-points.tex` and `sections/07-audit.tex` that
the supplement does not yet contain. Each block is ready to paste. Labels are
unchanged, so every existing `\cref` (in the paper and in the supplement)
resolves once the block is in place. Until then the paper build reports
these undefined references: `prop:pts-exact`, `rem:lukvle10-seeds`,
`lem:audit-display`, `prop:spring-opt`, `prop:emfl-enclosure`,
`fig:audit-margins`.

Numbers were checked against the sources named in each move. Nothing here
is new; the text is the previous main-text wording, with the one number fix
noted in Move 2.

---

## Move 1: Proposition `prop:pts-exact` (statement)

Target: `sections/C-points.tex`, subsection `app:points-props`, directly
before `\begin{proof}[Proof of \cref{prop:pts-exact}]`. The subsection
title can stay; if the editor prefers, change it to
`Points in quadratic fields, and proofs for \texorpdfstring{\cref{sec:points}}{Section 6}`.
Section 6 now summarizes the proposition in one sentence (construction (A)).

```latex
\begin{proposition}[Points in $\Q$ or $\Q(\sqrt D)$]\label{prop:pts-exact}
Let $D>0$ be a rational number that is not the square of a rational.
\begin{itemize}
\item[(a)] Every element of $\Q(\sqrt D)$ has a unique form $p+q\sqrt D$ with $p,q\in\Q$, and its sign is decidable.
If $pq\ge0$, it is the sign of whichever of $p$ and $q$ is nonzero, and the element is zero if and only if $p=q=0$.
If $pq<0$, it is the sign of $p$ when $p^2>q^2D$ and the sign of $q$ when $p^2<q^2D$, and $p^2=q^2D$ cannot occur.
\item[(b)] Let $x$ be a point with coordinates in $\Q(\sqrt D)$, and let every row and bound of $\model$ be built from the coordinates and rational constants by $+$, $-$, $\times$, $\div$, integer powers and \texttt{sqrt}.
Evaluate every expression exactly in $\Q(\sqrt D)$; at a \texttt{sqrt} node with argument $a$, use a given candidate $s\in\Q(\sqrt D)$ after checking $s\ge0$ and $s^2=a$.
If every check passes, every denominator is nonzero, every row and bound comparison holds by the sign test in (a), and every integer variable has an integer value, then $x\in\feas$.
If the objective is built in the same way, $f(x)$ is the computed element of $\Q(\sqrt D)$.
\end{itemize}
The same holds row by row when each row involves coordinates from $\Q$ and at most one field $\Q(\sqrt{D_k})$.
\end{proposition}
```

## Move 2: Remark `rem:lukvle10-seeds` (with the seed experiment)

Target: `sections/C-points.tex`, subsection `app:points-instances`, at the
start of the paragraph `\paragraph{\inst{lukvle10}.}` (before "The seeds
$x_0,x_1$ are the values ..."). That paragraph already cites the remark.
Section 6 keeps a two-sentence summary (rational seeds define a rational
point; growth factor; 640 decimals) and cites the remark.

Number fix: the previous text printed $2.73^{999}\approx10^{436}$. Rows
$j=0,\dots,997$ apply the recursion 998 times and $998\log_{10}2.73=435.3$
(numbers-check item 18; `development/dossiers/lnts-lukvle10.md`, structure
paragraph). Sources for the other numbers:
`development/dossiers/primal-points.md` (lukvle10 paragraph of the
constructions and "Relation to the earlier tolerance points": p5 lies
5.14e-13 above the objective of x*), `development/dossiers/lnts-lukvle10.md`
(seed sensitivity; p5 residual 3.48e-15). The range 352.89 to 353.01 is the
Section 6 writer's correction of the dossier's 353.00 (write-result.json,
points report).

```latex
\begin{remark}[Seeds for \inst{lukvle10}]\label{rem:lukvle10-seeds}
Every row of \inst{lukvle10} reads $-x_j+3x_{j+1}-2x_{j+2}-2x_{j+1}^2=-1$ ($j=0,\dots,997$), and all 1000 variables are free.
Row $j$ defines $x_{j+2}$ from $x_j$ and $x_{j+1}$, and the objective is defined at every real point, because its \texttt{power} nodes have exponents of the form $x_k^2+1>0$ (\cref{def:sem-model}).
Any two rational seeds $x_0,x_1$ therefore define a rational, exactly feasible point (\cref{prop:pts-triangular}).
The denominators roughly square at every step, so the point cannot usefully be printed.
Useful seeds must also be very precise.
At the fixed point $-1/\sqrt2$ of the recursion, its linearization has the eigenvalues $2.731$ and $0.183$, so seed errors grow by a factor of about $2.73^{998}\approx10^{435}$ along the chain.
In a floating-point experiment at 1500 digits, the 15-digit seeds of MINLPLib's listed point p5 drive $|x_j|$ above $10$ at index $40$.
Seeds that agree with a numerical local minimizer to 50--420 decimals give objective values between $352.89$ and $353.01$; seeds with 440 decimals give a value within $\sci{2}{-14}$ of the local minimizer's, and 460 or more decimals reproduce it to 20 digits.
Our point uses seeds with 640 decimals; the seeds and the recursion define it.
MINLPLib's listed point p5, whose rows hold to $\sci{3.48}{-15}$, evaluates about $\sci{5.1}{-13}$ above the objective of our point.
\end{remark}
```

## Move 3: how far the powerflow points moved

Target: `sections/C-points.tex`, paragraph
`\paragraph{\inst{powerflow0030p}, \inst{powerflow0039p}, \inst{powerflow0039r}.}`,
directly before "The objectives of the exact points exceed those of p1 by
...". Source: `development/dossiers/primal-points.md`, "Relation to the
earlier tolerance points".

```latex
The free variables of the exact points differ from those of p1 by at most $\sci{1.4}{-14}$, $\sci{2.5}{-13}$ and $\sci{7.8}{-12}$.
```

## Move 4: Lemma `lem:audit-display` (statement)

Target: `sections/E-audit.tex`, subsection `app:audit-hyp`, directly before
`\begin{proof}[Proof of \cref{lem:audit-display}]`. Section 7 now
paraphrases the lemma and cites it. Also change the first sentence of
`E-audit.tex` from "the proofs of \cref{lem:audit-display}, ..." to "the
statements and proofs of \cref{lem:audit-display}, \cref{prop:spring-opt}
and \cref{prop:emfl-enclosure}, ...".

```latex
\begin{lemma}[when Hypothesis~H holds]\label{lem:audit-display}
Let $b\in\R$ be a reported dual bound and $s$ the string displayed for it, with $\dval{s}\neq0$.
\begin{enumerate}
\item[(a)] Suppose $\dval{s}$ arises from $b$ by finitely many steps, each a rounding (to nearest with any tie rule, or directed) or a truncation to an integer multiple of a power of ten.
Then $|b-\dval{s}|<\tfrac{10}{9}\dunit{s}$.
If at most one step changes the value, or if the last step that changes it rounds to nearest, Hypothesis~H holds.
\item[(b)] Suppose the site stores a binary64 number $b'$ with $|b'-b|\le 2^{-53}|b|$, rounds $b'$ to nearest at ten significant digits, stores the result in binary64, and displays it rounded to nearest at eight decimals without trailing zeros.
If $|\dval{s}|\le 6\cdot10^{7}$, Hypothesis~H holds.
\end{enumerate}
\end{lemma}
```

## Move 5: Proposition `prop:spring-opt` (statement)

Target: `sections/E-audit.tex`, subsection `app:audit-spring`, after the
model description (the `gather*` display and the sentence that ends "and
the objective is $(a_0+a_1i_4)\,x_1x_2^2$.") and directly before
`\begin{proof}[Proof of \cref{prop:spring-opt}]`. Section 7 keeps the value
$\vstar=0.846245665643154281\ldots$, the attainment, the eight-decimal
rounding and the 1,100-assignment enumeration in one sentence.

```latex
\begin{proposition}[\inst{spring}]\label{prop:spring-opt}
With $a_0=1.570796327$, $a_1=0.7853981635$, $c=0.283$, $\lambda=1.78571428571429\cdot10^{-3}$, $K=6.95652173913044\cdot10^{-7}$ and $x_5^\ast=\bigl(\lambda c/(9K)\bigr)^{1/3}$, the optimal value of \inst{spring} is $\vstar=(a_0+9a_1)\,c^{3}\,x_5^\ast=0.846245665643154281251664635037\ldots$, attained with $i_4=9$, $x_2=0.283$ and $x_3=\lambda$.
The five displayed bounds 0.84624567 equal $\vstar$ rounded to eight decimals.
\end{proposition}
```

## Move 6: Proposition `prop:emfl-enclosure` (statement) and the S-mark numbers

Target: `sections/E-audit.tex`, subsection `app:audit-emfl`, directly
before `\begin{proof}[Proof of \cref{prop:emfl-enclosure}]` (after the
proof of `lem:audit-socp`). The second block goes after the paragraph that
follows `tab:audit-emfl` ("All listed points of ... Checker V1, a third
implementation, ..."). Section 7 keeps all numbers of the proposition in
prose and the relative S-mark margin $1.166\cdot10^{-6}$; the absolute
margin and the two listed values are only here. Sources:
`development/dossiers/audit.md` (emfl table), decision register AU-11 and
AU-12; the margins use the lower end of checker V2's enclosure and widen the
displayed values by half a display unit.

```latex
\begin{proposition}[\inst{emfl}]\label{prop:emfl-enclosure}
For \inst{emfl050_3_3}, \inst{emfl050_5_5}, \inst{emfl100_3_3} and \inst{emfl100_5_5}, the optimal values lie in the first-line intervals of \cref{tab:audit-emfl}, each of width below $3.4\cdot10^{-11}$.
Every listed dual bound of these instances is valid.
The best listed primal values lie below $\vstar$ by at least $1.41\cdot10^{-5}$, $1.98\cdot10^{-3}$, $2.92\cdot10^{-4}$ and $6.86\cdot10^{-6}$, so no exactly feasible point attains them; for the S-marked \inst{emfl050_3_3} this is at least $1.36\cdot10^{-6}$ relative.
\end{proposition}
```

```latex
The best listed dual bound of the S-marked \inst{emfl050_3_3}, 10.40173999, lies at least $1.213\cdot10^{-5}$ (at least $1.166\cdot10^{-6}$ relative) below the exact optimum.
Its S mark is consistent with the listed primal value 10.40173793, and since the mark is defined with tolerance-feasible points, we do not call it wrong.
```

## Move 7: Figure `fig:audit-margins`

Target: `sections/E-audit.tex`, subsection `app:audit-screen`, after the
paragraph "Classes." (after `tab:audit-solvers` is fine). Section 7 cites
the figure for the margin groups. The figure file is unchanged
(`figures/fig-audit-margins.pdf`, from `figures/make_fig_audit.py`); the
caption is the previous one with "half a unit" kept.

```latex
\Cref{fig:audit-margins} shows the margins of all refuted and class (i-r) bounds.

\begin{figure}[t]
\centering
\includegraphics[width=\textwidth]{fig-audit-margins}
\caption{Margins $d-f$ of the refuted and the class (i-r) listed dual bounds, in units of the last displayed digit of $d$ (horizontal) and relative to $|d|$ (vertical). $f$ is the upper end of the objective enclosure at an exactly feasible point (for \inst{spring}, the proved optimum). Pairs with the same bound and point values are drawn once (19 class (i) pairs give 15 marks, 12 class (i-r) pairs give 4). Vertical lines: the screen's slack of half a unit and the one unit of Hypothesis~H. Horizontal lines: MINLPLib's gap tolerance $10^{-6}$ and the common relative gap tolerance $10^{-4}$. Pages of 2026-09-30.}
\label{fig:audit-margins}
\end{figure}
```

## Move 8: invalid bounds that equal earlier listed point values

Target: `sections/E-audit.tex`, subsection `app:audit-screen`, at the end of
"Undecided pairs." or as its own short paragraph before "How MINLPLib
aggregates." Previously in Section 7.4. It is an observation, not a cause
(outline section 8, item 7: no inference that a solver reported a local
optimum as a bound).

Check (read-only, `R/bound-audit/pages.json`, script in
`/tmp/m-pa/check10.py`): a listed point "agrees" with a bound if its value,
rounded to the bound's number of decimals, equals the bound; the point must
be dated on or before the bound and have a value above the proved $f$. The
ten pairs: \inst{glider100} COUENNE and LINDO (p1), \inst{methanol50} LINDO
(p3, same day), the four \inst{sssd} instances, LINDO (p2), \inst{ghg_3veh}
ANTIGONE and BARON (p1), \inst{nd_netgen-2000-3-4-b-a-ns_7} GUROBI (p1).

```latex
In ten of the 19 class (i) pairs, the invalid bound agrees, to all its displayed digits, with the value of a listed point that was added on or before the date of the bound and whose value lies above the proved objective value: \inst{glider100} (COUENNE and LINDO), \inst{methanol50}, the four \inst{sssd} instances, \inst{ghg_3veh} (ANTIGONE and BARON) and \inst{nd_netgen-2000-3-4-b-a-ns_7} (GUROBI).
The pages do not record how any bound was computed, and we draw no conclusion about the cause.
```

## Move 9: earlier checks of benchmark data (literature details)

Target: `sections/D-literature.tex`, paragraph "Benchmark checks and solver
reliability.", after its second sentence ("The closest precedents are
MINLPLib~2 ..."). Previously the closing paragraph of Section 7.5; Section
1.4 summarizes the same sources, and Section 7 now keeps one sentence. The
detail not stated elsewhere is Neumaier et al.'s announcement of existence
proofs as future work, and the specific PAVER and MIPLIB checks.

```latex
\citet{vigerske2014-minlplib-2} explains that providing dual bounds in verifiable form was not feasible for the library, which therefore trusts a solver's bound only if at least two other solvers verify it, and the accompanying slides state ``No way to verify correctness of bound!'' \citep{vigerske2014-towards-minlplib-2-0}.
Benchmark tools check consistency with tolerances: PAVER flags runs whose bounds contradict known bounds \citep{bussieck2014-paver-2-0-an-open}, and MIPLIB~2017 checks solutions in arbitrary precision with tolerances and removed instances with inconsistent solver results from its benchmark selection \citep{gleixner2021-miplib-2017-data-driven-compilation}.
\citet{neumaier2005-a-comparison-of-complete-global} counted wrong claims of complete solvers and announced rigorous existence proofs for nearby feasible points as future work.
```

---

## Not moved (already in the supplement or in another main-text section)

- Section 6.2 details (dtoc5 controls defined by rows; chain substitution
  and $R_N$ sizes; Krawczyk systems of 3 and 222/262/270 equations; radii):
  `C-points.tex` (certificate box of `prop:pts-former` and the family
  paragraphs).
- Old Section 6.3 ("Tolerance-feasible values err in both directions"):
  lnts50 p1 in Section 4 and `tab:claims`; camshape p2 and the deficit
  bound $D_n(\varepsilon)$ in Section 5 (`prop:camshape-deficit`); optcdeg2
  KKT point and hvycrash p1/p2 in Section 8.1 and `tab:claims`; the
  display-only list in Section 2.3; lukvle10 p5 in Move 2.
- Old Section 6.4 per-family implementation counts: `tab:points-all`
  (arithmetic column) and `C-points.tex`.
- Section 7.3 route details, the second implementations and the trust base
  of the seven Krawczyk refutations: `E-audit.tex` (`app:audit-existence`,
  "Trust and replay").
- Model history details, the GAMS/OSIL comparison and the binary64 rerun:
  `E-audit.tex` (`app:audit-history`) and Remark `rem:sem-readings`.
- How MINLPLib aggregates (third-best bound, `.solu` rule):
  `E-audit.tex`, "How MINLPLib aggregates."
- Absolute margins $d-f$, no longer a column of `tab:audit-pairs`:
  `data/numbers.json` (`audit.pairs[*].margin`); every claim uses the
  relative margins or display units, which the table keeps.
