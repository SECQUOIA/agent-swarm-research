# M-limits — mathematics of Section 10 and Appendix G

Date: 2026-10-03.
Scope: `sections/limits.tex`, `sections/appendix-lbproduct.tex` and
`sections/appendix-moments.tex`, plus the summaries of these results in the
abstract, introduction, conclusion and Remark `rem:fpt`. Line numbers refer to
the current sources. The PDF numbering is from `/tmp/dpaper/out/main.aux`:
Section 10 is on pp. 62–71 and Appendix G on pp. 119–123.

## Verdict

Every reduction and lower bound in scope is correct as stated. I re-derived
each proof and tested every construction on small instances in exact
arithmetic. The tests found no counterexample.

The issues raised in rounds w2/w3 are fixed:
- `lim:prop:setgrowth` is restricted to runs of filtering with thresholds
  U_j ≥ OPT, and part (c) covers general path certificates.
- The t_c argument is used in `lim:prop:oracle`.
- The results are attributed to rETH, and rETH is defined.
- The proof includes the reduction from Clique to multicolored clique and
  uses the effective form of o(p).
- Occupied widths are defined for each feasible point.
- The decoding step in `prop:lbwidth` is now proved.
- The L = 0 instance Ψ_0 is given.

What remains is minor:
1. The summary "the exponent of κ cannot be o(p)" omits the qualifier that
   the polynomial in I has fixed degree. The qualifier is needed, because κ
   and I are polynomially related on the hard instances.
2. The comparison after Proposition `prop:oraclebarrier`, and in the
   introduction, does not separate the barrier from CT, whose number of
   queries also grows (logarithmically) with the accuracy.
3. SETH is used without being defined or cited.
4. Remark `lim:rem:dk` says "exponential in the input length". The input
   length is Θ(k log k), so "exponential in the number of variables" is the
   accurate wording.
5. The Bienstock–Muñoz credit lacks its locator. I checked it: Appendix A,
   formulation (26).

## Checks run (targeted, exact arithmetic)

All scripts are in `process/w4/checks/`. Each finished in under 2 s, one
process at a time.

