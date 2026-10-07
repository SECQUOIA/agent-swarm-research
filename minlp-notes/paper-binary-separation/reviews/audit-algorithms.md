# Algorithmic boundaries and gap-zero audit

The mathematical claims audited here are sound after the qualifications
below. No fatal flaw was found in the integer precursor, the polynomial
certificate arguments, or the gap-zero construction. The paper sections
[`05-algorithms.tex`](../sections/05-algorithms.tex) and
[`06-gap-zero.tex`](../sections/06-gap-zero.tex) contain the corrected
journal proofs. This report records the independent reasoning and the
scope decisions.

The inputs were the complete integer split note,
`research-20261001/binary-separation/note.md` §§4 and 6 and Lemma 3, and
`research-20261001/split-practice/note.md` §4. I also read the root
`AGENTS.md`, the paper notation and the newly supplied core theorem to
align the section interfaces. No literature search, computational
experiment, checker rerun, CI inspection or project-wide verification
was performed. Verification consisted of reading the specified proofs
and deriving the arguments below. Bibliographic verification of the
exact CVP theorem was supplied by the separate literature lane.

## Findings that needed repair or qualification

1. **Fixed-rank search needs a precise CVP algorithm.** The quotient
   reduction is correct. The notes' blanket alternative saying that LLL
   followed by Fincke–Pohst enumeration gives a parameter-only time
   factor does not supply a sufficient proof. Enumerating every point in
   the original threshold ball can take exponentially many steps in the
   bit length even at fixed rank. The paper cites the verified exact
   fixed-dimensional CVP result and proves a rational-input bridge; it
   makes no blanket enumeration-time claim.
2. **Fixed support and gonality are polynomial for fixed parameters.**
   Enumeration over supports has an exponent depending on the support
   parameter. This is XP, not a proved FPT result in support or gonality.
   The fixed-support hypermetric argument can use the induced
   fixed-dimensional problem instead of a bound on facet coefficients.
3. **The normalized-threshold theorem is exact only in its stated
   positive-semidefinite, rational-input domain.** Its parameterized
   bound is XP in the inverse threshold. Polynomial separation of an
   arbitrary raw split at a non-PSD point does not solve its normalized
   threshold problem.
4. **Rank-one boundary examples belong to general integer moments.**
   Rank-one Boolean moments satisfy `x_i² = x_i` and are integral. The
   fractional rank-one raw maximum and the rank-one 0/1-restricted
   hardness example cannot be described as phenomena inside the binary
   relaxation.
5. **Primitive domination needs a nonnegative root entry.** In Lemma B
   of the practice note, the algebraic identity holds for every
   symmetric `Y`, but the domination conclusions need `Y_00 ≥ 0`.
   They apply at all normalized moments `Y_00 = 1` used here. As an
   unrestricted statement they fail: take the all-minus-one `2×2`
   matrix, `w' = 1`, `k = 3`, `s = 1`. The nonprimitive split
   `v = (−2,3)` has value `−2`, while the two adjacent primitive splits
   `(−1,1)` and `(−2,1)` both have value zero. This assumption should
   be explicit wherever that lemma is reproduced.
6. **Gap-zero is ordinary NP-complete with a PARTITION reduction.** No
   pseudo-polynomial algorithm is supplied, and no strong-hardness result
   is proved. Calling the problem “weakly NP-complete” would assert more
   than the proof establishes. Its metric-polytope promise is correct
   and has simple exact bounds.
7. **General-gap exclusions require care.** A non-PSD point has a
   polynomial-size violating coefficient vector for the general gap
   family. Computing that vector's exact gap is a separate task. The
   generic construction does not compute a tight right-hand side; that
   fact does not prove that every possible search algorithm must be
   difficult. At PSD points, the present reductions do not exclude
   gap violators with gap at least three in no-instances.

## Exact rational negative directions and the lattice quotient

