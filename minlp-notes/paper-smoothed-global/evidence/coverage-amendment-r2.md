# Coverage amendment: mathematical revision R2

**Scoped verdict: no unresolved coverage omission or coverage regression was found.** The 69 in-scope inventory entries retain their actual statements and manuscript proofs or named classical interfaces. The missing comparison specifics previously recorded under O1, O7 and O8 are now explicit in the actual R2 text. The separate exact-active-coordinate comparison noted under X15 is covered by the same O8 repair. These were comparison omissions, not missing principal proofs.

This amendment carries forward [coverage-final.md](coverage-final.md), including its roles, limitations, overlap and E1–E10/A10/D3 dispositions, except for the comparison omissions expressly closed below. The inventory is F1–F18, A0–A9, B1–B10, C1–C13, D1–D2 and X1–X16: **69 coverage entries, not 69 original results**. Elementary tools, classical methods, reused infrastructure, extensions, specializations and limitations remain identified as such. The three supplementary analytical developments—shared-root coordinate/value conversion, qualified universal resolution, and fixed-degree piecewise-polynomial integer unaries—remain integrated within the established proof chain without additional novelty counts.

The target is the immutable `snapshots/mathematical-revision-r2/`, captured at `2026-10-06T04:04:44.496806+00:00`. Its manifest SHA-256 is `5bfd6e629b8e2c911e69f514f38003d854f858e0815b85ad5f544ed23be0a89e`. The sole later TeX change inspected is the introductory sign correction discussed below. This is a coverage amendment, not a new independent review of all mathematics or final publication approval. Final source audit, bibliography and a final literature-integrated delivery snapshot are outside this verdict and are not assumed ready. No final delivery hash is claimed.

Read context: `BRIEF.md`, the prior coverage map, `review-disposition-final-r1.md`; the five R1 specialist reports `final-foundations-sol-r1.md`, `final-quadratic-sol-r1.md`, `final-sparse-domain-sol-r1.md`, `final-recourse-integer-sol-r1.md`, and `final-front-boundaries-sol-r1.md`; the focused foundations, quadratic and recourse R2 reports; and `shared-root-universal-independent-sol-r2.md`. The editorial R1 record was also consulted for its scope distinctions. These reports identify repairs and review limits; the coverage conclusions below use the actual frozen sources and comparisons.

## Actual comparison repairs

All locators use the R2 file hashes below. S1 and S2 are the introduction and model.

| Prior omission | Actual R2 location and content | Coverage disposition |
| --- | --- | --- |
| O1: joint-convex specialization | S1:452–454 explicitly credits the exact-arithmetic companion's jointly convex value/selected-core specialization and its lexicographically least optimizer when there is no residual block. The named companion citation is at S1:448–449. | Closed at comparison-presence level. The value/core/coupled/QP and cubic/convexifier comparisons remain. |
| O7: conditioned polynomial and boundary descriptor scope | S1:512–520 credits a Hessian lower bound on free coordinates at a point-growth optimizer, a rational face box with strongly convex restricted objective, the implicit optimizer format, strict complementarity at active continuous bounds, and polynomial dependence on reciprocal-margin bit length. It distinguishes the present finite-noise margin tails and exact same-draw fallback. | Closed at comparison-presence level. No deterministic companion proof is being newly claimed here. |
| O8 and X15's exact-active distinction | S1:476–484 credits exact active-coordinate recognition for a uniformly strongly convex cubic versus polynomial arbitrary point approximation, expanded-minimal-polynomial growth on the path family versus a linear-size recurrence, and specified rational rectangle/active-sign enclosure denominators. S2:370–373 explicitly cites the companion and connects the active-coordinate distinction to the present evaluator. | Closed at comparison-presence level. The limits are scoped to the stated output interfaces and do not exclude compact implicit descriptors. Direct SRS/PosSLP/core-noise proofs remain in S9/AppG. |

These are the supplied Luna-source-verified comparisons as integrated by the root; this coverage check did not independently research or certify their sources. Exact bibliography metadata, source locators and final literature applicability remain the literature owner's work. O2–O6 and all exclusion/supersession scopes carry forward; no companion result is relabelled as an original theorem.

## Actual later sign correction

