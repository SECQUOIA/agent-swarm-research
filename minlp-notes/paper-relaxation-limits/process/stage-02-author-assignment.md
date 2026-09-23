# Stage 2 author assignment (to begin only after Stage 1 gate closes)

Write a complete, compilable account of every Stage 2 row in `scope-proposal.md`, in one or more coherent LaTeX section/appendix files. Preserve verified Stage 1 mathematics. One author owns the stage; do not launch subagents. Root will freeze it and assign 15 independent reviewers.

Read each canonical result in full and relevant audit corrections. Check all proofs afresh. Existing status labels are not evidence of correctness. Provide complete proofs of repository results, allowing short precise citations only for established external tools. Finite certificates should be readable and reproducible without proprietary solvers. Use the existing notation contract. Give all controlling parameters and limiting quantifiers explicitly.

Before returning, write `process/stage-02-author.md` with a row-by-row claim/label coverage ledger, proof/source checks, any original errors corrected, and any bounded development attempted. Stage 1 review found a finite-results omission; avoid a repeat by explicitly mapping all of the following:

- Dyadic sparse construction, exact cutoff formula, arbitrary versus nested partitions, dense predecessor and homogeneous reduction.
- Distinct dyadic coupling and tail lemma (appendix is appropriate); harmonic global law, original explicit finite bound and sharp leading degree/dimension asymptotics.
- Optimized cutoff fixed point, scalar mixture optimality scope, Lambert certificate, second-order upper denominator, and special rho=1 reciprocal refinement. No second-order lower claim.
- Exact cloning of both envelopes, uniform random sampling, homogeneous/interior reduction; finite nonconstructive 25,000-variable bound alongside the stronger explicit example.
- Cubic finite exact 18/24/192-variable witnesses, complete primal and dual certificates or compact tables with proof/checker; 25-variable homogeneous interior bound.
- Analytic family including exact Bernstein positivity table and slack improvement: strongest limiting lower is 1610000/743033, the reduced form of 4830000/2229099. It is a supremum lower bound, not a claimed attained finite optimum. Reconcile older headlines 483/223.
- Two-level family, limiting 243/115, exact 32-variable 135/67, explicit 52-variable 4,320-monomial unit homogeneous interior 2700/1343.
- General endpoint-orientation bound (cubic 8/3), three-law cubic bound 31/12, mixture-family optimality only.
- Exact finite equal-marginal formula, dimension-free supremum and degree optimizer, sharp two and its classical attribution.

Root replays: `verification/repository-checks/global.json` records five passing scripts, including all finite cubic certificates. `verification/check_harmonic_cutoffs.py` independently checked 24 (degree,cutoff) cases numerically, not a proof. Root read Sherali's original PDF pp.252–253 (PDF8–9): equation (13) and Theorem3 give the complete elementary-symmetric convex envelope; DOI not needed, verified original https://math.ac.vn/uploads/files/9701245.pdf. Read `literature/AGENTS.md` before further local source use. Do not copy copyrighted originals into the paper folder. Add verified primary references in the paper-local bibliography.

Write for an outside mathematical reader, with motivation and transitions. Avoid merely concatenating repository notes. Do not describe internal agents or historical discovery chatter in the paper. Compile using `python verification/build_and_check.py` from the paper folder or its full path. Resolve LaTeX warnings before returning. Other paper folders are outside scope.
