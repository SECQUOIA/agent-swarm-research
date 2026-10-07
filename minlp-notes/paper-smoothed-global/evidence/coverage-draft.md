# Draft inventory coverage record

Prepared by the independent Sol reviewer on 2026-10-05 local time.
This is a coverage map of a partial manuscript, not approval of its mathematics,
literature claims, or submission readiness. It records **all 69 in-scope inventory
IDs once**: F1–F18, A0–A9, B1–B10, C1–C13, D1–D2, and X1–X16. These IDs
include reused tools, classical oracles, examples, variants, limitations,
and prior/sibling results. They are not 69 independent original contributions.

The source readset was captured at
`2026-10-06T02:49:33.394057+00:00` while the authors were still writing.
Its temporary location is
`/tmp/smoothed-global-coverage-draft-readset/`; its `manifest.json`
records the hashes reproduced below. The map uses this stable readset rather
than mixing line numbers from later author edits. A temporary readset is
a review aid, not a permanent submission dependency. The root must finalize
this record against the complete reviewed manuscript snapshot.

I read `evidence/BRIEF.md`, `evidence/inventory.md`,
`evidence/integration-contract.md`, and
`evidence/integration-decisions.md`. The five retained gaps A0, B10, X8,
X15, and X16 below also reflect the root's later decisions and updated
contract read during this audit. Those decisions require integration;
they are not deliberate exclusions.

**How to read the map**

“Present” means that a matching statement and a manuscript proof or named
classical interface were found. It does not mean the result has passed
independent review. “Proof pending” means the statement is present but its
promised appendix is absent from this capture. “Partial” means some scope or
support is missing; “Pending integration” means the root has required that
missing content. Existing independent-review corrections are mentioned only
when they affect an item's contract. They remain open until the completed
source is checked.

Statement and proof references use actual TeX labels and captured line
numbers. An unlabelled worked example is identified by its enclosing label
and exact lines. Route results called “developed” are candidate contributions
of the present topic, subject to Luna's nearest-source comparison; this map
does not certify priority.

**Immediate integration requirements**

- `appendices/B-quadratic.tex`, `appendices/D-constraints.tex`, and
  `appendices/F-integer.tex` were absent. Consequently much of Route A,
  the nonbox constrained-domain results, the constructive component solver,
  native-integer/flow/TU recourse, lattice closure, and both strong-field
  families have statements but no completed manuscript proof in this
  capture. Outlines and private author reports do not count as those proofs.
- A0 still states only the continuous growth-conditioned theorem. The
  contract requires the deterministic mixed-integer counterpart with the
  convex-MIQP oracle factor.
- B10 is qualitative only. Decision 10 requires the explicit
  conditional-recourse count and its certified lower/upper oracle contract.
  X16 likewise needs the deterministic flow-core grid error/work comparison.
- X8 has the correct generic threshold-crossing proposition but lacks the
  explicit width-two NO family, its exponentially small gap, and source
  attribution required by the updated contract.
- X15 has the PosSLP reduction and the indirect Square Root Sum consequence.
  Its sentence declining structural versions conflicts with decision 11,
  which requires the direct width-two, bounded-coefficient Square Root Sum
  reduction and self-contained proof. PosSLP's construction must keep its
  different structural scope.
- A9 retains the inventory's quartic specialization but has not integrated
  the authorized fixed-degree piecewise-polynomial convex-unary extension.
  The generic fallback/component shared-root value contracts also await the
  repairs already identified by the foundations/integer reviewers.
- O1–O8 lack precise comparator citations and scope distinctions in the
  captured introduction. An unnamed generic “companion” paragraph does not
  satisfy the related-work requirement. The literature owner must supply
  exact bibliographic identities and verify the comparisons.

No inventory item is silently dropped in this record. The partial and pending
rows state the loss explicitly. No scanned submission source refers to a
private research note as its proof; the material problem is absent promised
appendices, not a visible private-path citation. Final integration must preserve
that distinction.

**Captured source locations**

Line references below belong to these hashes. Paths are relative to
`paper-smoothed-global/`. The missing appendix aliases are AppB =
`appendices/B-quadratic.tex`, AppD = `appendices/D-constraints.tex`,
and AppF = `appendices/F-integer.tex`.

| Alias | Submission source at capture | Lines | SHA-256 |
| --- | --- | ---: | --- |
| S0 | `sections/00-abstract.tex` | 28 | `debebb10e59db28f479b90ae50ab7df430a1b106e7b47c3513a6fc91c492f79c` |
| S1 | `sections/01-introduction.tex` | 353 | `e375d03010604128a90abda05cbea31f80b28ec34e78e2533a7284f0de408b6c` |
| S2 | `sections/02-model.tex` | 446 | `2a6115404d2d26b9e11cf61c92153dae6da58140d74c85c25c4159599c2eeef9` |
| S3 | `sections/03-counting.tex` | 575 | `eceb3aa3bd4b9d8e86b32c7f79901d51e2ba2d4ccc9ffdd30bc27f495ba42cbd` |
| S4 | `sections/04-quadratic.tex` | 860 | `d0001f2e7913202b1f8e5f65fc479dc4891ddd2a2bc0b501b934c285095915b4` |
| S5 | `sections/05-sparse.tex` | 926 | `8294f707d601873a4ac3656246c69a370e085a5d1de6c465dabb444b7d707f24` |
| S6 | `sections/06-constraints.tex` | 739 | `cf4859647dbdcb4c0b120d606041ad687f940a26d5ef58d26a0ba31674e3b196` |
| S7 | `sections/07-recourse.tex` | 671 | `93346b701c72cb5ba0bab450b6a859e9cb074a5a2fa91c0c79430a4fa7ca20e2` |
| S8 | `sections/08-integer.tex` | 597 | `7e460d708db99cdaf10278727ccc0ea8db1048c3423364f976392cf814aeff89` |
| S9 | `sections/09-boundaries.tex` | 738 | `bffab517f587685cef0a2d32d5cae2e03927d21495a5b4fbb59680c7f7a2fdb1` |
| S10 | `sections/10-discussion.tex` | 142 | `ef04ec8ac60914a53ee8c3358e3c7348836e1b3f6929aef11dee2a1cd6af67dc` |
| AppA | `appendices/A-finite-noise.tex` | 507 | `05b29ebba8703253ac20498b7c2e10ac362054fe968122267ec7bb25bf9a6644` |
| AppC | `appendices/C-sparse.tex` | 272 | `28ca1ef81b4d15abfacd076ec1b604afea413f5e8e1d0e4eb54e324074a89d21` |
| AppE | `appendices/E-recourse.tex` | 866 | `c9d52e8de3f0a456d7c5ece335b229d7e4fb5f0c2ec2b4dd4c48ce12ef465bc9` |
| AppG | `appendices/G-boundaries.tex` | 380 | `d0665b5d38f40adb46019041ccaf4dd442216082bfb3ce7c21cf9ed1debd9bde` |

