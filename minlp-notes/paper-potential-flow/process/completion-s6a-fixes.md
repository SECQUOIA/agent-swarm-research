# Stage 6a minor-fix report

All three repairs required by `completion-s6a-adjudication.md` are applied. The repaired source and evidence are frozen for lead verification; this report does not accept S6a or advance the completion plan.

The starting Section 11 matched the author freeze, SHA-256 `0730038a9098898f45ce72c4373ae64101fd1fdc74b4f6d92d8ae093ecf0f09e`. I read the adjudication and the actual frozen section before editing.

The manuscript changes are confined to four short edits in `complexity/sections/11-certified-computation.tex`:

- `thm:a-cert-hessian` now begins, “Let $y\in\mathbb{Q}^m$ satisfy $Ay=b$.” Its remaining statement and proof are unchanged.
- `ex:a-cert-paths` introduces rational $0<\epsilon<1$ and takes the displayed asymptotic as rational $\epsilon\downarrow0$. The formulas and rational-attainment construction are unchanged.
- The benchmark paragraph now states a full coefficient ratio of $3\cdot10^6$. The fixture identifier, base-scale parameter, data, and recorded results are unchanged.

I imported `verification/build_and_check.py` and called only `build('complexity')`. I did not invoke its command-line entry point. The Paper A build completed with return code zero, a PDF present, no errors, no undefined references or citations, no duplicate labels, and **zero overfull boxes**. Zero overfull boxes was an explicit additional assertion, since the helper's `passed` flag alone does not require it.

All 18 final source hashes were checked against the actual files and the regenerated `completion-s6a-build.json`. Comparing this manifest with the frozen manifest identified exactly one changed input: Section 11. The other 17 inputs retain their frozen hashes, including the main file and bibliography.

The only change to `completion-s6a-checks.json` is its `final_build_sha256` value. Parsed-data comparison confirmed that every other field is identical to the frozen record. In particular, both new diagnostic runs, all 14 existing replay runs, all ten benchmark result records, all source and saved-input hashes, the dataset transformation record, primary-source hashes, and the preservation evidence remain unchanged. The existing true `final_inputs_match_build` value was independently reverified.

All 73 recorded code-source hashes, all four recorded saved-input hashes, and the new diagnostic hash were checked against the current files before editing and again at final verification. The author report remains byte-for-byte unchanged. A comparison against the pre-repair repository-file snapshot found only the three expected changed existing files: Section 11 and the two S6a JSON records. This fix report is the only added repository source file. Generated Paper A build artifacts were rebuilt as described above. No numerical or mathematical checks were rerun for these wording repairs. No Paper B, research, implementation, managed-literature, plan, or coverage files were edited, and no commit was created.

Final SHA-256 values:

| File | SHA-256 |
| --- | --- |
| `complexity/sections/11-certified-computation.tex` | `5f0b6d8a13cd351e48e9ad8d23e284720e975cc9cdac07fa9a4529583298bd15` |
| `process/completion-s6a-build.json` | `4d14dd18a264ce6ab483991a1186614ad697138639e7045123a36a5452994c2d` |
| `process/completion-s6a-checks.json` | `05285cb729c7547406c4724c45c0250e640b77021e56411db32ed3d519d7c44a` |
| `process/completion-s6a-author.md` (unchanged) | `449a0046a8be81e3775c1940b78891ae9990199e122bd350dc336498d1cbc812` |
| `verification/check_s6a_certificates.py` (unchanged) | `72d595b543c6b50247c0d7ac23540a6aebf1e0164f78f93d07f077f97822d341` |
| `complexity/build/main.pdf` | `855f9fd604635180bf465d7cc592589f4659a819e55ceeb0286e6db9099e4edf` |
| `complexity/build/main.log` | `acb11b55a4bdf452ee7bf6079dbe7b1dd5b993af3a510e21dd3952e14a9cbf4d` |

The checks file's final-build link is `4d14dd18a264ce6ab483991a1186614ad697138639e7045123a36a5452994c2d`, matching the final build record above. The complete 18-input hash inventory is retained in that build record.
