# Opus R1 review: upper comparisons, lower reductions, and heights

Date: 2026-10-05. Reviewer: independent Opus review sub-agent, round R1 (no
earlier Opus review). This file is the only file I wrote; I made no manuscript
change. This is an internal analytic review, not external peer review.

## 1. Scope, versions, and method

Reviewed pairs:

- `sections/03-upper.tex` with `appendices/A-upper.tex`;
- `sections/04-reductions.tex` with `appendices/B-reductions.tex`;
- `sections/07-heights.tex` with `appendices/F-heights.tex`.

Interfaces cross-checked against the actual text: `sections/01-models.tex`
(Hessian Gram definition, `lem:models-det-trace`,
`lem:models-gram-curvature`, `lem:models-low-degree`,
`lem:models-strong-convexity`, `lem:models-rational-squares`,
`def:models-circuits`, `rem:models-gram-kinds`); `sections/02-points.tex` and
`appendices/C-points.tex` (`lem:convex-value` statement and proof,
`thm:global-point`); `sections/06-algebraic.tex` and `appendices/E-algebraic.tex`
(`lem:algebraic-gram` with its covariance proof, `lem:quartic-realization`
with its proof, `thm:singleton-field`, `thm:algebraic-cyclic`);
`sections/08-fields.tex` (certificate definitions and its use of
`rem:heights-gram-field`); the statements of `cor:structured-single-sign` and
`cor:constraints-binary` in `sections/05-constraints.tex` (interface only);
and the introduction's summary rows for these results.

Evidence read: `evidence/BRIEF.md`, `evidence/coverage-map.md`,
`evidence/authoring/{DECISIONS,CONVENTIONS,upper,reductions,heights}.md`,
`evidence/literature-review.md`, and, after my own pass, the Sol R1 reports
`evidence/reviews/{upper,reductions,heights}-r1.md`. I did not adopt any audit
verdict; every proof listed in Section 5 was reconstructed by hand.

The root applied Sol R1 repairs while I reviewed. My verdict refers to the
versions with these SHA-256 hashes (2026-10-05 16:04 EDT):

```text
4e9c21362b7e87a8b8093c1b2aff70aa317552fbdb4c1383b5a15e4dbcd1d219  sections/03-upper.tex
42eec91386c49100c000f9c77ff728772fe5662573fe3b3fd99101b145dfce93  appendices/A-upper.tex
32648ab439cadd654a90c167614d30502c122b0e706882598b8872244c5ff76f  sections/04-reductions.tex
1c78b5cd28b75854390eac3d8f48ffa6c623ecb7061f3bc4142375d70a692b94  appendices/B-reductions.tex
391e702e12dd39d4b61632d239ae0222e84d535b35de7e17b8abda8b9adae470  sections/07-heights.tex
523e1364bd3cc09c05d4f79d889826a1d4b010ead6276e8c1e71629b85d021d3  appendices/F-heights.tex
f5ba83b498e1c190aa6ad6d0fa78eacada6c2685f8cb5e46fb6e795e2e22e191  appendices/E-algebraic.tex
b14f683b56a2cb8dcc47f566b20106e521c7f3bf75d5bf6c4898f61a2b9c0cd5  sections/06-algebraic.tex
```

Line numbers below refer to these versions.

## 2. Verdict

**Mathematics: ready.** I found no false statement that a theorem depends on,
no gap in any proof of the three pairs, and no defect in the shared
realization and covariance lemmas they use. Every high-risk item listed by the
root survived reconstruction (Section 5). No invalidating defect was found, so
no urgent root message is needed.

**Submission readiness in this scope: not yet, for non-mathematical reasons
only.** Before the pairs are journal-ready:

1. integrate the 14 missing citation keys of Section 7/Appendix F and resolve
   the one in Appendix A (P1-1);
2. correct two attribution/contribution sentences in Section 3 (P2-1, P2-2);
3. confirm two imported-source details through the literature owner (P2-3,
   P2-4).

The P3 items are optional or cosmetic. Once items 1–3 are done, I consider
the three pairs ready.

## 3. Findings

Severity: **B** blocks a theorem; **P1** must be fixed before submission;
**P2** is an imprecise or insufficiently supported statement to correct before
submission; **P3** is minor, editorial, or optional. There are no B findings.

### P1-1. Citation keys absent from `references.bib`

`sections/07-heights.tex` cites 14 keys that are absent from both
`references.bib` and `evidence/literature.bib`: `BasuPollackRoy1996` (lines
315, 708), `BorweinWolkowicz1981`, `GaertnerMagronVallentin2026`,
`HeltonNie2010`, `Jiang2021`, `KolmogorovNaldiZapata2024`, `Laplagne2020`,
`Lasserre2009`, `ODonnell2017`, `PatakiTouzov2024`, `PeyrlParrilo2008`,
`RaghavendraWeitz2017`, `SafeyElDinZhi2010`, `Zhang2020`.
`appendices/F-heights.tex` adds `BasuPollackRoy1996` (line 811) and
`BorweinWolkowicz1981`. `appendices/A-upper.tex:141` cites
`JeronimoPerrucciTsigaridas2013`, also absent.