| Command | What it checks | Result |
|---|---|---|
| `python3 mlimits_unique_lbwidth.py` | `lim:prop:unique`: 60 random Subset Sum instances, m = 2..5, 38 yes and 22 no. Distinct vertex values; gap ≥ λ to the second vertex; decision thresholds 1/(2m) and 1/m; σ(x) ∈ [−A,2A]; the split identity (`lim:eq:split`) at 300 rational points per instance; growth with g = λ/(m(1+2(m−1)‖a‖²)), including points with y = σ(x) and points near x\*; the bound 4/g ≤ 2^{m+3}m²(1+2m‖a‖²); symbolic second derivatives (4 for y, 2a_i²−2‖a‖² for x). `prop:lbwidth`: all 75 graphs with n ≤ 4 and 10 random graphs with n = 6. Binary values distinct; ⌊Ψ\*/2^n⌋ = −α, also for every value within 1/2; growth 1/(2n) for Ψ and 1/n for Ψ_0 at random points. `lim:prop:constraints`: 80 random instances, m ≤ 7. Unique minimizer; x₀\* = 0 iff yes; growth 1/(2m+3) over all feasible points; 2m+3 coordinates. `lim:prop:oracle`: 2r ≤ 1 and \|𝒞\| ≥ (κ/(8p))^{p/2} for p ≤ 4. | PASS |
| `python3 mlimits_lbproduct.py` | `prop:lbproduct`: 25 random multicolored-clique instances, k = 2 and 3, N₀ = 2. Each pair subproblem is brute-forced (823,536 assignments in total). Φ_cd = 0 iff (x_c,x_d) ∈ E_cd; the encoding of an edge is unique; the value at an encoding is its weight; Φ ≥ 1 gives value ≥ W₀; OPT ≤ W₀−1 when a clique exists and OPT ≥ W₀ otherwise; the minimizer is unique iff the minimum-weight clique is unique. Symbolic Hessian diagonal for k = 4, N₀ = 3: max 7790 ≤ W₀(2+4N₀²+2k) = 9430, and n ≤ k+2k²N₀². Isolation lemma by exact enumeration on a small family (probability 0.77 ≥ 1/2). The ψ′ construction. | PASS |
| `python3 mlimits_messages_setgrowth.py` | `lim:prop:messages`, m = 2..7: Ψ_m ≥ (1/8)(‖ξ‖²+‖z‖²) at random points and at points near the chain; binary digits give zeros of V₀ at every integer of [0,2^m−1]; diagonal entries (10, 4, 7/4) and minimum eigenvalue ≥ −1/4 (m = 4). `lim:prop:setgrowth`: 150 random rational grids, n = 2..4, with valid L_i ≥ 2. Every min-marginal satisfies m_j(v) ≤ −(L_j/8)w_j(v)²; β ≤ −(L_j/8)W_j²; no interval is removed at U = 0; set growth 2/(n(n−1)) at random points. The n = 2, ε = 1/50 certificate: all stage-0 min-marginals are −1/50, stage-1 β is −1/50, the gap is ε, the bound requires 5 nodes, and removed intervals have length ≤ 2√ε. `prop:oraclebarrier`: symbolic gradient and Hessian of f_{c,w}, the cubic identity, and the counting step (M^n > Q+1 and M < 1/(2√(6ε))). | PASS |
| `python3 mlimits_moments.py` | `lim:prop:moments`, r = 1..4: F = Ψ at ζ⁰; Ψ−1/4 = 2Υ+λ(ū+v̄); split identity `lim:eq:momsplit` with random δ; ζ⁰ ∈ [−2r,2r]; growth g_r at random feasible points; vertex values (a−b)(a−b−1)/2; parity laws sum to 1; moments equal through order 2r−1 and different at order 2r; value 1/4−(2r+1)/(16r); atoms in [0,rh]. Remark `lim:rem:moments`: identity, Hessian decomposition, L = 32/h², growth 1/22, moments (1/2, 5/16, 7/32 against 11/64 and 41/256), value 3/32, completion matching both bags, McCormick for s ∈ [0,2h] and s ∈ [0,h], covariance PSD, triangle pseudo-expectation −1/8. | PASS |

Negative control: a copy of `mlimits_moments.py` with a perturbed moment and
an inflated growth constant fails as expected.

I compared Remark `lim:rem:dk` with Del Pia–Khajavirad (2026), Theorem 3
and eqs. (18)–(24), in `literature/papers/pia2026-treewidth-and-the-complexity-of/original.pdf`,
pp. 20–25. I read the extracted text of Remark 2 on p. 25. I also checked
Bienstock–Muñoz (2018), Appendix A, formulation (26), in
`literature/papers/bienstock2018-lp-formulations-for-polynomial-optimization/fulltext.md`.

I did not run any project-wide verification and did not consult CI.

## What was checked and found correct

**Prop. `lim:prop:unique` (10.1).**
- Bags and path decomposition, with p ≤ 3; polynomial data.
- e, σ_k, σ_m = a₀, and the residual identity y_i − y_{i−1} − a_ix_i = −e/m + Δδ_i.
- The split (`lim:eq:split`), using ΣΔδ = 0.
- σ(x) ∈ [−A,2A]^{m−1}, so δ = 0 is feasible.
- The path inequality, Σ_k k = m(m−1)/2.
- Concavity of Φ: its Hessian is (2/m)aaᵀ − 2‖a‖²I ⪯ 0.
- Distinct vertex values: the left side lies in m⁻¹ℤ, and the right side is below λ2^m = 1/(2m) in absolute value.
- The gap λ.
- Jensen for the product law, and Pr(Y ≠ x\*) ≥ max_i|h_i| ≥ ‖h‖²/m.
- ‖σ(x)−σ(x\*)‖² ≤ (m−1)‖a‖²‖h‖², using |c_kj| ≤ 1.
- The growth constant g, using g ≤ λ/m < 1/(m(m−1)).
- L = 4 and κ ≤ 2^{m+3}m²(1+2m‖a‖²).
- The decision thresholds 1/(2m) and 1/m, and a^Tx\* = a₀ on yes-instances.

