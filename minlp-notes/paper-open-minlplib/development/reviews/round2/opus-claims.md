# Round 2 review: claims, qualifiers and trust base (lens: opus-claims)

Date: 2026-10-04. Lens:
- whether each item of `round1/opus-claims.md` is resolved;
- overclaiming and qualifier drift in the main paper and the supplement;
- novelty statements, including the new literature (Araya et al. 2025, Borst–Eifler–Gleixner 2024, Szeider 2026, Hoen–Gleixner 2025, Belotti et al. 2025, Sudermann-Merx 2026);
- the status words (proved / verified by a separately written implementation / computed / floating-point output / interpretation);
- the definition of "separately written" and its use;
- the solver and published-claim categories;
- the KAN and `eg` trust bases after the guard and audit results;
- the outline section 8 list.

Paths are relative to `paper-open-minlplib/` unless they start with `R/` (`research-20260929/`) or `D/` (`development/`). Line numbers refer to the sources as of this review.

## Verdict

**Minor revision (0 blockers, 1 major, 13 minor).**

All 23 round-1 items are resolved or adequately addressed:
- 21 are fully resolved;
- item 22 is resolved in substance;
- item 23 is resolved in the paper but not in one development record (issue 14 below).

The three heaviest round-1 points are now in good shape:
- the AI-agent disclosure;
- the rocket and GAMS/OSIL reruns;
- the claim register with explicit status labels. The validator passes from a `/tmp` copy.

The status words, the category A/B wording, the KAN and `eg` trust statements and the outline section 8 list are used consistently, with the exceptions below.

The remaining major issue is the scope of the AI-use disclosure. Both the declaration and §2.6 say that agents *implemented and checked* the computations. The records indicate that agents also devised the certificates and wrote the proofs. The other issues are local qualifier drift:
- two headline observations;
- Remark 2.3(1);
- the stored data of the `eg` certificates;
- the guarded KAN replay;
- abstract wording;
- the meaning of "separately written" in two places.

## Checks run (targeted, local)

- **Main paper.** Read all sections, Appendix A and the generated tables `tab-trust`, `tab-claims`, `tab-kan`, `tab-points-all`.
- **Supplement.** Read the certificate boxes and verification passages of B1–B9, C, D (S3.1–S3.2), E (second checkers, spring, rocket, GAMS/OSIL), F (Theorem S5 trust statement), H (SCIP witnesses, CAMINO) and I (setup, claim register, regeneration).
- **Development records.** Read `round1/adjudication.md` and the `open` fields of `D/revise3-result.json`. Read `D/build-r3.md`, `D/open-items.md`, outline §8, `kan-guard/report.md`, `D/reviews/sol-eg-audit.md`, `round1/sol-math-supp2.md` and the `round1/eg-dyadic/` logs.
- **Dossiers and research records.** Read the dossier passages `small.md:787,1015-1030`, `powerflow.md:18-28,868-878`, `eg.md:425-450`, `solvers.md:520-533` and `chain-catmix.md:626`. Read `R/publication/scip-bug/report.md:125-151` and `R/README.md`.
- **Knowledge base.** Read the KB entries `literature/papers/{araya2025,borst2024,szeider2026,hoen2025,belotti2025,merx2026}-*/paper.md`. Searched the Hoen–Gleixner full text for the §6 repair claim, which is confirmed.
- **Pre-revision diff.** Extracted `/workspace/local-home/paper-backups/paper-open-minlplib-r1-20261004-1841.tar` to `/tmp/opus-claims-r2/old/`. Diffed the novelty sentences and compared the deleted main-text certificate boxes with the new certificate sentences.
- **Claim register.** Copied `artifact/check_claims.py` to `/tmp/opus-claims-r2/` and ran it on two cores with `--repo-root <repo>`. Result: `PASS: 65 claims; 5334 SHA-256 references; 1894 distinct files; all paths and LaTeX labels valid`. Also listed `verification_label` and `status` for all 65 entries of `artifact/claims.json` (read-only).
- **Numbers.** Inspected `data/numbers.json` `headline` (22/18/16 with rocket; 79 same-model duals; 2 runs within 1e-6).
- No repository script was run in place, no paper file was edited and nothing was committed. No CI result was consulted.

