# Moves from Sections 1, 2 and Appendix A to the supplement

Key: m-intro-sem. Files revised: `sections/00-abstract.tex`,
`sections/01-introduction.tex`, `sections/02-semantics.tex`,
`sections/A-semantics.tex`.

Target file for all moves: `sections/I-reproduction.tex` (Section S7 of the
supplement). Paste Moves 1 to 4 as one new subsection right after
`\subsection{Setup}\label{app:repro-setup}` and its text, before
`\subsection{Claim register}`.

All facts below were in the verified first draft of Appendix A
(`sections/A-semantics.tex`, before this revision) and were checked there
against `development/data-semantics.md`, `development/data-semantics-checks/`
and `data/numbers.json` (hash prefixes: `instances.*.size.osil_sha256`).
Nothing below is new; only the place changes.

Main-text references after this revision:

- `main.tex` no longer defines `tab:sem-hashes` or `tab:sem-operators`;
  nothing in the main text or the supplement cites them except the old
  Appendix A, which no longer does. Definition 2.1 now says the hashes are
  "recorded in the archive; \cref{app:repro}", and Appendix A says "The
  archive and \cref{app:repro} record the SHA-256 hashes". Move 1 makes
  that pointer true.
- `tab:sem-gams` stays in main Appendix A (compact form, four rows);
  `H-solvers.tex` line 46 still cites it correctly. Move 3 adds the
  per-family detail under a new label `tab:sem-gams-detail`.
- One sentence in `I-reproduction.tex` must change (see Move 1).

## Move 1: SHA-256 prefixes of the 43 stored models

Also change, in `I-reproduction.tex` (subsection `app:repro-register`,
currently line 50),
"The input models are identified by the SHA-256 hashes of \cref{app:semantics}."
to
"The input models are identified by the SHA-256 hashes of \cref{tab:sem-hashes}."