The frozen R2 introduction at S1:68 still says “minus a concave term”; the quadratic R2 reviewer identifies this as a minor description error. The inspected live `sections/01-introduction.tex:68` says **“plus a concave term with k supplied factor rows”**. Direct comparison with R2 confirms that this single word is the only difference among the 20 scientific TeX files at the inspection time. The corrected working introduction has 545 lines and SHA-256 `166834340f629ad92e0720d15ab16c06b2910af778817c79e8fa5da6f45fa829`. This is the inspected working-file fingerprint, not a frozen or final delivery manifest. The correction agrees with the unchanged `def:qp:sep` model (S4:752) and changes no statement label, proof, perturbation law or bound.

## Frozen R2 file locators

| Alias | File relative to the R2 snapshot | Lines | Actual SHA-256 |
| --- | --- | ---: | --- |
| Main | `main.tex` | 44 | `e22e0015a0b032eedbd618b75c6be0fb8c120f6789e12acb0b9cafc5420b9000` |
| Macros | `macros.tex` | 32 | `ac79fc04907f0edc4f964033bbcfa9c1d4d5b07b36428ad0466c72a34d6c8abd` |
| S0 | `sections/00-abstract.tex` | 27 | `2b1dd7bfef41dd05d68d527afcba9c1526ce5b4ca243d96d926f63b2236bfbc2` |
| S1 | `sections/01-introduction.tex` | 545 | `ff426b32af15073bc6bbe5fa15081600bda1e4b0e05f4c1c6504b0fcdcef8bf8` |
| S2 | `sections/02-model.tex` | 569 | `b2ee85b74131bf95659b085dbfe7976e63746acfccfe1500eb060e088891c8ca` |
| S3 | `sections/03-counting.tex` | 758 | `28141913b9357189bace34ee2f3e5ee19fd9d04fdfdfcbdaab9edeb375f4c7c8` |
| S4 | `sections/04-quadratic.tex` | 909 | `020d70a1f2d3380776aa908dc25a5d9351c126674c0571a74e73a7dab867edd5` |
| S5 | `sections/05-sparse.tex` | 1145 | `df3ef7c7f7c08d415044d9d93e3f9daa9b8a5d6c301954b950c3130c6718f047` |
| S6 | `sections/06-constraints.tex` | 818 | `9467eb72e20f355b3afb70d844bfedcf0a7fe52ba8f53d2483327162ad9db898` |
| S7 | `sections/07-recourse.tex` | 740 | `6dbb5f51199e261d613afbe67a88b4bd9f8f43dfc3c2fd6bb34a22243f659c6b` |
| S8 | `sections/08-integer.tex` | 777 | `b88b511b7201f75c12a4f51d9e39725d5dee823c80ee8981e8cdf1e5b8d6461c` |
| S9 | `sections/09-boundaries.tex` | 825 | `fcc8051f9f19582837624ce11d8db5f49b8a2520ed934bf8870f119815c13761` |
| S10 | `sections/10-discussion.tex` | 146 | `b011835c28d33095c9c2c59a72dea31f42b5a5eb36c2d43e528858f04afa8f2a` |
| AppA | `appendices/A-finite-noise.tex` | 829 | `895d4ce273e88a2ab9e9a7a4196b950a619ffdf829a2033536c43dc59295a6d8` |
| AppB | `appendices/B-quadratic.tex` | 890 | `29d21acfe56716f49e6098efd1f51cb9cd4babe3f114146891728d94ec6f7e2a` |
| AppC | `appendices/C-sparse.tex` | 278 | `a93e0493bd253e24e72b5fa1d903f360f8422a84222ec04d80eed069ca9b2974` |
| AppD | `appendices/D-constraints.tex` | 1080 | `c0b90de5054e469a278c2d09f560ce39a746c5b1025c79ecf4aee75ca0f4e66b` |
| AppE | `appendices/E-recourse.tex` | 894 | `e3bba43cbcfa9cfd373661b350711c3f890ebb73a9994dc6dfc13fae49676e1f` |
| AppF | `appendices/F-integer.tex` | 1131 | `7720acea2407b43cc60844522197094936d3572373ed0759ac2f7611112d69e2` |
| AppG | `appendices/G-boundaries.tex` | 481 | `163333352717c3b090f62924f8a8b90eea63cf7c4fc50bf1da0dafd4556f1553` |

## Carried inventory statements and proofs

