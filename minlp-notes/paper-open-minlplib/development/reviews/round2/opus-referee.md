# Round-2 referee report (lens: senior MPC referee)

Manuscript: "Rigorous certificates for open MINLPLib instances and an audit of listed dual bounds". Revised main paper `build/main.pdf` (60 pp., built 2026-10-04 22:59, after the last source edit at 22:58) and supplement `build/supplement.pdf` (135 pp.). Pre-revision sources: `/workspace/local-home/paper-backups/paper-open-minlplib-r1-20261004-1841.tar`, extracted to `/tmp/r2-opusref/old/`. Page numbers below refer to the revised `main.pdf`; line numbers refer to the current sources.

**Recommendation: minor revision (text only).** The revision fixes both round-1 blockers that were not placeholders: Table 2 now prints in full. It also resolves four of the seven major items (M2, M3 in substance, M4, M6) and most minor items. I found no mathematical error in the main text. Two issues remain major, and both are editorial; neither needs new computation:

1. The AI-use disclosure is accurate about the code. It understates the agents' role in constructing the mathematics, and the declaration and Section 2.6 describe that role differently (issue 1).
2. The body is still about 5 pages over the 38-page target that the authors set themselves (issue 2).

Counts (placeholders excluded): 0 blockers, 2 major, 13 minor.

---

## 1. Status of the round-1 items

