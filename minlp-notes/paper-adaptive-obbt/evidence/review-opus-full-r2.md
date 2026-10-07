# Full manuscript review, round 2 (Opus)

Reviewer role: independent final Opus reviewer. The review was read-only.
I wrote only this file. I edited no manuscript, evidence, or companion file.
I ran no experiment, numerical routine, project-wide check, or CI inspection,
and I did no literature search or KB work. Source accuracy is assessed only
against the literature lead's delivered audit and bibliography.

## 1. Verdict

**Ready for submission after small text edits. No blocking issue remains.**

- All findings of `review-opus-full-r1.md` (M1–M3, m1–m15) and of
  `review-opus-foundations-r1.md` (F1–F8, A1–A8) are closed (Section 4).
- **M1 is closed against the final audit.** The final bounded audit
  (`evidence/literature-audit.md`, SHA-256 `3a109aeb…`) gives dispositions
  for all 37 keys and 13 access gaps. The merged bibliography matches the
  vetted file. The manuscript respects every disposition and caution I could
  check (Section 2). Sol's source-integration review
  (`review-integration-r3.md`) independently accepts the same scope.
- I found no false implication, omitted premise, missing proof obligation,
  claim–policy mismatch, or unsupported priority contrast. The front matter
  matches the body statements, including:
  - strict factors and sufficiently small scales;
  - upper-order wording;
  - the singleton certificate;
  - pool expiry versus the box threshold;
  - the current-round-only scope of the measured policy.
- **Recommended before submission (small, no result changes):** two edits
  that align the text with the audit (N3, N12) and eight text or citation
  edits (N5–N11). N1 and N4 and two further notes are optional.

## 2. M1 closure against the final audit

**Inputs.**

- Final audit: SHA-256 `3a109aeb…`, 242 lines. I first read revision
  `736e57cb…`. The final revision changed only the identities of two uncited
  access-gap items: item 9, the title of the 2007 Caprara–Locatelli report,
  and item 13, the title of the 1996 Ryoo–Sahinidis paper. The manuscript
  relies on the read 2010 and 1995 papers instead. The dispositions this
  review uses are textually unchanged.
- Vetted bibliography: `evidence/literature-references.bib`, 37 entries,
  `5ffcc29f…`.
- `references.bib` matches the vetted file entry by entry, with three
  harmless root changes: DOI URLs for `borrelli2003parametric` and
  `walker2011anderson`, and a brace-protected `{McCormick}` in
  `bompadre2013-…`.
- All 37 keys are cited (`main.aux`). The source check passes.
- No manuscript file changed after my final snapshot (02:48:10 UTC). I
  confirmed this again at 02:55:11 UTC.

**Dispositions checked against the text.**

- **Contribution boundary.** The introduction (`introduction.tex:156–189`)
  and related work claim only the boundary the audit supports:
  - the shape- and position-indexed tangent model and box-to-box map with
    sufficient contraction and stall tests;
  - model-specific exact quadratic results;
  - the composite coefficient for ordinary clipped McCormick, with
    composition and order rules credited;
  - the scalar threshold presented as matching the cluster thresholds;
  - rebuilt-hull certificates distinguished from frozen-round filtering.
- **Repeated OBBT is credited as prior art.** Nagarajan et al., Sundar et
  al., Caprara et al., Coffrin et al., and Puranik–Sahinidis are cited.
  "Rebuilding, repeating, and using an incumbent cutoff are established
  procedures" (`related.tex:68–69`).
