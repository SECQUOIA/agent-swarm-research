# Round-3 referee report (lens: senior MPC referee, final check)

Manuscript: "Rigorous certificates for open MINLPLib instances and an audit of listed dual bounds" (Mathematical Programming Computation).

Material read:
- `build/main.pdf` (56 pp., SHA-256 `d281b313…`, which matches `artifact/RELEASE.md`). No source file is newer than the build.
- `build/supplement.pdf` (131 pp.), searched and read in the parts that the main text cites.
- `artifact/README.md`, `RELEASE.md` and `claims.json`.
- The round-2 reviews and `adjudication.md`, and `development/build-r4.md`.

Line numbers refer to the current sources. Page numbers refer to `main.pdf`.

## Recommendation

**Ready for submission after one correction. Referee verdict: minor revision (text only).**

The revision resolves every major item of round 2 that the authors could act on:
- The AI-use statement is accurate, and it says the same thing in §2.6, the declarations, S7 and the README.
- The claim index is repaired.
- Table 1 is upright, and its status labels are defined.
- Replay tiers have one home.
- The paper is 4 pages shorter.

I found no mathematical error in the certificates.

The final condensation moved Propositions 4.3(c) and 4.5 (last statement), Proposition 8.3 and Lemma 8.4, and merged Sections 9 and 11. I checked every moved statement and its new pointer against the round-3 sources (r3 tar):
- The moved statements and proofs in S1.10 and S6.6 are verbatim and correct.
- One pointer sentence is wrong. The one-sentence replacement of Lemma 8.4 in §8.2 states a false rounding fact. That fact contradicts Appendix A.4 of the same PDF and Lemma S6.3 (issue 1, major, one-sentence fix).
- Two other pointers drop a hypothesis (issue 7, minor).

Counts (placeholders excluded): **0 blocker, 1 major, 9 minor.**

**Submission condition (placeholder, not counted).** The declaration `\TODO` must say concretely what a person has checked. Two sentences are currently silent about the authors themselves: §2.6 (`02-semantics.tex:179`) says "No person outside the authors has checked the code or the proofs", and §11 (`11-conclusion.tex:26`) says the same.
- If an author read some proofs or code, name them, in §2.6 as well as in the declarations.
- If no author did, say so plainly: "No person has checked the proofs or the code line by line; every check reported here was made by an agent session or by a program."

An MPC editor will weigh this sentence. It must not stay implicit.

---

## 1. Status of the round-2 items

### 1.1 `round2/opus-referee.md` (15 items)

| # | item | status | evidence |
|---|---|---|---|
| 1 | AI-use statement understates the agents' role | **resolved** (author confirmation pending) | One wording in §2.6 (`02-semantics.tex:177–179`), the declarations (`11-conclusion.tex:52–56`), the README (`:8–15`) and S7 (`I-reproduction.tex:19`). Code inspection is attributed to "an agent session" (`02:169`, `A-semantics.tex:34`). Issue 3 is a small follow-up on "we". |
| 2 | Length | **partly** | Body 42.85 → 41.07 pp.; PDF 60 → 56 pp. Done: (a) upright Table 1; (b) shorter C1–C4; (c) Prop. 8.3 and Lemma 8.4 moved; (d) §7.4 folded; (e) §10 regeneration details moved; (f) tier clauses deleted and §9.1 cut. Rejected with a reason: (g) Appendix A stays (R2-01). The body is still 3.1 pp. over the authors' own target; issue 8 (optional). |
| 3 | Inverted sentence | resolved | `01-introduction.tex:59`; `11-conclusion.tex:41`. |
| 4 | eg trees stored or not | resolved | `03-results.tex:58`; `11-conclusion.tex:28`. |
| 5 | powerflow readers | resolved | `02-semantics.tex:189–190`; `05-other.tex:173`. |
| 6 | Interval-solver sentence | resolved | `01-introduction.tex:120–122`, including the IbexOpt rigor mode. |
| 7 | Abstract ambiguities | resolved | "seven of the 31 … (one for a copy)"; "The six KAN instances in our set". The optional phrase was rejected (R2-07), which I accept. |
| 8 | Tiers before their definition | resolved | No "Tier" in §§4–5. Tiers are only in §10 and Table 7. |
| 9 | §9 opening true by construction | resolved | `09-interpretation.tex:26`. |
| 10 | "census" undefined | resolved | `03-results.tex:51` ("Three programs, written in at least two separate agent sessions"). |
| 11 | "by hand", "authors' code" | resolved | `02:164`, Table 1 ("written proof"), `06:78`. The supplement uses first/second code. |
| 12 | Table 1 status labels | resolved | Caption of `tables/tab-trust.tex` defines verified, weaker second, partial second, proved and shared core. |
| 13 | Proposition 8.1 wording | resolved | `08-solvers.tex:47–48`. |
| 14 | Upstream reports | **partly** | The text now says that communication is pending, and it no longer reads the tracker search as proof of absence (`08:111–112`, `07:103`, README `:52`). Nothing was filed (author action, R2-04). Issue 9. |
| 15 | Artifact residuals (folder names, Tier-1 leaf logging) | not done; reasons accepted | Rejected as R2-02 and R2-03. The README vocabulary is a separate, smaller point (issue 10). |