---

## Status of the round-1 items

| # | round-1 item | status | where |
|---|---|---|---|
| 1 | AI-agent provenance not disclosed (blocker) | Resolved in substance. §2.6 discloses agent provenance, the limits of "separately written" and the common-mode risk. The declarations contain an AI-use statement (placeholder wording). "By hand", "second party" and "separate review" are replaced; "none is peer review" is removed. The disclosure covers only part of the AI work (new issue 1). | `02-semantics.tex:177-207`; `11-conclusion.tex:76-79`; `B0-families.tex:11`; `I-reproduction.tex:19` |
| 2 | Rocket and GAMS/OSIL claims before the rerun | Resolved (R-14). The reruns are done and recorded, and the main text says "rerun from a clean copy by a separate agent session". | `07-audit.tex:59-60,100`; `E-audit.tex:477,549` |
| 3 | `catmix` level "stored" | Resolved: `rerun` in Table 1, the certificate sentence, the register and the S1.4 box; "14 closures at level rerun". | `tab-trust.tex:23`; `04-split.tex:272`; `I-reproduction.tex:146`; `03-results.tex:51` |
| 4 | Claim register labels mechanical and invalid | Resolved. There is an explicit status column, `build_claims.py` maps it, and the validator passes. | `artifact/claims.json` (`verification_note`); `I-reproduction.tex:48-51` |
| 5 | SCIP trigger unscoped | Resolved. | `04-split.tex:322`; `01-introduction.tex:64` |
| 6 | Lesson 3 attributes amplification to equality chains | Resolved (scoped to `camshape`, proved bound plus numerical evidence). | `01-introduction.tex:63` |
| 7 | "Re-proofs by separately written code" for every point | Resolved (sentence replaced; exceptions stated). | `01-introduction.tex:77`; `02-semantics.tex:191`; `06-points.tex:76-78` |
| 8 | `catmix` per-stage agreement scope | Resolved. | `04-split.tex:271`; `B4-chain-catmix.tex:430` |
| 9 | Library-function assumption; `fsum` | Resolved. | `02-semantics.tex:152`; `07-audit.tex:71`; `B8-waterno2.tex:287`; `tab-trust.tex:31` |
| 10 | Shared components incomplete | Resolved. `powerflow` is understated (new issue 13). | `02-semantics.tex:187-188`; `B8-waterno2.tex:283-286` |
| 11 | KAN path (II) NaN assumption | Resolved. | `05-other.tex:329`; `tab-trust.tex:33` |
| 12 | "Tolerance artifact" as a cause | Resolved (caption and qualifiers). | `tab-claims.tex:8`, rows `lukvle10`, Kosolap |
| 13 | Prior-status classes of copies | Resolved in §1, §3.4 and S3. The abstract keeps the short form (new issue 9). | `03-results.tex:70-79`; `D-literature.tex:118-129`; `01-introduction.tex:76` |
| 14 | KAN "no optimal value" | Resolved. | `03-results.tex:64-65` |
| 15 | `camshape` "to all digits" | Resolved. | `05-other.tex:67`; `tab-trust.tex:20` |
| 16 | `hvycrash` witness count | Resolved everywhere. | `05-other.tex:248`; `06-points.tex:78`; `B5-small.tex:53` |
| 17 | "Multipliers control" overgeneral | Resolved. | `02-semantics.tex:101` |
| 18 | Claim register mapping; "archived" | Resolved; "archived" kept with the DOI placeholder (R-17). | `01-introduction.tex:104`; `10-reproducibility.tex:89` |
| 19 | SCIP version for the feasibility check | Resolved. | `01-introduction.tex:93`; `08-solvers.tex:68` |
| 20 | MINOTAUR "false" | Resolved ("invalid as recorded (cause unknown)"). | `01-introduction.tex:96-97`; `08-solvers.tex:125` |
| 21 | Novelty of the `lnts` control; R_P | Resolved. | `B1-lnts-lukvle10.tex:125`; `D-literature.tex:61` |
| 22 | Limitations: which proofs had a second reading | Resolved in substance. §11.2 names the Appendix B proofs and the `eg` primal check as rechecked by agent sessions, with no human outside the authors. | `11-conclusion.tex:49-51` |
| 23 | open-items vs audit-priority sentence | Paper side resolved: S3.1 lists the sources read. `D/open-items.md` still contradicts itself (new issue 14). | `D-literature.tex:32-43`; `D/open-items.md:58-76` |

