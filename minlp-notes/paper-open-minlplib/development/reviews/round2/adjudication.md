# Round-2 adjudication: consolidated change list

Date: 2026-10-04. Paper: `paper-open-minlplib` (main: Sections 1–11 and
Appendices A–B; supplement: S1–S8). Inputs: the six round-2 reviews in this
folder (`sol-referee.md`, `sol-verify-changes.md`, `opus-referee.md`,
`opus-writing.md`, `opus-consistency.md`, `opus-claims.md`), the lead-author
decisions LD2-1 to LD2-5, and the development records (`development/outline.md`
§8, `style-guide.md`, `terminology.md`, `build-r3.md`, `open-items.md`, the
dossiers, `research-20260929/` reports).

Source references use the review file stem and the item number, for example
`opus-writing 14` or `sol-verify U5`; `sol-referee k` is item k of its
"Remaining requested changes". Line numbers refer to the sources as reviewed.
The reviewed sources are archived in
`/workspace/local-home/paper-backups/paper-open-minlplib-r3-20261004-2302.tar`
(called **the r3 tar** below). `diff -rq` of its `sections/` and `artifact/`
against the working tree showed no difference on 2026-10-04, so its line numbers
are the ones cited here.

Verdicts: all six reviews recommend minor revision except `sol-referee`
(major, for length only). No review found a mathematical error or an unsafe
certified display, so **no certified number changes in this round**. The only
changed numeric strings are a computed margin (G1-15, taken from S4.7) and a
numerical-evidence range (G3-05, taken from S1.7).

## 0. How to use this file

- Each item has an id (`Gk-nn`), its sources, a severity (blocker, major,
  minor; the highest among its sources), a decision (accept, accept-modified,
  reject) with the reason and the evidence checked, the change, and the files.
  Where a reviewer gave replacement text, it is quoted with any modification
  already applied; "as given" means: use the reviewer's text. Rejected parts are
  listed again in Section 10.
- Editor groups and their files:
  - **G1 front:** `00-abstract`, `01-introduction`, `02-semantics`, `A-semantics`
    (and `macros.tex` if needed).
  - **G2 results and split:** `03-results`, `04-split`, `G-proofs-split`
    (Appendix B), `figures/*.py` and figure PDFs.
  - **G3 other, points, audit:** `05-other`, `06-points`, `07-audit`.
  - **G4 end:** `08-solvers`, `09-interpretation`, `10-reproducibility`,
    `11-conclusion` (and the merge of Sections 9 and 11).
  - **G5 supplement certificates:** `B0`–`B9`, `F-eg-rounding`, the new
    `B10-split-extras.tex`, and the one new `\input` line in `supplement.tex`.
  - **G6 supplement other:** `C`, `D`, `E`, `H`, `I` (except the two
    subsections owned by G7), `J`; every generator (`data/make_tables.py`,
    `make_campaign_table.py`, `make_points_table.py`), `data/numbers.json`,
    every generated `tables/*.tex`; `references.bib`.
  - **G7 artifact:** `artifact/*` (README.md, build_claims.py, check_claims.py,
    run_short_checks.py, new `HISTORY.md`, `RUNS.md`, `RELEASE.md`,
    `prepare_paper_inputs.py`); in `I-reproduction.tex` the subsections
    `\subsection{Setup}` (`app:repro-setup`) and `\subsection{Claim register}`
    (`app:repro-register`), because the setup recipe and the register are the
    artifact's interface; the development records (`terminology.md`,
    `open-items.md`, `labels.md`, `outline.md` §8).
- Shared files have one owner. A group that needs a change in another group's
  file names it in its item; the owner makes it. Moved text is always taken
  from the r3 tar (extract it to `/tmp/<group>/r3/`), never from a file that
  another group may be editing.