- **Unread sources.** A grep finds no absolute-novelty or contrast phrase
  ("novel", "first to", "to our knowledge", "no prior", "unlike", "in
  contrast to"). The only novelty disclaimer is `effort.tex:12`.
  - Bompadre–Mitsos 2012 and Najman–Mitsos 2016 are cited only at the
    generic order level.
  - Bompadre–Mitsos–Chachuat 2013 is credited without a negative claim.
  - Robinson is cited only as a general error-bound attribution.
  - None of Jansson, Zamora–Grossmann, Locatelli–Schoen, Najman–Mitsos
    2019, the Caprara–Locatelli report, or Ryoo–Sahinidis 1996 is cited.
  - Nothing says that prior observed ratios do not exist.

**N1. Coffrin et al. 2015 (resolved; optional wording).** The audit read the
full chapter (pp. 10–12): "repeated feasibility-based bound consistency …
not incumbent-cutoff OBBT". `related.tex:56–59` ("iterate feasibility-based
bound propagation") is consistent with this. Sol's r3 reads the sentence as
FBBT. My unverified recollection is that the chapter computes its
consistency bounds by optimizing over the convex relaxation; that would be
OBBT without a cutoff, not interval FBBT. Optional wording that is true
under either reading and keeps the audit's distinction: "iterate bound
tightening without an objective cutoff to strengthen convex relaxations of
power-network models".

**N2. Sundar et al. (resolved).** `related.tex:63–67` attributes the details
to the preprint, and the bibliography note names arXiv v3 as the text
consulted. This is exactly what the audit prescribes.

**N3. Belotti et al. (minor alignment).** The audit says to cite the 2010
published chapter jointly with the 2012 manuscript that was read.
`related.tex:51` does so. `foundations.tex:10–11` still cites only
`belotti2012fbbt` for greatest fixed points of FBBT. Add the 2010 key there
as well.

**N12. Number-zero callbacks (audit guidance not yet reflected).** For
`scip1002tree` the audit says: "the probing interpretation is inferred from
source behavior. Keep the manuscript's safer phrase 'number-zero
callbacks.'" The text does disclose the inference (`experiments.tex:272–273`),
but three places present "probing nodes" as a category:

- the `tab:work` row label (line 292);
- "the policy treated all probing nodes of a run as one node" (line 275);
- "Probing nodes consumed 360 of the fixed variant's LPs" (line 343).

Suggested fixes:

- Relabel the row "Nonroot, number 0".
- Line 275: "the policy treated all nonroot nodes with number zero in a run
  as one node".
- Line 343: "Callbacks at nonroot nodes with number zero consumed…".
- Keep lines 268–273 as the explanation of what these nodes probably are.

**Positive check: SCIP 10.0.2 defaults.** The audit limits `scip2026obbt` to
"this version's behavior only", that is, the inspected master commit. The
10.0.2 defaults stated at `experiments.tex:91–93` are supported by the
retained 10.0.2 source (`research-20260929/publication/scip-bug/src/scipoptsuite-10.0.2/`):

- `prop_obbt.c` has `PROP_FREQ 0` (root only) and
  `DEFAULT_ITLIMITFACTOR 10.0` (a budget tied to root LP iterations).
- `prop_nlobbt.c` has `PROP_FREQ -1` (disabled).
- `prop_genvbounds.c` has frequency 1 with timing `ALWAYS`.

A citation for this statement is item N5.

Sol's source-integration review (`review-integration-r3.md`, snapshot
02:54:30 UTC) accepts the same paragraphs and bibliography against this
audit. It does not discuss `foundations.tex:10–11` (N3) or the
number-zero wording in `experiments.tex` (N12). The literature lead reports
KB_CHECK=ok. I did not inspect the run record or the KB.

## 3. Other findings (minor)

**N4 (optional). The Collatz–Wielandt name.** The abstract (lines 10–11),
`introduction.tex:51`, and `local-rates.tex:212–214` call `r*` an upper
Collatz–Wielandt number. The audit notes that the comparison is elementary
and needs no nonlinear Perron–Frobenius theorem. Crediting the borrowed name
with a standard reference is still good practice. The alternative is to
describe `r*` without the name.

**N5. Cite the software and test set.** This carries over source request 8 of
round 1. MINLPLib (`experiments.tex:17`, `introduction.tex:144–145`),
SCIP 10 (the SCIP Optimization Suite report), HiGHS, PySCIPOpt, and Gurobi 13
are used but not cited; versions appear only in the text. Mathematical
programming journals normally expect these citations. For the defaults at
`experiments.tex:91–93`, cite the release-tagged 10.0.2 source, as
`scip1002tree` already does for `tree.c`. These are additions for the
literature lead to vet.