For a rational symmetric matrix `A`, symmetric elimination provides
either a PSD certificate or a polynomial-size rational negative
direction. At a current Schur complement `C`, a negative diagonal gives
`e_i`. If `C_ii = 0` and `C_ij ≠ 0`, take `z_j = 1` and
`z_i = −(C_jj + 1)/(2 C_ij)`; its quadratic value is `−1`. Otherwise
pivot on a positive diagonal. A direction `z_R` in the next Schur
complement lifts by `z_i = −C_iR z_R/C_ii`. If the remaining Schur
complement is zero, the matrix is PSD.

The positive pivot indices `K` form a positive definite principal
submatrix. Schur-complement entries are ratios of minors, so they have
polynomial encoding length after denominators are cleared and the
determinant bound is applied. The final negative direction has at most
two nonzero uneliminated coordinates. Its eliminated coordinates can be
computed at once as `−A_KK⁻¹ A_KR z_R`; Cramer's rule bounds their
encoding lengths. Multiplying by a common denominator gives a
polynomial-size integral negative direction. This avoids the false
claim that an eigenvector of a rational matrix is necessarily rational
or has a rational polynomial-size encoding.

When `A` is PSD of positive rank `r`, the zero Schur complement gives

`A = Pᵀ G P`, where `P = A_K,·` and `G = A_KK⁻¹ ≻ 0`.

These are rational matrices of polynomial encoding length. For a common
denominator `D`, the integer matrix `DP` has full row rank. Its column
Hermite normal form gives a basis `H` of `(DP) Z^m`. Thus
`Λ = P Z^m = (H/D) Z^r` is a discrete rank-`r` lattice. Solving
`(DP) t_j = H_·j` supplies polynomial-size integral preimages of its
basis columns. With those preimages in `T`, a basis is `W = PT = H/D`.
For any rational `y ∈ Λ` of polynomial encoding length, the feasible
system `(DP)z = Dy` has a polynomial-size integral solution obtained by
Hermite normal form. This is the precise lifting statement needed for
both NP membership and the fixed-rank search algorithm.

The lattice statement does not require a rational real-space Gram
factor. Rationality of the metric and quotient data is sufficient.

## Complete short-witness arguments

For hypermetrics write `δ = diag M` and
`g_M(z) = zᵀMz − δᵀz`.

* If `M` is not PSD, take an integral negative direction and choose its
  sign so that `δᵀz ≥ 0`. Then `g_M(z) < 0` immediately; no large
  multiplier is needed.
* If `M` is PSD and `δ` is outside its range, orthogonality of range and
  kernel gives a rational kernel-basis vector `k` with `δᵀk ≠ 0`.
  Clear denominators and choose its sign so that `δᵀk > 0`. Then
  `g_M(k) = −δᵀk < 0`.
* If `M` is PSD and `δ` belongs to its range, use the quotient above.
  Put `D_0 = M_KK`, `P = M_K,·`, `G = D_0⁻¹` and `t = δ_K/2`.
  The range condition gives `δ = PᵀGδ_K`, hence

  `g_M(z) = ||Pz − t||_G² − ||t||_G²`.

  A violator gives `y = Pz` with `||y||_G < 2||t||_G` and
  `|y_i| < 2 sqrt((D_0)_ii) ||t||_G`. The square of each bound is
  rational of polynomial encoding length. Each coordinate of `y` has
  denominator dividing the common denominator of `P`. Its numerator
  and denominator therefore have polynomial encoding lengths. Hermite
  normal form lifts this same `y` to an integer `z'` of polynomial
  encoding length, preserving `g_M`. The associated hypermetric vector
  `(1 − sum z', z')` also has polynomial encoding length.

If `M = 0`, then `δ = 0` and there is no violation. The three nontrivial
cases exhaust arbitrary rational symmetric input and prove NP
membership without any positive-definiteness promise.

For general integer splits, with `Y_00 = 1`,

