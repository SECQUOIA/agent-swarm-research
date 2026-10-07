# Stage 6, round 1 — review 01

I reviewed the entire introduction and Section 6, with extra attention to the telescoping identity and the physical price response. I found no mathematical defect requiring correction.

## Proof and hypothesis checks

Locations below refer to `sections/06-synthesis.tex` unless stated otherwise.

- **Lines 11–63, endpoint certificate and exposure.** Expanding each summand gives the stated linear coefficients and cancels every square except the last. The weights are strictly positive. Since the two endpoints of every conditional interval are distinct, equality is equivalent to exactly one active endpoint per coordinate. The triangular recursion is feasible for every bit vector. Terminal values uniquely recover the bits. The exposing inequality has the correct direction and proves uniqueness, including the two terminal extremes. The published alternative direction is accurately attributed: Gärtner et al., original PDF p.8, Definition 11 and Lemma 12, gives the displayed cubic-power direction; its parameter bound follows by summing the geometric series of even powers.
- **Lines 66–181, physical path, relay and penalty.** I independently derived both internal physical rows before normalization: capacity gives `t_j >= t_(j-1)` and the midpoint upper quality gives `t_j <= s_j-t_(j-1)`. The relay reset equation copies the rightward flow without changing source/product degree. The source count `2n-2`, arc-variable count `4n-4`, duplicated supply sequence and endpoint capacities agree. For the tangent direction, `d_j/s_j = 3s_j`; the sum of these coefficients is `1-s_1`, so the base revenue bound of three holds uniformly in the entire parameter interval. The constant revenue offset excludes the varying final revenue. The penalty is a physical revenue change: its first part rewards all source throughput and its second part rewards exactly the reset demands. All relaxed contract deficits are nonnegative because the corresponding upper bounds remain. Applying the actual lemma `s3:hoffman` with integral coefficient bound one gives `H=N^N`; its maximum row violation is at most the sum of contract deficits. Thus `M=3H+1` strictly improves every flow with a nonzero deficit, uniformly in price, and has polynomial bit length. The argument uses no nonlinear repair and correctly retains nonlinear interface contracts later.
- **Lines 184–241, output descriptions and coordinate ports.** Every unique exposed vertex persists for an interval of prices. Distinct terminal values give distinct slopes and supporting lines. The line-factor argument applies to graph and epigraph boundaries after deleting identically zero polynomials. The state message has exactly one segment between consecutive exposed projected vertices. The backward recurrence has the correct sign and constant update. Fourier–Motzkin elimination preserves two variables per row, and the proposed simplex midpoint witnesses the coordinate-projection obstruction. The arbitrary-linear-image exclusion is explicit.
- **Lines 243–437, nonlinear interface and geometry.** The stated contracts force all six interface flows and `q=2-t`; only `z>=t-t^2` is nonredundant. The economic objective is exactly the displayed path linear form minus `z`. This proves the complete finite optimal set, not merely a selected family of optimizers. The strict-local proof correctly uses edge directions to control the entire tangent cone; the terminal denominator bound makes the perturbation strictly smaller than every nonzero terminal difference. Additional clean flow strictly lowers profit. The parity argument proves the integer-coordinate lower bound even with unbounded integer variables, and the binary-index convex lift attains the count. The hull proof establishes both containments and physical feasibility of every hull vertex, while correctly requiring an optimal vertex for recovery. The relay economics place the nonzero coefficient on the duplicate immediately preceding the next descending step. The general-supply identity also telescopes, and strict supply growth separates both endpoint branches. The counterexample obtained by deleting the pool lower bound satisfies the retained contracts and has the claimed positive profit.
- **Lines 452–503, dense slab.** Both SUBSET SUM directions, the strict integer rounding gap, nonempty-domain argument, polynomial encoding, endpoint-bit certificate and rank-one Hessian check out. The padding fixes local coefficients only after adding the explicitly stated singleton bounds. The distinction from physical degree-two hardness and the bare-path linearization are sound.
- **Lines 507–684, interaction rank and oracle.** Double centering gives the claimed minimum residual rank. The projected boxes have fixed dimension; incremental vertex enumeration can retain original box-corner witnesses. A slice vertex lies on an original vertex or edge, and enumerating additional chords adds only feasible candidates. At fixed total the two sequential linear minimizations preserve global optimality. The candidate objective is `alpha*S+beta+gamma/S`; the minimum cases, singletons and zero-total limit are all covered. The construction stays in one quadratic field with polynomial encoding. The rank-one specialization uses four scalar endpoint products, which is necessary for signed factors. Its breakpoint and recovery work satisfy the claimed arithmetic bound. The Lagrangian cost factors through the input attribute matrix, including signed combination of upper/lower multipliers, and the residual constraint restrictions are explicit. The cost-approximation bound follows from nonnegativity and the total-flow bound.
- **Lines 686–737, parameter matrices and nonlinear leaves.** The two sign branches give an exact reformulation, including `z=0`; finite LP optima yield rational recovery of the parameter. The rank-two construction uses independent supports in the fixed-one and second-factor columns. The convex-singleton example gives precisely Square-Root Sum and makes no unsupported hardness inference.
- **Lines 739–857, adjacent results.** I compared the margin, correlation-face, stability, approximate SDP, anchored common-factor, integer-anchor, and network summaries with their canonical result files. The face selection and affine inverse are valid. Exact LP nonpolyhedrality is separated from finite positive-error LP bounds; SOC, fixed-block PSD and unrestricted PSD claims are distinguished. The inverse-quadratic error constants agree with the canonical transfer estimates. Common-factor optimization, common-distribution hull separation and integer-range telescoping retain their different hypotheses. The network claims retain equality balance, the parallel-path block restriction, and data-dependent simplex coefficients. The power-flow paragraph makes only the stated qualified comparison and does not import a power-flow theorem into pooling.
- **Lines 859–927 and the entire introduction.** The open degree-two problem is not resolved by any displayed response, geometry, or abstract-slab construction. The helper-pool example loses private supplies as stated. I compared the principal abstract, table and roadmap scopes against the relevant theorem statements in Sections 2–5, including growing attribute dimension in the one-pool ETR theorem, certificate versus algorithm distinctions, actual pool interface degrees, exact contracts, redundant versus restrictive common bounds, feasibility-only two-vector scope and retained-coordinate objective restrictions. I found no contradictory scope claim.