### 1.2 `round2/opus-claims.md` (14 items)

| # | item | status |
|---|---|---|
| 1 | AI disclosure omits devising constructions and proofs | resolved (wording now names them). |
| 2 | Definition of "separately written" admits the `ann` second code | resolved differently. The definition is now code-based: no import, no run, no copied code. The `ann` second code is excluded because it copied an idiom (`rem:ann-saturation`). §2.6, Table 1, S1.9, the register and `claims.json` agree. Issue 2 is the remaining transparency point. |
| 3 | "Six to eight separately written checkers" | resolved: "eight code bases from six agent sessions" (`08:89`, S6.6); "three programs, … at least two separate agent sessions" (`03:51`, S3.4). |
| 4 | "little search remained" | resolved (`01:58`; `11:41`, "27 of the 31"). |
| 5 | "changes the verdict" | resolved (`01:61–62`; `11:43`). |
| 6 | Remark 2.3(1) overstates the exact GAMS/OSIL comparison | resolved (`02:49`: 17 exact, 4 `catmix`, 22 sampled; `08:150`). |
| 7 | §3.2 vs. stored eg partitions | resolved. |
| 8 | KAN guard not explained | resolved (`05:330`). The register names the guarded replay. |
| 9 | Abstract and §8 qualifiers | resolved (`00:7,9,13`; `08:41`). |
| 10 | "part of the domain" in §1 | resolved (`01:54`). |
| 11 | IbexOpt; Hoen–Gleixner "certify" | resolved (`01:120–124`). |
| 12 | Status words; register row of `prop:kan-infeasible` | resolved: "floating-point output" is defined (`02:201`); the register row now reads `hand+stored` with a second checker. |
| 13 | powerflow separately written reader | resolved. |
| 14 | `open-items.md`; README "independently" | resolved. |

### 1.3 `round2/opus-consistency.md` (16 items)

| # | item | status |
|---|---|---|
| 1 | §4.6 stale waterno2 tier | resolved (the clause was deleted). |
| 2 | Three status labels for `ann_cumene_tanh` | resolved: "proved" everywhere, for one reason (copied idiom). |
| 3 | Claim index: empty waterno2 displays, inflated labels, wrong commands | resolved. I reran the validator from `/tmp`: `PASS: 65 claims; 5604 SHA-256 references; 1914 distinct files`. The `register-07/08` displays are present. `register-17` and `register-21` are labelled *proved*. |
| 4 | S1.3 QPLIB thresholds | resolved (`B3-camshape.tex:283`). |
| 5 | `tab:claims` caption: 15 vs. 35 points | resolved. |
| 6 | eg ratio 44–151 | resolved ("3.2 to 151", `05:265`, `09:79`). |
| 7 | "stored model" in `tab:solvers` | resolved ("unmodified model (GAMS file)"). |
| 8 | §3.2 eg partitions | resolved. |
| 9 | powerflow readers | resolved. |
| 10 | Register "2nd" caption | resolved (`I-reproduction.tex:116`). |
| 11 | C2 "settles conflicts" | resolved (`01:89`). |
| 12 | 1.11 vs. 1.115 units | resolved (`A-semantics.tex:103`). |
| 13 | Missing tier clauses | superseded: the tier clauses were removed (R2-05). |
| 14 | Table 7 `eg_disc2_s` cell | resolved (`10:74`). |
| 15 | README "independently" | resolved (`README.md:33`). |
| 16 | (a) Table 5 caption; (b) 2.93e-15 record; (c) unused figure; (d) `labels.md`; (e) "This section" openings; (f) homeless superseded displays | all resolved: (a) caption shortened; (b) source comment in S6.6 and `RUNS.md`; (c) moved to `development/unused-figures/`; (d) current numbering; (e) "This subsection"; (f) `HISTORY.md`. |

