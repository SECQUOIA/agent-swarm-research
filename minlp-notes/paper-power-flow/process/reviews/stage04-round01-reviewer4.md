# Stage 4, round 1 — independent reviewer 4

**Verdict: PASS on mathematical integration; three minor reproducibility/attribution clarifications. No major issue found.**

I reviewed the frozen integration, author report, introduction, abstract, conclusion, bibliography, verification appendix, README, coverage, and packaging rules. All 22 snapshot hashes agree. Independently comparing accepted mathematics and checkers confirmed byte identity except the documented Bienstock–Verma citation/version wording in section 06. I did not read another stage-4 review or edit manuscript files.

## Required minor clarifications

1. **Specify Python 3.10 or newer in the README.** The run instructions currently say “Python 3.” `check_resistive_exact.py` evaluates `variable: str | None`, requiring Python 3.10+, and the developments checker imports that module. The implementation can remain unchanged; state the actual minimum version once in the execution instructions.

2. **Qualify Bienstock–Muñoz's theorem numbering by version.** The introduction cites “Theorem 7 and Corollary 8” through the journal entry `BienstockMunoz2018`. I independently verified precisely those statements in the locally archived arXiv full text, p.4. The publisher exposes the journal abstract and metadata, but its PDF link redirects to an access page, so that check does not verify journal numbering. The archived preprint and journal are visibly different versions (even their reference lists differ). Add “of the arXiv version” to the locator, identifying the checked version in the bibliography if needed, or replace it with a separately verified journal locator. The underlying approximation claim is supported and correct; this is precise source attribution, not a mathematical objection.

3. **Clarify path bases in the coverage map.** Its opening says paths below are relative to the repository root unless stated otherwise, but the final sections use `process/worktree-coverage-audit.json`, `verification/root/worktree-coverage-final-check.json`, and `verification/stage04-*.log` for files actually inside `paper-power-flow/`. The legacy-winding row similarly points to `verification/root/legacy-winding.log`. State that source paths are repository-relative while manuscript `process/` and `verification/` paths are relative to `paper-power-flow/`, or prefix those paths consistently. The README uses the correct paper-directory-relative convention.

## Substantive findings

The integrated overview matches the proved results. It retains all simultaneous graph restrictions, dependence of the finite alphabet on fixed girth, positive voltages, signed/independent intervals, and the distinction between a high-girth graph and a tree. The coefficient field Q now appears in the abstract and introduction's sharp rational-universality statement. General compact semialgebraic topology is correctly separate from rational equivalence. The unique-degree and certificate claims do not conflate irrational coordinates with exclusion from NP.

The three AC conventions remain distinguishable: consistent real bus angles use cycle conditions; boxes fix reference phases; positive principal-only windows have size-dependent cosine data. One-sided reactive intervals are described as exact balance consequences. No symmetric-tolerance hardness or fixed positive principal-window classification is insinuated. The numerical overview identifies residual precision, a specified promise, and reactive stability separately; the conclusion does not turn the explicit tiny-residual family into an algorithmic lower bound.

I checked every analytic example in the verification table against the original script's eight `run_case` systems. All six feasible rows have the stated unique source solutions in `[1/2,2]`. The two infeasible rows are ruled out by AM–GM and the forced x=1/4 respectively. The unpinned-looking double-addition row is indeed unique because z=4x<=2 and x>=1/2. The golden-ratio row and three-leaf fan-out row are correct. Applying the already proved unique extension gives exact original-network conclusions.

The historical solver paragraph agrees with the repository's recorded final run: four feasible AC examples with 15, 19, 23, and 25 buses and reported upper bounds below 10^-6 on the sum of squared imaginary voltages. It clearly says that the solver was not rerun and that floating point bounds are not exact certificates. The deterministic counts in the new appendix agree with the previously executed, hash-identical checker suites. I reran the earlier winding checker and obtained exactly 360 scaled pairs, 4,136 cycles, and 256 nonzero windings.

## Independent primary-source verification

- **Gan–Low:** opened the [primary Caltech PDF](https://smart.caltech.edu/papers/optimalflowjournal.pdf). Its first page distinguishes the physical DC model from the linear approximation and states sufficient SOCP exactness conditions involving voltage upper bounds and injection lower bounds. The introduction attributes scoped sufficient conditions without claiming universal tractability.
- **Jeeninga et al.:** read the archived primary full text's fixed-source model, Theorem 3.18 on closed convex feasible demand sets, and Theorem 3.22 on exact feasibility versus interior feasibility. The manuscript preserves the two different matrix alternatives and does not infer a Turing-polynomial exact algorithm merely from an LMI characterization.
- **Lehmann et al.:** read the primary problem definition and star reduction. The unit magnitude, active/reactive constraint, and star-network descriptions are accurate. The manuscript does not misidentify this as its purely resistive-line subclass.
- **Bienstock–Verma:** checked the primary introduction's lossless model and explicit absence of reactive-power constraints. The manuscript uses a separate versioned entry for the arXiv Section 1.3 approximation question, avoiding the former journal/preprint conflation.
- **Bienstock–Muñoz:** read the primary arXiv Theorem 7 and Corollary 8, including scaled feasibility/optimality tolerance. Those support the comparison. The [publisher abstract](https://epubs.siam.org/doi/10.1137/15M1054079) also confirms the two approximation regimes; journal theorem numbering remains the minor attribution issue above.
- **Lavaei–Low:** downloaded and extracted the openly served [primary Caltech PDF](https://smart.caltech.edu/papers/zeroduality.pdf). Appendix B Case 2 explicitly adds real admittance and zero reactive injections. The introduction credits this connection while relying on the manuscript's own real-lift energy proof, and does not endorse the source's unrestricted discrete-phase conclusion.
- The previously audited ETR-INV, crossover, triangulation, polynomial-minimum, and oscillator dependencies are unchanged. The repaired conjunction-only arithmetic proof is still present; the integration does not reinstate the invalid unrestricted Boolean rational-equivalence claim.

## Build and packaging evidence

All reviewer artifacts are in the absolute directory `/workspace/minlp-notes/paper-power-flow/verification/reviewer4/stage04-round01/`.

- `manifest-check.log`: all 22 frozen hashes verified.
- `accepted-dependencies.log`: accepted math/code identity confirmed, allowing only the documented version-specific citation change.
- `build.log`, `build/`, `manuscript-layout.txt`: independent 28-page build succeeded; final log has no warnings, undefined references/citations, or overfull/underfull boxes.
- `page27.png`: visually inspected the eight-example table and surrounding verification prose; equations, row separation, captions, and page boundaries are readable without clipping.
- `legacy-winding.log`: independent legacy check rerun with the exact counts printed above.
- `lavaei-low.pdf` and `lavaei-low.txt`: primary-source retrieval and extraction used to verify the scoped historical attribution.

The coverage map gives explicit dispositions for historical failed claims and duplicate worktree material. Generated build directories and diagnostic images are excluded while mathematical code and useful text evidence remain. I found no missing result that needs to be added at this integration stage. Address the three minor clarifications before stage acceptance; no major-issue repeat is required on my findings.
