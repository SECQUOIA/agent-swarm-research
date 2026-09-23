# Stage 3, round 1 — independent reviewer 4

**Verdict: REVISE — one major source-dependency issue and one minor wording error.**

I independently reviewed all new structural, algebraic, and numerical statements, their accepted dependencies, new checker, abstract, bibliography, and coverage map in `paper-power-flow/process/snapshots/stage03-round01`. I did not read other stage-3 reviewer reports or edit the manuscript. The graph, residual, separation, certificate, and stability developments pass my mathematical audit. The general rational-universality theorem needs a sounder justification than the cited source proof supplies.

## Required major correction

**M1 — The cited arithmetic universality proof has a concrete normal-form failure for Boolean input formulas.** Location: `sections/05-algebraic.tex`, Theorem `thm:universality` and its proof, and corresponding abstract/coverage claims.

The manuscript invokes Dynamic Toolbox Theorem 1 for every compact semialgebraic set. I checked the underlying proof rather than only its statement. The source's Lemma A (pp.5–7) claims that converting arbitrary Boolean ETR formulas to conjunctive form preserves the entire solution set by a rational bijection and projection inverse. Its steps 2 and 3 introduce nonnegative auxiliary variables for each inequality, but leave the defining equality inside its original Boolean branch. On an inactive branch, those auxiliary values need not be determined. The claimed forward map on p.7 therefore need not be defined, injective, or surjective.

A compact explicit example is

`Phi(x) := (x=0 OR x>0) AND (1-x>=0)`,

whose solution set is `[0,1]`. The source's displayed transformations yield, after replacing the disjunction by a product,

`x*(x*z-1)=0, 1-x-w=0, z>=0, w>=0`.

For `x=0`, every `z>=0` and `w=1` is feasible. The transformed set contains an unbounded ray, so projection is not one-to-one and the proposed coordinate `z=1/x` is undefined at an original feasible point. I visually verified the actual original PDF p.6 transformation rules; this is not an extraction artifact. The source p.7 indeed assigns `z=1/q` for variables introduced by step 2. An exact reproduction is in my verification artifacts.

This counterexample refutes the cited general normal-form proof; it does **not** prove that the particular set `[0,1]` lacks another realization, or by itself refute every possible proof of the source's general theorem. Nevertheless, an identified gap in the precise dependency used for an important manuscript theorem cannot be left unaddressed under the requested verification standard.

**Required fix:** either supply a valid independently checked result/proof covering arbitrary compact semialgebraic sets with the stated rational equivalence, or narrow rational equivalence to compact **basic closed** semialgebraic sets over Q and justify it using the conjunction-starting arithmetic chain (Toolbox Lemmas C–G, after introducing unique polynomial slack variables). That restriction avoids the broken Boolean preprocessing. If the full topological claim is retained, it can be separately developed through finite triangulation: a finite simplicial complex has a basic closed rational standard realization using nonnegative barycentric coordinates summing to one and zero products for nonfaces. This gives a route to homeomorphism for arbitrary compact semialgebraic sets, while preserving rational equivalence for the basic closed case. Verify/cite triangulation and write that distinction explicitly if taking this route; do not present it as rational equivalence for the original arbitrary set.

The designated algebraic-degree application starts with a conjunction defining an isolated algebraic root and does not need the broken Boolean step. It can survive, but its proof should point to the verified conjunction-starting source chain rather than implicitly relying on the same unrestricted normal-form assertion. The arithmetic replacement coordinates are explicitly scalar shifts/scalings in the source construction, so designated-coordinate field recovery remains justified.

## Required minor correction

**m1 — Misdescribe D's incident copies in the residual proof.** At `sections/06-numerical.tex:66–67`, “including its two weighted x copies and one y copy” describes three external copies at D, but D has only one complemented x copy with conductance 2 and one complemented y copy with conductance 1, besides W. The other complemented x copy is attached to `C_I`. Replace by “including its x copy with weight 2 and its y copy with weight 1.” The bound `epsilon+3 delta` is already correct and needs no change.