---

## 2. The final paper read afresh

**Contribution and structure.** By the end of p. 3 the reader knows four things:
- the problem (Box 1);
- the exact semantics;
- what a closure is;
- the three observations.

C1–C4 are now readable at about a page. Most of the reorganisation is a clear improvement:
- the semantics and protocol (§2) come before the results;
- the certificates (§§4–6) come before the audit and the solver claims (§§7–8);
- the interpretation and the recommendations share one section (§9), and that section is labelled untested throughout.

§11 now does what a conclusion should do: limitations, open problems, and a return to the three observations that §1.2 announces.

**Correctness.** I reread the following and found them correct:
- Lemma 4.1 to Proposition 4.5 with Appendix B;
- the lnts proof (B.5): the root, feasibility via $c_j=w_j(r_j+N/2)$, optimality with $\mu^*=-\nu^*N/2$, and the enclosure;
- Proposition 4.8;
- Lemma 5.1 and Theorem 5.3;
- Proposition 5.13 (hvycrash), including $\kappa<6.52\cdot10^{-3}$ and $3-50\kappa/0.85>2.6$;
- Theorem 5.11 with the uniqueness argument of Corollary 5.12 in S1.5 (interior maximizer);
- Proposition 7.1;
- the moved Propositions S1.78, S1.79 and S6.2 and Lemma S6.3.

In rational arithmetic I checked:
- the camshape listed-dual gaps (8.27%, 16.31%, 19.93%);
- the CAMINO margins (0.2445944, 0.4312902, 5.2010558; 4.33%, 7.48%, 80.5%);
- the SCIP excess ranges of Proposition 8.2;
- $39157472136693483/2^{47}=278.2305\ldots$;
- the counts behind "12 of the 31 closures … more than $|U|/2$" and "eleven more have δ ≤ 3.00·10⁻¹³".

**Consistency.** The counts agree across the abstract, §§1–11, the tables, S4, S6, S7, `claims.json` and the README:
- 31/14 families, 28+3, 7+9+15 prior status, 14 rerun closures;
- 12+6+7+2 = 27 branching census;
- 19+12+12+63+25 classes, 22/18/16 LINDO;
- 129/109 = 79+6+6+18, 35 = 30+5.

The supplement's cross-references to main-text numbers are current (for example "Proposition 8.4" for CAMINO and "Proposition 4.3" for affine splits). The recipe in S7.1 and the README is identical (diff). Table 7, the register and the README agree on every tier.

**AI-use disclosure.** It is now adequate in substance. Four things are in place:
- it is in the methods section;
- it names what the agents did, including devising the constructions and writing the proofs;
- it defines "separately written" by what the code does and says plainly that most second sessions had read the first code;
- it keeps the common-mode paragraph.

Two items remain:
- The authors' confirmation (submission condition above).
- Issues 2 and 3, which make the disclosure easier to apply across the paper.

**Condensation check.**

| moved item | new pointer in main text | verdict |
|---|---|---|
| Prop. 4.3(c) → Prop. S1.78 | `04-split.tex:86` | statement and proof verbatim; the pointer omits differentiability (issue 7) |
| Prop. 4.5 last statement → Prop. S1.79 | `04-split.tex:118` | verbatim; I rechecked the potential construction with the cap $M_t$; the pointer omits "SP finite" (issue 7) |
| Prop. 8.3 → Prop. S6.2 | `08-solvers.tex:92` | accurate summary |
| Lemma 8.4 → Lemma S6.3 | `08-solvers.tex:93` | **wrong summary (issue 1)** |
| §11 recommendations → §9.2 | `09-interpretation.tex:55–81` | consistent; labelled as untested proposals; §1.5 and §1.2 point correctly |