```latex
\subsection{Stored models}\label{app:repro-models}

The stored models of \cref{def:sem-model} are the OSIL files whose SHA-256 hashes begin as in \cref{tab:sem-hashes}; the archive records the full hashes, and \nolinkurl{prepare_inputs.py} rejects any file whose hash differs.
At the refresh of 2026-10-02, the OSIL files on the MINLPLib site for all 69 instances used in the paper and in the audit had the same hashes as our copies.

% Rows generated from data/numbers.json (instances.*.size.osil_sha256, first 16 hex digits);
% regenerate them if a model file changes.
\begin{table}[ht]
\centering
\small
\caption{SHA-256 prefixes (first 16 hexadecimal digits) of the 43 stored OSIL models. The files were fetched on 2026-09-29 and found unchanged on 2026-10-02.}
\label{tab:sem-hashes}
\begin{tabular}{@{}llll@{}}
\toprule
instance & SHA-256 prefix & instance & SHA-256 prefix \\
\midrule
\inst{lnts50} & \texttt{3d8234b338afc4cd} & \inst{etamac} & \texttt{6716cc88e1c4c61f} \\
\inst{lnts100} & \texttt{284bddc374db070c} & \inst{pindyck} & \texttt{c7b3b5e4a2c46b3e} \\
\inst{lnts200} & \texttt{c2dde9ef8ede3c16} & \inst{powerflow0030p} & \texttt{5c4b386b1f9a721a} \\
\inst{lnts400} & \texttt{96eb445643601734} & \inst{powerflow0039p} & \texttt{0a27073f39f6cc49} \\
\inst{dtoc5} & \texttt{ac7b2d9472dbbfe9} & \inst{powerflow0039r} & \texttt{d8ba3132cb69744e} \\
\inst{optcdeg2} & \texttt{6a9bcd91abdbe1b2} & \inst{hvycrash} & \texttt{27a0a05abecc0d64} \\
\inst{lukvle10} & \texttt{1eb1236df017099f} & \inst{eg_int_s} & \texttt{a462a01b98801f45} \\
\inst{chain50} & \texttt{f6b2b409aa4f3d00} & \inst{eg_disc_s} & \texttt{5f21b8d743b12c22} \\
\inst{chain100} & \texttt{45cb302006643309} & \inst{eg_disc2_s} & \texttt{8849e06b478f5b93} \\
\inst{chain200} & \texttt{634acc6242ce83fa} & \inst{waterno2_06} & \texttt{3b0b316d7a9fa834} \\
\inst{chain400} & \texttt{7cd93486e4610aa4} & \inst{waterno2_09} & \texttt{015932376b18ded5} \\
\inst{catmix100} & \texttt{9f5b5bae82032ecc} & \inst{waterno2_12} & \texttt{add485a67c22faee} \\
\inst{catmix200} & \texttt{9194135d049ce928} & \inst{waterno2_18} & \texttt{968ff496844df939} \\
\inst{catmix400} & \texttt{3dfc4d7f2886fa12} & \inst{waterno2_24} & \texttt{91d2612f435cd751} \\
\inst{catmix800} & \texttt{40b572a4b80446a5} & \inst{ann_cumene_tanh} & \texttt{13a44f74762fdb47} \\
\inst{camshape100} & \texttt{9e17da72f0cfe538} & \inst{kan_r3_h1_n4} & \texttt{2991cd53706de81f} \\
\inst{camshape200} & \texttt{76d6141d111fb1a0} & \inst{kan_r3_h1_n5} & \texttt{203647dbe25965ee} \\
\inst{camshape400} & \texttt{a53174a46ad923ef} & \inst{kan_r3_h1_n9} & \texttt{267fc6596ea164a0} \\
\inst{camshape800} & \texttt{d0692d0f81211081} & \inst{kan_r5_h1_n3} & \texttt{75d5998686158c0d} \\
\inst{ex6_2_5} & \texttt{eed480570b4fa8c1} & \inst{kan_r5_h1_n5} & \texttt{4288259a89d635d9} \\
\inst{ex6_2_7} & \texttt{c7f7cd3756d230cf} & \inst{kan_r5_h1_n8} & \texttt{595f66966d00affc} \\
\inst{pricing050} & \texttt{56d3e00fcac90c09} & & \\
\bottomrule
\end{tabular}
\end{table}
```

## Move 2: expression nodes of the 43 stored models

Main Appendix A.1 now lists the node types in one sentence and keeps the
four `power` cases and the domain-rule cases in prose. The per-instance
table below records where each node occurs (it supports the statement in
A.1 that the domain rule excludes points within the bounds only in
`hvycrash` and `pindyck`).