---

## New issues

### Major

#### 1. The AI-use disclosure describes only part of the AI work: the records show that agents also devised the certificates and wrote the proofs (major)

- **Where.**
  - `sections/11-conclusion.tex:77`: "AI coding and writing assistants … were used, under the authors' direction, to implement and re-implement the certificate computations, to check them, to search the literature and to draft the manuscript."
  - `sections/02-semantics.tex:177`: "The certificates, their checking programs, the separately written re-implementations and the reviews of code and proofs … were produced with AI coding agents".
- **Problem.**
  - The declaration says that AI implemented and checked computations and drafted text. It does not say that AI devised the certificates and wrote the proofs, which are the paper's mathematical contribution. Examples are the `camshape` comparison argument, the `lnts` characterization, the `chain` calibration, the `catmix` minorants, the Appendix B proofs, the audit lemmas and the SCIP analysis.
  - §2.6 lists the reviews of proofs, but not the proofs themselves.
  - A reader of either passage will assume that the theorems and proofs are human work and that AI only coded and checked them. This is the same kind of overstatement of human involvement that round-1 item 1 addressed.
- **Evidence.**
  - `D/dossiers/primal-points.md:471`: "The authors and reviewers are AI agents". In the dossier language, "the authors" are the sessions that wrote the first implementations and proofs.
  - `R/README.md:5-6`: theory notes reviewed by "an independent research agent".
  - `D/dossiers/chain-catmix.md:673`: the dossier session gives the proofs "in my" Section 3.
  - `R/publication/scip-bug/report.md:1`: the SCIP report is the output of an "author of track scip-bug in workflow …".
  - The round-1 adjudication (G1-01) records that all implementations and reviews are agent work. Nothing in `D/` records a human author deriving a certificate or proof.
- **Fix.** This completes the existing `[authors to confirm]` placeholder; it does not replace it.
  - `02-semantics.tex:177`: "The certificates and the arguments that prove them, their checking programs, the separately written re-implementations, the audit and solver analyses, and the reviews of code and proofs that the supplement reports were produced with AI agents (Anthropic Claude and OpenAI GPT models) directed by the authors; the project records do not identify the model of every session."
  - `11-conclusion.tex:77`: "AI agents (Anthropic Claude and OpenAI GPT models) were used, under the authors' direction, to devise the certificates and write their proofs, to implement, re-implement and check the certificate computations, to carry out the audit and the solver experiments, to search the literature and to draft the manuscript. The authors take full responsibility for the content."
  - If some constructions or proofs are the authors' own, name them there. The TODO at `:79` already asks the authors to say which proofs or codes they read.

### Minor

#### 2. The definition of "separately written" admits the `ann_cumene_tanh` second code, which the paper then treats as an exception (minor)

- **Where.**
  - Definition: `02-semantics.tex:184` ("it neither imports nor runs the first implementation in its checking computation").
  - The `ann` exception: `:186`, `:189`; `tab-trust.tex:32` ("second written after reading the first"); `I-reproduction.tex:206` (status "proved"); `05-other.tex:296`; `B9-ann-kan.tex:150,165`.
- **Problem.**
  - By the stated criterion, the `ann` second code is separately written: it does not import or run the first code.
  - Yet §2.6 and Table 1 treat it as an exception to "two separately written implementations", and the register gives it status "proved", not "verified".
  - The real criterion the paper applies is whether the second session read the first certifying code before writing its own. The definition does not state that criterion.
  - The labelling is conservative, so this is no overclaim. But the definition and its use disagree, and a reader cannot apply the definition to the other families.
- **Evidence.** §2.6:186 itself names the other cases: reading "to learn file formats or to compare parameters after its own results existed" is allowed, and reading the first code "in full" before writing is not.
- **Fix.** `02-semantics.tex:184`: "We call it *separately written* if it neither imports nor runs the first implementation in its checking computation and its session did not read the first implementation's certifying code before its own results existed, apart from reading file formats (some second sessions ran or imported first code for side comparisons, which the records name and no certificate uses)." Leave `:186` and Table 1 as they are; they then agree with the definition.