Repair: integrate vetted entries. `BasuPollackRoy1996` is load-bearing for
`thm:interior-gram`(a); the vetted report now confirms its contract (JACM
43(6), Theorem 4.1.2, pp. 1031–1032). The other heights keys are attribution
or comparison only. The JPT key supports only the optional
`rem:upper-explicit-separation` (A-upper.tex:134–146); if it is not vetted,
delete the remark (see P3-4). Sections 0 and 7 now both use `Lasserre2009`,
so the earlier `Lasserre2008` conflict is gone.

### P2-1. Section 3 overstates what it classifies

`sections/03-upper.tex:546–550`: “What this section adds is the
classification of explicit globally strongly convex objectives and strongly
monotone maps of polynomially bounded degree, for arbitrary polynomial
observables and including equality …”

Section 3 proves an upper bound. A classification needs the lower bounds of
Section 4, which exist only for strict and weak order tests, and are proved
for value and coordinate observables of certified quartics (and hence for the
gradients of those quartics as cubic maps). Equality has only the upper
bound, as the section itself says at lines 264–265. The sentence therefore
claims a classification of equality that the paper does not prove.

Repair (suggested wording): “What this section adds is a one-instance upper
bound for explicit globally strongly convex objectives and strongly monotone
maps of polynomially bounded degree, for arbitrary polynomial observables and
all six relations, including equality. With the lower bounds of
Section 4 it classifies the strict and weak value and coordinate comparisons
for certified quartics and certified cubic maps; equality keeps only the
upper bound.” This matches the vetted report's safe novelty statement
(“a specialized theorem, not a new general Newton-circuit architecture”).

### P2-2. Inconsistent attribution of Square Root Sum to Allender et al.

`sections/03-upper.tex:531–534` says Allender et al. “used it to reduce the
sum of square roots to PosSLP”. `sections/01-models.tex:408–410` says
“Square Root Sum lies in P^PosSLP”, citing the same paper, and the vetted
report describes that paper as establishing the real-computation/PosSLP
**Turing** bridge. A reader will take “reduce … to PosSLP” in Section 3 to
mean the many-one notion that Section 3 itself defines (line 65).

Repair: state the source's exact result, for example “showed that the sum of
square roots lies in P^PosSLP”. If a many-one statement is wanted, attribute
the step from P^PosSLP to one instance to `thm:posslp-closure`(b), not to
Allender et al. The literature owner should confirm the exact form (P2-2 in
Section 6).

### P2-3. The warm-start lemma uses one detail of GLS that is not yet in the vetted contract

`appendices/A-upper.tex:319–337` (case n ≥ 2 of `lem:upper-warm-start`) says
that, by GLS Theorem 3.2.1 and Remark 3.2.33, the method “stops either at a
center where the oracle asserts membership, that is, at an accepted point, or
with an ellipsoid of volume less than ε that contains K₁”. The vetted report
confirms the retained-core part: with Remark 3.2.33 the cuts need only be
valid on the fixed K₁ ⊆ K, and the final small ellipsoid contains K₁. It
does not record the first alternative in the form used. If the imported
theorem only promises an output point in S(K, ε), the proof still works with
an adjusted radius, but the text as written relies on the output being a
queried center at which the oracle asserted membership. This is how the
central-cut method operates; the contract should say so.

Repair: have the literature owner confirm that the membership alternative of
GLS Theorem 3.2.1 (with Remark 3.2.33) returns the queried center at which the
oracle asserted membership. Fallback that needs no confirmation: state the
lemma's conclusion as ‖x − p‖ ≤ ρ₀ + ε for an output x ∈ S(K, ε), and in the
application of `lem:newton-circuit`(b) halve the acceptance radius: accept when
‖T(x)‖ ≤ μρ/2 (so ρ₀ = ρ/2) and take δ₀ = μ³(ρ/2)²/(2Λ³). The rejection
estimate keeps its form, T(x)ᵀ(y − x) < −Λδ₀ on B̄(p, δ₀), and the volume
parameter ε = (δ₀/n)ⁿ is at most ρ/2, so ‖x − p‖ ≤ ρ. The internal
inequalities of the lemma as written (retained ball B̄(p, δ₀),
δ₀ = μ⁵/(32Λ⁵), cut value < −Λδ₀) are correct. The answer-length hypothesis added after Sol R1 is now
present (lines 298–302) and composes correctly with exact sparse evaluation of
T.