**Cor. `lim:cor:nopolylog` (10.2) and the paragraph after it.**
- q = ⌈log₂ 4m⌉ separates the two cases.
- f_1 ≤ f·poly(1+log₂κ) follows from the proof of `thm:exact`.
- Padding with t_j² leaves p unchanged. It also leaves κ unchanged, because g ≤ 1 and L = 4 ≥ 2.
- NP-hardness at κ ≤ 2^{I^δ}.

**Remark `lim:rem:dk` (G.1).** Checked against the DK source.
- ℓ = ⌈log₂(U+1)⌉ = ⌈log₂ 2c⌉, D = 2^ℓ, N = 2nℓ+n+ℓ = 5ℓ+2.
- (1,0) is the unique solution.
- At (0,1) only (24) is nonzero, with value D⁻², and ‖y′−v\*‖² ≥ 2ℓ.
- The largest Hessian diagonal is 10: 8+2 for z_ik and w_k. This matches their ‖Q‖_max ≤ 5.
- κ ≥ 20ℓD² ≥ 80ℓc².
- The fractional point (1/c,1) is feasible with all residuals zero, and Ψ = ϱ/c.
- dᵀ∇²Ψd = −2(ϱ²+1), so ν/g ≥ 2c(ϱ+1/ϱ) ≥ 4c.
- The claim about weights holds.
- The refinement of DK Remark 2 described in §10.1 is accurate. DK use a unit-weight penalty x_i(1−x_i) with scaled partial sums. The paper uses the penalty ‖a‖² and a lexicographic tie-break.

**Prop. `lim:prop:oracle` (10.3) and Remark `lim:rem:oracle`.**
- Coordinate curvature: the minimum of an affine and a concave function is concave.
- Growth (needs κ ≥ 2), r² = 2p/κ, 2r ≤ 1, \|𝒞\| ≥ (κ/(8p))^{p/2}, and disjoint balls.
- t_c argument: at most one c has t_c = ∞, the finite t_c are distinct, and the run on F_c agrees with the constant run up to and including evaluation t_c.
- The randomized bound (Q+1)/\|𝒞\|.
- Query points outside X do not affect the argument.
- Remark: K = 10θ⁻¹⌈log₂(p+2)⌉ with 2^μ ≤ 6√κ̄ and κ̄ = κ for equal L_i. The gap is (C√p log(p+2))^p times the number of stages. The bound is exponential in p for κ ≥ 32p.

**Prop. `prop:lbwidth` (10.5) and the following paragraphs.**
- Binary injectivity, and min Φ = −α (deletion step 1−2d(u) ≤ −1).
- Multilinear extension, and Pr[Y = x\*] ≤ 1 − max δ_i.
- x_i(1−x_i) ≤ δ_i, g = 1/(2n), L = 1/n, κ = κ̄ = 2.
- The binary case gives g ≥ 1/n.
- Decoding ⌊Ψ̃/2^n⌋ = −α, using χ(x\*) ∈ [1, 2^n−1].
- I = n^{O(1)} and p = n give the ETH consequence.
- Ψ_0 has L = 0 and g = 1/n, so κ = 1, and CT with P = ∅ runs in 2^p·poly(I). The SETH consequence uses Lokshtanov–Marx–Saurabh with p = tw+1. See finding 3 on the missing definition.

