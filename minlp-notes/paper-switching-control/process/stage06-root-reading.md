# Stage 6 primary-agent audit

## Independent public-profile calculation

Downloaded the pinned CSV independently and verified its exact SHA256. Parsed all three rate columns from the six-column source (not the older driver’s selected subset), used the first12000 rows as cell rates, and verified exact uniform widths1/1000 and horizon12. Independent largest-remainder quantization used mode-index tie breaking and verified the normalization and quantization bounds.

The independent integer-arithmetic script process/stage06-root/public_independent.py never imports the manuscript optimizer or cost recurrence. It computes physical block-end occupations directly for every ordered mode word and boundary combination, allowing all budgets below the cap. It reproduces the fine one-switch optimum1889/1000 and all budgets0–3 on grids12,24,48. Exact outputs and schedules are in its JSON. For3switches, values are1067507/1250000,2631679/5000000,10526709/20000000, respectively. All48-cell values therefore also have independent full-word corroboration.

A separate per-cell affine crossing calculation evaluated all6 ordered pairs and constants for continuous one-switch optimization. On quantized input it gives4721469/2500000, attained by mode1 then2 at that same time. Exact pair outputs are public-continuous-crossings.json. This independently develops the benchmark beyond the earlier grid-only result.

The same calculation on the exact normalized decimal source, before quantization, gives continuous error approximately1.8885877661091461, switch time1.8885877662201223, and grid error1.8889999998888654 at time1.889, always word1→2. All exact fractions, terminal masses and pair values are in normalized-public-one-switch.json. Tiny positive source mass in mode1 is rounded to zero, so the original-source grid value is not exactly1.889. This verifies the importance of distinguishing exact quantized optimization from original-data claims. The previously stated cumulative perturbation interval remains valid.

## Source audit

Read the local literature instructions and the relevant minimum-dwell paper’s Section5.2. Visually inspected original PDF page17/printed669, Corollary1: unrestricted CIA optimum <=((2n−3)/(2n−2))*maximumwidth. Equal-cell discretization with k cells and exact averaging immediately gives the classical continuous hard-budget upper((2n−3)/(2n−2))*T/k, hence the leading dimension-free T/k rate already follows from prior work. Source sharpness is not automatically sharpness under a different hard-budget model. This precise comparison was sent to the author.

Targeted primary-source searches also confirmed the scope of the2025 dynamic-programming-inspired paper and the2024 transformedMIOCP study; no exhaustive novelty or priority claim is warranted. Direct ScienceDirect/Lirias access did not supply a full2025 PDF; the author is verifying the indexed primary introduction and documenting that limitation.

The author remains active. Full draft reading and five independent stage reviews are pending.

## Complete new-text and integration reading

Read the new introduction, computations, discussion, bibliography, source record and definitive coverage map in full. Compared all previously accepted mathematical section files against stage05-accepted: the only substantive addition is the explicitly attributed classical small-mode comparison in07; the entire higher-reach section moves byte-for-byte into14-higher-reach. All other accepted mathematical sections are unchanged.

Checked every public optimum and displayed coarsening interval against the independent exact outputs. Read the experiment generator, offline checker, and display generator. Requested and confirmed drafting fixes: binary uniform one-switch oracle1/6; archived schedule validation, separate uniform-grid word enumeration, precise arithmetic complexity in the abstract, omission of unnecessary support language from the heavy-mode synopsis, and a figure legend separating the geometric one-sided term from the actual full uniform-input optimum. Visually inspected both standalone figures; their discrete-grid and minimax scopes are now explicit.

The finite-grid uniform n3/s2 comparison1/6 has a separate analytic proof, avoiding misuse of the accepted k<n uniform theorem. The source perturbation bounds, same-grid budget comparisons, nested fine-grid intervals, and runtime scope are consistently stated. The experiment does not imply nonlinear state or economic performance.

The stage6 author is finishing verification and layout. No additional mathematical issue has been identified in the current new text. Formal five-reviewer assessment remains required.

## Frozen-draft validation

After author handoff, froze stage06-round01 (161 files) and dispatched five independent reviewers. A fresh root relocation ran verification/run_all.py successfully: every portable proof, artifact-integrity, exact-algorithm and archived-experiment suite passed. A clean LaTeX/BibTeX build from that relocation also passed with no warnings, undefined references, or overfull/underfull boxes. Logs are in process/stage06-root; no frozen file was changed.

Visually inspected representative frozen opening, synopsis, exact-table and bibliography pages in addition to both standalone scientific figures. The table entries, strict versus closed interval brackets, notation and source-data qualifications agree with the independently computed values. The updated verifier directly checks archived schedule witnesses, and all new standalone entry points reject disabled assertions.
