# Final inventory coverage against the integrated mathematical snapshot

This is a statement/proof presence and scope map, not an independent mathematical review, a priority determination, or submission approval. All **69 in-scope IDs** occur exactly once in the table: F1–F18, A0–A9, B1–B10, C1–C13, D1–D2 and X1–X16. They include elementary consequences, classical tools, reused results, extensions, specializations and limitations; they are not 69 original novelties.

The map uses only the immutable `evidence/snapshots/integrated-mathematical-draft-r1/`, captured at `2026-10-06T03:49:31.635993+00:00`. Every line locator below refers to the SHA-256 file catalog below, not to live files or an older snapshot. “Present” means a matching actual statement and manuscript proof, or an explicitly named classical interface, were located. It does not mean the argument passed final independent review.

Readset: BRIEF, inventory, architecture, integration-contract, integration-decisions, the old partial coverage-draft, all four `*-sol-final.md` author reports, root-integration-to-final-math, the frozen statement/proof catalog and relevant actual passages, and the supplied Luna `literature-preliminary.md` companion audit. The old coverage gaps A0, B10, X8, X15 and X16 are replaced by their current actual locators below. Appendices B, D and F are all present. Shared-root/value conversion, universal resolution and the lattice extension are integrated proofs, mapped separately after the inventory table.

Coverage of the 69 entries at statement/proof level is complete. Specific companion comparison details remain outstanding under O1/O7/O8 below. The five final mathematical reviews were in progress when this mapping was assigned; this record does not mark any as passed in the absence of its final report. Prior reviews and author responses do not approve this snapshot. Bibliographic identities, precise classical/companion locators and the final Luna audit remain pending separately.

## Frozen file locators

| Alias | Snapshot file | Lines | SHA-256 |
| --- | --- | ---: | --- |
| Main | `main.tex` | 44 | `e22e0015a0b032eedbd618b75c6be0fb8c120f6789e12acb0b9cafc5420b9000` |
| Macros | `macros.tex` | 32 | `ac79fc04907f0edc4f964033bbcfa9c1d4d5b07b36428ad0466c72a34d6c8abd` |
| S0 | `sections/00-abstract.tex` | 27 | `2b1dd7bfef41dd05d68d527afcba9c1526ce5b4ca243d96d926f63b2236bfbc2` |
| S1 | `sections/01-introduction.tex` | 524 | `c3b27472e13d0c6a94d1cb6693d264d6ac0f6137c7e64d039bc613eb3d35ba56` |
| S2 | `sections/02-model.tex` | 559 | `0a9267cd7a893497d212e5ccb0fbb6433b6428c4784793dd9fc79ec4f4e38a63` |
| S3 | `sections/03-counting.tex` | 754 | `9818728f37864c878ab2e7d0bb1690bb79e8d53f3a338e2f316e31787692b049` |
| S4 | `sections/04-quadratic.tex` | 909 | `020d70a1f2d3380776aa908dc25a5d9351c126674c0571a74e73a7dab867edd5` |
| S5 | `sections/05-sparse.tex` | 1145 | `df3ef7c7f7c08d415044d9d93e3f9daa9b8a5d6c301954b950c3130c6718f047` |
| S6 | `sections/06-constraints.tex` | 818 | `9467eb72e20f355b3afb70d844bfedcf0a7fe52ba8f53d2483327162ad9db898` |
| S7 | `sections/07-recourse.tex` | 740 | `6dbb5f51199e261d613afbe67a88b4bd9f8f43dfc3c2fd6bb34a22243f659c6b` |
| S8 | `sections/08-integer.tex` | 775 | `27809e4472aa7e53c36e8a211bf91d348f5e25c651d74f75936e9d5df7e3f573` |
| S9 | `sections/09-boundaries.tex` | 824 | `1acb7217806f6e53e27a653e9ca36df3adfa3d37cc25a428b45c4770cb8e7bf8` |
| S10 | `sections/10-discussion.tex` | 144 | `d1e176dc2598a40d80d9bc6e13773cd634a713cd6f8e236d5b6e992ebfc49c56` |
| AppA | `appendices/A-finite-noise.tex` | 822 | `4ff3fe30e76466dcc744389e88deaa9759fc19a2709c1104cba89612379c39cd` |
| AppB | `appendices/B-quadratic.tex` | 888 | `c15f3a6f76d6a65ab4b6a4f2e861597d0b1c21f35baa41b1b4f670ad63308d31` |
| AppC | `appendices/C-sparse.tex` | 278 | `a93e0493bd253e24e72b5fa1d903f360f8422a84222ec04d80eed069ca9b2974` |
| AppD | `appendices/D-constraints.tex` | 1080 | `c0b90de5054e469a278c2d09f560ce39a746c5b1025c79ecf4aee75ca0f4e66b` |
| AppE | `appendices/E-recourse.tex` | 894 | `e3bba43cbcfa9cfd373661b350711c3f890ebb73a9994dc6dfc13fae49676e1f` |
| AppF | `appendices/F-integer.tex` | 1127 | `c561d9401b3cc15e9072ab7bffe843f6205a894886fba219a8ee02150a472ef0` |
| AppG | `appendices/G-boundaries.tex` | 481 | `163333352717c3b090f62924f8a8b90eea63cf7c4fc50bf1da0dafd4556f1553` |

