# F-referee: final referee assessment for Mathematical Programming (round w6)

Version reviewed: `main.tex` and `sections/*.tex` as of 2026-10-03 (after W5), and the build
`/tmp/dpaper/out/main.pdf` (127 pages: main text pp. 1-70, references pp. 71-84 with 188 entries,
appendices A-H pp. 84-127). Page numbers come from `/tmp/dpaper/out/main.aux` and `pdftotext`.
Line numbers refer to the individual source files.

## 1. Recommendation

**Ready for submission after small changes.** I found no wrong statement among the main claims.
The abstract, Theorems 1.1 and 1.2, Table 1, the scope paragraph and the conclusion agree with
the theorems they cite. Novelty and limits are stated accurately and with the right credits
(Bajaj-Hasan, Hochbaum-Shanthikumar, Bienstock-Munoz, Del Pia-Khajavirad, Rosenberg,
Wainwright-Jaakkola-Willsky, Werner, the diagonal-certificate literature). The remaining items are:

- one editorial item (length, F-referee-1). It is the only part of the previous required change
  R-referee-1 that is still open;
- missing submission metadata (F-referee-2);
- four local wording fixes (F-referee-3 to F-referee-6).

## 2. Assessment

**Significance and novelty.**
- The core result is new and suitable for MP:
  - a growth-free path certificate;
  - certified approximation in f(p, κ̄)(I+q+1)^5 bit operations for mixed-integer box QP, where
    κ̄ is never an input;
  - exact output in f_1(p, κ) poly(I).
- The lower bounds form a coherent picture:
  - κ cannot be replaced by log κ;
  - p cannot be dropped;
  - under rETH the exponent of κ cannot be o(p) (with a fixed degree in I, as stated);
  - p/2 is optimal for value oracles.