`q_Y(v) = vᵀYv + vᵀYe_0 = ((e_0 + 2v)ᵀY(e_0 + 2v) − 1)/4`.

At a non-PSD point choose an integral negative direction `v` with
`vᵀYe_0 ≤ 0`; then `q_Y(v) < 0`. At a PSD point use its quotient and
a hypothetical violated `u = e_0 + 2v`. The vector `y = Pu` satisfies
`yᵀGy < 1`, hence `|y_i| < sqrt((Y_KK)_ii)`. Its common-denominator
bound again gives polynomial encoding length. The feasible integral
system `2Pv' = y − Pe_0`, after denominators are cleared, has a
polynomial-size solution by Hermite normal form. It preserves `Pu` and
therefore the strict violation. This includes singular PSD input and
proves the required NP certificate bound.

## Fixed-rank search, and what support bounds imply

After the two easy hypermetric cases, the search is exact closest vector
to `t = δ_K/2` in `Λ = P Z^m` under the positive definite rational
metric `G`. In the lattice basis `W`, let `F = WᵀGW` and
`ξ = W⁻¹t`. The objective is `(a − ξ)ᵀF(a − ξ)`, `a ∈ Z^r`.
For splits the target is `−Pe_0/2` and the threshold is exactly `1/4`.
The lattice contains zero, so a nearest lattice point has norm at most
twice the target norm. Its rational coordinates and then its integer
basis coordinates have polynomial encoding lengths. Integral lifts
through `T` preserve the objective.

The literature lead verified Kannan's 1987 Theorem 4.5 in §4, p. 430:
the closest-vector algorithm takes `O(r^r L)` arithmetic operations
with polynomially bounded rational intermediate encoding lengths, for
rational basis and target input. Consequently it gives
`r^{O(r)} poly(L)` bit time here. The paper makes the rational-input
bridge explicit rather than attributing a rational Gram factorization
to Kannan.

One completely constructive bridge is useful. Rational LDLᵀ
factorization gives `F = L_0 diag(p_i/q_i) L_0ᵀ`, with positive rational
diagonals. Expand the positive integer `p_i q_i` in binary. An even
bit position is one integer square, and an odd bit position is two
equal integer squares. Thus it is a sum of `O(log(p_i q_i))` integer
squares. Dividing their square roots by `q_i` expresses `p_i/q_i` as
a sum of rational squares. Applying these rows to `L_0ᵀ` constructs a
rectangular rational `C` of polynomial encoding length with `CᵀC = F`.
The Euclidean CVP instance has independent rational generators `C` and
rational target `Cξ`, and still has lattice rank `r`. Its lattice
operations use the same rational inner products and projections.
Polynomial ambient dimension contributes only polynomial overhead.

The unsupported full-ball enumeration alternative should be omitted.
For example, take rank-two Euclidean generators
`b_0 = (0,2M+1)`, `b_1 = (1,0)`, `b_2 = (0,1)` and normalize their
Gram matrix by `(2M+1)²` so the root entry is one. The parity/CVP sphere
has radius `M+1/2` before normalization and contains Θ(`M²`) lattice
points, despite input length `O(log M)` and rank two. A good exact CVP
algorithm need not enumerate those points. The example specifically
rules out inferring a bit-polynomial bound from enumerating the original
threshold sphere; it does not rule out a more carefully specified
optimization algorithm.

For fixed hypermetric support `k`, enumerate vertex sets of size at
most `k`, choose a root in each set and solve its induced metric. The
correlation matrix has order at most `k−1`; no coefficient bound or
facet classification is needed. For rounded psd support `k`, the split
correspondence on each induced metric gives a moment matrix of order at
most `k`. For splits with variable-direction support `k`, solve each
principal submatrix on `{0} ∪ I`, of order at most `k+1`. These use
`O(n^k)` calls to the fixed-rank algorithm.