```latex
\Cref{tab:sem-operators} lists the expression nodes that occur in the 43 files and their meaning under \reading{b} (\cref{app:semantics-osil}).
The models \inst{dtoc5}, \inst{optcdeg2}, \inst{catmix}, \inst{camshape} and \inst{powerflow0039r} have no expression trees; their nonlinear terms are all quadratic terms.

\begin{table}[ht]
\centering
\small
\caption{Expression nodes in the 43 stored models and their meaning under \reading{b}. Linear and quadratic terms are read as in \cref{app:semantics-osil}.}
\label{tab:sem-operators}
\begin{tabular}{@{}lp{0.3\linewidth}p{0.4\linewidth}@{}}
\toprule
node & \raggedright meaning & \raggedright instances \tabularnewline
\midrule
\texttt{number}, \texttt{variable} & \raggedright $\dval{\sigma}$; $\texttt{coef}\cdot x_j$ & \raggedright all instances with expression trees (\texttt{number} not in \inst{ann_cumene_tanh}) \tabularnewline
\texttt{sum}, \texttt{product}, \texttt{negate} & \raggedright real arithmetic & \raggedright most instances with expression trees \tabularnewline
\texttt{divide} & \raggedright quotient; denominator nonzero & \raggedright \inst{ex6_2_5}, \inst{pindyck}, \inst{hvycrash}, KAN \tabularnewline
\texttt{square} & \raggedright $a^2$ & \raggedright \inst{lukvle10}, \inst{chain}, \inst{pricing050}, \inst{powerflow0030p}, \inst{powerflow0039p}, \inst{eg} \tabularnewline
\texttt{sqrt} & \raggedright nonnegative root; argument $\ge0$ & \raggedright \inst{chain} \tabularnewline
\texttt{power} & \raggedright \cref{def:sem-model}(iii) & \raggedright \inst{lukvle10}, \inst{etamac}, \inst{pindyck}, \inst{pricing050}, \inst{waterno2} \tabularnewline
\texttt{exp} & \raggedright $e^{a}$ & \raggedright \inst{pricing050}, \inst{eg}, KAN \tabularnewline
\texttt{ln} & \raggedright natural logarithm; argument $>0$ & \raggedright \inst{ex6_2_5}, \inst{ex6_2_7}, \inst{etamac} \tabularnewline
\texttt{sin}, \texttt{cos} & \raggedright argument in radians & \raggedright \inst{lnts}, \inst{powerflow0030p}, \inst{powerflow0039p}; \texttt{cos} also in \inst{hvycrash} \tabularnewline
\texttt{tanh} & \raggedright hyperbolic tangent & \raggedright \inst{ann_cumene_tanh} \tabularnewline
\bottomrule
\end{tabular}
\end{table}
```

## Move 3: GAMS/OSIL comparison by family, with methods

Main Appendix A.3 keeps a four-row summary (`tab:sem-gams`: exact /
identical; exact / catmix rows differ; evaluation; evaluation at 5
points). The table below keeps the method details per family that the
summary drops, and the `dtoc5` example of the objective-variable
substitution. The `catmix` coefficient strings are already in
`B4-chain-catmix.tex` (line 298); the audit-instance comparison is
already in `E-audit.tex` (lines 544-551).

```latex
MINLPLib's GAMS files minimize an objective variable defined by an objective row, while the OSIL files usually substitute it out; \inst{dtoc5}, for example, has 99,999 OSIL variables and 100,000 GAMS variables.
\Cref{tab:sem-gams-detail} gives, per family, how the GAMS form \reading{a} was compared with the OSIL form \reading{b} (summary in \cref{tab:sem-gams}).

\begin{table}[ht]
\centering
\small
\caption{Comparison of the GAMS form \reading{a} with the OSIL form \reading{b}, by family. ``Exact'' means a symbolic comparison with rational data; ``evaluation'' means agreement of the rows at random points in 50- or 60-digit arithmetic (evidence only).}
\label{tab:sem-gams-detail}
\begin{tabular}{@{}p{0.3\linewidth}p{0.4\linewidth}p{0.24\linewidth}@{}}
\toprule
\raggedright instances & \raggedright comparison & \raggedright result \tabularnewline
\midrule
\raggedright \inst{lnts50}--\inst{lnts400}, \inst{lukvle10}, \inst{chain50}--\inst{chain400}, \inst{ann_cumene_tanh}, KAN & \raggedright conversion by GAMS and evaluation; variables, types and bounds exact & \raggedright no difference \tabularnewline
\raggedright \inst{ex6_2_5}, \inst{ex6_2_7}, \inst{pricing050}, \inst{etamac}, \inst{pindyck}, \inst{hvycrash} & \raggedright evaluation at 5 points with 50 digits & \raggedright no difference \tabularnewline
\raggedright \inst{dtoc5}, \inst{optcdeg2} & \raggedright exact check of every row, objective coefficient and bound of the GAMS text & \raggedright identical \tabularnewline
\raggedright \inst{camshape100}--\inst{camshape800} & \raggedright exact, constants and rows & \raggedright identical \tabularnewline
\raggedright \inst{catmix100}--\inst{catmix800} & \raggedright exact & \raggedright rows differ (\cref{app:chain}); objective identical \tabularnewline
\raggedright \inst{powerflow0030p}, \inst{powerflow0039p}, \inst{powerflow0039r} & \raggedright exact, term by term & \raggedright identical \tabularnewline
\raggedright \inst{eg_int_s}, \inst{eg_disc_s}, \inst{eg_disc2_s} & \raggedright exact, OSIL decoder against a separately written GAMS reader & \raggedright identical \tabularnewline
\raggedright \inst{waterno2_06}--\inst{waterno2_24} & \raggedright exact, rows as polynomials, bounds, types and objective; two negative controls detected & \raggedright identical \tabularnewline
\bottomrule
\end{tabular}
\end{table}
```