**Shared framework and foundations**

| ID | Role and draft status | Actual statement/location | Actual proof or remaining dependency | Coverage qualification |
| --- | --- | --- | --- | --- |
| F1 | Elementary reused tool; **Partial** | `lem:count:rounding` (S3:171) | proof of `lem:count:rounding` (AppA:74); `lem:sp:round` (S5:319) with inline proof S5:328 | Product/mixed-box rounding is present. Correlated simplex and common-quantile order rounding are outlined in S6; their AppD proofs are pending. |
| F2 | Shared counting tool; **Present** | `lem:count:interval` (S3:59); `thm:count:local` (S3:100); `cor:count:levels` (S3:140) | proof of `lem:count:interval` (AppA:8); proof of `thm:count:local` (AppA:29); proof of `cor:count:levels` (AppA:46) | Independent coefficient intervals, deterministic dominating grids, balanced meshes, and the finite atomic allowance are stated and proved. |
| F3 | Developed quantitative probability tool; priority qualified; **Present** | `thm:count:growth-tail` (S3:340) | proof of `thm:count:growth-tail` (AppA:234) | The manuscript uses the stronger lower-semicontinuous compact-domain version and proves sharpness; classical qualitative genericity is separately cited. |
| F4 | Shared quadratic finite-law tool; **Proof pending** | `lem:qp:growth-sections` (S4:222); cross-reference in S3:450 | AppB (`appendices/B-quadratic.tex`) absent; only statement/analysis outline available | The explicit 8(F+1)^2 bound is stated, including mixed labels and Gaussian transfer. Its elementary quadratic proof has not arrived. |
| F5 | Elementary transfer tool reused from companion work; **Present** | `lem:count:transfer` (S3:277) | proof of `lem:count:transfer` (AppA:139) | Product replacement covers finite uniform laws and Kolmogorov-close laws. Specific companion overlap remains to be cited under O4. |
| F6 | Application of classical quantifier elimination; **Present** | `lem:count:finite-tails` (S3:399)(a); `thm:count:renegar` (AppA:327) | proof of `lem:count:finite-tails` (AppA:347) | Two-block, one-scalar section count is proved for reduced objectives on compact mixed semialgebraic domains; binary-encoded native labels are expanded only in the proof format. |
| F7 | Reusable margin analysis from Bézout and isolation; **Partial** | `lem:count:finite-tails` (S3:399)(d); `lem:sp:tails` (S5:707); `lem:sp:bezout` (AppC:13) | proof of `lem:count:finite-tails` (AppA:347)(d); AppC:19 for nonsingular zeros | Mixed-box active-gradient tails are present. Simplex exposure, order paired-noise, and implicit-graph bordered-KKT versions are assigned to the missing AppD. |
| F8 | Generalized native-label isolation tool based on prior isolation; **Proof pending** | `lem:qp:isolation` (S4:399) | AppB (`appendices/B-quadratic.tex`) absent; only statement/analysis outline available | Uniform-grid and Kolmogorov variants are stated, conditioned on continuous noise. Do not count the named prior isolation results as new contributions. |
| F9 | Elementary rational fallback; **Partial** | `lem:qp:face` (S4:295); `lem:sp:faces` (AppC:220) | AppC:234 proves mixed-box face enumeration; AppB (`appendices/B-quadratic.tex`) absent; only statement/analysis outline available | Mixed-box rational fallback is fully written. General bounded (mixed) polytope row-subset enumeration is stated but its AppB proof is pending. |
| F10 | Reused/generalized exact-arithmetic fallback; **Present with contract repair pending** | `thm:count:fallback` (S3:512) | proof of `thm:count:fallback` (AppA:426) | The written theorem and proof return canonical coordinate/value root isolators. The model requires a single shared-root tuple; the authorized conversion supplement is still an evidence-only dependency. Output length wording also needs the existing root review correction. Rational feasible approximants are promised only for mixed boxes. |
| F11 | Application of classical weak convex optimization; **Present** | `lem:sp:gls` (AppC:61); `prop:sp:eval` (S5:837) | AppC:96 proves the general oracle/polytope lemma; proof of `prop:sp:eval` (AppC:180) | General rational relative polytopes and certified approximate oracles are included. Graph outputs use a rational free point and exact dependent lift rather than full rational feasibility. |
| F12 | Elementary localization invariant reused across routes; **Present** | `prop:sp:prune` (S5:380); `prop:sp:closure-stop` (S5:652); `lem:app:rec:stopping` (AppE:335) | S5:392 and S5:663; AppE:342 | Retained witnesses plus growth localize all relevant cells. The deterministic grids and global rounding allowance are explicit. |
| F13 | Application of cited algebraic tube theorem plus finite jitter; **Partial** | `prop:rec:tube` (S7:536)(c); `it:app:rec:tube` (AppE:83) | proof of `prop:rec:tube` (AppE:558) (AppE:558, including the jitter calculation) | The C8 specialization and exact C(q,D) constant are present. The flow/TU reuse and their chart-image formats await AppF. No standalone generic grid-tube lemma is presently labeled. |
| F14 | Finite sampler and Gaussian counting tools; **Partial** | `lem:count:gauss-sampler` (S3:299); `lem:qp:gauss-count` (S4:663) | proof of `lem:count:gauss-sampler` (AppA:166); AppB (`appendices/B-quadratic.tex`) absent; only statement/analysis outline available | The bounded rational sampler proof is present. The Gaussian-weighted lattice sum and the base-only support/precision loop await AppB. Existing foundation-review arithmetic corrections remain to be integrated. |
| F15 | Constructive interface using classical algebraic methods; priority open; **Proof pending** | `thm:int:solver` (S8:63); `cor:int:mixed-solver` (S8:110) | Promised `app:int:solver`, `lem:int:budget`; AppF (`appendices/F-integer.tex`) absent; promised proof labels are not yet defined | Constant-base common-root coordinates are stated, with ties/continua and an explicit budget. The value is currently stated with its own root polynomial; the required same-root value map and epsilon!=0 clarification remain pending. The full constructive proof is required; private evidence is not a substitute. |
| F16 | Elementary accounting and schedule design; **Present with scope qualification** | `lem:count:rare-fallback` (S3:453); `sec:count:template` (S3:548); `def:sp:schedule` (S5:736) | proof of `lem:count:rare-fallback` (AppA:411); `lem:sp:rare` (S5:759) with inline proof S5:764 | The order B, thresholds, J, law is written and applied. S3's blanket template still needs to exclude the lattice/strong-field architectures and preserve parameter-dependent precision for nonlinear boundary flow/TU. |
| F17 | Cited classical external oracles; **Present as cited tools** | `prop:qp:primitives` (S4:55); `cor:rec:forest` (S7:348); `prop:int:hs` (S8:205); `lem:sp:gls` (AppC:61) | Named convex QP/MIQP/LP citations in S4:55; proof of `cor:rec:forest` (AppE:428); HS statement/citation S8:205; GLS proof AppC:96 | Oracle contracts are stated. External attribution and exact source/version verification are Luna's work; the map does not certify that literature audit. |
| F18 | Elementary original-objective corollary; **Present** | `prop:model:regret` (S2:344); `rem:qp:regret` (S4:574) | Inline proof S2:358; applications S2:374–403, S4:574, S8:264 and S8:518 | Regret width is valid for every support vector. Calibrating sigma to epsilon excludes strong-field sufficient conditions; Gaussian-like laws use their actual support radius. Graph evaluation requires an exact feasible lift. Front matter must be checked against these qualified contracts. |