## Audit of the remaining mathematics

### Structural construction

- The three crossover equations force `X'=X`, `Y'=Y`, and uniquely `Z=X+Y`. The stated intervals `[1/2,2]` for transmitted values and `[1,4]` for local sums suffice. The manuscript adds explicit interval preservation rather than importing a bounded-witness promise as a full-set statement.
- The crossing figure has a valid planar incidence embedding with alternating terminal order. Segment variables, original variable vertices, and repeated occurrence strands are handled consistently. Polynomially many original strands yield polynomially many crossing disks; the construction does not recursively create crossings involving new local sums.
- For complement constant `C=9/2`, fixed injections `2-C`, `3-C`, and `5-3C` produce the required copy/addition/inversion equations. An inversion solution with x,y in `[1/2,4]` automatically lies in `[1/2,2]`, so the old W bound remains valid on all actual solutions. No false claim about h(x) on the whole enlarged box is used.
- Ordering each variable's requests by its incidence embedding, leaving a break in its copy path, and duplicating the x corridor into adjacent strands supplies an embedding respecting all port orders. The inversion tree has only three external leaves, so reflection suffices for either cyclic order. Repeated names never identify electrical buses.
- Each component has a root of degree at most two and free injection. Adding its pinned-voltage free-injection connector changes only redundant constraints; path connections among connector buses have zero drop. Choosing each attachment face as exterior gives a planar connected network. Empty arithmetic input is correctly represented by one fixed voltage bus.
- Replacing an edge of conductance 1 or 2 by 4L or 2L unit edges gives old current divided by 4L. Positive internal voltages plus zero injection force unique affine interpolation. Scaling every old injection interval therefore proves both directions, not merely forward feasibility. Even path lengths give bipartiteness; cycles traverse full paths and have at least 6L edges. All claimed graph restrictions and finite alphabets hold simultaneously for fixed girth.
- The AC transfers apply to the final network and compute the shrinking cosine from the final bus count, so their structural corollary is valid.

### Algebraic singleton result

The root-isolating interval describes a compact basic closed singleton. In the arithmetic chain, each original coordinate has a designated scalar-affine replacement; the source's introduction and Lemmas D–G explicitly exhibit those replacements. Rational forward maps place every coordinate in Q(alpha), and affine recovery of irrational alpha forces equality of the designated coordinate field. The electrical transformations retain that original root voltage and add only uniquely determined rational coordinates. The rational-alpha single-bus case, Eisenstein degree construction, and exact AC magnitude/reference-box conclusions are all correct. The proof properly distinguishes one coordinate's field from the field jointly generated by all coordinates.

### Residual correspondence and tiny infeasible family

- Each copy residual accumulates by at most epsilon per extension, giving delta=6m epsilon. The addition bound is epsilon+3delta. For inversion, positive `v_I>=1/2` permits dividing the I residual, and `|h'|<=2` on `[1/2,2]`. The resulting bound is exactly `10epsilon+10delta`; the forward canonical extension gives at most twice the source residual. The argument treats the full original bus equations and exact voltage boxes.
- The recurrence family forces positive `delta_(j+1)=delta_j^2/(1+delta_j)` and is incompatible with its final equation. All exhibited source values satisfy their intervals; only the last electrical D bus violates an injection, by `1/(d_k+1)`. The denominator recursion and strict bound are correct at k=0 as well as later k. Compactness supplies strictly positive minimum residual. Counts `4k+3` variables and `4k+4` equations give the displayed graph-size upper bounds, and connectedness follows from the actual incidence connections.
- The accuracy consequence is stated as a failure of universal residual thresholds, not as a decision-algorithm lower bound. Exponential witness coordinate precision is not conflated with polynomial-size input construction.

### Polynomial-minimum separation

