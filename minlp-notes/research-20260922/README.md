# Research continuation started 2026-09-22

This folder holds the research program started on 2026-09-22. Its goal is new,
correct MINLP results with practical value for solvers. Earlier work in the
repository is context only.

"Independently reviewed" means checked by a fresh research agent, not peer
reviewed. A failed literature search does not establish novelty.

## Results so far

1. **Convex envelopes of `sigma(a^T x + b)` over a box for any lower semicontinuous
   `sigma`** ([theory](ridge-envelopes/theory.md)). The envelope equals a minimum
   of `E sigma(S)` over laws dominated in convex order by a comonotone
   "staircase" law. Dually, it is a supremum over concave minorants `psi` of
   staircase interpolations of `S -> psi(a(S))`. Every exactly concave
   `psi <= sigma` yields cuts valid on the whole box. The result also holds on
   order polytopes and products of simplices.
   - Status: independently reviewed ([review](ridge-envelopes/review-theory.md));
     numerically verified on 1800 cases ([verification](ridge-envelopes/numerical-verification.md)).
   - Novelty ([check](ridge-envelopes/novelty.md)): the probabilistic core is
     Mao–Wang (2015). Concave and S-shaped `sigma` are known (Tawarmalani,
     Richard and Xiong 2013; Carrasco and Muñoz 2026). The general case, the
     cut form and the localization were not found.
   - Practical value is modest. On neural-network optimization the cuts close
     a median 3.6% of the root gap (about 20% for SiLU and GELU) and save
     nodes, but a Python branch-and-bound is slower with them
     ([experiment](ridge-envelopes/nn-experiment/report.md)). In MINLPLib the
     structure is mostly two-variable ([scan](ridge-envelopes/minlplib-ridge-scan.md)).
2. **Certified finite dual bounds for the 18 open `nuclear*` MINLPLib
   instances** ([report](benchmark-observations/nuclear-bounds.md)). The bounds
   combine Collatz–Wielandt bounds with a new peaking-aware bound. Listed gaps
   were infinite or about 1e6; the certified gaps are 3–20% where a feasible
   point is known. The mathematics is classical; the application to reload
   patterns was not found in the literature.
   - Status: independently reviewed; all values reproduced exactly with
     separate code ([review](benchmark-observations/review-nuclear-bounds.txt)).
   - Follow-up ([assessment](nuclear-global/assessment.md)): proving
     optimality with bound-driven branch and bound is not feasible with the
     current bounds. Exactly certified root bounds improve the earlier bounds
     by 0.22–1.25% on the seven F1 instances (va–vf, nuclear14). Local search
     improved the listed primal values of six instances by up to 0.2%; these
     points were re-checked with a separate evaluator at 60 digits.
     Independently reviewed ([review](nuclear-global/review-assessment.txt)).
3. **Contraction theory of iterated OBBT** ([theory](iterated-obbt/theory.md),
   [proofs of Theorem 12 and Proposition 11](iterated-obbt/proofs-12-11.md)).
   - Near a minimizer, the OBBT operator is approximated by a monotone map `Phi`
     on box shapes that is positively homogeneous of degree 1. A
     Collatz–Wielandt-type constant `r*(Phi)` bounds the local linear rate from
     above, and a stall certificate shows when OBBT cannot contract at all.
   - Exact rate `(sqrt(2a^2+4a)-a)/2` for `x^2 + y^2 + a xy` with McCormick.
   - A row condition under which OBBT tightens nothing, even for strongly
     convex objectives.
   - The root gap after iterated OBBT is `O(epsilon)` in the contracting regime.
   - The second-order tangent expansion holds for composite McCormick
     relaxations of factorable `C^2` functions.
   - Status: independently reviewed ([review](iterated-obbt/review-theory.md)).
     No published rate theory was found ([literature](iterated-obbt/literature.md),
     [cluster literature](iterated-obbt/literature-cluster.md)).
   - Computation ([report](iterated-obbt/experiment-report.md)) is negative for
     practice. On 339 MINLPLib QCQPs with realistic incumbents, iterated OBBT
     as an external presolve reduces nodes but is 1.2–1.7 times slower than
     Gurobi 13 or SCIP 10 defaults. Even with zero OBBT time, the tightened boxes
     give the same final-solve time as a no-OBBT control. Independently reviewed
     ([review](iterated-obbt/review-experiment.md)).