## Inventory statement/proof presence

Proof entries give the actual named proof's starting line, the enclosing proof subsection label, or an exact inline calculation range. Where a statement has no separate proof label, the start line identifies its proof; several inventory IDs legitimately share one theorem/proof.

| ID | Role | Actual statement and frozen location | Actual proof/interface location | Scope/disposition |
| --- | --- | --- | --- | --- |
| F1 | Elementary reused rounding | `lem:count:rounding` S3:175; `lem:sp:round` S5:333; `lem:con:simplex-round` AppD:399; order rounding AppD:721 | AppA:74; S5:342; AppD:408,721 | Product/mixed rounding and correlated simplex/common-threshold order rounding are present. |
| F2 | Reused counting infrastructure | `lem:count:interval` S3:62; `thm:count:local` S3:104; `cor:count:levels` S3:144 | AppA:8,29,46 | Independent interval products, nested balanced grids, deterministic domination and finite atoms. |
| F3 | Extension: quantitative growth tail | `thm:count:growth-tail` S3:358 | AppA:238 | Compact lower-semicontinuous domain version, sharp constant; priority is literature-qualified. |
| F4 | Reused quadratic finite-law tool | `lem:qp:growth-sections` S4:243 | AppB:151 | Explicit 8(F+1)^2 section bound and threshold-uniform transfer. |
| F5 | Elementary reused replacement tool | `lem:count:transfer` S3:293 | AppA:140 | Uniform-grid and Kolmogorov product replacement; overlap credited under O4. |
| F6 | Classical QE application | `lem:count:finite-tails` S3:416(a); `thm:count:renegar` AppA:331 | AppA:356 | Two-block scalar-section count for compact mixed semialgebraic domains; classical locator remains a literature audit item. |
| F7 | Reused/extended active-margin tool | `lem:count:finite-tails` S3:416(d); `lem:sp:tails` S5:897; `lem:con:kkt` AppD:216; `lem:con:simplex-tail` AppD:594; `lem:con:order-tail` AppD:977 | AppA:356; S5:910; AppC:19; AppD:225,606,986 | All box, graph, simplex and order variants now have proofs. Equality-budget multipliers are excluded from nonnegative inequality margins. |
| F8 | Extension of classical discrete isolation | `lem:qp:isolation` S4:446 | AppB:407 | Native integer widths, arbitrary label costs, grid atoms and Kolmogorov variant; conditional application fixes continuous noise. |
| F9 | Elementary reused rational fallback | `lem:qp:face` S4:327; `lem:sp:faces` AppC:226 | AppB:120; AppC:240 | General bounded polytope row subsets and mixed-box faces; ties/continua included. |
| F10 | Reused/extended algebraic fallback | `thm:count:fallback` S3:539; `lem:count:shared-root` AppA:439 | AppA:455,564 | Shared optimizer-coordinate-and-value root is now constructed; base degree versus added height and Euclidean precision are explicit. Feasible rational approximation is restricted to mixed boxes. |
| F11 | Classical weak-optimization application | `lem:sp:gls` AppC:61; `prop:sp:eval` S5:1036 | AppC:96,186; domain uses AppD:74,301,669,1047 | Relative polytopes, boundary minimizers and point branches; implicit graph feasibility belongs to the exact lift. |
| F12 | Elementary reused localization | `prop:sp:prune` S5:397; `prop:sp:closure-stop` S5:842; `lem:app:rec:stopping` AppE:346 | S5:409,853; AppE:353 | Retained witnesses localize cells under growth; other routes reuse their stated count/closure variants. |
| F13 | Classical tube theorem plus extension to grid | `prop:rec:tube` S7:599(c); `it:app:rec:tube` AppE:90 | AppE:582; chart uses AppF:608,806,943 | Exact C(q,D) tube bound and jitter argument; flow/TU charts reuse it. Published theorem/source version pending audit. |
| F14 | Extension: finite sampler/count composition | `lem:count:gauss-sampler` S3:317; `lem:qp:gauss-count` S4:725 | AppA:167; AppB:576,639 | Bounded rational sampler, Gaussian proxy/frame majorant, capped lattice sum, base support/precision loop. |
| F15 | Classical algebraic methods, developed constructive interface | `thm:int:solver` S8:64; `cor:int:mixed-solver` S8:136 | `app:int:solver` AppF:23; correctness AppF:239; `lem:int:values` AppF:259/proof272; cost AppF:295; budget AppF:341; mixed AppF:374 | Full quotient/critical-limit construction, good-form screening, ties/continua, common-root value and effective constant-base cost. No novelty claim for RUR or critical-point methods. |
| F16 | Elementary reused budget accounting | `lem:count:rare-fallback` S3:471; `sec:count:template` S3:603; `def:sp:schedule` S5:926; `lem:sp:rare` S5:949 | AppA:424; S5:954; route budgets AppB:639, S5:990, AppE:401,743, AppF:438,806 | Base budget precedes thresholds/cap/law. Lattice and strong-field routes terminate without rare fallback; nonlinear boundary precision stays parameter-dependent. |
| F17 | Classical external oracles | `prop:qp:primitives` S4:60; `cor:rec:forest` S7:365; `prop:int:hs` S8:242; `lem:sp:gls` AppC:61 | Cited QP/MIQP/LP interfaces S4:60–83; forest AppE:446; TU adaptation AppF:517; GLS AppC:96 | These are expressly cited tools, not independently re-proved new algorithms. Exact source identities/locators are pending Luna audit. |
| F18 | Elementary consequence | `prop:model:regret` S2:420; `rem:qp:regret` S4:634 | S2:434; calibrated consequences S2:470–516 | Actual support, aligned widths and zero noisy width are respected; original-objective work retains numerical ratios. Strong-field scale cannot generally be calibrated arbitrarily small. |
| A0 | Reused foundation and deterministic extension | `lem:qp:normalize` S4:101; `lem:qp:aux` S4:146; `thm:qp:conditioned` S4:195; `cor:qp:conditioned-mixed` S4:228 | AppB:11,93,191,262 | Normalization, growth transfer, cell counts/packing, rational recovery and deterministic MIQP oracle factor are all present. Supplied factors use attaining witnesses without kernel inclusion. |
| A1 | Extension: two-inertia smoothed composition | `thm:qp:two` S4:261 | AppB:282; main calculation S4:280–297 | Uniform and finite Gaussian-like laws; capped-moment work preserves linear numerical dependence. X9 scopes its failure beyond two directions. |
| A2 | Extension: aligned exact closure composition | `thm:qp:aligned` S4:615; `lem:qp:pieces` S4:362; `lem:qp:tube` S4:513 | AppB:318,430; `app:qp:main` AppB:639–756 | Aligned continuous factor noise, fixed critical-region tubes, every-draw rational completion and same-draw fallback. |
| A3 | Extension: uniform ambient variant | `thm:qp:uniform` S4:594 (continuous case); `lem:qp:volume` S4:660 | AppB:539; `lem:qp:sections` AppB:505/proof512; `lem:qp:uniform-count` AppB:556/proof563; AppB:639–756 | Dependent auxiliary coordinates use complementary-minor volume. Fixed-k polynomial dimension powers remain; no structure-only FPT claim. |
| A4 | Extension: Gaussian-like ambient variant | `thm:qp:gauss` S4:559 (continuous case); `lem:qp:gauss-count` S4:725 | AppB:576; AppB:639–756; sampler AppA:167 | FPT in stated joint structural/numerical parameters with bounded finite law and support loop. |
| A5 | Extension: uniform ambient mixed QP | `thm:qp:uniform` S4:594 (mixed case); `lem:qp:gap` S4:423; `lem:qp:isolation` S4:446 | AppB:378,407,512; AppB:639–756 | Best-other-label exclusions, whole-cell region/gap test and f(n_z) exact convex-MIQP factor. |
| A6 | Extension: Gaussian-like mixed QP | `thm:qp:gauss` S4:559 (mixed case) | AppB:407,512,576; AppB:639–756 | Scalar label isolation and base support loop; h_J≤1 yields support-independent mixed-gap constants. |
| A7 | Extension: separable mixed recourse | `def:qp:sep` S4:752; `lem:qp:scalar` S4:777; `thm:qp:sep` S4:815 | AppB:782,802 | Aligned and ambient uniform cases, unrestricted integer dimension, rational piece coefficients and breakpoints. |
| A8 | Extension: anisotropic Gaussian separable recourse | `lem:qp:aniso` S4:836; `thm:qp:sep-gauss` S4:853 | AppB:838,856 | Full row rank, rational rotation/dyadic scaling, balanced meshes, supplied concave-curvature numerical parameter. |
| A9 | Extension: integer lattice exactness | `thm:int:lowrank` S8:682; input S8:652–681 | `app:int:lowrank` AppF:1018; proof AppF:1020–1127 | Inventory quartics are a specialization of the integrated fixed-degree continuous convex piecewise-polynomial unaries. Arbitrary/dependent/zero rows, k=0, binary-encoded labels, common original-value lattice and no fallback. |
| B1 | Extension: sparse search composition | `lem:sp:cells` S5:207; `lem:sp:allowed` S5:250; `lem:sp:dp` S5:278; `lem:sp:round` S5:333; `prop:sp:prune` S5:397; `prop:sp:count` S5:489 | S5:220,254,290,342,409,498 | Nested native grids, separator min-marginals, global whitelist rounding and witnesses, deterministic retained-count domination. |
| B2 | Specialization: sparse quadratic closure | `cor:sp:qp` S5:1071; `lem:sp:faces` AppC:226 | AppC:240,263; common closure S5:794,853 | Mixed-box every-draw rational optimizer/value, singular faces and exact convex-QP closure. |
| B3 | Extension: sparse fixed-degree polynomial closure | `thm:sp:main` S5:138; `prop:sp:closure-sound` S5:785; `prop:sp:closure-stop` S5:842; `prop:sp:eval` S5:1036 | S5:794,853,990; AppC:186 | Compact implicit patch versus common-root fallback; global trace has expected-size bound; fixed-width polynomial work, not width-FPT. |
| B4 | Extension/specialization: explicit graphs | `thm:con:graph` S6:223(E); `lem:con:expand` S6:208 | AppD:9,45 | Fixed-depth substitution, expanded bags and conditional pullback curvature. Exact lift of free-coordinate output. |
| B5 | Extension: implicit graphs | `thm:con:graph` S6:223(I); `lem:con:chart` S6:319; `lem:con:approx` S6:346; `def:con:charted` S6:272 | AppD:92,157,199,225,268 | Global brackets/floors, certified lower DP, 4E witnesses, bordered KKT tails, charted exact feasibility and point-output branch. |
| B6 | Extension: simplex domains | `thm:con:simplex` S6:587; `def:con:simplex` S6:554 | `app:con:simplex` AppD:386; AppD:408,449,531,606,644 | Coarse vertices and fine feasible corners; block counts; inequality-only margin event; unrestricted equality multipliers; relative evaluator. |
| B7 | Specialization: continuous orders | `thm:con:order` S6:700 with all coordinates continuous; `eq:con:orderbound` S6:716 | AppD:721,767,820,868,929,986,1026 | Sharper B8 transport count specialized to n_c=n and p_c=p supersedes inventory's older chamber count deliberately. |
| B8 | Extension: binary/continuous mixed orders | `thm:con:order` S6:700; `ex:con:premature` S6:776 | `app:con:order` AppD:700; AppD:767,820,868,929,986,1026 | Endpoint-preserving transport; continuous bag size p_c; fix binaries before LP exposure; weighted curvature/closure and paired-noise margin tail. |
| B9 | Specialization: actuator dynamics | `thm:con:actuator` S6:491; `ex:con:dyn` S6:524; `ex:con:actuator` S6:539 | `app:con:actuator` AppD:333; proof AppD:335 | Affine state recurrences and fixed-degree polynomial actuators; positive curvature enclosure; all-fixed trajectories. Nonlinear state recurrences excluded. |
| B10 | Elementary extension of reused deterministic filter | `prop:sp:conditional` S5:598; `eq:sp:conditional` S5:625; front corollary `prop:lim:conditional` S9:296 | S5:633–693; S9:313 | Explicit certified lower/feasible-upper oracle, eta≤a e, incumbent before retention, feasible returned witnesses and p-based product count. Oracle cost is not supplied by this bridge. |
| C1 | Extension: exact quadratic recourse | `thm:rec:qp` S7:337; `prop:rec:search` S7:211; `lem:rec:exclusion` S7:261; `lem:rec:closure` S7:292 | AppE:145,205,225,401 | Box-stable restricted recourse; excluded slabs; core counts; rational output on all draws, including fallback. |
| C2 | Specialization using classical forest oracle | `cor:rec:forest` S7:365 | AppE:446 | Feedback-vertex core leaves residual forest; the cited exact oracle handles tightened boxes. |
| C3 | Extension: certified polynomial recourse | `thm:rec:poly` S7:432; `lem:rec:convex-oracle` S7:402 | AppE:251,401; shared search AppE:145 | Certified global lower values and feasible completions; residual convexity is a sufficient oracle specialization. Empty-core positive accuracy allowance retained. |
| C4 | Limitation/separation example | `prop:rec:rank` S7:480 | AppE:460 | Degree-five merely convex recourse needs high-rank fixed PSD quadratic convexifier; does not contradict the uniformly strong residual Schur convexifier. |
| C5 | Extension: native integer recourse | `thm:int:native` S8:175; `eq:int:label` S8:207 | `app:int:native` AppF:385; competing labels AppF:402,426; theorem AppF:438 | Bound-tightening oracle, infeasible +infinity branch, whole-core common-root completion and exact every-draw output. |
| C6 | Extension: implicit native-core variant | `cor:int:native-implicit` S8:225 | AppF:477 | Ordinary integer label plus core patch, rare exact completion, active margins and evaluation. |
| C7 | Classical oracle and elementary certificate | `prop:int:hs` S8:242; `lem:int:potentials` S8:267 | AppF:517,534 | Endpoint tangent extension/TU oracle adaptation; rational-height marginal potentials, parallel arcs and loops. No polynomial bound for naive repeated unit augmentation. |
| C8 | Extension: strongly convex core-only recourse | `thm:rec:core-only` S7:528; `prop:rec:tube` S7:599; `prop:rec:release` S7:631; `lem:app:rec:lift` AppE:497 | AppE:510,557,582,662,743 | Lipschitz selector, projected-to-full growth, relative active strata, tube, two-sided multiplier release. Modulus is sufficient; companion's broader cubic point result is credited. |
| C9 | Specialization: interior integer flows | `thm:int:flow-interior` S8:370 | AppF:608 | Nonempty residual set; every permitted noise has interior optimal cores; chart/potential tube proof; network-only scope and polynomial sampling precision. |
| C10 | Extension: deterministic all-optimal-flow certificate | `lem:int:proximity` S8:416; `thm:int:face` S8:431; `lem:int:face-general` AppF:697 | AppF:672,708,737 | All tied-flow intervals, losing-label gap and inward derivative over all ties, cycle proximity. |
| C11 | Extension: boundary integer flows | `thm:int:flow-boundary` S8:460; `lem:int:margin` AppF:754; `lem:int:normal` AppF:782 | AppF:763,793,806 | Any core face and persistent ties; parameter-dependent sampling/output/refinement bits retain f_d(k). |
| C12 | Specialization: bilinear flow coupling | `cor:int:bilinear` S8:489; `lem:int:affine-margin` AppF:866 | AppF:873,884 | Empty/nonempty affine zero-set branches, polynomial sampling bits and curvature of core phi alone. |
| C13 | Extension: TU integer recourse | `thm:int:tu` S8:514; `cor:int:tu-ineq` S8:549; `lem:int:tu-dual` AppF:905 | AppF:920,943 | Fixed-degree expanded costs, fixed nonempty TU set, adjacent-slope compact dual, conformal circuits and bounded zero-cost slacks. Distinct from unrestricted continuous TU rounding. |
| D1 | Extension: strong-field QP composition | `thm:int:strong-field` S8:588 (quadratic case); `eq:int:sf-regime` S8:608 | `app:int:strong-field` AppF:962; proof AppF:964–1017 | Derivative enclosures, independent bad sites, elementary component enumeration; every-draw rational output; strong-noise/subcritical premises. |
| D2 | Extension: strong-field polynomial composition | `thm:int:strong-field` S8:588 (fixed-degree case); `cor:int:mixed-solver` S8:136 | AppF:964–1017; component solver AppF:374 | Constant-base algebraic components, common-root values per component, symbolic total value and separate joint refinement. General algebraic-sum comparison is not promised. |
| X1 | Limitation of specified global-error retention rule | `thm:lim:width` S9:99 | S9:130 | Connected exact treewidth, all-draw count/nonclosure and easy endpoint DP. No general algorithmic width lower bound. |
| X2 | Reused limitation/star examples | `prop:lim:local` S9:227; `ex:rec:star` S7:153 | S9:240; AppE:829 | 32-leaf all-draw deletion and positive-definite d^2-leaf error variation; deterministic companion credited. |
| X3 | Limitation of ambient count surrogate | `thm:lim:ambient` S9:361; `prop:qp:ambient-barrier` S4:690; `prop:qp:fiber-sharp` S4:674 | `app:lim:ambient` AppG:5–176; fiber AppB:760 | Local and near-optimal lower counts, continuous/finite laws and shared S4→S9 proof interface; no lower bound on the solver. |
| X4 | Conditional complexity limitation and counterexample | `thm:lim:constraints` S9:419; `ex:lim:coupled` S9:488 | S9:445; inline S9:488–518 | Width-three affine feasibility reduction, all-draw separation, Las Vegas consequence; TU diagonal coordinate-count obstruction. |
| X5 | Limitation of parameterization premises | `ex:con:graph-curv` S6:390 | Inline S6:390–405 | Bounded inverse need not preserve conditional noise independence or retained curvature. |
| X6 | Limitation of single-flow boundary certificate | `prop:lim:flow` S9:760 | `app:lim:flow` AppG:440–481 | Exact 1/16 event, origin growth and no uniform optimal label; chained enumeration cost. |
| X7 | Limitation of convex-patch closure | `ex:rec:fiber` S7:673 | AppE:859 | Rotating fiber and strictly convex interior-unique variant; short certificates, no general solver lower bound. |
| X8 | Limitation: threshold compatibility | `prop:lim:threshold` S9:530; `rem:lim:dk` S9:564 | S9:543; worked witness S9:564–582 | Explicit DK width-two NO family, witness indicator one, exponential 2^(-2r-4) gap and atomic crossing bound are now present. Exact external reduction locator still awaits literature audit. |
| X9 | Limitation of inverse-growth moment proof | `rem:qp:moments` S4:299 | Inline S4:300–323; capped moment AppB:282 | Correct lower integration limit max{1,a_0^(k/2)} and nonempty range; argument limitation only. |
| X10 | Limitation: finite atom requires fallback | `ex:qp:atom` S4:536; supporting `ex:model:tie` S2:525; `ex:count:atom` S3:244 | Inline S4:536–548, S2:525–559, S3:244–269 | Endpoint draw and persistent crossing cell; exact fallback handles the original atom. |
| X11 | Limitation: matching corner labels unsound | `ex:qp:corner-labels` S4:467 | Inline S4:467–478 | Exact slice-value calculation exhibits interior winner, including piece-region validity distinction. |
| X12 | Limitation: rational pieces insufficient | `def:qp:sep` S4:752; example S4:770–775 | Inline S4:770–775 | Irrational sqrt(2) optimum shows rational breakpoints are needed for rational output. |
| X13 | Limitation: premature binary exposure | `ex:con:premature` S6:776 | Inline S6:776–785 | Fix binary labels before LP exposure. |
| X14 | Limitation: release needs two-sided core ball | `ex:rec:weak` S7:691; `ex:rec:two-sided` S7:702 | AppE:882 | Vanishing/weak multiplier and boundary-core derivative examples. |
| X15 | Reused companion arithmetic limitations | `thm:lim:posslp` S9:699(a–c); `prop:lim:value` S9:614 | `app:lim:posslp` AppG:177; SRS AppG:248–335; PosSLP AppG:336–423; core consequences AppG:424–438; regularization S9:637 | Direct SRS width-two bounded-coefficient proof, separate unrestricted PosSLP proof, core-only and deterministic consequences now present and attributed. Exact-active-label versus some-point comparison remains an outstanding overlap detail, see O8. |
| X16 | Reused deterministic baselines/consequence | `cor:int:grid` S8:324; binary/listed baseline S8:728–739 | AppF:559; inline zonotope/Minkowski explanation S8:728–739 | Deterministic fixed-residual core grid error kL/(8m^2)+eta and work are now proved; direct k=0/L=0 branches. Listed-label enumeration is polynomial only at fixed k. |