| item | status | evidence in the revision |
|---|---|---|
| B1 Table 2 clipped | **resolved** | p. 13: the caption starts with "Table 2: The 31 closures", and the rows run to `eg_disc2_s`. Checked in a rendering at 80 dpi and with `pdftotext`. A float check exists (`development/check_floats.py`; build-r3 §2.3: "31 of 31"). |
| B2 placeholders | placeholder (not counted) | p. 44: `[TODO: licence]`, AI wording, competing interests and funding; `[archive DOI]` ×4; `main.tex:15` `\author{}` (R-12). |
| M1 length | **partly** | Body (Sections 1–11): 45.8 → 42.85 pp. (build-r3 §5). PDF: 62 → 60 pp. Body words: about 31.8k → 29.1k (−8%), but the appendices grew from about 4.7k to 5.6k words (new A.4 proofs). Done: certificate boxes moved out of §§4–5, §9 halved, the structure table dropped, the funnel moved to S3.4, C1–C9 merged into C1–C4. Not done: Table 1 is still a full sideways page (p. 11); C1–C4 still run to about 1,100 words (pp. 3–4); §§7–8 take 7.1 pp. against the 4 pp. I asked for; Appendices A and B stay in the main paper (R-05). See issue 2. |
| M2 framing of abstract, C5, C7 | **resolved** | Abstract (p. 1): (a) "No dual bound from one-hour BARON, Gurobi and SCIP runs reached ours; BARON reached tolerance-level closures on two" replaces "closed no instance"; (b) size breakdown "four ... exceed 1%, eleven are below 10⁻⁶"; (c) `ann_cumene_tanh` qualified by its exp variant; (d) "for seven, floating-point closures or near-closures had been reported". C3 (p. 4) uses the C7 text. §1.4 (p. 5) now discusses IbexOpt. Remaining: the reason given for not running an interval solver (issue 6) and two ambiguities in the abstract (issue 7). |
| M3 who wrote the code | **resolved in substance** | §2.6 (p. 10, continued on p. 12) now defines "separately written" accurately. It says that the sessions shared a file system, names the cases in which a second session read the first code (`ann` in full), names the three shared components and states the common-mode risk. The declarations (p. 44) include "Use of AI tools". Remaining: the role of the agents in the mathematics, and what a person checked (issue 1). |
| M4 §9 and Lesson 1 | **resolved** | §9 is titled "What the certificates exploit: an interpretation" and says the interpretation was not tested by experiment and that no certificate depends on the section (p. 39). The structure table is gone. §11.1 labels the stage-structure item "As an untested proposal" (p. 43). §1.2 observation 1 (p. 3) is the requested replacement. Option (a), the experiment, was not run (R-02); I accept this given the new framing. Remaining: issues 3 and 9. |
| M5 artifact | **partly** | The claim index was rebuilt and passes validation (build-r3 §2.4: 65 claims, 5,334 hashes). The limits are now stated in §10 (p. 42: versions "not recorded consistently") and §11.2 (p. 43: one machine, no stored trees). Not done (R-03): curated layout, stored leaf partitions, replay on a second machine. The DOI is a placeholder. The residual is minor (issue 15). |
| M6 audit thresholds | **resolved** | §7.1 (p. 33): class (i) is "margin at least u(s)", and class (ii) is split into (ii) and (ii′). §7.2 (p. 33) and C2 (p. 4) carry the replacement sentence, which notes that only `rocket100` needs Hypothesis H. |
| M7 taxonomies | **partly** | The T-* labels moved to S7 (p. 9: "Section S7 gives labels"). The instance-list dual is defined once (§2.1, p. 7). The glossary (R-04) and "fp near-closure" (R-16) were declined. New since round 1: replay tiers are used in §§4–5 before §10 defines them (issue 8), and Table 1's status column uses labels that its caption does not define (issue 12). |
| m1 catmix not a split | resolved | p. 3, observation 2; §4 opening (p. 16); §11.3 (p. 44). |
| m2 closure used before defined | resolved | §1.2 (p. 2) defines it inline. |
| m3 opening repeats abstract | declined (R-10) | I accept the decision. |
| m4, m5, m6 | resolved | p. 1 "a standard benchmark library"; p. 2 "These records, and solver claims of the same kind, nevertheless serve as reference values"; p. 5, one paragraph on classical mechanisms. |
| m7 inverted sentence | **not resolved** | p. 3: "Why general-purpose solvers did not find such bounds we do not test"; p. 44: "why general-purpose solvers did not find such bounds we have only interpreted". See issue 3. |
| m8 library functions | resolved | §2.5 (p. 9), including the 90-digit mpmath exponential of the second audit checker. |
| m9 rerun level for eg | **resolved in §2.5, contradicted elsewhere** | p. 10 states that the eg leaf partition is stored, but p. 14 (§3.2) and p. 43 (§11.2) say that no rerun certificate stores its tree. See issue 4. |
| m10 unused results | resolved by the alternative | p. 17: "no certificate uses part (c)"; p. 18: "No certificate uses the last statement of Proposition 4.5". |
| m11 certificate boxes | resolved | No certificate boxes in §§4–5. Box 2 (SCIP) remains, which is appropriate. |
| m12 Table 3 term | resolved | p. 14, footnote a: "one slope per separator on a 113–162-cell partition". |
| m13 Figure 1 | mostly resolved | p. 12: KAN rows have their own panel (b), with an axis break at 10⁻²⁰. The hollow triangle is kept (R-08), which is reasonable. |
| m14 structure table | resolved | Removed. |
| m15 "a referee should expect" | resolved | p. 42: "the order of magnitude to expect". |
| m16 report upstream | not done (author action, R-11) | p. 38 is still dated "searched on 2026-10-02". See issue 14. |
| m17 merge C2 into C1 | resolved | p. 3, C1. |
| m18 selection funnel | resolved | p. 14, §3.1. One leftover sentence is unclear (issue 10). |

## 2. The revised paper read afresh

**Pages 1–2: is the contribution clear?** Yes, with small blemishes:

- The abstract is dense (about 247 words and 13 numerical facts), but every claim in it is now qualified correctly.
- The opening paragraph and Box 1 (camshape800: a valid but weak listed dual bound, and a listed point below the optimum) make the problem concrete by the end of p. 2. §1.2 states the exact semantics and defines "closure" before C1 uses it.
- The reader learns on p. 3 what the certificates exploit (observation 2) and that they are built per instance with no general solver (C1 preamble). That is early enough.
- Two ambiguities in the abstract remain (issue 7).

**Can an expert follow without the supplement?** Mostly yes:

- These parts are self-contained, with statements and complete or near-complete proofs in the main text:
  - §2 (semantics, Lemma 2.5, Proposition 2.6);
  - §4.1 with Appendix B;
  - lnts (Theorem 4.7 with Appendix B.6), dtoc5 (Proposition 4.8, Theorem 4.9) and camshape (Lemmas 5.1–5.2, Theorem 5.3);
  - pricing050, powerflow0030p (Proposition 5.7, Theorem 5.8), pindyck and hvycrash;
  - §6 (Theorem 6.1, Proposition 6.2) and §7.2 (Proposition 7.1).
