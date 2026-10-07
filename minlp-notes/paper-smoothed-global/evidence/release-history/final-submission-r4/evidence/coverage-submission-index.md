# Final coverage index

This index supplies final-source locations for the 69 entries in the reviewed
topic inventory. It carries forward the roles, proof chains and exclusions in
`coverage-final.md` and `coverage-amendment-r2.md`; it is not a claim of
69 original results or a new independent mathematical review. Several entries
share a statement or proof. The first stable label for each entry is linked
below; the detailed amendment identifies the remaining interfaces.

The final snapshot is `snapshots/final-submission-r4/`, with manifest SHA256
`0c48e0cda82b7a4f25be956980b536577311fa71d40220cc35c8d1a47d0af061`.
All 410 labels and 138 proof signatures survive from the reviewed mathematical
revision. The expanded Appendix C root-count proof and Appendix F numerical
ledger have their separate independent passes. All 20 TeX files equal the
reviewed literature-integrated R2 files. Final bibliography display repairs
change no statement or proof.

| Inventory ID | Carried role | First stable statement/interface label | Final source location |
| --- | --- | --- | --- |
| F1 | Elementary reused rounding | `lem:count:rounding` | [sections/03-counting.tex](/workspace/minlp-notes/paper-smoothed-global/sections/03-counting.tex:175) |
| F2 | Reused counting infrastructure | `lem:count:interval` | [sections/03-counting.tex](/workspace/minlp-notes/paper-smoothed-global/sections/03-counting.tex:62) |
| F3 | Extension: quantitative growth tail | `thm:count:growth-tail` | [sections/03-counting.tex](/workspace/minlp-notes/paper-smoothed-global/sections/03-counting.tex:359) |
| F4 | Reused quadratic finite-law tool | `lem:qp:growth-sections` | [sections/04-quadratic.tex](/workspace/minlp-notes/paper-smoothed-global/sections/04-quadratic.tex:243) |
| F5 | Elementary reused replacement tool | `lem:count:transfer` | [sections/03-counting.tex](/workspace/minlp-notes/paper-smoothed-global/sections/03-counting.tex:294) |
| F6 | Classical QE application | `lem:count:finite-tails` | [sections/03-counting.tex](/workspace/minlp-notes/paper-smoothed-global/sections/03-counting.tex:417) |
| F7 | Reused/extended active-margin tool | `lem:count:finite-tails` | [sections/03-counting.tex](/workspace/minlp-notes/paper-smoothed-global/sections/03-counting.tex:417) |
| F8 | Extension of classical discrete isolation | `lem:qp:isolation` | [sections/04-quadratic.tex](/workspace/minlp-notes/paper-smoothed-global/sections/04-quadratic.tex:447) |
| F9 | Elementary reused rational fallback | `lem:qp:face` | [sections/04-quadratic.tex](/workspace/minlp-notes/paper-smoothed-global/sections/04-quadratic.tex:327) |
| F10 | Reused/extended algebraic fallback | `thm:count:fallback` | [sections/03-counting.tex](/workspace/minlp-notes/paper-smoothed-global/sections/03-counting.tex:540) |
| F11 | Classical weak-optimization application | `lem:sp:gls` | [appendices/C-sparse.tex](/workspace/minlp-notes/paper-smoothed-global/appendices/C-sparse.tex:98) |
| F12 | Elementary reused localization | `prop:sp:prune` | [sections/05-sparse.tex](/workspace/minlp-notes/paper-smoothed-global/sections/05-sparse.tex:397) |
| F13 | Classical tube theorem plus extension to grid | `prop:rec:tube` | [sections/07-recourse.tex](/workspace/minlp-notes/paper-smoothed-global/sections/07-recourse.tex:599) |
| F14 | Extension: finite sampler/count composition | `lem:count:gauss-sampler` | [sections/03-counting.tex](/workspace/minlp-notes/paper-smoothed-global/sections/03-counting.tex:318) |
| F15 | Classical algebraic methods, developed constructive interface | `thm:int:solver` | [sections/08-integer.tex](/workspace/minlp-notes/paper-smoothed-global/sections/08-integer.tex:64) |
| F16 | Elementary reused budget accounting | `lem:count:rare-fallback` | [sections/03-counting.tex](/workspace/minlp-notes/paper-smoothed-global/sections/03-counting.tex:472) |
| F17 | Classical external oracles | `prop:qp:primitives` | [sections/04-quadratic.tex](/workspace/minlp-notes/paper-smoothed-global/sections/04-quadratic.tex:60) |
| F18 | Elementary consequence | `prop:model:regret` | [sections/02-model.tex](/workspace/minlp-notes/paper-smoothed-global/sections/02-model.tex:430) |
| A0 | Reused foundation and deterministic extension | `lem:qp:normalize` | [sections/04-quadratic.tex](/workspace/minlp-notes/paper-smoothed-global/sections/04-quadratic.tex:101) |
| A1 | Extension: two-inertia smoothed composition | `thm:qp:two` | [sections/04-quadratic.tex](/workspace/minlp-notes/paper-smoothed-global/sections/04-quadratic.tex:261) |
| A2 | Extension: aligned exact closure composition | `thm:qp:aligned` | [sections/04-quadratic.tex](/workspace/minlp-notes/paper-smoothed-global/sections/04-quadratic.tex:616) |
| A3 | Extension: uniform ambient variant | `thm:qp:uniform` | [sections/04-quadratic.tex](/workspace/minlp-notes/paper-smoothed-global/sections/04-quadratic.tex:595) |
| A4 | Extension: Gaussian-like ambient variant | `thm:qp:gauss` | [sections/04-quadratic.tex](/workspace/minlp-notes/paper-smoothed-global/sections/04-quadratic.tex:560) |
| A5 | Extension: uniform ambient mixed QP | `thm:qp:uniform` | [sections/04-quadratic.tex](/workspace/minlp-notes/paper-smoothed-global/sections/04-quadratic.tex:595) |
| A6 | Extension: Gaussian-like mixed QP | `thm:qp:gauss` | [sections/04-quadratic.tex](/workspace/minlp-notes/paper-smoothed-global/sections/04-quadratic.tex:560) |
| A7 | Extension: separable mixed recourse | `def:qp:sep` | [sections/04-quadratic.tex](/workspace/minlp-notes/paper-smoothed-global/sections/04-quadratic.tex:753) |
| A8 | Extension: anisotropic Gaussian separable recourse | `lem:qp:aniso` | [sections/04-quadratic.tex](/workspace/minlp-notes/paper-smoothed-global/sections/04-quadratic.tex:837) |
| A9 | Extension: integer lattice exactness | `thm:int:lowrank` | [sections/08-integer.tex](/workspace/minlp-notes/paper-smoothed-global/sections/08-integer.tex:684) |
| B1 | Extension: sparse search composition | `lem:sp:cells` | [sections/05-sparse.tex](/workspace/minlp-notes/paper-smoothed-global/sections/05-sparse.tex:207) |
| B2 | Specialization: sparse quadratic closure | `cor:sp:qp` | [sections/05-sparse.tex](/workspace/minlp-notes/paper-smoothed-global/sections/05-sparse.tex:1071) |
| B3 | Extension: sparse fixed-degree polynomial closure | `thm:sp:main` | [sections/05-sparse.tex](/workspace/minlp-notes/paper-smoothed-global/sections/05-sparse.tex:138) |
| B4 | Extension/specialization: explicit graphs | `thm:con:graph` | [sections/06-constraints.tex](/workspace/minlp-notes/paper-smoothed-global/sections/06-constraints.tex:223) |
| B5 | Extension: implicit graphs | `thm:con:graph` | [sections/06-constraints.tex](/workspace/minlp-notes/paper-smoothed-global/sections/06-constraints.tex:223) |
| B6 | Extension: simplex domains | `thm:con:simplex` | [sections/06-constraints.tex](/workspace/minlp-notes/paper-smoothed-global/sections/06-constraints.tex:587) |
| B7 | Specialization: continuous orders | `thm:con:order` | [sections/06-constraints.tex](/workspace/minlp-notes/paper-smoothed-global/sections/06-constraints.tex:700) |
| B8 | Extension: binary/continuous mixed orders | `thm:con:order` | [sections/06-constraints.tex](/workspace/minlp-notes/paper-smoothed-global/sections/06-constraints.tex:700) |
| B9 | Specialization: actuator dynamics | `thm:con:actuator` | [sections/06-constraints.tex](/workspace/minlp-notes/paper-smoothed-global/sections/06-constraints.tex:491) |
| B10 | Elementary extension of reused deterministic filter | `prop:sp:conditional` | [sections/05-sparse.tex](/workspace/minlp-notes/paper-smoothed-global/sections/05-sparse.tex:598) |
| C1 | Extension: exact quadratic recourse | `thm:rec:qp` | [sections/07-recourse.tex](/workspace/minlp-notes/paper-smoothed-global/sections/07-recourse.tex:337) |
| C2 | Specialization using classical forest oracle | `cor:rec:forest` | [sections/07-recourse.tex](/workspace/minlp-notes/paper-smoothed-global/sections/07-recourse.tex:365) |
| C3 | Extension: certified polynomial recourse | `thm:rec:poly` | [sections/07-recourse.tex](/workspace/minlp-notes/paper-smoothed-global/sections/07-recourse.tex:432) |
| C4 | Limitation/separation example | `prop:rec:rank` | [sections/07-recourse.tex](/workspace/minlp-notes/paper-smoothed-global/sections/07-recourse.tex:480) |
| C5 | Extension: native integer recourse | `thm:int:native` | [sections/08-integer.tex](/workspace/minlp-notes/paper-smoothed-global/sections/08-integer.tex:175) |
| C6 | Extension: implicit native-core variant | `cor:int:native-implicit` | [sections/08-integer.tex](/workspace/minlp-notes/paper-smoothed-global/sections/08-integer.tex:225) |
| C7 | Classical oracle and elementary certificate | `prop:int:hs` | [sections/08-integer.tex](/workspace/minlp-notes/paper-smoothed-global/sections/08-integer.tex:242) |
| C8 | Extension: strongly convex core-only recourse | `thm:rec:core-only` | [sections/07-recourse.tex](/workspace/minlp-notes/paper-smoothed-global/sections/07-recourse.tex:528) |
| C9 | Specialization: interior integer flows | `thm:int:flow-interior` | [sections/08-integer.tex](/workspace/minlp-notes/paper-smoothed-global/sections/08-integer.tex:370) |
| C10 | Extension: deterministic all-optimal-flow certificate | `lem:int:proximity` | [sections/08-integer.tex](/workspace/minlp-notes/paper-smoothed-global/sections/08-integer.tex:416) |
| C11 | Extension: boundary integer flows | `thm:int:flow-boundary` | [sections/08-integer.tex](/workspace/minlp-notes/paper-smoothed-global/sections/08-integer.tex:460) |
| C12 | Specialization: bilinear flow coupling | `cor:int:bilinear` | [sections/08-integer.tex](/workspace/minlp-notes/paper-smoothed-global/sections/08-integer.tex:489) |
| C13 | Extension: TU integer recourse | `thm:int:tu` | [sections/08-integer.tex](/workspace/minlp-notes/paper-smoothed-global/sections/08-integer.tex:514) |
| D1 | Extension: strong-field QP composition | `thm:int:strong-field` | [sections/08-integer.tex](/workspace/minlp-notes/paper-smoothed-global/sections/08-integer.tex:588) |
| D2 | Extension: strong-field polynomial composition | `thm:int:strong-field` | [sections/08-integer.tex](/workspace/minlp-notes/paper-smoothed-global/sections/08-integer.tex:588) |
| X1 | Limitation of specified global-error retention rule | `thm:lim:width` | [sections/09-boundaries.tex](/workspace/minlp-notes/paper-smoothed-global/sections/09-boundaries.tex:100) |
| X2 | Reused limitation/star examples | `prop:lim:local` | [sections/09-boundaries.tex](/workspace/minlp-notes/paper-smoothed-global/sections/09-boundaries.tex:228) |
| X3 | Limitation of ambient count surrogate | `thm:lim:ambient` | [sections/09-boundaries.tex](/workspace/minlp-notes/paper-smoothed-global/sections/09-boundaries.tex:362) |
| X4 | Conditional complexity limitation and counterexample | `thm:lim:constraints` | [sections/09-boundaries.tex](/workspace/minlp-notes/paper-smoothed-global/sections/09-boundaries.tex:420) |
| X5 | Limitation of parameterization premises | `ex:con:graph-curv` | [sections/06-constraints.tex](/workspace/minlp-notes/paper-smoothed-global/sections/06-constraints.tex:390) |
| X6 | Limitation of single-flow boundary certificate | `prop:lim:flow` | [sections/09-boundaries.tex](/workspace/minlp-notes/paper-smoothed-global/sections/09-boundaries.tex:761) |
| X7 | Limitation of convex-patch closure | `ex:rec:fiber` | [sections/07-recourse.tex](/workspace/minlp-notes/paper-smoothed-global/sections/07-recourse.tex:673) |
| X8 | Limitation: threshold compatibility | `prop:lim:threshold` | [sections/09-boundaries.tex](/workspace/minlp-notes/paper-smoothed-global/sections/09-boundaries.tex:531) |
| X9 | Limitation of inverse-growth moment proof | `rem:qp:moments` | [sections/04-quadratic.tex](/workspace/minlp-notes/paper-smoothed-global/sections/04-quadratic.tex:299) |
| X10 | Limitation: finite atom requires fallback | `ex:qp:atom` | [sections/04-quadratic.tex](/workspace/minlp-notes/paper-smoothed-global/sections/04-quadratic.tex:537) |
| X11 | Limitation: matching corner labels unsound | `ex:qp:corner-labels` | [sections/04-quadratic.tex](/workspace/minlp-notes/paper-smoothed-global/sections/04-quadratic.tex:468) |
| X12 | Limitation: rational pieces insufficient | `def:qp:sep` | [sections/04-quadratic.tex](/workspace/minlp-notes/paper-smoothed-global/sections/04-quadratic.tex:753) |
| X13 | Limitation: premature binary exposure | `ex:con:premature` | [sections/06-constraints.tex](/workspace/minlp-notes/paper-smoothed-global/sections/06-constraints.tex:776) |
| X14 | Limitation: release needs two-sided core ball | `ex:rec:weak` | [sections/07-recourse.tex](/workspace/minlp-notes/paper-smoothed-global/sections/07-recourse.tex:691) |
| X15 | Reused companion arithmetic limitations | `thm:lim:posslp` | [sections/09-boundaries.tex](/workspace/minlp-notes/paper-smoothed-global/sections/09-boundaries.tex:700) |
| X16 | Reused deterministic baselines/consequence | `cor:int:grid` | [sections/08-integer.tex](/workspace/minlp-notes/paper-smoothed-global/sections/08-integer.tex:324) |

The verification here was a targeted Python check of exact-once IDs, label
existence, final line numbers and the unchanged label/proof catalogs. It did
not rerun experiments or broaden any prior reviewer's verdict.