- Rules for every group:
  1. Do not edit `research-20260929/` or `literature/`. Do not commit.
  2. Never run a scientific script in place; copy it and its inputs to `/tmp`.
     At most two CPU cores per agent (`taskset -c 0,1`,
     `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`).
  3. Build only in a private copy (`rsync -a` of the paper to `/tmp/<group>/`,
     `make` there). The single final `make` in the paper tree belongs to the
     Build phase (Section 9).
  4. Keep every theorem statement, every hypothesis, every proof and every
     qualifier of a claim. A cut removes repetition or moves operational and
     historical records; it never removes a condition. Moved statements keep
     their proofs and get a cross-reference at the old place.
  5. One home per repeated statement (round-1 rule 6 still applies). New homes
     in this round: replay tiers only in Table 7 (§10), the certificate boxes,
     the register and the README; floating-point closure terms in §2.2;
     superseded and unsafe strings only in `artifact/HISTORY.md`; checker
     paths, commands and run records only in `artifact/RUNS.md` and S7.
  6. Agent-work vocabulary: "first code"/"second code" (or "first/second
    implementation"), never "the authors' code"/"the verifier's code";
     "separately written" only in the §2.6 sense; "by hand" only as the name of
     the evidence level `\evid{hand}`.
  7. Prose uses "best listed dual bound" (G1-07); table headers and figure
     legends may keep "best listed dual" where the caption defines it.
- Records of moved operational and historical text: G5 writes the passages it
  removes from S1 and S5 verbatim into `development/moves/r2-G5.md`, G6 those
  from S2–S8 into `development/moves/r2-G6.md`, each passage under a heading
  that names its source (file and label) and its destination (`HISTORY.md` or
  `RUNS.md`). G7 merges them into the artifact (G7-09).
- Order of work: G1–G7 edit in parallel. Cross-references to labels that
  another group creates (`prop:split-forced`, `prop:split-cellwise-best`,
  `tab:trust-full`) may be undefined in private builds until the merge.
  G7-09 runs last, after G1–G6 report done (if G7 has already finished, the
  Build phase runs G7-09 first). Then the Build phase (Section 9).

## 1. Lead-author decisions

| id | decision | implemented by |
|---|---|---|
| LD2-1 | Consolidate: shorten repeated opening summaries; reduce the unused affine-slope and cellwise-maximality results to cross-references (keep what the certificates use); merge the interpretation (§9) and the recommendations (§11) and make §11 short; move superseded-display history, long file paths and operational run records from the supplement into `artifact/HISTORY.md` and `artifact/RUNS.md`, referenced from S7. Targets: Sections 1–11 about 38 pages, supplement body about 105 pages. Keep every theorem statement, hypothesis, proof and qualifier. | Section 2; G1-10, G1-12, G1-14, G2-01, G2-02, G2-05, G2-06, G3-01, G3-08, G4-04, G4-06, G4-09, G5-01, G5-02, G6-01, G6-02, G6-04, G6-05, G6-06, G6-09, G7-03, G7-04, G7-05 |
| LD2-2 | AI-use disclosure, accurate per the records: AI agents (Anthropic Claude and OpenAI GPT models), under the authors' direction, devised the certificate constructions, wrote the proofs, implemented and separately re-implemented the computations, checked them, searched the literature and drafted the manuscript. Said once, identically in substance, in §2.6 and in the declarations; keep "[authors to confirm, including which proofs and code the authors checked themselves]"; keep the common-mode risk and mitigations in §2.6. | G1-01, G1-15, G4-08, G5-06, G6-09, G6-10, G7-07 |
| LD2-3 | Upstream communication: state that the SCIP reproducer and the MINLPLib bound witnesses are in the supplement and archive and that communication with the developers and maintainers is pending at the time of writing; do not claim that a tracker search proves the absence of a report. | G1-12, G3-08, G4-04, G6-05, G7-07 |
| LD2-4 | Artifact: local, isolated full recipe (concrete disposable `WORK`; all model reads from the archived-input root; no writes to the user's `~/.cache`; a paper-only input preparation that succeeds or handles the 26 unrelated models explicitly); fix `build_claims.py` (waterno2 displays, status words, relevant recorded commands only); add `artifact/RELEASE.md` with SHA-256 of the final PDFs (written in the Build phase) and separate source/evidence validation from PDF identification. | G7-01, G7-02, G7-03, G7-06, G7-09, Section 9 |
| LD2-5 | Apply every other accepted round-2 item; reject only with a reason checked against sources. | this file; Section 10 lists the rejections |

Evidence for the LD2-2 wording (checked for this file): the agents also chose
the research direction and the instances (`research-20260929/root-research-log.md`:
"Candidates weighed (root judgment, not reviewed)", the census and "Launched an
agent to compute rigorous decomposition-aware dual bounds", the audit "chosen
for breadth of impact"); the one-hour campaign report was written by "author of
track solver-campaign in workflow wf_2951b32d-9f3"
(`research-20260929/publication/solver-runs/report.running.md:1`); the code
reading behind Appendix A.2 is an agent task (`development/data-semantics.md:1–12`,
"I read the dual codes"); the proof and code reviews are agent sessions
(`development/decision-register.md` G-09, O-3; `research-20260929/README.md:5–6`).
No record shows a person deriving a certificate or a proof. G1-01 therefore
adds "selected the instances" and "ran the solver experiments and the audit" to
the lead author's list (accept-modified); the author-confirmation placeholder
stays, and no editor writes what a person checked.

## 2. Page budget and moves

Baseline: `build-r3.md` §5 (main Sections 1–11: 42.85 pages; supplement body
S1–S8: 124.91 pages). Targets follow LD2-1 and leave about 0.7 page of slack in
the main text for the new text of G1-01, G1-02 and G3-02.

### 2.1 Main paper

| part | now | target | group |
|---|---:|---:|---|
| §1 Introduction | 4.59 | 3.8 | G1 |
| §2 Semantics (with Table 1) | 6.58 | 5.6 | G1 |
| §3 Results (with Tables 2–4, Figure 1) | 3.19 | 3.1 | G2 |
| §4 Split certificates | 7.18 | 6.6 | G2 |
| §5 Other certificates | 7.09 | 6.6 | G3 |
| §6 Points | 2.49 | 2.2 | G3 |
| §7 Audit | 3.59 | 2.9 | G3 |
| §8 Solvers | 3.51 | 3.0 | G4 |
| §9 Interpretation and recommendations (merged) | 1.40 + 0.9 of §11 | 1.6 | G4 |
| §10 Reproducibility | 1.41 | 1.2 | G4 |
| §11 Limitations and conclusion | 1.83 (with recommendations) | 0.7 | G4 |
| **Sections 1–11** | **42.85** | **37.3** (about 38 with new text) | |
| Appendix A | 3.42 | ≤ 3.3 | G1 |
| Appendix B | 4.35 | ≤ 3.0 | G2 |

Group totals for Sections 1–11: G1 9.4, G2 9.7, G3 11.7, G4 6.5.

### 2.2 Supplement

| part | now | target | group |
|---|---:|---:|---|
| S1 opening, S1.1–S1.9, new S1.10 (explanatory split results, +1.4) | 76.57 | 66 (with S5) | G5 |
| S5 eg rounding-error analysis | (in the line above) | | G5 |
| S2 Points | 7.10 | 6.2 | G6 |
| S3 Literature (+0.3 for the moved citation list) | 7.05 | 6.8 | G6 |
| S4 Audit | 12.81 | 10.8 | G6 |
| S6 Solvers (+0.6 for Prop. 8.3 and Lemma 8.4) | 12.57 | 10.9 | G6 |
| S7 opening, S7.2 (+0.9 full Table 1), S7.4, S7.5 (former S8) | 7.02 + 1.80 together with G7's part | 2.3 | G6 |
| S7.1 Setup, S7.3 compact register | (in the line above) | 2.2 | G7 |
| **Supplement body** | **124.91** | **about 105** | |

If a group reaches its content floor (statements, proofs, hypotheses,
qualifiers and the evidence behind printed claims) above its target, it stops
and reports the indispensable material page by page (`sol-referee 1`: explain
any excess by naming the indispensable material).

### 2.3 Moves (nothing is deleted without a destination)

| # | material (r3 tar location) | destination | removes / inserts |
|---|---|---|---|
| M1 | Prop. 4.3(c) and its proof, with the paragraph "Unrolled, … no certificate uses it" (`04-split.tex:83–85, 89–90`; `G-proofs-split.tex`, part (c) of the proof of `prop:split-affine` and the following paragraph) | S1.10, new Proposition with label `prop:split-forced` | G2 / G5 |
| M2 | Last statement of Prop. 4.5 (`04-split.tex:118`) and the "Best constants" part of its proof with the remark on the cap (`G-proofs-split.tex`, from "\emph{Best constants.}" to the end of `app:splitproofs-cellwise`) | S1.10, new Proposition with label `prop:split-cellwise-best` | G2 / G5 |
| M3 | Prop. 8.3 (`prop:scip-reproducers`) with the note after it, and Lemma 8.4 (`lem:scip-cube`) with its proof note (`08-solvers.tex:75–91`) | S6.6, labels unchanged | G4 / G6 |
| M4 | §7.4 paragraphs "Class (i-r)", "The emfl instances", "rocket: outside the screen" (`07-audit.tex:89–101`) | one folded paragraph in §7.4; the details are already in S4.4–S4.6 | G3 / G6 checks |
| M5 | §7.5 second paragraph on MINLPLib's aggregates (`07-audit.tex:110–112`) | S4.1 "How MINLPLib aggregates" | G3 / G6 |
| M6 | §10 regeneration details (`10-reproducibility.tex:39–42`: waterno2 regenerated values, powerflow0030p, topopt basis) | S7.4 (already holds most of it) | G4 / G6 |
| M7 | §1.4 citation list of classical mechanisms (`01-introduction.tex:128`, all keys) | new paragraph in S3.1 | G1 / G6 |
| M8 | Data-reading and primal-construction columns of Table 1 | full table `tab:trust-full` in S7.2 (generated) | G6 / G6 |
| M9 | §11 recommendations (`11-conclusion.tex:14–44`) | §9 (label `sec:conclusion-recs` moves with them) | G4 |
| M10 | S8 table `tab:displays-unsafe` and its explanatory paragraph | `artifact/HISTORY.md` | G6 / G7 |
| M11 | S8 rules paragraph | S7.5 (J becomes a subsection of S7) | G6 |
| M12 | Checker paths, arguments and expected outputs of the register (`I-reproduction.tex:96–254`) | `artifact/RUNS.md`, one block per register row | G7 |
| M13 | Run records and history in S1, S5 (G5) and S2–S7 (G6) | `development/moves/r2-G5.md`, `r2-G6.md`, then `HISTORY.md`/`RUNS.md` | G5, G6 / G7 |
| M14 | README section "Round-1 reruns and checks" | `artifact/RUNS.md` (README keeps one pointer) | G7 |
| M15 | Superseded displays removed from S1 in round 1 without a home (`build-r3.md` §6 open item 3: earlier `lnts` dual, two earlier `dtoc5` bounds, the `optcdeg2` progression, the earlier `camshape` mpmath code), taken from `/workspace/local-home/paper-backups/paper-open-minlplib-r1-20261004-1841.tar` and `development/dossiers/dtoc5-optcdeg2.md` | `artifact/HISTORY.md` | G7 |

---

## 3. G1 front: `00-abstract`, `01-introduction`, `02-semantics`, `A-semantics`

### G1-01 AI-use disclosure in §2.6
- Sources: LD2-2; opus-referee 1; opus-claims 1; sol-referee (AI assessment: adequate; do not guess model identifiers).
- Severity: major. Decision: accept-modified. Reason: §2.6 and the declarations describe the agents' role differently and omit that agents devised the constructions and wrote the proofs; the records (Section 1) also show that agents selected the instances and ran the campaign and the audit. The sentence on what a person checked cannot be written by an editor (R2-13).
- Change: replace `02-semantics.tex:177–178` by

  > AI agents (Anthropic Claude and OpenAI GPT models), working under the authors' direction, selected the instances, devised the certificate constructions, wrote the proofs, implemented the computations and re-implemented them separately, checked code and proofs, ran the solver experiments and the audit, searched the literature and drafted the manuscript.
  > The project records do not identify the model of every session.
  > No person outside the authors has checked the code or the proofs.

  Keep the source comment that points to the declaration `\TODO` (G4-08 prints the confirmation request). Also `:169`: "inspection of the code showed" → "inspection of the code by an agent session showed" (combined with G1-07). Keep the common-mode paragraph (`:200–207`, edited by G1-04).
- Files: `sections/02-semantics.tex`.

### G1-02 "Separately written", the `ann_cumene_tanh` status and the shared readers
- Sources: opus-consistency 2 (major), 9; opus-claims 2, 13; opus-referee 5; opus-writing 14 (`:189`).
- Severity: major. Decision: accept-modified (opus-claims 2 definition and opus-consistency 2 status combined). Reason: by the current definition (`:184`) the `ann` second code is separately written, yet Table 1, §2.6 and the register treat it as an exception; the criterion actually applied is whether the second session read the certifying first code before its own results existed. `B6-powerflow.tex:303` confirms a separately written reader for `powerflow`.
- Change: replace `02-semantics.tex:182–189` by

  > The *first implementation* of a certificate is the code that produced it.
  > A *second implementation* was written later, in a separate agent session that received the statement to be checked, the model files and the stored inputs, and wrote its own code.
  > We call it *separately written* if it neither imports nor runs the first implementation in its checking computation and its session did not read the first implementation's certifying code before its own results existed, except to learn file formats (some second sessions ran or imported first code for side comparisons, which the records name and no certificate uses).
  > This is weaker than independent development.
  > The sessions shared one file system, and the verification records state where a second session read first code.
  > The session that wrote the second bounding code for \inst{ann_cumene_tanh} read the first in full (\cref{app:annkan-ann-verif}); that code is therefore not separately written, and the \inst{ann_cumene_tanh} bound has the status proved, not verified.
  > Three components are shared by both implementations: mpmath where \cref{tab:trust} lists it; one rigorous exponential and interval core used by both KAN bounding paths; and one OSIL reader, used by both implementations for [the eleven families of the current `:187`, unchanged].
  > Separately written readers reproduced its output exactly for \inst{powerflow}, \inst{waterno2}, \inst{ann_cumene_tanh} and the KAN instances, and further readers check the model data of the other families (\cref{app:families}).
  > Apart from these shared components, every computer-assisted dual certificate except that of \inst{ann_cumene_tanh} has at least two separately written implementations, which need not certify the same value (\cref{tab:trust}).

  Keep `:190–191`. Before inserting, check the new criterion against the verification records named in round-1 G1-01 (`research-20260929/reviews/wave3-verification/verification-report.md`, `wave2-small-verification/verification-report.md`, `waterno2-recheck.md`, `cops-verification/verification-report.md`) for every family that Table 1 marks verified. If a record shows that a second session read certifying first code before its own results existed, that family's status becomes proved: tell G6 (Table 1) and G7 (register). The names "authors' code" and "verifier's code" disappear here (G5-06, G6-10 rename them in the supplement).
- Files: `sections/02-semantics.tex`.

### G1-03 Status words, floating-point output, interpretation, the name `hand`
- Sources: opus-writing 14 (`:193`); opus-claims 12; sol-referee 8 (p. 10); opus-referee 11.
- Severity: minor. Decision: accept-modified. Reason: `:198` ("Interpretation, like numerical evidence, never supports a claim") is too broad; `:167` already restricts numerical evidence correctly, so only the interpretation half is kept. "Floating-point output" is used by Table 1 and the register but not defined.
- Change:
  - End the paragraph after `:193` (replay/regeneration); start a new paragraph with "We use three words for the status of a statement."
  - After `:197` add: "Solver output and published values are \emph{floating-point output}: we compare them with our results but never use them as premises."
  - Replace `:198` by: "Interpretation (\cref{sec:interpretation}) is labelled as such and is never used as a premise."
  - `:164`, after the definition of \evid{hand}, add: "(the name refers to the form of the proof, not to who wrote or checked it)".
- Files: `sections/02-semantics.tex`.

### G1-04 Common-mode paragraph
- Sources: sol-verify N1; opus-writing 14 (`:204`).
- Severity: minor. Decision: accept. Reason: `:203` omits the audit exceptions (360 `methanol50` and 30 `lop97icx` objective coefficients, `E-audit.tex:549–552`); `:204` nests two relative clauses.
- Change: `:203` → "Separately written readers reproduce the shared OSIL reader where stated, and for the 21 of the 43 instances whose GAMS and OSIL forms we compared exactly, the forms agree except for the \inst{catmix} coefficients (\cref{app:semantics-gams}; the audit comparisons and their exceptions are in \cref{app:audit-history})." `:204` → "MINLPLib's listed points have small residuals under our readers; a misread coefficient that matters at those points would make these residuals large."
- Files: `sections/02-semantics.tex`.

### G1-05 Remark 2.3(1) and the list of statements about other readings
- Sources: opus-claims 6; sol-verify N1, U1.
- Severity: minor. Decision: accept. Reason: Table A9 compares 17 instances exactly (21 with `catmix`) and 22 only at sample points (checked: 1+1+4+3+3+5 exact, 4 `catmix`, 16+6 evaluated = 43); the exception list at `:46` omits the audit's transfer to the GAMS forms (`07-audit.tex:59`, `E-audit.tex:538–543`).
- Change:
  - `:51` → as given in opus-claims 6: "Readings (a) and (b) define the same model for the 17 instances whose forms we compared exactly, and differ for the four \inst{catmix} instances, whose OSIL files print binary64 products such as \texttt{0.045000000000000005} in place of $9/200$; for the other 22, a comparison at sample points found no difference (numerical evidence; \cref{app:semantics-gams})."
  - `:46` → "The exceptions, each named where it occurs, are the transfer of the \inst{catmix} bounds to \reading{a} (\cref{prop:catmix-transport}), the statements about \reading{c} in \cref{rem:sem-readings}(2) and \cref{app:semantics-binary64}, the statements about binary64 data of small derived models in \cref{sec:solvers-invalid}, and the transfer of the audit refutations to the GAMS forms (\cref{sec:audit-hyp})."
- Files: `sections/02-semantics.tex`.

### G1-06 Floating-point closure terms
- Sources: opus-writing 2.
- Severity: major. Decision: accept-modified. Reason: the abstract, C1 and §3.4 use "floating-point closure" and "near-closure", which only the supplement defines (`D-literature.tex:15`, `:55`, "printed gaps of at most 0.01%"). The first clause follows the supplement's definition rather than the reviewer's, so that the two documents do not define the term twice in different words.
- Change: replace `02-semantics.tex:82` by

  > A solver run reaches a \emph{floating-point closure} if it reports optimality, or a gap below its tolerance, under its own feasibility tolerances, and a \emph{floating-point near-closure} if its printed relative gap is at most $10^{-4}$.
  > A floating-point closure is a \emph{tolerance-level closure} if, in addition, its dual bound is valid.
  > None of these is a closure in the sense of \cref{def:sem-certificate}; we credit them by name (\cref{sec:results-prior}).

  G2-05 points §3.4 to it; G6-07 replaces the supplement definitions by a pointer.
- Files: `sections/02-semantics.tex`.

### G1-07 Wording in §2.1–§2.5
- Sources: opus-writing 11, 12, 13, 30.
- Severity: minor. Decision: accept.
- Change:
  - `:117` → as given in opus-writing 11.
  - `:143` → "Dual bounds are rounded down and primal values up (reversed for maximization), so that each display is itself a valid bound."
  - `:152` "No proof of record assumes" → "No proof in this paper assumes".
  - `:161` "also pad library values of exponentials and integer powers" → "also widen library values of exponentials and integer powers by explicit error margins".
  - `:169` → "Every certificate proves its statement for \reading{b}: inspection of the code by an agent session showed that each certifying code reads the data exactly, as outward enclosures, or as correctly rounded binary64 values whose rounding its error analysis covers (the data readings of \cref{app:semantics-codes})."
  - `:60`, `:64`: "best listed dual" → "best listed dual bound" (definition and use). G7-08 updates `terminology.md`.
- Files: `sections/02-semantics.tex`.

### G1-08 Table 1 description (text side of G6-02)
- Sources: opus-referee 2(a), 12; sol-referee 7.
- Severity: minor. Decision: accept-modified. Reason: Table 1 becomes an upright compact table (G6-02); its data-reading and primal columns move to the full table `tab:trust-full` in S7.2 rather than to the register.
- Change: `:171` → "\Cref{tab:trust}, a reference for \cref{sec:split,sec:other,sec:points}, gives for each certificate family (a row of the table) the arithmetic and trusted primitives, the implementation that certifies the displayed dual bound and what the second one certifies, the status (\cref{sec:semantics-protocol}) and the evidence level; \cref{tab:trust-full} adds the data readings and the primal constructions." Keep `\input{tables/tab-trust}` where it is; check the float position in the private build.
- Files: `sections/02-semantics.tex`.

### G1-09 Abstract
- Sources: opus-referee 7; opus-writing 3; opus-claims 9, 13; sol-referee 4, 8; sol-verify U3.
- Severity: minor. Decision: accept-modified (all requests combined within 250 words, counted with `wc -w` on the source lines between `\begin{abstract}` and `\end{abstract}`; the text below has 250). Reason: "seven" reads as seven of the nine; "Our six … instances" suggests authorship; "we enclose their optima" refers to the infeasible stored models; the solver headline pools 30 non-comparable outputs (§8.3 separates them); the dtoc5 credit is for a copy; "archived" asserts an unverified deposit. The device list is shortened (sol-referee 8); the AI disclosure stays out of the abstract (R2-07).
- Change: replace `00-abstract.tex:5–14` by

  > MINLPLib lists tolerance-feasible points and solver-reported dual bounds and marks an instance solved when three solvers claim global optimality; none of these records is a proof.
  > We study 43 nonconvex instances without this mark, reading stored decimals as rationals and requiring exact feasibility.
  > For 31 instances we prove a dual bound and exhibit an exactly feasible point within a relative gap of at most \sci{3.1}{-9}; for nine we characterize the optimal value exactly, and for seven of the 31, floating-point closures or near-closures (one for a copy) had been reported.
  > For five pump-scheduling instances we raise the best listed dual bounds 1.68- to 6.21-fold (gaps at most 10.82\%); for \inst{ann_cumene_tanh}, whose variant \inst{ann_cumene_exp} has floating-point closures, we prove a bound with gap 0.195\%.
  > The six Kolmogorov--Arnold network instances in our set have no exactly feasible point; dropping their partition-of-unity rows, we enclose the optima within \sci{2.42}{-8}.
  > The certificates combine classical devices (Lagrangian duality, Sturm comparison, Taylor models) with exact or outward-rounded arithmetic; with named exceptions, separately written code rechecks them, sometimes only for a weaker bound or part of the domain.
  > Of MINLPLib's 11,086 per-solver dual bounds, we prove 22 invalid under a stated display hypothesis; four proved relative margins exceed 1\% and eleven are below $10^{-6}$.
  > A seed-dependent SCIP~10 error gives wrong optimal values on \inst{waterno2} subproblems.
  > All 79 same-model one-hour BARON, Gurobi and SCIP dual bounds with a globality guarantee were weaker than ours; BARON reached tolerance-level closures on two instances.
  > An archive holds code, certificates and points.
- Files: `sections/00-abstract.tex`.

### G1-10 §1 opening and §1.1
- Sources: LD2-1; sol-referee 1 (m3 not resolved), 8 (p. 2); opus-writing 6 (`:27`).
- Severity: major. Decision: accept-modified. Reason: the opening repeats the abstract and C1–C3; some headline numbers stay (round-1 R-10), the rest have one home in §1.3. `:28` calls every tolerance-based use an inherited error.
- Change:
  - `01-introduction.tex:6–11` →

    > We examine 43 nonconvex instances of the mixed-integer nonlinear programming (MINLP) library MINLPLib \citep{bussieck2003-minlpliba-collection-of-test-models,vigerske2014-minlplib-2} that the library does not mark as solved, and ask what can be proved about them when the stored decimal data are read as rational numbers and feasibility is exact.
    > For 31 of them we prove a dual bound and exhibit an exactly feasible point within a relative gap of at most \sci{3.1}{-9}.
    > Applying the same standard to the library's records and to solver output, we prove 22 listed per-solver dual bounds invalid under a stated hypothesis on how MINLPLib's pages display numbers, and we report a seed-dependent error in SCIP~10 (\cref{sec:intro-contrib}).
  - `:27` → as given in opus-writing 6 (three sentences).
  - `:28` → "Uses that need only tolerance-level reference values are consistent with these records. A conclusion about exact optimality is not: a gap measured against a listed point that is feasible only within a tolerance can compare a dual bound with a value below the optimum, and a reported bound can be invalid."
- Files: `sections/01-introduction.tex`.

### G1-11 §1.2 approach and observations
- Sources: opus-referee 3; opus-writing 4, 5, 10; opus-claims 4, 5, 10.
- Severity: minor. Decision: accept-modified. Reason: observation 1 says "little search remained" although `eg_disc2_s` has 1,114,361 leaves and `ex6_2_5` needed 131,111 boxes (`09-interpretation.tex:29–30`); its syntax is inverted (round-1 m7). Observation 3 says exact feasibility "changes the verdict" on bounds that are invalid under every tolerance (`07-audit.tex:59`), and "lose … for the tabulated ε" is unclear. The obs-1 text does not call all branching low-dimensional (outline §8 item 8; R2-17).
- Change:
  - `:54`: after "for some families only for a slightly weaker bound" add "or, for \inst{eg_disc2_s}, only on part of the domain".
  - Item 1 →

    > Once a bound fitted to the structure of the model was in place, branching was absent in 12 closures and at most three-dimensional in 15 more, although the \inst{ex6_2_5} bound needed 131,111 two-dimensional boxes; the \inst{pindyck} certificate splits one box into 9, and the three \inst{eg} certificates branch on their 7 original variables, with up to 1,114,361 leaves.
    > We do not test why general-purpose solvers did not find such bounds; \cref{sec:interpretation} offers an interpretation.
  - Item 3 →

    > Exact feasibility decides questions that tolerance-feasible data leave open.
    > Some listed dual bounds are invalid under every feasibility tolerance, which an exactly feasible point proves (\cref{sec:audit}).
    > Some listed and published optimal values hold only within tolerances, and along long chains of coupled rows a tolerance can lower the objective by far more than its own size: for \inst{camshape}, points that violate each row and bound by at most $\varepsilon$ lie at most $0.61\,n^2\varepsilon$ below the optimum (proved for the values $\varepsilon\le10^{-8}$ of \cref{tab:camshape-deficit}), and explicit tolerance-feasible points reach about 87\% of this bound (numerical evidence).
    > SCIP~10 returns wrong optimal values on some subproblems; in the 15 wrong runs that we traced, a binary64 residual of decimal data triggered the error (\cref{sec:solvers-invalid}).
- Files: `sections/01-introduction.tex`.

### G1-12 §1.3 contributions C1–C4
- Sources: opus-referee 2(b); sol-referee 1, 4, 8, 9; opus-writing 6 (`:74`, `:76`, `:80`), 7 (`:77`), 8, 10 (`:94`); opus-consistency 11; sol-verify N3, U3; LD2-3.
- Severity: major. Decision: accept-modified. Reason: C1–C4 run to about 1,100 words and restate the homes of the SCIP mechanism (§8.2), the CAMINO details (§8.2), the 79/109 split (§8.3), the 13 earlier-violating closures (§6.2) and the KAN widths (Theorem 5.17). The model-correspondence assumptions and "causes unknown" stay (sol-referee 8; R2-12). C2's "settles conflicts by proving that an exactly feasible point exists" no longer matches §7 (opus-consistency 11). C4's number-file promise is broader than the file (sol-verify N3), and "a public archive holds" asserts an unverified deposit (sol-verify U3).
- Change: replace `:73–104` by four items of at most about 10 printed lines each:

  > \item[C1 (certificates under exact semantics).]
  > For 31 instances that are not marked solved (snapshot of \cref{sec:semantics-model}) we prove a dual bound that is valid for every exactly feasible point of the stored OSIL model, and we exhibit an exactly feasible point within a relative gap of at most \sci{3.1}{-9} (\cref{tab:closures}).
  > They come from 14 instance families; 28 are continuous and three mixed-integer.
  > We chose the instances by judged tractability, so 31 is not a solve rate (\cref{sec:results-selection}).
  > For nine of them (\inst{camshape100}--\inst{camshape800}, \inst{hvycrash} and \inst{lnts50}--\inst{lnts400}) we characterize the optimal value exactly and prove that it is attained.
  > To our knowledge, within the search described in \cref{sec:intro-prior} and \cref{app:literature}, no rigorous certificate had been published for any of these 31 stored models.
  > For seven of them, floating-point closures or near-closures had been reported: for six on the same model, for \inst{dtoc5} on a copy under assumed variable bounds; \cref{sec:results-prior} credits these and the other earlier results by name.
  > For the five \inst{waterno2} instances we prove dual bounds 1.68 to 6.21 times the best listed ones, leaving relative gaps of at most 10.82\% (\cref{tab:unclosed}); we claim no priority for period decomposition.
  > For \inst{ann_cumene_tanh} we prove a dual bound within 0.195\% of an exactly feasible point; it applies verbatim to \inst{ann_cumene_exp}, which SCIP and LINDO closed in floating point \citep{vigerske2026-minlplib-a-library-of-mixed}, and is weaker than their values.
  > The six KAN instances in our set have no exactly feasible point (\cref{prop:kan-infeasible}); for the model $\RP$ without their partition-of-unity rows and its network relaxation $\Rnet$ we enclose the optimal values (\cref{thm:kan-enclosure}); these enclosures say nothing about points that satisfy the OSIL rows only within a tolerance.
  >
  > \item[C2 (audit of listed dual bounds).]
  > We screened all 11,086 per-solver dual bounds on MINLPLib's 1,633 instance pages against the 2,816 listed points.
  > Under a stated hypothesis on how the pages display numbers (\cref{hyp:audit-display}), we prove 22 listed bounds on 18 instances invalid: 19 on 15 instances from the screen, each proved again by a second implementation, and three LINDO bounds on \inst{rocket100}, \inst{rocket200} and \inst{rocket400} outside it.
  > Only \inst{rocket100} needs \cref{hyp:audit-display} itself; the other 21 refutations need only that each display arises from the reported number by decimal roundings or truncations (\cref{sec:audit-hyp}).
  > Four margins exceed 1\% of the displayed value and eleven lie below $10^{-6}$; no refutation contradicts a solved mark, and we attribute no cause.
  > MINLPLib~2 cross-checked dual bounds by agreement among solvers \citep{vigerske2014-minlplib-2}, and wrong solver bounds have been reported for individual instances \citep{nowak2008-lago-a-heuristic-branch-and,vigerske2017-scip-global-optimization-of-mixed}; to our knowledge, within the search of \cref{app:literature}, this is the first systematic screen of MINLPLib's listed per-solver bounds that refutes listed bounds only by proving that an exactly feasible point exists below them.
  >
  > \item[C3 (solver and published claims).]
  > SCIP 10.0.2, 10.0.3, 10.1.0 and a development snapshot \citep{hojny2025-the-scip-optimization-suite-10} return wrong optimal values on subproblems of \inst{waterno2_06} for some random seeds; exactly feasible rational witnesses, which SCIP~10.0.2's feasibility check accepts, refute these claims, and a reproducer with 15 variables shows the same error (\cref{sec:solvers-invalid}).
  > Assuming that CAMINO used the current MINLPLib files and recorded AMPL's \texttt{bestbound}, its bounds for Gurobi 13.0.0 on \inst{eg_disc2_s}, \inst{eg_disc_s} and \inst{eg_int_s} \citep{ghezzi2026-camino-benchmark-results-for-nonconvex} exceed the objective values of exactly feasible points by at least 4.33\%, 7.48\% and 80.5\%.
  > Assuming that the \texttt{.nl} file of QPLIB\_8803 encodes the MINLPLib model \inst{optcdeg2}, MINOTAUR~0.4.1's infeasibility report for it is contradicted by an exactly feasible point.
  > Both claims are invalid as recorded; the causes are unknown.
  > We also catalogue listed and published optimal values that no exactly feasible point attains (\cref{sec:solvers-tolerance}).
  > In one-hour runs of BARON 26.5.27, Gurobi 13.0.2 and SCIP 10.0.3 on all 43 instances, all 79 final dual bounds with a globality guarantee for the unmodified models of the non-KAN instances are weaker than our certified bounds, and so are the 30 other finite ones, which \cref{sec:solvers-campaign} qualifies; five improve the best listed dual bound.
  > Only BARON's runs on \inst{camshape100} and \inst{camshape200} ended with a relative gap of at most $10^{-6}$; they are tolerance-level closures (\cref{prop:baron-camshape}).
  > The runs check the status of current solvers on the stored models; they do not rank them.
  >
  > \item[C4 (reproducibility).]
  > The archive that accompanies this paper (\archiveDOI) holds the models with their SHA-256 hashes, the certificate data, the exact point definitions, the first and the separately written implementations, a number file with the exact value, source and rounding direction of every generated certified display (bounds, primal ends, gaps and derived margins), a claim register that maps each result to its checkers and inputs, and replay commands in three tiers of effort (\cref{sec:repro,app:repro}); it separates replay of stored certificates from regeneration, which may produce a different valid certificate (\cref{sec:semantics-protocol}).

  Keep `:69–70` (scope sentence). The dated tracker sentence (`:95`) and the SCIP cube mechanism (`:94`) leave C3; their homes are §8.2 (G4-04) and observation 3 (G1-11).
- Files: `sections/01-introduction.tex`.

### G1-13 §1.4 prior work: rigorous solvers, MIP certificates, mechanism list
- Sources: sol-referee 2 and its fresh assessment of p. 5; opus-referee 6; opus-writing 9; opus-claims 11.
- Severity: minor. Decision: accept-modified. Reason: `:123` implies that IbexOpt cannot certify equality-feasible points. The IbexOpt documentation (IBEX 2.9, `https://ibex-team.github.io/ibex-lib/optim.html`, read for this adjudication on 2026-10-04) says: "In the rigor mode, IbexOpt solves the original NLP, with strict equations", and returns a box such that "for some x inside we do have h(x)=0"; by default equations are relaxed to $|h(x)|\le\varepsilon_h$ ($10^{-8}$). The statement that its lower bounds would be "rigorous for the stored models" is not adopted, because IbexOpt reads binary64 data (R2-08). `:125`: Hoen and Gleixner check rather than certify. The mechanism list (`:128`) is long; credit moves to S3.1 (M7).
- Change:
  - `:122–123` →

    > Current interval solvers such as IbexOpt combine reliable affine and Taylor relaxations and certify LP-derived lower bounds by interval post-processing \citep{araya2025-hybridizing-two-linear-relaxation-techniques}.
    > By default IbexOpt relaxes equality rows by a tolerance; in its rigor mode it returns a box that is proved to contain a point satisfying the equalities exactly \citep{ibex2026-ibexopt-ibex-documentation}.
    > We did not run such a solver, because this study builds instance-specific certificates rather than comparing methods; its lower bounds would be a natural rigorous baseline for ours, and whether they reach our bounds on these instances is open.
  - `:125`: "these certify linear MIP results" → "these certify or check linear MIP results".
  - `:128` → "Every mechanism in our certificates is classical: [the mechanism names of the current sentence, in the same order, without citations]; \cref{app:literature-scope} gives the references." Keep `:129–131`. G6-07 adds the full citation sentence to S3.1; G6-08 adds the bib entry.
- Files: `sections/01-introduction.tex`.

### G1-14 §1.5 Organization
- Sources: LD2-1 (merge of §9 and §11).
- Severity: minor. Decision: accept.
- Change: `:135` → "… \cref{sec:audit,sec:solvers} the audit and the solver and published claims, \cref{sec:interpretation} an interpretation and recommendations, and \cref{sec:repro,sec:conclusion} reproduction, limitations and conclusions." Keep `:136`.
- Files: `sections/01-introduction.tex`.

### G1-15 Appendix A
- Sources: opus-referee 1(c); opus-writing 30; opus-consistency 12; consequence of G6-02.
- Severity: minor. Decision: accept.
- Change:
  - `A-semantics.tex:34` → "An agent session inspected every code that certifies a dual bound or a primal point and recorded how each numeric string $\sigma$ enters it."
  - `:36–40`: "an \emph{exact} reading" → "an \emph{exact data reading}", likewise outward, rounded and binary64.
  - `:43`: "(\cref{tab:trust})" → "(\cref{tab:trust-full})".
  - `:104` → "Every class~(i) margin is still at least $1.115\,\dunit{s}$, where …" (the value of `E-audit.tex:559`; the sentence keeps "computed, one implementation").
  - Trim repetition so that Appendix A stays at or below 3.3 pages; no new content.
- Files: `sections/A-semantics.tex`.

---

## 4. G2 results and split: `03-results`, `04-split`, `G-proofs-split`, figures

### G2-01 Explanatory split results leave the main PDF
- Sources: LD2-1; sol-referee 1 ("reduce the unused affine-slope and cellwise-maximality results to cross-references"; round-1 m10 "not resolved").
- Severity: major. Decision: accept-modified. Reason: no certificate uses Prop. 4.3(c) or the last statement of Prop. 4.5 (`04-split.tex:90`, `:122`); together with their proofs in Appendix B they cost about 1.7 main pages. Destination: the supplement (M1, M2), where statements and proofs stay complete.
- Change:
  - `04-split.tex`: delete item (c) of `prop:split-affine` (`:83–85`). Replace `:89–90` by: "Exact affine slopes are not free: at a minimizer whose bags are interior they are the copy-row multipliers, and after the dynamics rows are eliminated they are the discrete costates (\cref{prop:split-forced}, explanatory). The affine certificates below take their slopes from a local KKT point; validity never depends on this choice." Keep `:91`.
  - Delete the last sentence of `prop:split-cellwise` (`:118`, "If, in addition, …"). Replace `:122` by: "With exact pair bounds on a partition, $\mathrm{SP}$ is also the largest bound that cellwise-affine splits with these slopes give (\cref{prop:split-cellwise-best}, explanatory)." Keep `:121`.
  - `G-proofs-split.tex`: delete part (c) of the proof of `prop:split-affine` and the paragraph after the proof ("Unrolled, … This is explanatory; no certificate uses it."); delete the "Best constants" part of the proof of `prop:split-cellwise` and the closing remark on the cap. Keep the validity proofs. G5-02 inserts the deleted statements and proofs.
  - Appendix B target: at most 3.0 pages.
- Files: `sections/04-split.tex`, `sections/G-proofs-split.tex`.

### G2-02 §4 certificate sentences without tiers
- Sources: opus-referee 2(f), 8; opus-consistency 1 (major); opus-writing 16, 19; opus-consistency 13 (rejected, R2-05).
- Severity: major. Decision: accept-modified. Reason: tiers are used in §§4–5 before §10 defines them, and §4.6 still prints the pre-revision waterno2 tier (Tier 3 for all searches; Table 7, the S1.8 box, the register and the README give Tier 2 for `waterno2_09` and `waterno2_12`). Deleting the tier clauses fixes both; tiers keep one home in Table 7 and the boxes. Times go with the tiers.
- Change: in each certificate sentence keep arithmetic, displayed bound, second implementation and evidence level, in the form "In the certificate (\cref{…}), …; its evidence level is \evid{…}."
  - `:167`, `:209`, `:236`, `:255`: delete ", and it replays in Tier~1".
  - `:272` → "The bounds have evidence level \evid{rerun}, since the per-stage chord values are not stored; the points have level \evid{stored} (exact rational state evaluation)."
  - `:297–298` → "In the certificate (\cref{app:lukvle10-proof}), one code gives the displayed bound and a separately written one certifies 352.238025369202; both use interval arithmetic \arith{I} with \texttt{mpmath}'s interval $\exp$ and $\log$, and the evidence level is \evid{rerun}."
  - `:324` → "Its evidence level is \evid{rerun}, because the search trees are not stored."
  - `:320`: "(\cref{sec:repro})" → "(\cref{app:repro-regen})" (the regenerated values move there, M6).
- Files: `sections/04-split.tex`.

### G2-03 §3.1 Selection
- Sources: opus-writing 1 (major); opus-referee 10; opus-claims 3.
- Severity: major. Decision: accept-modified. Reason: `:42` says all 43 instances come from the 155, but two do not (`D-literature.tex` funnel: 12 others among the 155, 2 closures outside it); "census" is undefined in the main text. Whether the three counting programs are separately written in the §2.6 sense must be checked (opus-claims 3; the records show at least one, `development/dossiers/pattern-theory.critique.md:54`, "own code (recount.py)").
- Change: replace `03-results.tex:42–44` by

  > Of our 43 instances, 41 lie among the 155 nonconvex instances that are open by a selection rule stricter than MINLPLib's (\cref{app:literature-funnel} gives the rule, the funnel and its caveats).
  > We chose the 43 in two rounds by judged tractability, the first 11 before the rule was fixed, so the 29 closures among the 155 are not a solve rate.
  > The other two closures, \inst{camshape100} and \inst{lnts50}, are not open by that rule, because their best listed dual bounds were already within \sci{1.22}{-6} and \sci{3.9}{-5}, relative, of the best listed points and of our proved optima; for them what is new is the exact optimal value, its proof and an exactly feasible point.
  > [Three separately written programs] reproduce every count of the funnel from the saved page and width data; no separate agent session reviewed the code that computed the widths and applied the rule.

  Write "separately written" only if the records show three agent sessions whose code fits the §2.6 definition; otherwise write what the records show (for example "Three programs, two of them from separate agent sessions"). Tell G6 the result for `D-literature.tex:290` (G6-07).
- Files: `sections/03-results.tex`.

### G2-04 §3.2 Stored data of the rerun closures
- Sources: sol-referee 3; opus-referee 4; opus-consistency 8; opus-claims 7.
- Severity: minor. Decision: accept. Reason: `:51` says no search tree is stored for the 14 rerun closures, but the `eg` leaf partitions are stored and checked (`02-semantics.tex:165`, `B7-eg.tex:275`, `I-reproduction.tex:201`).
- Change: `:51` → as given in opus-claims 7: "For the 14 closures at evidence level \evid{rerun} (\cref{tab:trust}), the per-leaf or per-stage certificate data are not stored, so a check reruns the search or the stage computation; for the three \inst{eg} instances the leaf partition is stored and its coverage is checked exactly."
- Files: `sections/03-results.tex`.

### G2-05 §3 opening, class glosses and prior status
- Sources: LD2-1 (opening summaries); opus-writing 2, 15, 30.
- Severity: minor. Decision: accept.
- Change:
  - Delete `:15` ("We first explain how we chose the 43 instances.").
  - `:53` → as given in opus-writing 15.
  - `:64` → "…, and \cref{thm:kan-enclosure} encloses the optimal values of two related models, $\RP$ and its network relaxation $\Rnet$ (\cref{tab:kan})."
  - `:70` → "Seven closures have prior status \emph{fp closure} or \emph{fp near-closure} (\cref{sec:semantics-cert}): a floating-point closure or near-closure was reported for the same model, or, for \inst{dtoc5}, for a copy under assumed variable bounds."
  - `:76`: "\emph{listed solve} (a benchmark page lists a solver as solving the instance or a copy, without a value or log that we can check)".
  - `:43`, `:55`, `:56`: "best listed dual" → "best listed dual bound".
- Files: `sections/03-results.tex`.

### G2-06 §4 wording
- Sources: opus-writing 17, 18; LD2-1 (opening summary of §4).
- Severity: minor. Decision: accept.
- Change:
  - `04-split.tex:222–223` → as given in opus-writing 17.
  - `:247` → as given in opus-writing 18.
  - `:10–15`: shorten so that the opening defines the staged class and the split idea once; the list of the 15 instances and the `catmix` variant stay, the repetition of observation 2 goes.
- Files: `sections/04-split.tex`.

### G2-07 Unused figure
- Sources: opus-consistency 16(c).
- Severity: minor. Decision: accept-modified (remove; do not add it to S1.3, R2-10).
- Change: if `figures/make_fig_camshape.py` produces only `fig-camshape-profiles.pdf`, move both to `development/unused-figures/`; otherwise remove only that output from the script and move the PDF. Check that no source includes it.
- Files: `figures/`.

---

## 5. G3 other, points, audit: `05-other`, `06-points`, `07-audit`

### G3-01 §5 certificate sentences without tiers, in one style
- Sources: opus-referee 2(f), 8; opus-writing 19; opus-consistency 13 (rejected, R2-05).
- Severity: minor. Decision: accept-modified (same rule as G2-02).
- Change:
  - `:67` → "In the certificate (\cref{app:camshape-proof}), (K1)--(K6), $v_n$ and every row at $(E,d^E)$ are evaluated in \arith{E} without branching, and three separately written codes with their own readers (two exact, one with directed rounding) agree on $v_n$ to all printed digits; its evidence level is \evid{hand}+\evid{stored}."
  - `:118–119` → "For \inst{ex6_2_5} and \inst{ex6_2_7} the displayed bounds come from one code, and a separately written code certifies slightly stronger ones; their evidence level is \evid{rerun}. For \inst{pricing050} two codes reproduce the bound and one code checks the point; its evidence level is \evid{stored}."
  - `:217` → "Both certificates have evidence level \evid{stored} (\cref{app:small-etamac,app:small-pindyck})."
  - `:175`, `:248`: G3-03, G3-04.
- Files: `sections/05-other.tex`.

### G3-02 Powerflow sketch: angle rows of the stored 0039p certificate
- Sources: sol-verify U5.
- Severity: minor. Decision: accept. Reason: the sketch defines leaf relaxations from $\mathcal Q$, which omits the angle rows (`:128`), but the stored `powerflow0039p` multipliers weight angle rows; the full proof applies the proposition on $\mathcal Q_i^\angle$ (`B6-powerflow.tex:216`, checked).
- Change: replace `:168–169` by "On leaf $i$, add to $\mathcal Q$ the box $B_i$ and four rows $W_{2,2}\le H$ with $H\ge F$ at the eight vertices of $B_i$ (checked exactly); by \cref{lem:pf-leaf,lem:pf-planes} every exactly feasible point lies in one of these leaf relaxations. \Cref{prop:pf-duality} applies verbatim to them, with each leaf's stored multipliers and a rational shift $\varepsilon_i$; for \inst{powerflow0039p}, whose stored multipliers also weight the angle rows, the leaf relaxations keep these rows (\cref{app:powerflow-0039})." Keep `:170–172`.
- Files: `sections/05-other.tex`.

### G3-03 Powerflow readers
- Sources: opus-referee 5; opus-consistency 9.
- Severity: minor. Decision: accept. Reason: "with two separately written readers" contradicts §2.6 (one shared reader); `B6-powerflow.tex:303` names a separately written reader and row builder.
- Change: `:175` → "In the certificate (\cref{app:powerflow-verification}), both implementations share one OSIL reader, whose rows a separately written reader reproduced exactly; the first implementation's replay and a separately written exact replay, both in \arith{E}, reproduce or exceed every bound; the evidence level is \evid{stored}."
- Files: `sections/05-other.tex`.

### G3-04 hvycrash checks
- Sources: opus-writing 20.
- Severity: minor. Decision: accept.
- Change: `:248` → as given in opus-writing 20.
- Files: `sections/05-other.tex`.

### G3-05 eg sentences
- Sources: opus-consistency 6; opus-writing 21.
- Severity: minor. Decision: accept-modified. Reason: S1.7 reports median-gap ratios 3.2, 44, 112, 146 and 151 at relative widths 0.3 to 0.003 (`B7-eg.tex:287`, checked); the main text drops 3.2. `:281` crosses the defined words "first" and "second".
- Change:
  - `:267`: "on sampled boxes, bounds that add up the term ranges were 44 to 151 times looser" → "on sampled boxes, bounds that add up the term ranges had median gaps 3.2 to 151 times larger, the ratio growing as the boxes shrink".
  - `:281` → as given in opus-writing 21.
- Files: `sections/05-other.tex`.

### G3-06 ann and KAN sentences
- Sources: opus-claims 2 (consequence), 8; opus-writing 22.
- Severity: minor. Decision: accept.
- Change:
  - `:296`: "(the second does not import the first, but the session that wrote it read it in full; …)" → "(the session that wrote the second code read the first in full, so the second is not separately written in the sense of \cref{sec:semantics-protocol}; \cref{app:annkan-ann-verif})".
  - `:317` → as given in opus-writing 22.
  - `:330` → as given in opus-claims 8.
- Files: `sections/05-other.tex`.

### G3-07 §6 wording
- Sources: opus-writing 7 (`06:6`, `06:66`), 30 (`06:69`); opus-referee 11.
- Severity: minor. Decision: accept.
- Change: `:6` and `:66` as given in opus-writing 7; `:69` "As far as we found (\cref{app:literature})" → "To our knowledge, within the search of \cref{app:literature}"; `:78` "the existence proof is by hand" → "the existence proof is a written proof (evidence level \evid{hand})". Keep `:68` (its duplicate in the Table 5 caption goes, G6-03).
- Files: `sections/06-points.tex`.

### G3-08 §7 consolidation, wording and witnesses
- Sources: opus-referee 2(d); opus-writing 23, 24; LD2-3; sol-referee 9.
- Severity: major. Decision: accept-modified. Reason: the class (i-r), `emfl` and `rocket` paragraphs and §7.5's aggregate paragraph repeat S4.1 and S4.4–S4.6. The folded text keeps the qualifiers that support "no refutation contradicts a solved mark" and the (i-r) caveat.
- Change:
  - `:28` → as given in opus-writing 23.
  - `:60`, `:69`, `:79` → as given in opus-writing 24.
  - Replace `:89–101` (M4) by one paragraph:

    > \paragraph{Other classes and \inst{rocket}.}
    > The 12 class (i-r) bounds, on four instances, date from 2013-09-17; for \inst{spring} page rounding explains them (\cref{prop:spring-opt}), while the six-digit bounds on \inst{eniplac}, \inst{lop97icx} and \inst{stockcycle} are invalid by far more than the display rounding if stored as displayed, which an unproved rounding to six digits before storage would explain (\cref{app:audit-spring}).
    > For the four \inst{emfl} instances, exact enclosures checked by two implementations prove every listed dual bound valid, and the best listed primal values are tolerance artifacts (category~A); the solved mark of \inst{emfl050_3_3} rests on tolerance-feasible points, and we do not call it wrong (\cref{prop:emfl-enclosure}).
    > On \inst{rocket100}, \inst{rocket200} and \inst{rocket400}, LINDO's bounds form display ties with the only listed point; exactly feasible points prove them invalid under Hypothesis~H by 1.06, 4.70 and 18.9 display units, and two implementations agree (\cref{app:audit-rocket}).
    > Of the 22 bounds on 18 instances proved invalid under Hypothesis~H, 16 are LINDO's (one per instance).
  - Replace `:110–112` (M5) by: "MINLPLib's aggregate values, the dual bound in the instance list and the \texttt{=bestdual=} entry of the \texttt{.solu} file, agree with every proved point, except the six-digit (i-r) entries in the instance lists of \inst{eniplac} and \inst{stockcycle}, which only the unproved six-digit rounding explains; no solved mark is contradicted (\cref{app:audit-screen})." G6-06 moves the full statement into S4.1.
  - Add at the end of §7.5 (LD2-3): "The exactly feasible points and existence certificates behind the 22 refutations are in the archive (\cref{app:audit-existence}); communication with the MINLPLib maintainer is pending at the time of writing."
- Files: `sections/07-audit.tex`.

### G3-09 §5 opening glosses (optional)
- Sources: opus-writing 15 (`05:9`, optional).
- Severity: minor. Decision: accept, only if it does not lengthen §5: put each class gloss before its instances.
- Files: `sections/05-other.tex`.

---

## 6. G4 end: `08-solvers`, `09-interpretation`, `10-reproducibility`, `11-conclusion`

### G4-01 §8 opening
- Sources: sol-referee 4; opus-claims 9; opus-writing 8 (`08:25`).
- Severity: minor. Decision: accept-modified (sol-referee's comparable count leads; the KAN qualifier of opus-claims 9 is kept).
- Change: `:22` "both floating-point values" → "both floating-point output (\cref{sec:semantics-protocol})"; `:25` → "In one-hour runs, all 79 finite final dual bounds with a globality guarantee for the unmodified non-KAN models were weaker than our certified bounds, and so were the other 30, which \cref{sec:solvers-campaign} qualifies; only BARON's two optimality claims ended with a relative gap of at most $10^{-6}$ (\cref{sec:solvers-campaign})."
- Files: `sections/08-solvers.tex`.

### G4-02 Proposition 8.1
- Sources: opus-referee 13; opus-writing 25 (lead-in, rejected R2-06).
- Severity: minor. Decision: accept-modified (text as given; no lead-in sentence, for length). Reason: (a) and (b) state the same gap once as relative, once as absolute; the reviewer's distances were checked in rational arithmetic (opus-referee §2: $5.258\cdot10^{-7}$ and $1.227\cdot10^{-7}$; $2.053\cdot10^{-6}$ and $4.798\cdot10^{-7}$).
- Change: `:31–32` → as given in opus-referee 13.
- Files: `sections/08-solvers.tex`.

### G4-03 §8.1 and §8.3 sentences
- Sources: opus-writing 25 (`:44`, `:135`).
- Severity: minor. Decision: accept.
- Change: `:44` and `:135` as given in opus-writing 25.
- Files: `sections/08-solvers.tex`.

### G4-04 §8.2: move the reproducer proposition and the cube lemma; upstream; witness checkers
- Sources: opus-referee 2(c), 14; sol-referee 9; LD2-3; opus-claims 3; opus-writing 25 (`:103`).
- Severity: major. Decision: accept-modified. Reason: Box 2 and Observation 8.5 carry the mechanism; Prop. 8.3 and Lemma 8.4 with their notes cost about 0.5 page (M3). The dated tracker sentence must not read as proof of absence. The "six to eight separately written checkers" are eight code bases from fewer sessions (`research-20260929/publication/scip-bug/report.md` §4 table: authors "first", "second", "third"; `development/dossiers/solvers.md:526–533`: the reviewer's two checkers, the earlier draft's and the dossier's).
- Change:
  - Delete `:75–91` (Prop. 8.3, the note after it, Lemma 8.4 and its note); G6-05 inserts them in S6.6 with unchanged labels. In their place: "The reproducer \inst{fm336} has optimal value $187/270$, and SCIP's values for it are wrong in three senses: they exceed the optimal value of the decimal model, they are inconsistent with SCIP's own tolerances, and in the binary64 model the returned points are infeasible (\cref{prop:scip-reproducers}). The trigger is a rounding fact: $\fl(0.7)^3$ lies strictly below $\fl(0.343)$, although $0.7^3=0.343$, while the other station values of \inst{waterno2} show no such gap (\cref{lem:scip-cube})."
  - `:72`: "confirmed for each witness by six to eight separately written checkers, two of which read the GAMS files" → "confirmed for each witness by six to eight exact checkers (eight code bases from six agent sessions; two of them read the GAMS files; \cref{app:solvers-scip})". Check the session count against the two records above before inserting; if it cannot be established, write "eight code bases written in several agent sessions".
  - `:103` → as given in opus-writing 25.
  - `:107–108` →

    > Wrong results of global solvers \citep{…} and rounding errors in the branch-and-bound decisions of MIP solvers \citep{…} have been reported before, and propagation that accounts for rounding, so that it discards no feasible point, is classical \citep{…}.
    > A search of SCIP's public issue tracker on 2026-10-02 found no report of this defect in the nonlinear propagation of SCIP's expression framework \citep{…}; the search does not show that no report exists.
    > The archive contains the minimal reproducer \inst{fm336} with its exact witness and the other witnesses (\cref{app:solvers-scip}); communication with the SCIP developers is pending at the time of writing.

    (Same citation keys as now.)
- Files: `sections/08-solvers.tex`.

### G4-05 §8.3 GAMS and OSIL forms
- Sources: opus-claims 6.
- Severity: minor. Decision: accept.
- Change: `:146` → "The solvers ran the GAMS files and the certificates concern the OSIL files; the two forms are identical or agree at sample points (\cref{tab:sem-gams}), and for \inst{catmix}, whose coefficients differ in the last digits, \cref{prop:catmix-transport} transfers the certified bounds."
- Files: `sections/08-solvers.tex`.

### G4-06 Merge the interpretation and the recommendations; §9 contents
- Sources: LD2-1; sol-referee 1; opus-referee 2(f) (§9.1), 9; opus-writing 10 (`11:22`), 26, 28 (`11:16`, `:39`, `:41`); opus-consistency 6 (`11:41`).
- Severity: major. Decision: accept-modified. Reason: §9 and §11.1 repeat the observations and examples of §§1, 5 and 8; one shorter section keeps the interpretation caveats and the "untested proposal" label. §9's opening sentence holds by construction (opus-referee 9; the replacement holds: the closest listed duals are 1.22·10⁻⁶ for `camshape100` and 3.9·10⁻⁵ for `lnts50`).
- Change:
  - `09-interpretation.tex`: title `\section{Interpretation and recommendations}`, label `sec:interpretation` unchanged. Opening (`:18–20`) →

    > For none of the 31 instances of \cref{tab:closures} did a listed dual bound come within $10^{-6}$, relative, of the optimum; the certificates of \cref{sec:split,sec:other} did.
    > Our interpretation, which we did not test by experiment, is that termwise relaxations cannot see the structure that each certificate uses: free states along long chains of nonconvex equalities, hidden convexity or monotonicity, and cancellation among many terms.
    > We did not rerun any solver with our derived enclosures added as variable bounds, or on the reformulations that the certificates use; no certificate depends on this section, and its recommendations (\cref{sec:conclusion-recs}) are untested proposals.

    Keep `:21` (termwise relaxation).
  - §9.1 (`:25–30`): keep the staged-chain sentence, the 6-of-14-families sentence and the per-instance branching dimensions (`:27`); delete what observation 1 of §1.2 now states (pindyck boxes, eg leaves, the 131,111 boxes).
  - §9.2: keep; shorten where it repeats §8.3.
  - §9.3: `:48` delete the clause after the semicolon; `:57` "each bag is a period" → "each stage is a period".
  - New §9.4 `\subsection{Recommendations}\label{sec:conclusion-recs}` with the text of `11-conclusion.tex:16–44` (M9), edited: `:16` "The recommendations below are proposals; precedents …"; `:22` → as given in opus-writing 10; `:39` → "\emph{Exploit stage structure, and keep cancellation when bounding sums of many similar terms.} This proposal is untested; for circumstantial evidence see \cref{sec:interpretation-evidence}."; `:41` "were much looser than" → "had median gaps 3.2 to 151 times larger than". Remove repetitions of §§5, 7 and 8 where a cross-reference suffices.
  - Target: §9 at most 1.6 pages including §9.4.
- Files: `sections/09-interpretation.tex`, `sections/11-conclusion.tex`.

### G4-07 §11 Limitations and conclusion
- Sources: sol-referee 3; opus-referee 3, 4; sol-verify U1; opus-writing 5, 28 (`:53`); opus-claims 4, 5.
- Severity: minor. Decision: accept-modified (opus-claims 4/5 and opus-referee 3 combined).
- Change:
  - `11-conclusion.tex:12` → `\section{Limitations and conclusion}\label{sec:conclusion}`; §11 keeps `sec:conclusion-limits` and `sec:conclusion-open`; target 0.7 page before the declarations.
  - `:51` → "Replay was run on one machine. The \evid{rerun} certificates store no per-leaf or per-stage certificate data; apart from the \inst{eg} leaf partitions and the saved node counts from which the \inst{ann_cumene_tanh} replay reconstructs its partition, their search partitions are not stored either."
  - `:53` → "Unless a statement names another reading, the claims concern \reading{b} of the stored OSIL files (\cref{sec:semantics-model} names the exceptions), and statements about listed data concern the pages fetched on the dates of \cref{sec:semantics-model}; \cref{rem:sem-readings} states what transfers to the GAMS text and to the binary64 data that solvers read."
  - `:65` → "First, once a bound fitted to the structure of the model was in place, the remaining branching was low-dimensional for 27 of the 31 closures; we have only interpreted, not tested, why general-purpose solvers did not find such bounds (\cref{sec:interpretation})."
  - `:67` → "Third, proving exact feasibility settled conflicts among listed bounds and changed the verdict on listed points and solver claims often enough that benchmark values should carry their data semantics, their provenance and, where possible, a certificate that others can check."
- Files: `sections/11-conclusion.tex`.

### G4-08 Declarations: AI use and data availability
- Sources: LD2-2; opus-referee 1; opus-claims 1; sol-verify U3.
- Severity: major. Decision: accept-modified (same wording as G1-01; the confirmation placeholder stays).
- Change:
  - `:76–79` →

    > \paragraph{Use of AI tools.}
    > AI agents (Anthropic Claude and OpenAI GPT models), working under the authors' direction, selected the instances, devised the certificate constructions, wrote the proofs, implemented the computations and re-implemented them separately, checked code and proofs, ran the solver experiments and the audit, searched the literature and drafted the manuscript.
    > \Cref{sec:semantics-protocol} states how the implementations were produced and checked.
    > The authors take full responsibility for the content.
    > \TODO{authors to confirm, here and in \cref{sec:semantics-protocol}, including which proofs and code the authors checked themselves}
  - `:72` → "Code, certificate data, exact point definitions, logs, the number file and the claim register form the archive that accompanies this paper; it will be deposited at \archiveDOI{} under \TODO{licence of the archived code and data}." Keep `:73–74`.
- Files: `sections/11-conclusion.tex`.

### G4-09 §10 Reproducibility
- Sources: sol-verify N2, N3, U3; opus-writing 27; opus-referee 2(e); opus-consistency 14.
- Severity: minor. Decision: accept.
- Change:
  - `:28` → "All certificates, points, checkers and logs are in the archive that accompanies this paper (\archiveDOI)."
  - `:30` → "A number file stores, for every generated certified display (bounds, primal ends, gaps and derived margins), its exact value or certificate end, its source and the rounding direction; run times and fixed metadata come from the run records and the claim register (\cref{app:repro})."
  - `:36` → as given in opus-writing 27.
  - `:39–42` (M6) → "Regeneration also reruns the numerical steps that produced the stored inputs (local solves, SDP and LP solves, solver-derived targets, time-limited searches) and may give a different valid certificate; for \inst{waterno2_18}, \inst{waterno2_24}, \inst{powerflow0030p} and the \inst{topopt-cantilever_60x40_50} point of the audit it does, the reported values rest on the stored certificates, and \cref{app:repro-regen} gives the regenerated values." G6-09 makes S7.4 hold every number deleted here.
  - Table 7 (N2): split the KAN enclosures by the per-instance rule of `:45`: the three `r3` models in Tier 1 and the three `r5` models in Tier 2, if every code's recorded wall time for an `r3` model is under 10 minutes (guarded replay 24.74, 22.71 and 58.86 s, `development/reviews/round1/kan-guard/report.md`; first implementation and the unguarded original: the register and the logs in G7-03). If a time is missing, keep Tier 2 and add to the caption that a result takes the tier of its slowest code. Use the same assignment as the register, the S1.9 box and the README.
  - Table 7, `eg_disc2_s` cell → "\inst{eg_disc2_s} (audited re-certification of the stored leaves, 4.1\,h over eight parts; regenerating its search took about 3.4 CPU-hours)".
- Files: `sections/10-reproducibility.tex`.

---

## 7. G5 supplement certificates: `B0`–`B9`, `F`, new `B10`

### G5-01 Consolidate S1 and S5
- Sources: LD2-1; sol-referee 1 ("the supplement still combines derivations with implementation histories, command mappings and superseded displays"), round-1 item 10 ("repeated verification summaries … in the family descriptions and supplement boxes"); opus-consistency 16(f).
- Severity: major. Decision: accept-modified (target 66 pages for S1 and S5 together, including the new S1.10).
- Change, in this order, with the estimated savings:
  1. Listed status and prior results (`B1:20`, `B1:122`, `B3:44`, the prior-work half of `B3:291`, `B6:58`, `B6:309`, `B7:69`, and the listed-status parts of the model subsections of B2 and B8): one sentence pointing to S3.2 and Table 2, unless an argument uses the listed data (B0 already says "we repeat them only where an argument uses them"). About −1.5 pages.
  2. One home per verification statement, the certificate box: delete prose that restates a box field (for example `B4:216` "Arithmetic and implementations", `B4:391`, `B4:396`, `B4:487` "Checks of the proofs and prior work", `B5:196`, the run details of `B7:234` and `B7:260`, `B8:267`, `B9:312`). Run records (timings beyond the box's replay field, machine load, job counts, log names, aborted, earlier or repeated runs) go to `development/moves/r2-G5.md` for `RUNS.md`; history (earlier codes, earlier bounds, the unguarded-to-guarded history beyond the sentence of G5-04, "an earlier interval branch and bound of ours") goes there for `HISTORY.md`. About −3.5 pages.
  3. Numerical-evidence paragraphs (`B2:263`, `B7:283`, `B4:435`): keep the numbers that the main text cites (for example the 0.6258 `optcdeg2` affine gap, the `chain` value 4.77, the 3.2–151 ratios, `fig:eg-enclosures`) and their labels as evidence; move exploratory run details to the moves file. About −1.2 pages.
  4. Model restatements: where a subsection restates a model that §4 or §5 already states, replace it by a cross-reference and keep only the data the proofs use. About −1.5 pages.
  5. S5 (`F-eg-rounding.tex`): keep the setting, hypotheses, rounding facts, the proof of `lem:eg-padding`, what the auditor checks and the trust statement; move job lists, timings and partial-run records of S5.4–S5.5 to the moves file. About −1.5 pages.
  6. Line-level tightening (repeated "separately written" sentences, repeated cross-references). About −2 pages.
  Every lemma, proposition, theorem, proof, hypothesis and certificate box stays. Report the page counts per subsection after the private build.
- Files: `sections/B0-families.tex`–`B9-ann-kan.tex`, `F-eg-rounding.tex`, `development/moves/r2-G5.md`.

### G5-02 New S1.10: explanatory results on splits
- Sources: LD2-1 via G2-01 (moves M1, M2).
- Severity: major. Decision: accept.
- Change: create `sections/B10-split-extras.tex` with `\subsection{Two explanatory results on splits}\label{app:split-explanatory}`, one opening sentence ("No certificate uses these results; they explain why the certificates choose their slopes as they do."), then
  - Proposition (forced slopes), label `prop:split-forced`: the statement of the deleted part (c) of `prop:split-affine`, made self-contained ("Let $\varphi$ be an affine split as in \cref{prop:split-affine}. Suppose $B(\varphi)=\vstar$, …"), followed by the deleted proof of (c) (it uses part (b) of \cref{prop:split-affine}) and the "Unrolled …" paragraph;
  - Proposition (best constants), label `prop:split-cellwise-best`: the deleted last statement of `prop:split-cellwise` with its hypotheses, followed by the "Best constants" proof and the remark on the cap.
  Text verbatim from the r3 tar (`04-split.tex`, `G-proofs-split.tex`), with cross-references to main-paper labels. Add `\input{sections/B10-split-extras}` after `B9-ann-kan` in `supplement.tex` (the only change to that file).
- Files: `sections/B10-split-extras.tex` (new), `supplement.tex`.

### G5-03 QPLIB thresholds in S1.3
- Sources: sol-verify U2; opus-consistency 4.
- Severity: minor. Decision: accept. Reason: `B3-camshape.tex:289` calls the round-to-nearest thresholds the upper ends of all numbers that display as the reported values; `H-solvers.tex:108–118` uses one-unit thresholds. Checked: −4.2842974 > −4.284301 and −4.2771732 > −4.2773, so the inequality still holds.
- Change: `:289` → as given in opus-consistency 4.
- Files: `sections/B3-camshape.tex`.

### G5-04 S1.9: KAN guard, KAN tiers, `ann` wording
- Sources: opus-claims 8, 2; sol-verify N2.
- Severity: minor. Decision: accept.
- Change: `B9-ann-kan.tex:336` → as given in opus-claims 8; KAN box replay field: `r3` models Tier 1, `r5` models Tier 2, by the rule and times of G4-09; `:150`, `:165`: describe the second `ann` code as written after its session read the first, not as separately written (G1-02).
- Files: `sections/B9-ann-kan.tex`.

### G5-05 S1.7 first-implementation wording
- Sources: opus-writing 21.
- Severity: minor. Decision: accept.
- Change: `B7-eg.tex:344` in the wording of G3-05 (opus-writing 21), keeping the binary64 bounds and the side condition.
- Files: `sections/B7-eg.tex`.

### G5-06 "First code" and "second code"; the S1 provenance sentence
- Sources: opus-referee 11; LD2-2.
- Severity: minor. Decision: accept. Reason: after the disclosure, "the authors' code" suggests human-written code.
- Change: `B0-families.tex:11` → "\emph{The first code} of a certificate is its first implementation and \emph{the second code} its second implementation; \cref{sec:semantics-protocol} states that AI agents wrote both, what ``separately written'' means and the resulting common-mode risk." Replace "the authors' code/search/script" and "the verifier's code/re-certifier" by "the first code/search/script" and "the second code/re-certifier" throughout B1–B10 and F (also in paragraph titles such as `B7:234`, `B7:260`).
- Files: `sections/B0`–`B10`, `F-eg-rounding.tex`.

### G5-07 Section openings
- Sources: opus-writing 31; opus-consistency 16(e).
- Severity: minor. Decision: accept.
- Change: `B3:6`, `B4:6`, `B5:8`, `B6:4`: "This section" → "This subsection" or a content opening; add the opening sentence of opus-writing 31 to B7; B0's first sentence starts with the content ("Family by family, we complete …"); `B1:20` heading as in opus-writing 31 (or removed with the paragraph, G5-01); `B2:24` "we read this as a sign" → "we take this as a sign …, which is an interpretation".
- Files: `sections/B0`–`B7`.

### G5-08 Records check of three open wordings
- Sources: opus-consistency (status of G5 open note 5).
- Severity: minor. Decision: accept.
- Change: check "read twice, in separate agent sessions" (`B4:489`, `:491`), "a later separate agent session" (`B5:342`) and "Tier 1; minutes on one core" (`B3:284`) against the verification records and the register times; keep what the records confirm, otherwise write what they show.
- Files: `sections/B3`, `B4`, `B5`.

---

## 8. G6 supplement other: `C`, `D`, `E`, `H`, `I` (G6 parts), `J`; generators; `references.bib`

### G6-01 Consolidate S2, S3, S4, S6 and G6's parts of S7
- Sources: LD2-1; sol-referee 1.
- Severity: major. Decision: accept-modified (targets in §2.2: S2 6.2, S3 6.8, S4 10.8, S6 10.9, G6's S7 parts 2.3).
- Change: same method as G5-01: one home per verification statement (the certificate box); listed status and prior results only in S3.2; run records and history to `development/moves/r2-G6.md` (for example the per-run admission and measurement details of S6.1, the run lists of S6.6 "Wrong runs" and "Instrumented runs and settings" beyond what Observation 8.5 and Table S-runs need, S4.7 archive-copy listings beyond the claims of §7.4, the audit input hash table `tab:audit-inputs` if its hashes are already in the archive manifest); keep every statement, proof and number that a printed claim uses. Report page counts.
- Files: `sections/C-points.tex`, `D-literature.tex`, `E-audit.tex`, `H-solvers.tex`, `I-reproduction.tex` (G6 parts), `development/moves/r2-G6.md`.

### G6-02 Table 1: compact main table and full supplement table
- Sources: opus-referee 2(a), 11, 12; sol-referee 7; opus-consistency 2; opus-claims 12.
- Severity: major. Decision: accept-modified. Reason: Table 1 is a full sideways page with a visible overlap in the `lnts` row (sol-referee 7); its status column uses undefined labels ("second written after reading the first", "verified; shared core", "proved"); "proof by hand" suggests human work. The full table moves to S7.2, next to "Data reading by family" (not to the register, which changes in G7-03).
- Change in `data/make_tables.py`:
  - `tables/tab-trust.tex` (label `tab:trust`): upright `table`, `\footnotesize`, about half a page, columns family | dual arithmetic and trusted primitives | displayed dual certified by; second implementation (short) | status | level. No data-reading and no primal column.
  - Caption defines every status used: *verified*; *weaker second*, *partial second* (proved, and a separately written implementation certifies a weaker bound or part of the domain); *proved* (no separately written second implementation: `hvycrash`, a written proof; `ann_cumene_tanh`, the session that wrote the second code read the first in full, §2.6); *shared core* (both KAN paths use one rigorous exponential and interval core). It points to `tab:trust-full` for data readings and primal constructions.
  - `ann_cumene_tanh` status cell → "proved; second code written after reading the first"; `hvycrash` cells: "identity proved on paper", "written proof" (no "by hand").
  - New `tables/tab-trust-full.tex` (label `tab:trust-full`): the current sideways table with the same cell edits and widths that remove the `lnts` overlap; input in S7.2.
  - Apply any status change reported by G1-02. Run the generator from a `/tmp` copy (798 checks must pass); render both tables and inspect them by eye.
- Files: `data/make_tables.py`, `tables/tab-trust.tex`, `tables/tab-trust-full.tex`, `sections/I-reproduction.tex` (S7.2).

### G6-03 Other generator captions and labels
- Sources: opus-consistency 5, 7, 16(a); opus-writing 29, 30.
- Severity: minor. Decision: accept. Reason: `tab:claims` and S6.4 present the 15 evaluated campaign points as all 35 points beyond a certified bound (checked: `H-solvers.tex:60–62`, `08-solvers.tex:143`); `tab:solvers` calls the GAMS models the "stored model"; the Table 5 caption repeats §6.2 and makes "evidence" feasible.
- Change: `tab:claims` caption and `H-solvers.tex:83` as given in opus-consistency 5; `tab:solvers` row label as given in opus-consistency 7; Table 5 caption first sentence "The 13 closures whose earlier points were feasible only within a tolerance." and delete its last sentence; in caption prose "best listed dual" → "best listed dual bound" (headers may keep the short form, R2-11).
- Files: `data/make_tables.py`, `data/make_points_table.py` (wherever the caption is written), generated tables, `sections/H-solvers.tex`.

### G6-04 S8 becomes S7.5; its table moves to the artifact
- Sources: LD2-1 (superseded-display history to `HISTORY.md`).
- Severity: minor. Decision: accept-modified (the rules paragraph stays in the supplement; only the list of strings moves).
- Change: in `J-displays.tex` change `\section{Display record}` to `\subsection{Display record}` (label `app:displays` unchanged; it follows S7.4 because `J` is input after `I`); keep the rules paragraph; replace the table and its introduction by one sentence: "Strings in older records that must not be read as bounds, including displays corrected in this version, are listed in the archive (\cref{app:repro-register} names the file)." G7-04 moves the table (M10).
- Files: `sections/J-displays.tex`.

### G6-05 S6.6: reproducer proposition, cube lemma, related reports, checker counts
- Sources: opus-referee 2(c); LD2-3; opus-claims 3; opus-consistency 16(b).
- Severity: minor. Decision: accept-modified.
- Change:
  - Insert Prop. 8.3 with its note and Lemma 8.4 with its proof note (M3, from the r3 tar `08-solvers.tex:75–91`) at the start of "Proof of …" in S6.6, labels unchanged; merge their proof notes with the existing proof paragraphs (`H:227`, `H:246`) so that nothing is stated twice.
  - `H:306` → "A search of the SCIP issue tracker on 2026-10-02 found no matching report; this does not show that none exists." Add: "Communication with the SCIP developers is pending at the time of writing."
  - `H:215` and the box at `H:222`: the checker wording of G4-04 (eight code bases, six agent sessions, after the same records check); `H:133` "three separately written codes": check the sessions in `D/dossiers/camshape.md` and the QPLIB records; keep or reword as in G2-03.
  - The source comment of the SCIP witness box names `development/reviews/round1/sol-numbers.md:34–40` as the record of the $2.93\cdot10^{-15}$ check (G7-03 adds it to the register row in `RUNS.md`).
- Files: `sections/H-solvers.tex`.

### G6-06 S4 receives the folded §7 content
- Sources: opus-referee 2(d).
- Severity: minor. Decision: accept.
- Change: make S4.1 "How MINLPLib aggregates" hold the full content of `07-audit.tex:110–112` from the r3 tar (the instance set, the `.solu` comparison, the 0.083 and 0.31 excesses on `eniplac` and `stockcycle`); check that S4.4–S4.6 hold every statement of the folded §7.4 paragraphs (spring display, best listed primal 0.8462441 below $\vstar$, the (i-r) six-digit discussion, the `emfl` widths and the 1.166·10⁻⁶ remark, the `rocket` margins and the clean-copy rerun) and add any that is missing.
- Files: `sections/E-audit.tex`.

### G6-07 S3: closure terms, mechanism citations, funnel programs
- Sources: opus-writing 2, 31; sol-referee 2 and fresh assessment of p. 5; opus-claims 3.
- Severity: minor. Decision: accept-modified.
- Change:
  - `D-literature.tex:15` → "A \emph{floating-point closure} and a \emph{floating-point near-closure} are defined in \cref{sec:semantics-cert}; neither is a certificate in the sense of \cref{def:sem-certificate}." `:55` "printed gaps of at most 0.01\%" → "(\cref{sec:semantics-cert})".
  - Add to S3.1 a paragraph `\paragraph{Classical mechanisms.}` with the sentence of `01-introduction.tex:128` from the r3 tar, all citation keys unchanged (M7), and one sentence on IbexOpt's rigor mode with the new key (G6-08).
  - `:290`: "three separately written programs" as decided in G2-03.
- Files: `sections/D-literature.tex`.

### G6-08 Bibliography
- Sources: sol-referee 2.
- Severity: minor. Decision: accept.
- Change: add `@misc{ibex2026-ibexopt-ibex-documentation, author = {{IBEX team}}, title = {{IbexOpt}}, howpublished = {IBEX~2.9 documentation, \url{https://ibex-team.github.io/ibex-lib/optim.html}}, year = {2026}, note = {Read on 2026-10-04}}`. There is no KB entry (the KB has `araya2025-…` and `trombettoni2011-…`, which describe the relaxed equality mode only).
- Files: `references.bib`.

### G6-09 S7 opening, S7.2 and S7.4
- Sources: LD2-2; sol-verify U3; opus-referee 2(e); LD2-1.
- Severity: minor. Decision: accept.
- Change:
  - `I-reproduction.tex:18–19`: start with the content (no "This section"); provenance sentence → "As \cref{sec:semantics-protocol} states, AI agents working under the authors' direction wrote the implementations and ran the checks; that section defines ``separately written''." `:20`: "the root of the archive (\archiveDOI)" stays; no "public archive" anywhere in S2–S8.
  - S7.2: input `tables/tab-trust-full` after "Data reading by family".
  - S7.4: keep the regeneration facts that printed claims use, including every value deleted from §10 by G4-09 (the regenerated `waterno2_18` and `waterno2_24` bounds 4790.820086 and 6576.150434, rounded down, valid and slightly weaker; the clean-copy replay of all 63 periods at the stored targets; `powerflow0030p`; the `topopt` basis); move script names and run details beyond these to `development/moves/r2-G6.md`.
- Files: `sections/I-reproduction.tex` (G6 parts).

### G6-10 Names and openings in C–J
- Sources: opus-referee 11; opus-writing 31; opus-consistency 16(e).
- Severity: minor. Decision: accept.
- Change: "the authors' code" and "the verifier's code" → "the first code" and "the second code" in C, D, E, H, I (G6 parts), J; content openings instead of "This section …" in S2, S3, S4, S6 and S7.
- Files: `sections/C`, `D`, `E`, `H`, `I`, `J`.

---

## 9. G7 artifact (and the Build phase)

### G7-01 Isolated reproduction recipe and paper-only input preparation
- Sources: LD2-4; sol-referee 5 (round-1 item 13 "partly").
- Severity: minor. Decision: accept-modified (HOME isolation inside `WORK` plus a wrapper, because `prepare_inputs.py` and 109 research scripts read `~` and `research-20260929/` must not be edited; checked: `prepare_inputs.py` verifies models at `expanduser(record["path"])` and exits with status 1 if any of its pinned models is missing).
- Change:
  - One recipe, identical in S7.1 (`app:repro-setup`, G7-owned) and in the README:

    ```bash
    ARCHIVE=/path/to/unpacked/archive                 # read only
    WORK=$(mktemp -d /tmp/minlp-work-XXXXXX)           # disposable; rm -rf "$WORK" when done
    cp -r "$ARCHIVE"/. "$WORK"/ && cd "$WORK"
    export HOME="$WORK/home" XDG_CACHE_HOME="$WORK/home/.cache" PIP_NO_CACHE_DIR=1
    R="$WORK/research-20260929"; P="$WORK/paper-open-minlplib"
    export MINLP_REPO_ROOT="$WORK" EG_AUDIT_R="$R" MINLPLIB_OSIL_ROOT="$WORK/osil"
    export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
    export NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
    mkdir -p "$MINLPLIB_OSIL_ROOT" "$HOME/.cache/minlplib/minlplib"
    cp "$R"/publication/minlplib-status/pages/models/osil/*.osil "$MINLPLIB_OSIL_ROOT"
    ln -s "$MINLPLIB_OSIL_ROOT" "$HOME/.cache/minlplib/minlplib/osil"
    python3 -m venv "$WORK/venv" && . "$WORK/venv/bin/activate"
    python -m pip install -r "$R/publication/reproduction/requirements.txt"
    python "$P/artifact/prepare_paper_inputs.py"
    cd /tmp && python "$P/data/make_tables.py"
    ```
  - New `artifact/prepare_paper_inputs.py` (standard library only): runs the archived `prepare_inputs.py` of the `WORK` copy as a subprocess, parses its JSON, and exits 0 if and only if the saved inputs were restored, all 69 paper models (`tab:sem-hashes`, `tab:audit-inputs`) are present in `$MINLPLIB_OSIL_ROOT` with the recorded SHA-256, and the missing set equals the documented list of 26 models that the paper does not use (stored by name in the script); it prints that list as "not needed by the paper" and fails on any other missing or changed file. It never downloads.
  - README and S7.1: say that the cache folder is a link to the archived input root inside `WORK`, that nothing is written outside `WORK` and `/tmp/minlp-artifact-*`, and keep the distinction between the tested short recipe and the untested long replays. List as a limitation any script that reads an absolute path outside `WORK` (grep the archived scripts for `expanduser`, `Path.home`, `~/` and `/home/`).
  - Test (targeted, 2 cores): the wrapper and the short runner on a minimal `/tmp` copy with `HOME` inside it; confirm that the real `~/.cache` is unchanged (listing with sizes and modification times before and after). Record the commands and results in `artifact/logs/`.
- Files: `artifact/README.md`, `artifact/prepare_paper_inputs.py` (new), `sections/I-reproduction.tex` (S7.1), `artifact/logs/`.

### G7-02 Claim builder and validator
- Sources: opus-consistency 3 (major); LD2-4.
- Severity: major. Decision: accept. Reason (checked in `artifact/build_claims.py`): line 58 `allmodels.update(numbers['waterno2'])` replaces the full `numbers['instances']['waterno2_*']` entries, so `displayed_values` is empty for the waterno2 rows; `status_label` maps any status that starts with "verified" to "verified …", so register-17 (`eg_disc2_s`: partial second) and register-21 (`etamac`, `pricing050`: one implementation) are overstated; recorded commands are matched by script basename (`:214–215`).
- Change:
  - (a) merge instead of replace: `for src in (numbers['waterno2'], numbers['kan']): for k, v in src.items(): allmodels[k] = {**allmodels.get(k, {}), **v}`.
  - (b) per-instance status: parse the parenthetical exceptions of the status field ("verified (eg_disc2_s: partial second)", "verified (etamac, pricing050: proved)"); write `status_by_instance` and `verification_label_by_instance`; the row's `verification_label` is the weakest of its instances. Update `verification_note` and the README mapping.
  - (c) match `recorded_commands` on the full relative path and the working directory, not the basename.
  - Validator (`check_claims.py`): fail if an instance of a register row has empty displayed values (with an explicit exemption list for rows without numeric displays, such as `prop:kan-infeasible` and the campaign row), if a label "verified …" is attached to an instance whose status carries "partial second", "weaker second" or "proved", or if the rows of `RUNS.md` and the register disagree (G7-03).
- Files: `artifact/build_claims.py`, `artifact/check_claims.py`.

### G7-03 Compact register in S7.3 and register rows in `RUNS.md`
- Sources: LD2-1 (long paths), LD2-4; opus-consistency 10, 16(b); opus-claims 8, 12; sol-verify N2.
- Severity: minor. Decision: accept-modified (the register keeps its 27 rows and their order; its paths, arguments and expected outputs move to `RUNS.md`, M12).
- Change:
  - `tab:repro-register` (S7.3): four columns, result | checkers (file names only; "2nd:" marks the other implementation) | time | tier; level; status; trust. Caption: "``2nd'': the other implementation and what it certifies; for \inst{lukvle10}, \inst{catmix} and \inst{etamac} this is the first implementation, which certifies a weaker bound, for \inst{ex6_2_5} and \inst{ex6_2_7} a third code with stronger bounds" (check against the boxes `B4:429`, `B1:283`, `B5:214`, `B5:342`).
  - One sentence in S7.3, the only place where the supplement names the two files: "\nolinkurl{$P/artifact/RUNS.md} gives for every row of \cref{tab:repro-register} the full checker paths, arguments, expected outputs and run records, and \nolinkurl{$P/artifact/HISTORY.md} lists earlier and superseded certificates and displays, including strings in older records that must not be read as bounds."
  - Row edits: `thm:kan-enclosure`: the guarded copy is the second checker, the unguarded original is historical (`HISTORY.md`), tiers `r3` 1 and `r5` 2 as in G4-09; `prop:kan-infeasible`: level `\evid{hand}+\evid{stored}`, and add the separately written propagation over $\mathcal Q$ (`B9-ann-kan.tex:252`) as 2nd; `prop:scip-witnesses` row in `RUNS.md` names `development/reviews/round1/sol-numbers.md:34–40` for the $2.93\cdot10^{-15}$ residual check; `ann_cumene_tanh` status "proved (the second code's session read the first)" as now.
  - `RUNS.md` format: one block per row, headed `R01`–`R27` in register order, with the paper labels, the checker paths in backticks with `$R/` or `$P/` prefixes (a bare name lies in the folder of the preceding path), arguments, expected output and recorded time. `build_claims.py` reads labels, instances and the last column from S7.3 and paths, recipes and expected outputs from `RUNS.md`, matched by row number; it asserts 27 rows in both and equal label sets.
  - Update the S7.1 counts (claims, SHA-256 references, files) after the rebuild (G7-09).
- Files: `sections/I-reproduction.tex` (S7.3), `artifact/RUNS.md`, `artifact/build_claims.py`.

### G7-04 `HISTORY.md`
- Sources: LD2-1; opus-consistency 16(f).
- Severity: minor. Decision: accept.
- Change: new `artifact/HISTORY.md` with (1) the S8 table `tab:displays-unsafe` and its explanatory paragraph, from the r3 tar, as a Markdown table with the same rows and the note that each entry was rechecked in exact rational arithmetic (M10); (2) the superseded displays removed from S1 in round 1 (M15), with their sources; (3) the history passages from `development/moves/r2-G5.md` and `r2-G6.md` (G7-09); (4) the unguarded KAN second code as the historical checker. Update `outline.md` §8 item 11: the unsafe and superseded strings appear only in `HISTORY.md` (and 352.238025369202 as the weaker second bound).
- Files: `artifact/HISTORY.md` (new), `development/outline.md`.

### G7-05 `RUNS.md`
- Sources: LD2-1.
- Severity: minor. Decision: accept.
- Change: `artifact/RUNS.md` holds the register rows (G7-03), the README section "Round-1 reruns and checks" (M14; the README keeps one pointer), the Tier 2 and 3 run table details that the README does not need, and the run records from the moves files (G7-09).
- Files: `artifact/RUNS.md` (new), `artifact/README.md`.

### G7-06 `RELEASE.md`: identifying the PDFs
- Sources: LD2-4; sol-referee 6.
- Severity: minor. Decision: accept. Reason: the README says the PDFs of "the version that the index validates" are included, but `claims.json` hashes neither PDF.
- Change: new `artifact/RELEASE.md` with the SHA-256 of `build/main.pdf` and `build/supplement.pdf`, the build date and the validator's PASS line; the Build phase writes the hashes (G7 creates the file with marked fields). README "Release contents" and S7.1 say: "\nolinkurl{check_claims.py} validates the sources and the evidence (hashes of inputs, code and outputs, paths and labels); it does not identify the PDF files, whose SHA-256 hashes \nolinkurl{$P/artifact/RELEASE.md} records." `RELEASE.md` is not hashed in `claims.json`.
- Files: `artifact/RELEASE.md` (new), `artifact/README.md`, `sections/I-reproduction.tex` (S7.1).

### G7-07 README wording
- Sources: LD2-2, LD2-3; opus-consistency 15; opus-claims 14; sol-verify U3, N2, N3.
- Severity: minor. Decision: accept.
- Change: provenance paragraph (`README.md:8–11`) in the LD2-2 wording; `:23` "independently regenerated" → "regenerated `eg_int_s` audit (a separate run from a clean copy)"; `:28–30` the archive "will be deposited" with the DOI placeholder; a sentence that the SCIP reproducer, the witnesses and the audit's existence certificates are in the archive and that communication with the SCIP developers and the MINLPLib maintainer is pending; KAN tiers as in G4-09; the number file covers generated certified displays only.
- Files: `artifact/README.md`.

### G7-08 Development records
- Sources: sol-verify U4; opus-claims 14; opus-consistency 16(d); consequences of G1-02, G1-06, G1-07, G2-02.
- Severity: minor. Decision: accept.
- Change: `open-items.md:66–77`: remove the audit-novelty search from the open O-8 readings and record it as done (S3.1); `labels.md:242–243`: Table 7 is `tab:repro-tiers`, no `tab:structure`; `terminology.md`: "best listed dual bound" in prose, floating-point closure and near-closure defined in §2.2, "separately written" with the new criterion, status words including *proved* (with the `ann` case) and *floating-point output*, main-text certificate sentences without tiers (§6), first/second code instead of authors'/verifier's code.
- Files: `development/open-items.md`, `labels.md`, `terminology.md`.

### G7-09 Final integration and index rebuild (runs last)
- Sources: LD2-4; order of work.
- Severity: minor. Decision: accept.
- Change: after G1–G6 report done, merge `development/moves/r2-G5.md` and `r2-G6.md` into `HISTORY.md` and `RUNS.md`; rebuild `claims.json` from `/tmp` copies of the builder and validator; update the counts in S7.1 and the README; rebuild and validate once more (the index hashes `I-reproduction.tex`); run the 15 short checks under the new recipe on cores 0 and 1.
- Files: `artifact/*`, `sections/I-reproduction.tex` (S7.1 counts).

### Build phase (not an editor group)
- Run once, from an empty `build/`, after G7-09: `make`; the checks of `development/build.md` (no undefined or duplicate labels, no `??`, only the declaration placeholders and `[archive DOI]` print); `development/check_floats.py`; inspect Table 1 (now upright), Table 2, Figure 1, `tab:trust-full` and the register by eye; scans: no "Tier" in §§4–5, no "authors' code"/"verifier's code", no "public archive", no outline §8 item 11 string in either PDF except 352.238025369202 as the weaker second bound.
- Measure pages per section as in `build-r3.md` §5 and report them against Section 2.
- Write the SHA-256 of `build/main.pdf` and `build/supplement.pdf` into `artifact/RELEASE.md` (do not rebuild afterwards).

---

## 10. Rejections (full or partial), with reasons

| id | source | rejected | reason (checked) |
|---|---|---|---|
| R2-01 | opus-referee 2(g) | moving Appendix A.2–A.5 to the supplement | LD2-1 fixes the binding targets (Sections 1–11; supplement about 105 pages, which must shrink by about 20 pages); A.4 holds the residual proofs for Remark 2.3(2) that round 1 asked for and sol-verify accepted (opus-math-main 1 row); the reviewer counts Appendix A outside the body target himself |
| R2-02 | opus-referee 15(a) | renaming review-round folders in the deposited copy | the paths are hashed in `claims.json` and printed in S7 and `RUNS.md`; renaming only the deposited copy would desynchronize index and text; S7 already explains the working-folder names; the authors may rename at deposit with a rebuilt index |
| R2-03 | opus-referee 15(b) | rerunning the four Tier-1 searches with leaf logging | new certificate searches would change evidence levels and need review; sol-referee 5 calls new certificate searches unnecessary; the missing trees are stated as a limitation (G2-04, G4-07) |
| R2-04 | opus-referee 14; sol-referee 9 (part) | filing the SCIP issue and citing its number; sending the 22 bounds to the maintainer and requesting stored per-solver values | author actions that editors cannot take; LD2-3 states the pending communication and makes the witnesses available instead (G3-08, G4-04, G6-05, G7-07) |
| R2-05 | opus-consistency 13 | adding the missing tier clauses to `hvycrash`, `eg`, `ann` and KAN | the main-text tier clauses are deleted instead (G2-02, G3-01), which also settles opus-referee 8 and the stale waterno2 tier; tiers keep one home in Table 7 and the boxes |
| R2-06 | opus-writing 25 (part) | a lead-in sentence before Proposition 8.1 | optional in the review; the §8 opening already introduces BARON's claims; length |
| R2-07 | opus-referee 7 (option) | "separately written code from separate agent sessions" in the abstract | 250-word limit; LD2-2 places the disclosure in §2.6 and the declarations; "separately written" is defined in §2.6 |
| R2-08 | opus-claims 11 (part) | "its lower bounds would be rigorous for the stored models" | IbexOpt reads binary64 data, so validity for reading (b) is not established; the text says its lower bounds would be a natural rigorous baseline (G1-13) |
| R2-09 | opus-consistency 16(b) (option) | adding the $2.93\cdot10^{-15}$ residual check to `make_tables.py` | the generator uses only the standard library and the number file; the exact model evaluation belongs to the SCIP checkers; the reviewer's alternative (naming the record) is taken (G6-05, G7-03) |
| R2-10 | opus-consistency 16(c) (option) | including `fig-camshape-profiles` in S1.3 | the supplement must shrink; the figure supports no statement; it is moved out of the build instead (G2-07) |
| R2-11 | opus-writing 30 (part) | renaming "best listed dual" in table headers and figure legends | headers and legends need the short form; captions define it; prose changes everywhere (G1-07) |
| R2-12 | opus-referee 2(b) (part) | dropping the CAMINO margins and assumptions from C3 | sol-referee 8 requires keeping the model-correspondence assumptions and "causes unknown"; the margins take one clause (G1-12) |
| R2-13 | opus-referee 1 (bracketed sentence) | an editor writing which proofs or code a person read | only the authors can state it; the `\TODO` stays (LD2-2, G4-08) |
| R2-14 | opus-claims 3 (part) | a per-witness count [k] of sessions | the records give eight code bases from six sessions but no per-witness session list; the text states the totals after a records check (G4-04, G6-05) |
| R2-15 | sol-verify U3 (part) | supplying a deposited release now | author action; the text no longer asserts a completed public deposit (G1-09, G1-12, G4-08, G4-09, G7-07) |
| R2-16 | opus-writing 8 (part) | leading the C3 campaign sentence with "all 109" | sol-referee 4 asks to lead with the 79 comparable bounds; the 30 others follow with their qualifier (G1-12) |
| R2-17 | opus-claims 4 (part) | "the remaining branching was low-dimensional" for all closures in observation 1 | outline §8 item 8 forbids claiming low-dimensional branching for `pindyck` and `eg`; observation 1 states the facts per group, and §11 restricts "low-dimensional" to 27 of 31 (G1-11, G4-07) |

Full rejections of a whole review item: opus-consistency 13 and opus-referee 15
(both parts). All other rejections are of parts or options.

No action needed (accepted as they are): the round-1 items that the reviews
mark resolved; sol-referee on Table 2 ("usable but … dense"; no column change
in this round) and on Figure S4 staying in the supplement; opus-referee m13
(hollow marker, R-08 accepted); sol-verify's two "rejected-justified" rows.

## 11. Coverage index (review item → adjudication id)

- **sol-referee:** 1 → LD2-1, G1-10, G1-12, G2-01, G4-06, G5-01, G6-01, G6-04, G7-03, G7-04, G7-05; 2 → G1-13, G6-07, G6-08; 3 → G2-04, G4-07; 4 → G1-09, G1-12, G4-01; 5 → G7-01; 6 → G7-06, Build phase; 7 → G1-08, G6-02; 8 → G1-03, G1-09, G1-10, G1-12; 9 → LD2-3, G3-08, G4-04, G6-05, G7-07, R2-04; fresh assessment p. 5 (mechanism list) → G1-13, G6-07.
- **sol-verify-changes:** N1 → G1-04, G1-05; N2 → G4-09, G5-04, G7-03, G7-07; N3 → G1-12, G4-09, G7-07; U1 → G1-05, G4-07; U2 → G5-03; U3 → G1-09, G1-12, G4-08, G4-09, G6-09, G7-07, R2-15; U4 → G7-08.
- **opus-referee:** 1 → LD2-2, G1-01, G1-15, G4-08, G5-06, G6-10, G7-07, R2-13; 2(a) → G1-08, G6-02; 2(b) → G1-12, R2-12; 2(c) → G4-04, G6-05; 2(d) → G3-08, G6-06; 2(e) → G4-09, G6-09; 2(f) → G2-02, G3-01, G4-06; 2(g) → R2-01; 3 → G1-11, G4-07; 4 → G2-04, G4-07; 5 → G1-02, G3-03; 6 → G1-13; 7 → G1-09, R2-07; 8 → G2-02, G3-01; 9 → G4-06; 10 → G2-03; 11 → G1-03, G3-07, G5-06, G6-02, G6-10; 12 → G1-08, G6-02; 13 → G4-02; 14 → LD2-3, G4-04, R2-04; 15 → R2-02, R2-03.
- **opus-consistency:** 1 → G2-02; 2 → G1-02, G6-02, G7-03; 3 → G7-02; 4 → G5-03; 5 → G6-03; 6 → G3-05, G4-06; 7 → G6-03; 8 → G2-04; 9 → G1-02, G3-03; 10 → G7-03; 11 → G1-12; 12 → G1-15; 13 → R2-05; 14 → G4-09; 15 → G7-07; 16(a) → G6-03; 16(b) → G6-05, G7-03, R2-09; 16(c) → G2-07, R2-10; 16(d) → G7-08; 16(e) → G5-07, G6-10; 16(f) → G5-01, G7-04.
- **opus-writing:** 1 → G2-03; 2 → G1-06, G2-05, G6-07; 3 → G1-09; 4 → G1-11; 5 → G1-11, G4-07; 6 → G1-10, G1-12; 7 → G1-12, G3-07; 8 → G1-12, G4-01, R2-16; 9 → G1-13; 10 → G1-11, G1-12, G4-06; 11 → G1-07; 12 → G1-07; 13 → G1-01, G1-07; 14 → G1-02, G1-03, G1-04; 15 → G2-05, G3-09; 16 → G2-02; 17 → G2-06; 18 → G2-06; 19 → G2-02, G3-01; 20 → G3-04; 21 → G3-05, G5-05; 22 → G3-06; 23 → G3-08; 24 → G3-08; 25 → G4-02, G4-03, G4-04, R2-06; 26 → G4-06; 27 → G4-09; 28 → G4-06, G4-07; 29 → G6-03; 30 → G1-07, G1-15, G2-05, G3-07, G6-03, G7-08, R2-11; 31 → G5-07, G6-07, G6-10.
- **opus-claims:** 1 → LD2-2, G1-01, G4-08; 2 → G1-02, G3-06, G5-04; 3 → G2-03, G4-04, G6-05, G6-07, R2-14; 4 → G1-11, G4-07, R2-17; 5 → G1-11, G4-07; 6 → G1-05, G4-05; 7 → G2-04; 8 → G3-06, G5-04, G7-03; 9 → G1-09, G4-01; 10 → G1-11; 11 → G1-13, R2-08; 12 → G1-03, G6-02, G7-03; 13 → G1-02; 14 → G7-07, G7-08.

## 12. Counts

| group | items | major | minor | accept | accept-modified |
|---|---:|---:|---:|---:|---:|
| G1 front | 15 | 5 | 10 | 5 | 10 |
| G2 results and split | 7 | 3 | 4 | 3 | 4 |
| G3 other, points, audit | 9 | 1 | 8 | 6 | 3 |
| G4 end | 9 | 3 | 6 | 3 | 6 |
| G5 supplement certificates | 8 | 2 | 6 | 7 | 1 |
| G6 supplement other, generators, bib | 10 | 2 | 8 | 5 | 5 |
| G7 artifact | 9 | 1 | 8 | 7 | 2 |
| **total** | **67** | **17** | **50** | **36** | **31** |

No blockers. Inputs: 93 numbered review items (sol-referee 9, sol-verify 8,
opus-referee 15, opus-consistency 16, opus-writing 31, opus-claims 14) and five
lead-author decisions, deduplicated into 67 change items and the Build phase.
Rejections: 17 (Section 10), two of them full (opus-consistency 13,
opus-referee 15). Every review item maps to at least one change or rejection
(Section 11). Certified numbers changed: none.