## Supplementary integrated analytical developments

These rows do not create additional inventory IDs or independent novelty claims.

| Development | Actual statement | Actual proof and application | Role/scope |
| --- | --- | --- | --- |
| Generic shared root for coordinates and value | `lem:count:shared-root` AppA:439; strengthened `thm:count:fallback` S3:539 | AppA:455 and AppA:564, with application AppA:632–655 | Classical algebraic conversion adapted to the required tuple; base-only degree envelope, added-bit height, selected tuple and Euclidean allowance. Covered infrastructure within F10. |
| Complete universal-law budget | `cor:count:universal-law` S3:664; model summary `prop:model:uniform` S2:174 | `app:count:universal` AppA:675, proof AppA:677–822; model proof S2:200 | Elementary effective uniformization of grid/Gaussian schedules. Nonlinear boundary flow/TU requires supplied K; strong-field actual q_i/beta must be recomputed. Geometric/oracle qualifications and numerical factors remain. |
| Fixed-degree piecewise-polynomial integer extension | Input S8:652–681; `thm:int:lowrank` S8:682 | `app:int:lowrank` AppF:1018, proof AppF:1020–1127 | Extension of A9's quartic specialization using discrete convexity/exact evaluation and the original objective lattice. No separate priority claim. |

## Companion overlap dispositions

