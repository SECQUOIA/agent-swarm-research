# Shared authoring conventions

Read BRIEF.md, INCOMING-AUDITS.md, your relevant full audit, and ARCHITECTURE.md when available. The architecture refines scope; it does not authorize claims rejected by an audit. Write a journal manuscript, not a catalogue of repository notes. Include complete proofs of every nonstandard claim used by your main results. A result requiring an unresolved assumption must state it or be excluded. All literature requests go to root, who routes them to the Luna lead.

ARCHITECTURE-DECISION.md records the root's final integration choices and supersedes stale proof-status or summary statements in ARCHITECTURE.md. All existing author allocations remain unchanged; a separate focused decomposition chapter is being added.

Working title: Instance-dependent certification complexity in branch-and-bound.

Root owns main.tex, macros.tex, BUILD.txt, README.md, global integration, and delivery. Planned inputs (each allocated to one writer):
1. sections/introduction.tex
2. sections/certificates.tex and sections/geometry.tex
3. sections/face-exact.tex
4. sections/propagation.tex
5. sections/branching.tex
6. sections/lattice.tex
7. sections/regression.tex
8. sections/binary-least-squares.tex
9. sections/experiments.tex
10. sections/discussion.tex

Prefix every label with your subject, except main section labels: sec:certificates, sec:geometry, sec:face-exact, sec:propagation, sec:branching, sec:lattice, sec:regression, sec:binary-least-squares, sec:experiments. Use appendix prefixes app:geometry, app:face, app:propagation, app:branching, app:lattice, app:regression, app:bls. Root decides appendix placement at integration. Keep long proofs in your owned appendix where that materially improves reading; no omitted proofs in internal evidence files.

Added decomposition author owns sections/decomposition.tex and appendices/decomposition-proofs.tex, using sec:decomposition and app:decomp labels. It follows face-exactness and precedes propagation in main.tex.

Standard environment names available: theorem, proposition, lemma, corollary, definition, assumption, example, remark. All numbered within sections with a shared theorem counter. Packages available: amsmath, amssymb, amsthm, mathtools, bm, booktabs, longtable, array, graphicx, enumitem, microtype, natbib (author-year), hyperref, cleveref, algorithm, algpseudocode. Use standard LaTeX commands when possible. Global macros available: \R, \N, \Z, \E, \Pbb, \OPT, \argmin, \argmax, \diag, \dist, \vol, \supp, \rank, \cone, \cl, \relint. Request additional shared macros from root; local names may be defined at the top of your file if necessary and must be unique.

Baseline continuous notation: D is a compact axis-aligned root box in R^n, F is its feasible set, f_* is the optimal value, m(x)=f(x)-f_*, epsilon>0 is the additive certificate tolerance, B is a closed test box, L(B) its lower bound. State explicitly whenever dimensions, oracle, constraints, or incumbent conventions change. Use N_cover, N_rect, and N_tree for distinct spatial certificate classes rather than treating covers, arbitrary partitions, and guillotine trees as equal. Owned sets A_e resolve shared boundaries; test boxes C_e are closed. Tree nodes, leaves, bound evaluations, tightening rounds, and removed-piece certificates are different costs.

Integer/statistical chapters can use M for sample size and N or p for ambient dimension, but define each model afresh and map its certificate measure to the framework. Specify incumbent assumptions and whether planted points are proven globally optimal. Never compare numerical exponent constants across different oracle classes without qualification.

Citations: use provisional ASCII keys from LITERATURE-KEYS.md. They are placeholders until the Luna lead verifies source identity and theorem locators. Never fabricate bibliographic fields. Mark literature queries in your separate AUTHOR-<subject>.md evidence file, not in the manuscript. Submission prose must contain no internal review history, agent names, repository-process text, unresolved TODOs, or claims of journal acceptance.

Write only your assigned files. Report mathematical developments and source/proof/claim mappings in your assigned evidence report. Do not edit existing papers, experiments, bibliography, main.tex, or other authors' chapters. Do not rerun computational experiments or browse literature. Targeted TeX compilation will be done by root after integration.

Before finalizing your assignment, reread INCOMING-AUDITS.md, ISSUES.md, the latest LITERATURE-KEYS.md/LITERATURE.md, your full source audit, and any named independent development review. These are updated during concurrent writing. Your final evidence report must state which version/independent findings your chapter incorporates and list only concrete remaining integration requests. Internal reports are not submission dependencies.