### P2-4. The cited bounded-circuit lemma is not in the vetted contract list

`sections/04-reductions.tex:154–157` now states the content of
`EY2010`, Lemma 5: a linear-size circuit over {+, ×, /} whose gate values all
lie in (0, 1), and an order comparison of its output. The vetted literature
report does not cover EY2010. The statement is comparison only; no proof uses
it.

Repair: the literature owner should confirm the lemma number and version
(the bib entry points to the SICOMP 2010 article), the gate set, whether
*all* gate values lie in (0, 1), the exact threshold predicate, sharing, and
that the reduction is deterministic many-one. If any item fails, weaken the
sentence to what the source states.

### P3-1. The min-sign proof uses a sign that the compiler theorem does not state

`sections/04-reductions.tex:467–469` derives `u_0 > 0` “by
(eq:reductions-compiler-output)”, but that display (lines 276–277) states only
`0 < (ξ_e − 1)²`, that is, `ξ_e ≠ 1`. The appendix proves the stronger fact
`0 < s_e = ξ_e − 1` (appendices/B-reductions.tex, auxiliary chain), and the
min-sign argument uses only `u_0²` and `u_0 ≠ 0`. No result is affected.

Repair: either add `ξ_e > 1` to the display of
`thm:reductions-root-circuit`, or write `u_0 ≠ 0` at line 469.

### P3-2. Attribution of the convex warm start

`sections/03-upper.tex:539–541`: the warm start “rests on the ellipsoid method
and, for explicit convex polynomials, on the bounds of SlotSteurerWiedmer2025”.
In this section the warm start for strongly convex objectives uses the
elementary bound ‖p‖ ≤ ‖∇f(0)‖/μ to fix a box, and then the GLS-based
`lem:convex-value` on that box (A-upper.tex:388–392). Hesse's bounds are not
used. Suggested wording: “uses polynomial-time convex value optimization over
an explicit box (Lemma `lem:convex-value`), which rests on the ellipsoid
method; for merely convex polynomials on unbounded domains the corresponding
radius and value bounds are due to Slot, Steurer and Wiedmer.”

### P3-3. Optional: the BPR import can be avoided

`thm:interior-gram`(a) (`appendices/F-heights.tex:799–823`) and the comparison
after `thm:heights-witness` (`sections/07-heights.tex:312–318`) import BPR 1996
Theorem 4.1.2. This contract is now verified, so no change is required. For
robustness, the same `poly(L)2^{O(n)}` bound also follows from results the
paper already proves. Apply `lem:separation`(b) to the formula ∇f(X) = 0,
z − f(X) = 0 (s = n, d = 4, τ = poly(L)). This gives |min f| ≥
2^{−2τ4^{c₀n}} when min f ≠ 0. Round the minimizer p (‖p‖ ≤ 2^{poly(L)}) to a
dyadic grid of mesh 2^{−2τ4^{c₀n} − poly(L)}. On a unit ball about p the
Lipschitz constant of φ = f − ‖∇f‖²/(2μ) is 2^{poly(L)}, so the rounded point
keeps φ > 0 (interior Gram) or f < 0 (witness), and it has poly(L)2^{O(n)}
bits.

### P3-4. Optional remark with an unvetted source

`rem:upper-explicit-separation` (`appendices/A-upper.tex:134–146`) is not
used by any proof. Keep it only if Luna vets JPT 2013 Theorem 1, including
its s ≥ 2 convention (here s = n + 1 ≥ 2) and the compact-component
hypothesis (here the singleton {(p, h(p))}). Otherwise delete it.

### P3-5. The letter N has two local meanings

Section 4 uses N for the number of variables of a realization
(`sections/04-reductions.tex:340`); Section 7 now uses N for the Gram order
binom(n+2, 2) (`sections/07-heights.tex:96`, after the D→N rename). Each
section defines its own N, so nothing is wrong, and the rename correctly
frees D for degree. A different letter for one of them would help a reader
who moves between the sections; this is optional.

### P3-6. Informal phrase

`sections/03-upper.tex:13–14`, “this precision problem is the whole
difficulty”, is informal. The next sentence states the precise claim; the
phrase can be dropped.

## 4. Sol R1 findings: are the repairs sufficient?