The companion keys identify unpublished manuscripts. Statements essential here have actual manuscript proofs above; comparison-only results below are cited, not newly claimed. Metadata and precise source locators require Luna's final audit.

| ID | Actual frozen treatment | Disposition and remaining scope |
| --- | --- | --- |
| O1 | Named exact-arithmetic companion at S1:447–466: all-precision value/selected-core, coupled-polytope and QP reconstruction; output selectors/Cauchy names versus finite patches. | Cited comparison. The inventory's joint-convex coordinate specialization is not explicitly identified in the frozen comparison; outstanding specificity, not a missing Route C proof. |
| O2 | Exact rational QP reconstruction credited S1:449–453; present QP routes and C1 have their own proofs. | Cited/reused comparison; do not imply exact core-noise QP is new. Final theorem/version locator pending. |
| O3 | Cubic residual-convex and supplied-convexifier point results S1:453–466, S7:514–574 and S9:593–600. | Cited comparison. Cubic/product-box and cubic/polytope versus fixed-degree/global-convexity scopes, selector, common per-draw factor, and numerical convexifier comparison are explicit. |
| O4 | Shared finite-law/section/projected-growth/fallback overlap credited S1:467–468; actual extended proofs in S3/AppA. | Re-proved reused/extended infrastructure; finite-law model and shared-root algebraic representation expressly not claimed new at S1:438–445. |
| O5 | Named decomposition-aware counterpart S1:475–500 and S5:1130–1145; deterministic filter credited S5:689–693 and S9:313; X2 is re-proved. | Cited/re-proved deterministic mechanics. Weighted/point growth, approximation/exact work, graded/common-grid counts and restricted rETH scope are explicit. Bibliographic locators remain pending. |
| O6 | Named sparse-indicator comparison S1:502–514. | Cited sibling; indicator-only finite-grid penalty noise, every-draw dictionaries, fixed-width/numerical work and NP⊆ZPP consequence kept at its own scope. No screening result imported. |
| O7 | Deterministic conditioned grids/boundary output broadly credited S1:475–500 and S5:1130–1145; actual polynomial patch proofs are present here. | Cited/re-proved counterpart. The specific polynomial Hessian-at-optimum/implicit-patch and deterministic boundary-enclosure comparison requested by the inventory is not spelled out. Outstanding comparison scope; no missing B3/B5 proof. |
| O8 | Output limitations appear S1:307–315 and S2:350–378; X15 is explicitly credited S9:735–748 and AppG:179–182. | Partial specific attribution: the companion's active-sign rectangle and expanded-algebraic-output propositions are not identified/cited at those output-limit passages. The exact-active-label versus approximating-some-point distinction from `prop:points-active` is also absent. Record as outstanding scope/attribution, not as covered by the direct SRS proof. |

