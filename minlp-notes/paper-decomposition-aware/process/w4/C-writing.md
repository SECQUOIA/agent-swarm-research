# W4 review C-writing: writing and structure

Reviewer key: C-writing. Scope: writing and structure of the whole paper, judged as a
submission to Mathematical Programming (Series A). Sources read: `main.tex`,
`macros.tex`, every file in `sections/` that is input by the build (main text in full,
appendices skimmed for structure and prose). Page and number references come from
`/tmp/dpaper/out/main.aux` and the 123-page PDF (main text pp. 1-80, references
pp. 80-91, appendices pp. 92-123). Line numbers refer to the `.tex` files as of
2026-10-03 12:04. The earlier reports (`process/w2/R6-writing.md`, `R9-referee.md`,
`process/w3/reports/front.md`, `process/w3/CONVENTIONS.md`) were read only to check
whether earlier issues were fixed and to avoid re-reporting deliberate decisions. The
decision to keep one paper (CONVENTIONS, first paragraph) is respected below; finding 1
asks only for the "focused main text" that CONVENTIONS itself adopted (Option B).

## Verdict

The prose is plain, precise and nearly free of filler: a search for the usual inflated
or generic words (crucially, notably, importantly, novel, significant, remarkably,
clearly, essentially, etc.) found none in the main text. There are no drafting leftovers,
untitled remarks, British spellings, overfull boxes or undefined references, and the
algorithm names and the terms "nodes per coordinate" and "table entries" are used
consistently. The main result is easy to find (Theorem 1.1 on p. 2), and the
contribution statements are precise. The main weaknesses are structural. The main
text is 80 pages, 3 pages longer than before the revision, although CONVENTIONS
adopted a focused main text. The extensions (Sections 7-9, 31 pages) still outweigh
the core (Sections 3-6, 21 pages). The introduction takes more than five pages, plus a
full-page table, and its extension paragraphs are hard to read. The growth-scope
caveat that the revision added is worded so that it credits growth with a restriction
that holds at every minimizer. It also leaves out the global part of the restriction.
Several summaries are repeated three to five times. All findings below have concrete
replacement text. None changes a theorem.

## The 10 most valuable improvements

1. Move about 13 pages of secondary material and long proofs of secondary results
   to the appendices (list in C-writing-1), so the main text is about 67 pages and the
   extensions no longer outweigh the core.
2. Replace the three extension paragraphs and the long catalogue of further limits in
   the introduction with the shorter versions in C-writing-2.
3. Correct the growth-scope caveat in the introduction and in Remark 3.4
   (C-writing-3). It should say that minimality alone puts negative curvature at active
   bounds or integer coordinates. Growth adds a quantitative condition on the interior
   Hessian block and excludes near-optimal distant local minima.
4. Use the 250-word abstract in C-writing-4. It also states the scope caveat.
5. Remove the repeated summaries: the lower-bound sentence (five copies), the
   parameterized-form paragraph (two copies), the S1 numbers (two copies), the
   novelty claim (two copies) and the ETH definition (two copies) (C-writing-5,
   C-writing-6).
6. Replace the bullet list that opens Section 10 with a roadmap tied to Theorem 1.2
   (C-writing-9).
7. Move the sharpness block (`growth-sharp.tex`) after Lemma 5.11. This removes two
   forward references and lets Section 5 go directly from Lemma 5.5 to CT and
   Theorem 5.9 (C-writing-7).
8. State the paragraph after Theorem 4.7 as a corollary, because the proof of
   Theorem 5.9 relies on it (C-writing-8).
9. Resolve the notation that contradicts Table 2 or is undefined: the four uses of
   `J`, `s_i` in Section 6, the dummy `kappa` in `f(p,kappa)`, the bracket notation in
   Corollary 6.19 and the undefined `C_2` in Section 6.6 (C-writing-10 to C-writing-12).
10. Retitle the paper so that the title names the main result (C-writing-15), and
    fix the smaller presentation items: the single subsection of the introduction,
    appendix titles, experiment labels, table captions, Table 1 cells, and
    "minimizer" versus "optimizer" (C-writing-16 to C-writing-21).

## Findings

### C-writing-1 (major). The main text is still 80 pages, and the extensions outweigh the core

Location: whole paper (`main.tex` 11-25). Page budget from `main.aux`:
§1 pp. 1-7, §2 7-10, §3 10-13, §4 13-17, §5 17-23, §6 23-31, §7 31-44 (27 numbered
items), §8 44-53, §9 53-62, §10 62-71, §11 71-78, §12 78-80.

Problem. CONVENTIONS adopted Option B of R6: "a focused main text, with secondary
results and long proofs moved to appendices". R6 set a target of about 60 pages
before the references. The W2 build had about 77 pages of body. The current build
has 80. The appendices grew from 11 to 32 pages, but the main text did not shrink.
The core (§§3-6) takes 21 pages and the three extensions (§§7-9) take 31. An MP
referee will again ask for focus (R9 raised this as R1).

Fix. Keep one paper and every proved result. Move the following blocks to the
appendix of their section. In the main text, keep the statement or a two- to four-line
summary with a pointer. Estimated savings are in parentheses.