| Sol finding | Current text | My assessment |
|---|---|---|
| A-upper `n^{3/2}`, `√n` constants called rational | A-upper.tex:565–566 use `n²D³‖f‖₁R₂^D` and `nD‖h‖₁R₂^D` | Sufficient. The operator norm of the third-derivative tensor is at most `n^{3/2}` times the largest entry, so `n²` is a valid rational bound; `ζρ_φ ≤ 1/4` and all later inequalities only use upper bounds. |
| Rounded-cut lemma omitted answer length | A-upper.tex:298–302 | Sufficient (see P2-3 for a separate detail). |
| Horner update | A-upper.tex:152–154, “double and then add 1” | Sufficient. |
| Heights summary 39–44 and line 728 claim that circuits remove “all” obstructions | 07-heights.tex:39–50, 58–65, 742–744, 815–833 | Sufficient. Item (vi) now covers every certified quartic only for the witness and the interior Gram; the circle family is named separately; the text states that rational circuits cannot describe the irrational optimizers and certificates of (iii). I checked each new claim: the optimizer, `ee^T`, and `𝒯_p(A)` of the circle family are values of polynomial-size circuits built on the k complex squarings. |
| Table assigned PosSLP validation to all-yes families | 07-heights.tex:850–872 and 881–890 | Sufficient. Hardness is now stated over general certified quartics, with the explicit remark that both predicates are always true on g_k and h_k. |
| “Positive definite Gram” of √2·X₁² | 08-fields.tex:106–107 now says positive semidefinite; 07-heights.tex:208–210 now names the full-basis PSD Gram | Sufficient. Note that the source of the error was also in Section 7 (the earlier text said “the positive Gram (√2)”, which is PD only on the one-element basis); both places are now correct. The unique PSD Gram of √2·X₁² in the basis (1, X₁, X₁²) is diag(0, √2, 0). |
| Block sum in `prop:reductions-sums` has no PD Gram | 04-reductions.tex:717–726 | Sufficient. I checked all cases: m ≥ 2 nonempty blocks give a zero diagonal entry at x_j v_i (cross-block), so no PD full Gram; m = 1 with irrational root is the quartic of `thm:singleton-field`(v); m = 1 with rational root gives the Gram [[2+12α², −12α], [−12α, 12]] of determinant 24 > 0; the empty list gives diag(2, 12). |
| “Only a PD quadratic can dominate” indefinite squares | 04-reductions.tex:216–227 | Sufficient. The identity (x²−y²)² + (2xy)² = (x²+y²)² is correct, and the text now says the exposing square is a feature of the construction. |
| First parameter radicand bits | B-reductions.tex:315–318, Q = 12T + 7 | Sufficient; Q = (2T+5) + (T+1) + 9T + 1 = 12T + 7. |
| Quaternion constants of arbitrary length | B-reductions.tex:1001–1010 | Sufficient. |
| D reused for the Gram order | renamed to N in Section 7 and Appendix F | Sufficient; I found no leftover use of D for the Gram order and no clash inside Section 7 (see P3-5 for the cross-section note). |
| Circle approximation “dyadic” at j = 0 | F-heights.tex:448–451 | Sufficient. |
| Jiang parameter unit | 07-heights.tex, now “least common denominator … 5^{2^k}” | Sufficient; the sentence is now unit-neutral. Luna should still confirm the source's parameter (Section 6). |

## 5. Independent reconstruction of the high-risk items

Each item was checked line by line against the current text. Only the facts
that determine correctness are recorded here.

**5.1 Full positive definite Hessian Gram on the whole tensor space.**
`lem:quartic-realization`(c) (`appendices/E-algebraic.tex:368–434`) proves
positivity of the centred canonical Gram M on all of ℝ^{n+n²}, not only on
vectors (v, u⊗v). The blocks are: C = 2ℓℓᵀ + 2εΣb_jb_jᵀ ⪰ 2εν²I on ℝⁿ;
Ξ = Ξ(H) + εΣΞ(T_j) on all of ℝ^{n²}, where Ξ(H) ⪰ 4H⊗H ⪰ 4μ²I (the
Kronecker product has eigenvalues λ_aλ_b ≥ μ² on the whole space, including
non-symmetric tensors) and Ξ(T_j) ⪰ −4I because T_j⊗T_j has eigenvalues
≥ −‖T_j‖²; hence Ξ ⪰ (4μ² − 4εm)I ⪰ 2μ²I. The cross block satisfies
‖Δ(b,T)‖_F ≤ 6‖b‖‖T‖_F (triangle inequality on its two summands), so
‖Δ‖ ≤ 6√n ε(Λ + mβ). The Schur complement is ⪰ (3/2)εν²I under the third
bound on ε, and the completed-square estimate gives
M ⪰ min{(3/2)εν², 2μ²}/((1+θ)² + 1)·I. The downstream uses also hold on the
whole space: `thm:reductions-min-sign` uses M_G = λM + B with ‖B‖ ≤ ‖B‖_F =
(12κ² + 10)^{1/2} < 8; the witness and interior families use
λ_kA_k ∓ 2ι_kι_kᵀ ⪰ 3I − 2I.