**N6. Fix a stale cross-reference left by the M3 move.**
`constraints.tex:823–824` places `prop:restricted-tangent-con` in
`Section~\ref{sec:local-rates-tangent}` (4.2). It is Proposition 4.14 in
Section 4.3; use `\ref{sec:local-rates-contraction}`. Also,
`local-rates.tex:157–158` says "A remark on exactly represented linear
equations closes Section 4.3". The section now ends with the remark and the
restricted proposition, so write "The restricted tangent contraction for
exactly represented linear equations closes Section 4.3."

**N7. Paraphrase the stall theorem correctly.** `discussion.tex:18–22`
summarizes `thm:local-stall` as "the relaxation's gap at the center of a box
outweighs the curvature along the coordinate directions". That describes the
quadratic row condition (a) of `prop:quadratic-rows`, not the general
hypothesis. Suggested text:

> If on every face of a box shape some point has negative tangent-model
> value, that is, its second-order relaxation gap exceeds the objective's
> second-order growth, then the boxes of that shape around a minimizer are
> fixed at every sufficiently small scale and every cutoff $U\ge f^*$
> (Theorem~\ref{thm:local-stall}); for quadratic objectives with McCormick
> relaxations, condition~(a) of Proposition~\ref{prop:quadratic-rows} gives
> this at every scale.

**N8. Remove an "if and only if" reading.** `introduction.tex:126–129` says
the singleton "bounds the remaining movement, exactly when the iterates
converge to that point". `local-rates.tex:1308–1310` says "exactly if the
iterates converge to it". Both can be read as "if and only if". Use the
discussion's wording (`discussion.tex:54–56`): "…bounds the remaining
movement, and the bound is exact if the iterates converge to that point."

**N9. Upper bounds motivate; they do not show worth.**
`introduction.tex:131–133` says the upper bounds of order $\sqrt\epsilon$ and
$\epsilon$ "explain why OBBT is worth reconsidering after the incumbent
improves". Upper bounds show that a better incumbent permits a smaller
limit. They do not show that reconsidering pays off, and the evidence
section is careful on exactly this point. `algorithms.tex:468–471` already
says "motivate". Suggested text: "…motivate reconsidering OBBT after the
incumbent improves; in the two-variable model the limit itself shrinks at
exactly these orders."

**N10. Align "three objects" with "three limits".** `introduction.tex:30–31`
says "three objects limit what further rounds can remove", but item (iii) is
a rate. Foundations now says "three limits on further tightening"
(F6); use that phrase.

**N11. Write "at most", not "below", for the maximum.**
`experiments.tex:390` says the propagator time "stayed below 1.00501 seconds
per run", while `experiments.tex:325` reports 1.00501 s as the largest run
total. Write "stayed at most 1.00501 seconds per run".

**Optional.**

- `related.tex:85`: `thm:composite-expansion` covers the clipped and the
  unclipped construction, which have the same expansion. The audit's phrase
  "ordinary clipped McCormick" is accurate for the monotone setting; "clipped
  or unclipped" would match the theorem exactly.
- Source request 9 of round 1 (algorithm-portfolio citations for
  `thm:interleaving` and `prop:rescue`) remains optional, because
  `effort.tex:11–12` disclaims novelty.

## 4. Closure of earlier findings