4. **Certified curve-hull cuts for variables with several univariate terms**
   ([report](curve-hulls/report.md), [review](curve-hulls/review.txt)).
   - A general separator handles the convex hull of `(t, f_1(t), ..., f_k(t))`.
     Its cut constants are certified by interval arithmetic.
   - On waterno2_06/09/12/18/24, root cuts raise Gurobi 13's 1800 s dual
     bounds above MINLPLib's best listed bounds (165/274/480/771/1095).
     Regenerated, reproducible runs reach 226/656/1573/3144/4442, and earlier
     runs reached 230/637/1555/3226/4464. These are uncertified floating-point
     runs, but an independent rebuild reproduced the effect.
   - This extends the repository's earlier moment-hull note to arbitrary
     curves and to waterno2_24. The hull theory itself is known (Ballerstein 2013).
   - Other instances gain little or nothing.
5. **Benchmark facts from classical theorems** ([report](benchmark-observations/report.md)):
   - Reinhardt's theorem solves polygon25 and polygon75, and it reduces the
     polygon50 and polygon100 gaps from 18.5 and 42.3 to 1.3e-4 and 1.6e-5.
   - The D5 root system improves the knp5-40 primal value to exactly 1.
   - SCIP solves mpbp_06 and waternd_shamir within a minute.
   - Exact certificates ([report](benchmark-observations/structural-bounds.md),
     [review](benchmark-observations/review-structural-bounds.txt)):
     - Yudin/Delsarte LP bounds cut the elec25/50/100/200 (Thomson problem)
       gaps from 170–221% to 0.013–0.07%.
     - The hadamard objectives are proven to be 0/1 determinants.
       Max-determinant theorems close hadamard_6, 7 and 9 and bound
       hadamard_8 by 65 (primal 56).

## Negative results

- Box-aware rank-one quadratic cuts `b^T X b <= Lambda_b(x)` are implied by
  McCormick (RLT) inequalities; quadratic ridge envelopes equal termwise
  McCormick ([log](log.md)).
- Theorem 1 cuts do not speed up global optimization of small trained networks
  in a Python branch-and-bound, because separation cost outweighs node savings.
- Iterated OBBT as an external presolve does not pay off on MINLPLib QCQPs
  with realistic incumbents (result 3).
- Spatial-branching setting changes move node counts no more than random
  seeds do on MINLPLib samples; reusing parent duals for child bounds captures
  2.3% of the true bound gain ([solver-core scout](scouting/brainstorm2-solvercore.md)).

## Files

- `log.md`: chronological research log, including negative results.
- `scouting/`: literature, MINLPLib open-instance and brainstorm reports.
- `ridge-envelopes/`: result 1, with code, verification, review, novelty check and experiments.
- `benchmark-observations/`: results 2 and 5, with code and reviews.
- `eigen-cg/`: investigation of Eigen-CG Conjecture 1: special cases proved,
  a verified negative result on higher-rank CG cuts, no resolution
  ([investigation](eigen-cg/investigation.md), [review](eigen-cg/review.md)).
- `iterated-obbt/`: result 3, with literature checks, review, code and experiments.
- `curve-hulls/`: result 4, with code, results and review.
- `nuclear-global/`: follow-up to result 2 (assessment, review, code).
- `pooling-multiattribute/`: feasibility assessment of a pooling direction.
  Multi-attribute pooling cuts give a safe root bound on pooling_sppc0 that
  beats MINLPLib's best listed dual bound (-93325.22 against -95124.69). A
  claimed improvement on sppb0 was refuted by independent verification
  ([verification](pooling-multiattribute/verification.txt)). The theory
  direction (hulls with correlated qualities) is recorded as an open option;
  it was not pursued.
