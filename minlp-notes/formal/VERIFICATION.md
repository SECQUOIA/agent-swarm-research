This page preserves historical verification snapshots through 2026-09-16.
For current completion status and later topic-specific evidence, see the
[topic index](topics/README.md). The counts, commands and fingerprints below
describe their original stages, not the current source tree. Subsequent prose
updates do not constitute new Lean checks or refresh historical fingerprints.

The focused cubic paper completion was verified on 2026-09-16, after the
multilinear completion below had passed all checks. Thirteen new proof modules
bring the canonical project to 160 modules and 15,019 audited declarations.
The warning-free build, generated-certificate checks, import coverage,
transitive axiom audit, and full canonical kernel replay passed. The separately
built 61-module cubic paper export also passed its 1,247-declaration audit
and full kernel replay. The [cubic completion record](topics/11-cubic-completion/VERIFICATION.md)
contains logs, fingerprints, mathematical review, and paper checks.

Its precise scope is the universal `31/12` upper bound, fixed-mixture
optimality for the actual laws, and the analytic lower bound `1610000/743033`
for the original cube and all-box degree-three suprema. The focused manuscript
has complete mathematical coverage; its coverage map explicitly excludes
separate coefficient-removal and equal-marginal research.

The records below describe earlier completion stages and their source counts.

The standalone multilinear paper completion was verified on 2026-09-16.
The canonical project contained 147 proof modules at that completion stage and 14,756 audited
declarations. The warning-free build, import coverage, transitive axiom audit,
and full canonical kernel replay passed. The separately built 48-module
paper export also passed its audit and kernel replay. The
[completion record](topics/10-multilinear-completion/VERIFICATION.md) gives
logs, fingerprints, mathematical review, and paper checks.

The records below describe earlier snapshots.

The exact multilinear hull formula and sharp degree/dimension growth
extensions were verified locally on 2026-09-12. They add 25 proof modules,
bringing the project to 140 modules and 14,663 audited declarations.
The integrated build with warnings treated as failures, import coverage,
full transitive axiom audit, and kernel replay of all 25 new modules passed.
Only `propext`, `Classical.choice`, and `Quot.sound` are allowed.
Independent agent reviews found no mathematical or specification issue.
The [exact-formula record](topics/08-exact-multilinear/VERIFICATION.md)
and [sharp-growth record](topics/09-sharp-multilinear/VERIFICATION.md)
give reproduction commands, logs, fingerprints, and precise scope.

The new endpoints prove the exact finite dyadic hull gap with attainment
and leading-constant-one growth over all finite nonnegative boxes, by
degree allowance and by exactly n ambient coordinates. The optimized
finite harmonic certificate and second-order upper bound remain outside
this verification. Earlier records below describe historical snapshots;
their shared root-import and audit files have since been extended.

The positive multilinear disproof extension was verified locally on
2026-09-12. Its [record](topics/07-multilinear-disproof/VERIFICATION.md)
covers nine new modules, bringing the project to 115 proof modules and
14,171 audited declarations. The root build, full axiom audit, import
coverage, and kernel replay of the nine new modules passed. It proves
unbounded gap ratios, with the exact hull formula and sharp asymptotics
still excluded. The records below describe the earlier 106-module snapshot.

Local verification completed on 2026-09-11 in WSL2 Ubuntu 24.04, x86-64.
All six additional topics were completed in order, with each topic checked and
documented before work started on the next. A subsequent exact-count completion
added six modules for the monotone extension and the remaining construction
claims. The original eleven exact-count proof modules remain unchanged. The [topic index](topics/README.md) links each package's
explanation, precise coverage, and verification evidence.