**Prop. `prop:lbproduct` (10.6) and App. G.2.**
- Isolation lemma: α_e does not depend on w(e), the event w(e) = α_e has probability 1/ρ, and the union bound applies.
- The decomposition is valid, with p = max{k,7}.
- Encoding:
  - Φ is a nonnegative integer.
  - Φ = 0 forces exactly one ζ_{l\*} = 1 per pair, with (x_c,x_d) = (a_{l\*},b_{l\*}).
  - Each clique has exactly one encoding.
  - The tie-break is at most W₀−1, and Φ ≥ 1 gives a value ≥ W₀.
  - The minimizer is unique iff the minimum-weight clique is unique.
- Conditioning: g = 1/(nN₀²); the Hessian diagonal is at most W₀(2+4N₀²+2k) (ζ: 2+2a²+2b²; σ, y, y′: 4; x_c: 2(k−1)); n ≤ k+2k²N₀²; κ and I are poly(kN₀).
- The clocked reduction has no false positives. With isolation probability ≥ 1/2, it finds the clique on yes-instances.
- Clique reduces to multicolored clique. The ETH proof for Clique is a chain of deterministic Karp reductions after sparsification. With a one-sided-error oracle, the composition has one-sided error ≤ 1/4 after two runs, which contradicts rETH.
- Restricting to k ≥ k₀ is harmless: set s′ = 1 below k₀.
- The ψ′ = max{1, min{ψ, p/C}} step and f(p,κ) ≤ 4c₀(c₁p)^pκ^{p/2+2}. This uses (1+log₂κ)² ≤ 4κ.

**Prop. `lim:prop:messages` (10.7).**
- The bags.
- I = O(m²).
- The induction bound on ξ_t, ‖(2^{t−m})‖² ≤ 4/3, and the shift series has operator norm ≤ 1.
- ‖ξ‖²+‖z‖² ≤ 8Ψ_m.
- Diagonal entries 10, 4, 7/4, so κ ≤ 80, and ∇²Ψ_m ⪰ −I/4.
- V₀ vanishes exactly at the 2^m integers.
- Both representation bounds give N_pc ≥ 2^{m−1}.
- CT is polynomial by Theorem `thm:approx`.
- DK's claim of linearly many pieces on forests is confirmed in their abstract and Proposition 1.

**Prop. `lim:prop:setgrowth` (10.8), the revised version.**
- The set-growth constant 2/(n(n−1)) holds (Cauchy–Schwarz), with the n = 2 identity, L_i ≥ 2 and κ_S ≤ 2n(n−1).
- (a) The outward construction works for every valid L_i ≥ 2, on every grid of X.
- (b) Every interval contains t𝟏, so it is retained when U ≥ OPT. Every stage keeps box X, so W_j ≤ 2√ε and \|G_j\| ≥ 1+1/(2√ε). This covers TRIAL and CT, whose thresholds are incumbent values.
- (c) is correct with (C1), and also in the case k = 0.
- The example certificate with n = 2 and ε = 1/50 is valid. The open question and the comparison with Theorem `thm:cells` are stated correctly.

**Prop. `prop:oraclebarrier` (10.9).**
- The derivatives, the C² property, and ∂_ii f ≤ (1−ρ)² ≤ 1.
- The identity 1−(1−ρ)³−ρ = ρ(1−ρ)(2−ρ), giving g_S = w²/(6n).
- The zero function has κ_S = 1.
- Counting: M = ⌊(Q+1)^{1/n}⌋+1 gives M^n > Q+1 and M < 1/(2√(6ε)), so an empty subcube exists, and w ∈ (√(6ε), 1/(2M)) can be chosen rational.
- Both output types are refuted.

**Prop. `lim:prop:constraints` (10.10) and the TU paragraph.**
- The summed recurrence gives Σa_ix_i = a₀. The x₀ item is feasible and the only feasible choice with x₀ = 1. Values are distinct, and the dummy value is 2^{m+1} > 2^m−1. g = 1/(2m+3), κ = 1, and the 1/2 separation holds.
- After scaling, the matrix in Y consists of difference rows plus unit rows, which is TU. η = 1, s = a₀ and K_Z = 2, so Definition `def:tu-model` holds. Only s/η is not polynomially bounded, which matches the discussion after Theorem `thm:tu-approx`.
- Attribution: Bienstock–Muñoz, Appendix A, (26), is a running-sum encoding of Subset Sum/Partition with treewidth 2. DK cite the Cifuentes–Parrilo example ("Example 1 in [6]") for the same path system.