**5.2 Canonical translation covariance.** I re-derived
Γ(g) = Ψ_cᵀΓ(g(·+c))Ψ_c as an identity of matrices, not only of biforms,
for one square, block by block. With A_c = c⊗I_n and b' = b + 2Tc:
the lower right block is Ξ(T) on both sides; the off-diagonal block is
Δ(b',T) − A_cᵀΞ(T) = Δ(b,T), because A_cᵀΞ(T) = Δ(2Tc,T) and Δ is linear in
its first argument; the upper left block reduces to 2bbᵀ + 4g₀T, using
h₀ − b'ᵀc + cᵀTc = g₀. The map g ↦ Γ(g) is quadratic and translation is
linear in the coefficients, so polarization extends the identity to every
weighted representation Σ S_kl g_k g_l. Hence the rational matrix computed
from the rational square factors is the congruent image of the centred PD
matrix, with Γ_f ⪰ λ_min(M)(1+‖p‖)^{−2}I/(εν²); no approximation of p and no
second rational projection is needed. The bound uses ‖p‖ only in the analysis.

**5.3 Signed-root and cube-root compiler error bounds.** The analytic gadget
bound |mul(x,y) − xy| ≤ 2²⁴|xy|(|x|+|y|) for |x|, |y| ≤ 1/400 follows from
Cauchy's estimate on the radius-1/100 polydisk, exact vanishing on both axes
(evenness of θ), and the tail Σ_{i,j≥1,(i,j)≠(1,1)} s^i t^j ≤ (16/9)st(s+t).
Signal arithmetic: addition error ≤ 34Θ²δ^{d+1}, multiplication error
≤ (3Θ² + 2²⁸Θ³)δ^{a+b+1}, both ≤ 2³⁰Θ³δ^{d+1}. All bounds are absolute; none
divides by a prescribed coefficient, so zero values, exact cancellation,
repeated wires (mul(s,s), φ(s−s) = 0), and arbitrary sharing are covered.
Sums only add signals of equal order because each sum cross-multiplies by the
denominator signals. log₂Θ_t = 16·3^t − 15, and 4·2^{2T+5} = 2^{2T+7}
≥ 16·3^T + 15 gives Θ_Tδ ≤ 2^{−30}. The output satisfies
|s_o − Wδ^d| ≤ 2^{−30}δ^d with W = 2V − 1 ≠ 0; the auxiliary signal gives
s_e² ≤ δ^{2^{T+2}} ≤ δ^dδ³ ≤ |s_o|/8. The box certificates are proved
separately by the direct interval test with w_i = 1000^iδ₀
(1 − 12w + 3w² ≥ 1 − 13w; (1 ± w_i)³ bounds). The nine raw gates of a mul
macro compute exactly 1 + mul(x,y) (radicand 1 + (3/8)Σ±(ζ_k − 1)).
The signed-root realization: normalization by σ_iκ preserves the interval
test; |det J| = Π d_iα_i^{d_i−1} ≥ 1 (tangent change of basis); T_α = ΔT₀Δ
with λ_min(T₀) = 2sin²(π/(2(n+1))) ≥ 2/(n+1)²; P_α restricted to the power
curve equals (t−α)(t^d−α^d); the coupled form with ρ = (h₀/(4A))² has
off-diagonal row sums ≤ h₀/4; the exact vanishing representation
E_i* = S_i − α_iT_i + Σχ_m(α_i)R_{i,m} keeps G(p) = 0 for every rational
replacement of α_i; ‖G − E*‖₁ ≤ kτB₀ then gives ‖H − H*‖ ≤ γ/2 and
‖∇G(p)‖ ≤ ε. Every hypothesis of `lem:quartic-realization` holds with the
stated constants.

**5.4 Exact minimum tilt.** For G = λF − u²v: G(p) = −u₀²v₀,
∇G(p) = −2u₀v₀e_a − u₀²e_b. If V > 0 then G* ≤ G(p) < 0. If V ≤ 0, with
t = −v₀ ∈ (0, 1/8] and u₀² ≤ t/2, strong convexity with modulus one gives
G* ≥ u₀²t − 2u₀²t² − u₀⁴/2 ≥ u₀²t/2 > 0. The Gram of the cubic's Hessian
biform is printed correctly (entries 2κ, 2κ, −1, −2 reproduce
−2v z_a² − 4u z_a z_b). Only u₀ ≠ 0 is needed (see P3-1).

**5.5 Rational quaternion signs and expanded size.** I checked ι, rot
(c i c̄ = j by direct expansion), pr(u) = (1 − 2u₁², 2u₀u₁, 2u₁u₃, −2u₁u₂),
the exact commutator identity [u,w] − 1 = 2(0, u⃗×w⃗)ūw̄, and the
near-identity bound 4|u⃗||w⃗|(|u⃗|+|w⃗|). The generator invariant
(g₀ > 0, 0 < g₁ ≤ 2^{−16}, |(g₂,g₃)| ≤ 64g₁²) is preserved, with
x² ≤ g₁' ≤ 6x², so 0 < g₁^{(j)} < 2^{−16·2^j}. Signal bounds 18Θ², 142Θ³,
396Θ⁴ fit Θ' = 2²⁰Θ⁴; log₂Θ_t = (41·4^t − 20)/3 < 14·4^t, and
Θ_Tδ < 2^{−50·4^T}. Homogenized coefficients (4C₁C₂, 4D₁D₂) and
(8(C₁D₂ ± C₂D₁), 8D₁D₂) keep C = DV with D > 0. Every gate value is an exact
rational unit quaternion, so p ∈ ℚ^N ∩ [−1,1]^N. The generator coordinate is a
coordinate of p, nonzero and below 2^{−64·4^T}, so its reduced denominator has
more than 64·4^T bits; with N = Θ(T) this is 2^{Ω(N)}, as stated. The
realization: the exposing identity E_i(p+U) = |U_i|² − |U_a − p_iŪ_b|² holds
with the factor order shown and for a = b (it rests on
⟨ab, c⟩ = ⟨a, c b̄⟩ and p_i p̄_b = p_a); weights 16^{1−i} give
H* ⪰ (11/15)ω_k I; the Euclidean rounding recurrence e_i ≤ h(3^i − 1) keeps
the rounded coefficients within η/2; only coefficients of exact residuals
are rounded, so the zero is exactly the gate list.

**5.6 Unary sparse Newton reduction, equality, monotone warm start, pivots,
separation.** Derivative bounds: exponent 5L'² + (13/2)L' ≤ 10L'². Local
Newton: q_{t+1} ≤ q_t², q₀ ≤ 1/8, so the error after e + 1 steps is at most
(2μ/Λ)2^{−6·2^e} and |h(x̂) − h(p)| ≤ 2^{−2^e−3} = g/8. Separation: the
proof of `lem:separation` (a nonzero eliminated polynomial must vanish at the
singleton; then the nonzero integer constant term gives
|α| ≥ 2^{−2τd^{c₀s}}) is complete; in the Newton application τ = 4L',
d, s ≤ L', and log₂(8L') + c₀L'log₂L' ≤ (c₀+3)L'². The six shifted
expressions have margins 3g/8 (order) and 15g²/64 (equality); I checked
both signs of every row. Pivots: if vᵀAv > 0 for all v ≠ 0, the homotopy to
the identity shows every leading minor is positive, so elimination without
exchanges divides only by positive pivots, also for non-symmetric J_T. The
monotone warm start: acceptance ‖T(x)‖ ≤ μρ gives ‖x − p‖ ≤ ρ; rejection
gives ‖x − p‖ > μρ/Λ and Tᵀ(x)(y − x) < Λδ₀ − 2Λδ₀ on B̄(p, δ₀). Existence
by Brouwer and the bound ‖p‖ ≤ 2^{3L} are correct. The certificate language
maps invalid certificates to the circuit 0 for all six relations, including
equality.