**Route A: small nonconvex auxiliary dimension**

| ID | Role and draft status | Actual statement/location | Actual proof or remaining dependency | Coverage qualification |
| --- | --- | --- | --- | --- |
| A0 | Reused Fenchel/normalization framework and deterministic contrast; **Pending integration** | `lem:qp:normalize` (S4:95); `lem:qp:aux` (S4:137); `thm:qp:conditioned` (S4:186) | AppB (`appendices/B-quadratic.tex`) absent; only statement/analysis outline available | The factor no longer requires kernel inclusion, as authorized. The captured conditioned theorem explicitly assumes n_z=0; the inventory's deterministic MIQP counterpart is required by the updated contract and remains to be stated/proved with its convex-MIQP oracle factor. |
| A1 | Developed route result; **Proof pending** | `thm:qp:two` (S4:240) | Main-text capped-moment calculation S4:258–271; AppB (`appendices/B-quadratic.tex`) absent; only statement/analysis outline available | Both finite uniform and finite Gaussian-like variants retain the linear numerical factor. The conditioned exponent and exact section-count proofs are still needed in AppB. |
| A2 | Developed exact low-rank route result; **Proof pending** | `thm:qp:aligned` (S4:555); `lem:qp:pieces` (S4:330); `def:qp:closure-search` (S4:420); `lem:qp:tube` (S4:453) | AppB (`appendices/B-quadratic.tex`) absent; only statement/analysis outline available | Aligned finite noise, critical-region extraction, every-draw rational output, same-draw fallback, and the attaining-witness upper model are stated. Supplied factors require no extra kernel inclusion. |
| A3 | Developed ambient-uniform route result; **Proof pending** | `thm:qp:uniform` (S4:534); `lem:qp:volume` (S4:600) | Promised `lem:qp:sections` plus volume/closure/budget proofs in AppB; AppB (`appendices/B-quadratic.tex`) absent; only statement/analysis outline available | Ambient coefficients induce dependent auxiliary noise. The main result includes the fixed-k polynomial dimension factor, not an FPT claim. |
| A4 | Developed Gaussian-like route result; **Proof pending** | `thm:qp:gauss` (S4:499); `lem:qp:gauss-count` (S4:663) | AppB (`appendices/B-quadratic.tex`) absent; only statement/analysis outline available; sampler itself is proved in AppA:166 | The actual finite law, Gaussian proxy, frame condition, and FPT numerical parameter are stated. Weighted counts and support-loop accounting are still proof obligations. |
| A5 | Developed smoothed mixed-integer route result; **Proof pending** | `thm:qp:uniform` (S4:534) (mixed case); `lem:qp:gap` (S4:376); `lem:qp:isolation` (S4:399) | AppB (`appendices/B-quadratic.tex`) absent; only statement/analysis outline available | The exact convex MIQP oracle contributes f(n_z), with polished polynomial-length solutions. The best-other-label test is stronger than matching corner winners. |
| A6 | Developed smoothed mixed-integer Gaussian route result; **Proof pending** | `thm:qp:gauss` (S4:499) (mixed case); `lem:qp:gap` (S4:376); `lem:qp:isolation` (S4:399) | AppB (`appendices/B-quadratic.tex`) absent; only statement/analysis outline available | The scalar isolation transfer, mixed section count, and finite support-loop proof remain pending. |
| A7 | Developed separable mixed route result; **Proof pending** | `thm:qp:sep` (S4:753); `lem:qp:scalar` (S4:715); `def:qp:sep` (S4:690) | AppB (`appendices/B-quadratic.tex`) absent; only statement/analysis outline available | Aligned and ambient-uniform cases are stated with unrestricted integer dimension, rational piece coefficients, and rational breakpoints. |
| A8 | Developed anisotropic separable route result; **Proof pending** | `thm:qp:sep-gauss` (S4:791); `lem:qp:aniso` (S4:774) | AppB (`appendices/B-quadratic.tex`) absent; only statement/analysis outline available | Full row rank and supplied curvature beta=alpha||T||^2 are explicit. The row rotation/dyadic scaling and curvature-balanced count await AppB. |
| A9 | Developed exactness-by-lattice route result; **Proof pending; original inventory scope retained** | `thm:int:lowrank` (S8:541); `eq:int:lowrank-model` (S8:528) | Promised `app:int:lowrank`; AppF (`appendices/F-integer.tex`) absent; promised proof labels are not yet defined | Quartic convex unaries, aligned rowwise noise, objective lattice, and no fallback are stated. The subsequently authorized fixed-degree piecewise-polynomial generalization has not entered the theorem; its evidence supplement should not be counted as manuscript coverage. |

**Route B: sparse bags and constrained domains**

