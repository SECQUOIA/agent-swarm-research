# Stage 03, round 01 — review 08

Assigned focus: the explicit polyhedral error bound, coefficient encoding, nonemptiness of the copy polytope, and the subsequent exact penalty.

I reviewed the entire frozen `papers/pooling/sections/03-restricted-hardness.tex` (lines 1–1286). `cmp` confirmed that it matched `process/snapshots/stage-03-round-01.tex` during this review. I read the reviewer protocol and `literature/AGENTS.md`. I did not edit the manuscript or inspect other reports from this round.

## Findings

No major or minor findings. No correction is requested. The following records the mathematical checks supporting that verdict, especially the places where the penalty argument could otherwise fail.

## Explicit error bound

**Lines 799–827, Lemma `s3:hoffman`.** The hypotheses and the constant are sufficient.

1. A nonempty polyhedron is closed and has a Euclidean projection, including when it is unbounded or lower dimensional. For the projection $v$, $h=w-v$ belongs to the cone of the active outward row normals. Opposite rows representing equalities cause no problem: their nonnegative conic hull includes both directions of an equality normal.
2. The independent-support reduction at lines 812–816 is valid. Starting with positive coefficients on the supported normals, orient any dependence to have a positive coefficient and subtract the largest permissible multiple. At least one supported coefficient becomes zero, all remain nonnegative, and the represented vector does not change. Repetition gives independent rows. For $h\ne0$, their number satisfies $1\le r\le N$.
3. For those rows, $Bh$ equals their residual vector because they are tight at $v$. Individual components can be negative; this does not invalidate $\lambda^TBh\le\|\lambda\|_1\eta$, since $\lambda\ge0$ and each residual is at most the maximum positive residual $\eta$.
4. Full row rank gives $\|B^T\lambda\|_2\ge\sigma_{\min}(B)\|\lambda\|_2$. The displayed multiplier estimate consequently holds with $\sqrt r\le\sqrt N$.
5. $BB^T$ is a positive-definite integer matrix, so its determinant is a positive integer. The product of the $r$ singular values is its determinant's square root and is at least one. Bounding the other $r-1$ singular values by $\|B\|_F\le\sqrt{rN}K_0\le NK_0$ gives exactly the stated lower bound on the least singular value.
6. Cancellation and the two norm comparisons give $\|h\|_1\le N(NK_0)^{N-1}\eta$. The distance in the statement is at most this particular projection displacement; the proof does not incorrectly identify Euclidean and one-norm projections. The $N=1$ case also works.

The residuals must be measured after row scaling. Lines 801–802 make that convention explicit. No bound on the magnitude of the right-hand side is required for the mathematical estimate.

I checked the attribution against the local Hoffman original, printed pp. 263–264, as well as its extracted text: [[hoffman1952-on-approximate-solutions-of-systems]] p.1-2. Section 2 supplies the general error-bound theorem; the active-normal cone argument also appears in the source's Lemma 4. The manuscript appropriately presents its coarse integer-coefficient constant as directly proved, rather than attributing that exact formula to Hoffman.

## Copy polytope and penalty

**Lines 843–877.** The choice of variables and residual scaling are sound. Every arc counted in an exact copy-source supply or copy-output demand is included in $w$, including actual pool intakes from conversion sources. The anchor and primary outlets belong to no such copy contract. The separate throughput upper bound supplies $\sum x_i\le2$. Copy-output quality rows are linear because their incident sources have fixed qualities.

Nonemptiness at lines 859–862 does not assume that the original source polytope is nonempty. At zero original signals the homogeneous cone rows hold. Complementary leaves may equal two, and their auxiliary averages generally need not be zero, but filling them at their determined values satisfies the original row-source bounds. The full/half cycles, coupling sources, and complement-flow source splitting preserve this extension. Thus the exact copy polytope contains a point even for a source no instance with no positive-throughput point. This is the correct nonemptiness hypothesis needed for Hoffman.

After deleting lower bounds, the retained upper contracts ensure every deficit is nonnegative. The rows of $A$ have nonpositive residual before and after positive denominator clearing. Leaving $E$ and $-E$ unchanged makes the only possible positive residuals the individual unscaled deficits, each at most their sum $\delta$. There is therefore no omitted scaling factor in (s3:restore-copy).

The bit-length claim is adequate: clearing a row by the product of its denominators has bit length bounded by the sum of their bit lengths. The final network has polynomially many explicitly specified rational entries. A computable integer $K_0\ge1$ therefore has polynomial bit length, and

\[
\log_2 H=\log_2N+(N-1)(\log_2N+\log_2K_0)
\]

is polynomial as well. Neither an optimal error-bound constant nor an algorithm for the projection is needed to construct the instance.

