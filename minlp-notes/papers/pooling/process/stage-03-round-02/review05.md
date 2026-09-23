# Stage 3, round 2 — independent review 05

Reviewed the entire `sections/03-restricted-hardness.tex`, lines 1–1294, against the round instructions and reviewer protocol. Both the manuscript and frozen snapshot have SHA-256 `b8201a4bc6a61d4304f888649afe97bfc4aeefd9234d314a8cae3b805b3fad40`. I did not consult other current-round reports, edit the manuscript, or delegate review work.

No major or minor findings. The following records the substantive checks behind that verdict; these are verification observations, not requests for changes.

1. **Orientation and degree restrictions, lines 20–153.** The occurrence cycle forces equality of copies while allowing each literal at most two occurrences. Private weight-two triangles force their attached unit edges into the clause vertices. Both orientation directions survive bipartite subdivision, including the case where neither half-edge enters the subdivision vertex. The two physical placements give the stated degrees and threshold equality conditions. The omitted-pool-capacity variants need only a load dominated by the physical endpoint throughput, which is what the proof establishes. The PARTITION variants are properly limited to ordinary hardness. The LP reduction for pool minimum degree one preserves each incoming quality mass.

2. **All-degree-two, weighted modes, and tolerance, lines 155–348.** Cleanup preserves strict and dirty flows separately while decreasing resource use. Fixed mode choices yield a capacitated bipartite flow problem. The weighted extension retains both physical arc capacities in each mode bound; signed rewards do not invalidate cleanup or integral optimization. The independent-set recovery on twice-subdivided matching edges is constructive and does not introduce interference between modifications. Merging lax outputs adds a constraint already imposed in pure modes by the shared dirty input. The factor-three approximation transfer and the positive-tolerance loss estimate have the stated directions and constants. The K4 witness has profit `3+2δ`, whereas integral unit-capacity flows at `δ<1` remain zero-tolerance feasible. The two full-class threshold NP statements now expressly require upper-only endpoint specifications, matching the Section 1 certificate.

3. **Corrected Matsui source, lines 350–425.** An active square system exists at every vertex even if the polytope is lower-dimensional. Its integral coefficients have absolute value at most one, and the chosen determinant bound supplies the coordinate separation `h`. At the largest fractional index `k`, every term involving a larger index cancels. Apart from the `(k,k)` term, remaining exponents are at most `2k-1`; bounding each signed summand below by `-p^(2k-1)` is valid. Thus the repaired estimate follows without the report's invalid arbitrary-`p` simplification. The identity `ph=n^(n^3(n-3))` makes its bracket greater than one. Concavity of `Y-X²` extends the strict vertex separation to all convex combinations. The product identity gives the correct yes/no directions, both factors are positive on the source polytope, and the largest coefficient has `O(n^5 log n)` bits. No assertion of positive generator values for `V` is needed later; the required generator upper bound is sufficient.

4. **Two pools and FPTAS, lines 427–556.** LP normalization preserves the factor product; the safe cut retains every yes witness. Simplex embedding carries all rows, including cube bounds. The argument correctly allows signed individual coefficients while using `a≥1` and `b≥0` only on feasible mixtures. Anchor cancellation enforces each row through any positive outlet. The physical radial maximum is attained, and the threshold equivalence is exact. Tree topology, suppression to one bypass, economics, redundant bounds, and exact unit demands are consistent. The grid FPTAS handles the zero grid and zero optimum, uses polynomial-bit rational LP solutions, and requires the supplied family representation.

5. **Copy networks and penalty, lines 558–967.** Full and half ports, signed children, padded averaging trees, distinct port occurrences, conversion feeds, separate closed cycles, and full/half coupling preserve the stated projections. Positive conversion endpoint qualities are the hypothesis needed for the upper-only cycles. Complement-flow collectors preserve equations while reducing input degree. The explicit error bound follows from the active-normal cone and the singular-value product bound. Contract residuals remain unscaled, so the bound applies to total deficit. Radial repair only divides by `S′` when it exceeds one, preserves the homogeneous source cone, and gives the stated profit estimate. The separate private-input economics estimate does not assume relaxed copies are equal. All penalty constants have polynomial bit length.

6. **Constant data and five exceptions, lines 969–1272.** Least-to-most-significant averaging implements each dyadic coefficient. Splitting signed rows and choosing `B` as stated keeps every nonnegative partial sum below two, including affine constants. The attained generator lower bound and coarse upper bounds justify dyadic normalization, positive integer `b_i`, and the claimed quality interval. Only the two converted master signals become actual feeds. The physical threshold circuit excludes zero intake. Completion reaches its upper bound exactly when every removed contract holds; the bounded economic offset preserves that objective. For feasibility, slack comparisons, complementary-port grouping, and splitting both supply-two and supply-four sources preserve the original equations. Copy tightness is established independently of filler supplies, so grouping is not circular. The two conversion fillers and anchor are the three variable inputs; the two primary outputs are the remaining exceptions. The data palette, degree counts, redundant pool bound, and strong-hardness claims follow. No approximation gap is inferred from constant data.

I checked Section 1's endpoint-disjunction argument and Section 2's basis-index certificate and pooling parameterizations against their uses here. All fixed-quality/fixed-outlet applications have bounded flow fibers. I compared the seven canonical Stage 3 result files with the manuscript, and read the distinct positive-tolerance, positive-product approximation, degree-four, degree-three, closed-cycle, linear-universality, and weighted-mode notes. Their relevant mathematical guarantees are represented; historical PASS labels were not used as evidence.

Source checks included Matsui's local METR95-13 original and extracted text, especially pp. 2–7. I visually checked the original PDF pp. 3–4: the stated arbitrary-positive-integer-`p` theorem and the problematic simplification are actually printed there. The manuscript and bibliography expressly limit those locators and the counterexample to the report, without attributing a verified defect to the unavailable journal version. Chlebík–Chlebíková's author manuscript pp. 25–26 explicitly constructs the edge-three-colored cubic source and preserves its objective/gap. Asahiro et al., Section 5, supports the credited starting orientation construction. The local final Haugland 2016 discussion at printed p. 214 and Haugland–Hendrix 2016 at printed p. 607 support the parameter questions as described. The published [Baltean-Lugojan–Misener article, Remark 4.6](https://link.springer.com/article/10.1007/s10898-017-0577-y) does assert one-pool capacity hardness, as the manuscript carefully states. An initial PMC access attempt returned a browser check; the publisher's article was accessible.

For reproducibility, the only new arithmetic execution was this exact standard-library check of the report counterexample:

```bash
python - <<'PY'
from fractions import Fraction as F
n,p,e=5,2,F(1,4)
r=[F(1,2)]*n
X=sum(p**(i+1)*r[i] for i in range(n))
Y=sum(p**(2*(i+1))*r[i] for i in range(n))
D=Y-X*X
bound=p*p*e/2-p*n*n
assert D == -279 and bound == F(-99,2)
print(X, Y, D, bound)
PY
```

Output: `31 682 -279 -99/2`. This verifies that particular arithmetic example, not the asymptotic theorem.

Verification limits: this was a proof and source review, not a formal verification or exhaustive novelty search. I did not independently reprove the literature's underlying approximation-gap theorem, obtain Matsui's journal version, audit every later-stage theorem, compile the manuscript, or rerun historical numerical pooling experiments. Compilation belongs to root under the review instructions.

**Verdict: no findings.**