| Finding | Status in the reviewed snapshot |
| --- | --- |
| M1 literature | Closed against the final audit (`3a109aeb…`), consistent with Sol's `review-integration-r3.md`: 37 keys vetted, merged, and cited; contribution boundary and cautions respected; alignment edits N3 and N12 remain. |
| M2.1 contribution sentence | Closed: `introduction.tex:182–186` limits the policy to current-round screening and heuristic triggers. |
| M2.2 evidence sentence | Closed: `introduction.tex:149–151` attributes the search-time argument to Section 10. |
| M3.1 repeated policy disclaimer | Closed: kept in the abstract, `introduction.tex:147–149`, `algorithms.tex:520–544`, `experiments.tex:380–383`, and `discussion.tex:111–112`; removed from the closings of certificates, residual, and constraints. |
| M3.2 observed progress | Closed: `prop:history` and all artificial history examples are in `residual.tex:295–425`; `local-rates.tex:1289` and `discussion.tex:64` cite `prop:history`. |
| M3.3 restricted tangent theorem | Closed: `local-rates.tex:448–529`; proof byte-identical per `structure-revision.md`. Stale pointer: N6. |
| Appendix moves | Closed: parametric proofs, scheduling, and numerical validation appendices; labels kept; pointers resolve. |
| m1 mixing example | Closed: `cutoff.tex:142–160` separates stale lifts from a truly unprotected hull at cutoff 0. |
| m2 `prop:continue` | Closed: `cutoff.tex:297–319`, finite-step sandwich, no closedness or $U'\ge f^*$; empty-set convention at `foundations.tex:124–126`. |
| m3 Starting paragraph | Closed: `discussion.tex:7–37`. Paraphrase precision: N7. |
| m4 upper orders | Closed: `discussion.tex:69–74`, `local-rates.tex:1160–1163`. |
| m5 singleton at $\epsilon=0$ | Closed in substance in the introduction, local rates, and discussion. Wording: N8. |
| m6 numerically safe step | Closed: `certificates.tex:189–193` requires proved safe dual bounds. |
| m7 two thresholds | Closed: `introduction.tex:133–137` and `discussion.tex:78–83`; "at most $2n$ face optimizations" now agrees with `cutoff.tex:99–100`. |
| m8 abstract stall sentence | Closed. Abstract has 248 words. |
| m9 dichotomy wording | Closed: `local-rates.tex:339–340`; `ex:many-term` retitled. |
| m10 start-box premise of `cor:local-gap` | Closed: `local-rates.tex:1223`. |
| m11 precursor comparison caveat | Closed: `precursor-study.tex:227–229`. |
| m12 precursor wording in discussion | Closed: `discussion.tex:99–102`. |
| m13 per-callback allocation | Closed: `effort.tex:38–40`, `experiments.tex:313–316` ("per recorded callback"). |
| m14 terminology | Closed: "sidecar" remains only in an invisible label. Keeping $B_0'$ is justified in `structure-revision.md`, because $B_0$ is the outer domain in those results. |
| m15 packaging | Closed: `submission-source.zip` exists, and its `main.tex`, `references.bib`, `main.bbl`, `introduction.tex`, and `related.tex` are byte-identical to the current files. |
| F1/A1 moving tangents | Closed: `foundations.tex:88–107` and `algorithms.tex:337–348, 529–533`. I rechecked the counterexample, including the policy's extra product-interval bounds $y\in[0,\max\{\ell^2,u^2\}]$, which leave it unchanged. |
| F2 greatest fixed box | Closed: `lem:greatest-fixed` (order only; $P_U=\emptyset$ convention), `prop:fixed-limit` ($B_\infty=P_U$ under closedness), `ex:not-fixed`, and the chain at `foundations.tex:435`. The new connection in `thm:closure`(b) (returned box = $P_U$ = Jacobi limit) is correct. |
| F3–F7 | Closed: vacuous clause removed; joint-lsc premise and independence of closedness and monotonicity (`foundations.tex:373–395`); cutoff condition on persistence (`foundations.tex:301–307`); wording; cofinal-subsequence proof (`foundations.tex:199–208`). |
| F8 attribution | Closed: neutral wording at `foundations.tex:211–214`; the audit confirms order independence in Caprara–Locatelli (pp. 4–9, 13–14). |
| A2 floating point | Closed: `numerical-validation.tex:83–162`. Extended pred/succ, faithful rounding, both overflow signs, no FTZ/DAZ. I re-derived that an overflow followed by an opposite-direction step keeps the enclosure, and that the third pass does not need monotone rounding. |
| A3–A7 | Closed: trigger rationale (`algorithms.tex:466–473`), row-correction sets, infeasible LP and sign convention, closure discussion with threshold $U_{\widehat W}$ and containing boxes, acting callbacks (`algorithms.tex:446–465`; `experiments.tex:275–278, 313–316`). |
| A8 attribution | Closed: `applegate2007` (`algorithms.tex:115`), `neumaier2004` (`numerical-validation.tex:43`), `gleixner2017` (`algorithms.tex:303`); all three are full-text dispositions in the audit. |