#### 3. The SCIP witnesses are said to be checked by "six to eight separately written checkers", but some of these were written in the same session (minor)

- **Where.** `08-solvers.tex:72`; `H-solvers.tex:215,222`.
- **Problem.**
  - In §2.6, "separately written" means written in a separate agent session.
  - The count of six to eight is a count of code bases. At least two pairs among them come from one session each.
- **Evidence.**
  - `R/publication/scip-bug/report.md:131-136`: `exact_check.py` and `spec_check.py` are both by the "first" author session.
  - `D/dossiers/solvers.md:526-533` lists eight code bases: the track's four, the reviewer's `rv_cip_exact.py` and `rv_gms_exact.py` (one session), the draft's `mycheck.py` and the dossier's `cipchk.py`. That is about six sessions for eight codes.
- **Fix.**
  - `08-solvers.tex:72`: "…confirmed for each witness by six to eight exact checkers from at least [k] separate agent sessions, two of which read the GAMS files…". Take [k] per witness from the logs: the minimum number of distinct sessions among the checkers that covered that witness.
  - Make the same change at `H-solvers.tex:215,222`.
  - Check the other places that count "separately written" codes in the same way, for example "three separately written programs" (`03-results.tex:44`, `D-literature.tex:290`) and "three separately written codes" (`H-solvers.tex:133`).

#### 4. Observation 1, "little search remained", conflicts with the paper's own counts for the `eg` and `ex6_2_5` certificates (minor)

- **Where.** `01-introduction.tex:58`; `11-conclusion.tex:65`.
- **Problem.**
  - The evidence is low-dimensional branching, not little search. The `eg_disc2_s` certificate has 1,114,361 leaves.
  - The `ex6_2_5` liquid-phase bound needed 131,111 boxes. §9 states both (`09-interpretation.tex:29-30`).
  - This is a headline observation, and §11 repeats it.
- **Fix.**
  - `01-introduction.tex:58`: "Once a bound fitted to the structure of the model was in place, the remaining branching was low-dimensional: it was absent in 12 closures and at most three-dimensional in 15 more, though the `ex6_2_5` bound needed 131,111 two-dimensional boxes; the `pindyck` certificate splits one box into 9, and the three `eg` certificates branch on their 7 original variables, with up to 1,114,361 leaves."
  - `11-conclusion.tex:65`: "First, once a bound fitted to the structure of the model was in place, the remaining branching was low-dimensional for 27 of the 31 closures; why general-purpose solvers did not find such bounds we have only interpreted (…)."

#### 5. Observation 3 and §11 say that exact feasibility "changes the verdict" on listed bounds, but the refutations hold under every tolerance (minor)

- **Where.** `01-introduction.tex:61-62`; `11-conclusion.tex:67`.
- **Problem.**
  - The 22 refuted bounds are invalid under every feasibility tolerance (`07-audit.tex:59`).
  - Exact feasibility did not change their verdict. It *decided* conflicts that tolerance-feasible points leave open.
  - The verdict changed only for listed points and solver values, which are category A.
- **Fix.**
  - `01-introduction.tex:61-62`: "Exact feasibility decides questions that tolerance-feasible data leave open. Some listed dual bounds are invalid under every feasibility tolerance, which an exactly feasible point proves."
  - `11-conclusion.tex:67`: "Third, proving exact feasibility settled conflicts among listed bounds and changed the verdict on listed points and solver claims often enough that…".

#### 6. Remark 2.3(1) asserts that readings (a) and (b) agree for every instance except `catmix`, but this was proved for only 17 of them (minor)

- **Where.** `02-semantics.tex:51`; the reliance on it at `08-solvers.tex:146`.
- **Problem.**
  - The main clause asserts that the GAMS and OSIL forms define the same model for 39 instances.
  - Table A9 (`A-semantics.tex:64-67`) compares 17 of them exactly (21 including `catmix`, whose rows differ). The other 22, among them `lnts`, `chain`, `lukvle10`, `ann`, KAN, `ex6_2_*`, `pricing050`, `etamac`, `pindyck` and `hvycrash`, were only compared at sample points.
  - The tail clause ("numerical evidence for the others") does not undo the main assertion.
  - §8:146 compares GAMS-run solver values with OSIL certificates, naming only `catmix` as different. `H-solvers.tex:42` states this correctly ("exactly or at sample points").
