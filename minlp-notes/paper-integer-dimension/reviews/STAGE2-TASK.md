# Stage 2 review task

The user commissioned a standalone LaTeX paper covering every substantive repository development on integer dimension of nonlinear graph approximation. They explicitly require fifteen independent reviewers after each drafting stage, root adjudication, a separate correction agent, and another fifteen-reviewer round whenever major issues are found. Stage 1 has passed its gate; stage 2 is now complete. Stages 3–4 are not yet drafted.

Read `PROCESS.md`, `reviews/PROTOCOL.md`, the round's `snapshot.json`, **all stage-2 section files listed in the snapshot, together with their dependencies in `sections/01-foundations.tex`**, relevant bibliography, and `coverage.md`. Independently check the stage's mathematical claims and exposition. Compare the corresponding original `results/` proofs, supporting `notes/` and audits, but do not accept previous reviews as proof. Use your numbered primary lens in `reviews/STAGE2-LENSES.md` for extra depth while checking the whole stage. Be constructive and exacting. Do not invent problems or accept an unsupported main claim for convenience. The paper must contain rigorous standalone proofs of its contributions; citations to established external theorems are allowed with accurate hypotheses. The rational noncommutative-rank rate preview in stage 1 must now be fully proved. Unwritten stage3–4 proofs explicitly previewed for later are not omissions in this stage, but their stated scope must be accurate. Check all stage-2 coverage rows, including supporting propositions, degeneracies and counterexamples.

Manuscript paths are relative to `paper-integer-dimension/`; the repository root is `/home/sgusev/repo/minlp-notes`. Primary-source PDFs/text retrieved by root are in `build/source-cache/`, including GGOW, IQS, Zhang–Sra, Criscitiello–Boumal, GLS1981, Dadush–Peikert–Vempala, and Del Pia. Root independently checked their main imported interfaces; verify them yourself when relevant. Root notes are in `verification/stage2-root-source-audit.md`. Read `literature/AGENTS.md` before using the literature knowledge base. Bibliographic and novelty claims require primary-source evidence, not a search result or a prior agent's opinion. You may browse official/author sources when needed. Do not edit manuscript, bibliography, original research, or other reviewers' reports. Do not spawn subagents. You may write a focused independent checker under `verification/` with a unique reviewer prefix if useful.

Write your report at the exact path specified in your assignment. Include:

- Reviewed file SHA-256 hashes checked against the snapshot, and actual coverage/verification limits.
- A concise overall assessment.
- Numbered concrete findings: severity MAJOR / MINOR / QUESTION, exact theorem or line location, the reasoning/counterexample or missing obligation, and a suggested repair when available.
- Distinguish a false theorem from a proof gap, missing hypothesis, inaccurate source attribution, and expository weakness.
- State explicitly `Major findings: N` and `Minor findings: N`. If none, say so without claiming certainty.

Your final message to root should summarize major findings first, then minor findings, the report path, and any executed checks. Do not stop after inspecting only your specialist subsection.