## Move 4: per-family details of the data-reading check and of binary64 data

Main Appendix A.2 now says only that type B "occurs only in early author
scripts for lnts, lukvle10, dtoc5, camshape and optcdeg2, which use only
binary64-exact or exactly re-entered data". The per-family reasons, the
type of the `eg` fast mode, and the string counts under reading (c) (main
Appendix A.4 keeps only "none in lukvle10, two in each lnts and chain file,
up to 3,332 in eg_disc2_s") are below. Sources:
`development/data-semantics.md` (table and DS-3; `data_survey.py` row of
its check list).

```latex
\paragraph{Data reading by family.}
Type~B (\cref{app:semantics-codes}) occurs only in early author scripts, and it is harmless there: the \inst{lnts} certificate uses only binary64-exact data (its angle bound $\pm1.5707963267949$ is not used), \inst{lukvle10} has only integer data, \inst{dtoc5} enters $h=1/50000$ exactly, the \inst{camshape} strings are recovered exactly from their binary64 values by a shortest round trip, and the \inst{optcdeg2} script uses string literals.
The fast mode of the \inst{eg} search, which serves only as a cross-check (\cref{app:eg}), is of type~M.

\paragraph{Strings changed by binary64 rounding.}
Under \reading{c} every decimal $\sigma$ of an OSIL file is replaced by $\fl(\dval{\sigma})$.
The number of distinct strings that this changes is 0 in \inst{lukvle10}, 2 in each \inst{lnts} and \inst{chain} file, between 3 and 10 in \inst{dtoc5}, \inst{optcdeg2}, \inst{catmix}, \inst{camshape} and \inst{hvycrash}, and from 37 (\inst{pindyck}) to 3,332 (\inst{eg_disc2_s}) in the other files.
The KAN and \inst{ann_cumene_tanh} files contain between about 1,000 and 2,400 strings with 16 or 17 significant digits each, and \inst{powerflow0039r} contains 24; these strings are printed binary64 numbers.
```

## Material cut without a move (already in the supplement or not needed)

- Box "Results at a glance" (Section 1): every item is in the abstract or
  in contributions C1-C7; the three LINDO `rocket` bounds are now in C5.
- Notation box (Section 2): every entry is defined in the text of Section 2
  or in Section 5.5 (R, R_P).
- Appendix A provenance details now only in the supplement:
  powerflow shunt values, the case30 local value 576.8923368 and the
  ±0.26 rad angle rows (`B6-powerflow.tex` lines 21, 51-55); the
  `pindyck` initial-state values 18, 6.5, 0, 500 (`B5-small.tex` line
  432); the `waterno2` station B1 sign (`B8-waterno2.tex` line 55); the
  `catmix` coefficient strings for N = 200, 400, 800 (`B4-chain-catmix.tex`
  line 298); the audit GAMS/OSIL comparison numbers (`E-audit.tex` lines
  544-551). Appendix A points to these sections.
- Section 1.4, last paragraph: the near-closure figures for `camshape100`
  and `lnts50` stay in one sentence that points to Section 3.1, which
  carries them.