I verified the original JPT PDF p.2 formula and hypotheses. Its bound is `(2^(4-q/2)*Htilde*d^q)^(-q*2^q*d^q)`. With d=2 this gives exactly the manuscript's `-q4^q` exponent. The epigraph T is nonempty, compact, and connected through its top face. It has 4n+2 weak quadratic inequalities in q=n+1>=2 variables; singleton voltage intervals and degeneracy do not violate the theorem. Clearing denominators preserves the set and gives integer coefficients with polynomial bit length, including the objective. For fixed numerical alphabet and bounded degree, H can be constant and tau is O(log n), giving the claimed scale. The tiny family has linearly many buses, so it supplies the matching worst-case exponential logarithmic scale.

### Promise certificates and reactive stability

The gradient row-sum bound 4UD is valid, interval distance is 1-Lipschitz, and dyadic rounding followed by clamping preserves singleton and general rational voltage intervals. The chosen mesh has polynomial encoding length and proves the stated promise completeness and soundness, without claiming a polynomial search algorithm or solving an unpromised threshold problem. D=0 and empty-network cases are covered.

For reactive stability, the energy is bounded below by `(2/pi)*ell^2*theta^T L_g theta`, then Cauchy–Schwarz and the centered Poincare inequality give both estimates with the stated powers of lambda2 and ell. Each bus's active discrepancy is nonnegative and bounded by half U^2 times the total energy. Replacing the sine bound by `t sin t>=t^2/2` gives rational constants 2 and 2. The path argument yields `lambda2>=2g_min/(n-1)^2`. Substituting ell=1/2, U=4, g_min>=1, and `||q||_2^2<=n eta^2` gives exactly `256n(n-1)^2 eta^2`. Isolated buses and disconnected component centering are treated correctly; the real-angle hypothesis is not replaced by a principal-angle one.

## Primary-source checks

- Toolbox: read Theorem 1, Definitions 4–5, Lemma A and its proof, and the coordinate-preserving arithmetic reductions. Original p.6 was rendered and visually checked, revealing M1; source p.4 was independently extracted for the field-recovery dependency.
- Dobbins et al.: verified Theorem 2.1, its bounded-witness definition, and its three crossover equations against the [primary article in PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10244296/). The Utrecht PDF URL returned HTTP 403 in my browser tool; the openly accessible PMC copy supplied the needed evidence. No inaccessible text is claimed read.
- JPT: independently extracted the original archived PDF p.2 and verified the explicit base/exponent, objective coefficient condition, even-degree hypothesis, and compact-connected-component requirement.
- Bienstock–Verma: the manuscript's scope distinction concerns the previously verified lossless sine-equation approximation question and is consistent with the accepted model discussion.

## Verification artifacts

Repository-relative `paper-power-flow/verification/reviewer4/stage03-round01/` contains:

- `developments-check.log`: the frozen exact checker passed 49 generalized crossover profiles, 8 generalized inversion profiles, the three-component connector, three subdivision scales, 360 perturbed original-network profiles, tiny instances k=0,...,10, and 100 exact Poincare/Lipschitz samples. For example k=10 has 479 buses, 524 lines, and an exhibited residual denominator of 1385 bits. The checker appropriately makes no claim that these finite samples prove planarity or quantified theorems.
- `source_normal_form_counterexample.py` and its log: exact reproduction of the inactive-branch normal-form failure in M1.
- `toolbox-p6.png`, `linear-extension-source.txt`, and `jpt-source-p2.txt`: independently rendered/extracted primary passages.
- `build.log`, `build/`, and `manuscript-layout.txt`: successful independent frozen LaTeX build, without final warnings, undefined references/citations, or overfull/underfull boxes; compiled text extracted for checking.
- `manifest-check.log`: all frozen source hashes match their manifest.

No optional extension is required beyond resolving M1 and correcting m1. After the major dependency is repaired, the changed universality statement and its consequences require another independent review round.

Artifact packaging note: the review artifacts were relocated byte-for-byte from the repository-root `verification/reviewer4/` directory into `paper-power-flow/verification/reviewer4/`. Historical command and build logs retain their actual original paths.
