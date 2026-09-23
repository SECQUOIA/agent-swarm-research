# Stage 2 independent review 1

**Verdict: no major issues and no required minor corrections identified.** The Stage 2 change is mathematically sound. I recommend accepting it and proceeding to the integration stage. This verdict concerns the frozen manuscript and supporting checks, not a guarantee that external peer review will identify no issue.

## Scope and independence

I read the entire `stage2-snapshot`: the driver and abstract, macros, all eight section files, both appendices, bibliography, and all four Python checkers. I also read `stage2-author.md` and inspected the Stage 2 AC/checker/verification diff. I did not read the other new reviewer reports, rely on earlier PASS labels, edit manuscript files, or spawn another agent.

I reconstructed the main mathematical arguments directly. I reran all four frozen checkers from my own directory, `reviewer1-stage2/`, and added independent symbolic, geometric, and rational-linear-algebra checks there. All five executions exited zero. The finite checks supplement the proof reading; they do not establish the universally quantified claims.

## Stage 2 change: AC potential encoding

The replacement of explicit fundamental-cycle equations by root-normalized vertex equations is correct.

- The orientation is consistent: for an oriented line from j to i, the manuscript has `delta_ij = alpha_i - alpha_j + 2*pi*k_ij`; hence `a_i-a_j=k_ij` gives `theta_i=alpha_i+2*pi*a_i` with the required ordinary edge difference. The sign is not reversed.
- Forest propagation determines each vertex shift as a sum of signed integer edge counts. Root normalization removes exactly one constant per connected component. Therefore real quantification suffices and integrality is a consequence, not a hidden requirement.
- The non-tree equations are consistent exactly when fundamental-cycle sums vanish. Conversely the vertex differences telescope on every cycle. Isolated vertices, disconnected graphs, and zero vertices are covered.
- Four variables per vertex and one per line are sufficient. The crossing disjunction has constant size; expanded injections contribute a constant number of monomial occurrences per incident line. The linear counts for variables, atomic predicates, and monomial occurrences are justified. Rational coefficients and graph indices require polynomial, rather than necessarily linear, bit length, as the theorem states.
- The new source acknowledgment appropriately treats vertex potentials and zero winding as established graph/network mathematics. The claimed contribution remains their use with a rational phasor branch rule for this exact decision formulation.

The supplementary all-simple-cycle oracle is logically independent of forest propagation. In my additional check, exact rational Gaussian elimination on the incidence equations agreed with the checker on 420 reproducible graph instances of orders 1 through 12. This tests a separate computational formulation of the consistency condition.

## Ordinary electrical gadgets and structural restrictions

I found no gap in Sections 2--4.

1. Positivity justifies replacing `x=1` by `xx=1`, and unused variables remain actual coordinates. Pinned-bus complement and addition equations have the stated constants. The allocation rule needs at most two extensions per request and never reuses a requested bus. Repeated names therefore create distinct incidence attachments, including normalized `xx=1`.
2. In the inversion gadget, direct nodal elimination gives `I=x`, `W=2*x-1+1/x`, and `y=W-2*x+1`. The stated range of W follows from its unique interior minimum and endpoint maximum. I verified the nodal identities symbolically for a symbolic complement constant, so the ordinary and enlarged constants are checked by the same calculation.
3. Free-injection redundancy is valid on the entire voltage box. Its use is not limited to exact source solutions. Bus/line counts, simplicity and degree three follow from the explicit allocation and gadget sizes.
4. The arithmetic crossover has unique extension. The transmitted wires retain `[1/2,2]`; only local sums need `[1,4]`. Successive crossovers do not require transmitting those sum coordinates through later crossings. This avoids the bounded-witness versus bounded-solution-set issue in the imported theorem.
5. The electrical planarization uses the incidence rotation order to order the variable path. Each variable disk contains an open path with outward equation attachments, and each inversion disk contains a three-leaf tree. Doubling one occurrence corridor leaves its two ports adjacent. A three-leaf tree can meet either cyclic order, so no extra embedding constraint is left unproved. Repeated names remain separate occurrence corridors and separate electrical buses.
6. For the enlarged complement constant `9/2`, the fixed injections are `-5/2`, `-3/2`, and `-17/2`, as stated. An inversion solution in the enlarged box must in fact have both operands at most 2, so W retains its valid range.
7. Each nonempty electrical component contains an arithmetic root with a free injection and degree at most two. The connector uses its one available degree and preserves all constrained injections. Choosing an incident face as the exterior face is valid independently for each disconnected component. The zero-variable case is explicitly treated.
8. Zero-injection internal subdivision buses impose the discrete harmonic equation because their voltages are positive. Endpoint current is divided by `4L` for both original conductances. Scaling all old injection intervals therefore gives exact equivalence. Even path lengths imply bipartiteness, and an old simple cycle has at least three edges, yielding girth at least `6L`. The finite alphabet and polynomial-size statement are appropriately for fixed L/fixed girth.

The finite crossover drawing in my added checker has no proper straight-line edge crossings. I also reran the full 12,751-profile ordinary suite and structural/residual suite. I did not infer the general disk-and-corridor proof from these finite instances.

## Full-manuscript mathematical checks