- The novelty sentence (intro.tex:110-113) is scoped correctly ("nonconvex or mixed-integer box
  QP", "to the best of our knowledge"). The closest prior work is compared in one place each:
  - the cluster problem and Hochbaum-Shanthikumar (related.tex:86-128);
  - Bienstock-Munoz (Remark `rem:tu-bm`);
  - Khajavirad (Remark `rem:cv-instances`).

**Limitations.** These are stated honestly:
- κ can be exponential in I (setting.tex:140-146; intro.tex:198-201);
- there is no claim about κ on application models, and all continuous families are synthetic
  (computation.tex:3-10);
- several extensions are classical constructions inside the certificate (intro.tex:283-286;
  Remarks `rem:cr-cut-prior`, `rem:shor`);
- the TU algorithm is not FPT (intro.tex:297-300).

**Correctness.** Earlier rounds re-derived the proofs. I re-checked the following and found no
error:
- the main-text statements of Sections 3-10 against their proofs and appendix counterparts:
  - `thm:approx`, `thm:exact`, `thm:transfer`, `lem:states`;
  - `thm:valuefn`, `thm:cv`, `prop:cv-limit`, `thm:cr-filter`, `thm:cr-search`, `prop:cr-growth`,
    `thm:balanced`;
  - `prop:tu-sound`, `thm:tu-states`, `thm:tu-approx`, `thm:tu-exact` (including the level
    bound J_ex);
  - `thm:cells`, `thm:endpointset`, `thm:diagdiscovery`;
  - `lim:prop:unique`, `prop:lbwidth`, `prop:lbproduct`, `lim:prop:oracle`,
    `lim:prop:messages`, `lim:prop:setgrowth`, `prop:oraclebarrier`, `lim:prop:constraints`;
- the numbers quoted in the computation section against Appendix H and the result files. One
  example: the replay ratio 2.54 = 50.927/20.019 from `experiments/recourse/results.csv`.

The constants checked by `process/w6/checks/F-referee-spot.py` all pass:
- the radius constant 7.296 < 7.3 and the node cap of Lemma `lem:states`;
- 2^{μ*} ≤ 6√κ̄;
- inequality (`eq:logabsorb`);
- the example in Section 3;
- the comparison in Remark `rem:cf`;
- Lemma `lem:tu-uniform`;
- the level bound of Theorem `thm:tu-exact`.

**Structure.** The structure is clear:
- Theorems 1.1 and 1.2 and Table 1 give the whole picture in four pages.
- Each extension has one intro paragraph with its novelty statement.
- Section 7 has a roadmap.
- The appendices follow the section order.

Section 7 (13 pp.) is the longest section. Section 7.2 sits between 7.1 and 7.3, although only
7.4 uses it (optional O3).

**Length.** The main text has 70 pages and the whole PDF 127 pages. A single comprehensive paper
was chosen deliberately, and the core (Sections 3-6 and 10.1-10.3, about 26 pp.) is now easy to
find. Even so, the main text is still 5-8 pages above the binding W5 target (62-65 pp.) and well
above the 50-55 pp. that the previous report asked for. F-referee-1 lists mechanical moves that
reach about 65 pages without removing any result.

## 3. Status of the previous referee items (process/w4/R-referee.md)

| Item | Status | Evidence |
|---|---|---|
| R-referee-1 (length) | **Partly resolved; still open** | Main text 80 → 70 pp. All listed moves were made: prop:star and the multilevel discussion, thm:cv-recog, TU-EXACT, prop:tu-misaligned/ex:tu-sum, the 9.3 proofs and prop:sshard, the 10.4-10.7 proofs, E3 merged into E2, 11.5/11.6 merged, App. H created, duplicate novelty sentence removed. The page target is not met (F-referee-1). |
| R-referee-2 (Results length, repeated lower-bound summary) | Resolved | "Results" is about 3.1 pp. plus Table 1 (pp. 2-6). There is one short paragraph per extension. The lower-bound summary appears in the abstract and the intro "Thus" paragraph; rem:fpt (growth.tex:282-284) and limits.tex:12-15 point to Thm 1.2. The conclusion keeps one qualified sentence (conclusion.tex:12-14), which is acceptable. |
| R-referee-3 (scope logic) | Resolved | intro.tex:185-201 and Remark rem:nonconvex (setting-growthcert.tex:59-80) now separate what minimality gives from what growth adds. |
| R-referee-4 (symbol overloads) | Resolved | Exponent ϖ_i (growth.tex:35), proximal weight ω (optsets.tex:409), REC free set J_f (exact.tex:187), minimizer x° (Section 6). The remaining double uses (J, R, r, η) are listed in Table 2 (setting.tex:182-192). |
| R-referee-5 (no application instance) | Resolved by statement | computation.tex:6-10 says that all continuous families are synthetic and that the paper does not test whether modelled instances have small width and moderate κ. |
| R-referee-6 (κ̄ as an instance parameter) | Resolved | setting.tex:103-113 (largest valid γ, independent of x*), intro.tex:106-110, Remark rem:fpt. |
| Housekeeping (orphan appendix-smoothed.tex) | Resolved | The file is gone. figures/ holds only the two figures that are used. |

## 4. Required changes

### F-referee-1 (major): the main text is still 70 pages, above the binding target of 62-65 pages

**Where:** whole main text. Page spans from main.aux:
- §§1-2: pp. 1-9;
- §§3-6: pp. 9-30;
- §7: pp. 30-43;
- §8: pp. 43-51;
- §9: pp. 51-57;
- §10: pp. 57-64;
- §11: pp. 64-69;
- §12: pp. 69-70.

**Problem:**
- `process/w5/CUTPLAN.md` set "main text about 62-65 pages". The previous report asked for
  50-55 pp. (R-referee-1, its first required change).
- The extensions in §§7-9 (27 pp.) are longer than the core in §§3-6 (21 pp.). They still carry
  several long proofs of secondary results in the main text.
- A manuscript of 127 pages will draw editorial objections at MP. Each page that can be moved
  without losing a result should be moved.

**Fix.** These moves keep every statement and label in place. In each case, replace the
`\begin{proof}...\end{proof}` block in the main text by the given sentence, and insert the
unchanged block in the named appendix as `\begin{proof}[Proof of Theorem~\ref{...}] ... \end{proof}`.

(a) **Proofs of secondary results in §§7-9.** About 213 source lines, roughly 2.7 pages:

- recourse-convex.tex:219-261 (proof of `thm:cv`)
  - Replace by: "The proof is in Appendix~\ref{app:recourse-convex}."
  - Merge it there with the existing "Proof of the exact-output part of
    Theorem~\ref{thm:cv}(iii)" (appendix-recourse-convex.tex:424).
- recourse-cuts.tex:116-133 (`thm:cr-oracle`), 203-222 (`thm:cr-search`) and 240-252
  (`prop:cr-growth`)
  - Replace each by: "The proof is in Appendix~\ref{app:recourse-cuts}."
- constraints.tex:255-296 (`prop:tu-sound`), 328-350 (`thm:tu-states`) and 392-406
  (`thm:tu-approx`)
  - Replace each by: "The proof is in Appendix~\ref{app:tu}."
  - In Appendix E, insert them as a new subsection after E.1:
    `\subsection{Proofs for Sections~\ref{sec:tu-filter}--\ref{sec:tu-complexity}}`.
  - Keep the proofs of `lem:tu-round` and `lem:tu-allow` in the main text; they carry the idea
    of the section.
- optsets.tex:148-186 (proof of `thm:cells`)
  - Replace by: "The proof is in Appendix~\ref{app:proximal}."
  - Place it first in Appendix F.

(b) **Table `tab:chain`** (computation.tex:169-187). About 0.3 page:
- Move the table environment to appendix-computation.tex, after its "Exact output" paragraph.
- In computation.tex:155 replace "Table~\ref{tab:chain} reports CT on the family" by
  "Table~\ref{tab:chain} in Appendix~\ref{app:computation} reports CT on the family". The text of
  §11.3 already quotes the numbers that matter.

(c) **§6.5 Localized acceptance** (exact-localized.tex:2-135). About 1.4 pages net:
- Move lines 2-135 unchanged to appendix-localized.tex, before the proof of `cor:local`.
- Retitle Appendix B.1 "Localized acceptance". Keep `\label{app:localized}`.
- Leave this paragraph under `\subsection{Localized acceptance}\label{sec:localized}`:

> The acceptance rule of Proposition~\ref{prop:accept} needs a certified gap below
> $1/(\Omega W)$, as small as about $2^{-315}$ on the instances of
> Section~\ref{sec:comp-exact}. Appendix~\ref{app:localized} gives a second test that uses the
> filtering history. On the box retained by a stage of a filtering run, it checks a candidate by
> one sign condition per coordinate and one exact positive-semidefiniteness test
> (Proposition~\ref{prop:local}); its validity needs neither uniqueness nor growth. Under point
> growth and strict complementarity at the active bounds, the face candidate of
> Definition~\ref{def:facecand} equals $x^*$ and passes this test at every stage that ends by
> filtering in a trial of CT with a common mesh and $8\kappa\theta^2\le1$, once the mesh $h_j$
> is at most a threshold $h^*$; the least such $j$ is at most $\poly(I)+O(\log\kappa)$
> (Corollary~\ref{cor:local}). In experiment S1
> (Section~\ref{sec:comp-localized}) the test accepted the face candidate within nine stages on
> 29 of 30 random mixed-integer instances.

Together, (a)-(c) bring the main text to about 65-66 pages. None of the moved proofs is cited as
"the proof of ..." anywhere in the paper; I checked this with grep. If the editor accepts 70
pages, (c) can be dropped.

### F-referee-2 (minor): submission metadata and code availability are missing

**Where:**
- main.tex:4-8: `\author{}` is empty, and there are no keywords and no MSC codes;
- sections/abstract.tex:28;
- computation.tex:57-58: "Code, inputs, raw results and reproduction scripts (one command per
  experiment group) accompany the paper."