For gonality at most `k`, every integer coefficient vector is a sum of
at most `k` signed unit vectors. Enumerating those descriptions gives
`O((2|V|+1)^k)` candidates, followed by the appropriate sum or parity
filter. All these methods are polynomial for fixed `k`; their dependence
on `n` is XP, and they do not prove FPT in support or gonality.

## Normalized threshold and general integer rank-one boundaries

For a rational PSD general moment matrix
`Y = [[1,xᵀ],[x,B]]`, put `S = B − xxᵀ`. With `t = wᵀx`,

`q_Y(v_0,w) = (v_0+t)(v_0+t+1) + wᵀSw`.

The best offset is `v_0 = −floor(t) − 1`; if `t` is integral, the offset
`−floor(t)` ties. Its raw violation is exactly
`φ(t) − wᵀSw`, where `φ(t) = {t}(1−{t}) ≤ 1/4`. Since `S` is PSD,
normalized violation is at most `1/(4||w||²)`.

For rational `ρ > 0`, a normalized violation strictly greater than
`ρ` requires the positive integer `||w||²` to be at most

`B_ρ = max(0, ceil(1/(4ρ)) − 1)`.

If this bound is zero, no qualifying split exists. Otherwise enumerate
at most

`sum_(j=1)^min(n,B_ρ) binom(n,j) (2 floor(sqrt B_ρ))^j`

directions; this is at most
`(B_ρ+1)(2n sqrt B_ρ)^{B_ρ}`. Compute each exact best offset and compare
`φ(t) − wᵀSw` with `ρ||w||²`. The integer coefficients have
`O(log(B_ρ+1))` bits. Dot products, the exact floor and fractional part,
and the rational comparison have polynomial bit cost in their input
lengths. Thus the rigorous bound is `f(B_ρ)n^{B_ρ} poly(L+size ρ)`.
It is polynomial for fixed `ρ` and XP in the inverse threshold, with
strict equality handled correctly. This does not prove an efficient
algorithm for a threshold that shrinks as part of the input.

For rational PSD `Y`, the raw maximum is attained. If `D` is a common
denominator of `Y`, the values `uᵀYu` for `u ∈ e_0+2Z^{n+1}` form a
nonempty subset of the discrete nonnegative set `D⁻¹ Z`. Its minimum
exists. The parity identity gives a raw maximum at most `1/4`, and
`v = 0` guarantees that it is nonnegative. Equality with `1/4` holds
exactly when `Yu = 0` for such an integer parity vector. Clearing
denominators and solving `2Yv = −Ye_0` by Hermite normal form decides
that equality in polynomial time and produces an attaining split.
This does not compute a raw maximum below `1/4`, which remains within
the hard unrestricted separation problem.

The primitive-direction domination result has an exact proof. For
`w = k w'`, `k ≥ 2`, define

`t = floor((2s+1−k)/(2k))`,

`b = ((2s+1)k − (2t+1)k²)/2`, `a = k² − b`,

`c = (k(t+1)−s)(k(t+1)−s−1)`.

The floor gives `(2t+1)k ≤ 2s+1 < (2t+3)k`, hence `0 ≤ b < k²`
and `a > 0`. The value `c` is nonnegative because it is a product of
two consecutive integers. Matching quadratic and linear coefficients
in `(kz−s)(kz−s−1)` with `a(z−t)(z−t−1)` and
`b(z−t−1)(z−t−2)` gives the stated `a,b`. Evaluating at `z = t+1`
gives the constant `c`. Thus, for every symmetric matrix,

`q_Y(−s−1,kw') = a q_Y(−t−1,w') + b q_Y(−t−2,w') + cY_00`.

When `Y_00 ≥ 0`, negating and dividing by `k²||w'||²` bounds the
original normalized violation by the convex combination of the two
component normalized violations. One is at least as large. Repeating
with a common divisor yields a primitive direction, without losing
violation or normalized objective value. This proves the result in its
proper domain and supplies the correction identified above.