| Block | Source lines | Keep in main text | Saving |
|---|---|---|---|
| Setup and Prop. 7.5 (grid min-marginals are not certified recourse) | `recourse-local.tex` 85-147 | 4 lines: statement of the two families' consequence and pointer | ~1 p |
| Recognition of affine selectors and limits of recourse curvature (Thm 7.12, Prop 7.13 and discussion) | `recourse-convex.tex` 282-345 | 2 sentences each | ~1 p |
| Remark 8.2, Prop. 8.3, Example 8.11 | `constraints.tex` 86-118, 382-406 | one sentence on how to check (8.2) | ~1 p |
| §8.6 TU exact output (Algorithm 8.13, Thm 8.14) | `constraints.tex` 477-571 | 6 lines: constants, acceptance with Omega_TU, row snapping, one-sentence theorem | ~1.2 p |
| Prop. 8.15, its numerical illustration, Example 8.16 | `constraints.tex` 590-650 | 3 sentences (the intro of §8 already states the conclusion) | ~1 p |
| Proof of Prop. 9.1 | `optsets.tex` 65-127 | none | ~1 p |
| Proofs of Lemma 9.6 and Cor. 9.8 | `optsets.tex` 303-345, 412-443 | none | ~1 p |
| PROX, Lemma 9.13, DISC and the discussion after Thm 9.15 | `optsets.tex` 538-622 | Lemma 9.10, a 4-line description of DISC, Thm 9.15, statement of Prop 9.16 | ~1.3 p |
| Proofs of Props 10.7, 10.8, 10.9, 10.10 | `limits.tex` 422-466, 502-545, 576-607, 647-660 | statements and the discussion paragraphs | ~2.5 p |
| Bullet list opening §10 | `limits.tex` 13-45 | roadmap of C-writing-9 | ~0.4 p |
| Numeric part of the proof of Lemma 5.5 | `growth.tex` 162-174 | first paragraph of the proof | ~0.3 p |
| Introduction (C-writing-2), §6.5 (C-writing-6), Remark 5.10 (C-writing-5) | see those findings | | ~1.5 p |

Total about 13 pages, giving a main text of about 67 pages. The main line (§§3-6 and
§§10.1-10.3) stays fully proved in the main text.

### C-writing-2 (major). The introduction is too long, and its extension paragraphs are hard to read

Location: `intro.tex` 194-217 ("Thus, ..."), 219-246 (Conditional recourse), 248-268
(Coupling constraints), 270-294 (Several minimizers), 299-370 (Table 1). The
introduction runs from p. 1 to p. 7. "Results" (§1.1) alone is about five pages
including the full-page Table 1.

Problem. R9 asked for a results section of at most two pages, and R6 asked for an
introduction of at most three pages. The three extension paragraphs read like
condensed section abstracts. They contain 10, 7 and 5 cross-references, and they use
terms that are defined only later: "value factors", "global overlay of the pieces",
"certified cancellation", "core point", "level-0 grid", "endpoint dynamic program",
"Bellman residuals". Table 1 then repeats the same results. The sentence at
194-217 restates Theorem 1.2 in words and then lists five further limits in one
sentence of about 110 words. The first item of that list (exponentially large
messages, 203-204) repeats the "Exact messages" paragraph six lines above
(152-158).

Fix. Replace 194-217 with:

```latex
Thus, unless P${}={}$NP, neither parameter can be dropped and the dependence
on $\kappa$ cannot be polylogarithmic; under ETH the dependence on $p$ is
exponential even for $\kappa\le2$; and under rETH the exponent of $\kappa$
cannot be $o(p)$, already for integer box quadratics, whereas
Theorem~\ref{thm:intro-main}(b) has exponent $p/2+O(1)$. The same statements
hold for $\bar\kappa\le\kappa$. In the value-oracle model of part~(d), CT
attains the exponent $p/2$ up to a factor $(C\sqrt p\log(p+2))^p$ and the
number of stages (Remark~\ref{lim:rem:oracle}). Section~\ref{sec:limits} also
shows that growth towards a continuum of minimizers does not bound filtered
grids and cannot be exploited by value and derivative queries, that local
affine equalities make the problem NP-hard at bag size three and
$\kappa=1$, and that matching separator moments of any finite order gives no
local error bound in terms of negative curvature. As far as we know, the
expanding-box chain, the unique-minimizer hardness with explicit growth (a
refinement of \cite[Remark~2]{DelPiaKhajavirad2026}), the rETH bound and the
moment obstruction are new. The other statements adapt standard
constructions, among them the running-sum encoding of Subset Sum of Bienstock
and Mu\~noz \cite{BienstockMunoz2018} (see also
\cite[Example~1.1]{CifuentesParrilo2016}).
```

Replace 219-246 with:

```latex
\paragraph{Conditional recourse.}
The condition number is built from diagonal curvature, so a stiff convex
term inflates it even when the subproblem it defines is easy. We therefore
also minimize exactly over some variables for fixed values of the others;
we call this \emph{recourse}. Partial minimization preserves upper
coordinate curvatures and growth, so the certificate and the growth analysis
apply to the value function (Theorem~\ref{thm:valuefn}). Two classes have
exact recourse with certificates. For private convex quadratic blocks, the
coordinate curvature of their contribution to the value function is
certified by piecewise-affine optimal responses, and the certified reduction
is the largest possible for the block (Theorem~\ref{thm:cv} and
Proposition~\ref{prop:vf-curv}). Residual problems that are concave in each
coordinate and submodular after sign changes are solved by one minimum cut
for each value of the remaining coordinates, so only those coordinates are
gridded (Theorems~\ref{thm:cr-oracle} and~\ref{thm:cr-search}). For balanced
box quadratics the grid problem itself is a minimum cut, so no tree
decomposition is needed (Theorem~\ref{thm:balanced}). Parametric quadratic
programming and cut representations of submodular functions are classical;
what is new is the curvature and growth accounting that keeps them inside
the certificate. Recourse does not reduce the parameter to the ratio of
negative curvature to growth in general (Proposition~\ref{prop:cv-limit}).
```

