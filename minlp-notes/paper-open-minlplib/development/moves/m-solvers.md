# Moves from Section 8 (`sections/08-solvers.tex`) to the supplement

Key: m-solvers. Target file for all moves: `sections/H-solvers.tex`
(Section S6 of the supplement, `app:solvers`).

Section 8 now cites the five moved labels across documents: `tab:claims`,
`tab:solvers`, `fig:camshape-deficit`, `prop:qplib-copies` and
`prop:kan-scip`. Until the blocks below are pasted, both builds report these
labels as undefined (other files cite them too: Sections 1, 4, 5, 6, 9, 11;
B1, B2, B3, B7, B9, D, H, I). Nothing that cites them needs to change.

I test-pasted all five blocks, at the places given, into a copy of the paper
in /tmp/m-solvers and ran `make`: neither document had an undefined
reference from these labels.

Order inside `H-solvers.tex` after pasting:
- `app:solvers-runs`: Move 3 (tab:solvers), then the existing `tab:campaign-runs`;
- `app:solvers-points`: existing camshape-deficit paragraph, Move 2 (figure), existing `tab:claims-campaign`;
- new `app:solvers-claims` (Move 1) after `app:solvers-points`;
- `app:solvers-baron`: existing BARON paragraph and certbox, Move 4 (prop:qplib-copies), existing "The QPLIB copies" paragraph and certbox;
- `app:solvers-published`: existing CAMINO and MINOTAUR paragraphs, Move 5 (prop:kan-scip), existing KAN paragraph.

You may add `\cref{app:solvers-claims}` to the list in the first sentence of
`H-solvers.tex`.

## Move 1: the claims register (`tab:claims`)

The sideways table took a full page of Section 8. The main text keeps one
sentence pointing to it.

Where: new subsection directly after the subsection `app:solvers-points`
(after `\input{tables/tab-claims-campaign}`) and before
`\subsection{BARON's claims and the QPLIB copies}`.

```latex
\subsection{Reported values that no exactly feasible point attains}\label{app:solvers-claims}

\Cref{tab:claims} collects the reported values that we found to be unattainable under exact feasibility (category~A of \cref{def:sem-categories}): listed MINLPLib points, MINLPLib's listed dual bound of \inst{optcdeg2}, the two optimality claims and one returned point of our one-hour runs, and published values.
It lists the values that we checked; it is not the result of a complete search.
The further returned points of our runs that lie beyond a certified bound are in \cref{tab:claims-campaign}.
Category~A covers both directions: MINLPLib's points p1 and p2 of \inst{hvycrash} report $-0.21413$, while every exactly feasible point has the objective value $-0.2185$ (\cref{prop:hvycrash-identity}), and a floating-point KKT point of \inst{optcdeg2} has an objective at least $\sci{5.95}{-12}$ above the rigorous upper bound.

\input{tables/tab-claims}
```

Source: the paragraph after `\input{tables/tab-claims}` in the old Section 8;
the numbers are the table's own rows (generated from `data/numbers.json`).

## Move 2: Figure `fig:camshape-deficit`