For rational rank-one general moments, write `Y = (1,x)(1,x)ᵀ`, let
`D` be the least common denominator of `x`, and put `p = D(1,x)`.
The vector `p` is primitive: for every prime dividing `D`, a reduced
coordinate denominator contains its highest power in `D`, and the
corresponding coordinate of `p` is not divisible by that prime. Hence
`pᵀv` ranges over every integer. Writing `m = pᵀv`,

`q_Y(v) = m(m+D)/D²`.

It is negative if and only if `−D < m < 0`, so separation is possible
exactly when `D ≥ 2`. The raw maximum is
`floor(D²/4)/D²`, obtained at `m = −floor(D/2)` or `−ceil(D/2)`.
Extended Euclid supplies a polynomial-size integer preimage of either
value. In particular the maximum is at least `2/9` for every fractional
rational point, even arbitrarily near an integer point.

For one variable `x_1 = 1−1/D`, the elementary violation is
`(D−1)/D²`; the raw maximizer has `v = (−a,a)`,
`a = floor(D/2)`. Its normalized value is `(D−a)/(D²a)`, strictly
smaller than the elementary value for `D ≥ 4`. This supports a precise
distinction between objectives, not a claim about the resulting SDP
bound improvements.

A restriction to `v ∈ {0,1}^{n+2}` can be hard at these general rank-one
points. From positive SUBSET SUM data `a_i,T`, take
`x_i = −12a_i/5`, `x_(n+1) = (12T−2)/5` and `Y = (1,x)(1,x)ᵀ`.
Violation means `−1 < τ < 0`, where
`τ = v_0 + sum v_i x_i`. Without the extra variable, `τ` is either
nonnegative or at most `−7/5`. With it, for a selected sum `A_I`,
`τ = v_0 − 2/5 + (12/5)(T−A_I)`. If `A_I = T`, choose `v_0 = 0`.
If the difference is negative, both offsets give `τ ≤ −9/5`; if
positive, both give `τ ≥ 2`. Therefore restricted violation is
NP-complete by SUBSET SUM, while unrestricted separation is polynomial.
The argument proves ordinary hardness only and does not prove the
signed-box analogue at rank one.

These rank-one facts are outside the fractional Boolean moment domain:
its identities `Y_ii = Y_0i` force `x_i² = x_i` and integrality at rank
one. Keeping them in a separately named general-integer subsection is
essential for a coherent binary paper.

## Integer hardness as a consequence of the binary core

The older integer reduction has a sound strong-hardness argument: X3C
has bounded 0/1 data, its Gram numerators and common denominator are
polynomially bounded, and strict violators are exactly the specified
exact-cover vectors. Its positive-definite and bounded-support promises
are consistent with the certificate and fixed-rank results.

It need not be reproduced as a second main reduction. The paper's binary
construction already gives positive definite normalized general moment
matrices with the Boolean identities, numerators and denominators
bounded by `4(8n+2p+1)`, and precisely the exact-cover split violators.
Together with the short-split witness lemma this proves strong
NP-completeness of unrestricted integer split violation.

The same binary construction also recovers general-integer restricted
0/1 hardness without the older reduction. Its violator is
`(0,−1_T,1_g)`. Conjugating the moment matrix by
`diag(1,−1,…,−1,1)` turns this into `(0,1_T,1_g)` while preserving
positive definiteness, the normalized root entry and the polynomial
numerical bounds. In a no-instance there are no splits at all. This
proves strong restricted 0/1 hardness in the general moment domain.
The sign conjugation does not preserve the Boolean diagonal identities,
so this particular 0/1-family conclusion must not be asserted at binary
moment points on that basis.

