# W5 report: front (abstract, intro, related, conclusion; references.bib additions)

Files edited: `sections/abstract.tex`, `sections/intro.tex`, `sections/related.tex`,
`sections/conclusion.tex`. I added 11 entries at the end of `references.bib` and changed no
existing entry. Check scripts: `process/w5/checks/front-pages.py` and
`process/w5/checks/front-scope.py`.

## 1. Page spans

Measured in a private build (`/tmp/w5-front`, current tree including the other groups'
concurrent edits). Positions are fractional page positions in `pdftotext -layout` output.
Labels are from `main.aux`.

| Part | Before (snapshot build) | After | Change |
|---|---|---|---|
| Section 1 (sec:intro) | pp. 1-7 (1.60-7.20), 5.60 pp | pp. 1-6 (1.60-6.11), 4.52 pp | -1.08 |
| "Results" text | 3.71 pp, plus Table 1 on a full float page (p. 6) | about 3.1 pp, plus Table 1 (0.63 p, top of p. 3) | -0.6 text; table -0.4 |
| Section 2 (sec:related) | pp. 7-10 (7.20-10.07), 2.87 pp | pp. 6-8 (6.11-8.86), 2.75 pp | -0.12, with the HS comparison and six other additions included |
| Section 12 (sec:conclusion) | pp. 78-80 (78.84-80.11), 1.27 pp | pp. 69-70 (69.80-70.93), 1.13 pp | -0.14 |
| Abstract | 256 words | 250 words (counted as in `process/w4/checks/cwriting_wordcount.py`) | |

The front sections saved about 1.3 pp. The main text now ends at p. 71 (references start on
p. 71); before, it ended at p. 80. That figure includes all groups.

## 2. Cut-plan items (CUTPLAN "front")