The following are the prior exact-once inventory rows with their stable labels and updated R2 line locators. Roles and scope qualifications in the original coverage map carry forward; its O1/O7/O8/X15 outstanding-comparison clauses are superseded by this amendment. A proof location identifies the actual named proof start or its enclosing subsection/inline calculation. Shared statements and proofs legitimately cover several inventory entries.

| ID | Carried role | Actual statement and R2 location | Actual proof/interface and R2 location |
| --- | --- | --- | --- |
| F1 | Elementary reused rounding | `lem:count:rounding` S3:175; `lem:sp:round` S5:333; `lem:con:simplex-round` AppD:399; order rounding AppD:721 | AppA:74; S5:342; AppD:408,721 |
| F2 | Reused counting infrastructure | `lem:count:interval` S3:62; `thm:count:local` S3:104; `cor:count:levels` S3:144 | AppA:8,29,46 |
| F3 | Extension: quantitative growth tail | `thm:count:growth-tail` S3:359 | AppA:238 |
| F4 | Reused quadratic finite-law tool | `lem:qp:growth-sections` S4:243 | AppB:151 |
| F5 | Elementary reused replacement tool | `lem:count:transfer` S3:294 | AppA:140 |
| F6 | Classical QE application | `lem:count:finite-tails` S3:417(a); `thm:count:renegar` AppA:333 | AppA:358 |
| F7 | Reused/extended active-margin tool | `lem:count:finite-tails` S3:417(d); `lem:sp:tails` S5:897; `lem:con:kkt` AppD:216; `lem:con:simplex-tail` AppD:594; `lem:con:order-tail` AppD:977 | AppA:358; S5:910; AppC:19; AppD:225,606,986 |
| F8 | Extension of classical discrete isolation | `lem:qp:isolation` S4:446 | AppB:407 |
| F9 | Elementary reused rational fallback | `lem:qp:face` S4:327; `lem:sp:faces` AppC:226 | AppB:120; AppC:240 |
| F10 | Reused/extended algebraic fallback | `thm:count:fallback` S3:540; `lem:count:shared-root` AppA:441 | AppA:457,566 |
| F11 | Classical weak-optimization application | `lem:sp:gls` AppC:61; `prop:sp:eval` S5:1036 | AppC:96,186; domain uses AppD:74,301,669,1047 |
| F12 | Elementary reused localization | `prop:sp:prune` S5:397; `prop:sp:closure-stop` S5:842; `lem:app:rec:stopping` AppE:346 | S5:409,853; AppE:353 |
| F13 | Classical tube theorem plus extension to grid | `prop:rec:tube` S7:599(c); `it:app:rec:tube` AppE:90 | AppE:582; chart uses AppF:610,808,945 |
| F14 | Extension: finite sampler/count composition | `lem:count:gauss-sampler` S3:318; `lem:qp:gauss-count` S4:725 | AppA:167; AppB:576,639 |
| F15 | Classical algebraic methods, developed constructive interface | `thm:int:solver` S8:64; `cor:int:mixed-solver` S8:136 | `app:int:solver` AppF:23; correctness AppF:241; `lem:int:values` AppF:261/proof274; cost AppF:297; budget AppF:343; mixed AppF:376 |
| F16 | Elementary reused budget accounting | `lem:count:rare-fallback` S3:472; `sec:count:template` S3:604; `def:sp:schedule` S5:926; `lem:sp:rare` S5:949 | AppA:426; S5:954; route budgets AppB:639, S5:990, AppE:401,743, AppF:440,808 |
| F17 | Classical external oracles | `prop:qp:primitives` S4:60; `cor:rec:forest` S7:365; `prop:int:hs` S8:242; `lem:sp:gls` AppC:61 | Cited QP/MIQP/LP interfaces S4:60–83; forest AppE:446; TU adaptation AppF:519; GLS AppC:96 |
| F18 | Elementary consequence | `prop:model:regret` S2:430; `rem:qp:regret` S4:634 | S2:444; calibrated consequences S2:480–526 |
| A0 | Reused foundation and deterministic extension | `lem:qp:normalize` S4:101; `lem:qp:aux` S4:146; `thm:qp:conditioned` S4:195; `cor:qp:conditioned-mixed` S4:228 | AppB:11,93,191,262 |
| A1 | Extension: two-inertia smoothed composition | `thm:qp:two` S4:261 | AppB:282; main calculation S4:280–297 |
| A2 | Extension: aligned exact closure composition | `thm:qp:aligned` S4:615; `lem:qp:pieces` S4:362; `lem:qp:tube` S4:513 | AppB:318,430; `app:qp:main` AppB:639–756 |
| A3 | Extension: uniform ambient variant | `thm:qp:uniform` S4:594 (continuous case); `lem:qp:volume` S4:660 | AppB:539; `lem:qp:sections` AppB:505/proof512; `lem:qp:uniform-count` AppB:556/proof563; AppB:639–756 |
| A4 | Extension: Gaussian-like ambient variant | `thm:qp:gauss` S4:559 (continuous case); `lem:qp:gauss-count` S4:725 | AppB:576; AppB:639–756; sampler AppA:167 |
| A5 | Extension: uniform ambient mixed QP | `thm:qp:uniform` S4:594 (mixed case); `lem:qp:gap` S4:423; `lem:qp:isolation` S4:446 | AppB:378,407,512; AppB:639–756 |
| A6 | Extension: Gaussian-like mixed QP | `thm:qp:gauss` S4:559 (mixed case) | AppB:407,512,576; AppB:639–756 |
| A7 | Extension: separable mixed recourse | `def:qp:sep` S4:752; `lem:qp:scalar` S4:777; `thm:qp:sep` S4:815 | AppB:784,804 |
| A8 | Extension: anisotropic Gaussian separable recourse | `lem:qp:aniso` S4:836; `thm:qp:sep-gauss` S4:853 | AppB:840,858 |
| A9 | Extension: integer lattice exactness | `thm:int:lowrank` S8:684; input S8:654–683 | `app:int:lowrank` AppF:1022; proof AppF:1024–1131 |
| B1 | Extension: sparse search composition | `lem:sp:cells` S5:207; `lem:sp:allowed` S5:250; `lem:sp:dp` S5:278; `lem:sp:round` S5:333; `prop:sp:prune` S5:397; `prop:sp:count` S5:489 | S5:220,254,290,342,409,498 |
| B2 | Specialization: sparse quadratic closure | `cor:sp:qp` S5:1071; `lem:sp:faces` AppC:226 | AppC:240,263; common closure S5:794,853 |
| B3 | Extension: sparse fixed-degree polynomial closure | `thm:sp:main` S5:138; `prop:sp:closure-sound` S5:785; `prop:sp:closure-stop` S5:842; `prop:sp:eval` S5:1036 | S5:794,853,990; AppC:186 |
| B4 | Extension/specialization: explicit graphs | `thm:con:graph` S6:223(E); `lem:con:expand` S6:208 | AppD:9,45 |
| B5 | Extension: implicit graphs | `thm:con:graph` S6:223(I); `lem:con:chart` S6:319; `lem:con:approx` S6:346; `def:con:charted` S6:272 | AppD:92,157,199,225,268 |
| B6 | Extension: simplex domains | `thm:con:simplex` S6:587; `def:con:simplex` S6:554 | `app:con:simplex` AppD:386; AppD:408,449,531,606,644 |
| B7 | Specialization: continuous orders | `thm:con:order` S6:700 with all coordinates continuous; `eq:con:orderbound` S6:716 | AppD:721,767,820,868,929,986,1026 |
| B8 | Extension: binary/continuous mixed orders | `thm:con:order` S6:700; `ex:con:premature` S6:776 | `app:con:order` AppD:700; AppD:767,820,868,929,986,1026 |
| B9 | Specialization: actuator dynamics | `thm:con:actuator` S6:491; `ex:con:dyn` S6:524; `ex:con:actuator` S6:539 | `app:con:actuator` AppD:333; proof AppD:335 |
| B10 | Elementary extension of reused deterministic filter | `prop:sp:conditional` S5:598; `eq:sp:conditional` S5:625; front corollary `prop:lim:conditional` S9:297 | S5:633–693; S9:314 |
| C1 | Extension: exact quadratic recourse | `thm:rec:qp` S7:337; `prop:rec:search` S7:211; `lem:rec:exclusion` S7:261; `lem:rec:closure` S7:292 | AppE:145,205,225,401 |
| C2 | Specialization using classical forest oracle | `cor:rec:forest` S7:365 | AppE:446 |
| C3 | Extension: certified polynomial recourse | `thm:rec:poly` S7:432; `lem:rec:convex-oracle` S7:402 | AppE:251,401; shared search AppE:145 |
| C4 | Limitation/separation example | `prop:rec:rank` S7:480 | AppE:460 |
| C5 | Extension: native integer recourse | `thm:int:native` S8:175; `eq:int:label` S8:207 | `app:int:native` AppF:387; competing labels AppF:404,428; theorem AppF:440 |
| C6 | Extension: implicit native-core variant | `cor:int:native-implicit` S8:225 | AppF:479 |
| C7 | Classical oracle and elementary certificate | `prop:int:hs` S8:242; `lem:int:potentials` S8:267 | AppF:519,536 |
| C8 | Extension: strongly convex core-only recourse | `thm:rec:core-only` S7:528; `prop:rec:tube` S7:599; `prop:rec:release` S7:631; `lem:app:rec:lift` AppE:497 | AppE:510,557,582,662,743 |
| C9 | Specialization: interior integer flows | `thm:int:flow-interior` S8:370 | AppF:610 |
| C10 | Extension: deterministic all-optimal-flow certificate | `lem:int:proximity` S8:416; `thm:int:face` S8:431; `lem:int:face-general` AppF:699 | AppF:674,710,739 |
| C11 | Extension: boundary integer flows | `thm:int:flow-boundary` S8:460; `lem:int:margin` AppF:756; `lem:int:normal` AppF:784 | AppF:765,795,808 |
| C12 | Specialization: bilinear flow coupling | `cor:int:bilinear` S8:489; `lem:int:affine-margin` AppF:868 | AppF:875,886 |
| C13 | Extension: TU integer recourse | `thm:int:tu` S8:514; `cor:int:tu-ineq` S8:549; `lem:int:tu-dual` AppF:907 | AppF:922,945 |
| D1 | Extension: strong-field QP composition | `thm:int:strong-field` S8:588 (quadratic case); `eq:int:sf-regime` S8:608 | `app:int:strong-field` AppF:964; proof AppF:966–1021 |
| D2 | Extension: strong-field polynomial composition | `thm:int:strong-field` S8:588 (fixed-degree case); `cor:int:mixed-solver` S8:136 | AppF:966–1021; component solver AppF:376 |
| X1 | Limitation of specified global-error retention rule | `thm:lim:width` S9:100 | S9:131 |
| X2 | Reused limitation/star examples | `prop:lim:local` S9:228; `ex:rec:star` S7:153 | S9:241; AppE:829 |
| X3 | Limitation of ambient count surrogate | `thm:lim:ambient` S9:362; `prop:qp:ambient-barrier` S4:690; `prop:qp:fiber-sharp` S4:674 | `app:lim:ambient` AppG:5–176; fiber AppB:760 |
| X4 | Conditional complexity limitation and counterexample | `thm:lim:constraints` S9:420; `ex:lim:coupled` S9:489 | S9:446; inline S9:489–519 |
| X5 | Limitation of parameterization premises | `ex:con:graph-curv` S6:390 | Inline S6:390–405 |
| X6 | Limitation of single-flow boundary certificate | `prop:lim:flow` S9:761 | `app:lim:flow` AppG:440–481 |
| X7 | Limitation of convex-patch closure | `ex:rec:fiber` S7:673 | AppE:859 |
| X8 | Limitation: threshold compatibility | `prop:lim:threshold` S9:531; `rem:lim:dk` S9:565 | S9:544; worked witness S9:565–583 |
| X9 | Limitation of inverse-growth moment proof | `rem:qp:moments` S4:299 | Inline S4:300–323; capped moment AppB:282 |
| X10 | Limitation: finite atom requires fallback | `ex:qp:atom` S4:536; supporting `ex:model:tie` S2:535; `ex:count:atom` S3:245 | Inline S4:536–548, S2:535–569, S3:245–270 |
| X11 | Limitation: matching corner labels unsound | `ex:qp:corner-labels` S4:467 | Inline S4:467–478 |
| X12 | Limitation: rational pieces insufficient | `def:qp:sep` S4:752; example S4:770–775 | Inline S4:770–775 |
| X13 | Limitation: premature binary exposure | `ex:con:premature` S6:776 | Inline S6:776–785 |
| X14 | Limitation: release needs two-sided core ball | `ex:rec:weak` S7:691; `ex:rec:two-sided` S7:702 | AppE:882 |
| X15 | Reused companion arithmetic limitations | `thm:lim:posslp` S9:700(a–c); `prop:lim:value` S9:615 | `app:lim:posslp` AppG:177; SRS AppG:248–335; PosSLP AppG:336–423; core consequences AppG:424–438; regularization S9:638 |
| X16 | Reused deterministic baselines/consequence | `cor:int:grid` S8:324; binary/listed baseline S8:730–741 | AppF:561; inline zonotope/Minkowski explanation S8:730–741 |

