# W6 review F-proofread: proofreading of the rendered main text and appendix headings

Scope: main text pp. 1-70 of `/tmp/dpaper/out/main.pdf` and the appendix
headings. Sources: `main.tex` and the `sections/*.tex` files that the build
inputs. Line numbers refer to the current sources.

## Checks run

These are targeted local checks. No project-wide verification was run.

- `main.log`: no overfull or underfull boxes, no undefined references or
  citations.
- `pdftotext` scans of pp. 1-70: no `??` or `[?]`; no missing spaces before
  reference numbers; no repeated words except math artifacts; no
  lower-case `section`/`theorem`/`appendix`/... before `\ref`; no
  cross-reference names without `~`.
- Sources: article use (`a`/`an`) before words and math; British spellings;
  `non-` hyphenation; operator names in italic math; empty `\paragraph`
  headings; proof pointers inside statement environments; and generic
  "LLM-style" vocabulary. The usual inflated words do not occur.
- Visual pass at 80 dpi over pp. 1-70 and the first page of every appendix.
- Scratch build of the proposed fixes for findings 2 and 7 in
  `/tmp/w6proof` (a copy, not the sources). The fix for finding 7 works:
  equation (8.4) then has its number beside the display, with no overfull
  boxes. For finding 2, moving the table environment does not change where
  the table lands, and `[b]` pushes it to p. 125, so only the added
  sentence is proposed.

## Verdict

The rendered main text is clean. There are no LaTeX errors, unresolved
references, overfull lines or wrong-case cross-reference names. Section,
Appendix, Theorem and the other environment names are capitalized
consistently. The prose has almost none of the usual generic phrasing.
The 15 findings below are all minor and local: one broken phrase in the
abstract, one display with a misplaced equation number, two empty run-in
headings, one proof pointer inside a lemma statement, an unreferenced
Table 1, one undefined symbol (`k`), several ambiguous antecedents or word
choices, small spelling inconsistencies and one appendix title that
undersells its content. None of them changes a mathematical statement.

## Findings

### F-proofread-1 (minor). Abstract: "an exact minimizer takes f_1(p,kappa)I^{O(1)}"

Location: `abstract.tex:17-18`; same ellipsis in `conclusion.tex:9`.

Problem: a minimizer does not "take" a running time. The unit (bit
operations) is also left implicit in the abstract.

Replacement, `abstract.tex:17-18`:
```latex
ratio $\kappa\ge\bar\kappa$, computing an exact minimizer takes
$f_1(p,\kappa)I^{O(1)}$ bit operations. The growth constant is never needed.
```
Replacement, `conclusion.tex:9`:
```latex
under point growth exact output takes $f_1(p,\kappa)(I+1)^{C_1}$ bit operations, without
```

### F-proofread-2 (minor). Table 1 is placed before its first reference and splits Theorem 1.2

Location: `intro.tex:122-125` (table environment at 125-183).

Problem: Table 1 appears at the top of p. 4, between items (c) and (d) of
Theorem 1.2. It is first mentioned only in the Organization paragraph on
p. 6, so the reader meets an unannounced table in the middle of a theorem.

Evidence: `main.aux` puts `tab:results` on p. 4 and `sec:related` on p. 6.
`intro.tex` mentions `tab:results` only at line 330. The scratch build
showed that moving the environment does not change its placement.

Replacement, `intro.tex:122-123`:
```latex
Remark~\ref{rem:setgrowth}); point growth in part~(c) only bounds the time
needed to reach this accuracy. Table~\ref{tab:results} lists these results
together with the extensions and lower bounds described below.
```

### F-proofread-3 (minor). "they bound only the running time"

Location: `intro.tex:199-201`.

Problem: kappa and kappa-bar do not bound the running time. They enter
the running-time bounds. The sentence can be misread.

Replacement:
```latex
(Section~\ref{sec:setting}). We do not claim that $\kappa$ or $\bar\kappa$
is moderate for the application models mentioned above; they enter only the
running-time bounds, never the validity of the output.
```

### F-proofread-4 (minor). "These are the main results." in the Section 7 roadmap