| Item | Status | What was done |
|---|---|---|
| Results at most 3 pp plus Table 1 | Nearly done: about 3.1 pp of text plus a 0.63 p table | Started from `process/w4/checks/verify-C-writing-2-proposed.tex` and shortened further. (i) One short paragraph per extension, with no undefined terms. (ii) The "Parameterized form" paragraph became two sentences after Theorem 1.1. (iii) The "Exact messages" paragraph was merged into the list of further limits. (iv) The organization paragraph was shortened. (v) Table 1 is shrunk: 4 columns, lower-bound rows dropped (Theorem 1.2 states them), shorter cells, `[tb]` instead of `[tbp]`, so it no longer takes a float page. Theorems 1.1 and 1.2 are kept. The last 0.1 p could only be cut by removing required content (see Unresolved). |
| Scope caveat | Done | Replaced by the verifier's corrected text of C-writing-3: minimality alone gives H_{J0J0} PSD; point growth gives H_{J0J0} >= 2gI and kappa >= 2L/lambda_min(H_{J0J0}); weighted growth gives H_{J0J0} >= 2 gamma diag(L_i); globally kappa >= L‖x'-x*‖²/(F(x')-OPT); Example ex:family. I wrote "an indefinite Hessian" instead of "indefinite Hessian blocks" (coreA's request): H_{J0J0} is the "Hessian block" just defined, and it is PSD at a minimizer. Checked exactly by `front-scope.py`. |
| FPT wording | Done | "In parameterized terms, part (b) is a fixed-parameter bound in the parameters p and ⌈κ̄⌉, which CT neither receives nor computes; here κ̄ is the smallest weighted condition number of the instance, which exists (Section 3 and Remark rem:fpt)." coreA added the existence argument to setting.tex. I checked it: the valid γ form (0,γ*], a closed set independent of x* because x*_P is unique. |
| Related work toward 2 pp, each comparison in one place | Partly done: 2.87 to 2.75 pp | The roadmap paragraph is deleted. The duplicate novelty sentence (related 54-56) is deleted; the intro one is kept. All paragraphs are compressed, and every citation is kept, so no bib entry becomes orphaned. The Bienstock-Muñoz comparison now appears only in rem:tu-bm, plus a pointer here; the intro no longer has its own comparison sentence. The HS comparison is in one place (related.tex, "Accuracy-independent work under growth"); rem:tu-bm is untouched, and tu's constraints.tex pointer "Section 2 compares the two" now has its referent. Adding HS, Meyer and the six accepted minor literature items cost about 0.4 pp. |
| HS comparison (C-literature-1) | Done, 5 sentences | See the adjudication of C-literature-1. Meyer1977 was added to references.bib after a Crossref check. |
| Conclusion about 1 p | Done: 1.13 pp | Summary paragraph shortened. The lower-bound sentence became a pointer to Theorem 1.2 with the qualified rETH clause. The experiments paragraph was shortened. The open problems are kept, with "Negative curvature" still question 1 (recA cites it). The tu-hybrid idea remains one sentence in question 3, as CONVENTIONS requires. |

## 3. Adjudication of assigned findings

| Id | Decision | Reason | Change |
|---|---|---|---|
| M-limits-1 | ACCEPTED (my parts) | Prop. prop:lbproduct only excludes bounds with a fixed degree in I. | Abstract: "the exponent of κ in a bound f(p)κ^{a(p)}I^{O(1)} cannot be o(p)". Intro ("Thus ..." paragraph) and conclusion: "... in a bound f(p)κ^{a(p)}poly(I) cannot be o(p)". |
| M-limits-2 | ACCEPTED | CT's query count also grows with the accuracy, but only logarithmically; the barrier is about the rate. | Intro: "under growth towards an unknown optimal set, a deterministic algorithm that queries values and derivatives needs at least of order ε^{-n/2} queries, already when κ_S=1". |
| M-limits-5 | ACCEPTED | The locator matches the paper's v15 convention for BienstockMunoz2018 (limits' verifier checked Appendix A of v15). | `\cite[Appendix~A]{BienstockMunoz2018}` in the intro. |
| C-consistency-1 | ACCEPTED (via C-writing-20) | The Thm 7.10 row used κ for κ_V. | Table 1: parameters "p, κ_V"; caption defines κ_V=κ(L^+,g) for Theorem thm:cv. |
| C-consistency-4 | NO CHANGE NEEDED in my files | The intro uses r only for the number of optimal values, defined where it is used (minimizers paragraph, Table 1 TU row). Section 7's r does not occur in my files. | None. Table 2 belongs to coreA. |
| C-consistency-5 | ACCEPTED (my part) | ETH was stated with δ, m in the intro and with c, n' in Section 10.3. | The intro now states ETH and rETH with the Section 10.3 symbols (c, n', error probability at most 1/3, DellEtAl2014). Limits' verifier made Section 10.3 refer to this statement ("as stated before Theorem thm:intro-lower"), so each hypothesis is stated once. The other symbols are not in my files. |
| C-consistency-8 | NOT MY FILES | appendix-smoothed.tex is already gone from sections/; the figure file belongs to the coordinator. | Request to coordinator (figures/E3_plateau_vs_n.pdf). |
| C-consistency-9 | ACCEPTED | "fixed width" was ambiguous next to box widths. | "polynomial for fixed bag size p". |
| C-writing-1 | ACCEPTED (front part) | The main text was too long; the intro was the largest single source of growth. | Intro -1.08 pp, related -0.12 pp, conclusion -0.14 pp (Section 1 above). |
| C-writing-2 | ACCEPTED (verifier's corrected text, then shortened) | The intro was too long, and its extension paragraphs used undefined terms. | Started from verify-C-writing-2-proposed.tex: shorter "Thus" paragraph, one paragraph per extension, no undefined terms ("value factors", "core point", "level-0 grid", "Bellman residuals" and the like are gone). Fix (0) is kept: the expanding-box chain is named in the list of further limits, where it now also replaces the "Exact messages" paragraph. To reach the length target I also dropped "Two classes have exact recourse ...", the balanced-case bound (it stays in Table 1) and the Bienstock-Muñoz sentence (rem:tu-bm is the single place for it). |
| C-writing-3 | ACCEPTED (intro part; verifier's corrected text) | "Therefore" attributed to growth a restriction that minimality already implies. | Intro scope paragraph as described in Section 2. Remark 3.4 belongs to coreA, and the CONVENTIONS §5 update to the coordinator. |
| C-writing-4 | MODIFIED | 256 words, with no scope caveat. The proposed scope sentence ("distant local minima clearly worse") is false as a requirement when L=0 (C-writing-3 verifier). | New 250-word abstract based on the C-writing proposal. Scope sentence: "Growth with ratio κ forces the Hessian block of the interior continuous coordinates to have smallest eigenvalue at least 2max_iL_i/κ, and every other local minimizer x' to satisfy F(x')-min F >= max_iL_i‖x'-x*‖²/κ." This follows from H_{J0J0} >= 2gI and g >= L/κ. The abstract also carries the M-limits-1 qualifier. |
| C-writing-5 | ACCEPTED (my parts) | Repeated summaries. | (b) The "Parameterized form" paragraph was replaced by two sentences that cite rem:fpt. (c) related.tex 54-56 deleted. (a) The conclusion's lower-bound sentence became a pointer to Theorem 1.2. (e) The duplicate exact-messages statement is gone. (d) See C-consistency-5. |
| C-writing-10 | ACCEPTED (my parts) | κ was used as a dummy argument. | Theorem 1.1(b) and conclusion question (2): f(p,t)=c_0(c_1p√t)^p t(1+log_2 t)^2. |
| C-writing-13 | ACCEPTED | EX was used in Theorem 1.1 without a description. | Theorem 1.1(c): "EX (Algorithm alg:ex), which runs CT(2^{-q}) for q=1,2,4,... and snaps each incumbent to a rational stationary point of a nearby face of the box until an exact test accepts it, returns ...". Checked against alg:ex and REC. |
| C-writing-15 | FORWARDED | main.tex belongs to the coordinator. I agree that the title should name the problem class and the parameters. | Request: e.g. "Certified global optimization of sparse mixed-integer quadratic programs: corrected coordinate grids, treewidth and conditioning" (also update the pdftitle). |
| C-writing-16 | ACCEPTED | Section 1 had a single subsection. | `\paragraph{Results.}\label{sec:intro-results}`. The label is kept; `\ref` now prints "1". Currently no file refers to it. |
| C-writing-19 | ACCEPTED (my files) | "optimizer" and "minimizer" were mixed. | My four files contain no "optimizer" (Table 1, intro, and related.tex's multiparametric and polynomial sentences). |
| C-writing-20 | ACCEPTED / MODIFIED | The cells were cryptic, and κ was reused. | Table 1 rebuilt: the Thm 7.2 and 7.10 rows use κ_V, defined in the caption. The caption says that only the row of Theorem thm:valuefn has degrees depending on the oracle time bounds. The reviewer's caption would have said this of both rows, but thm:cv(iii) has absolute constants. Deviation: the Output column is folded into the caption ("Every algorithm returns a certificate that is valid without the growth hypotheses; 'exact' marks the bound for computing an exact minimizer"), and setting cells note special outputs (exactly feasible output, all minimizers, the optimal set). The lower-bound rows are dropped because Theorem 1.2 sits next to the table. This takes the table from a full float page to 0.63 p. |
| C-literature-1 | ACCEPTED (verifier's corrected fix, condensed to 5 sentences) | HS proximity scaling is the closest classical antecedent, and it was uncited as such. | related.tex, "Accuracy-independent work under growth", second paragraph. HS is a separable convex objective over {Ax>=b}, with a piecewise-linear interpolation on a grid of O(nΔ) points per variable, in a box halved by proximity. For continuous variables it uses ⌈log₂(B/(2ε))⌉ grids and reaches a point within ε of an optimal solution in the maximum norm, "guaranteed but not certified" \cite[Section 1.3 and Theorems 1.1, 3.8 and 4.4]{HS90}. The TU specialization: one LP \cite{Meyer1977}, \cite[Theorem 4.3]{HS90}; Lemma lem:tu-round uses the same integrality. The differences: nonseparable nonconvex objective, filtering that needs no assumption and yields a certificate, growth only bounding the size, and dynamic programming on a tree decomposition. Everything was checked against the local HS full text (Sec. 1.3; Thms 1.1, 3.8, 4.3, 4.4). Meyer's TU sentence is in this paragraph and not in "Constraints" (verifier step 2), so the comparison stays in one place. related.tex 141-143 is unchanged, as the verifier asked. |
| C-literature-2 | ACCEPTED | Box QP in fixed dimension is polynomial by face enumeration. | "whether the problem is polynomial when the dimension is part of the input is open \cite[footnote 2]{BNW} (for each fixed dimension it is, by enumerating faces \cite{Vavasis1990})". |
| C-literature-3 | ACCEPTED (related.tex part; grids.tex is coreA's) | The edge-concave underestimator is Hasan 2018; Bajaj and Hasan evaluate it at vertices. | related.tex: "... edge-concave, with a vertex-polyhedral envelope [..., Hasan2018, ...], and Bajaj and Hasan evaluate such an underestimator, built from an upper bound on the diagonal Hessian entries, at the 2^n vertices of a box". Checked against the AIChE 2018/2019 abstracts (WebSearch). The intro's "vertex lower bound of Bajaj and Hasan" is accurate and unchanged. |
| C-literature-4 | ACCEPTED | Vavasis 1992 is not a Turing-model algorithm. | "for QP with a fixed number of negative eigenvalues in exact real arithmetic \cite{Vavasis1992}, ... or, in the bit model, ... \cite{DelPia2026Jacobi}". Checked in the local full text of Del Pia (arXiv:2607.29386, p. 2). |
| C-literature-5 | ACCEPTED (intro part, modified) | The intro called the rETH bound new without saying what is new. | "the rETH bound (a quadratic encoding of multicolored clique with a unique minimizer)", which matches limits' new sentence in Section 10.3. I did not attribute the encoding to Chen et al. 2006 in the intro, because, like the limits agent, I could not check that paper for it. |
| C-literature-6 | ACCEPTED | Exact rational SOS certificates and the current exact-MIP reference were missing. | "Rational sum-of-squares certificates give exact lower bounds for polynomial objectives \cite{PeyrlParrilo2008,KaltofenEtAl2008}, but these bounds are values of relaxations, whereas a path certificate brackets OPT within any prescribed 2^{-q}." EiflerGleixner2023 cited next to CookKochSteffyWolter2013. |
| C-literature-7 | ACCEPTED (wording modified) | LP optimal-face identification is the classical antecedent of snapping. | "in linear programming the optimal face is identified once the gap is below a threshold set by the encoding length \cite{Ye1992,MehrotraYe1993}; Lemma lem:snap does this for box QP, with set growth turning a small gap into proximity to the optimal set". The reviewer's "in place of LP duality" is imprecise, so I did not use it. |
| C-literature-8 | ACCEPTED | The sharp certified-evaluation result was missing. | "Bachoc, Cesari and Gerchinovitz characterize, instance by instance, the number of evaluations needed to find and certify an ε-optimal point". Checked against the arXiv abstract and the NeurIPS BibTeX. |
| C-literature-9 | ACCEPTED | Optional additions; no novelty statement changes. | (a) "Decision diagrams give outer approximations of integer nonlinear programs \cite{DavarniaVanHoeve2021} and, on partitions of continuous domains with spatial branch-and-bound, a global method for bounded mixed-integer nonlinear programs \cite{DavarniaKiaghadiQiu2026}". The second paper was read locally (sub-domain partitions, spatial B&B). (b) "In fixed dimension, integer QP in the plane \cite{DelPiaWeismantel2014} and, according to a recent preprint, mixed-integer QP \cite{AriHildebrand2026} are solved exactly in polynomial time". Ari-Hildebrand v2 (the version with the MIQP result) is cited; its abstract was read locally. |
| C-literature-11 | FORWARDED | I may only add entries to references.bib. appendix-smoothed.tex is already gone. | Request to coordinator: fix the provenance comments above Khajavirad2026PolyBox and BhathenaEtAl2026Graphs. |
| R-referee-1 | ACCEPTED (front part) | Same as C-writing-1. | Duplicate novelty sentence deleted (related 54-56); intro and conclusion cut. |
| R-referee-2 | MODIFIED | The Results section was too long and repeated. The proposed single 15-line extension paragraph conflicts with CONVENTIONS §1, which requires one paragraph per extension with novelty statements. | One short paragraph per extension; attributions shortened to one clause. The lower-bound summary stays in the abstract and in the intro "Thus" paragraph, both qualified; the conclusion now points to Theorem 1.2. |
| R-referee-3 | ACCEPTED (intro part) | Same as C-writing-3. | Verifier text of C-writing-3. Remark 3.4 belongs to coreA. |
| R-referee-6 | ACCEPTED (intro part) | The parameter must be a function of the instance. | The intro names κ̄ as the smallest weighted condition number of the instance, which exists (Section 3, where coreA added the argument, and Remark rem:fpt). |
| R-referee-5 | NO CHANGE in my files | The intro already says "We do not claim that κ or κ̄ is moderate for the application models mentioned above"; the sentence is kept. The computation group added the statement that the instances are synthetic. | None. |

## 4. Labels

All labels in my files are kept: sec:intro, sec:intro-results, thm:intro-main, thm:intro-lower,
tab:results, sec:related, sec:conclusion. None was moved. sec:intro-results now sits on a
`\paragraph` and renders as "1" (anchor section*.1). Every `\ref` in my files resolves. References
to moved results name their appendix: cor:cv-nu (Appendix app:recourse-convex),
lim:prop:moments (app:moments), prop:tu-misaligned and ex:tu-sum (app:tu), prop:weakcompl
(app:boundary). The intro no longer cites prop:star or thm:cv-recog.

## 5. New references.bib entries (appended at the end, with provenance comments)

All metadata verified on 2026-10-03:

- Meyer1977: Crossref, doi 10.1137/0315059; abstract checked.
- PeyrlParrilo2008: Crossref, doi 10.1016/j.tcs.2008.09.025.
- KaltofenEtAl2008: Crossref, ISSAC 2008, pp. 155-164, doi 10.1145/1390768.1390792.
- EiflerGleixner2023: Crossref, Math. Program. 197(2):793-812, doi 10.1007/s10107-021-01749-5.
- Ye1992: Crossref, Math. Program. 57:325-335, doi 10.1007/BF01581087.
- MehrotraYe1993: Crossref, Math. Program. 62:497-515, doi 10.1007/BF01585180.
- DavarniaVanHoeve2021: Crossref, Math. Program. 187(1-2):111-150, doi 10.1007/s10107-020-01475-4.
- DavarniaKiaghadiQiu2026: Crossref, J. Glob. Optim. 96(1):1-38, doi 10.1007/s10898-026-01635-4.
- DelPiaWeismantel2014: Crossref, SODA 2014, pp. 840-846, doi 10.1137/1.9781611973402.62.
- BachocCesariGerchinovitz2021: NeurIPS 34, pp. 24180-24192, from the proceedings BibTeX.
- AriHildebrand2026: arXiv:2609.18266v2, from the arXiv abstract page (v1 16 Sep, v2 23 Sep 2026).

No existing entry was changed. No key is duplicated, and every entry is cited somewhere in
sections/.

## 6. Requests for other files

1. coordinator, main.tex (C-writing-15): retitle so that the title names the problem class and
   the parameters, e.g. "Certified global optimization of sparse mixed-integer quadratic programs:
   corrected coordinate grids, treewidth and conditioning". Update `pdftitle` too.
2. coordinator, CONVENTIONS §5: replace the "Growth scope" bullet with the C-writing-3 verifier
   text (as coreA also requested). Under "FPT", note that κ̄ means the smallest valid value.
3. coordinator, references.bib (C-literature-11): fix the two misplaced provenance comments
   above Khajavirad2026PolyBox and BhathenaEtAl2026Graphs. Also add limits' AbelloEtAl2001, the
   only undefined citation in the current build.
4. coordinator (C-consistency-8): remove figures/E3_plateau_vs_n.pdf from the submission tree if
   it is still unused.
5. computation / coordinator: the intro no longer quotes the chain run (10^{-3}, m=64, eleven
   nodes); it cites only Example ex:chain and Proposition lim:prop:messages. The computation
   report kept Table tab:chain in Section 11 "because the introduction advertises the chain
   result", so moving it to Appendix H is now possible if wanted.
6. tu: no action. related.tex now contains the HS comparison, so the constraints.tex pointer
   "Section 2 compares the two" is valid. Keep the label lem:tu-round, which related.tex cites.
7. limits: no action. ETH and rETH are stated right before Theorem thm:intro-lower with c, n',
   error probability at most 1/3 and DellEtAl2014. The order of Theorem 1.2 parts (a)-(d) is
   unchanged.

## 7. Checks run (local, targeted; not CI)

- `latexmk -pdf -interaction=nonstopmode main.tex` in the private copy /tmp/w5-front (current
  tree): exit 0. The whole log has no `!` errors, no LaTeX warnings (no undefined references,
  no multiply defined labels) and no overfull or underfull boxes. BibTeX gives one warning, for
  AbelloEtAl2001 (limits' key, pending the coordinator). The PDF has 127 pages.
- `python3 process/w5/checks/front-pages.py <pdf>` on the snapshot build (/tmp/w5-front-base)
  and on the final build: the page spans in Section 1.
- `python3 process/w5/checks/front-scope.py`: exact checks on Example ex:family and on an L=0
  instance of the scope statements in the abstract and intro. Passed.
- Abstract word count with the counting function of `process/w4/checks/cwriting_wordcount.py`:
  250.
- Cite-key script: every `\cite` key in my files exists in references.bib; references.bib has
  no uncited and no duplicate keys.
- Label script: the label sets of my files are unchanged, and every `\ref` target in my files
  exists.
- Metadata checks: Crossref API queries for 9 DOIs; the arXiv abstract page (Ari-Hildebrand,
  Bachoc et al.); the NeurIPS proceedings BibTeX; WebSearch for the Bajaj-Hasan AIChE
  abstracts.
- Sources read locally: Hochbaum-Shanthikumar 1990 (Sec. 1.3; Thms 1.1, 3.8, 4.3, 4.4); Del Pia
  arXiv:2607.29386 (p. 2, Turing-model remark on Vavasis 1992); Davarnia-Kiaghadi-Qiu 2026
  (abstract, Sections 2-3); Ari-Hildebrand v2 (abstract).
- Every claim of the rewritten intro was re-read against the current statements of thm:approx,
  thm:exact, alg:ex, thm:transfer, rem:setgrowth, lem:growthcert, ex:family, ex:chain,
  thm:valuefn, prop:vf-curv, thm:cv, prop:cv-limit, thm:cr-oracle, thm:cr-search, thm:cr-exact,
  thm:balanced, thm:tu-approx, thm:cells, thm:endpointset, cor:facecsp, thm:diagdiscovery,
  lim:prop:unique, lim:cor:nopolylog, prop:lbwidth, prop:lbproduct, lim:prop:oracle,
  lim:rem:oracle, lim:prop:setgrowth, prop:oraclebarrier, lim:prop:constraints and
  lim:prop:moments.

No project-wide verification was run, and CI was not consulted.

## 8. Unresolved

- Results is about 3.1 pp of text plus a 0.63 p table, slightly over the 3-page target. More cuts
  would remove content that is required: the Theorem 1.2 statement, the binding scope text, or
  the novelty statement of each extension.
- Related work is 2.75 pp against "toward 2 pp". The accepted additions (HS/Meyer, SOS
  certificates, LP face identification, Bachoc et al., decision diagrams, exact fixed-dimension
  MIQP) cost about 0.4 pp. Further cuts would drop citations and leave bib entries orphaned.
- Table 1 has no separate Output/certificate column; that information is in the caption. This
  deviates from the column list in CONVENTIONS §1, and the coordinator should confirm it.
- The title (C-writing-15) is pending the coordinator.

## Verification (W5 verifier for front)

Outcome: the revision is sound. No mathematical statement in the four files is wrong, and all 34
assigned findings are resolved or justifiably forwarded. I fixed one literature misstatement
(Hochbaum-Shanthikumar Theorem 4.3), a Table 1 caption that overclaimed and was ambiguous, the
remaining long "further limits" sentence with undefined symbols, and several small precision and
notation problems. The verifier edits are listed below. I used process/w5/assign/front.json
(front-verify.json does not exist) and diffed every file against
process/w5/sections-before-w5/.

### Findings

Every adjudication in Section 3 was re-checked against the current text of the cited results
(setting.tex, setting-growthcert.tex, growth.tex, exact.tex, recourse-*.tex, constraints.tex,
optsets.tex, limits.tex, and the appendices for cor:cv-nu, thm:cr-exact, prop:weakcompl,
lim:prop:moments, prop:tu-misaligned and ex:tu-sum).

| Id | Verdict on the agent's handling | Verifier change |
|---|---|---|
| M-limits-1 | Correct: the abstract, intro and conclusion carry the fixed-degree qualifier, matching prop:lbproduct ("f(p)κ^{a(p)}I^C with a constant C"). | None. |
| M-limits-2 | Correct in substance, but ε was undefined in the intro. | "needs at least of order ε^{-n/2} queries for accuracy ε" (matches prop:oraclebarrier). |
| M-limits-5 | Correct. limits.tex uses the same locator. | None. |
| C-consistency-1, C-writing-20 | κ_V is used in both recourse rows. The caption had three defects: (i) "κ_V=κ(L^V,g) or κ(L^+,g)" did not say which row uses which; (ii) "In the recourse rows, exact bounds assume point growth of F" is wrong for the cut-recourse row (thm:cr-exact assumes core growth of V) and for the L^+=0 bound of thm:cv(ii), which needs no growth; it also omitted that thm:valuefn(c) needs a quadratic F; (iii) f' and κ_K were undefined. | The caption assigns κ_V per row and restricts the assumption to "the exact bounds with κ_V" in the rows of Theorems 7.2 and 7.9 ("a quadratic F with point growth"). It also defines f' and κ_K (Proposition prop:cr-growth). |
| (caption claim) | "Every algorithm returns a certificate that is valid without the growth hypotheses" is not established for every row. For example, thm:endpointset only says that the equations are "computed and checked". | Replaced by the pre-W5 statement, which is accurate: "Certificates are valid without the growth hypotheses, which enter only the running times." |
| C-consistency-4 | No change needed; r has one meaning in the front files. | None. |
| C-consistency-5 | Correct. The intro states ETH and rETH once with c, n' and 1/3, and limits.tex 262-263 refers to that statement. | The sentence said that the whole theorem "assumes" all three hypotheses. It now reads "Parts (a)-(c) ... assume ...; part (d) is unconditional" (lim:prop:oracle is information-theoretic). |
| C-consistency-8 | Correctly forwarded. appendix-smoothed.tex is gone; figures/E3_plateau_vs_n.pdf is still in the tree. | None (coordinator). |
| C-consistency-9 | Correct ("fixed bag size p"). | None. |
| C-writing-1, R-referee-1 | Front part done (see page spans below). | Further trims; see the related-work and intro edits. |
| C-writing-2, R-referee-2 | Mostly done. The "Section 10 also shows that ..." list was still one sentence of about 100 words. That is the defect the finding flagged. The sentence also used m and ε without defining them, and it no longer cited Proposition lim:prop:messages, which proves the 2^{m-1} bound and the polynomial running time of CT on the chain. | Split into a separate paragraph, "Section 10 proves further limits.", with four sentences. It now says "the expanding-box chain of length m", "CT certifies accuracy 2^{-q} on it in time polynomial in m and q" and "the exact Bellman message for its last state has at least 2^{m-1} quadratic pieces (Proposition lim:prop:messages)", as in ex:chain and lim:prop:messages. |
| C-writing-3, R-referee-3 | Correct; the text matches the verifier's corrected fix and coreA's Remark rem:nonconvex ("an indefinite Hessian" is used in both). | None. |
| C-writing-4 | Correct. I re-derived the abstract's scope sentence: H_{J0J0} ⪰ 2gI (Lemma lem:growthcert(b)) and g ≥ L/κ give λ_min ≥ 2L/κ, and growth gives F(x')-OPT ≥ g‖x'-x*‖² ≥ L‖x'-x*‖²/κ for every x'. Nothing in it is attributed to growth that minimality alone implies. Word count 250 (cwriting_wordcount.py). | None. Exact check: front-verify-scope.py. |
| C-writing-5 | Correct. | Also removed two remaining duplicates: the Del Pia-Khajavirad results sentence in related.tex (the theorem locator moved to the intro sentence) and the prop:cellwise sentence in related.tex, which repeated the intro "Results" paragraph (CONVENTIONS §1: one place per comparison). |
| C-writing-10 | Correct: f(p,t) in Theorem 1.1(b) and conclusion question (2). | None. |
| C-writing-13 | Correct: the EX description matches alg:ex and alg:rec. | None. |
| C-writing-15 | Correctly forwarded (main.tex). | None. |
| C-writing-16 | Correct. sec:intro-results now sits on a \paragraph; no file refers to it. | None. |
| C-writing-19 | Correct: no "optimizer" in the four files. | None. |
| C-literature-1 | Mostly correct, with one error. The text said that "one linear program over the interpolation solves the integer problem [Meyer1977], [HS, Theorem 4.3]". HS Theorem 4.3 (Algorithm 4.2) solves one LP per scale, ⌈log₂((m/n)‖b‖∞)⌉ LPs in total; only Meyer uses a single LP. Two notation clashes: Δ is reserved for the Section 6 denominator constant (CONVENTIONS §4), and B was used for the initial box width, for which the paper reserves s. | "the integer problem is solved by one linear program over the interpolation at all integer points [Meyer1977], or by one such linear program per scale [HS, Theorem 4.3]". Δ → Δ_A, B → s. The long sentences are split. Checked in the local HS full text: Section 1.3, Theorem 1.1, Remark 4.2, Algorithm 4.2, Theorem 4.3 and its proof, and the definition of ε-accuracy before Theorem 4.4. |
| C-literature-2 | Correct. | None. |
| C-literature-3 | Correct (related.tex part). | None. |
| C-literature-4 | Correct. | None. |
| C-literature-5 | Correct (intro part); consistent with limits.tex 354-357. | None. |
| C-literature-6 | Correct. | None. |
| C-literature-7 | Correct. | None. |
| C-literature-8 | Correct; the arXiv abstract (2102.01977) confirms "characterize the optimal number of evaluations ... to find and certify". | None. |
| C-literature-9 | Correct. The Ari-Hildebrand v2 abstract (local copy) states exact polynomial-time MIQP in fixed dimension. | The agent had dropped a load-bearing word: "Distributed constraint optimization" → "Continuous distributed constraint optimization". The cited works are continuous DCOP; discrete DCOP does not refine discretizations. |
| C-literature-11 | Correctly forwarded. | None. |
| R-referee-5 | No change needed: computation.tex 5-10 states that the families are synthetic. | None. |
| R-referee-6 | Correct. setting.tex (after Definition def:growth) proves that the smallest κ̄ exists, and rem:fpt uses it. | None. |

### Other verifier edits

intro.tex:
- Polynomial factors. "Under point growth, part (b) extends to fixed-degree polynomial factors" was
  changed to "the approximation result extends, with κ in place of κ̄, to factors that are
  polynomials of fixed degree". Corollary cor:poly is a different bound,
  f_d(p,κ)(I+q+1)^C, not the bound of part (b).
- Several minimizers. "..., which gives uniqueness, the dimension ..." could be read as "implies
  uniqueness". It now says "From it, uniqueness of the minimizer, the dimension of the optimal set
  and, if it is finite, the number of minimizers are computed in ...", as in cor:facecsp(iii).
- Recourse. "certify the largest possible reduction of their contribution to the coordinate
  curvatures" now reads "certify a reduction of the coordinate curvatures of the value function that
  is the largest possible for the block" (prop:vf-curv(c)).
- The Del Pia-Khajavirad sentence now carries the locator [Theorems 1-3].
- Smaller cuts: the duplicated clause "and the certificates are valid in every case" in the scope
  paragraph, and a shorter Organization paragraph.

related.tex:
- The rem:cv-instances parenthetical again says what the remark compares ("Khajavirad's
  elimination of the continuous components with our value factors"), not "this".
- "Value functions of parameters that enter linearly" again reads "that enter the objective
  linearly". Linear parameters in the constraints give convex value functions, so the dropped words
  were needed.
- "exactness of its relaxations" now reads "exactness of relaxations of box QP" (unclear
  antecedent).

conclusion.tex:
- "A replayable certificate also certifies a floating-point incumbent: projected onto the box, its
  exact value ..." now reads "turns a floating-point incumbent into a certified one: the exact value
  of its projection onto the box and a grid certificate give a rigorous gap". What is certified is
  the projected point, as in the corrected SCIP paragraph of Section 11.

No citation was removed. Every key cited before W5 is still cited in the four files.

### Cut plan, labels, page spans

- The label sets of all four files are identical to the snapshot. No label is duplicated in
  sections/, and every \ref in the four files resolves.
- References to moved results name their appendices: cor:cv-nu (C), lim:prop:moments (G.4),
  prop:tu-misaligned and ex:tu-sum (E), prop:weakcompl (B.2). thm:cr-exact (D.2) is cited in
  Table 1 by its appendix number.
- Page spans in the final build (/tmp/w5-front-verify, current tree including the other groups'
  edits; front-pages.py):
  - abstract: p. 1, 250 words.
  - sec:intro: 1.60-6.19, 4.59 pp. Theorem 1.1 is on p. 2, Theorem 1.2 on p. 3 and Table 1 at
    the top of p. 4 (about 0.65 p). "Results" to "Organization" is 3.91 pp including Table 1 and
    the bottom margin of p. 5.
  - sec:related: 6.19-9.00, 2.81 pp.
  - sec:conclusion: 69.80-70.93, 1.13 pp.
  - The references start on p. 71; the PDF has 127 pages.
- Compared with the agent's build, the intro is 0.07 pp longer and related work 0.06 pp longer.
  The extra length comes from the required precision fixes: the split limits paragraph, the
  caption and the HS correction. The cuts above recovered part of it.
- CUTPLAN status:
  - Results: slightly over 3 pp of text plus Table 1.
  - Related work: 2.81 pp, against "toward 2". All comparisons now appear in one place.
  - The HS comparison is done and in one place; rem:tu-bm is unchanged, and the constraints.tex
    pointer "Section 2 compares the two" is valid.
  - The scope caveat and the FPT wording are done.
  - The conclusion is about one page.

### Checks run (local, targeted; CI not consulted)

- Private build: `rm -rf /tmp/w5-front-verify && mkdir -p /tmp/w5-front-verify && rsync -a main.tex
  macros.tex references.bib sections figures /tmp/w5-front-verify/ && cd /tmp/w5-front-verify &&
  latexmk -pdf -interaction=nonstopmode main.tex`, run after every round of edits. Final result:
  exit 0, no `!` errors, no undefined references, no multiply defined labels, and no overfull or
  underfull boxes. The only warning is the undefined citation AbelloEtAl2001 (limits.tex 267,
  p. 60), which is not in the front files.
- `python3 process/w5/checks/front-verify-scope.py` (new): exact rational checks of the abstract's
  scope inequalities. On the Example ex:family block (g=1/2, L=21/8, κ=21/4) it checks
  λ_min(H_{J0J0}) ≥ 2L/κ and F-OPT ≥ L‖x-x*‖²/κ on a 17³ grid, and it checks g ≥ L/κ on
  10^4 random rational pairs. Passed.
- `python3 process/w5/checks/front-scope.py` (agent's script): passed.
- `python3 process/w4/checks/cwriting_wordcount.py`: abstract 250 words.
- `python3 process/w4/checks/cwriting_longsent.py 50`: no sentence of 60 or more words remains in
  the four files.
- Label, \ref and cite-key scripts:
  - the label sets are unchanged and there are no duplicates;
  - every cite key in the four files exists;
  - references.bib has no duplicate or uncited keys;
  - no key was dropped relative to the snapshot.
- Crossref API, queried by the verifier, for the 9 new DOIs (Meyer1977, PeyrlParrilo2008,
  KaltofenEtAl2008, EiflerGleixner2023, Ye1992, MehrotraYe1993, DavarniaVanHoeve2021,
  DavarniaKiaghadiQiu2026, DelPiaWeismantel2014). Authors, titles, venues, volumes, issues and
  pages all match the entries.
- arXiv API for Bachoc et al. (2102.01977): title and NeurIPS 2021 confirmed. The page range
  24180-24192 is the agent's, from the proceedings BibTeX, and was not re-fetched.
- Local full texts read: Hochbaum-Shanthikumar 1990 (sections cited above) and the Ari-Hildebrand
  v2 abstract.
- Visual check of the rendered pages 4 and 5 (Table 1, Theorem 1.2, extension paragraphs).

### Requests for other files

- coordinator, references.bib: add AbelloEtAl2001 (cited in limits.tex 267). It is the only
  undefined citation in the build. I did not add it myself because the limits group or the
  coordinator may add it concurrently, and a duplicate key would break BibTeX.
- The agent's requests 1-5 in Section 6 stand. These are the title (C-writing-15), CONVENTIONS §5,
  the bib provenance comments (C-literature-11), figures/E3_plateau_vs_n.pdf, and the optional move
  of tab:chain.

### Unresolved

- Length. Results is slightly over the 3-page target (about 3.2 pp of text plus Table 1), and
  related work is 2.81 pp against "toward 2 pp". Further cuts would remove required content or
  citations.
- Table 1 has no separate Output/certificate column, so it deviates from the column list in
  CONVENTIONS §1. The coordinator should confirm this.
- AbelloEtAl2001 is still missing from references.bib (coordinator or limits).