| ID | Role and draft status | Actual statement/location | Actual proof or remaining dependency | Coverage qualification |
| --- | --- | --- | --- | --- |
| B1 | Developed sparse-search composition; **Present** | `lem:sp:cells` (S5:193); `lem:sp:allowed` (S5:236); `lem:sp:dp` (S5:264); `lem:sp:round` (S5:319); `prop:sp:prune` (S5:380); `prop:sp:count` (S5:472) | Inline proofs S5:206, 240, 276, 328, 392, 481 | Clipped native-integer grids, separator-key min-marginals, whitelist-preserving global rounding, globally consistent witnesses, and deterministic dominating counts are written. |
| B2 | Quadratic specialization of developed sparse result; **Present** | `cor:sp:qp` (S5:870); `lem:sp:faces` (AppC:220) | proof of `cor:sp:qp` (AppC:257); AppC:234; common sparse closure proofs S5:610, 663 | Every-draw rational output and mixed-box fallback are present. It uses the general degree-two section bound; the sharper elementary F4 bound is separately pending AppB. |
| B3 | Developed sparse polynomial route result; **Present** | `thm:sp:main` (S5:128); `prop:sp:closure-sound` (S5:601); `prop:sp:closure-stop` (S5:652); `prop:sp:eval` (S5:837) | proof of `thm:sp:main` (S5:791); S5:610, 663; proof of `prop:sp:eval` (AppC:180) | Implicit patch versus algebraic fallback, polynomial descriptor length, expected global proof-record size, and arbitrary-precision evaluation are explicit. F10's common-root conversion is a remaining shared-contract dependency. |
| B4 | Developed graph reduction/corollary; **Proof pending** | `thm:con:graph` (S6:194) (E); `lem:con:expand` (S6:179); `def:con:charted` (S6:240) | Promised `app:con:graph`; AppD (`appendices/D-constraints.tex`) absent; promised proof labels are not yet defined | The expanded factor scopes and uniform pullback curvature are stated. Noise on dependent coordinates is conditioned on; sparse original-coordinate encoding and exact charted lifts are retained. |
| B5 | Developed implicit-graph route result; **Proof pending** | `thm:con:graph` (S6:194) (I); `lem:con:chart` (S6:282); `lem:con:approx` (S6:309); `def:con:charted` (S6:240) | Promised `app:con:graph`; AppD (`appendices/D-constraints.tex`) absent; promised proof labels are not yet defined | Global brackets/floors, certified lower-cost DP with 4E witness tolerance, derivative errors, charted exact output, and no full rational-feasibility promise are stated. Bordered-KKT margins remain a proof obligation. |
| B6 | Developed simplex-domain extension; **Proof pending** | `thm:con:simplex` (S6:529); `def:con:simplex` (S6:497) | Promised `app:con:simplex`, `lem:con:simplex-round/count/close/tail`; AppD (`appendices/D-constraints.tex`) absent; promised proof labels are not yet defined | Disjoint resource/probability simplex blocks, whole-block bags, and native integer intervals are included. Count/rounding/relative face tests are outlined but the detailed proofs are absent. |
| B7 | Developed continuous-order specialization; older count superseded; **Proof pending; superseded count recorded** | `thm:con:order` (S6:623) with all coordinates continuous; `eq:con:orderbound` (S6:638) | Promised `app:con:order`, `lem:con:transport`, `prop:con:order-count`, `lem:con:lpgap`; AppD (`appendices/D-constraints.tex`) absent; promised proof labels are not yet defined | The sharper B8 transport count is specialized to n_c=n and p_c=p, as authorized. The old chamber-count bracket is intentionally superseded, not silently lost. |
| B8 | Developed mixed-order extension; **Proof pending** | `thm:con:order` (S6:623); `ex:con:premature` (S6:698) | AppD (`appendices/D-constraints.tex`) absent; promised proof labels are not yet defined; binary-before-exposure example is inline S6:698 | Only binary native coordinates are included. Endpoint-preserving transport, p_c rather than full bag size, LP exposure after fixing binaries, and weighted curvature are stated. |
| B9 | Developed dynamic-model corollary/example; **Proof pending** | `thm:con:actuator` (S6:436); `def:con:actuator` (S6:384); `ex:con:dyn` (S6:467); `ex:con:actuator` (S6:482) | Promised `app:con:actuator`; AppD (`appendices/D-constraints.tex`) absent; promised proof labels are not yet defined | Affine state recurrences with polynomial actuators preserve the free-variable decomposition; nonlinear state recurrences remain outside scope. |
| B10 | Bridge corollary overlapping deterministic companion; **Pending integration** | `sec:sp:width` (S5:531) (qualitative discussion S5:557–563); `sec:disc:open` (S10:102) (S10:104–110) | No statement or proof of the inventory's certified conditional-recourse tuple-count bound found | The captured draft explains that true conditional values remove the dimension error, but does not state the explicit p-based product count with certified oracle error <= a e_B. Root decision 10 requires the quantitative bridge and short proof; it does not supply an efficient recourse oracle. |

**Route C: small core and conditional recourse**