The older raw-approximation corollary is also correct. Its sharpened
embedding argument excludes odd root coefficients of magnitude at
least three using the parity-block lower bound `n`, and gives raw
maximum either zero or `2/(N+7)` in input-matrix order `N`. It supports
the stated zero-versus-positive multiplicative obstruction and the
additive error obstruction below half that gap. It proves neither a
constant additive-gap result nor any normalized-violation result.
The binary core supplies a shorter analogous conclusion without another
construction: `μ(Y_ε)` is zero in no-instances and `1/(2N)` in
yes-instances, where now `N = 8n+2p+1` is the scaling parameter. A finite
multiplicative approximation, or additive error strictly below
`1/(4N)`, would distinguish X3C. These two uses of `N` must not be
confused. Manuscript inclusion is a scope choice; the existing
algorithmic section does not state a normalized approximation theorem.

## Gap-zero equivalence, certificates and complete reduction

Let `Z` be rational with unit diagonal. The condition `γ(b) = 0` is
equivalent to `sᵀb = 0` for some sign vector `s`. Thus a gap-zero
violator is a negative direction of `Z` on `s⊥`. Conversely, use the
integer basis `e_i − s_i s_n e_n`, `1 ≤ i < n`, of `s⊥`. Exact
negative-direction elimination on the restricted rational matrix gives
a polynomial-size integral negative vector in that hyperplane. Hence
gap-zero violation is equivalent to non-PSD restriction on at least one
such hyperplane. This proves NP membership with the sign vector `s`
alone as certificate. It also proves that every PSD point satisfies
every gap-zero inequality.

For hardness, pad a PARTITION instance to at least three entries and
append an equal number of zeros. A solution can be balanced in
cardinality by signs on the appended zeros. Thus it suffices to ask,
for nonnegative integer `c` of even length `n ≥ 6` and positive
`C = sum c`, whether there is a sign vector with
`sᵀc = sᵀ1 = 0`.

Put `K = 4nC`, `a = c+K1`, `A_2 = ||a||²`, and let `a_−,a_+`
be its extreme coordinates. Set

`θ_* = [2(n−1)a_−² − (n+1)a_+²]/[(n−1)(n−2)]`,

`ν = θ_*/(A_2 a_+²)`,

`ρ_i = a_i²(1 + νa_i²/A_2)`, `Δ = sum ρ_i`,

`θ_ij = (ρ_i+ρ_j)/(n−2) − Δ/[(n−1)(n−2)]`.

With the edge-weight Laplacian `L_θ` and `D_a = diag a`, define

`Z = D_a⁻¹ L_θ D_a⁻¹ − ν aaᵀ/A_2`.

The ratio `a_+/a_− ≤ 1+1/(4n)` implies `θ_* > 0` for `n ≥ 4`.
Also `θ_* ≤ a_−²/(n−1)` and
`ν ≤ 1/[n(n−1)a_+²] ≤ 1/n`. Thus
`ρ_− ≥ a_−²`, `ρ_+ ≤ a_+²(1+1/n)`, and

`θ_ij ≥ [2(n−1)ρ_− − nρ_+]/[(n−1)(n−2)] ≥ θ_* > 0`.

Summing the edge weights at vertex `i` gives exactly `ρ_i`.
Consequently `Z_ii = 1` and `Za = −νa`.

For `b ⊥ a`, put `h = D_a⁻¹b`. For every real `t`,

`sum a_i²(h_i−t)² = ||b||² + t² A_2 ≥ ||b||²`.

Since all edge weights are at least `θ_*`,

`bᵀZb = hᵀL_θh ≥ nθ_* min_t sum(h_i−t)²`

`≥ (nθ_*/a_+²)||b||²`.

Thus `Z` has exactly one negative eigenvalue, `−ν`, with eigenvector
`a`, and is uniformly positive definite on `a⊥`. If `sᵀa = 0`, the
integer vector `b = a` is a violated gap-zero coefficient vector.
Conversely, suppose `sᵀb = 0` and `bᵀZb < 0`. Decompose
`b = ta+b_⊥` with `b_⊥ ⊥ a`. The cross term vanishes. Negativity
forces `t ≠ 0` and