The O1/O7/O8 details above were reported to the root. They need a concrete comparison repair or an explicit reasoned exclusion before claiming every inventory comparison obligation complete. No missing principal in-scope statement or promised appendix proof was found by this presence audit. This finding does not adjudicate the proofs' correctness.

## Excluded, superseded and supporting material

| ID | Frozen treatment/disposition |
| --- | --- |
| E1 | Maximal-response approach superseded by F3/F4; not a separate claim. |
| E2 | Summed-response approach superseded by F3/F4; not a separate claim. |
| E3 | Interior strong-recourse antecedent subsumed by C8; selector/growth lift `lem:app:rec:lift` AppE:497/proof510 and core tails AppE:544/proof557 retained; interior remark S7:659. |
| E4 | Weaker value/core Cauchy-name results belong to O1; random-real input model excluded by finite rational model S2:75–235. |
| E5 | Structural affine-fiber/selector exploration supplies no asserted general closure theorem. Rotating-fiber limitation X7 remains. |
| E6 | Exploration conclusions retained through X7/C8, with no extra theorem or generic tractability claim. |
| E7 | Aligned continuous TU feasible rounding is proved at S6:789–805 using integrality and full Hessian allowance. No controlled count/closure for unrestricted continuous TU is claimed; integer-core TU C13 is a different complete theorem. |
| E8 | Random indicator screening excluded as outside topic; sibling indicator model cited under O6. |
| E9 | Deterministic sparse/negative-curvature/general TU targets remain scoped open questions S10:103–144. Universal resolution is now a proved qualified corollary, not the old blanket open question. |
| E10 | Monte Carlo genericity audit is not a paper theorem; deterministic F15 supplies the actual constructive proof. |
| A10 (excluded) | Accuracy-tuned low-rank approximation superseded by A2 exact closure; F2 supporting count retained. |
| D3 (excluded) | Indicator screening outside this topic, as E8; no experiments or screening theorem included. |