Replace 248-268 with the following. It keeps the CONVENTIONS wording. The sentence
on non-uniform alternatives is already in the introduction of §8
(`constraints.tex` 15-18).

```latex
\paragraph{Coupling constraints.}
The certificate rests on rounding each coordinate independently, which
breaks under coupling constraints. Totally unimodular (TU) coupling
constraints with mesh-aligned data admit exactly feasible correlated
rounding, which restores the certificate and, for quadratics, exact output
(Section~\ref{sec:constraints}). Under set growth with finitely many optimal
values per coordinate, the algorithm is polynomial for fixed width when the
condition number $\kappa_c$, the box widths measured in mesh units ($s/\eta$)
and the number $r$ of optimal values per coordinate are polynomially bounded
(Theorem~\ref{thm:tu-approx}). It is not fixed-parameter tractable, because
its meshes are uniform, and its pseudopolynomial first grid cannot be removed
unless P${}={}$NP (Proposition~\ref{lim:prop:constraints}). Bienstock and
Mu\~noz \cite{BienstockMunoz2018} treat arbitrary polynomial constraints with
a feasibility tolerance; our class is narrower but exactly feasible
(Remark~\ref{rem:tu-bm}).
```

Replace 270-294 with:

```latex
\paragraph{Several minimizers.}
One graded grid can need exponential time already with two isolated
minimizers (Proposition~\ref{prop:twocenters}). If the optimal set is finite,
unions of uniform cells keep $O(r\sqrt{n\kappa_S})$ nodes per coordinate,
where $r$ bounds the number of optimal values of a coordinate and
$\kappa_S=\max\{1,L/g_S\}$ uses the growth constant $g_S$ towards the optimal
set (Theorem~\ref{thm:cells}). For quadratics with nonpositive diagonal on a
mixed box, a dynamic program over the box endpoints describes the whole
optimal set as a constraint problem on the same tree decomposition, from
which uniqueness, the dimension of the optimal set and, if it is finite, the
number of minimizers follow in $2^{O(p)}\poly(I)$ bit operations
(Theorem~\ref{thm:endpointset} and Corollary~\ref{cor:facecsp}). This
combines Rosenberg's face description \cite{Rosenberg1972} with zero-residual
descriptions of optimal labelings \cite{WainwrightJaakkolaWillsky2005,Werner2007};
the treatment of strictly concave coordinates and mixed boxes and the
factored form are new. For continuous box quadratics with a classical
diagonal Lagrangian certificate \cite{JeyakumarRubinovWu2006,LiWuQuan2015},
a minimizer and the optimal set are found in $f'(p,\kappa_S)\poly(I)$ bit
operations without knowledge of $g_S$ (Theorem~\ref{thm:diagdiscovery}).
```

Table 1: see C-writing-20.

### C-writing-3 (major). The growth-scope caveat credits growth with a restriction that holds at every minimizer, and it leaves out the global restriction

Location: `intro.tex` 137-145; `setting-growthcert.tex` 59-66 (Remark 3.4). The
wording comes from CONVENTIONS §5.

Problem. The paragraph opens "Growth restricts where nonconvexity can occur" and
concludes "The nonconvex instances covered by our bounds therefore have their
negative curvature in directions that involve active bounds or integer coordinates".
But at every global minimizer of a box QP, the block `H_{J0J0}` of the continuous
coordinates strictly inside their bounds is positive semidefinite. The paper's own
Lemma 3.3(b) says so, first sentence: "let x* be a minimizer. Then zeta_{J0}=0 and
H_{J0J0} ⪰ 0". So negative curvature lies in directions involving active bounds or
integer coordinates at every minimizer, with or without growth. Growth adds
two quantitative restrictions that the paragraph does not state:

* (local) `H_{J0J0} ⪰ 2gI`, so `kappa >= L/g >= 2L/lambda_min(H_{J0J0})` whenever
  `J0` is nonempty: the interior block must have smallest eigenvalue comparable
  to the largest diagonal curvature;
* (global) every other local minimizer `x'` must satisfy
  `F(x')-F* >= g||x'-x*||^2`, so nearly tied local minima far from `x*` force a large
  `kappa`. Section 3 says this for integer assignments (`setting.tex` 128-130), but
  the introduction does not.

These two restrictions are what a reader needs in order to judge how often `kappa` is
moderate.

Fix. Replace `intro.tex` 138-145 (from "Growth restricts" to
"(Example~\ref{ex:family}).") with:

```latex
At every minimizer of a box QP, the Hessian block $H_{J_0J_0}$ of the
continuous coordinates strictly inside their bounds is positive
semidefinite, so negative curvature can occur only in directions that
involve active bounds or integer coordinates; this holds with or without
growth. Growth adds two quantitative restrictions
(Lemma~\ref{lem:growthcert}). Locally, point growth forces
$H_{J_0J_0}\succeq2gI$, so $\kappa\ge2L/\lambda_{\min}(H_{J_0J_0})$ whenever
some continuous coordinate is strictly inside its bounds, and an instance
whose minimizer lies in the interior of a continuous box has point growth
only if it is strongly convex; weighted growth gives
$H_{J_0J_0}\succeq2\gamma\diag(L_i)$. Globally, every other local minimizer
$x'$ must satisfy $F(x')-\OPT\ge g\norm{x'-x^*}^2$, so nearly tied local
minima far apart force a large condition number. Within these limits the
covered instances can be far from convex and can have exponentially many
strict local minima (Example~\ref{ex:family}).
```

Keep 145-150 ("The condition number can be large: ..."). In Remark 3.4 replace
`setting-growthcert.tex` 60-66 with:

```latex
For a box QP, the Hessian block of the continuous coordinates strictly inside
their bounds at a minimizer is positive semidefinite, so at every minimizer,
with or without growth, negative curvature lies in directions that involve
active bounds or integer coordinates. Point growth makes the block positive
definite, $H_{J_0J_0}\succeq2gI$, hence $\kappa\ge2L/\lambda_{\min}(H_{J_0J_0})$
if $J_0\ne\emptyset$; weighted growth bounds it below by
$2\gamma\diag(L_i)_{i\in J_0}$ (Lemma~\ref{lem:growthcert}(b)). Instances
with active bounds or integer coordinates can still have a small condition
number and exponentially many strict local minima (Example~\ref{ex:family}).
```

Update CONVENTIONS §5 accordingly. The derivation `g <= lambda_min/2` comes from
`H_{J0J0} ⪰ 2gI` in Lemma 3.3(b), and `kappa >= L/g` comes from the definition of
`kappa`.

### C-writing-4 (minor). The abstract is slightly over the MP limit and omits the scope caveat

Location: `abstract.tex` 2-26.

Problem. The abstract has 256 words, counting each math expression as one word
(`process/w4/checks/cwriting_wordcount.py`). MP asks for 150-250. The sentence at
16-20 has about 60 words and four nested qualifiers. "Two quantities make tree
decompositions useful" (5-6) reads as a fact about the world rather than as a result of
the paper. The abstract says nothing about how restrictive growth is (see
C-writing-3).

Fix. Replace the abstract with the following text, which has 252 words counted the
same way (file `process/w4/checks/cwriting_abstract_proposed.tex`). It is about 250
words if `$2L/\kappa$` is written as `$2\max_iL_i/\kappa$`.

```latex
Small treewidth alone does not make nonconvex mixed-integer optimization
tractable: box-constrained nonconvex quadratic programming is strongly
NP-hard at treewidth two. We show that two further quantities make tree
decompositions useful for certified global optimization: upper bounds $L_i$
on the curvature along each coordinate, and quadratic growth. Subtracting
$L_iw^2/8$ at each grid node, where $w$ is the longest adjacent grid
interval, turns exact dynamic programming over a product grid into a valid
lower bound. Min-marginals then filter the grids, and the stage grids form a
certificate that is checked by recomputation and needs no growth assumption.
Under growth in the norm weighted by the $L_i$, graded grids keep
$O(\sqrt{\bar\kappa}\log(n+2))$ nodes per coordinate at every accuracy, where
$\bar\kappa$ is a scale-invariant ratio of curvature to growth. For rational
mixed-integer quadratic programs on a box with bag size $p$ and input length
$I$, this certifies accuracy $2^{-q}$ in $f(p,\bar\kappa)(I+q+1)^5$ bit
operations; under growth at a unique minimizer, with the Euclidean ratio
$\kappa\ge\bar\kappa$, an exact minimizer takes $f_1(p,\kappa)I^{O(1)}$. The
growth constant is never needed. A moderate $\kappa$ requires the Hessian
block of the interior continuous coordinates to have smallest eigenvalue at
least $2\max_iL_i/\kappa$, and distant local minima to be clearly worse than
the global one. Unless P${}={}$NP, neither parameter can be dropped and the
dependence on $\kappa$ cannot be polylogarithmic; under the randomized
exponential-time hypothesis its exponent cannot be $o(p)$. We extend the
method to exact partial minimization, totally unimodular coupling
constraints and several minimizers, and test an exact-arithmetic
implementation with an independent checker.
```

### C-writing-5 (minor). The same summaries are repeated several times

Locations and fixes:

