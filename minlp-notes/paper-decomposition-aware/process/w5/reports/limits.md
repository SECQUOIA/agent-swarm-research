# W5 report: limits group

Files edited: `sections/limits.tex`, `sections/appendix-lbproduct.tex`.
`sections/appendix-moments.tex` is unchanged; it is now subsection G.4
instead of G.3.

## Page spans (private build in /tmp/w5-limits, main.aux and pdftotext)

| | Before (W5 snapshot of my files) | After |
|---|---|---|
| Section 10 | pp. 62-71 (62.20-71.45, 9.25 pp) | pp. 58-65 (58.20-65.75, 7.55 pp) |
| Appendix G | pp. 119-123 (4.97 pp) | pp. 118-125 (118.89-125.56, 6.67 pp) |

Net saving in the main text: **1.70 pp**. In the baseline PDF the moved
proofs took 1.95 pp and the opening took 0.80 pp. The roadmap takes 0.35 pp.
The summary sentences and the new precision sentences (M-limits-1, -2, -3,
C-literature-5) add about 0.4 pp. The measurement script is
`process/w3/checks/w5-limits-pages.py`.

## CUTPLAN items

1. **Proofs moved to Appendix G (done).** The proofs at limits.tex 422-466
   (`lim:prop:messages`), 502-545 (`lim:prop:setgrowth`), 576-607
   (`prop:oraclebarrier`) and 647-660 (`lim:prop:constraints`) are now in the
   new subsection G.3, "Proofs for Sections 10.4-10.6"
   (`\label{app:limits-proofs}`, at the end of appendix-lbproduct.tex). Each
   proof starts with `\begin{proof}[Proof of Proposition~\ref{...}]`. In the
   main text, each statement is followed by a sentence of at most three
   lines that points to the appendix and gives the idea of the proof. The
   proofs depend only on objects that remain globally available:
   Proposition `prop:cellwise`(c), Definition `def:cert` (C1)/(C2) (now
   cited explicitly in the moved proof), m_j, Q, D, w_i,
   `GareyJohnson1979`. The moved proofs contain no labels. The
   main-line proofs of Sections 10.1-10.3 stay in the main text, as the
   C-writing-1 verifier required.
2. **Opening bullet list shortened (done, C-writing-9).** Lines 3-45 are
   replaced by a roadmap. It keeps the four-hypotheses paragraph, states
   that the section proves Theorem `thm:intro-lower` (10.1 part (a),
   10.2 part (d), 10.3 parts (b) and (c)), and gives one clause for each of
   10.4-10.7. The vague phrase "close to necessary" and the fourth copy of
   the lower-bound summary are removed. The Del Pia-Khajavirad paragraph
   (old 46-50) is kept.

## Adjudication of assigned findings

