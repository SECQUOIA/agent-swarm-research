# Passive potential-flow manuscript

Paper A, [Topology, Uncertainty, and Precision in Passive Potential-Flow Optimization](complexity/main.tex), is complete after the staged writing, review, and correction process. It includes a focused main narrative, references, and all technical proofs as appendices. Its scope covers all 43 promoted potential-flow results, including uncertainty geometry, weighted cactus and higher-block algorithms, correlated design, energy, and rational certificates. No result requires an unwritten companion paper.

Stages S1–S7 are accepted through the required independent-agent review and separate correction process. The final five-reviewer whole-manuscript round found no major issue, and every valid minor finding has been corrected and verified by the lead. Internal research-agent review is not journal peer review or formal proof certification. The pre-existing `uncertainty/` manuscript is outside this task and is not included in the Paper A archive.

Formal verification follow-up (2026-09-20): [topic 03](../formal/topics/03-potential-flow/COVERAGE.md) and [topic 16](../formal/topics/16-potential-flow-certificates/COVERAGE.md) verify the deterministic certificate mathematics in Appendix K, including conditional scenario recovery and the two-path comparison. They do not verify the full manuscript, original uncertainty-to-envelope mapping, Python implementation, conservation-repair producer, bit-complexity claims or effective-resistance reformulation. The source now also states the quantitative support-convergence estimate proved in Lean. The [current PDF](complexity/main.pdf) includes these updates and was rebuilt from clean sources for the [September 20 documentation follow-up](../notes/lean-verification-documentation-followup.md). The completion PDF and archive linked below remain historical artifacts.

- [Standalone build and reproduction instructions](reproducibility/README.md)
- [Completion PDF](dist/paper-a.pdf) and [completion source archive](dist/potential-flow-paper-a.tar.gz)
- [Detailed result/extension map](process/completion-coverage.md) and [308-file source inventory](coverage.md)
- [Completion process](PROCESS.md) and [authoritative completion plan](process/completion-plan.md)

From the repository root, build only Paper A:

```sh
python paper-potential-flow/reproducibility/build_paper.py
python paper-potential-flow/verification/check_coverage.py
python -S paper-potential-flow/reproducibility/reproduce.py --output exact-replay.json
```

The build requires latexmk and TeX Live; the exact replay uses only Python's standard library. The build gate requires zero errors, undefined references/citations, duplicate labels, and overfull boxes. Numerical diagnostics require the separately listed scientific dependencies and run in isolated copies to preserve saved data. The numerical producers are not implementations of every theoretical algorithm; proofs establish universal results and exact replays establish particular witness guarantees.

The bibliography contains only actually cited references. Primary version locators and qualified comparisons appear in the text and the [literature screen](process/completion-literature-screen.md). The source archive excludes managed literature PDFs, original dataset INP files, internal review reports, and other manuscripts.