## 5. Scope and snapshots

I read all 19 TeX inputs, `references.bib`, and both bibliography files in
snapshot A. All dates are 2026-10-06. Three files changed during the review,
and I reread them in full (`related.tex` twice). I then read the final audit
completely.

| Snapshot (UTC) | Content |
| --- | --- |
| A, 02:31:49 | All inputs; full read |
| B, 02:44:01 | `introduction.tex`, `related.tex`, and `references.bib` changed (root M1 merge); diffs and full context reread |
| Final, 02:48:10 | `related.tex` changed again (Sundar "preprint" wording, Bompadre sentence split); reread |
| Audit, 02:50:23 | `literature-audit.md` revision `736e57cb…` read in full; no manuscript file changed since 02:48:10 |
| Frozen, 02:55:11 | Final audit `3a109aeb…` (two uncited gap identities corrected) and `review-integration-r3.md` read; no manuscript file changed |

Final SHA-256 values:

```
2f7bc1d789ea36cad2340620181224e1f790d4214b5c1ba423d485a539825168  main.tex
f75cb5164d64ebc45ae450352fab170a68e99c1199589cc9f369ca02ea4fea4d  abstract.tex
cc6c2691c7eaf877c0e2e8b4ed945d10f29cd070008cd3828a8e53a06e15dbaa  references.bib
564a50f6f73c647af6f568bd9912d6337993b71b31cce4acf3643fff9bd0d00b  sections/introduction.tex
2b07d38eb0bbd5b50cada072ca29cbc6f58708a8385be1d07e5c17eb4379a666  sections/related.tex
f30184c925375bf1f37300ce465057216656d36aadfdb9bed0c5476d009bb10d  sections/foundations.tex
de079f21574486bd3e0fa5f914d857279dc1a328b2c5bfda8f088a1337bfbd75  sections/local-rates.tex
a4373749b2d769e600d364c4ae67f173a5fafbc966e95ce89647f71cbcbbb9db  sections/certificates.tex
ca8717986aad87156b02328832adbe13765b973ac98b9acfb3f779a26318e318  sections/cutoff.tex
f26e7f76d4ce48e1bda03711a2f7c42d055f75e162968b00bf518b232524c3fe  sections/residual.tex
ae8ad2d7a960904d5b2822b5487ea8d74a706c57892be4cbe51165f166acb9d2  sections/constraints.tex
dfbf09c38202404ea77a30b3d8cd5068e842758bf3cf7aa9b02dc20924c4d327  sections/algorithms.tex
1a75a74507989ac98cddf6815993175d66540e10154dda24916a406117951e82  sections/effort.tex
facfe5d03aab6102d1fbbb994634d5f32e9b18fb36f78fb7781d9606ef48d391  sections/experiments.tex
57672aa74ee14a0533df7d75dfe80cc2079bc82b083c3330081f5e11aaefa5c3  sections/discussion.tex
5d764d0cb323afba53ef96b079424a3525c55b72bef871f1d114d840cf43294c  appendices/local-proofs.tex
dc58fdd51989e1b9b61010890d56c7ef52c606d1caaa4435ee4d24e3afd9bc85  appendices/numerical-validation.tex
a4b1c8b1121d170d8ef793884fad0ef1103dae17cbb5c5b2c0a08716d4d1e6b1  appendices/parametric-proofs.tex
03109bf8cf22c3012bd2f60925c36af35a9ecf73e676b4148fa176c42199bf36  appendices/scheduling.tex
a7dd809513f3eb9b2a23695a3327bd99c1a64de610eb5417ef679a18c0611c61  appendices/precursor-study.tex
d6268d88002ac02a14c87f63ae40999d67039d636553cc39842fd9d55f71a2ab  figures/rates.pdf
d6d39fcb62d985a481e20116a1c52a39cb1dbcbcea78f26b2c77be65221a3428  main.pdf
6c72defff87757048136b0e304b9ffa3116153c1f9aa157a3c708897682b6521  submission-source.zip
5ffcc29f326ad1b5a5d724b32acd7dbd276449accc4b2e77a541115ef51a0ac9  evidence/literature-references.bib
3a109aebf9c7c03959083abd6da9b0ba2438c283cbe8f213b0c24502807a9aa8  evidence/literature-audit.md
1613cd5e0d416f487501009678210fa194618a6d4030d6011b9d9d8b189577a4  evidence/review-integration-r3.md
```