| ID | Role and draft status | Actual statement/location | Actual proof or remaining dependency | Coverage qualification |
| --- | --- | --- | --- | --- |
| C1 | Developed exact quadratic recourse route result; **Present** | `thm:rec:qp` (S7:320); `prop:rec:search` (S7:196); `lem:rec:exclusion` (S7:244); `lem:rec:closure` (S7:275) | proof of `thm:rec:qp` (AppE:388); proof of `prop:rec:search` (AppE:138); proof of `lem:rec:exclusion` (AppE:195); proof of `lem:rec:closure` (AppE:214) | Box stability and global lower values for restricted recourse are explicit; output is rational on every draw. The empty-core certified-search mismatch in the existing review is not cured merely by listing these proofs. |
| C2 | Oracle corollary using cited prior forest solver; **Present** | `cor:rec:forest` (S7:348) | proof of `cor:rec:forest` (AppE:428) | The core leaves a residual forest and the cited exact rational forest-box oracle is used under every tightened residual box. |
| C3 | Developed certified nonlinear recourse route result; **Present with existing review repairs pending** | `thm:rec:poly` (S7:406); `lem:rec:convex-oracle` (S7:385); `eq:rec:tangent` (S7:389) | proof of `lem:rec:convex-oracle` (AppE:240); proof of `thm:rec:poly` (AppE:388) | Certified lower values, feasible rational box completions, nonlinear closure, and implicit output are written. Generic k=0 does not itself imply convexity; the empty-core accuracy and Hessian convexity-certificate wording await existing review corrections. |
| C4 | Structural separation example; **Present** | `prop:rec:rank` (S7:448); `sec:lim:rank` (S9:712) | proof of `prop:rec:rank` (AppE:442) | Degree-five one-core family, every fixed PSD quadratic convexifier's residual rank, and the nonquadratic correction qualification are retained. It belongs to merely convex recourse, not the uniform-modulus core-only class. |
| C5 | Developed ambient native-integer route result; **Proof pending** | `thm:int:native` (S8:145); `eq:int:label` (S8:170) | Promised `app:int:native`; AppF (`appendices/F-integer.tex`) absent; promised proof labels are not yet defined | Competing-label exclusions, whole-core completion, every-draw short algebraic output, and rational quadratic specialization are stated. Depends on the missing F15 proof. |
| C6 | Implicit-output variant of developed integer route; **Proof pending** | `cor:int:native-implicit` (S8:188) | AppF (`appendices/F-integer.tex`) absent; promised proof labels are not yet defined; proof outline S8:197–199 | Ordinary labels plus core patches and rare exact completion replace the c_d^k ordinary solve. Evaluation and tail accounting await AppF. |
| C7 | Cited classical TU oracle plus flow certificate; **Partial** | `prop:int:hs` (S8:205); `lem:int:potentials` (S8:229) | Hochbaum–Shanthikumar citation S8:219–226; shortest-path explanation S8:229–240; tangent-extension/box-stability details assigned to missing `app:int:native` | The established oracle is identified as such. No polynomial bound is claimed for naive repeated unit augmentation. |
| C8 | Developed core-only continuous recourse route result; **Present** | `thm:rec:core-only` (S7:481); `prop:rec:tube` (S7:536); `prop:rec:release` (S7:568); `lem:app:rec:lift` (AppE:479) | proof of `thm:rec:core-only` (AppE:715); proof of `prop:rec:tube` (AppE:558); proof of `prop:rec:release` (AppE:638); AppE:492 | Uniform residual modulus, Lipschitz selector, growth lift, relative active-pattern formula, tube, and two-sided small-multiplier release are written. The rank-at-most-k convexifier caveat is explicit. |
| C9 | Developed interior network-flow variant; **Proof pending** | `thm:int:flow-interior` (S8:283) | AppF (`appendices/F-integer.tex`) absent; promised proof labels are not yet defined; chart/potential proof outline S8:297–311 | Interiority is required for every permitted noise vector, solely for work. Only network flows are claimed; polynomial sampling precision is retained. |
| C10 | Developed deterministic certificate; **Proof pending** | `thm:int:face` (S8:341); `lem:int:proximity` (S8:326) | AppF (`appendices/F-integer.tex`) absent; promised proof labels are not yet defined; interval/derivative-convexity explanation S8:313–324 | The optimal-flow intervals represent all ties; losing-flow margins and the minimum inward derivative over all tied flows are separate required checks. |
| C11 | Developed boundary network-flow route result; **Proof pending** | `thm:int:flow-boundary` (S8:370) | AppF (`appendices/F-integer.tex`) absent; promised proof labels are not yet defined; value-margin/normal-noise explanation S8:385–397 | Arbitrary core faces and persistent ties are included. Work, output/refinement, and sampling bits retain f_d(k) factors; no polynomial-bit law is substituted. |
| C12 | Developed bilinear flow refinement; **Proof pending** | `cor:int:bilinear` (S8:399) | AppF (`appendices/F-integer.tex`) absent; promised proof labels are not yet defined; affine-margin explanation S8:406–413 | The polynomial sampling-bit regime and the core curvature of phi alone are retained. |
| C13 | Developed TU extension; **Proof pending** | `thm:int:tu` (S8:417); `cor:int:tu-ineq` (S8:437) | AppF (`appendices/F-integer.tex`) absent; promised proof labels are not yet defined; adjacent-slope dual/circuit outline S8:427–435; bounded slack construction S8:442–447 | The general and bilinear regimes transfer to separable convex costs over bounded TU systems; explicit zero-cost bounded slacks are stated. This is separate from general continuous TU feasible rounding. |

**Strong-field families**

| ID | Role and draft status | Actual statement/location | Actual proof or remaining dependency | Coverage qualification |
| --- | --- | --- | --- | --- |
| D1 | Developed strong-field composition using elementary enumeration; **Proof pending** | `thm:int:strong-field` (S8:472) (quadratic case); `eq:int:sf-regime` (S8:488) | Promised `app:int:strong-field`; AppF (`appendices/F-integer.tex`) absent; promised proof labels are not yet defined | Every-draw rational QP output, pre-draw derivative enclosures, independent bad sites, and the subcritical weighted count are stated. This is a strong-noise regime, not a small-noise approximation scheme. |
| D2 | Developed polynomial strong-field composition; **Proof pending** | `thm:int:strong-field` (S8:472); `cor:int:mixed-solver` (S8:110) | AppF (`appendices/F-integer.tex`) absent; promised proof labels are not yet defined; dependent F15 constructive proof is also absent | Per-component common-root output and symbolic value sum are retained. Expanding the total value or comparing arbitrary algebraic sums is expressly excluded. |

**Examples, limitations, and deterministic comparisons**