**Problem:**
- Springer's MP submissions need keywords, MSC 2020 codes, author data and a
  statements/declarations block (funding, competing interests, data availability).
- The code sentence names no location. According to `process/w5/reports/computation.md`
  (C-computation-6), the repository is private, and the pinned solver tree is not bundled.

**Fix:**
- In abstract.tex, insert before `\end{abstract}`:

```
\par\medskip\noindent\textbf{Keywords:} global optimization; mixed-integer quadratic
programming; tree decomposition; dynamic programming; quadratic growth; certificates;
parameterized complexity
\par\noindent\textbf{Mathematics Subject Classification (2020):} 90C26, 90C11, 90C20, 90C39,
90C60, 68Q27
```

- In computation.tex:57-58, replace the sentence by:
  "Code, inputs, raw results and reproduction scripts (one command per experiment group),
  together with the solver files they import, are available at \url{<archive DOI>}."
- Archive the tree pinned in `experiments/results/dependencies_sha256.json` before submission.
- Fill in `\author{...}`.
- Before `\bibliographystyle`, add a `\section*{Statements and declarations}` with Funding,
  Competing interests and Data availability (the same DOI).

### F-referee-3 (minor): the conclusion states the headline bounds without the problem class

**Where:** conclusion.tex:3-12.

**Problem:** The paragraph opens with "sparse mixed-integer problems" and then states the CT and
EX bounds without saying that they hold for mixed-integer box quadratic programs. Theorems
`thm:approx` and `thm:exact` assume explicit rational quadratics (`cor:poly` covers fixed-degree
polynomials, with κ).