The figure took half a page of Section 8. Section 8 still cites it once
(BARON's deficits are about 87% of `D_n(1e-10)`); the camshape paragraph of
`app:solvers-points` already cites it. Caption unchanged.

Where: subsection `app:solvers-points`, directly after the paragraph that
begins "For the \inst{camshape} points, \cref{prop:camshape-deficit} at the
point's largest violation bounds ..." and the sentence after it ("One
returned point lies on the safe side ..."), before
`\input{tables/tab-claims-campaign}`.

```latex
\begin{figure}[t]
\centering
\includegraphics[width=0.9\textwidth]{fig-camshape-deficit.pdf}
\caption{Deficit $v_n-f$ below the exact optimum against the largest row or bound violation $\varepsilon$, for tolerance-feasible points of \inst{camshape<n>}: returned points of the one-hour runs (50-digit evaluation of the savepoints) and MINLPLib's listed points p1 and p2 (exact evaluation), with the proved upper bounds $D_n(\varepsilon)$ of \cref{prop:camshape-deficit}.
The gray level of a marker gives $n$ as for the curves.
No point lies above its curve; BARON's three points at $\varepsilon\approx10^{-10}$ reach about 87\% of $D_n$, and MINLPLib's points p2 about 29\%.
QPLIB's reference points of \inst{QPLIB_2703} and \inst{QPLIB_3177} lie at the positions of the points p2, measured against the optima of these copies.
The curves are computed from the construction of \cref{app:camshape-deficit} in 60-digit arithmetic and agree with \cref{tab:camshape-deficit}.}
\label{fig:camshape-deficit}
\end{figure}
```

## Move 3: Table `tab:solvers` (counts of the one-hour runs)

Section 8.3 now gives the essential counts in prose (129 runs; 2 optimality
claims, 0 accepted closures; 109 finite duals, 35/36/38 by solver, 91 + 18;
5 improvements; 35 returned values beyond a bound; 10 runs in the overloaded
batch; 3 memory stops; 6 + 6 qualified bounds; 9 + 1 failures) and points to
the table. The per-solver split of the other rows exists only in the table.

Where: subsection `app:solvers-runs`, replacing its first sentence with the
two sentences below and the table, before `\input{tables/tab-campaign-runs}`.

```latex
\Cref{tab:solvers} counts the outcomes by solver, and \cref{tab:campaign-runs} gives the outcome of all 129 kept runs and the distance of each finite final dual bound to the certified primal value, on the scale of \cref{fig:results-headline}.

\input{tables/tab-solvers}
```

## Move 4: Proposition `prop:qplib-copies` (statement and proof)

Section 8 now states the result in prose (values, margins, violation
thresholds, the `.nl` assumption, category A) and cites the proposition.
The existing paragraph "The QPLIB copies" and its certificate box in H stay as
they are; the box is titled "Certificate for \cref{prop:qplib-copies}".

Where: subsection `app:solvers-baron`, after the BARON certbox and before
`\paragraph{The QPLIB copies.}`.

```latex
\begin{proposition}[Reported optima of the rounded copies]\label{prop:qplib-copies}
Read \inst{QPLIB_3177} (the copy of \inst{camshape800}) and \inst{QPLIB_2738} (the copy of \inst{camshape100}) with exact decimals.
In Mittelmann's QPLIB benchmark \citep{mittelmann2026-continuous-non-convex-qplib-benchmark}, MINOTAUR~0.4.1 reports the optimal value $-4.2774$ for \inst{QPLIB_3177}, and ANTIGONE~1.1 the global minimum $-4.284302$ for \inst{QPLIB_2738}.
\textup{(a)}~No exactly feasible point of the copy attains any number that displays as the reported value; the margins are at least $\sci{3.162}{-3}$ and $\sci{1.552}{-4}$.
\textup{(b)}~Every point of \inst{QPLIB_3177} with objective at most $-4.27735$ violates some row or bound by more than $\sci{8}{-9}$, and every point of \inst{QPLIB_2738} with objective at most $-4.2843015$ violates some row or bound by more than $\sci{2.5}{-8}$.
For MINOTAUR, which read \inst{QPLIB_3177} in AMPL's \texttt{.nl} format, we assume that this file has the rows and bounds of the GAMS copy.
\end{proposition}

\begin{proof}
By \cref{prop:camshape-copies}, the optimal values of the copies are at least $-4.2741871514717434$ and $-4.2841462678046117$.
Every number that displays as $-4.2774$ is at most $-4.27735$, and every number that displays as $-4.284302$ is at most $-4.2843015$; subtraction gives~(a).
For~(b), \cref{app:camshape-copies} applies the construction of \cref{prop:camshape-deficit} to the copies; the paragraph below gives the resulting objective bounds.
\end{proof}

The dual bounds implied by the two claims equal the reported values and are valid, so both values are tolerance artifacts on the copies (category~A); points built in floating point reach them with violations of $\sci{9.7}{-9}$ and $\sci{2.9}{-8}$ (numerical evidence).
```

Source: Proposition 8.2, its proof and the paragraph after it in the old
Section 8 (all numbers unchanged; checked in `numbers-check.md`, "Margins":
3.162e-3 / 1.552e-4).

## Move 5: Proposition `prop:kan-scip` (statement and proof)

Section 8 now states the result in prose (margins 1.70e-3 / 2.03e-3, no point
of R or R_P attains the values, trivially valid as duals of the infeasible
OSIL models, the model-identity assumption, the scale 970) and cites the
proposition. The existing KAN paragraph of `app:solvers-published` says what
the proposition needs.

Where: subsection `app:solvers-published`, directly before
`\paragraph{The KAN models of \citet{karia2025-deterministic-global-optimization-over-trained}.}`.

```latex
\begin{proposition}[Published SCIP optima for two KAN models]\label{prop:kan-scip}
For \inst{kan_r3_h1_n4} and \inst{kan_r3_h1_n5}, \citet{karia2025-deterministic-global-optimization-over-trained} report SCIP~9.0.1 runs that end with ``optimal solution found'' and gap~0 at $\sci{1.08116412047821}{-3}$ and $\sci{-1.30809958982354}{-2}$ \citep{karia2025-karia-et-al-zenodo-default}.
These values lie at least $\sci{1.70}{-3}$ and $\sci{2.03}{-3}$ below the certified lower bounds $\Lcert$ of \cref{thm:kan-enclosure}, so no point of $\Rnet$ or $\RP$ attains them.
\end{proposition}

\begin{proof}
The displays of $\Lcert$ in \cref{tab:kan}, $0.002781237152581$ and $-0.01104267952179$, are rounded down; subtracting the reported values from them gives the margins.
Since $\Lcert\le\min_{\Rnet}F\le\min\RP$, no point of either model attains the reported values.
\end{proof}
```

Source: Proposition 8.3 and its proof in the old Section 8 (numbers unchanged;
`numbers-check.md`, "Margins": 1.70e-3 / 2.03e-3).

## Text cut from Section 8 that needs no move (already in the paper)

| cut from Section 8 | where the fact remains |
|---|---|
| D_n(1e-10) for n = 100, 200: 6.05e-7 and 2.36e-6 | `tab:camshape-deficit` (B3); Section 5, `prop:camshape-deficit` (n = 100) |
| QPLIB copies: optima raised by at least 8.539e-7 (n = 100) to 8.699e-5 (n = 800); above 1e-6 relative for n >= 200 | `tab:camshape-copies` and the text before it (B3); Section 3 for QPLIB_2480 |
| QPLIB reference points of QPLIB_2703 / QPLIB_3177 at least 8.15e-6 / 3.27e-5 below the copies' optima | B3 (`app:camshape-copies`) and `tab:camshape-copies`; caption of `fig:camshape-deficit` |
| hvycrash p1/p2 at -0.21413 against the constant -0.2185 ("both directions") | Section 2 (`sec:semantics-categories`); `tab:claims`; Move 1 |
| optcdeg2 float KKT point 5.95e-12 above the upper bound | B2 (paragraph before the `prop:optcdeg2-point` certbox); `tab:claims`; Move 1 |
| camshape400/800 p2: hundreds of rows violated by about 1e-10, at least 8.15e-6 / 3.27e-5 below | Section 5 after `prop:camshape-deficit`; B3 (`app:camshape-deficit`) |
| GUROBI's listed optcdeg2 dual equals the value of p2 (violation 1e-6), at least 1.45 below the optimum | Section 4 (optcdeg2 listed status); `tab:claims`; B2 |
| BARON's returned points violate rows and the upper bound of r_1 by just under 1e-10 | H `app:solvers-baron` (9.995e-11 to 9.998e-11); Section 8 keeps "just under 1e-10" |
| MINOTAUR 0.4.1 on QPLIB_8585: 5.3897 after default bounds | Section 3 (`sec:results-prior`); Section 4; B2; D |
| SCIP memory stops: instance names ex6_2_5, ex6_2_7, pindyck | H `app:solvers-protocol` ("Failures and warnings"); Section 8 keeps the count |
| GUROBI's dual on lnts50 at 3.9e-5 relative (closest after BARON's camshape bounds) | `tab:campaign-runs` (H) |
| CAMINO: GUROBI 13.0.2 through GAMS reached the time limit on all three eg instances with valid bounds | H `app:solvers-published` ("Our GUROBI 13.0.2 runs ...") |
| Box details on fm336 (data, the two propagation rounds) | H `app:solvers-scip` ("Models", "The traced steps"); Lemma 8.6 and Observation 8.7 stay in Section 8 |
