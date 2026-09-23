# Stage 6, round 1 — independent review 04

Reviewed the complete introduction and Section 6, with particular attention to the physical optimal set, strict local optimality, integer dimension, exact LP hull, and supply/alphabet extensions. I followed the round instructions and reviewer protocol, read `literature/AGENTS.md`, and did not inspect other review reports or edit the manuscript.

The reviewed working files match the frozen snapshots. SHA-256 values are `5449b1254d6eb682f3238465e01f93b5b493ebdcb068c66edb1d7d8583c928f1` for the introduction and `3c2752d7d04769b796fed4e48cb05259fa313dcd5da006830a3e945db859867c` for Section 6. Locations below refer to the working `.tex` files, which have identical snapshot line numbering.

## Findings

No major or minor mathematical defect identified. No correction is requested. The following records the substantive checks behind that verdict, rather than relying on earlier PASS labels or computational output.

## Main geometry checks

- **Physical interface and isolated global optima — `06-synthesis.tex:243–304`.** The exact demand at product n and supplies of A and B, together with exact pool throughput and demand at W, force every new interface flow other than z. The pool remains active, so its quality is uniquely `2-t`; there is no inactive-quality continuum hidden in the optimizer count. The remaining quality row is exactly `z >= t-t^2`. The stated costs and revenues give `d^T x-z` with no omitted constant. The certificate then makes the global optimal set exactly the `2^n` lifted endpoint vertices. The graph audit gives one cycle, B–P–W–B, and all claimed local degrees are preserved.
- **Strict local optima — lines 306–336.** I checked both the economics of the perturbation and the passage from incident edges to the whole feasible neighborhood. The added revenue and source cost produce precisely `delta t`; they leave the coefficient of extra z equal to minus one. Terminal values have denominators dividing `4^(n-1)`, so the claimed choice `delta=4^(-n)` makes every outward edge derivative strictly negative. If `r_i` are normalized incident edge rays, set `eta=min_i(-grad(H)(v)·r_i)>0`. For any tangent-cone direction `h=sum_i a_i r_i`, `a_i>=0`, one has `grad(H)(v)·h <= -eta sum_i a_i <= -eta ||h||`. Thus the uniform linear decrease controls the quadratic remainder; checking edges is sufficient here. The clean-flow graph is continuous and all other physical coordinates are affine, so strict local optimality transfers to the actual flow set. The final global-optimality argument identifies the unique terminal-one vertex correctly. The proof appropriately makes no claim that its list exhausts all local maxima.
- **Integer dimension — lines 338–362.** The midpoint formula is positive for every pair of distinct selected vertices, because their terminal values differ. The parity argument therefore applies to one arbitrarily chosen lift of each full physical optimizer, including unbounded integer coordinates and arbitrary continuous auxiliaries. With fewer than n integer coordinates, there are too few parity classes. The upper construction also works: an integral point in the binary-coordinate hull must be binary, and a convex combination producing that binary vector can use only its single assigned optimizer. This proves the exact integer count without a formulation-size claim. I checked the attribution against Lubin, Vielma, and Zadik, Section 4.2, Lemma 4.1, in the local original PDF, printed p.12.
- **LP hull and optimizer recovery — lines 364–392.** The certificate supplies the lower containment. Vertex decomposition of x supplies the lower affine graph, and `(x,1)` supplies the upper graph; their vertical segments prove the reverse containment. The graphs never meet because `d^T x <= 1/4`. A hull vertex must lie on one graph and have a path vertex as its x-coordinate. Therefore returning an optimal LP vertex, as explicitly required, really returns a feasible physical optimizer. A general point of the LP optimal face would not suffice, and the manuscript correctly warns about that. Polynomial rational encoding follows from the explicit rational LP and affine physical map.
- **Alphabet and supply extensions — lines 394–429.** The relay has a zero-quality terminal source, so attaching the same interface is valid. In the relay economics the price increment may move to the equal-flow duplicate, but it remains `(s_(j+1)-s_j)t_j`; this preserves the objective. The resulting input alphabet is `{0,1,2}` and the path/reset additions introduce no new cycle. For general supplies I expanded the physical-coordinate identity independently. The squares cancel, the last supply is one, and the remaining linear coefficient of `t_j` is `s_j-s_(j+1)`. The strict condition `s_(j+1)>2s_j` makes the endpoint intervals disjoint and all endpoint systems nonsingular. The equality, midpoint, and hull arguments transfer. The text correctly withholds the specific strict-local perturbation claim for arbitrary supplies.
- **Deleted-throughput example — lines 431–437.** At the displayed assignment the sole pool feed is A with flow one quarter, all B goes directly to W, and the quality at V is exactly its allowed value. Other exact contracts remain satisfied and z is zero. Its profit is `3/16`, so the example correctly demonstrates that deleting the nonlinear interface's pool lower bound changes the optimum. The linear repair penalty is not being applied to a nonlinear feasible set.