---

## 3. Remaining issues

### Major

**1 (major). §8.2 restates Lemma 8.4 (now Lemma S6.3) wrongly, and the restatement contradicts Appendix A.4.**
- File: `sections/08-solvers.tex:93` (p. 36).
- Problem: the sentence reads "The trigger is a rounding fact: $\fl(0.7)^3$ lies strictly below $\fl(0.343)$, although $0.7^3=0.343$, while no other station value or power in waterno2 shows such a gap." Under its natural reading, the second half is false.
  - $\fl(0.6)^3<\fl(0.216)$, $\fl(0.85)^3<\fl(0.614125)$ and $\fl(0.7)^2<\fl(0.49)$ also hold. Lemma S6.3's proof lists these residuals (`H-solvers.tex:279`), and Proposition S6.2(3) uses $\fl(0.6)^3<\fl(0.216)$ (`H-solvers.tex:262`).
  - Appendix A.4 of the same PDF says "For stations A, B2 and D the binary64 values violate these identities" (`A-semantics.tex:95`, p. 52). S1.8 says the same (`B8-waterno2.tex:49`).
  - What distinguishes the $0.7$ cube is narrower: the tightest interval with binary64 ends around $\fl(0.7)^3$ lies entirely below $\fl(0.343)$, because the residual exceeds one binary64 spacing. For every other station and power, that interval still reaches $\fl(\ell^k)$.
- The error was introduced by the last condensation. The r3 text kept the full lemma statement, which is correct. The error is on the paper's one diagnosed solver defect, and §8.2's next paragraph and the trigger scan (`08:107`) rely on the correct distinction.
- Fix: replace `08-solvers.tex:93` by
  > The trigger is a rounding fact: although $0.7^3=0.343$, the tightest interval with binary64 ends around $\fl(0.7)^3$ lies strictly below $\fl(0.343)$; for the other station values and powers of \inst{waterno2}, the binary64 residual is smaller than one binary64 spacing, so the tightest such interval still reaches $\fl(\ell^k)$ (\cref{lem:scip-cube}).

### Minor

**2 (minor). §2.6 says that the second session received only the statement, the model files and the stored inputs, and then says that most second sessions had read the first code. The reader cannot tell which families have the stronger form of separation.**
- Files: `sections/02-semantics.tex:184` and `:187` (p. 10); `data/make_tables.py` (`tab-trust-full`, Table S37).
- Problem:
  - Line 184 ("received the statement to be checked, the model files and the stored inputs, and wrote its own code") reads as a description of everything the second session saw.
  - Line 187 then says "in most families the session that wrote the second implementation had read the existing code in full before writing its own".
  - Both statements are true, but together they leave the reader guessing. "Verified by a separately written implementation" is the paper's strongest status word, and its weight differs between families whose second session read the first code and families whose session did not.
  - `build-r4.md` §11 item 1 records that the session records identify these families: about nine, namely lnts, dtoc5, optcdeg2, camshape, chain, catmix, pindyck, powerflow0039 and waterno2.
  - On the open lead-author decision: I recommend keeping the code-based definition. It is checkable from the code, and the current text is consistent with it. The reading fact should be shown per family rather than in the definition.
- Fix:
  - `:184`: "… that received the statement to be checked, the model files and the stored inputs, and wrote its own code; in most families it also read the first implementation (see below)."
  - `:187`: after "as part of reviewing it", add "(\cref{tab:trust-full} names these families)". Add one column, or a caption note, to Table S37: "second session read the first code before its own results: yes/no". Take the entries from the records that G1 checked, and confirm "about nine" exactly before printing.

**3 (minor). After the disclosure, "we" is ambiguous where an action was taken by agent sessions.**
- Files: `sections/02-semantics.tex:177–179` (p. 10). Examples:
  - `01-introduction.tex:53` ("We built each dual bound");
  - `01-introduction.tex:76`, `03-results.tex:49` and `11-conclusion.tex:32` ("We chose the instances by judged tractability");
  - `01-introduction.tex:129` ("Our search for prior results").