**Section 10.7, Lemma `lim:lem:mixture`, Definition `lim:def:moments`, Prop. `lim:prop:moments`, Remark `lim:rem:moments`.**
- Lemma: Σ_ii ≤ (u′−x̄)(x̄−ℓ′) ≤ (u′−ℓ′)²/4, and ⟨H,Σ⟩ ≥ −ν tr Σ.
- Point masses are feasible.
- Construction:
  - The relabelling c = (u, −½, −v_{r−1}, …, −v₁) and c̄ = ū−v̄−½.
  - The split identity, ζ⁰ ∈ [−2r,2r] and h ≤ 1/(4r).
  - Υ is multilinear with vertex values ≥ 0, and OPT = 1/4 at a unique minimizer.
  - The path inequality with 2r in place of m, node displacement ≤ 2‖(u,v)‖₁, the constant g_r, and ∇²F ⪰ −2I.
- Witness:
  - The parity laws and the finite-difference argument for moments.
  - Cell conditions at every separator.
  - The value (2r−1)/(16r), the occupied widths, and the consequence via 2r−1 ≥ k.
  - The r = 1 case also works: the right law is the point mass at s = h/2.
- Remark: verified in full (see the table above). F_h equals F_{2,h/2} with y₁ and z₁ eliminated.

**Section opening and bullets.** All cross-references resolve: Prop. 9.1, Prop. 7.5, Appendix G.3. The claims match the propositions, except for the qualifier discussed in finding 1.

## Findings

### Minor

**M-limits-1. The rETH summary omits the fixed-degree qualifier.**
Locations:
- `limits.tex` 21–22 (bullet) and 362 (proposition title);
- `abstract.tex` 22–23;
- `intro.tex` 196–197;
- `conclusion.tex` 16–18;
- `growth.tex` 282–284.

*Issue.* Read literally, "the exponent of κ cannot be o(p)" claims more than Proposition `prop:lbproduct` proves. The proposition excludes running times f(p)(κI)^{p/ψ(p)}. In particular, it excludes f(p)κ^{a(p)}I^C with C constant and a(p) ≤ p/ψ(p).

*Why.* On the hard instances, κ and I are both poly(kN₀) (App. G.2, "Conditioning"). The reduction therefore cannot separate the exponent of κ from the degree in I. An algorithm with running time κ³I^p has κ-exponent 3 = o(p), but it is not of the excluded form. It contradicts neither this proposition nor ETH: it gives N₀^{O(k)} on the clique instances and 2^{O(I)} on the instances of Prop. 10.1. Theorem 1.2(c) and the sentence after Proposition 10.6 ("in the sense a(p) ≤ p/ψ(p) above") are precise. The shorthand summaries are not.

*Fix.* At `limits.tex` 21–22, write: "under randomized ETH the exponent of κ in a bound f(p)κ^{a(p)}I^{O(1)} cannot be o(p), already for integer box quadratics (Proposition 10.6)." Use the same qualifier, "in a bound f(p)κ^{a(p)}poly(I)", in the abstract, the introduction (196–197), the conclusion (16–18) and Remark `rem:fpt` (282–284). The proposition title can stay if the qualifier appears in the statement, which it does.

**M-limits-2. The barrier comparison does not separate the barrier from CT.**
Locations: `limits.tex` 609–613; `intro.tex` 205–208.

*Issue.* The text says no algorithm "can do the same" as CT under unknown set growth. The introduction says such an algorithm "needs a number of queries that grows with the accuracy". Under point growth, CT's number of evaluations also grows with the accuracy: it makes about 2(J+1)K^p evaluations with J = O(I+q) stages. So the introduction's statement does not mark the difference. The difference is the rate: logarithmic in 1/ε for CT, against at least (1/(2√(6ε))−1)^n − 1 = Ω(ε^{−n/2}) for every algorithm here.