## Checks of the remaining introduction and Section 6

- **Introduction, abstract, table, and roadmap — `00-introduction.tex:1–217`.** I compared the principal restriction/algorithm claims with the accepted statements at `s2:etr-complete`, `s2:one-pool-etr`, `s2:pooling-np`, `s3:all-two-thm`, `s3:constant-thm`, `s4:vertex-integrity`, `s4:degree-boundary`, `s5:fixed-products`, `s5:arbitrary-exceptions`, `s5:restrictive-capacity`, and `s5:two-vector-theorem`. The introduction preserves the differences between threshold hardness and feasibility, quality count and affine rank, bounded attachments and long paths, exact contracts and interval supplies, and feasibility-only two-vector results. The isolated-optimum example is explicitly paired with its positive LP-hull result. The roadmap does not incorrectly label the unrestricted one-pool/one-quality threshold problem open.
- **Telescoping certificate and physical price response — `06-synthesis.tex:10–182`.** Expansion gives the stated `d_j`, nonnegativity, endpoint equality characterization, and unique exposing functional. The physical capacity and midpoint quality rows give the required two opposing strip inequalities. The source-cost-zero price identity has a parameter-independent constant. The relay reset is an actual demand equation, not a hidden nonphysical equality. For contract removal, the retained source/reset upper bounds make each deficit nonnegative, all scaled rows have coefficients in `{-1,0,1}`, and Stage 3's proved error bound gives `H=N^N`. The uniform infinity-norm bound of three makes `M=3H+1` sufficient over the stated parameter interval. Both throughput bonuses are implementable by the specified output revenues. No magnitude-independent price claim is made.
- **Output-size and coordinate-port obstructions — lines 184–241.** Each open value segment is a boundary segment and forces a distinct line factor in the product of nonzero defining polynomials. The total-degree lower bound follows for graph and epigraph formulas with no auxiliaries. The dense fixed-objective message has all projected vertices on its upper boundary, giving exactly one fewer intervals than vertices. The backward recurrence is consistent with eliminating the conditional endpoint interval and does not conflict with explicit-output bounds. Fourier–Motzkin elimination preserves the two-variable row property; every coordinate pair of `(1/2,1/2,1/2)` extends into the simplex, establishing the stated coordinate-projection obstruction. Arbitrary linear images are correctly excluded from that obstruction.
- **Dense-slab hardness — lines 444–503.** I checked both rounding directions, the zero-certificate characterization, the nonempty-domain promise, and polynomial binary lengths. In the padded construction every padding upper branch is at least three quarters and is excluded by its singleton upper bound; all free bit patterns still extend. The source weights and objective coefficients remain binary data, so the ordinary-hardness qualification is necessary and present. The bare-path linearization is valid at all its vertices and explains why the additional slab is essential.
- **Interaction rank and exact optimization — lines 505–651.** The double-centering identity proves the claimed minimal residual rank after subtracting additive costs. The projected-box dimension and vertex count are sufficient. At fixed total, an optimal pair of slice vertices exists because the objective is affine in each margin separately. The smallest-face argument ensures that original vertices and edges cover all such slice vertices. Enumerating additional nonedge segments creates only feasible candidates. Corner interpolation gives actual original margin witnesses. The common-total objective is `alpha S+beta+gamma/S`; the stationary-point cases, zero-total extension, comparisons, and reconstruction stay within the stated quadratic-field scope. The rank-one specialization uses four scalar endpoint products and sorted continuous-knapsack envelopes even for signed factors. Its irrational example checks directly.
- **Oracle and perturbation guarantee — lines 653–684.** Dualizing homogeneous quality rows gives `Q Lambda^T - 1 h^T`, with the correct minimization sign. Additive row/column terms do not change interaction rank; upper and lower multipliers use the same input-quality columns. The remaining-constraints qualification excludes extra physical couplings. The error guarantee follows by applying the entrywise perturbation bound twice to nonnegative matrices of total at most `S_max`.
- **Constraint-matrix rank and convex leaves — lines 686–737.** The two sign branches are exact, including the `z=0` case, and bounded parameter intervals keep the zero branch from admitting a spurious w. Rational LP solutions recover rational parameters; finite minima over either nonempty polyhedron are attained even when X is unbounded. The fixed-one column and second factor in the positive-product reduction have independent supports. The singleton leaves are convex sets despite their nonlinear defining equations, and the aggregate condition is exactly Square-Root Sum. The manuscript states an arithmetic implication, not unproved NP-hardness.
- **Adjacent conic/common-factor/network summaries — lines 739–857.** I compared the scopes with the named canonical result files. The correlation face selects equal binary margins, then excludes double choices, then fixes one member per pair; its inverse follows by expanding the four blocks. Exact LP impossibility is separated from positive-error LP size bounds. The entrywise norm and total PSD-order conventions match the cited notes. Common-factor optimization is distinguished from a compact hull, reciprocal leaves require a shared scalar distribution, and the integer-anchor claim is limited to consecutive integers. The network discussion retains equality balances, the restricted parallel-path block class, and the difference between original-space coefficients and extended hulls. The AC paragraph preserves the distinction between real-angle and principal-angle constraints. These paragraphs do not infer physical pooling theorems from adjacent models.
- **Open questions — lines 859–927.** The dense aggregate issue remains after endpoint projection, and the abstract slab is properly used as a warning rather than as a physical reduction. The shared-helper example loses the private midpoint supply relation as stated. The final comparisons preserve each contract, common-bound, objective, and arithmetic restriction.