**Fix.** In conclusion.tex:7-10, replace "Under weighted growth, CT (Algorithm~\ref{alg:ct})
certifies accuracy $2^{-q}$ in $f(p,\bar\kappa)(I+q+1)^5$ bit operations, and under point growth
exact output takes $f_1(p,\kappa)(I+1)^{C_1}$, without knowledge of the growth constant;" by:

> For mixed-integer box quadratic programs with a tree decomposition of bag size $p$, CT
> (Algorithm~\ref{alg:ct}) certifies accuracy $2^{-q}$ in $f(p,\bar\kappa)(I+q+1)^5$ bit
> operations under weighted growth, and EX returns an exact minimizer in
> $f_1(p,\kappa)(I+1)^{C_1}$ bit operations under point growth, without knowledge of the growth
> constant;

### F-referee-4 (minor): the intro uses "set growth" and κ_S before defining them

**Where:**
- intro.tex:118-123: "a growth constant $g_S>0$ towards its optimal \emph{set}";
- intro.tex:256: "already when $\kappa_S=1$", on p. 5;
- intro.tex:293: "Under set growth";
- Table 1 rows `thm:tu-approx`, `thm:cells` and `thm:diagdiscovery`.

κ_S is first defined at intro.tex:307-308.

**Problem:** A reader meets κ_S and the term "set growth" one page before their definition.

**Fix:**
- Replace intro.tex:118-123, from "Exactness itself needs no uniqueness:" to "reach this
  accuracy.", by:

> Exactness itself needs no uniqueness. Every instance has \emph{set growth}:
> $F(x)-\OPT\ge g_S\dist(x,\mathcal S)^2$ on $X$ for some $g_S>0$, where $\mathcal S$ is the set
> of minimizers; we put $\kappa_S=\max\{1,L/g_S\}$. A certified gap of $2^{-k}$ with
> $k=\poly(I)+\max\{0,\log_2(1/g_S)\}$ lets the snapping step return an exact minimizer
> (Theorem~\ref{thm:transfer} and Remark~\ref{rem:setgrowth}); point growth in part~(c) only
> bounds the time needed to reach this accuracy.

- In intro.tex:305-308, replace "where $r$ bounds the number of optimal values of a coordinate and
  $\kappa_S=\max\{1,L/g_S\}$ uses the growth constant $g_S$ towards the optimal set
  (Theorem~\ref{thm:cells})" by "where $r$ bounds the number of optimal values of a coordinate
  (Theorem~\ref{thm:cells})".

### F-referee-5 (minor): §6.5 overstates the scope of the S1 threshold measurement

**Where:** exact-localized.tex:128-131. The text reads: "whereas one CT run needed up to 72 stages
to reach the threshold of Proposition~\ref{prop:accept}".

**Problem:**
- The sentence suggests a maximum over the 29 accepted instances.
- The measurement covers only the five instances on which EX used the most stages:
  - computation.tex:228-231: "on the five instances on which EX used the most stages, one CT run
    reached this threshold after 40 to 72 stages";
  - experiments/README.md:310-312 says the same.