| Id | Verdict | Reason | Change |
|---|---|---|---|
| M-limits-1 | ACCEPTED (limits part) | The shorthand "exponent of kappa cannot be o(p)" omits the fixed degree in I. | The bullet is gone (roadmap). Proposition `prop:lbproduct` is retitled "The exponent of $\kappa I$ cannot be $o(p)$" and now ends with "...has $a(p)=p/2+O(1)$ and $C=5$". The text after it says that the improvement to o(p) is excluded while the degree in I stays fixed. It explains why: kappa and I are polynomially related on the hard instances, so a bound such as kappa^3 I^p is not excluded. The appendix proof now derives $C=5$: $(I+2)^5\le3^5I^5$, and $(1+\log_2\kappa)^2\le4\kappa$ is stated as the reason for the bound on f. Abstract, intro, conclusion and rem:fpt: see requests. |
| M-limits-2 | ACCEPTED (reworded) | The old comparison did not separate CT from the barrier. | The paragraph after `prop:oraclebarrier` now says: under point growth CT's nodes per coordinate do not depend on the accuracy, so its evaluations grow only through the number of stages, which is linear in log(1/eps) (Algorithm `alg:ct`, Remark `lim:rem:oracle`). Under unknown set growth, every algorithm that queries values, gradients and Hessians needs Omega(eps^{-n/2}) queries, already for n=p=1 with kappa_S=1. The proof idea (hidden C^2 bump) is given in one sentence. "the functions f_{c,w}", now defined only in the appendix, became "the bumps". |
| M-limits-3 | ACCEPTED (different source) | SETH was used but not defined. | Section 10.3 now defines SETH with the same symbols as ETH ($\epsilon$, $k$, $n'$) and cites `\cite[Chapter~14]{CyganEtAl2015}` (existing key; Chapter 14 is the ETH chapter whose Theorem 14.21 the appendix already cites). The two later uses say "SETH". No new key. |
| M-limits-4 | ACCEPTED | I = Theta(k log k), so "exponential in the input length" was imprecise. | limits.tex: "exponential in the number of variables". Remark `lim:rem:dk`: "For $c=2^k$, $k\ge2$, ... $\kappa\ge80(k+1)4^k$ is exponential in the number of variables. The instance has $O(k)$ monomials and bags, listed by variable indices of $\Theta(\log k)$ bits, so $I=\Theta(k\log k)$ and $\kappa\ge2^{\Omega(I/\log I)}$." The condition k>=2 matches the remark's hypothesis c>=3. |
| M-limits-5 | REJECTED for now (not applied) | The locator is verified only in arXiv 1501.00288v15 (Appendix A, "Dependence on eps in Theorem 15", formulation (26); local copy `literature/papers/bienstock2018-.../fulltext.md` 830-894). The SIOPT version (28(2):1121-1150) could not be checked: epubs.siam.org returned 403 and Unpaywall reports it closed. The arXiv title and theorem numbering differ from the journal's. | The citation in Section 10.6 stays without a locator, as the task instructs. See Unresolved. |
| C-consistency-2 | ACCEPTED | The old bullet said bag-local corrections are not valid lower bounds. | The bullet is removed. The roadmap says "bag-local corrections combined with grid min-marginals are not valid lower bounds". The first paragraph of Section 10.7, which was already qualified, now points to "Proposition~\ref{prop:star} in Appendix~\ref{app:recourse-convex}" (recA moved it) and to Theorem `thm:cr-filter`. |
| C-consistency-5 | ACCEPTED (limits part) | ETH was stated twice with different symbols. | ETH, rETH and now SETH are stated once, in Section 10.3, with the symbols c, n' (as the fix asks). The intro should refer to them (request). nu in my files always means negative curvature. eta in limits.tex is the TU mesh unit, as in Section 8. No other change. |
| C-writing-5 | MODIFIED (limits part) | The duplicate lower-bound bullet is removed. The fix's second part (move the ETH definition to Section 1) conflicts with C-consistency-5 (state it once in Section 10.3). The front agent is rewriting the intro concurrently, so deleting the Section 10.3 definition could leave ETH undefined. | The definitions stay in Section 10.3, where the propositions and the appendix proof use them. A request asks the front agent to refer to them or use the same symbols. |
| C-writing-9 | ACCEPTED | See CUTPLAN item 2. | Roadmap. |
| C-writing-10 | ACCEPTED (limits part, minor) | f(p,kappa) in limits.tex and in the appendix is an evaluation of f(p,t) (growth.tex now defines f(p,t)), not a definition. | "the function f(p,kappa)=... of Theorem" became "the factor f(p,kappa)=... in Theorem". My files contain no stage limit J. In the moved proof, J denotes a grid interval (the reserved meaning) and is now named where it is introduced: "Let $J=[a,a']$ be a grid interval". |
| C-literature-5 | ACCEPTED (limits part) | (a) The box formulation of maximum independent set had no source. (b) The text did not say what is new in the rETH reduction. | (a) "a variant of the box formulation of maximum independent set \cite{AbelloEtAl2001}". Verified in the authors' preprint (mauricio.resende.info/doc/indep-polyn.pdf, Theorem 3, (P2): alpha(G)=max over [0,1]^n of sum x_i - sum_E x_i x_j). Bibliographic data verified on Crossref. This needs a new key (below). (b) After `prop:lbproduct`: "It encodes multicolored clique in the standard way, with one integer variable of domain size N_0 per color class and one pair constraint for each pair of classes. What is new is a quadratic encoding of the pair constraints with a unique minimizer, obtained by random weights and isolation, and with kappa polynomial in kN_0." I did not attribute the CSP encoding to Chen et al. 2006, because I could not check that paper for it; I did not add Marx 2010 (new key, not checked). |
| R-referee-2 | ACCEPTED (limits part) | The lower-bound summary was repeated. | Section 10 no longer repeats it. The precise statements are in Propositions 10.1-10.6 only. |

## New BibTeX entry (for the coordinator; cited in limits.tex)

```
@article{AbelloEtAl2001,
  author  = {Abello, James and Butenko, Sergiy and Pardalos, Panos M. and Resende, Mauricio G. C.},
  title   = {Finding independent sets in a graph using continuous multivariable polynomial formulations},
  journal = {Journal of Global Optimization},
  volume  = {21},
  number  = {2},
  pages   = {111--137},
  year    = {2001},
  doi     = {10.1023/A:1011968411281}
}
```
Crossref (`api.crossref.org/works/10.1023/A:1011968411281`) matches the
title, authors, journal, volume 21(2), pages 111-137 and date 2001-10. Until
the coordinator adds the key, `\cite{AbelloEtAl2001}` renders as [?]. My
private build added the entry to its own copy of references.bib.

## Labels

- All labels of my three files are kept (checked by diffing the label
  lists against `process/w5/sections-before-w5`).
- New label: `app:limits-proofs` (Appendix G.3).
- No labelled object moved. The four moved proofs had no labels, and their
  propositions stay in Section 10 with the same labels.
- Appendix G is now G.1 `app:dk`, G.2 `app:lbproduct`, G.3
  `app:limits-proofs`, G.4 `app:moments`.

## Requests for other files

1. front, `abstract.tex` 22-23, `intro.tex` 196-197 (the "Thus ..."
   paragraph), `conclusion.tex` 16-18; coreB, `growth.tex` rem:fpt
   (M-limits-1). Qualify "the exponent of kappa cannot be o(p)" as "the
   exponent of kappa in a bound f(p)kappa^{a(p)}I^{O(1)} (fixed degree in
   I) cannot be o(p)", or replace the sentence by a reference to Theorem
   1.2 / Proposition `prop:lbproduct`.
2. front, `intro.tex` 205-208 (M-limits-2). Replace "needs a number of
   queries that grows with the accuracy" by "needs at least of order
   eps^{-n/2} queries (Proposition `prop:oraclebarrier`), whereas CT needs
   a number of evaluations logarithmic in 1/eps under point growth".
3. front, `intro.tex` 161-165 (C-consistency-5 / C-writing-5). The intro
   defines ETH with delta and m, Section 10.3 with c and n'. Either refer to
   Section~\ref{sec:limits-width} for the definitions of ETH, rETH and SETH,
   or use the symbols c and n'.
4. front, Theorem `thm:intro-lower`. The Section 10 roadmap cites its parts
   (a) conditioning/P≠NP, (b) width/ETH, (c) rETH, (d) value oracle. Please
   keep that order, or tell the coordinator so that the roadmap sentence can
   be changed.
5. front, `intro.tex` 210-212 (M-limits-5). Do not add "Appendix A" to the
   Bienstock-Muñoz citation unless it is verified in the SIOPT version. Only
   arXiv v15 is verified. limits.tex has no locator.
6. front, `intro.tex` 214-217 (C-literature-5(b)). Section 10.3 now states
   what is new in the rETH reduction. The intro's novelty sentence can say
   it the same way or point to it.
7. coordinator, `references.bib`: add `AbelloEtAl2001` (above).

## Checks run (targeted; no project-wide verification, CI not consulted)

- `latexmk -pdf -interaction=nonstopmode main.tex` in a private copy
  (/tmp/w5-limits, with the current sections of all agents and the
  AbelloEtAl2001 entry added to the copy's bib). Exit 0, no `!` errors, no
  undefined references or citations, no multiply defined labels, and no
  overfull or underfull boxes in the whole log (the last run had none
  anywhere). An earlier run had one overfull box, in appendix-tu.tex (not
  mine).
- Baseline build (/tmp/w5-limits-before) with the W5 snapshot of my three
  files, for the before page spans.
- `python3 process/w3/checks/w5-limits-pages.py <pdf>`: fractional page
  spans of Section 10, its subsections and Appendix G.
- `python3 process/w3/checks/w5-limits-constants.py`: PASS. It checks
  (1+log2 k)^2 <= 4k for k >= 1 (hence f(p,k) <= 4c0(c1 p)^p k^{p/2+2});
  (I+2)^5 <= 3^5 I^5; for c=2^k, ell=k+1, 5 ell+2=5k+7 and
  80 ell c^2=80(k+1)4^k; and (1/(2 sqrt(6 eps))-1)^n-1 = Omega(eps^{-n/2}).
- Source checks: Abello et al. Theorem 3 (P2) in the authors' preprint;
  Crossref metadata of Abello et al.; the Bienstock-Muñoz arXiv v15 appendix
  in the local copy. The SIOPT page was not reachable (HTTP 403).
- I did not rerun the W4 construction scripts (`mlimits_*.py`). The moved
  proofs and the constructions are unchanged apart from the two explicit
  cross-references added.

## Unresolved

- M-limits-5: the "Appendix A" locator for Bienstock-Muñoz (SIOPT 2018)
  still needs a check of the journal version. If the journal version also
  has the running-sum system in Appendix A, use
  `\cite[Appendix~A]{BienstockMunoz2018}` at limits.tex (Section 10.6, first
  sentence) and in the intro.
- The ETH/SETH definitions live in Section 10.3. Whether the intro keeps its
  own definition (duplicate, different symbols) depends on the front agent
  (request 3).

## Verification (W5 verifier)

Scope: I diffed `sections/limits.tex`, `sections/appendix-lbproduct.tex` and
`sections/appendix-moments.tex` (unchanged) against
`process/w5/sections-before-w5/`, and checked the twelve findings in
`process/w5/assign/limits.json`. There is no `limits-verify.json`. W4
`all-results.json` has no verifier entries for these ids, so the
reviewers' fixes are the reference.

### CUTPLAN

- **Proof moves: confirmed.** A whitespace-normalized comparison shows that
  the four proofs in G.3 are verbatim copies. The only changes are "Part 1:"
  to "Part 1.", "Let $J=[a,a']$" and "of Definition~\ref{def:cert}". All
  dependencies are still available: `prop:cellwise`, `def:cert`, `def:corr`,
  `def:filter` and `GareyJohnson1979`. The notation each proof uses is
  defined in its proposition, which stays in Section 10.
- **Summaries: re-derived and correct.** Each main-text summary points to
  `app:limits-proofs`.
- **Roadmap: correct.** It matches the current Theorem `thm:intro-lower`:
  (a) is proved in 10.1, (b) and (c) in 10.3, and (d) in 10.2.
- **Labels: unchanged.** The only addition is `app:limits-proofs`. No label
  is duplicated in `sections/*.tex`.

### Findings

| Id | Verifier verdict | Notes / changes made by the verifier |
|---|---|---|
| M-limits-1 | Confirmed, with one wording fix | Re-derived $C=5$. Theorem `thm:approx`(b) gives $f(p,\bar\kappa)(I+q+1)^5$. With $q=1$, $(I+2)^5\le3^5I^5$, and $(1+\log_2t)^2\le4t$ for $t\ge1$ (its square-root form has a minimum of 0.83 > 0). "$\kappa$ and $I$ are polynomially related on the hard instances" was not proved: the appendix only bounds both above by $(kN_0)^{c_2}$. Changed to "on the hard instances both $\kappa$ and $I$ are bounded by a polynomial in $kN_0$", and "is not excluded" to "it does not exclude a bound such as $\kappa^3I^p$". |
| M-limits-2 | Confirmed, with one fix | Proposition `prop:oraclebarrier` is stated for deterministic algorithms. Added "deterministic" in the paragraph after it and in the roadmap. "Linear in $\log(1/\varepsilon)$" holds: $j_{\max}$ is the least integer with $\frac9{16}n_P\eta_0^2 4^{-j_{\max}}\le\varepsilon$. The intro sentence (front) is fixed too. |
| M-limits-3 | Confirmed | Chapter 14 of Cygan et al. states SETH. |
| M-limits-4 | Confirmed | For $c=2^k$: $\ell=k+1$, $5\ell+2=5k+7$, $D=2c$, $20\ell D^2=80(k+1)4^k$ (exact check). $I=O(k\log k)$ is enough for $\kappa\ge2^{\Omega(I/\log I)}$. |
| M-limits-5 | **Overturned: ACCEPTED and applied** | The `BienstockMunoz2018` entry in references.bib carries the note "Theorem and appendix numbers refer to the preprint arXiv:1501.00288v15". constraints.tex and related.tex already use v15 locators, and intro.tex (front) now cites `\cite[Appendix~A]{BienstockMunoz2018}`. In the local v15 copy (`literature/papers/bienstock2018-.../fulltext.md` 830ff), Appendix A, "Dependence on eps in Theorem 15", contains the running-sum Subset Sum system (26) of treewidth 2. So the locator is correct under the paper's stated convention. Section 10.6 now cites `\cite[Appendix~A]{BienstockMunoz2018}`. |
| C-consistency-2 | Confirmed | `prop:star` is in `app:recourse-convex` (appendix-recourse-convex.tex 144). |
| C-consistency-5 / C-writing-5 | Changed by the verifier | The front agent now defines ETH and rETH before `thm:intro-lower` with the Section 10.3 symbols ($c$, $n'$), so both were defined twice, identically. Section 10.3 now reads "we use ETH and rETH, as stated before Theorem~\ref{thm:intro-lower}, and SETH: ..." and defines only SETH. This applies the C-writing-5 fix and states each hypothesis once. It depends on intro.tex keeping these definitions (now at intro.tex 202-207). |
| C-writing-9 | Confirmed | — |
| C-writing-10 | Confirmed | $f(p,t)$ in growth.tex 209 matches the evaluation in limits.tex and in the appendix. |
| C-literature-5 | Confirmed | (a) The Abello et al. metadata is re-checked on Crossref (title, authors, J. Glob. Optim. 21(2):111-137, 2001). (b) The summary matches the appendix: one variable $x_c\in[1,N_0]$ per class, one path gadget per pair, $\kappa\le(kN_0)^{c_2}$. Leaving "the standard way" without a citation is acceptable; the appendix cites Chen et al. and Cygan Thm 14.21 for the lower bound. |
| R-referee-2 | Confirmed | — |

### Other fixes by the verifier

- **Summary after `lim:prop:setgrowth`.** "The corrections outweigh the edge
  terms" was imprecise: equality is possible ($L_i=2$, $|v_k-v_i|=\delta_i/2$,
  $w_i(v_i)=\delta_i$). It now says that each other coordinate is set,
  outward along the path from $j$, to the grid node nearest to the previous
  coordinate, and that its correction is at least the square term of its
  edge to the previous one.
- **Source rewrap.** One long source line in the moved proof of (c) is
  rewrapped; the output is unchanged.

### Checks run (targeted; no project-wide verification, CI not consulted)

- **Private build.** `latexmk -pdf -interaction=nonstopmode main.tex` in
  `/tmp/w5-limits-verify`, with `AbelloEtAl2001` added only to the copy's
  bib. Exit 0. The whole log has no `!` errors, no undefined references or
  citations, no multiply defined labels and no overfull or underfull boxes.
  Rebuilt after the last edit with the same result.
- **Exact checks.** `python3 process/w5/checks/limits-verify-constants.py`:
  PASS. It checks:
  - $(1+\log_2t)^2\le4t$;
  - $(I+2)^5\le3^5I^5$;
  - the Remark `lim:rem:dk` counts;
  - Proposition `lim:prop:setgrowth`(a), $m_j(v)\le-L_jw_j(v)^2/8$, by
    exhaustive exact minimization on 340 random grids with $n=2,3,4$.
- **Other checks.** Label diff against the snapshot, duplicate-label grep,
  the whitespace-normalized comparison of the moved proofs, and a Crossref
  lookup of DOI 10.1023/A:1011968411281.
- **Page spans.** Measured with `process/w3/checks/w5-limits-pages.py`.
  Section 10 runs pp. 57-64 (57.23-64.75, 7.52 pp; the snapshot had 9.25 pp,
  so the saving is 1.73 pp). Appendix G runs pp. 116-123 (116.88-123.55,
  6.67 pp), with G.1 and G.2 on p. 117, G.3 on p. 119 and G.4 on p. 120.

### Remaining items (other files)

1. **front, M-limits-1.** `abstract.tex` 22-23 and `conclusion.tex` 16-18
   still say "the exponent of $\kappa$ cannot be $o(p)$" without the
   fixed-degree qualifier. intro.tex now has it.
2. **front.** intro.tex must keep the ETH/rETH definitions before
   `thm:intro-lower`, because Section 10.3 now refers to them.
3. **coordinator.** Add `AbelloEtAl2001` to references.bib (entry above,
   metadata re-verified). Until then `\cite{AbelloEtAl2001}` renders as [?].
4. **Process note.** The revision agent reported that it once sent the
   account email address as the contact parameter of an Unpaywall API
   query. No file is affected; this is recorded for the user.