**5.7 Supplied slack gap.** Gap-to-distance with ε ≤ μδ²/(128σ²) gives
slack errors ≤ δ/8 and the exact active set by the threshold δ/2; both signs
of small tangent moves are feasible, so p_P is stationary on the active
affine space without strict complementarity. The chart bound ζ = 2^{2L+1}
(Hadamard plus Cramer, chosen before the active set is known) and Λ_φ =
ζ³Λ_f + ζΛ_h + μζ give ζρ_φ ≤ 1/4. The (x, λ) formula defines the singleton
h(p_P) with s = n + r ≤ 2L, and e₂(L) = (2c₀+3)L² suffices.

**5.8 Adaptive O(S²) compiler and universal interpreter.** |values| ≤
B = 2^{2^S}; for t ∈ [1, σ], 2σt − (σ + t²) = (t−1)(σ−t) + (σ−1)t ≥ 0 gives
F_σ(t) ∈ [1, √σ]; the schedule σ_{S+2}, …, σ₁ compresses |4ṽ − 2| ≤ 4B + 3
≤ σ_{S+2} into [1, 2]; then 1 − G(t) = (1−t)²/(1+t²) and 2S + 5 refinements
give error ≤ 2^{−2^{2S+4}}. With κ = 3B, log₂(εκ^S) ≤ −2^{2S+4} +
S(2^S + 2) < −2, so all approximations stay within 1/4, through
cancellation and reuse. All pair denominators (QQ', σQ² + P², Q² + P², 2Q)
are positive without sign tests; output 2P − Q. The interpreter selects
operands by address indicators, computes all opcode candidates, counts
unselected products in S, maps malformed strings to 0, and enumerates
addresses rather than answer transcripts, so its size is polynomial in the
clock. The statement correctly excludes Las Vegas, UP/NP, FPT, and
multi-bit outputs.

**5.9 Cube-root language upper bound.** β_i = Dξ_i are algebraic integers;
conjugates are bounded by Ξ = (2L+1)2^L since 2^L(1 + LΞ + LΞ²) ≤ Ξ³; the
norm gives |ξ_o − r| ≥ 2^{−L−(4L+1)(3^L−1)} ≥ 2^{−2^{6L}}. Newton for the
cube root: ε_{t+1} = ε_t²(3+2ε_t)/(3(1+ε_t)²) ≤ min{ε_t², 2ε_t/3}, and
14L + 6 steps reach 2^{L+1−2^{10L}}; propagation E_i ≤ 2^{(6L+3)i}ε_N stays
below both 2^{−7L−1} and g/8.

**5.10 Strict witnesses, optimizer denominators, local conditioning.**
Witness: every point of the closed sublevel set lies within (2 + √6)δ_k of p;
ξ₁ is irrational because K₀³ < K₀³ + 3 < (K₀+1)³; 1 ≤ |M²a³ − (M²+3)b³| <
16b³M^{2−2^k}; and the clean bound log₂b > k2^k holds for k ≥ 2. Circle chain:
(3+4i)² ≡ 3 + 4i (mod 5) gives reduced denominators exactly 5^m; the exposer
identity E_j(P+u) = ‖u_j‖² − 2κ_j(t_{j−1}ᵀu_{j−1})² holds (linear terms
cancel because κ_j = 2c_j²R_{j−1}²); weights 8^{−j} (ρ = 1) and k + 1 − j
(ρ = 1/2) give the stated margins; ‖J^{−1}‖ ≤ 2^{k+1} and k + 1 respectively.
At p̃ the Hessian is 2ℓℓᵀ/(εν²) + 2(k+1)²JᵀJ, between 2I and
(8(k+1)² + 1)I. The text keeps this local (Hessian at the optimizer only) and
separates the exact-denominator family f_k from the conditioned family f̃_k.

**5.11 Taylor kernels; Gram field versus square factors.** The Taylor
identity has coefficients 1/2, 1/3, 1/12, completed to
(1/2)(U+V/3)ᵀA(U+V/3) + (1/36)VᵀAV. For A ≻ 0 the kernel is ℝz(a): the rows
of C_U, C_V span the coefficient vectors of the quadratics vanishing at a,
which form z(a)^⊥. Gradient completion uses Ā = A − μ diag(I,0) ⪰
μ diag(0, I); Q_a ≻ 0 when c_a > 0 because d_id_j, d_i + b_i/μ, and 1 span
all quadratics. Part (d) is about Gram entries and part (e) about square
factors; the rational weights of a rational Hessian Gram are sums of rational
squares, so no square root of a weight enters. The √2·X₁² example is now
stated correctly (Section 4 table).

**5.12 Moments: strict feasibility, strict complementarity, exposing
fields.** Both programs attain f*; the optimal moment matrix has range in
ker Q* = ℝe, so it equals eeᵀ; Gaussian moments are strictly feasible for
(P) and (f* − 1, Q* + e₀e₀ᵀ) for (S); ranks 1 + (N − 1) = N give strict
complementarity. A rank-(N−1) Gram over E has an E-rational kernel vector
normalizable to e, so p ∈ Eⁿ. Rational optimal Grams have rank ≤ N − r
because their rows lie in the kernel of ξ ↦ ξᵀe on ℚ^N. Exposing matrices
are c·eeᵀ, and eeᵀ = 𝒜*(y^p) is a one-step facial-reduction certificate
(real singularity degree exactly one). The corollary's bounds follow from
row-wise denominator clearing and Cramer's rule (|det Q''| ≤
(N−1)!2^{(N+1)(N−1)B}) and from Z_{0,x_k}/Z_{0,0} = a_k. The counterexample
X₁² + X₂² + X₂⁴ and the nullvector example W(x) (blocks PSD together only at
x = √2; Y(2,0) ≻ 0 with eigenvalues 2, 4, 3, 2 − √2, 2, 2 + √2) are correct.