| Package | Proof modules | Verification record |
|---|---:|---|
| Exact integer/binary counts, including completion | 17 | [Coverage](COVERAGE.md); [completion record](topics/00-exact-counts/VERIFICATION.md) |
| 1. Switching control | 21 | [Record](topics/01-switching-control/VERIFICATION.md) |
| 2. Primitive FBBT lower bound | 8 | [Record](topics/02-fbbt/VERIFICATION.md) |
| 3. Potential-flow certificates | 10 | [Record](topics/03-potential-flow/VERIFICATION.md) |
| 4. Cubic relaxation gaps | 28 | [Record](topics/04-cubic-gaps/VERIFICATION.md) |
| 5. Reciprocal-anchor hulls | 9 | [Record](topics/05-reciprocal-anchor/VERIFICATION.md) |
| 6. Network–simplex hulls | 13 | [Record](topics/06-network-simplex/VERIFICATION.md) |
| Total | 106 | All imported by `Formal.lean` |

| Final check | Result |
|---|---|
| Proof-module import coverage | PASS: 106 modules |
| Full `lake build --wfail` | PASS: no errors or warnings |
| Full axiom audit | PASS: 14,053 project declarations, including private helpers |
| Allowed axioms | Only `propext`, `Classical.choice`, `Quot.sound` |
| Kernel replay | PASS: every current proof module covered by the completed stage replays |
| Earlier source snapshots | PASS: all six other topic fingerprints and all eleven original proof sources unchanged at the completion stage |
| Generated certificate reproduction | PASS: saved potential-flow JSON and large cubic certificate |
| Audit negative control | PASS: an unrelated-namespace custom axiom was rejected during stage 1 |
| Mathematical specification review | Completed per topic; scope and exclusions recorded in each coverage table |

Stage 1 replayed the original package and switching control together. Each later
stage rebuilt and audited the whole project, then replayed the added topic.
The exact-count completion rebuilt all 106 modules, audited all project
declarations, and replayed all 17 exact-count modules, including the original
proofs and the six additions. Final fingerprint checks establish that the earlier verified sources are
unchanged. The [combined log](verification/run.log) preserves these stage logs
and the final snapshot checks; it is an aggregate of successful runs, not a claim
that all modules were replayed in one final invocation. The imported root module
also passes the final build and audit.

| Component | Version or revision |
|---|---|
| Lean | `4.33.1`, commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6` |
| Lake | `5.0.0-src+819816b`, bundled with Lean |
| Mathlib | `v4.33.1`, commit `0df444a360eaa60ab8c11dca51a86af692955474` |
| Python | `3.13.11`, for coverage and untrusted certificate-source generation |

Elan, Lean, and the pinned Mathlib dependencies and compiled cache are installed
locally. No external optimization solver is needed. Python-generated finite
certificates are checked by Lean; Python is not accepted as a proof oracle.

To check the recorded source, documentation, and log snapshot, run from `formal/`:

```bash
sha256sum -c verification/SHA256SUMS
```

To build, audit, check certificate reproduction, and replay the entire current
project in one invocation:

```bash
bash scripts/verify.sh
```

The script uses one Lean worker to limit memory consumption. The bundled
checker replays project proofs through the installed Lean kernel, with imported
Mathlib declarations as its dependency base. It is neither an independent
implementation of Lean's logic nor a fresh verification of all Mathlib.

The axiom audit checks every declaration owned by a project module, regardless
of namespace or visibility, and follows dependencies transitively. No unfinished
proof, custom mathematical axiom, native-computation axiom, or unchecked solver
certificate supplies a missing proof step.

These checks establish the formal statements under their stated definitions and
assumptions. The coverage tables identify how they correspond to manuscript
claims and which claims remain outside the formalization. Completion of a topic
does not mean every claim in its paper has been proved.

The original proof verification above was local. The later
[GitHub run 34659362171](https://github.com/sergey-gusev94/minlp-notes/actions/runs/34659362171)
stopped during compilation with `error code: 28, no space left on device`;
its audit and kernel replay steps were skipped. The workflow now frees the
hosted runner's unused Android and .NET SDK space before checkout and Lean setup,
and reports disk availability. YAML parsing and shell syntax checks passed
locally; the revised workflow still needs a successful hosted run. No proof
sources were changed for this CI repair. No repository push, publication, or
deployment was performed during the repair.
