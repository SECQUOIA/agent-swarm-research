**Structural consolidation completed (full review M3).** Ownership is released for the four revised sections and both new appendices. The accepted mathematics is unchanged. I edited only `sections/constraints.tex`, `sections/local-rates.tex`, `sections/residual.tex`, `sections/effort.tex`, the two new appendices below, and this evidence file.

The material now has these locations:

| Material | Location |
| --- | --- |
| Restricted tangent setup, `prop:restricted-tangent-con`, and its proof | `sections/local-rates.tex`, following the concise `rem:linear-equations` setup |
| Worked affine-equality map `prop:equality-con` | `sections/constraints.tex`, with a pointer back to the general local-rate proposition |
| General `prop:history` and both explicit artificial history examples | `sections/residual.tex`; the moved subsection retains `sec:histories-con` |
| McCormick trajectory example `ex:switch-con` | `sections/constraints.tex`, unchanged |
| Proofs of `thm:cover-con` and `prop:coverage-con` | New `appendices/parametric-proofs.tex`; their statements, interpretation, and explicit proof pointers remain in constraints |
| Interleaving, equal shares, serial rescue, and the indistinguishable-first-action example | New `appendices/scheduling.tex`, retaining the original statement, subsection, equation, and example labels |
| Ledger, enhanced-versus-independent execution distinction, and evaluation requirements | `sections/effort.tex`, with a short appendix pointer explaining the guarantees and the ideal work-model premises |

The restricted tangent statement and proof were moved verbatim. Its location-dependent setup and explanatory references now point to the local shape definitions, the constrained example, and the feasible-repair subsection. The old affine-equation remark is a concise introduction rather than a second account of the theorem. The local observed-ratio discussion already referred to `prop:history`; that reference remains correct in its consolidated home. The two history examples and the scheduling material retain their mathematical text exactly.

I removed the repeated measured-policy disclaimers at the close of constraints and residual, and the extra disclaimer after the constrained basis-switch example. The scientific conditions remain: complete region coverage, invariance, checked derivatives, uniform repair assumptions, and the distinction between work and elapsed time. The native-OBBT-active sentence was removed from constraints; the experiments section already carries it and was not edited.

The effort section now describes the measured ratio as non-LP time per **recorded callback**, about three times the time of one LP with validation. It no longer presents that allocation as a uniformly measured callback cost. Its timer prose uses **added propagator** and **propagator times**. All costs, allowance rules, and proofs are unchanged.

I retained `B_0'` in the restricted tangent and repair results. There `B_0` is the outer problem domain used by the standing assumptions, while `B_0'` is the potentially smaller starting box of the iteration. Renaming them alike would remove a necessary distinction.

Before editing, I saved byte-for-byte copies of the four sections in `/tmp/obbt-structure-before-x_s9xnpu`. The targeted preservation check compared the multisets of all proof environments before and after and the label-indexed mathematical environments (theorems, propositions, lemmas, corollaries, examples, and assumptions). All **42 proof environments** and **64 labeled mathematical environments** match exactly; none was lost or duplicated. The six moved proof hashes are:

| Proof | Identical SHA-256 before and after |
| --- | --- |
| prop:restricted-tangent-con | ed4cf42501bac89a2a5242b52823e2c65fa94136419e1cc29ddb4a9887ec9111 |
| thm:cover-con | 428e9900ad4e705bc34edc7ba90919a3909b91e80c4f5adebac394aabd31c8a9 |
| prop:coverage-con | bdc2c23476afcf036d59700ad5162355620fbf7c380811e72b4c9e57e1d68630 |
| thm:interleaving | 0712f8efcdc9b30df0cc5daa8c5fe358a3b8ee37a2285c0007beeffcec379443 |
| cor:equal-shares | 2746cbfaf6c42f6cb9164169b77bb5098937f843f85a0a23718b16110dd13733 |
| prop:rescue | 61d97ab935e9f4307aea4a9676af7fbbe01817c55d60e5ac11eb4397520ede56 |

A targeted reference check extracted only the reference targets used by the six changed sources, then located their definitions in the manuscript sources. All **118 targets** resolve exactly once. The six changed sources also pass a LaTeX environment-nesting check. I read the move boundaries and the new main-text pointers after applying the edits.

Commands actually run were targeted `cat` and `sed -n` reads of these sections, the two new appendices, the existing appendix style, `AGENTS.md`, the brief, and the full-review structure recommendation; `rg --files paper-adaptive-obbt/appendices`; `rg -n` searches for the moved labels, observed-ratio references, and repeated policy/timer prose; a Python snapshot-copy command; and a Python proof-preservation/reference/environment check. That check reported:

```text
Proof environments preserved byte for byte: 42
Labelled mathematical environments preserved byte for byte: 64
prop:restricted-tangent-con: ed4cf42501bac89a2a5242b52823e2c65fa94136419e1cc29ddb4a9887ec9111
thm:cover-con: 428e9900ad4e705bc34edc7ba90919a3909b91e80c4f5adebac394aabd31c8a9
prop:coverage-con: bdc2c23476afcf036d59700ad5162355620fbf7c380811e72b4c9e57e1d68630
thm:interleaving: 0712f8efcdc9b30df0cc5daa8c5fe358a3b8ee37a2285c0007beeffcec379443
cor:equal-shares: 2746cbfaf6c42f6cb9164169b77bb5098937f843f85a0a23718b16110dd13733
prop:rescue: 61d97ab935e9f4307aea4a9676af7fbbe01817c55d60e5ac11eb4397520ede56
Reference targets used by the six changed sources: 118; missing: 0; duplicate: 0
Environment nesting check: six changed sources balanced
Targeted preservation/reference checks: PASS
```

No experiment, solver, literature search, project-wide check, CI inspection, or build was run. Main and all other manuscript files were left to their owners. Root was notified to add `appendices/parametric-proofs.tex` and `appendices/scheduling.tex` to `main.tex`; their top-level labels are `sec:parametric-proofs` and `sec:scheduling`.