- **Foundations:** the rational quadratic membership encoding and dissipation identity are correct; signed injections respect losses. The certificate consequence correctly concerns arbitrary polynomially verifiable certificates and does not confuse irrational coordinates with exclusion from NP.
- **Remaining AC results:** expanding complex power gives the stated signs for both series susceptance and shunts. The short-arc rule treats the branch-cut endpoints and negative cosines correctly without squaring. The equal-angle energy proof requires ordinary real differences strictly below pi, exactly as stated. The four-cycle is a genuine principal-only counterexample. The shrinking window excludes every fundamental-cycle winding and has logarithmic coefficient bit length. Reference-fixed angle boxes remove common rotation. One-sided reactive intervals force exact zero by cancellation, without a claim about symmetric tolerances.
- **Rational universality:** the denominator collection in the basic-closedness invariant is sufficient; compactness permits a common positive rational separation from denominator zeros. The equations defining the candidate inverse image then give both inclusions. The three-quadrant obstruction follows from the lowest homogeneous terms and a direction avoiding their finitely many zero sets. The simplex nonface construction gives the required rational basic closed realization of a finite complex. Its topological use does not claim a rational triangulation. The algebraic-degree result retains one affine recovery coordinate and thus proves the individual-field claim, not merely a field generated jointly by all coordinates.
- **Arithmetic appendix:** circuit evaluation is unique, and scaling both sides of every multiplication uses the two products displayed. The shifted addition, shifted product, square decomposition, and reciprocal-square identities reconstruct correctly. The square gate has `h=1/(a*(a+1/2))`; its output is exactly `a^2`. At the base point all those rational gate coordinates are strictly interior. Continuity supplies one neighborhood for the finitely many gate types; compactness subsequently supplies the source scaling. The inverse algebra holds for every bounded final solution, so the range argument is not used circularly to exclude extraneous solutions. The Boolean-branch example supports the stated limitation of the cited broader universality claim.
- **Residual correspondence:** path errors accumulate at most `6m*epsilon`. The derivative bound for h is 2 on the ordinary source box. The reverse constant `10*(6m+1)` follows after the weighted D-bus and C/I-bus errors are combined. The recurrence starts at `delta_0=1/2`, gives `d_(j+1)=d_j*(d_j+1)`, remains in all source intervals, and contradicts the last equation. Exactly one D-bus residual remains in the canonical electrical extension. Compactness proves that the minimum is positive; the exhibited point only bounds that minimum above, as explicitly distinguished.
- **General residual separation:** the epigraph has `4n+2` inequalities, is compact and connected, and its objective minimum is precisely the residual minimum. The imported bound applies with ambient dimension `q=n+1>=2`, even degree bound 2, and coefficient height including the objective. Its exponent becomes `q*4^q`. Fixed rational data and bounded degree make the cleared coefficient height constant. The claimed worst-case exponential accuracy-bit scale is consequently supported.
- **Certificates and stability:** the voltage-box Lipschitz bound `4UD` is safe. Dyadic rounding followed by clamping preserves exact singleton bounds and polynomial bit length. Promise completeness/soundness are stated with distinct thresholds. The energy, Laplacian and active-error inequalities have the stated constants; the simple-path argument yields `lambda_2>=2*g_min/(n-1)^2`. Substitution yields the coefficient 256 in the final residual transfer, and singleton/disconnected components are covered.
- **Integration and exposition:** the introduction distinguishes the physical resistive model from the linear DC approximation, the known AC NP-hard subclasses from this subclass, exact feasibility from gap promises, and fixed numerical data from size-dependent principal cosines. The abstract and conclusion do not contradict the proved scope. I found no unsupported inference from numerical tests to a theorem.

## Primary-source checks

I checked the actual local Art Gallery PDF page 11, including the displayed three equation types, explicit source interval, and Theorem 7, rather than relying on the text extraction's missing display. The page extraction is saved in my directory.

I read Definition 4 and the Boolean preprocessing discussion in the local Dynamic Toolbox primary extraction. Its rational-coordinate definition matches the manuscript's relevant definition; the inactive-branch example is a valid objection to unique extension. The manuscript supplies its own conjunction-only gate proof, which I checked directly.

The published Dobbins et al. source confirms the bounded-witness premise and the three-equation crossover; the manuscript accurately credits and strengthens the needed solution-set property by its own explicit bounds. The initially attempted PMC page returned a browser challenge, so I used the published PDF available through the German National Library: [Dobbins et al., Theorem 2.1 and Figure 3](https://d-nb.info/1263469019/34).

I checked the compact triangulation premise and the finite-complex statement in the primary author manuscript: [Ohmoto--Shiota, Theorem 1.1 and Section 1.2](https://eprints.lib.hokudai.ac.jp/repo/huscap/all/71421/C1_triangulation_JT.pdf). This supplies exactly the imported topological step.

I read Theorem 1.1 in the cached published Jeronimo--Perrucci--Tsigaridas extraction, confirming the compact connected component, degree, dimension, coefficient-height hypotheses, and numerical bound. I also read the cached Jafarpour et al. Theorem 3.6 and the Farivar--Low angle-recovery discussion. The attribution of winding/potential ideas is consistent with those sources; Farivar--Low's extracted equation displays are incomplete, so that text reading alone was not treated as a verification of every printed formula in their theorem.

## Actual findings and optional improvements

**Major issues:** none identified.

**Minor corrections required for Stage 2:** none identified.

**Optional integration improvement:** Appendix B's historical solver narrative and references to earlier repository checks could be compressed in the final submission package. The current text already says those outputs are not exact certificates, and the mathematics does not depend on them, so this is editorial judgment rather than a correctness or completeness finding.

## Limits

This was a complete manuscript/proof/checker reading with reconstructed derivations and targeted primary-source verification. I did not reprove imported ETR completeness, triangulation or the general polynomial-minimum theorem. I did not perform an exhaustive search of every possible prior electrical universality result or an independent publisher-metadata audit of every bibliography entry. I did not run a new solver experiment or a formal proof assistant. These limits do not expose an unresolved mathematical issue in Stage 2; they bound the strength of this review verdict.
