# Moves from Section 3 (`sections/03-results.tex`) to the supplement

Key: m-results. Target file for Moves 1 and 2: `sections/D-literature.tex`
(Section S3 of the supplement, subsection `app:literature-funnel`, printed
as S3.4). Target file for Move 3: `sections/C-points.tex` (Section S2).

Section 3.1 now gives the funnel in prose, the informal meaning of sense (b)
and the width rule, and the caveats in short form. It points to
`app:literature-funnel` for the exact rules. The funnel table
(`tab:results-funnel`), the formal definitions, the chain width example and
the `fct` details are no longer in the main text.

`D-literature.tex` cites `\cref{tab:results-funnel}` twice (lines 249 and
289 of the current file). Until Move 1 is pasted, the supplement build
reports this label as undefined. Main.tex no longer cites
`tab:results-funnel` or `fig:results-funnel`; it cites only
`app:literature-funnel`, so you may keep the figure, the table or both.

All facts below were already verified (development/dossiers/pattern-theory.md
section 2.3 and its critique C1, C11; numbers-check item 11; decision
register G-05). The text is the former Section 3.1 text and footnotes, with
numbers-check item 11 applied ("361 and 295").

## Move 1 and 2: replace the start of `app:literature-funnel`

Replace the current subsection text before the figure (lines 247-253, from
`\subsection{How the 43 instances were selected}` to the sentence about
`fct`) with the block below. Keep the existing tikz figure
`fig:results-funnel` after it, or drop it if the table suffices (nothing in
main.tex cites the figure any more).

```latex
\subsection{How the 43 instances were selected}\label{app:literature-funnel}

\Cref{sec:results-selection} summarizes the selection; this subsection gives its exact rules.
Listed data refer to the snapshot of \cref{sec:semantics-model}.
The \emph{best listed point} is the listed point with the best objective value among those with listed violation at most $10^{-8}$.
The \emph{listing dual} is the dual value shown in MINLPLib's instance list; it equals the third-best single-solver entry up to display rounding (\cref{app:audit-screen}), and instances with fewer than three solver entries, such as the four \inst{catmix} instances, have none.
The \emph{listing gap} is the relative gap that MINLPLib's instance data record between the listing dual and the best known primal value.

We use ``open'' in two senses.
In sense~(a), an instance is listed as open if it has no S mark; all 43 instances of the paper are.
Sense~(b) is a stricter rule of ours, used only for selection; MINLPLib does not use it.
Let $d$ be the best listed dual and $p$ the objective value of the best listed point.
Set $g(p,d)=0$ if $p=d$; otherwise set $g(p,d)=\infty$ if $p$ and $d$ differ in sign or one of them is $0$, and $g(p,d)=|p-d|/\min(|p|,|d|)$ in all other cases.
An instance is \emph{open in sense~(b)} if $g(p,d)>10^{-4}$, or if it has no listed point or no finite listed dual.
Two of our closures, \inst{camshape100} and \inst{lnts50}, are listed as open but are not open in sense~(b): their values of $g(p,d)$ are at most \sci{1.3}{-6} and \sci{3.9}{-5}.

The \emph{width rule} asks for a factor-incidence width of at most 16, or for a nonlinear-primal width of at most 6 together with at least 50 nonlinear variables.
The factor-incidence graph has a node for each variable, each row and each nonlinear additive term; a row is joined to its linear variables and its terms, and a term to its variables.
In the nonlinear-primal graph, two variables are adjacent if they occur in a common nonlinear term.
Both widths are upper bounds on treewidth from a min-degree elimination heuristic with a time limit; instances for which the heuristic returned no value count as not meeting the rule.
The rule reflects our search for exploitable sparse structure; it is a selection device, and we do not claim that small width made these instances hard or easy (\cref{sec:interpretation}).

\begin{table}[htbp]
\centering
\small
\caption{Selection funnel on the MINLPLib snapshot of \cref{sec:semantics-model}.
Rows 2 to 6 each keep the instances of the row above that meet one more condition; the conditions are defined in the text.
The funnel is a post hoc reconstruction, and 29 of 155 is not a solve rate.}
\label{tab:results-funnel}
\begin{tabular}{@{}lr@{}}
\toprule
step & instances \\
\midrule
MINLPLib instance pages in the snapshot & 1,633 \\
\quad flagged nonconvex by MINLPLib & 1,257 \\
\quad and without the S mark (listed as open) & 596 \\
\quad and meeting the width rule & 360 \\
\quad and with a listing gap above $10^{-4}$ or infinite & 294 \\
\quad and open in sense (b) & 155 \\
\midrule
closed in the paper, among the 155 & 29 \\
other instances of the paper, among the 155 & 12 \\
closed in the paper, among the 294 but not the 155 & 2 \\
\bottomrule
\end{tabular}
\end{table}

The funnel is a post hoc reconstruction, and four caveats apply.
First, we chose our first 11 instances (\inst{camshape100}--\inst{camshape800}, \inst{lnts50}--\inst{lnts400}, \inst{dtoc5}, \inst{optcdeg2} and \inst{lukvle10}) before the rule was fixed, from a partial version of the width census.
They are families of constant width whose listed gaps grow with size (\inst{camshape}, \inst{lnts}), and very long chains with almost trivial listing duals (\inst{dtoc5}, \inst{optcdeg2}, \inst{lukvle10}).
All 11 lie among the 294, and 9 of them among the 155.
Second, we chose the other 32 instances from the remaining 146 instances open in sense~(b), ranked by our judgment of tractability and payoff.
Hence ``29 of 155'' describes what a targeted effort achieved; it is not a solve rate and does not measure how hard the open instances are.
Third, the widths are heuristic upper bounds and can be loose.
The census splits a nonlinear expression into terms only at a top-level sum.
The objective of \inst{chain50}--\inst{chain400} is written as a constant times a sum, so the census treats it as one term and records a nonlinear-primal width bound of $2N+1$, where $N$ is the number of intervals; the nonlinear-primal graph of these models has width~1.
Fourth, no separate review checked the census or the selection code; all counts in \cref{tab:results-funnel} reproduce with three separately written programs from the saved pages and census data.

One instance, \inst{fct}, is nonconvex and listed as open but missing from the width census, because its OSIL file was not in our cache.
It is counted in the first three rows of \cref{tab:results-funnel}.
It has 11 variables and no listing dual, and it would pass the next two steps, raising the fourth and fifth rows to 361 and 295.
Its value of $g(p,d)$ is $0$, so the count of 155 does not change.
```