| ID | Role and draft status | Actual statement/location | Actual proof or remaining dependency | Coverage qualification |
| --- | --- | --- | --- | --- |
| X1 | Mechanism-specific limitation; **Present** | `thm:lim:width` (S9:96) | Inline proof S9:127 | Connected actual treewidth, all-draw retention, whole-hull nonclosure, cutoff, and the n^(Omega(p)) state count are proved. The instance is easy by endpoint DP. |
| X2 | Reused mechanism limitation/example; **Present** | `prop:lim:local` (S9:224); `ex:rec:star` (S7:145) | Inline all-draw proof S9:237; proof of `ex:rec:star` (AppE:801) (including the uniformly positive-definite variant) | Both the robust 32-leaf deletion and d^2-leaf positive-definite error-variation example are present. Their precise deterministic-companion overlap is not yet cited. |
| X3 | Mechanism-specific ambient-count limitation; **Present, duplicate statement unresolved** | `thm:lim:ambient` (S9:321); `prop:qp:ambient-barrier` (S4:630); `prop:qp:fiber-sharp` (S4:614) | `app:lim:ambient` (AppG:5) (AppG:5–176); AppB counterpart absent | The self-contained boundary appendix now contains both local and near-optimal count lower bounds. The S4 formulation also states finite-grid scope; reconcile its proof interface and duplicate formulation in final integration. |
| X4 | Conditional complexity implication plus counting counterexample; **Present** | `thm:lim:constraints` (S9:377); `ex:lim:coupled` (S9:446) | Inline reduction proof S9:403; inline TU diagonal calculation S9:446–477 | Native binary controls plus continuous affine states, all-draw objective separation, polynomial sampling/work implication, and the quarter-probability TU event are explicit. |
| X5 | Noise/curvature premise counterexamples; **Present** | `ex:con:graph-curv` (S6:348) | Inline calculations S6:348–363 | The determinant-one/bounded-inverse example destroys conditional independence; the y=x example converts ambient mixed curvature into large retained curvature. |
| X6 | Mechanism-specific positive-probability limitation; **Present** | `prop:lim:flow` (S9:677) | `app:lim:flow` (AppG:339) (AppG:339–380) | Boundary origins, exact 1/16 atom probability, no uniform label on adjacent boxes, retained origin cells, and chained enumeration cost are retained. |
| X7 | Mechanism-specific closure limitation/example; **Present** | `ex:rec:fiber` (S7:610); discussion `sec:lim:points` (S9:522) | proof of `ex:rec:fiber` (AppE:831) | The rotating segment and strictly convex interior-unique variant are both proved, with short exact certificates; no general optimization lower bound is inferred. |
| X8 | Threshold-compatibility example; **Pending integration** | `prop:lim:threshold` (S9:488); surrounding S9:480–521 | Inline probability proof S9:501 | The generic crossing bound, delta>=0 repair, and qualified conclusion are present. Updated contract requires the explicit Del Pia–Khajavirad width-two NO family with gap 2^(-2r-4), a deterministic witness coordinate equal to one, and precise source attribution; these are still missing from the capture. |
| X9 | Limitation of an inverse-growth proof strategy; **Present with existing review repair pending** | `rem:qp:moments` (S4:273) | Inline capped-moment and sharp-tail calculations S4:273–288 | The k>2 term is explained as an argument limitation, not an algorithmic hardness theorem. The existing quadratic review identifies a wrong lower integration limit in the sharp-tail moment explanation; the updated contract requires its local repair. |
| X10 | Finite-atom closure example; **Present** | `ex:qp:atom` (S4:476); `ex:model:tie` (S2:412); `ex:count:atom` (S3:239) | Inline exact formulas S4:476–487, S2:412–446, S3:239–258 | The specific endpoint draw xi=1 and unresolved switch at relative position 1/3 are retained; general tie/count examples are supporting variants. |
| X11 | Unsound certificate example; **Present** | `ex:qp:corner-labels` (S4:817) | Inline slice-value calculations S4:817–828 | Matching corner labels can miss an interior winning label even if the chosen slice formula is valid on the cell. The normalized rescaling is supplied. |
| X12 | Rational-output premise example; **Present** | `def:qp:sep` (S4:690) and S4:708–713 | Inline breakpoint/minimizer example S4:708–713 | Rational coefficients of pieces alone do not imply rational output; rational breakpoints remain an explicit premise. |
| X13 | Unsound ordering-of-tests example; **Present** | `ex:con:premature` (S6:698) | Inline calculations S6:698–707 | Binary labels must be fixed before applying LP exposure to the continuous face. |
| X14 | Boundary-release premise examples; **Present** | `ex:rec:weak` (S7:628); `ex:rec:two-sided` (S7:639) | proof of `ex:rec:weak` (AppE:854) | Identically vanishing multipliers, the 2(v-1/2)^2 example, and a one-sided core vertex with nonzero multiplier derivative are retained. |
| X15 | Prior/sibling arithmetic boundary re-proved here; **Pending integration** | `thm:lim:posslp` (S9:629); `prop:lim:value` (S9:545) | proof of `thm:lim:posslp` (AppG:313); inline value/regularization proof S9:568 | PosSLP, indirect deterministic/Las Vegas Square Root Sum consequences, and precision/regularization limits are proved. S9:668–670 explicitly declines treewidth/bounded-coefficient variants; root decision 11 supersedes that omission and requires the direct SRS width-two bounded-coefficient construction, its proof, and overlap attribution. The exact-active-label distinction is also not specifically carried over. |
| X16 | Deterministic comparison/baseline; **Pending integration** | `sec:int:lowrank` (S8:521) (S8:570–579); `prop:rec:search` (S7:196) | Low-rank zonotope/Minkowski-sum explanation S8:570–579; deterministic core error follows from AppE:138 | Binary/listed-label low-rank baselines are discussed. The flow-core deterministic approximation work/error comparison kLh^2/8 is not stated; root decision 10 requires its short precise statement/proof. |

**Prior/sibling overlap: O1–O8**

These are attribution and comparison obligations, not additional in-scope
novelties. “EA”, “DA”, and “SI” are inventory aliases for the exact-arithmetic,
decomposition-aware, and sparse-indicator manuscripts. Their precise
bibliography entries and source comparisons belong to Luna's literature
audit. Local companion files below are evidence locators; they must not appear
as private proof dependencies in the submitted paper.