## Checks actually performed for this map

1. Scoped reads used `cat`, `sed -n` and `rg -n` on the named evidence and frozen sources. An inline `python3 -` extracted actual TeX labels, proof starts and section headings for the 20-file snapshot. Targeted passages checked the joint main quadratic proof, graph/simplex/order proof catalog, common-root/universal-law proof, lattice statement/proof, direct SRS construction, DK witness, conditional count and deterministic baseline. These were coverage checks, not a new independent full mathematical review.
2. An inline `python3 -` read the snapshot manifest and recomputed SHA-256 and line counts for each listed file. Result: **all 20 hashes and line counts match**, with no mutation of the snapshot.
3. An inline `python3 -` checked this table's exact inventory ID set/count/uniqueness and checked every cited TeX label against the frozen label catalog (excluding the explicitly absent companion-only `prop:points-active`). Result: **pass — 69 exact-once inventory rows, 149 cited frozen labels present, all explicit statement label/line locators matched, and all alias/start-line locators in range**. The explicitly absent companion-only `prop:points-active` is reported as outstanding, not mistaken for a frozen manuscript label.

No literature research, new proof diagnostics, optimization experiments, manuscript/source-note edits, project-wide checks, CI status/log inspection or delegation were performed. Only `evidence/coverage-final.md` was written. Builds, tests and prior author checks were not rerun or counted as verification of this map. Final mathematical approval, final literature audit, bibliography integration and final publication readiness are separate root obligations.