*Fix.* At `limits.tex` 609–613, write: "Under point growth, CT uses a number of nodes per coordinate that does not depend on the accuracy, and hence f(p,κ)·O(I+q) evaluations. Proposition `prop:oraclebarrier` shows that under growth towards an unknown set, every algorithm in this information model, even with exact derivatives, needs Ω(ε^{−n/2}) queries, already for n = p = 1 on an instance with κ_S = 1." At `intro.tex` 207–208, replace "needs a number of queries that grows with the accuracy" with "needs a number of queries polynomial in 1/ε (at least of order ε^{−n/2})".

**M-limits-3. SETH is used but not defined or cited.**
Locations: `limits.tex` 346–349 and 355–357.

*Issue.* ETH and rETH are defined, with citations, at lines 282–286. The strong exponential-time hypothesis is then invoked twice without a definition or a source; only the consequence from Lokshtanov–Marx–Saurabh is cited.

*Fix.* At line 346, write: "Under the strong exponential-time hypothesis (SETH: for every ε > 0 there is k such that k-SAT on n′ variables cannot be decided in time (2−ε)^{n′}) \cite{LokshtanovMarxSaurabh2018}, the same reduction, …". Alternatively, add the primary source: Impagliazzo and Paturi, "On the complexity of k-SAT", J. Comput. Syst. Sci. 62(2):367–375, 2001.

**M-limits-4. Remark `lim:rem:dk`: "exponential in the input length" is imprecise.**
Locations: `appendix-lbproduct.tex` 31–33; `limits.tex` 202–204.

*Issue.* For c = 2^k the instance has N = 5k+7 variables and O(k) monomials with bounded coefficients. Under the paper's encoding (§3, "Encoding": binary lengths, including variable indices and the decomposition), the input length is I = Θ(k log k). Then κ ≥ 80(k+1)4^k = 2^{Θ(k)} = 2^{Θ(I/log I)}, and ν/g ≥ 4c = 2^{k+2}. This is superpolynomial, but it is not 2^{Ω(I)}. The paper otherwise uses exact forms such as 2^{O(I)} and 2^{I^δ}.

*Fix.* At `appendix-lbproduct.tex` 31–33, write: "For c = 2^k there are N = 5k+7 variables and coefficients bounded by five, so κ ≥ 80(k+1)4^k is exponential in the number of variables (and 2^{Ω(I/log I)} in the input length), consistent with Corollary 10.2." At `limits.tex` 204, replace "exponential in the input length" with "exponential in the number of variables".

**M-limits-5. The Bienstock–Muñoz credit lacks a locator.**
Locations: `limits.tex` 623–624; `intro.tex` 210–212.

*Issue.* The running-sum encoding is credited to Bienstock–Muñoz (2018) without a locator. That paper is about LP formulations, and the encoding appears only in its Appendix A, formulation (26). There it is a Partition-type running-sum system of treewidth 2, used to show that tolerances cannot be improved. CONVENTIONS §5 asked for "App. A". The w3 report dropped the locator as unverified; I have now verified it in the source.

*Fix.* Write `\cite[Appendix~A]{BienstockMunoz2018}` in both places.

## Not reported (checked, deliberate, or out of scope)

- The proposition title "The exponent of κ cannot be o(p)" is acceptable once the statement carries the qualifier (it does).
- The order of Section 10, with the oracle subsection 10.2 between conditioning and width, matches the bullets.
- The remark title duplicates the heading of subsection G.1. This is cosmetic.
- Notation reuse inside Appendix G.3 (controls u_i, state s) is local and causes no ambiguity in the proofs.
- `computation.tex` 326–331 applies the n = 2 instance of `lim:prop:setgrowth` to instances that merely contain a(x₀−x₁)². Whether those instances inherit the bound is outside this scope (computation owner).