- Problem: §2.6 says that agents selected the instances, devised the constructions and searched the literature. The paper then says "we" did these things. The style guide asks the text to name the actor (`development/style-guide.md:15`). One convention sentence settles every case without rewriting the paper.
- Fix: after `02-semantics.tex:177`, add: "In this paper, ``we'' refers to the authors together with the agent sessions they directed; where a statement concerns what a person did, it says so."

**4 (minor). §11 names too few proof re-readings and uses an undefined term.**
- File: `sections/11-conclusion.tex:26` (p. 42).
- Problem:
  - "The extended-value proofs of Appendix B and the eg primal check were rechecked by separate agent sessions" reads as the complete list of re-read proofs. The supplement reports more:
    - the chain and catmix lemmas, "read in at least two separate agent sessions" (`B4-chain-catmix.tex:456, 458`);
    - the eg rounding analysis (`F-eg-rounding.tex:414`);
    - the KAN exponential code (`B9-ann-kan.tex:313`).

    The eg primal check that §11 names is `C-points.tex:269`.
  - "Extended-value proofs" is defined only by an aside in Appendix B's opening sentence.
- Fix: "Separate agent sessions reread the proofs of \cref{app:splitproofs}, of the \inst{chain}, \inst{catmix} and \inst{eg} rounding lemmas and the \inst{eg} primal check, as the supplement states for each; no person outside the authors has checked any proof."

**5 (minor). §5.1 says that for camshape200 "the gain is in rigor" immediately after giving that instance's listed gap of 8.27%.**
- File: `sections/05-other.tex:67` (p. 23).
- Problem: against the listed data, the camshape200 result is a large improvement, not only a gain in rigor. The clause means the gain over floating-point solver output: Octeract's listed solve of a rounded copy (§3.4), and BARON's tolerance-level closure in our runs (Proposition 8.1).
- Fix: "…19.93\%; for \inst{camshape100} and \inst{camshape200}, which floating-point solvers closed within their tolerances (\cref{sec:results-prior,prop:baron-camshape}), the gain over solver output is in rigor."

**6 (minor). The trigger scan covers 1,632 OSIL files, but the paper counts 1,633 instance pages, and the difference is not explained.**
- Files: `sections/08-solvers.tex:107` (p. 37) and `H-solvers.tex:321`, against `01-introduction.tex:15`, `07-audit.tex:13` and `D-literature.tex:267`.
- Problem: a reader will ask which instance was not scanned. Is it absent from the OSIL distribution, or missing from the cache?
- Fix: name the missing instance and the reason once in S6.6, for example "all 1,632 OSIL files of the snapshot (instance X has no OSIL file)". In §8.2, write "all OSIL files of the snapshot (\cref{app:solvers-scip})".

**7 (minor). Two condensed pointers to the moved explanatory results omit a hypothesis.**
- Files: `sections/04-split.tex:86` and `:118` (p. 17).
- Problem:
  - Proposition S1.78 needs each $F_t$ to be differentiable at $z^*_t$, a real condition for the extended-valued costs of §4.1. The pointer says only "at a minimizer whose bags are interior".
  - Proposition S1.79 needs $\mathrm{SP}$ finite. The pointer omits it.
- Fix:
  - `:86`: "…at a minimizer whose bags are interior and whose costs are differentiable there, they are the copy-row multipliers…".
  - `:118`: "With exact pair bounds on a partition and finite $\mathrm{SP}$, $\mathrm{SP}$ is also the largest bound…".

**8 (minor, optional). Length.**
- Files: whole main text. Measured in `build-r4.md` §10: Sections 1–11 take 41.07 pp. against the authors' target of about 38; the PDF has 56 pp.
- Problem: this is no longer an obstacle for MPC, which has no hard limit. Three paragraphs still restate material that has another home.
- Fix (about 0.4 p.; optional):
  - Delete the lnts50 paragraph at `01-introduction.tex:47`. Its fact is in Table S32 and in §9.2's second bullet.
  - Move the "Other observations" paragraph of §9.1 (`09-interpretation.tex:40–43`) to S6.3, leaving one sentence with a pointer.
  - Move §9.1's "Related effects" paragraph (`09-interpretation.tex:51–53`) to S3.1, keeping its last sentence ("We do not claim…") in §9.1.