`||b_⊥||²/t² < ν A_2 a_+²/(nθ_*)`.

Hence

`|sᵀa| ≤ sqrt(n)||b_⊥||/|t| < sqrt(νA_2a_+²/θ_*) = 1`.

Since `sᵀa` is integral, it is zero. Because
`sᵀa = sᵀc + K sᵀ1` and `|sᵀc| ≤ C < K`, vanishing is equivalent
to both balanced partition conditions. This proves the reduction.
All constructed data have polynomial encoding length: `a_+ ≤
(4n+1)C`, and the displayed rational formulas require only polynomially
many arithmetic operations on polynomial-length integers. No bounded
magnitude conclusion follows when PARTITION numbers are exponentially
large; strong hardness has not been shown.

The metric promise admits exact uniform bounds. For `n ≥ 4`, let
`r = a_+/a_−`. Then `r² ≤ 1+33/(64n)`, `r² < 2`,
`νr² ≤ 1/[8n³(n−1)] ≤ 1/(384n)`, and so
`(1+ν)r² < 1+3/(5n)`. Therefore, for `n ≥ 6`,

`θ_ij/(a_i a_j) < (n−4/5)/[(n−1)(n−2)] ≤ 13/50`;

the last inequality is `(n−6)(13n−11) ≥ 0`. Moreover

`νa_i a_j/A_2 ≤ θ_*/A_2² ≤ 1/[16n⁴(n−1)] < 1/100`.

Thus the cut coordinates are

`d_ij = 1/2 + θ_ij/(2a_i a_j) + νa_i a_j/(2A_2)`

and satisfy `1/2 < d_ij < 127/200`. Every ordinary triangle has
right-hand side above one and left-hand side below one. Every perimeter
is below `381/200 < 2`. The reduction therefore lies in the strict
interior of the metric polytope, in both yes- and no-instances.

Replacing `ν` by any smaller positive rational value and recomputing
the weights preserves every argument, with the converse estimate now
at most one. This also gives the promise of arbitrary prescribed
positive rational spectral distance to the PSD cone, polynomially
encoded in the requested tolerance. It always retains one negative
eigenvalue and does not imply hardness at PSD points.

For general gap inequalities at non-PSD points, a polynomial-size
integer negative direction already proves violation because
`bᵀZb < 0 ≤ γ(b)²`. The exact value `γ(b)` is not supplied by that
certificate. At PSD points the general gap separation question is not
settled by these arguments: a no-instance for rounded psd inequalities
need not exclude a gap inequality with `γ ≥ 3`. This should remain a
limitation, not be promoted to an unproved hardness theorem.

## Recommended paper scope

Keep the rational certificate and fixed-rank theory as one shared
algorithmic section. Include fixed support and gonality as short
consequences, and state the normalized-threshold bound as XP. Include
the general integer rank-one examples only in a clearly separated
subsection. Derive integer strong hardness directly from the binary
positive-definite core instead of repeating the older lattice
construction. Keep gap-zero as a separate theorem with ordinary
NP-completeness, the exact metric promise and its exclusion from PSD
points. Do not add the practice experiments, the unproved signed-box
rank-one analogue, normalized approximation hardness, or a claim about
general gap separation at PSD points.

## Targeted local verification record

Only source and authored-document reads were run: `cat AGENTS.md`,
`cat` on the three specified notes and the paper's `main.tex` and
`macros.tex`, `rg -n` for relevant section headings and labels,
`sed -n` for the proof ranges stated above and the authored section
text, and `rg --files paper-binary-separation`. The final targeted reads
confirmed the ancillary proof text, citation slots and removal of
typographical `+not`/`+alone` artifacts. No test, experiment, checker,
build or CI check was run by this audit; the results reported here are
analytical proof checks.

The independent reviewer `review_algorithms_gap` subsequently confirmed
the section proofs, both ancillary additions and the four wording
clarifications without requesting further mathematical changes. That
review was also analytical.