| ID | Inventory disposition | Current matching content | Draft attribution gap / required disposition |
| --- | --- | --- | --- |
| O1 | Cite EA core-noise all-precision value oracle, selected-core Cauchy name, coupled-polytope and joint-convex versions | S1:339–342 gives only generic companion prose; C1/C3/C8 develop stronger structured exact recourse | Identify EA `thm:recourse-core` and `cor:recourse-joint` precisely. Contrast Cauchy names under merely convex residuals with exact outputs under the present structured recourse assumptions. No generic value oracle is proved here under the weaker premise. |
| O2 | Cite EA exact QP Cauchy reconstruction | Present exact QP routes A2–A4 and C1; generic S1:339–342 only | Explicitly identify EA `cor:recourse-qp` and compare its reconstruction/output model and noise support. Do not imply that exact QP under core noise first appears here. |
| O3 | Cite EA full selected points under a convexifier and residual-convex cubics | C8's uniform-modulus route, rank caveat, and X15's residual boundary supply relevant distinctions | EA `thm:recourse-convexified` and `thm:recourse-cubic` are not specifically compared or cited in the capture. State their broader output and different structural premises. |
| O4 | Re-prove shared finite-law, section-count, lexicographic-fallback, projected-growth tools with expanded scope | F1–F6, F10, F16; S3 and AppA contain the actual shared proofs | Specific overlap with EA Appendix I is not attributed. These tools are reused/extended proof infrastructure, not automatically new because the present model spells out bit and output contracts. No private proof outsourcing is needed. |
| O5 | Cite DA deterministic grids, curvature correction, min-marginals, localization, boundary output, conditional-recourse filter, TU coupling, limits | S3/S5 re-prove core mechanics; X2 contains the local-error/star limits; B10 is missing quantitatively | Identify the deterministic counterpart and DA `thm:cr-filter`, `prop:star`, `thm:boundary`. Explain that noise supplies expected retained-state bounds and same-draw exact completion rather than making the underlying grid/error tools novel. |
| O6 | Cite SI sparse indicator penalty-noise theorem as a sibling model | No specific SI theorem or precise perturbation comparison found | Add a narrow comparison between penalty perturbations for indicator quadratics and independent linear objective noise on the present coordinates. Do not import the indicator screening result as a theorem here. |
| O7 | Cite DA deterministic conditioned sparse polynomial pruning and boundary/implicit patch certificates | S5 closure and S7 certified search are proved in the manuscript | The DA `sec:polynomial` / `app:boundary` comparison is not specified. Identify the deterministic growth/Hessian premises and how the sampled certificate/output contracts differ. |
| O8 | Cite EA active-sign rectangle precision and expanded algebraic output barriers | S2:299–308 and S1:251–258 distinguish expanded algebraic output from compact descriptors; X15 gives related arithmetic limits | Cite EA `prop:points-rectangle` and `prop:points-algebraic-output` precisely. The captured X15 does not explicitly give the exact-active-label versus approximating-some-point distinction; the direct SRS integration can supply that short contrast. |

The present source therefore contains substantial re-proved overlap but does
not yet provide a submission-ready relation-to-prior-work account. This is
an attribution gap, not evidence that each overlapping result was omitted.

**Excluded, superseded, or supporting developments: E1–E10**

| ID | Inventory disposition | Draft treatment / boundary |
| --- | --- | --- |
| E1 | Maximal-response growth method superseded by F3/F4 | Not a separate theorem. The proximal-growth proof replaces it; no development-history account is needed. |
| E2 | Summed-response refinement superseded by F3/F4 | Not a separate theorem. Its exclusion does not remove the current projected-growth guarantees. |
| E3 | Interior strong-convex recourse superseded by C8 | Supporting growth-lift and selector/tube ingredients are included through `lem:app:rec:lift`, `prop:rec:tube`, and `rem:rec:interior`; the broader active-boundary theorem is C8. |
| E4 | Core-value comparator notes belong to O1; random-real input model excluded | The paper uses finite-bit rational sampling. The related Cauchy/value contracts need O1's explicit comparison; they are not missing exact-output route theorems here. |
| E5 | Affine optimal fibers / selector interface: structural only, no closure theorem | No unsupported closure theorem is advertised. X7's rotating-fiber example is a separate negative certificate example. |
| E6 | Core-noise exploration conclusions captured by X7 and C8 | Not independently claimed. The relevant limitations and positive core-only route are retained. |
| E7 | TU feasible rounding / chamber counts: supporting scope only | S6:709–727 preserves aligned integral TU rounding as a preliminary. A fixed-polytope count with uncontrolled geometric constants is not converted into an expected-time TU optimizer. C13 is the separate bounded native-integer separable-cost theorem. |
| E8 | Random indicator screening is outside this topic (D3) | No screening theorem or experiment is included. SI remains a cited sibling under O6. |
| E9 | Deterministic sparse and negative-curvature targets: open, not developed theorems | S10:102–142 contains scoped open questions. Broader targets are not claimed proved; the contract also requires reconsidering its universal-law question using the root's separate report. |
| E10 | Monte Carlo component genericity audit motivates deterministic F15, no theorem | No genericity-audit result is claimed. F15's deterministic constructive proof must stand on its own in AppF; the private audit does not fill that absent appendix. |

Two noncounted developments are also excluded explicitly by the inventory:
A10, the fixed-accuracy low-rank approximate solver, is superseded by A2's
exact closure; D3, indicator screening, is outside topic as recorded under E8.
Neither is one of the 69 in-scope IDs.

**Required short integrations and direct-SRS construction locator**

The following is an implementation aid for the authors, not a substitute
proof or a fresh literature audit. I read the named local sources to establish
what content the inventory requires.

1. **A0 mixed conditioned counterpart.** The captured
   `thm:qp:conditioned` at S4:186 assumes `n_z=0`.
   Retain the inventory's exact MIQP counterpart with work
   `f(n_z,k,max(1,nu/g)) poly(I)` and the explicit retained-cell count
   `2^k(sqrt(k kappa)+4)^k`, where
   `kappa=alpha/g_W<2+4nu/g`. Its shared normalization/growth
   argument must be accompanied by the cited exact convex-MIQP oracle and
   rational reconstruction/polishing contract. AppB is still required.

2. **B10 quantitative conditional-recourse bridge.** The source
   `research-20261002/new-direction/local-error-recourse-interface.md`
   §§2–3 requires true outside recourse over a domain independent of the bag
   coordinates. At each bag corner, supply certified bounds
   `ell_B <= W_B <= u_B`, a feasible original-domain completion attaining
   `u_B`, and `u_B-ell_B <= eta <= a e`, with
   `e=pLh^2/8`. Update the incumbent from these completions before
   retention, or recheck after updating it. Retention then gives a corner
   with `W_B <= f*+2(e+eta)`. The shared independent-coordinate count
   yields
   `prod_{i in B}[4+(Lw_i/(2sigma))(1+(1+a)p/2)]`
   under the same finite-grid mesh condition.
   The certificate includes every outside optimization error; ordinary
   grid min-marginals do not satisfy this interface. This is a conditional
   bridge, not a supplied efficient oracle or an unrestricted width-FPT
   algorithm. Cite DA's deterministic `thm:cr-filter` for overlap and
   prove the short noisy count in the paper.