**9 (minor; author action). Report the SCIP defect before submission.**
- Files: `sections/08-solvers.tex:111–112` (p. 37); `07-audit.tex:103`; `artifact/README.md:52–53`.
- Problem:
  - The tracker search is dated 2026-10-02, and "communication … pending" will be stale at review.
  - An MPC referee will expect a solver defect of this kind to have been reported to its developers.
  - The 15-variable reproducer and the exact witness are ready.
- Fix:
  - File `fm336` (with `tiny2` and the witness) on SCIP's issue tracker and cite the issue number in §8.2, S6.6 and the README.
  - Send the 22 refutations to the MINLPLib maintainer.
  - Update the three "pending" sentences.

**10 (minor; artifact). The artifact documents describe internal review rounds as "rounds of the revision".**
- Files:
  - `artifact/README.md:22–23, 227` ("the round-1 reruns", "moved out of the supplement in round 2");
  - `artifact/HISTORY.md:24, 82–83, 95, 132, 143, 153, 170`;
  - `artifact/RUNS.md:450, 482` (39 occurrences of "round" in `RUNS.md`, 24 in `HISTORY.md`).
- Problem: this is a first submission. "Round 1 of the revision" will read to an MPC referee or technical editor as a prior review history of the paper. The folder names (`development/reviews/round1/`) stay for hash reasons (R2-02), so the vocabulary needs one definition.
- Fix: add near the top of the README: "``Round~1'' and ``round~2'' refer to the authors' internal review rounds before submission; folder names such as \texttt{development/reviews/round1/} keep these names." In the README's own prose, replace "the round-1 reruns" by "the reruns made during internal review", and "moved out of the supplement in round 2" by "run records that the supplement does not print". Rebuild and revalidate the index if a hashed file changes (`RUNS.md` is hashed).

---

## 4. Checks run for this review

All checks were targeted and local, on at most two cores. Nothing in the paper or the research tree was edited, no repository script was run in place, and no CI result was consulted.

- **PDFs and build.**
  - `sha256sum` of both PDFs against `artifact/RELEASE.md` (match).
  - `find -newer build/main.pdf` (no newer source).
  - `pdftotext` with and without `-layout`.
  - `pdftoppm` renders of main pp. 10–14 and 42–43 at 60 dpi: Table 1, Table 2 (sideways), Figure 1, Tables 3–4 and the declarations print in full.
- **Reading.**
  - Every main-text source read in full: `00`–`11`, `A-semantics.tex`, `G-proofs-split.tex` and `tables/tab-trust.tex`.
  - In the supplement: `B10-split-extras.tex`; S6.6 of `H-solvers.tex`; and the parts of B5 (pindyck uniqueness), B8 (stations), B9 (`ann`), E (aggregates, emfl) and I (S7.1, S7.3, S7.4).
- **Round-3 comparison.** Extracted `/workspace/local-home/paper-backups/paper-open-minlplib-r3-20261004-2302.tar` to `/tmp/r3-opusref/r3/`. Compared the moved statements: `04-split.tex:76–125` and `08-solvers.tex:70–95` (r3) against `B10-split-extras.tex` and `H-solvers.tex:242–283`.
- **Claim index.** Copied `artifact/check_claims.py` to `/tmp/r3-opusref/claims/` and ran it on two cores with `--repo-root`: `PASS: 65 claims; 5604 SHA-256 references; 1914 distinct files`. Listed the status and labels of the register entries with read-only `json.load`.
- **Recipe.** Diffed the S7.1 recipe against the README recipe (identical).
- **Arithmetic** (Python and by hand): the camshape gaps, the CAMINO margins, the SCIP excess ranges, the waterno2_06 shortest-path value, the hvycrash constants, the lnts root and optimality identities, the binary64 spacings behind Lemma S6.3, the abstract word count (250 in the source), and the counts listed in Section 2.
- **grep** of the sources for:
  - the 1,632/1,633 counts;
  - references to the moved and merged labels;
  - "agent session";
  - "round" in the artifact documents;
  - the printed numbering of Propositions S1.78, S1.79, S6.1–S6.4 and Lemma S6.3.