**5.13 Interior PD Gram bounds and circuit certificates.** W_n ⪰
I/(15(n+1)) (orthogonal basis 1, X_i, X_i² − 1/3, X_iX_j with mean squares
1, 1/3, 4/45, 1/9) bounds tr Q ≤ T_k; λ_min(Q) < h_k(p) = δ_k² <
M_k^{−2^{k+1}}; the squared upper-triangular denominators clear det Q, giving
the stated Ω(k2^k) bound. The circuit Gram is the completed Taylor Gram at the
exact rational Newton point, with constant c_x̂ = h(x̂) for the degree-six
observable h = f − ‖∇f‖²/(2μ); c_x̂ ≥ 7g/8 > 0 when min f > 0, and Q ≻ 0
forces min f > 0 because z contains 1. All divisions are by positive pivots,
μ, or fixed constants, on every certified input.

**5.14 Other results.** `prop:reductions-sums` (A1),
`prop:reductions-box-baseline` (A4: deficits δ_t ≥ 0 and weights
(2C+2)^{N−t} give Σ W_tε_t ≥ Σ W_sδ_s/(1+C)), `cor:reductions-feasibility`
(Hessian ⪰ (3/2)(8−κ)²I ⪰ 54I via the congruence of
`lem:models-gram-curvature`(b)), `cor:upper-two-minima`,
`prop:upper-circuit-witness`, `ex:upper-nongradient` (I recomputed the
biform and the leading minors 3, 47/16, 43/16, 65/16), and
`thm:quartic-complete` all check.