Location: `recourse.tex:25`.

Problem: the paper's main results are Theorems 1.1 and 1.2. Without
qualification, the sentence suggests that Theorems 7.2, 7.9 and 7.15 are
the main results of the paper.

Replacement: `(Theorem~\ref{thm:cr-oracle}). These are the main results of this section.`

### F-proofread-5 (minor). Empty run-in paragraph headings

Location: `recourse-convex.tex:11` (`\paragraph{Model.}`) and `:177`
(`\paragraph{The recourse theorem.}`).

Problem: each heading is followed by a blank line and then a titled
environment. The bold heading therefore stands alone on its own line on
p. 33 ("Model.") and p. 36 ("The recourse theorem."). These are the only
two such headings in the paper.

Replacement: delete both lines and the blank line after each. Definition
7.5 ("Convex recourse model") and Theorem 7.9 ("Certified convex
recourse") already carry these titles.

### F-proofread-6 (minor). Ambiguous "its part (d)"

Location: `recourse-mixed.tex:20-24`.

Problem: "its" can refer to Proposition D.4 or to Theorem 7.18, which is
cited just before. Both have a part (d) about checking without
optimization.

Replacement:
```latex
Proposition~\ref{prop:cr-greedy} in Appendix~\ref{app:recourse-cuts} states
the result precisely. It supplies, for concave--convex residuals, the exact
oracle required by CORE (Theorem~\ref{thm:cr-search} and
Proposition~\ref{prop:cr-growth}), with a certificate that part~(d) of
Proposition~\ref{prop:cr-greedy} checks without optimization. For $\mathcal R_+=\emptyset$ this is the class
```

### F-proofread-7 (minor). Equation (8.4) number pushed below the display

Location: `constraints.tex:452-457`.

Problem: the four definitions fill the line, so the number (8.4) drops
to a separate line under the display (p. 49). This is the only displayed
equation in the main text with this defect, according to a layout scan for
equation numbers on lines of their own.

Replacement (scratch build checked):
```latex
\begin{equation}\label{eq:tu-constants}
\begin{gathered}
C_{\hat H}=\max\Bigl\{1,\max_{i,k\le n_c}\lvert(\hat H_{xx})_{ik}\rvert\Bigr\},\qquad
R_{\mathrm{TU}}=(2n_cC_{\hat H})^{n_c},\\
\Omega_{\mathrm{TU}}=\Delta(\Delta_\eta R_{\mathrm{TU}})^2,\qquad
\tau_{\mathrm{TU}}=\frac1{4m'\Delta_\eta R_{\mathrm{TU}}} .
\end{gathered}
\end{equation}
```

### F-proofread-8 (minor). Two epsilon glyphs for two accuracies in Remark 8.11

Location: `constraints.tex:536-557`.

Problem: the remark writes Bienstock and Muñoz's tolerance as `\epsilon`
(ϵ) and the accuracy of TU-GRID as `\varepsilon` (ε). Item (iv) then
compares "an exponent p/2 in 1/ε against their ω+1 in 1/ϵ". The convention
is never stated, so a reader may take the second glyph for a typo.

Replacement, `constraints.tex:536-538`:
```latex
objective $c$, constraints of degree at most $\pi$ and coefficient $1$-norm at
most $\mathfrak F$, a constraint intersection graph of treewidth $\omega$ and a
tolerance $\epsilon$ (we keep their symbol, distinct from our accuracy
$\varepsilon$), a
```

### F-proofread-9 (minor). Ambiguous "it shows" after Proposition 9.1

Location: `optsets.tex:65-67`.

Problem: "it" follows "this instance", but the claim is made by the
proposition.

Replacement:
```latex
The proof is in Appendix~\ref{app:proximal}. Other methods solve this
instance easily; the proposition shows that the failure comes from the single
center, not from conditioning. Replacing hulls by unions of
```

### F-proofread-10 (minor). The proof pointer is typeset inside Lemma 9.10

Location: `optsets.tex:379`.

Problem: "The proof is in Appendix~\ref{app:proximal}." comes before
`\end{lemma}`. It is therefore set in italics as part of the statement, at
the top of p. 56. Everywhere else the pointer follows the environment.

Replacement: move line 379 below `\end{lemma}` (line 380), so the lines
read:
```latex
\end{enumerate}
\end{lemma}
The proof is in Appendix~\ref{app:proximal}.
```

### F-proofread-11 (minor). Undefined symbol k in the discussion of Proposition 10.6

Location: `limits.tex:353-357` and `:362`.

Problem: "with κ polynomial in kN_0" and "bounded by a polynomial in kN_0"
use `k`, the number of color classes. It is defined only in Appendix G.2
(`appendix-lbproduct.tex:78`). In the main text, `k` has other meanings,
for example the core size in Section 7.4.

Replacement, `limits.tex:353-355`:
```latex
The proof is in Appendix~\ref{app:lbproduct}. It encodes multicolored clique
with $k$ color classes in the standard way, with one integer variable of
domain size $N_0$ per color class and one pair constraint for each pair of classes.
```

### F-proofread-12 (minor). "It is a limit of filtered grids" can be read as a mathematical limit

Location: `limits.tex:466-468`.

Problem: in a paper about sequences of grids, "a limit of filtered grids"
reads like the limit of a sequence. The intended meaning is "limitation".

Replacement:
```latex
(Theorem~\ref{thm:cells}). The proposition concerns a continuum of optimal
coordinate values. It shows a limitation of filtered grids, not a hard
problem: here $F$ is a sum of squares.
```

### F-proofread-13 (minor). Tense shift in E6

Location: `computation.tex:277-279`.

Problem: "proved a candidate optimal, and on one no candidate is proved
optimal" switches from past to present tense within one sentence.

Replacement:
```latex
it. On the other 29 instances growth and $\kappa$ remain unknown; on 28 of
them the localized test of Proposition~\ref{prop:local} proved a candidate
optimal, and on the remaining one no candidate was proved optimal. For $n=8$ all candidates
```

### F-proofread-14 (minor). Spelling inconsistencies

Locations and evidence:
- `computation.tex:9`: "modelled" is British spelling. The rest of the
  paper uses American spelling ("behavior", "neighbor", "center"; 86
  occurrences).
- `constraints.tex:17`, `:508` (title of Section 8.7) and `:525`:
  "non-uniform", but `recourse-balanced.tex:73` has "nonuniform".
- `related.tex:92`: "non-asymptotic". Every other `non` compound in the
  paper is closed: nonconvex (15), nonnegative (23), nonempty (33),
  nonzero (19), nonunique, nondegenerate, nonseparable.

Replacements: "modelled" → "modeled"; "non-uniform" → "nonuniform" (three
times, including the title `\subsection{The uniform mesh: cost and
nonuniform alternatives}`); "non-asymptotic" → "nonasymptotic".

### F-proofread-15 (minor). The title of Appendix F undersells its content

Location: `appendix-proximal.tex:1`.

Problem: the heading "Proofs for Section 9" does not cover all of the
appendix. Besides proofs, it contains new supplementary results: Example
F.1 (tilted and disconnected optimal sets), Remark F.3 (a false guess) and
Proposition F.4 (hardness of discovery within the diagonal certificate
class). The parallel Appendix G is titled "Proofs and supplements for
Section 10".

Replacement:
```latex
\section{Proofs and supplements for Section~\ref{sec:optsets}}\label{app:proximal}
```

## Checked and not reported

- The appendix headings are capitalized consistently, render without
  defects, follow the section order and match the "Organization"
  paragraph.
- No float sits far from its first reference, except Table 1 (finding 2).
  Figures 1 and 2 and Table 3 sit on pp. 66-67, next to their references.
  Tables 4-6 are appendix tables near their appendix text.
- The counts in Section 11 add up: 20, 18 and 15 instances in E4; 21 = 12 +
  9 in E5; 40 = 11 + 29 in E6; 30 and 12 in S1; seven implementation
  differences in Appendix H; the message-piece column of Table 3.
- The "X, not Y" constructions and the "What is new is ..." sentences are
  informative contrasts in context. Only the ambiguous one is reported
  (finding 12).