- **Fix.**
  - `02-semantics.tex:51`: "Readings (a) and (b) define the same model for the 17 instances whose forms we compared exactly, and differ for the four `catmix` instances, whose OSIL files print binary64 products such as `0.045000000000000005` in place of 9/200; for the other 22, a comparison at sample points found no difference (numerical evidence; `\cref{app:semantics-gams}`)."
  - `08-solvers.tex:146`: "The solvers ran the GAMS files and the certificates concern the OSIL files; the two forms are identical or agree at sample points (`\cref{tab:sem-gams}`), and for `catmix`, …".

#### 7. §3.2 says that no search tree is stored for the 14 `rerun` closures, but the `eg` leaf partition and recorded trees are stored (minor)

- **Where.** `03-results.tex:51` ("no search tree or stage data are stored").
- **Evidence.**
  - `02-semantics.tex:165` and `B7-eg.tex:275`: "the leaf partition is stored and its coverage is checked exactly; only the per-leaf certificates are recomputed".
  - `B7-eg.tex:270`: "bookkeeping on the recorded trees".
  - `I-reproduction.tex:201`: "(leaf partition stored)".
- **Fix.** `03-results.tex:51`: "For the 14 closures at evidence level `\evid{rerun}` (`\cref{tab:trust}`), the per-leaf or per-stage certificate data are not stored, so a check reruns the search or the stage computation; for the three `eg` instances the leaf partition is stored and its coverage is checked exactly."

#### 8. The KAN text does not say why the path (I) replay was guarded, and the register still lists the unguarded code as the second checker (minor)

- **Where.** `05-other.tex:330`; `B9-ann-kan.tex:336-340`; `I-reproduction.tex:213`.
- **Problem.**
  - A review found that the original quadratic routine assumed exact halving of a binary64 curvature. A concrete subnormal input makes it return a value above the true minimum.
  - The paper says only that the guards "close the arithmetic-domain gap". A reader cannot tell that the archived second code is unsound in a corner case, or that the theorem now rests on the guarded replay.
  - The register's "2nd" entry still names the original `D/dossiers/ann-kan-checks/kan_bnb_rigexp.py`. The guarded copy appears only as a further replay.
- **Evidence.**
  - `round1/sol-math-supp2.md` item 1: for `t = 2^-1074`, `m = -t`, `g = 0` and `s` in [-3, 3], the routine returns `-3t` instead of at most `-9t/2`.
  - `round1/kan-guard/report.md`: guarded source `e5783a24`; zero guard triggers; bit-identical bounds.
- **Fix.**
  - `05-other.tex:330`: "A review found that the original path (I) bound routine assumes exact halving of a binary64 curvature, which fails for some subnormal inputs; a replay with a guarded routine, proved valid for all finite inputs, reproduced all six searches and their bounds bit for bit, with no guard triggered (`\cref{app:annkan-kan-enclosure}`)."
  - `B9-ann-kan.tex:336`: replace "close the arithmetic-domain gap in the quadratic routine" by "close a gap in the original routine, which assumed that halving a binary64 curvature is exact and can return a value above the true minimum for a subnormal curvature".
  - `I-reproduction.tex:213`: name the guarded copy as the 2nd checker and list the unguarded original as historical.

#### 9. The abstract and the §8 opening drop qualifiers (minor)

- **Where.** `00-abstract.tex:7,9,13`; `08-solvers.tex:25`.
- **Problem.**
  - `:9`: "Our six Kolmogorov–Arnold network instances" reads as if the instances were the authors'. They are MINLPLib's; elsewhere the paper says "the six KAN instances in our set".
  - `:13`: "No dual bound from one-hour … runs reached ours" counts 18 KAN values that are compared only descriptively with a bound for a different model (`R_net`). It also counts six BARON values that carry no globality guarantee. §8.3 (`08-solvers.tex:140-141`) separates these cases; §8:25 has the same unqualified sentence as the abstract.
  - `:7`: "for seven, floating-point closures or near-closures had been reported" omits that the `dtoc5` result is for a copy under assumed variable bounds (`03-results.tex:70,74`).