**Fix.** Replace exact-localized.tex:128-131, from "In experiment S1" to
"of~\eqref{eq:exact-constants}.", by:

> In experiment S1 (Section~\ref{sec:comp-localized}) the test accepted the face candidate within
> nine stages on 29 of 30 random mixed-integer instances; on the five of them on which EX used
> the most stages, one CT run needed 40 to 72 stages to reach the threshold of
> Proposition~\ref{prop:accept} with the constants of~\eqref{eq:exact-constants}.

If F-referee-1(c) is applied, make the same change in the moved text.

### F-referee-6 (minor): Table 1 says "all minimizers" where the results give a description

**Where:** intro.tex:175-180 (Table `tab:results`):
- row `thm:endpointset`/`cor:facecsp`: "output: all minimizers";
- row `thm:diagdiscovery`: "outputs also the optimal set".

**Problem:**
- Theorem `thm:endpointset` and Corollary `cor:facecsp` return a system of factored equations, or
  a tree-structured constraint problem, that describes the optimal set. That set can be a
  continuum, or have exponentially many points.
- Theorem `thm:diagdiscovery` returns the description (`eq:diagset`).
- The intro text says this correctly (intro.tex:309-313, 321-322). The table cells do not.

**Fix:**
- In intro.tex:176, replace "output: all minimizers" by "output: a description of the optimal
  set".
- In intro.tex:179, replace "outputs also the optimal set" by "outputs also an exact description
  of the optimal set".

## 5. Optional suggestions

- **O1 (references).** The paper has 188 references. The paragraphs "Adaptive discretization"
  (related.tex:130-147) and "Constraints, optimal sets and limits" (related.tex:209-230) together
  cite 36 works, most of them as one-line pointers. Keeping one or two representatives per
  sentence would shorten the reference list by 1-2 pages.
- **O2 (duplication in §11.1).** computation.tex:23-34 repeats items (a), (c), (d), (f) and (g)
  of the list in Appendix H (appendix-computation.tex:9-43). It would suffice to keep "It differs
  from the analysis in seven ways, none of which affects validity (Appendix~\ref{app:computation}
  lists them); the most important is that all coordinates share the mesh $h_j=s2^{-j}$, so the
  analysis that applies is Lemma~\ref{lem:commonmesh} with the Euclidean condition number
  $\kappa$, not Theorem~\ref{thm:approx}." This saves about 8 lines.
- **O3 (order in §7).** Only §7.4 uses §7.2 (bag cells, `lem:cr-cell`, `thm:cr-filter`).
  Placing it directly before §7.4, and adjusting the roadmap at recourse.tex:18-34, would let
  §7.1 lead straight into §7.3.
- **O4 (cover letter).** State that one comprehensive paper is intended, that the core is
  §§3-6 and §§10.1-10.3, and that §§7-9 are extensions with their long proofs in the appendices.

## 6. Commands run (targeted, local; not CI)

- `python3 process/w6/checks/F-referee-spot.py`: all checks pass (radius constant 7.2961; maximum
  ratio of needed nodes to the cap 0.9125; maximum 2^{μ*}/√κ̄ = 5.657; no violation of
  `eq:logabsorb`, `lem:tu-uniform`, the Section 3 example, `rem:cf` or the J_ex bound of
  `thm:tu-exact`).
- `pdfinfo` gives 127 pages. Section pages come from main.aux and fractional heading positions
  from `pdftotext -layout`. No `??` appears in the rendered text, and main.log has no
  undefined-reference or overfull warnings.
- Greps:
  - previous-referee renames (ϖ, ω, J_f);
  - the orphan file and the figures directory;
  - keywords/MSC/declarations;
  - references to the proofs proposed for moving (none found).
- Data checks:
  - `experiments/recourse/results.csv`: replay ratio 50.927/20.019 = 2.544;
  - `experiments/README.md`:310-312 and `results/S1_ex_replay.csv`: scope of the S1 threshold
    measurement.

No project-wide verification was run. CI was not consulted.