**Lines 879–920.** The nonlinear repair is valid. With $a_i>1$, $S/T\ge1$ whenever $T>0$. The two output capacities and the anchor imply $T\le1+T/S$, and the explicit flow assignment proves its sufficiency. When $T\le1$, output 2 alone suffices; when $T=0$, no division is used. Thus the scalar condition $F(x)\le0$ is exact on the stated throughput domain.

The derivative estimate is valid on the entire convex set connecting $x$ and $x'$: $|T-1|\le1$, $0\le S\le2a_{\max}$. A necessary radial repair occurs only when $T'>1$ and $S'>1$, so the division by $S'$ has a uniform denominator bound. The scaling factor preserves the composition and reaches its true radial maximum. Its removed mass is exactly $F(x')/S'$. Scaling the original signals preserves the homogeneous cone; rebuilding complementary ports and averages is essential and is explicitly prescribed. The proof does not incorrectly scale all physical bypass flows.

**Lines 916–958.** The objective estimate and strict penalty follow. For the original intake objective, the two intake displacements give the constant $C=b_{\max}(1+L)H$. For the economic realization, the private conversion-port objective can differ from $b^Tx$ at a relaxed point, and the manuscript correctly bounds this first displacement in the full vector $w$. Only at the exact point does it use the copy identity. It then bounds the radial change through the intake objective, without requiring a bound on the total displacement of all rebuilt copies.

Every deficit is penalized, $M_0=C+1$ is explicitly computable, and a contracted repair beats every point with positive deficit. This proves the claimed equality of optima, including the case where the source composition polytope is empty. The economics offset cancels through total mass conservation, and its size covers the possible combined input rewards. Normalizing qualities after computing the penalty changes no feasible flow or profit. The text correctly limits this large-coefficient construction to ordinary hardness.

As a supplementary check, I read and ran `code/pooling_bypass_copy/independent_penalty_bound_review.py`. It passed 500 exact rational radial/error estimates, including 183 nontrivial repairs, and 12 encoding bounds including 258-bit coefficients. These finite tests support the arithmetic check; they do not establish the error-bound theorem or replace the proof above.

## Remainder of the stage

- **Lines 20–160:** Checked the restricted satisfiability orientation construction, triangle saturation, both directions of subdivision, the edge-cost equality conditions, the two physical degree patterns, and the separate capacity-removal and partition extensions. I found no reduction-direction or capacity discrepancy.
- **Lines 161–340:** Checked pure-mode cleanup, bipartite matching replacement, the independent-set identity and constructive recovery, the redundant merged lax-output constraint, weighted rewards, and the positive-tolerance loss estimates and example. I verified the explicit edge-three-colored cubic source claim against the original author manuscript, pp. 25–26: [[chlebik2006-complexity-of-approximating-bounded-variants]] p.25-26. I did not rederive its underlying PCP gap.
- **Lines 342–548:** Checked the determinant-based fractional-coordinate bound, the corrected large-$p$ separation, the product identity and positivity estimates, simplex normalization, both directions of the two-pool reduction, topology, and the FPTAS grid argument. The large-$p$ proof is supplied independently of the stronger printed Matsui estimate. I consulted the locally extracted Matsui report for the source formulas and the stated scope of that estimate; the manuscript's displayed arithmetic was checked directly.
- **Lines 550–790:** Checked full and half port equations, homogeneous-row realization, averaging bounds, closed-cycle saturation, separate coupling of full and half cycles, and source splitting. In particular, the cycle equality argument tolerates distinct positive endpoint qualities and zero signal flows.
- **Lines 967–1163:** Checked the least-significant-bit-first multiplier, bounds on all partial sums, rational denominator clearing, finite flow/quality alphabets, the normalized factor inequalities, two-feed mass identity, and physical threshold circuit. The completion objective only tests simultaneous exact contract attainment, so it needs neither a nonempty contracted polytope nor an error bound. This is correctly separated from the earlier penalty argument.
- **Lines 1165–1264:** Checked slack comparisons, grouping complementary unused ports, splitting supply-four as well as supply-two sources, exact output qualities, removal of unnecessary designated ports, and the count of three exceptional inputs plus two exceptional outputs. These operations preserve the physical threshold circuit and exclude zero original intake where required.
- **NP membership and scope:** Checked the uses of accepted Section 1's endpoint disjunction and Section 2's pooling certificate scopes. Fixed pool-quality dimension applies to the one-pool constructions; fixed outlet-fraction dimension applies to the two-pool construction with growing attribute count. The final prose distinguishes external sources from actual feeds and separates the different approximation families.

## Verification limits and verdict

This was a mathematical source review of the entire stage with detailed verification of the assigned error-bound and penalty focus. I did not formally verify the proofs, independently rebuild every physical network in software, or re-audit all historical priority statements and the Haugland/Baltean-Lugojan source locators. I checked the applicability of the accepted certificate results rather than reopening their full proofs. No acceptance claim follows from these checks.

**Verdict: no findings.**