- **Fix.**
  - `00-abstract.tex:9`: "The six Kolmogorov–Arnold network instances in our set have no exactly feasible point; …".
  - `:13`: "In one-hour BARON, Gurobi and SCIP runs, no final dual bound reached our certified bound for the same model; BARON reached tolerance-level closures on two."
  - `:7`: "…and for seven, floating-point closures or near-closures (one of a bounded copy) had been reported."
  - `08-solvers.tex:25`: "In one-hour runs, every finite final dual bound was weaker than our certified bound for the same model (for the KAN instances we compare only descriptively with the bound for `\Rnet`), and …".

#### 10. The introduction's summary of the second implementations omits "part of the domain" (minor)

- **Where.** `01-introduction.tex:54` ("for some families only for a slightly weaker bound").
- **Problem.** For `eg_disc2_s` the second certificate covers only part of the domain (`02-semantics.tex:190`). The abstract (`:10`) and §11 (`:49`) say so; §1 does not.
- **Fix.** "…for some families only for a slightly weaker bound or, for `eg_disc2_s`, only on part of the domain (…)."

#### 11. Two sentences on the new literature are imprecise (minor)

- **Where.** `01-introduction.tex:123`, `:125`.
- **Problem.**
  - `:123`, "its bounds would need the same exact existence proofs for points": an IbexOpt lower bound needs no existence proof. Araya et al. state that their lower bounds remain valid with exact equalities (KB `araya2025…/paper.md`). Only its points would need existence proofs. As written, the sentence suggests that a rigorous interval solver could not have supplied comparable dual bounds; the paper did not test this.
  - `:125`, "these certify linear MIP results": Hoen and Gleixner check floating-point branch-and-bound decisions a posteriori; they issue no certificates.
- **Evidence.** KB summaries of Araya et al. 2025 (p. 3), Hoen and Gleixner 2025 (pp. 5-7, 13-14) and Szeider 2026. The Belotti et al. and Sudermann-Merx characterizations at `:126` match their KB entries.
- **Fix.**
  - `:123`: "We did not run such a solver; its lower bounds would be rigorous for the stored models, whether they reach ours we do not know, and its points would still need exact existence proofs such as ours."
  - `:125`: "these certify or check linear MIP results, whereas …".

#### 12. Status words are used beyond §2.6's list of three, and one register row is inconsistent (minor)

- **Where.** `02-semantics.tex:194`; `tab-trust.tex:10`; `I-reproduction.tex:211,246`; `artifact/README.md:49`; `artifact/claims.json` (`verification_label` "floating-point output").
- **Problem.**
  - The register and the claim index use the status "floating-point output", which §2.6 does not define; §2.6 says "We use three words".
  - Table 1 uses "proved" (`hvycrash`) and a free-text status for `ann`; its caption defines neither.
  - The register row for `prop:kan-infeasible` (`I-reproduction.tex:207-211`) has two problems:
    - it gives level `stored`, while the certificate box says `\evid{hand}` and `\evid{stored}` (`B9-ann-kan.tex:359`);
    - it lists one checker under status "verified", although the second, separately written propagation over Q (`B9-ann-kan.tex:252`) exists.
- **Fix.**
  - After `02-semantics.tex:197` add: "Solver output and published values are *floating-point output*; we compare them with our results but never use them as premises."
  - In the Table 1 caption add: "*proved*: proof by hand (`hvycrash`); `ann_cumene_tanh`: two codes, the second written after its session read the first (`\cref{sec:semantics-protocol}`)."
  - In `I-reproduction.tex:211` write `\evid{hand}+\evid{stored}` and add "2nd:" with the path of the propagation check.

#### 13. §2.6 omits `powerflow` from the list of shared readers reproduced by a separate reader (minor; understatement)

- **Where.** `02-semantics.tex:188`.
- **Evidence.** `B6-powerflow.tex:303`: "a separately written reader and row builder reproduced every row of Q … exactly for all three files". Also `D/dossiers/powerflow.md:23-24,873-876`.
- **Fix.** "Separately written readers reproduced its output exactly for `powerflow`, `waterno2`, `ann_cumene_tanh` and the KAN instances, …".