Also in `D-literature.tex`:
- line 16: "against the MINLPLib snapshot of `\cref{sec:results-selection}`" should
  read `\cref{sec:semantics-model}` (Section 2.1 defines the snapshot;
  Section 3.1 no longer describes it);
- the figure caption (line 289): replace "on the MINLPLib snapshot of
  `\cref{sec:results-selection}`" with "on the MINLPLib snapshot of
  `\cref{sec:semantics-model}`". Its "with the counts of
  `\cref{tab:results-funnel}`" resolves once the table above is pasted.
- The old line 250 ("`\Cref{sec:results-selection}` defines the notions it
  uses ... and states four caveats") is replaced by the block above; the
  four caveats and the definitions now live here.

Test: I pasted this block (and the two `\cref` fixes above) into a copy of
the paper in /tmp/m-results/paper and ran `make`. `tab:results-funnel`
resolved (it printed as a supplement table in S3.4), and the paste added no
undefined reference, multiply defined label or "??".

## Move 3 (optional detail): violation of the listed waterno2_06 point

Section 3.3 dropped the violation of MINLPLib's point p4. Source:
development/dossiers/waterno2.md lines 777-786 (listed infeasibility 2e-12;
exact maximum row violation 1.08e-11, row e94). In `C-points.tex`, after the
sentence "The \inst{waterno2_06} point lies within $\sci{3.1}{-13}$ of p4; it
is MINLPLib's point made exact, not our own." (current line 263), add:

```latex
The point p4 itself violates row e94 by \sci{1.08}{-11}.
```

## Not moved (already elsewhere)

Everything else cut from Section 3 is already stated in the main text or the
supplement:
- arithmetic counts of the dual and primal proofs: arith. column of
  `tab:closures`;
- the lnts characterization ($N h^*$, enclosures below $10^{-60}$):
  `thm:lnts-opt` (Section 4);
- the chain listed duals (below 0.18) against optimal values above 5.06:
  `B4-chain-catmix.tex` (Section S1.4);
- the five instances whose one-hour dual bounds improve the listed ones:
  Section 8.3; BARON's returned optimal values are unattainable:
  `prop:baron-camshape` (Section 8);
- waterno2 method details, p4 and the improved primal values:
  Section 4.5, `tab:unclosed` note, `C-points.tex`, `B8-waterno2.tex`; the
  SCIP error on period subproblems: Section 8.2;
- ann method details and the exact $L^*$: Section 5.5 (`thm:ann-bound`),
  `tab:unclosed` note;
- KAN details (Rosenbrock surrogates, tolerance-feasible listed points,
  shared exponential and interval core, SCIP margins, time limits on the
  other four models): Section 2 (`rem:sem-readings`, protocol), Section 5.5
  certificate box, `tab:trust`, `tab:kan` note, Section 8.1,
  `tab:literature`;
- prior-status details (publisher correction, MINOTAUR's later
  infeasibility report on QPLIB_8803, dates of the QPLIB listings, the exact
  QPLIB_8585 differences, Huang 2019 and the three unread waterno2 sources):
  `tab:literature` and `app:literature-unread` (Section S3).