- For optcdeg2, chain, catmix, lukvle10, waterno2, the Gibbs instances, eg, ann and KAN, the main text gives the statement and a proof idea, and validity rests on S-lemmas. That is the right split for MPC.
- Three things still make an expert reach for the supplement unnecessarily:
  - replay tiers are used in §§4–5 but defined only in §10 (issue 8);
  - Table 1 is a full rotated page with its own status vocabulary (issues 2 and 12);
  - "census" in §3.1 is defined only in S3.4 (issue 10).

**Is §9 now framed as interpretation?** Yes:

- The title, the first paragraph ("Our interpretation, which we did not test by experiment ... no certificate depends on this section") and §9.3 ("this is our explanation, not a measurement") all frame it that way.
- §9.2 sets counter-evidence beside the circumstantial evidence.
- §11.1 labels the derived recommendation as untested.
- Two small leftovers:
  - The opening sentence "did not close the 31 instances" is true by Definition 2.4 for any floating-point solver. This is the same by-construction problem that M2(a) removed from the abstract (issue 9).
  - The inverted sentence of m7 survives in §1.2 and §11.3 (issue 3).

**AI-use disclosure: accurate and adequate?**

The structure is adequate:

- a methods-level statement in §2.6, which Springer Nature's policy asks for;
- a declaration with a responsibility sentence;
- a pointer from §1.2;
- the same wording in S7 (`I-reproduction.tex:19`) and in the artifact README.

The definition of "separately written" is honest, and the common-mode paragraph is one of the better ones I have read. The content is not yet accurate in one respect. The records show that agent sessions did more than code and check:

- they ran the census and proposed the instances;
- they devised the certificate constructions and wrote the proofs;
- they ran the solver campaign and the audit;
- they made the code inspections that §2.5 and Appendix A.2 report as "we inspected".

The declaration names only implementation, checking, literature search and drafting, and calls the tools "coding and writing assistants". For a paper whose main contribution is proofs, the reader needs to know who devised them and who, if anyone, read them. The `[TODO]` placeholder asks the authors to state the second point. The final text must answer it concretely; a general sentence is not enough (issue 1).

**Length.** The paper is still long for MPC: 42.85 pages of body, 60 pages in all, plus a 135-page supplement. The cuts so far removed repetition in §§1, 3, 4 and 9. Sections 2, 7 and 8 and the appendices did not shrink. The cuts in issue 2 reach about 39 body pages without dropping any theorem statement or qualifier, and they shorten the PDF to about 55 pages.

**Correctness.** I found no mathematical error. These spot checks agree with the text:

- the ann gap (0.19402%, displayed as 0.195%);
- the five waterno2 factors and gaps;
- the BARON distances of Proposition 8.1 (5.258·10⁻⁷ absolute, 1.227·10⁻⁷ relative; 2.053·10⁻⁶ absolute, 4.798·10⁻⁷ relative);
- the camshape gaps of §5.1;
- the §3.2 and §9.1 counts (11 closures with δ ≤ 3.00·10⁻¹³; branching dimensions 12 + 6 + 7 + 2 = 27, plus pindyck and eg = 31);
- the §7.4 class and solver counts.

In addition, I reread these proofs and found them correct:

- Theorem 4.7 / Appendix B.6;
- Proposition 4.8;
- Proposition 5.13;
- Corollary 5.12;
- the residual arguments for dtoc5 and chain under reading (c) in A.4.

The remaining issues are about consistency (issues 4 and 5), not about validity.

---

## 3. Remaining requested changes

### Major

**1 (major). The AI-use statement understates the agents' role, and §2.6 and the declaration describe it differently.**
- Files:
  - `sections/02-semantics.tex:177–178` (§2.6, p. 10);
  - `sections/11-conclusion.tex:76–79` (declarations, p. 44);
  - `sections/02-semantics.tex:169` ("inspection of the code showed", p. 10);
  - `sections/A-semantics.tex:34` ("We inspected every code", p. 53).