#### 14. Development record and artifact README: two stale statements (minor; not printed)

- **Where.**
  - `D/open-items.md:58-76`. The first bullet records that the audit-priority sentence exists and that S3.1 lists its sources. The next bullet keeps "the audit-novelty search" among the open O-8 readings and says "The paper makes no such sentence".
  - `artifact/README.md:23`: "the independently regenerated `eg_int_s` audit" uses "independent" without the §2.6 definition (outline §8.10).
- **Fix.**
  - In `D/open-items.md`, remove "the audit-novelty search" from the O-8 list and record it as done (S3.1, `D-literature.tex:32-43`).
  - `artifact/README.md:23`: "…including the regenerated `eg_int_s` audit (a separate run from a clean copy)".

---

## Checked and found consistent (no action)

- **Novelty.**
  - Every "to our knowledge" is limited to the search of S3 and dated (`01-introduction.tex:76,89,95`; `08-solvers.tex:108`; `B1-lnts-lukvle10.tex:125`; `B7-eg.tex:74`). `D-literature.tex:49` limits every novelty statement to the search.
  - No mechanism is claimed as new (`01-introduction.tex:128-129`; `B3-camshape.tex:294`; `B8-waterno2.tex:143`; `B9-ann-kan.tex:116`).
  - No "first" is claimed about `R_P`.
  - The new references are characterized as their KB entries describe them, apart from issue 11. They do not affect the priority statements: all concern linear MIP, a geometric case study, solver architecture or interval-solver relaxations, and none audits MINLPLib bounds or certifies these instances.
- **Status words.**
  - Table 1, the register and `claims.json` agree row by row (verified / weaker second / partial second / proved).
  - "Computed" is used as a status twice, both labelled and not used as premises (`A-semantics.tex:104`; `E-audit.tex:560`).
  - "Proved by one implementation" for the GAMS/OSIL comparison (`07-audit.tex:60`) is consistent with R-07.
  - §9 is labelled as interpretation throughout.
- **Categories.**
  - Category B wording is fixed ("invalid as listed", "invalid as recorded; the cause is unknown").
  - "Wrong optimal value" and "defect" are used for SCIP only.
  - The BARON, QPLIB-copy, KAN-SCIP, `emfl` and `hvycrash` values are category A.
  - The `tab-claims` caption separates the category name from the cause.
- **KAN trust base.**
  - §5.5:329, Table 1, the B9 box and the register all state the following: shared reader, exponential and interval core; path (II) assumes no NaN; path (I) replayed with guards.
  - These statements match `kan-guard/report.md`: zero guard triggers, bit-identical `L_ver`, every value above the reported `L`.
  - The displayed `L` is the weaker bound, from path (II). Issue 8 concerns only how the guard is explained.
- **`eg` trust base.**
  - Theorem 5.14 (`05-other.tex:270`) and Theorem S5 (`F-eg-rounding.tex:398-416`) state the premises of `sol-eg-audit.md`: H0, correct code, faithful execution and retention.
  - The audited bounds are 6.4531031529331155, 5.760539610694993 and 5.642100574331458; the paper uses …993, not …994.
  - The audit's four minor issues are corrected, the eg-dyadic logs exist, and byte identity is claimed for `eg_disc2_s` only.
- **Outline §8.** Items 1–10 are respected.
  - KAN: no "the review reran r5"; the guarded replay is described as a replay.
  - `waterno2`: two codes, not three; p4 is not claimed as ours.
  - `topopt`: three points, none called independent.
  - Audit refresh: 69 files, not 1,632.
  - The only §8.11 display that appears is 352.238025369202, as the weaker second bound, which is allowed.
- **Counts.** 22/18/16 with rocket; 4 + 7 + 11 margin classes; 79 = 23 + 30 + 26 with 6 + 6 + 18; 7 + 9 + 15 prior statuses; 12 + 15 + 1 + 3 branching census; 14 `rerun` closures.
- **Primal claims.** "Every primal claim has two implementations except `etamac` and `pricing050`" holds against `tab-points-all`, C (`waterno2`: three checkers, one of them separately written; `eg`: dyadic plus two mpmath readers) and the `hvycrash` and `pindyck` rows.