## Sources and independent evidence

I read the relevant canonical path/relay/vertex-forcing/slab and low-rank-cost notes, and checked the cited polyhedral error-bound proof in Section 3. Primary-source checks included Gärtner et al. Section 4, Lubin–Vielma–Zadik Section 4.2, Punnen et al. Sections 3.2–3.3, Fawzi–Parrilo Theorem 1 and its SOC discussion, and the quantitative equation (3.11) in the author-hosted LRS manuscript. The LRS exponent and norm dependence used in the canonical approximate-SDP argument match that equation.

I also checked the specific limited comparisons against the [Boveroux et al. preprint, Sections 3.1 and 3.3](https://orbi.uliege.be/bitstream/2268/345162/1/OntheComplexityofLinearProgramswithparametricConstraintMatrices.pdf), the [Hladík et al. author abstract](https://kam.mff.cuni.cz/~hladik/publ/b2hd-HlaCer2021c.html), and [Grothey–McKinnon Section 3](https://arxiv.org/pdf/2002.10899v1). Those sources support the comparisons made here; this is not an exhaustive priority search.

I ran a new exact `Fraction` check over dimensions 2 through 8. All **87,376 ordered vertex pairs** passed the exposing-value identity, uniqueness test and midpoint identity. Two nongeometric rational supply sequences passed all **24 endpoint identities and terminal-distinctness checks**. The following script reproduces these checks with `/workspace/local-home/miniconda3/envs/minlp-notes/bin/python`:

```python
from fractions import Fraction as Q
from itertools import product
count = 0
for n in range(2, 9):
    e = Q(1, 4)
    d = [(1-e)*e**(2*(n-j)-1) for j in range(1, n)]
    vertices = []
    for bits in product((0, 1), repeat=n):
        x, old = [], Q(0)
        for bit in bits:
            old = bit+(1-2*bit)*e*old
            x.append(old)
        vertices.append(x)
    assert len({x[-1] for x in vertices}) == 2**n
    F = lambda x: x[-1]-sum(c*a for c, a in zip(d, x))-x[-1]**2
    for v in vertices:
        assert F(v) == 0
        for w in vertices:
            value = sum(c*a for c, a in zip(d, w))+(2*v[-1]-1)*w[-1]
            assert value == v[-1]**2-(w[-1]-v[-1])**2
            assert (value == v[-1]**2) == (w == v)
            assert F([(a+b)/2 for a, b in zip(v, w)]) == (v[-1]-w[-1])**2/4
            count += 1
assert count == 87376
for supplies in ([Q(1,100), Q(1,20), Q(1,4), Q(1)],
                 [Q(1,33), Q(1,7), Q(1)]):
    terminal = []
    for bits in product((0, 1), repeat=len(supplies)):
        previous, t = Q(0), []
        for bit, s in zip(bits, supplies):
            previous = s-previous if bit else previous
            t.append(previous)
        assert t[-1]-t[-1]**2 == sum(
            (supplies[j+1]-supplies[j])*t[j] for j in range(len(t)-1))
        terminal.append(t[-1])
    assert len(set(terminal)) == len(terminal)
print('87376 vertex pairs and 24 general-supply endpoints passed')
```

These finite exact checks corroborate the algebra; they do not replace the proofs. I made no manuscript changes, read no other reviewer reports, and ran no builds.

## Verdict and limits

**No findings.** I checked every new Section 6 argument and the introduction's substantive scopes. The adjacent programs were checked for correctness of the summarized mechanisms, source matches and hypotheses; I did not independently reconstruct every earlier reduction or every external conic lower-bound proof. Publication priority, full-paper consistency outside the referenced dependencies, bibliography completeness and compilation remain outside this review. No external-acceptance or exhaustive-correctness guarantee is implied.