- Problem:
  - §2.6 says that "the certificates, their checking programs, ... were produced with AI coding agents".
  - The declaration says the agents were "coding and writing assistants" used "to implement and re-implement the certificate computations, to check them, to search the literature and to draft the manuscript". It does not say that agents devised the certificate constructions and wrote the proofs, proposed the instances, or ran the audit and the solver campaign.
  - Code inspections done by agent sessions are reported as "we inspected".
  - A reader therefore cannot tell whether the proofs, the paper's main contribution, were devised or read by a person.
- Evidence:
  - `research-20260929/root-research-log.md:42–45` ("Five background agents: literature/novelty audit; theory of decomposition certificates; ... Root runs a treewidth census").
  - `:62–63` ("Launched an agent to compute rigorous decomposition-aware dual bounds for them").
  - `:140–143` ("The independent verifier ... rechecked all 11 bounds with its own code").
  - `research-20260929/README.md:5–6` ("'Reviewed' means checked by an independent research agent").
  - `development/data-semantics.md:1–12` (the code-reading audit behind Appendix A.2 is an agent task: "I read the dual codes").
  - `development/dossiers/camshape.critique.md:3–4` ("a Claude agent in the same project; not a human review").
- Fix (the authors confirm each verb against the records):
  - (a) Replace `02-semantics.tex:177–178` by:
    > AI agents (Anthropic Claude and OpenAI GPT models), run by the authors in directed sessions and multi-agent workflows, carried out most of the work reported here: they proposed the instances, devised the certificate constructions and wrote their proofs, wrote the first and the separately written implementations, ran the solver experiments and the audit, inspected the codes (Appendix A.2), and wrote the reviews of code and proofs that the supplement reports. The project records do not identify the model of every session. [One sentence on what a person has checked, e.g. "The authors read the proofs of Theorems 4.7 and 5.3 and of Proposition 5.13." If no person read any proof or code line by line: "No person has read the proofs or the code line by line; every check reported here was made by an agent session or by a program."] No person outside the authors has checked the code or the proofs.
  - (b) Replace `11-conclusion.tex:77` by:
    > AI agents (Anthropic Claude and OpenAI GPT models), directed by the authors, proposed the instances, devised the certificate constructions and their proofs, implemented and re-implemented the certificate computations, ran the solver experiments and the audit, checked code and proofs, searched the literature and drafted the manuscript. Section 2.6 states how the implementations were produced and checked and what a person has read. The authors take full responsibility for the content.
  - (c) If no person did the inspection:
    - `02-semantics.tex:169`: "inspection of the code showed" → "inspection of the code by an agent session showed".
    - `A-semantics.tex:34`: "We inspected every code ..." → "A separate agent session inspected every code ...".

**2 (major). The main text is still about 5 pages over the authors' own 38-page target, and Sections 2, 7, 8 and the appendices did not shrink.**
- Files: whole main paper. Measured: body 42.85 pp.; §2 6.58, §7 3.59, §8 3.51; Appendix A 3.42 (build-r3 §5).
- Problem: MPC readers face 60 pages before the supplement. Several results are still stated in full in more than one place:
  - the SCIP mechanism: C3 at `01-introduction.tex:94`, Box 2, Lemma 8.4, Observation 8.5, §11.1 and A.4. "0.343" occurs 10 times in the main PDF.
  - the CAMINO margins: C3 and Proposition 8.6.
  - the 79/109 breakdown: C3 and §8.3.
  - the branching dimensions: §1.2 observation 1 and §9.1.