(a) The lower-bound sentence ("unless P=NP neither parameter can be dropped ...;
under ETH ...; under rETH ...") appears in `abstract.tex` 20-23, `intro.tex` 194-198
(right after Theorem 1.2, which states it), `growth.tex` 279-284 (Remark 5.10),
`limits.tex` 15-23 and `conclusion.tex` 13-18. Keep the abstract, the introduction
and the conclusion. In Remark 5.10 replace 279-284 with
"Theorem~\ref{thm:intro-lower} gives the matching lower bounds." Replace the
§10 copy as in C-writing-9.

(b) The paragraph "Parameterized form" (`intro.tex` 124-131) and the first half of
Remark 5.10 (`growth.tex` 266-273) are nearly identical. Replace `intro.tex` 125-131
(up to "(Remark~\ref{rem:fpt}).") with:

```latex
The number $\bar\kappa$ is a property of the instance, which CT neither
receives nor computes; since $f$ is increasing in its second argument,
part~(b) is a fixed-parameter bound in $p$ and $\lceil\bar\kappa\rceil$
(Remark~\ref{rem:fpt}).
```

Replace Remark 5.10 (`growth.tex` 266-284) with:

```latex
The weighted condition number $\bar\kappa$ is a real parameter of the
instance: it is not part of the input, and CT never computes it. Since $f$ is
increasing in its second argument, the bound is at most
$f(p,\lceil\bar\kappa\rceil)(I+q+1)^5$, a fixed-parameter bound in the
parameters $p$ and $\lceil\bar\kappa\rceil$, which the algorithm does not
need to know. The exponent $5$ reflects schoolbook arithmetic and depends on
neither parameter, the factor $\lceil\log_2(n_P+2)\rceil^p$ is absorbed
by~\eqref{eq:logabsorb}, and no bound on the number of bags containing a
coordinate, on Hessian norms or on the number of local minima is used. If
only a treewidth bound is known, the decomposition of \cite{Korhonen2021}
gives the same result with $p=2\,\mathrm{tw}+2$.
Theorem~\ref{thm:intro-lower} gives the matching lower bounds.
```

(c) The novelty claim "no earlier result gives a running time of the form
f(p,kappa)poly(I+q) ..." appears in `intro.tex` 109-113 and again in `related.tex` 54-56.
Delete the sentence in `related.tex` 54-56.

(d) ETH is defined twice, with different symbols: `intro.tex` 161-165 ("for some
delta>0, 3-SAT with m variables cannot be solved in time 2^{delta m}") and
`limits.tex` 282-286 ("for some c>0, ... on n' variables in time 2^{cn'}"). Replace
`limits.tex` 282-286 with "We use ETH and rETH as stated in
Section~\ref{sec:intro-results}; for rETH the randomized algorithms have error
probability at most $1/3$ \cite{DellEtAl2014}."

(e) The exponentially large messages appear twice within the introduction
(152-158 and 203-204); the replacement in C-writing-2 removes the second copy.

### C-writing-6 (minor). Experimental results are reported in a theory subsection and again in Section 11

Location: `exact-localized.tex` 131-139, duplicating `computation.tex` 335-357.

Problem. §6.5 repeats the S1 numbers: 29 of 30 instances, nine stages, five stages,
40 to 72 stages, 542 stages. §11.6 reports the same numbers with their context.

Fix. Replace `exact-localized.tex` 131-139 (up to "used up to 542.") with:
"In the experiments of Section~\ref{sec:comp-localized} the test accepts the face
candidate within nine stages on 29 of 30 random mixed-integer instances, long before
the certified gap reaches the threshold of Proposition~\ref{prop:accept}." Keep
139-142 (the exclusion-box credit).

### C-writing-7 (minor). The sharpness block interrupts Section 5 and contains forward references

Location: `growth.tex` 179 (`\input{sections/growth-sharp}`); `growth-sharp.tex` 9-10,
35-37.

Problem. The sharpness block (Prop 5.6, Cor 5.7 and the UC paragraph) sits between
Lemma 5.5 and CT. It refers forward to Theorem 5.9 and Remark 5.10 ("which makes
Theorem~\ref{thm:approx} a fixed-parameter bound (Remark~\ref{rem:fpt})"). Cor 5.7
uses "the common mesh $h_j=s2^{-j}$", which is introduced only in Lemma 5.11. A
reader goes from the localization lemma through a page of lower-bound material
before reaching the algorithm and the main theorem.

Fix. Move `\input{sections/growth-sharp}` from `growth.tex` 179 to just before
`\subsection{Examples}` (`growth.tex` 335), under a new heading
`\subsection{Sharpness of the localization radius}`. In `growth-sharp.tex`, change
"run the stages of TRIAL without a cap, with the common mesh $h_j=s2^{-j}=2^{1-j}$"
to "run the stages of CT with a common mesh (Lemma~\ref{lem:commonmesh}) without a
cap, with $h_j=2^{1-j}$". The references to Theorem 5.9 and Remark 5.10 then point
backward.

### C-writing-8 (minor). A main proof relies on an unnamed paragraph

Location: `grids.tex` 274-282; used in `growth.tex` 224-225 ("validity follows from
Theorem~\ref{thm:certificate} and the paragraph after it").

Problem. The statement that a run of filtering with feasible thresholds produces a
valid path certificate is proved in running text. Theorem 5.9(a) and §6.5 depend
on it.

Fix. After Theorem 4.7 insert:

```latex
\begin{corollary}[Filtering runs give valid certificates]\label{cor:filtercert}
Suppose $G^{(0)}$ spans $X$, each $G^{(j+1)}$ spans the subbox obtained from
$G^{(j)}$ by the filtering step with a threshold $U_j$ that is the value of a
feasible point, $\beta$ is the corrected minimum of the last grid, and
$\hat x\in X$. Then $(G^{(0)},\dots,G^{(k)},\beta,\hat x)$ is a valid path
certificate.
\end{corollary}
\begin{proof}
[the present text of grids.tex 277-282, from "By Proposition~\ref{prop:filter}"
to "exceeds $U_j\ge\beta$."]
\end{proof}
```

Keep 283-290 as discussion. In `growth.tex` 224-225 write "validity follows from
Corollary~\ref{cor:filtercert}".

### C-writing-9 (minor). Section 10 opens with a bullet list that repeats the introduction

Location: `limits.tex` 3-45 (the "close to necessary" at line 12, the itemize at 13-45).

Problem. The list restates Theorem 1.2 and the introduction's list of further limits,
which is the fourth copy of the lower-bound summary. Two of its items point to results
proved in other sections (Prop 9.1, Prop 7.5). "Close to necessary" (line 12) is
vague, because Theorem 1.2 says exactly what is necessary.

Fix. Replace `limits.tex` 3-45 with:

```latex
The algorithms of Sections~\ref{sec:grids}--\ref{sec:exact} rest on four
hypotheses: a product domain, upper bounds on coordinate curvature, weighted
or point growth, and a correction that charges for rounding every
coordinate. Sections~\ref{sec:recourse}--\ref{sec:optsets} relax some of
them. This section proves Theorem~\ref{thm:intro-lower} and shows what fails
when a hypothesis is dropped without such a replacement.
Section~\ref{sec:limits-conditioning} proves part~(a),
Section~\ref{sec:limits-oracle} part~(d), and
Section~\ref{sec:limits-width} parts~(b) and~(c).
Section~\ref{sec:limits-messages} shows that exact piecewise-quadratic
messages can be exponentially large, Section~\ref{sec:limits-setgrowth} that
set growth does not bound filtered grids and cannot be exploited by value
and derivative queries, Section~\ref{sec:limits-constraints} that product
domains are essential, and Section~\ref{sec:limits-local} that local
corrections and finite-order local moments do not suffice.
```

Keep 46-50 (the Del Pia-Khajavirad paragraph).

### C-writing-10 (minor). Notation contradicts Table 2 or reuses reserved symbols

Locations and fixes:

(a) Table 2 claims to list "symbols that keep one meaning throughout the paper"
(`setting.tex` 146-147), but lists `J` twice (174-175: grid interval; stage limit). In
§6, `J` is also the free set of REC (`exact.tex` 187-232) and of the face candidate
(`exact-localized.tex` 89-99), and the stage limit (`exact.tex` 465). Fix: rename the
stage limit to `j_max` (`growth.tex` 42-57, 189-193, 226-256, 317-318;
`appendix-growth.tex`; `exact.tex` 465; `computation.tex` 27; and the last level `J`,
`J_ex` of `constraints.tex` 417-436, 553-563 as `j_max`, `j_ex`). Delete row 175 of
Table 2.

(b) In §6 a minimizer is called `s` and its coordinates `s_i` (`exact.tex` 64-67, 72,
102, 135-140, 204-226). Table 2 reserves `s_i` for the widths `u_i-\ell_i`, and line
102 reads "fixed at $s_i\in\{\ell_i,u_i\}$". Fix: rename the minimizer to `x^\circ`
(and `s'` to `x^{\circ\prime}`) in Definition 6.2, Lemma 6.3, the proof of Corollary 6.4,
Remark 6.5 and the proof of Lemma 6.8.

(c) `f(p,\kappa)=c_0(c_1p\sqrt\kappa)^p\kappa(1+\log_2\kappa)^2` defines `f` with
`kappa` as a dummy argument. It is then applied to `\bar\kappa`, while `kappa` denotes
the Euclidean condition number elsewhere in the same statement (`intro.tex` 96,
`growth.tex` 212, `limits.tex` 188, `conclusion.tex` 54). Fix: write
`f(p,t)=c_0(c_1p\sqrt t)^p\,t\,(1+\log_2t)^2` in all four places.

### C-writing-11 (minor). The bracket notation in Corollary 6.19 conflicts with the Iverson bracket of Lemma 5.5

Location: `exact-localized.tex` 112-116; compare `growth.tex` 135-137.

Problem. Lemma 5.5 defines `[i\in I_Z]` as 1 or 0. Corollary 6.19 writes
`\min\{\tfrac12[I_Z\cap P\ne\emptyset],\ \dots\}` and says "a bracketed term is
omitted when its condition fails". Read with the Iverson meaning, a failed condition
makes the minimum 0 and `h^*=0`.

Fix. Replace 112-116 with:

```latex
h^*=\frac{1}{\sqrt{n\kappa}}\min\mathcal M ,
```

followed by "where $\mathcal M$ contains $\frac12$ if $I_Z\cap P\ne\emptyset$,
$\frac16\delta_X$ if $I_C\cup(I_Z\setminus P)\ne\emptyset$, and
$\lambda_A/(5\Gamma)$ if $A\ne\emptyset$ ($\mathcal M$ is never empty)." The set is
nonempty: if `I_Z ∩ P` is empty, then `I_C ∪ (I_Z\P) = [n]`.

### C-writing-12 (minor). An undefined constant in the main text

Location: `exact.tex` 495-497.

Problem. "$B_\lambda=\lceil\log_2\max\{2,C_2/\lambda_A\}\rceil$": `C_2` is defined
only in Appendix B.2 (`appendix-boundary.tex` 10-13).

Fix. Replace 495-497 ("The cost carries a term ... at the active bounds;") with "The
cost carries a term logarithmic in $C_2/\lambda_A$, where $C_2$ bounds the absolute
row sums of the continuous second derivatives on $\bar X$ and $\lambda_A$ is the
smallest inward derivative at the active bounds (Theorem~\ref{thm:boundary});".

### C-writing-13 (minor). Theorem 1.1(c) uses EX without saying what it does

Location: `intro.tex` 100.

Problem. CT is described just before the theorem (76-78), but EX appears only as
"The algorithm EX (Algorithm~\ref{alg:ex})". A reader of the introduction cannot tell
how exact output is obtained.

Fix. Replace 100 with "\item The algorithm EX (Algorithm~\ref{alg:ex}), which runs CT
with $q=1,2,4,\dots$ and after each run snaps the incumbent to a rational stationary
point of the face of the box near which it lies, returns a global minimizer and".

### C-writing-14 (minor). An unclear clause in Theorem 5.9(b)

Location: `growth.tex` 216-217: "and the bound holds in particular with
$\kappa\ge\bar\kappa$."

Fix. "Since $f$ is increasing in its second argument, the bound also holds with
$\bar\kappa$ replaced by any $\kappa\ge\bar\kappa$, in particular by the Euclidean
condition number."

### C-writing-15 (minor). The title does not name the main result

Location: `main.tex` 3-6.

Problem. "Decomposition-aware global optimization: certified coordinate grids,
conditional recourse, and structural limits" names one extension (recourse) and the
lower bounds. It does not name the problem class (sparse mixed-integer quadratic
programs) or the parameters (treewidth and conditioning), which is the content of
Theorem 1.1. R6 m32 raised this, and it was not adjudicated (it is not in
`all-findings.json`).

Fix. For example, "Certified global optimization of sparse mixed-integer quadratic
programs: corrected coordinate grids, treewidth and conditioning".

### C-writing-16 (minor). The introduction has a single subsection

Location: `intro.tex` 37 (`\subsection{Results}`).

Problem. Section 1 has one subsection (1.1), which runs to the end of the section,
including "Organization".

Fix. Remove the heading and move the label to the paragraph:
`\paragraph{Results.}\label{sec:intro-results}`. The label is used only in the
replacement of C-writing-5(d). Alternatively, add `\subsection{Organization}` before
`intro.tex` 372.

### C-writing-17 (minor). Appendix titles say "deferred proofs" but the appendices contain new results

Locations: `appendix-localized.tex` 1 (Appendix B, which contains B.2 with Theorem B.4
and Props B.5-B.6); `appendix-recourse-convex.tex` 1-2 (C, which contains Props C.1 and
C.3, Corollaries C.7-C.8, Example C.9 and Prop C.10); `appendix-recourse-cuts.tex` 1 (D,
which contains Thm D.2, cited in Table 1, and Prop D.4).

Fix. Use "Exact output: proof of Corollary~\ref{cor:local} and polynomial boundary
optima", "Value functions, local corrections and convex recourse: proofs and
supplements", and "Cut-based recourse: exact output, concave--convex residuals and
proofs".

### C-writing-18 (minor). Experiment labels are out of order, and two table captions are incomplete

Locations: `computation.tex` (E1-E3 in §11.2, E6 in §11.3, E4 in §11.5, S1 in §11.6, E5
in §11.7); Table 3 caption 229-234; Table 6 caption 435-437.

Problems. The labels do not follow the order of presentation (E6 comes before E4 and
E5), and S1 follows a different scheme. Table 3 uses a column "bag" that its caption
does not define (it is defined only in the Table 5 caption). Table 6 does not define
the statuses "exact", "certified", "time limit" and "table limit", or the column "gap".
The "dense cut, n=33" row (0 entries, "table limit") cannot be understood without them.
The limit is `max_table_states=200000` in `experiments/recourse/run_recourse.py`.

Fixes. Renumber in order of appearance (E4 random, E5 exact output, E6 localized,
E7 SCIP), and map the old names in `experiments/README.md`. Add to the Table 3 caption:
"``Bag'' is the maximum bag size." Replace the Table 6 caption with: "Recourse
experiment: plain corrected grids (CT) versus the recourse pipeline (gap target
$2^{-10}$, 20-second limit). Status: ``exact'', exact minimizer certified;
``certified'', gap at most $2^{-10}$ certified; ``time limit'' and ``table limit'', run
stopped by the time limit or by the limit of $2\cdot10^5$ table entries, with the
certified gap reached in column ``gap''. ``Bag'' is the maximum bag size of the
decomposition used by the plain grids, and ``entries'' the total number of table
entries of the plain runs; times in seconds." The authors should confirm what the
limit applies to (per stage or per table).

### C-writing-19 (minor). "Minimizer" and "optimizer" are used interchangeably

Locations: 37 uses of "optimizer(s)" against 177 of "minimizer(s)" in the main text:
`intro.tex` 281, 289, 294, 330, 335, 340, 353, 356; `related.tex` 156, 165, 167;
`exact.tex` 6, 9; `recourse-local.tex` 54, 55, 81, 136; `recourse-convex.tex` 195, 202,
206, 244; `recourse-cuts.tex` 218; `optsets.tex` 13, 268 (subsection title), 347, 349,
371, 404, 407, 432, 525, 534, 638, 653-659.

Problem. In Table 1, adjacent rows say "exact minimizer" and "exact optimizer" for the
same output, and Theorem 1.1 says "global minimizer" while Theorem 7.4 says "global
optimizer".

Fix. Use "minimizer(s)" throughout the main text, including the title of §9.2 ("every
minimizer at once"). Keep "optimal set" and "optimal value".

### C-writing-20 (minor). Two rows of Table 1 are cryptic, and one row reuses `kappa` for a different quantity

Location: `intro.tex` 323-335.

Problem. The Thm 7.10 row gives the parameters as "$p,\kappa(L^+,g)$, $L^+$ reduced"
and then the bound "$f(p,\kappa)\kappa^{C}\dots$". Here `kappa` is `kappa_V` of
Theorem 7.10, not the `kappa` of Theorem 1.1. The Thm 7.2 row packs four hypotheses
and two bounds into narrow cells (see p. 6 of the PDF).

Fix. Replace the two rows with:

```latex
Thm.~\ref{thm:valuefn} & value function with exact polynomial-time value
factors; point growth of $V$ & $p$ (of $V$), $\kappa_V=\kappa(L^V,g)$ &
$f(p,\kappa_V)\poly(\kappa_V,I+q)$; exact $f(p,\kappa_V)\poly(\kappa_V,I)$ &
feasible point, certificate; exact minimizer\\
Thm.~\ref{thm:cv} & private convex QP blocks with certified responses;
point growth of $V$ (exact output: of $F$) & $p$, $\kappa_V=\kappa(L^+,g)$ &
as Thm.~\ref{thm:valuefn}; $2^{O(p)}\poly(I)$ if $L^+=0$ & feasible point,
exact minimizer\\
```

Also add to the caption: "the degrees of the polynomials in the rows of
Theorems~\ref{thm:valuefn} and~\ref{thm:cv} depend on the oracle time bounds".

### C-writing-21 (minor). An unclear motivation sentence in Section 7

Location: `recourse.tex` 3-5: "Stiff convex terms, which are easy to optimize, can make
them large, and so can a large residual problem whose nonconvexity is combinatorial
rather than metric."

Problem. "Metric" nonconvexity is not defined, and it is not said how a concave
residual makes the condition number large. Its coordinates have `L_i=0`. Their effect
comes through near ties, which make `g` small, and through dense couplings, which make
the bags large.

Fix. "Stiff convex terms, which are easy to optimize, can make them large. So can a
residual problem with combinatorial structure: nearly tied endpoint assignments of its
coordinates make the growth constant small, and a dense residual makes the bags
large."

## Checked and found correct

* No filler or inflated vocabulary in the main text. The search covered crucial(ly),
  notably, importantly, interesting(ly), remarkable/remarkably, powerful, novel,
  significant(ly), substantial(ly), elegant, clearly, obviously, essentially, really,
  actually, very, leverage, comprehensive, furthermore, additionally, simply, easily,
  natural(ly) and straightforward. The only hits are factual uses ("trivial kernel",
  "natural non-uniform alternatives" from CONVENTIONS, "easy to guess" in an honest
  caveat). Hedging is limited to justified "as far as we know" and "to our knowledge".
* No drafting leftovers ("FG", "the report", "Algorithm 1/2", "capped algorithm",
  "geometric grid", "slope", "labels per coordinate"). No doubled words and no
  British spellings. Every theorem-like environment has a title.
* The build log has no overfull boxes and no undefined or multiply defined
  references.
* Algorithm names (TRIAL, CT, REC, EX, UC, CORE, TU-GRID, TU-EXACT, PROX, DISC) follow
  CONVENTIONS §2. "Nodes per coordinate", "table entries", "graded grid" and
  "grading" are used consistently.
* Theorem 1.1 matches Theorems 4.7, 5.9 and 6.14 (hypotheses, the form of `f`, the
  exponent 5, and validity without growth). Theorem 1.2 matches Cor 10.2 and Props
  10.5, 10.6 and 10.3. The TU, FPT and lower-bound wording in the abstract,
  introduction, Remark 5.10, §8.5 and the conclusion matches CONVENTIONS §5 and
  Prop 10.10.
* Table 1 rows agree with the cited statements: 5.9, 6.14, 7.2, 7.10, 7.17/7.20/D.2,
  7.26, 8.12, 9.4, 9.7/9.8, 9.15 and the four lower bounds.
* The organization paragraph matches the section and appendix structure. The
  appendices are ordered by section. Every section from 4 to 11 opens with a
  roadmap. The §7 roadmap (`recourse.tex`) correctly separates main and side
  results and states the dependencies.
* The W2 writing issues are fixed: a headline theorem exists, the contributions list
  is gone, "recourse" is defined before use, "width three" is gone, the double "bound"
  is gone, "within k bits" is gone, "at least F(ell)" is gone, and the §6 opening
  matches its contents. Remark rem:np is in §6, and the related-work duplicates of
  in-section remarks have been removed.
* Captions of Figures 1-2 and Tables 4-5 agree with the text. The claim "at most
  eleven nodes per coordinate for m=64" in the introduction agrees with Table 4.
* Tense and voice are consistent: present tense for mathematics, past tense for
  experiments, "we" throughout.
* The scope caveat exists in the introduction and Section 3. C-writing-3 concerns
  only its accuracy.

## Targeted checks run (local; not CI)

* `python3 process/w4/checks/cwriting_wordcount.py`: current abstract 256 words,
  proposed abstract 252 (each math expression counted as one word).
* `python3 process/w4/checks/cwriting_longsent.py 60`: approximate scan for long
  sentences. The 110-word sentence at `intro.tex` 202-214 was found by reading,
  because the script does not split at semicolons.
* `grep` searches for filler words, drafting leftovers, British spellings, doubled
  words, untitled environments, "optimizer/minimizer" counts and the repeated
  lower-bound sentence. Page and number lookups used `main.aux`. Pages 4-6 and 73-74
  were rendered to check the layout of Table 1 and Figures 1-2.