3. **X16 flow-core deterministic baseline.** For a full deterministic core
   grid of mesh at most `h` and exact conditional flow recourse,
   interpolation from F2 gives an original feasible completion with gap
   at most `kLh^2/8`. For a unit core box, taking
   `h<=sqrt(8 epsilon/(kL))` gives roughly
   `(1+sqrt(kL/epsilon))^k` exact recourse calls, up to constants.
   Treat `k=0` or `L=0` separately to avoid division by zero.
   The source is
   `research-20261002/new-direction/boundary-core-flow-significance.md`
   §3. This compares deterministic additive approximation with exact
   optimization of one sampled objective; it is not a practical-speed claim.

4. **X8 explicit threshold witness.** The source
   `research-20261002/new-direction/sparse-smoothed-hardness-sanity.md`
   gives the Del Pia–Khajavirad reduction's NO inputs
   `a_1=2^r, a_2=2^r+2, T=2^r+1`, `r>=1`.
   With `ell=r+2` and `D=2^ell`, following the first-item-only
   trajectory makes all residuals vanish except the final square,
   whose value is `D^(-2)=2^(-2r-4)`.
   The trajectory is in the unit box and has a deterministic selected-item
   copy equal to one. Nonnegativity and the reduction's zero/YES
   equivalence give `0<min Psi<=delta`.
   Apply `prop:lim:threshold` to this witness and its gap.
   Luna must verify the exact primary theorem/proof locator and source
   attribution. The local note's recorded source reading is not my own
   literature verification.

5. **X15 direct Square Root Sum structural boundary.**
   The exact-arithmetic companion's precise statement is
   `paper-exact-arithmetic/sections/02-points.tex`,
   `thm:points-quartic-lower`(a),(c), lines 502–524.
   It maps a Square Root Sum instance either directly to its answer or to
   an explicit rational quartic on `[0,1]^N`, convex on that box,
   with a unique optimizer and a distinguished 0/1 coordinate encoding
   the strict comparison. Equality is handled by preprocessing.
   Its interaction graph has treewidth at most two; nonconstant
   coefficient magnitudes are bounded by an absolute constant; diagonal
   Hessian entries are at most 20. The coordinates and coefficients are
   rationally encoded with polynomial total length, even though active
   amplitudes can be extremely small.
   A separate independent quadratic core preserves this residual example
   under core-only noise, with the point decision holding on every draw.
   A point within Euclidean distance 1/4 decides the comparison.
   Polynomial deterministic total work implies Square Root Sum in P;
   always-correct polynomial expected total work implies a Las Vegas
   algorithm. A short unevaluated descriptor alone does not establish
   either implication.

   The self-contained construction dependencies are all in
   `paper-exact-arithmetic/appendices/C-points.tex`:
   `app:points-boundary` at line 1048;
   `lem:points-sign-test` at 1063 with proof 1077–1090;
   `lem:points-amplifier` at 1092 with proof 1113–1137;
   `lem:points-tree` at 1148 with proof 1169–1195;
   `lem:points-trace` at 1197 with proof 1202–1212;
   and the proof of `thm:points-quartic-lower`(a) at 1249–1280.
   The complexity consequence is proved at 1355–1363.
   Appendix G already has analogous sign/amplifier devices for PosSLP;
   those may be reused at their stated scope, with a clear cross-reference.

   Essential steps to retain:
   normalize radicals by powers of two `R_i`,
   `c_i=a_i/R_i^2 in [1,4)`, and weights
   `w_i=R_i/max R_i`; put cubic leaf selectors
   `u_i^3/3-c_i u_i` in a complete binary averaging tree;
   enforce parent averages by squared residuals.
   The tree's Hessian is at least `I/8` because its averaging operator
   has norm at most `1/sqrt(2)`, and the root is the normalized radical
   sum. The radical trace lemma shows an integral sum of positive radicals
   can occur only if all items are squares; test those items using integer
   square roots so a constructed instance has unequal root/threshold.
   Make two independent copies with opposite sign tests, giving exactly
   one positive activation amplitude. The paired quartic amplifier fixes
   its new coordinate to 0 or 1 and retains box convexity by absorbing the
   negative square term in the strong-convexity margin.
   Join the two averaging trees through bags
   `{s_+,theta_+}`, `{theta_+,y}`,
   `{theta_-,y}`, `{s_-,theta_-}`.
   Bags have at most three vertices and the running-intersection property.
   Unit-box affine rescaling preserves scopes and multiplies diagonal
   Hessian entries by at most four. Each variable belongs to at most three
   bounded-coefficient factors; consequently expanded nonconstant
   coefficients remain bounded. The constant term can be deleted.

   The exact-label comparison belongs to the companion's
   `prop:points-active`, statement at
   `sections/02-points.tex:458–479`, proof in
   `appendices/C-points.tex:1218–1234`.
   It gives a uniformly strongly convex cubic whose exact active lower
   bound decides Square Root Sum, including equality, while arbitrary
   point approximation is polynomial in requested precision.
   Preserve this distinction when explaining why exact active labels,
   selected optimizers, and some point near the optimizer have different
   contracts.
   This construction is prior/sibling material re-proved for completeness;
   decision 11 expressly forbids treating it as novel here.
   I checked these locators and dependencies for coverage. I did not
   independently re-audit every detail of the direct SRS proof in this
   coverage task.

**Coverage checks actually performed**

- Read the inventory and current captured sections/appendices; extracted
  actual statement labels, headings, and named proof environments.
- Matched each of the 69 inventory IDs to actual manuscript content or an
  explicit missing/narrowed/pending disposition. Checked that all labels
  cited as present in the map exist in the captured files.
- Checked the source capture's SHA-256 hashes and recorded line counts.
  The temporary capture consists of 15 submission-source files, with the
  three named appendices absent.
- Used scoped `rg` searches, `sed`/`cat` reads, and inline
  `python3` metadata/coverage checks. A search over captured submission
  sections and appendices for private-source paths, Markdown dependencies,
  and unfinished-placeholder words returned no matches (normal `rg`
  exit 1). This is only a scoped textual check, not a claim that the paper
  is complete.
- Read the local direct-SRS statement/proof and the short B10/X8/X16 source
  notes to give the concrete integration locators above. Existing
  independent reviews remain separate evidence and do not replace a
  completed paper proof.

No literature research, experiments, new mathematical diagnostics,
project-wide verification, CI inspection, manuscript/source-note edit,
or delegation was performed for this coverage task. The earlier boundary
audit has its own check record at
`evidence/reviews/early-boundaries-sol-r1.md`; its proof diagnostics are
not repeated or counted as checks of this draft coverage map.