- Evidence: phrase counts on `pdftotext` output (new / old): "0.343" 10/12, "wrong optimal value" 7/5, "camshape100 and camshape200" 6/7, "separately written" 38/35.
- Fix (savings estimated from the current layout; no theorem statement or qualifier is dropped, each keeps one home with a cross-reference):
  - (a) Table 1 (p. 11; generated by `data/make_tables.py:1503ff`). Replace it by an upright `\footnotesize` table with four columns (family | dual tags | status | level, about 0.4 page) and move the full table to S7. About −0.6 p.
  - (b) C1–C4 (`01-introduction.tex:73–107`, about 1,100 words). Limit each item to 10 lines. Drop the SCIP mechanism sentence (`:94`), the CAMINO margins and assumptions, the 79-of-109 breakdown, the 13-closures primal sentence (it belongs to §6.2) and the KAN width details (Theorem 5.17, Table 4). About −0.7 p. For example, C3 becomes:
    > **C3 (solver and published claims).** SCIP 10.0.2, 10.0.3, 10.1.0 and a development snapshot return wrong optimal values on subproblems of `waterno2_06` for some random seeds; exactly feasible rational witnesses, which SCIP's own feasibility check accepts, refute them, and an archived 15-variable reproducer shows the same error (Section 8.2). Under stated assumptions about the recorded runs, the CAMINO bounds for Gurobi on the three `eg` instances and MINOTAUR's infeasibility report for the QPLIB copy of `optcdeg2` are invalid as recorded (Section 8.2). In one-hour runs of BARON, Gurobi and SCIP on all 43 instances, every finite final dual bound is weaker than ours; only BARON's runs on `camshape100` and `camshape200` end within 10⁻⁶, as tolerance-level closures (Section 8.3). The runs check the status of current solvers; they do not rank them.
  - (c) §8.2. Move Proposition 8.3 and Lemma 8.4 with their proof notes (`08-solvers.tex:75–92`) to S6.6 and keep one sentence each, e.g. "The reproducer fm336 has optimal value 187/270, and SCIP's values for it are wrong in three senses (Proposition S6.x); fl(0.7)³ lies strictly below fl(0.343) (Lemma S6.x)". Box 2 and Observation 8.5 already carry the mechanism. About −0.5 p.
  - (d) §7.4–7.5. Fold the paragraphs "Class (i-r)", "The emfl instances" and "rocket: outside the screen" (`07-audit.tex:89–102`) into one sentence each with pointers to S4.4, Proposition S4.8 and S4.6. Move the second paragraph of §7.5 to S4.1. About −0.5 p.
  - (e) §10. Move the `waterno2` regeneration values and the `topopt` basis remark to S7.4; keep the definitions of replay and regeneration. About −0.3 p.
  - (f) Delete the twelve "replays in Tier n" clauses in §§4–5 (Table 7 has them; this also settles issue 8). Cut §9.1 to what §1.2 does not already say (pindyck, eg, box counts). About −0.3 p.
  - (g) Move Appendix A.2–A.5 (`A-semantics.tex:32–end`, about 2.5 pp.) to the supplement. Keep A.1 and one paragraph that summarizes A.2 and A.4 for Remark 2.3. This is outside the body count but brings the PDF to about 55 pages.

### Minor

**3 (minor). The inverted sentence of round-1 m7 survives twice.**
- Files: `sections/01-introduction.tex:59` (p. 3); `sections/11-conclusion.tex:65` (p. 44).
- Fix:
  - `:59`: "We did not test why general-purpose solvers did not find such bounds; Section 9 offers an interpretation."
  - `11:65`: "... little search remained; Section 9 only interprets why general-purpose solvers did not find such bounds."

**4 (minor). §3.2 and §11.2 say that no rerun certificate stores its tree, but §2.5 says that the eg leaf partitions are stored.**
- Files: `sections/03-results.tex:51` (p. 14); `sections/11-conclusion.tex:51` (p. 43); see `02-semantics.tex:165` and `B7-eg.tex:275`.
- Evidence: p. 14, "For the 14 closures at evidence level rerun (Table 1), no search tree or stage data are stored", against p. 10, "For eg the leaf partition is stored and checked for coverage". The 14 include the three eg instances.
- Fix:
  - `03:51`: "For the 14 closures at evidence level rerun (Table 1), no search tree or stage data are stored, except the leaf partitions of the three eg instances (Section 2.5)."
  - `11:51`: "Replay was run on one machine; the rerun certificates store no per-leaf certificate data and, except for eg, no search trees."

**5 (minor). §2.6 and §5.3 describe the powerflow readers inconsistently.**
- Files: `sections/02-semantics.tex:188` (p. 10); `sections/05-other.tex:175` (p. 26).
- Problem:
  - §2.6 lists powerflow among the families whose two implementations share one OSIL reader, but not among those whose reader output a separately written reader reproduced exactly.
  - §5.3 says the certificates "are checked in [E], with two separately written readers", which reads as if each implementation had its own reader.