**Reviewed in depth.**

- Every front-matter claim (abstract, introduction, related work,
  discussion) against the body statements it summarizes, and every source
  description against the audit's disposition for its key.
- Every changed mathematical passage:
  - foundations: five-tangent example, `lem:greatest-fixed`,
    `prop:fixed-limit`, closedness paragraph, sequential example;
  - the moved restricted tangent proposition and its link to
    `prop:equality-con`;
  - `ex:many-term` and the figure caption and render (page 23);
  - `cor:local-gap`;
  - `ex:mixing-hull` and `prop:continue`;
  - the history examples, with their arithmetic;
  - `thm:closure` with its new $P_U$ conclusion;
  - the policy's nonmonotonicity paragraph;
  - the full numerical-validation chain, step by step.
- The `tab:work` and `tab:campaign` arithmetic: 20.9%, 18.4%, 6.71 s and
  12.73 s, about 17 ms and 6 ms, PAR-2 means, and the 337 added callbacks.

**Not re-reviewed.**

- Proofs accepted in round 1 that did not change: the local-proofs appendix
  is byte-identical to the round-1 snapshot, and I checked other accepted
  proofs only where a new connection arose.
- Archived raw records: I relied on `review-evidence-r2.md` and
  `review-algorithms-r3.md`.
- The cited sources themselves, the KB, and the audit's run record: these
  belong to the literature lead, and Sol's integration review checks them
  separately.

## 6. Verification actually performed

All checks were targeted and read-only, apart from writing this file. None is
a project-wide or CI check.

1. Reads with `cat -n`, `awk`, `sed`, `grep`, and the Read tool: `AGENTS.md`,
   `evidence/BRIEF.md`, both round-1 Opus reports, `author-revision-r2.md`,
   `structure-revision.md`, `REVIEW-RESPONSES.md`, the five focused accepted
   reviews, `review-integration-r3.md`, `COVERAGE.md`, the preliminary and
   both final revisions of `literature-audit.md`, every manuscript input,
   `references.bib`, and the companion README.
2. `sha256sum` and private copies in `/tmp/opus-full-r2/snapA` and `snapB`,
   with `cmp` and `diff -u` between snapshots and the final files.
3. `python3 -I -B verification/check_sources.py`, run twice. Results:
   `SOURCE_CHECK=ok: 19 TeX files, 244 labels, 31 citations` (snapshot A) and
   `… 37 citations` (after the merge).
4. `main.log` of the root's current build: 96 pages, no warning, undefined
   reference, or overfull box. I did not rebuild.
5. `python3 -I` scripts that only read files:
   - comparing cited keys (`main.aux`) with `references.bib` and the vetted
     bibliography, field by field;
   - counting abstract words (248, inline math counted as one word);
   - comparing member hashes of `submission-source.zip` with the current
     files.
6. `grep` of the manuscript for novelty and contrast phrases and for the
   probing-node labels.
7. `grep` of `PROP_FREQ`, `PROP_TIMING`, and `DEFAULT_ITLIMITFACTOR` in the
   retained SCIP 10.0.2 sources `prop_obbt.c`, `prop_nlobbt.c`, and
   `prop_genvbounds.c`. No solver was executed.
8. `pdftoppm -f 23 -l 23` of the built `main.pdf` to view the analytic
   figure in place.
9. All mathematical checks were done by hand.

These are document, source-traceability, and analytic checks. They are
distinct from any CI result.