The supplementary shared-root proof is now `lem:count:shared-root` AppA:441, proof AppA:457, with strengthened `thm:count:fallback` S3:540 and proof AppA:566. The universal-law corollary is `cor:count:universal-law` S3:665, with `app:count:universal` AppA:677 and proof AppA:679. The generalized lattice statement/proof are `thm:int:lowrank` S8:684 and `app:int:lowrank` AppF:1022, proof AppF:1024. These are carried results, not new amendment claims.

## Review evidence and scope of this verdict

The five R1 specialists are now actual reports, so the prior map's “reviews in progress” status is historical. The sparse/domain report passes its assigned internal proof chain under its stated premises. The front/boundary report finds no substantive proof defect but retains minor presentation/comparison/source qualifications. Foundations R2 closes F1–F4 against this R2 snapshot. Quadratic R2 closes Q1/Q2 against R2 and identifies the sign wording subsequently corrected as above. The recourse/integer and shared-root R2 reports close the normalization and envelope-computation findings against the earlier `integration-repairs-r1` capture; they do not purport to approve every later R2 edit. No report is enlarged into complete-paper submission approval.

This coverage check inspected the corresponding actual R2 repair passages: S3:690–700 and AppA:706–714 charge evaluation of the supplied integer envelope; S2:283–285 and 381–385 retain sampled-height/parameter costs; S3:210–212 supplies the empty-retained-set convention; AppA:239–249 uses finite growth thresholds and handles singletons; AppB:768–772 includes the scalar fiber branch; AppF:60–63 clears the root polynomial denominator before the value routine. S8:617–623 and AppF:978–982 explicitly identify the unpinned bad event; the last S8 paragraph restricts a common root to one completion/component. S1:308–316, S9:10–14 and S10:83–95 contain the corrected record-size and probabilistic-scope qualifications. These changes preserve rather than remove the covered theorem/proof chain. They are presence/contract checks, not a fresh independent derivation of those arguments.