- Evidence: `B6-powerflow.tex:303`: "The first and second implementations share one OSIL reader; a separately written reader and row builder reproduced every row of Q ... exactly for all three files."
- Fix:
  - `02:188`: "Separately written readers reproduced its output exactly for powerflow, waterno2, ann_cumene_tanh and the KAN instances, ...".
  - `05:175`: "The two dual implementations share one OSIL reader, whose rows a separately written reader reproduced exactly; the first implementation's replay and a separately written exact replay, both in [E], reproduce or exceed every bound (Section S1.6.6); evidence level stored; Tier 1."

**6 (minor). The stated reason for not running an interval solver addresses only the primal side.**
- File: `sections/01-introduction.tex:123` (p. 5).
- Problem: "its bounds would need the same exact existence proofs for points that our certificates supply" is true of upper bounds only. The lower bounds of IbexOpt-type solvers would be the natural rigorous baseline for the paper's dual bounds and for the §9 interpretation.
- Fix: "We did not run such a solver. Its lower bounds would be a natural rigorous baseline for ours; its upper bounds would still need exact existence proofs, because it relaxes equality rows. Whether such solvers reach our dual bounds on these instances is open."

**7 (minor). Two ambiguities in the abstract.**
- File: `sections/00-abstract.tex:7, 9` (p. 1).
- Problem:
  - "for nine we characterize the optimal value exactly, and for seven, floating-point closures ... had been reported" reads as seven of the nine. The seven are lnts50–lnts400, dtoc5, camshape100 and eg_int_s.
  - "Our six Kolmogorov–Arnold network instances" makes the instances sound like the authors' own.
- Fix:
  - Line 7: "...; for nine we characterize the optimal value exactly, and for seven of the 31, floating-point closures or near-closures had been reported."
  - Line 9: "The six Kolmogorov–Arnold network instances we study have no exactly feasible point; ...".
  - To stay within 250 words, drop "calibrations," from the list of devices.
  - Optional: write "separately written code from separate agent sessions rechecks them", because the abstract's independence claim rests on that term.

**8 (minor). Replay tiers are used in §§4–5 before §10 defines them.**
- Files: `sections/04-split.tex:167, 209, 236, ...` (7 uses); `sections/05-other.tex` (5 uses); pp. 19–28.
- Fix: delete these clauses (issue 2(f)). Alternatively, add to §2.6 after the replay/regeneration sentence: "Section 10 sorts replays into three tiers by recorded wall time: under 10 minutes (Tier 1), under one hour (Tier 2) and longer (Tier 3)."

**9 (minor). §9 opens with a sentence that is true by construction.**
- File: `sections/09-interpretation.tex:18` (p. 39).
- Problem: under Definition 2.4, no floating-point solver can "close" an instance, so "The solvers whose bounds MINLPLib lists did not close the 31 instances" carries no information. The informative fact concerns the listed dual bounds.
- Fix: "For none of the 31 instances of Table 2 did a listed dual bound come within 10⁻⁶, relative, of the optimum; the certificates of Sections 4 and 5 did." This holds: the closest listed duals are those of camshape100 (1.22·10⁻⁶) and lnts50 (3.9·10⁻⁵).

**10 (minor). §3.1 uses "census" without defining it, and its last clause is unclear.**
- File: `sections/03-results.tex:44` (p. 14); the term is defined only in `D-literature.tex:282–290`.
- Fix: "Three separately written programs reproduce every count of the selection from the saved pages; no further agent session reviewed the code that applies the selection rule (Section S3.4)."

**11 (minor). Read after the disclosure, "by hand" and "the authors' code" suggest human work.**
- Files:
  - `sections/02-semantics.tex:164` (level hand, p. 10);
  - Table 1 hvycrash row, "identity proved by hand", "proof by hand" (`data/make_tables.py`, `tab_trust`);
  - `sections/06-points.tex:78` ("the existence proof is by hand");
  - supplement: "the authors' code" / "the verifier's code" (20 occurrences in `sections/*.tex`, defined at `B0-families.tex:11`).
- Fix:
  - Append to the definition of level hand: "(the name refers to the form of the proof, not to who wrote or checked it; Section 2.6)".
  - In Table 1: "identity proved on paper" and "written proof".
  - In §6.3: "the existence proof is a written proof (level hand)".
  - In the supplement: "the first code" and "the second code", as the main text already says.