## Source checks and independent exact evidence

I read the relevant canonical geometry, relay, slab, cost-rank, parametric-rank, convex-leaf, conic, common-factor, network, and power-flow result/note material identified by `coverage.md`, without treating their status lines as evidence. I checked the original Gärtner et al. PDF, Section 4.3, Definition 11 and Lemma 12, printed pp.8–9: its direction is the stated cubic-power direction, and the parameter bound follows by summing the even-power geometric series at epsilon one quarter. I checked the original Lubin–Vielma–Zadik midpoint lemma as noted above. The description of the earlier local-optimum example agrees with [Grothey and McKinnon, Section 3, PDF pp.9–10](https://arxiv.org/pdf/2002.10899v1). The rank-two reduction structure and one-column comparison agree with [Boveroux et al., Sections 3.1 and 3.3](https://orbi.uliege.be/bitstream/2268/345162/1/OntheComplexityofLinearProgramswithparametricConstraintMatrices.pdf).

The following fresh exact-arithmetic check was run with `/home/sgusev/miniconda3/envs/minlp-notes/bin/python`. It does not use the repository's geometry checker and tests physical coordinates directly. Its complete code is retained here for reproducibility:

```python
from fractions import Fraction as Q
from itertools import product

def vertices(s):
    out = {}
    for u in product((0, 1), repeat=len(s)):
        t = []; prev = Q(0)
        for bit, cap in zip(u, s):
            prev = cap-prev if bit else prev
            t.append(prev)
        out[u] = t
    return out

def cert(s, t):
    prev = Q(0); rhs = Q(0)
    for cap, val in zip(s, t):
        assert prev <= val <= cap-prev
        rhs += (val-prev)*(cap-prev-val)
        prev = val
    d = sum((s[j+1]-s[j])*t[j] for j in range(len(s)-1))
    lhs = t[-1]-t[-1]**2-d
    assert lhs == rhs >= 0
    return lhs

nv = ne = nm = 0
for n in range(2, 9):
    s = [Q(4)**(j-n+1) for j in range(n)]
    vs = vertices(s); delta = Q(4)**(-n)
    assert len({v[-1] for v in vs.values()}) == 2**n
    for u, v in vs.items():
        assert cert(s, v) == 0; nv += 1
        for j in range(n):
            w = vs[u[:j]+(1-u[j],)+u[j+1:]]
            dt = w[-1]-v[-1]
            assert -dt*dt+delta*dt < 0; ne += 1
            a = Q(2, 5)
            z = [(1-a)*p+a*q for p, q in zip(v, w)]
            assert cert(s, z) == a*(1-a)*dt**2; nm += 1
ns = 0
for n in range(2, 7):
    s = [Q(1)]*n
    for j in range(n-2, -1, -1):
        s[j] = s[j+1]/(3+j%3)
    vs = list(vertices(s).values())
    assert len({v[-1] for v in vs}) == 2**n
    for v in vs:
        assert cert(s, v) == 0; ns += 1
    for v, w in zip(vs, vs[1:]):
        mid = [(p+q)/2 for p, q in zip(v, w)]
        assert cert(s, mid) == (v[-1]-w[-1])**2/4 > 0
print(f'PASS: {nv} geometric vertices; {ne} strict incident-edge derivatives; '
      f'{nm} edge identities; {ns} nongeometric-supply vertices and '
      'distinct-terminal checks.')
```

Observed output:

```text
PASS: 508 geometric vertices; 3584 strict incident-edge derivatives; 3584 edge identities; 124 nongeometric-supply vertices and distinct-terminal checks.
```

These finite checks corroborate the algebra and derivative calculations; the general arguments above establish the reviewed conclusions.

## Verdict and limits

**No findings.** I reviewed the entire new text and all displayed new proofs, with deeper verification of the assigned geometry topics. I checked earlier accepted theorem statements and the penalty dependency as needed, rather than re-reviewing every proof in Sections 1–5. For the adjacent conic and network programs I checked the stated scope against their canonical notes and the elementary transfer arguments; I did not reconstruct every external extension-complexity theorem or all separate power-flow proofs. I did not perform an exhaustive novelty search, run a manuscript build, or claim exhaustive correctness or external-review acceptance.
