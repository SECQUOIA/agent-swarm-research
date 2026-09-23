# Stage 7 independent review 5

Reviewed: frozen synthesis and mathematical integration, 2026-09-22.

**Verdict: clean. No major or minor correction requests.**

## Scope and evidence

I read the stage 7 author report, current and historical coverage maps, stage 7 literature audit, main wrapper, abstract/introduction, setting, new formal overview, discussion, the complete Gram-map section, infinite-example section, and approximation section. I also checked the main certificate and consequences statements and proof setup, the PDLC theorem and external-input statement, and the many-row appendix's directional argument against the introductory summaries. I compared the three conjecture descriptions directly with the available primary BDS v2 text (`/tmp/quadratic-paper-literature/bdsv2.txt`, Conjectures 3.1–3.3), rather than relying only on the manuscript's source audit. The repository frontier-note headings and coverage inventory are consistent with the resulting section and appendix coverage. This review concerns synthesis and its newly introduced proof, not a claim to have independently rebuilt Lean or re-audited every earlier stage proof.

## New all-r two-point proof

The proof of Theorem `thm:ball-hulls` works for every r >= 2, including its previously difficult two-dimensional vector case. With a = sqrt(p), b = sqrt(q), the relation e perpendicular to b*u-a*v gives b(u·e)=a(v·e), hence precisely the common gamma used in the text. The perpendicular unit vector exists even if b*u-a*v=0. Strict scalar feasibility gives a nonempty interval max(0,(1/2-h)/(ab)) < k < 1. The roots of t²+2 gamma t=k have opposite strict signs because k>0. Substitution gives the stated norm increases p*k and q*k and inner-product increase ab*k. The displayed positive weights sum to one and their weighted t values cancel. Consequently both new points are strictly feasible and their convex combination is the original point. There is no unmentioned direction perpendicular to both original vectors and no r>=3 dependency.

Necessity uses good multipliers already established without the hull theorem. The subsequent cone-generation argument therefore introduces no circularity. The PD/PSD Schur-complement descriptions, strict-to-closed mixing argument, compact weak-system hull argument, and countable-dense weak description remain valid with the replacement proof. In particular, M(0,0,1/2) is positive definite, and the small scalar increase used after mixing handles the case where the lift parameter equals 1/2.

## Cardinality, quantitative results, and synthesis

The abstract and introduction distinguish nonconstant globally convex certificates from good hull-defining aggregations. They preserve nonemptiness and properness hypotheses, signed PDLC versus nonnegative aggregation, and strict versus closed hulls. The strong arbitrary-quadratic claim is supported by the planar analytic-arc proof: a nonzero degree-at-most-two restriction has finitely many zeros on the compact arc, identically zero restrictions cannot occur in a strict description containing the planar origin, and countably many finite zero sets cannot cover the arc. The closed claim is expressly finite and nonstrict; it does not exclude the countable dense family or either finite semidefinite lift.

The approximation section restricts its quantitative lower bound to good aggregations, allows interior multipliers and rescaling, and supplies the N+1-witness argument. The norm bound yields sqrt(2)/(2000*N²), matching the main theorem. Objective-specific exactness does not conflict with a lower bound for one family used uniformly over all objectives. The abstract and discussion do not convert these geometric bounds into runtime claims.

The Gram threshold and its exceptional image formula are correctly scoped: the full map has HHC also at k=r=1, whereas the displayed hypograph formula excludes that case. The introduction does not turn the full-map necessity into a necessity for every smaller family of repeated-block outputs.

## Prior work, coverage, and formal scope

The conjecture mapping is accurate against BDS v2: 3.1 is the HHC infinite-necessity question, 3.2 proposes a six-necessary PDLC example, and 3.3 is the nonnegative nonconstant convex certificate characterization. The four-bound discussion explicitly attributes the known bound and sharpness example, acknowledges the dissertation's stronger regular weak statement, and limits the contribution to the strict transfer. The fidelity identity, QMP convexification principles, approximation exponent, and objective duality are credited as prior ingredients. I found no contradiction between these detailed qualifications and the abstract or final discussion.

The current coverage inventory incorporates the direct r=2 proof and the completed many-row cone counterexample, while identifying superseded dimension bounds and constants. It does not present the historical proposed arbitrary-cone two-bound as a theorem. The main formal table explicitly excludes the improved paper-only lower constant, the shorter SDP-objective formulation, arbitrary-quadratic obstruction, general Gram threshold, PDLC and appendix results. Thus the integration does not advertise blanket formal verification of the whole manuscript. Unresolved algorithm design questions are delimited as outside the structural theorems rather than concealed proof obligations.

No manuscript edits or verification runs were performed by this reviewer. No unsupported priority, mathematical, or consistency claim requiring correction was identified within the reviewed stage 7 scope.