**12 (minor). Table 1's status column uses labels that the caption does not define.**
- Files: `data/make_tables.py:1255–1256` (rows `ann_cumene_tanh`, KAN) and the caption at `:1503`; p. 11.
- Problem: "second written after reading the first" and "verified; shared core" are not among the defined statuses (verified / weaker second / partial second / proved).
- Fix: add to the caption: "second written after reading the first: the session that wrote the second code had read the first (Section 2.6); shared core: both codes use one rigorous exponential and interval core." Or use "verified" with a footnote in each case.

**13 (minor). Proposition 8.1 states the same difference once as a relative and once as an absolute number, without saying so.**
- File: `sections/08-solvers.tex:31–32` (p. 36).
- Problem: (a) "within 1.23·10⁻⁷ and 4.80·10⁻⁷, relative" and (b) "at least 5.25·10⁻⁷ and 2.05·10⁻⁶ below" describe the same gap, because the reported dual and primal values are equal. On a first reading they look like two different gaps.
- Fix: "(a) Both reported dual bounds are valid; they lie below the exact optima by at least 5.25·10⁻⁷ and 2.05·10⁻⁶, and by at most 1.23·10⁻⁷ and 4.80·10⁻⁷ relative. (b) The reported optimal values equal these bounds; no exactly feasible point attains them, and the two returned points are not exactly feasible."

**14 (minor). Report the SCIP defect and the refuted bounds upstream before submission.**
- Files: `sections/08-solvers.tex:108` (p. 38); `sections/01-introduction.tex:95` (C3).
- Problem: the novelty sentence is dated 2026-10-02 and will be stale at review (round-1 m16; declined as an author action, R-11).
- Fix: file the fm336 reproducer with the SCIP developers and cite the issue number in both places. Send the 22 refuted bounds to the MINLPLib maintainer and ask for the stored per-solver values, which could make Hypothesis H unnecessary for `rocket100`.

**15 (minor). Residual artifact points for the MPC technical editor.**
- Files: `sections/I-reproduction.tex:213` and the register (S7); `artifact/README.md`.
- Problem:
  - The archive paths still name development and review rounds, e.g. `$P/development/reviews/round1/kan-guard/`, `$R/open-instances-wave3/` and `$P/development/dossiers/ann-kan-checks/`.
  - Four Tier-1 rerun certificates (chain, lukvle10, ex6_2_5, ex6_2_7) take minutes each, yet their leaf boxes are not stored. R-03 gave "needs new computations" as the reason; these computations are short.
- Fix (optional, before deposit):
  - In the deposited copy (not the research tree), rename the review-round folders to neutral names and record the mapping in the README.
  - Rerun the four Tier-1 searches with leaf logging, and archive the leaf boxes and per-leaf (V, H) or multiplier data, so that these results move from level rerun to stored.

---

## 4. Checks run for this review

All checks were targeted and run by this reviewer under `/tmp/r2-opusref/` on at most two cores. No repository script was run, and no CI result was consulted.

- `pdftotext -layout` of `build/main.pdf` (read in full) and `build/supplement.pdf` (searched); `pdfinfo`.
- `pdftoppm` renders of main pp. 1–4 (70 dpi) and 11–14 (80 dpi). Table 1, Figure 1 and Table 2 print in full.
- Extracted the round-1 backup tar to `/tmp/r2-opusref/old/`; compared the old and new PDF text (page and word counts, phrase counts).
- Python `fractions`: ann δ; the waterno2 factors and gaps; the BARON distances of Proposition 8.1; the camshape listed-dual gaps of §5.1; the abstract word count (247).
- Rechecked by reading: Theorem 4.7/B.6, Proposition 4.8, Proposition 5.13, Corollary 5.12, A.4 (dtoc5, chain), and the §3.2, §7.4 and §9.1 counts.
- `grep` of the sources: tier uses, "by hand", "separately written", the eg storage statements, the powerflow reader statements (`B6-powerflow.tex:303`), the AI statements (`I-reproduction.tex:19`, `B0-families.tex:11`).
- Read-only lookups in the development records named in issue 1.
