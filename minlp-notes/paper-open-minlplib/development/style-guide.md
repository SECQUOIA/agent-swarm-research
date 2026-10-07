# Style guide for the paper

Audience: experts in global optimization, MINLP and numerical verification
(Mathematical Programming Computation readers and referees). They know
spatial branch and bound, Lagrangian duality, McCormick relaxations and
interval arithmetic. They do not know our notes, our scripts or our
internal names.

## Language

- Write plain, direct English. Short sentences. One idea per sentence.
- Prefer the familiar word: "use" not "utilize", "show" not
  "demonstrate", "about" not "approximately" in prose (keep exact numbers
  exact).
- Use the active voice and "we" for our actions. Name the actor.
- Define every term at first use. Use the defined term consistently;
  never vary it for style.
- State each claim with its qualifier in the same sentence or the next.
  Never let a qualifier drift away from its claim.
- Precise hedges only where the evidence is limited ("to the best of our
  knowledge, within the search described in Appendix D"). Do not hedge
  proved statements.
- Explain why a step works, not only what it does, when the reason is not
  obvious to an expert.

## Banned patterns (LLM slop)

Do not use: "delve", "crucial", "pivotal", "notably", "importantly",
"interestingly", "it is worth noting", "it should be noted", "leverage",
"harness", "utilize", "seamless", "robust" (except as a technical term
with a definition), "comprehensive", "holistic", "landscape", "realm",
"journey", "tapestry", "unlock", "empower", "paves the way", "sheds light",
"plays a key/crucial role", "in the context of", "a wide range of",
"novel" (say what is new instead), "state-of-the-art" (name the solver
and version), "significantly" (unless statistical), "groundbreaking",
"cutting-edge", "game-changer", "In conclusion,", "In summary,"
at the start of paragraphs, "Moreover," / "Furthermore," / "Additionally,"
chains, rhetorical questions, and sentences that only announce what the
next sentence says.

Also avoid:
- reflexive triplets ("fast, accurate, and reliable");
- bold or italic inline labels inside prose paragraphs as pseudo-headings;
- bullet lists in the main text where a short paragraph reads better
  (lists are fine for contributions, assumptions and hypotheses);
- closing paragraphs that restate the section;
- em-dash chains; use at most one em dash per paragraph;
- "This paper/section presents..." openings for every section. Start
  with the content.
- anthropomorphizing software ("the solver believes"). Say "returns",
  "reports", "claims".

## Claims and numbers

- Every number must come from the verified sources (development/numbers
  or the dossiers/critiques/reviews), with the safe display direction:
  dual (lower) bounds rounded down for minimization, primal (upper) bounds
  rounded up; reversed for maximization; displayed gaps rounded up.
  Never round a bound to nearest.
- Distinguish: proved; verified by a separately written implementation
  (defined in Section 2.6; never "independent");
  computed (single implementation); floating-point solver output;
  interpretation. Use these words exactly.
- "Closed" means: a valid dual bound and an exactly feasible point within
  the stated gap, under the paper's model semantics (Section 2).
- Solver claims that our exact results contradict: say "not attainable
  by any exactly feasible point" or "a tolerance artifact" unless a
  genuine error is proved (the SCIP defect). Credit tolerance-level
  closures by name.
- Never write "first" or "previously unsolved" without the qualifier
  from the outline's contribution text.
- Internal names (scripts, wave numbers, "route R", dossier ids, agent
  names, review rounds) do not appear in the main text. Use them only in
  the reproducibility appendix, in a neutral form.

## Mathematics

- Theorem, lemma, proposition, definition, remark environments with
  labels. State hypotheses fully. Proofs complete; computer-assisted
  steps state exactly what the computation checks and in what
  arithmetic, and name the archived artifact in a certificate box.
- Notation from development/outline.md section 4 and the macros file;
  do not introduce competing symbols.
- Use the instance names exactly as MINLPLib spells them, in \texttt{}
  via the \inst{} macro.

## LaTeX

- Use the macros in macros.tex. One sentence per line is fine.
- Tables: booktabs, no vertical rules, units and conventions in the
  caption.
- Cross-reference with \cref. Cite with \citet/\citep and BibTeX keys
  from references.bib.