## Targeted checks actually run

- Scoped `rg --files`, `cat`, `sed -n`, and `nl -ba ... | sed -n ...` read the specified evidence and actual comparison/repair passages. No bibliography or literature search was performed.
- Inline `python3 - <<'PY'` with `pathlib`, `json` and `hashlib` recomputed both immutable manifests' file hashes and line counts: **20/20 matched in R1 and 20/20 matched in R2**. The R1 manifest fingerprint was `c439935acba1b1adeb5d883e3718b1416f71ca45839ab672f5545060343d92cf`; the R2 fingerprint is above.
- Inline `python3 - <<'PY'` with `re` checked the prior table's ID set/count/uniqueness and compared frozen label and proof catalogs: **69 exact-once IDs; all 149 previously cited manuscript labels survive; the complete 410-label set and all 138 proof-environment signatures are unchanged**. No statement/proof label was removed. Named proof catalogs plus the actual changed-file diff were checked; label survival alone was not treated as mathematical approval.
- Inline `python3 - <<'PY'` with `difflib` inspected every R1→R2 changed scientific file and compared live TeX to R2. The latter comparison found only the sign correction recorded above. It also supplied the shifted locators in this amendment. The final report-only check passed: 69 exact-once amendment rows, 148 cited manuscript labels present, all explicit label/start-line locators matched, all start lines in range, all 20 frozen fingerprints recorded, and clean newline/whitespace/control-character checks. The prior record's broader 149-label catalog was checked separately as stated above.

No unresolved coverage omission remains in this scoped amendment. Final literature/source contracts, bibliography identities/completeness, the later literature-integrated source and its delivery manifest, final layout and overall submission readiness remain outside this coverage verdict. No experiments, saved diagnostics, builds, project-wide checks, CI inspection, KB edits, literature research, other-paper edits or delegation were performed. Only `evidence/coverage-amendment-r2.md` was written; the prior coverage record and both immutable snapshots were preserved.