Interface checks: the `lem:convex-value` statement (02-points.tex:117–143) and
proof (exact feasibility repair, lower-dimensional polyhedra) match both
upper-bound warm starts; `thm:singleton-field`(v) supplies exactly what A1
uses; `thm:algebraic-cyclic`(a)(b) supplies what `rem:heights-cyclic-fields`
uses; `cor:constraints-binary` takes exactly the promises of
`thm:rational-optimizer`. The introduction's summary rows for these results
(00-introduction.tex:160–205, 360–410, 505–565) match the proved statements.
All `\ref` targets in the six files resolve, and no label is duplicated.

## 6. External contracts for the root to route to the literature owner

Only the literature owner should research these; I did no literature search.

1. **GLS Theorem 3.2.1 with Remark 3.2.33** (P2-3): confirm that the
   membership alternative returns the queried center at which the oracle
   asserted membership, under the retained-core oracle. The retained-core
   part and Lemma 3.2.8 are already in the vetted report.
2. **Allender et al. 2009** (P2-2): the exact form of the Square Root Sum
   result (membership in P^PosSLP via a Turing reduction, or a many-one
   reduction).
3. **EY2010 Lemma 5** (P2-4): lemma number and version, gate set, whether
   all gate values lie in (0, 1), threshold predicate, sharing, and the
   reduction type.
4. **Heights attributions** (P1-1): HeltonNie2010 Lemmas 7–8; Lasserre2009
   Theorems 2.6 and 3.3; Laplagne2020 Proposition 3.2 and Section 3.2;
   Jiang2021 Theorem 1.6 and Definition 2.6 (the unit of the denominator
   parameter); PatakiTouzov2024 pp. 2–3; Zhang2020 Example 2.5.3;
   KolmogorovNaldiZapata2024; BorweinWolkowicz1981; ODonnell2017 Theorem 1;
   RaghavendraWeitz2017 Theorem 2; PeyrlParrilo2008; SafeyElDinZhi2010
   Proposition 2.5; GaertnerMagronVallentin2026 Corollary 1.3 (the input is
   a supplied eigenvalue margin; the current sentence states only that the
   margin is part of the input, which is safe).
5. **JPT 2013 Theorem 1** (P3-4), only if the optional remark is kept.

Already confirmed in the vetted report and used correctly: Basu 2014
Theorem 2.27 (one-block QE with degree d^{O(s)} and coefficient bits
τd^{O(s)}, linear in τ); BPR 1996 Theorem 4.1.2 (rational points of
bit length τd^{O(n)} in strict open sets); ESY arXiv v2 Appendix C (the bib
entry points to v2); Dawson–Nielsen and König–Lohrey (comparison only); SSW
v1 Table 1.

## 7. Checks actually run

- Read the six reviewed files in full (two snapshots, plus diffs of every
  later change), and the interface passages listed in Section 1. Scratch
  copies for stable reading were placed in `/tmp`, outside the repository.
- One targeted inline Python document check over the six reviewed files:
  every `\ref`/`\eqref` target exists, no label is duplicated across
  `sections/` and `appendices/`, and the citation keys missing from
  `references.bib` are exactly those listed in P1-1.
- `sha256sum` of the reviewed and interface files (Section 1), and `grep`
  of `references.bib` and `evidence/literature.bib` for the keys in P1-1.
  The six reviewed files still had the Section 1 hashes at 16:08 EDT.
- Whitespace check of this report: an inline Python check (no trailing
  whitespace, final newline present) and
  `git diff --no-index --check /dev/null evidence/reviews/opus-numerical-r1.md`,
  which printed no diagnostics (exit status 1 only because the file differs
  from `/dev/null`).

No computational experiment, mathematical script, symbolic computation,
compilation, project-wide verification, or CI inspection was run, and no
literature search was performed. All mathematical checks were analytic, by
hand.
