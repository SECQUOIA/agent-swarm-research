# Independent review of the extensions manuscript

Reviewer: Sol. Date: 2026-10-05. This is an independent review of authored manuscript text, not an endorsement inferred from the development audits. No completed Opus manuscript review is claimed.

## Scope and final verdict

Section 08, `sections/08-extensions.tex`, was reviewed in full against the Section 02/03/04 interfaces. Its mathematical statements and proofs are accepted. No mathematical defect or proof-completeness blocker was found. The constrained statements have the necessary degree reserves and remain primal statements. The labelled statements handle label fibers, zero masses, empty continuous bags, all-discrete order zero, and pruning before Slater correctly.

Section 09, `sections/09-certificates.tex`, was then reviewed in full. Its rational witness theorem, quantitative box corollary, and exact checking claim are accepted. It correctly separates polynomial-bit witness existence and exact checking from a polynomial-time algorithm to locate the real or rational witness. No such construction-time claim is made, so the unresolved external strong-feasibility ellipsoid theorem is not a dependency of this manuscript section. No mathematical repair is required in either section.

## Findings requiring integration attention

**L1 — Literature dependency; not a mathematical defect.** Section 08 lines 383–398 (`rem:ext-prior`) attributes the dense constrained exponent to Tran–Toh and the lift composition to Heijmans-Kuryatnikova–Vera–Zuluaga, and compares the global hypothesis with Korda–Magron–Ríos-Zertuche's local hypotheses. These comparisons agree with the supplied architecture and development notes, but `evidence/LITERATURE.md` was absent, and `LITERATURE-PRELIMINARY.md` did not supply the Tran–Toh/lift source locators. Luna must validate the exact versions, theorem hypotheses, exponent convention, and fixed-data logarithmic composition. If the supplied literature evidence cannot establish the lift comparison, delete that comparison sentence; the authored direct-displacement theorem and proof do not depend on it. Priority is already appropriately qualified at lines 393 and 645–650.

**L2 — Shared standard-result dependencies; not a mathematical defect.** Section 08 lines 215–221 and 269–270 invoke the degree-preserving interval theorem in Section 02; lines 491–498 invoke standard-Borel gluing; lines 619–625 invoke finite-SDP primal Slater. The mathematical contracts are correct, including nonstrict univariate positivity and retained scalar blocks, but the preliminary literature file lists exact interval, disintegration, and finite-SDP Slater source locators as pending. Resolve those shared dependencies through Luna. No proof change in Section 08 is required if the cited sources establish the Section 02 statements as written.

## Independent reconstruction of Section 08

### Global repair and the distinction between local and global geometry

Lines 16–36 define the global intersection and squared violation using the supplied generators. Lines 53–65 give a complete measurable repair argument: a nearest point in a finite net has a Borel tie-breaking rule and lies at distance at most `dist(x,K)+epsilon`; Jensen applies to `t^(alpha/2)`; compactness of probability laws on compact `K` and continuity of the objective remove epsilon. This proves an existence result without assuming an efficient global projection or a measurable exact nearest-point selector.

The Lipschitz budget at lines 28–30 is valid in Euclidean norm: summing `|c_beta| sum_i beta_i^2` bounds the sum of coordinate derivative magnitudes, hence bounds their Euclidean norm. The common Slater interpolation at lines 75–82 repairs every generator simultaneously and stays in the box. The example at lines 85–95 has valid local repairs with constant one, but at `(t,0,0)` its global distance is `|t|` and squared violation is `t^4`, forcing `alpha<=1/2`. It therefore supports the precise caution made there and does not claim a hierarchy lower bound.

### Single-generator constrained preordering

Lines 100–111 specify the cone actually used: box-generator products times squares and each *one* additional generator times those products. No product of different additional generators is assumed. The Jackson kernel has certificate degree `2 v_b (m-1)<=2(r-d)` (lines 127–128). Multiplication by `(a+c g)^2` costs at most `2d`, leaving total degree at most `2r`; multiplication by `g` uses exactly the stated single-generator localizers and stays within degree `2r`.

The weighted PSD form at lines 134–147 gives `(-g(u))_+^2 h_b(u)<=L_b(K_b(g-g(u))^2)`, including zero density without division. Integration gives `J_b(g^2)-2g J_b g+g^2`. Its degree is at most `2d<=r`, as required by the half-range Chebyshev moment bound. The diagonal multiplier estimate applies also above the kernel frequency cutoff. By the Chebyshev product identity, `A(g^2)<=2 ||g||_Cheb A(g)`; therefore the displayed constant `12 ||g||_Cheb A(g)/D_m` at lines 155–159 follows. The objective and all generator violations are controlled under the *same* exactly glued box law. Global repair then proves the finite-order bound, and fixed `d,w` give `m=Theta(r)` and the asserted `r^-alpha` rate.

### Difference certificate and pseudo-displacement estimate

Lines 203–234 prove the multivariate difference inequality inside the ordinary box module, rather than apply a pointwise inequality to pseudomoments. For each tensor term, the normalized divided difference is polynomial of degree `k-1` and has interval modulus at most one by the derivative bound. Every factor complement has an interval certificate; telescoping their product uses square multipliers and one box generator per term. Consequently `1-R_ell^2` is certified through degree `2(|beta|-1)`. The exact weighted-square identity in lines 225–231 is valid: the pairwise-square sum equals `A sum w_ell(t_ell R_ell)^2-(sum w_ell t_ell R_ell)^2`. Multiplication by `t_ell^2` yields the degree cap `2 deg g`, including the constant case.

Lines 248–282 also establish the pseudo-displacement estimate with a certificate. Integrating polynomial squares yields PSD coefficient matrices, so `J_s` and `j_s=p_{s,N}J_s` are globally SOS. With the circular Fejer coefficients, Parseval gives `sum_j(b_j-b_{j-1})^2=2/s`, and `p_{s,N}<=2/C_s` gives `j_s<=4/(s C_s)`. The interval certificate for `c_s-j_s` has degree cap `D+2`. The mass factors are globally SOS, and the telescope for `1-prod omega` remains in the ordinary module. Thus both the subtracted displacement product and its upper complement are certified through degree `v_b D+2`, proving evaluation under `L_b`. No unproved implication from multivariate pointwise positivity to bounded-degree module membership appears.

### Exact-density domination and the constrained ordinary rate

The reserve `r>=wD+2d` in lines 285–287 covers each conditional square and localizer, the difference certificate multiplied by the SOS kernel, and the displacement bound. The difference certificate multiplication stays in the ordinary module, since every new multiplier is SOS. Lines 301–318 establish the integrated squared-violation estimate at degree `v_bD+2d<=r`, strictly within the functional's degree `2r`. Pointwise certificate choices are used only to prove scalar inequalities before integration, so there is no unaddressed measurability requirement.

The lower and upper source mass bounds at lines 320–328 follow from telescopes of interval-certified mass factors with SOS multipliers. The source term is the zero-residual term of the signed kernel. Singleton residual terms are nonnegative; all higher terms together are at least `-Delta_w`. Hence lines 330–345 correctly prove

`h_b^+ >= h_b/(1+Delta_w)`

and the positive remainder has mass `(1+Delta_w-Z_b)/(1+Delta_w)`. Its contribution to squared violation is bounded by `||g||_Cheb^2` times that mass, giving exactly the specified `U`. The same common correction gives exact separator marginals, so no tree disagreement probability or edge-count factor is introduced. The constants still contain the summed generator budgets, `H`, and the Lipschitz constant, as lines 375–376 state; no tree-independent *absolute* bound is claimed.

For lines 353–369, the even series length satisfies `delta<=s^-c_w/2` with `c_w>=3` and `2c_w>=w+1`. Thus `Delta_w=O_w(log^(max(w-2,0))(s)/s^3)=o_w(s^-2)` and `1-(1-delta)^v<=v delta`. These give `U=O(s^-2)` and `E=O(log(s)/s^2)`. The additive reserve leaves `s=Theta_w(r/log r)`. Raising squared violation to `alpha/2` gives `O((log r/r)^alpha)`; the separate objective term is smaller for every stated `alpha<=1`. Lines 372–381 correctly exclude automatic constrained dual attainment and qualify the power-one sharpness and logarithmic issue.

### Finite states, zero masses, and every separator fiber

Lines 403–435 specify explicit finite label lists, a common continuous box, running intersection for every variable, and fiber-summed separator equations for *every* separator assignment, including absent fibers. This is the correct separator contract. The mass-scaled Chebyshev proof at lines 443–454 bounds diagonal moments by the mass and uses PSD to eliminate all entries at mass zero. Splitting exponents into two factors of degree at most `r` proves that the *whole* truncated functional vanishes through degree `2r`, rather than merely its low-degree part.

For the labelled preordering, lines 481–498 obtain the mixed separator density by continuous integration followed by fiber summation. Global gluing preserves all bag marginals; arbitrary laws on null separator events do not change them; a finite union of forbidden-label events is null. Objective errors are multiplied by `tau_{b,a}`; maxima over labels make the data-only bound valid before taking the hierarchy infimum. Empty bags contribute scalar masses and zero error. The all-discrete argument at lines 504–508 uses the order-zero probability equations directly and never divides by width.

For the ordinary labelled cone, lines 535–554 use the same residual-square certificate and weighted PSD form with the label mass retained. Residual degrees are `(v_b+j)D<=2r`, and coefficient evaluation is used only at degree `(v_b-j)D<=r`. The common correction is `Delta_w tau_{b,a}`. The explicit separator formula at lines 559–565 makes *both* its signed part and its mass part agree after fiber summation. Absent fibers stay zero. This handles unequal fiber cardinalities without an extra label-count factor. The correction identity at lines 572–580 compares nonnegative measures of equal mass and remains valid at mass zero. Label-dependent constants cancel. The data-only estimate at lines 582–584 legitimately uses bag normalization before minimization. The `w=0` clause is separately proved.

### Pruning and real labelled duality

Lines 606–610 use the scalar mass equations to glue a finite law supported on the global permitted assignments. A nonextendable local label therefore has zero mass and a zero functional. Removal and reinsertion of these zero blocks preserve the feasible objectives. A strictly positive law on every global permitted assignment gives every retained local label positive mass; its product with a continuous uniform law makes every retained nonempty box-generator-weighted polynomial square strictly positive. Empty continuous bags retain positive scalar blocks. This is the required primal Slater point after pruning.

The moment argument at lines 620–623 proves compactness through degree `2r`; consequently the primal optimum is attained and finite. Finite-SDP Slater gives the attained dual and equality of values. Lines 627–642 correctly describe the labelled dual identity with fiber-indexed separator polynomials and cancellation for each permitted global assignment. The statement is not presented as an unlabelled surrogate-integer polynomial identity, an attained unpruned dual, or a rational size guarantee. The final Section 08 snapshot adds an explicit definition of `rho_r^mix` at lines 631–632; this clarification is accepted and changes no proof.

## Independent reconstruction of Section 09

### Cone, full bases, and the real membership prerequisite

Lines 13–42 define every retained Gram block and collect coincident bag-supported monomials globally. For the preordering, generator sets of cardinality greater than `r` are omitted, so every stated basis has a nonnegative degree allowance. For the ordinary module `r>=1` retains singleton scalar blocks. The map has integer coefficients of modulus at most two. The output space includes every monomial in a retained generator expansion, since its total degree is at most `2r` and its support lies in that bag.

The theorem's premise at lines 45–49 is real membership of `p-tau` in that *fixed* finite cone, with full bases. It does not replace this premise by positivity on the box. Lines 66–69 explicitly distinguish a short witness from a polynomial-time method of locating it. Running intersection is needed later for the rate-to-membership implication, not for the conditional algebraic theorem itself.

### Interior direction and trace bound

The complement identity at lines 83–101 is exact. Its first sum telescopes to `1-x^(2beta)`; its second sum to `x^(2beta)(1-q_I)`. A second-sum term uses monomial degree `|beta|+1` and a generator prefix of cardinality `a-1`, so its block allowance requires `|beta|+a<=r`, which follows from `|beta|+|I|<=r`. The first sum uses singleton blocks and satisfies their degree allowance. In the ordinary restriction, a singleton complement has only an empty-generator square in the second sum. Thus the proof works for both specified block families, including their highest-degree positions.

Averaging `1=h+(1-h)` over *all* `D_C` source diagonal positions gives each position its own `1/D_C` contribution and only nonnegative additional contributions. Therefore `H>=I/D_C` blockwise. A source identity contains `1+|beta|+|I|<=r+1` monomial squares with multiplicity, so its normalized contribution yields total trace at most `r+1`. No positive definite Gram representation is assumed without proof. Adding `tau H` to a real PSD representation of `p-tau` gives exact representation of `p` with margin `tau/D_C` in every block.

### Uniform moment outer bound and expanded-size qualification

Lines 142–156 prove positive definiteness of every weighted product-uniform moment matrix. The displayed one-dimensional uniform integrals are correct. The integer `((2r+3)!)^(2w)` clears their denominators even in generator-weighted coordinates. If a block has size `s`, its determinant is at least `q_0^-s` because the scaled integer matrix is positive definite; its other eigenvalues are at most `s` because its trace is at most `s`. This gives the stated lower eigenvalue bound and its common minimum `kappa_0`.

Applying one global uniform law to the *global coefficient identity* gives `sum tr(W Q)=ell(p)` exactly. Coincident monomials and overlaps create no extra factor. For PSD tuples, `ell(p)>=kappa_0 sum tr Q` and `ell(p)<=C_p`, giving the total-trace and aggregate-Frobenius bounds at lines 159–163. The encoding bound is polynomial because `r+1<=S` for a nonempty bag and `w` is bounded by the explicitly encoded bag lists. The argument uses expanded dimensions and does not infer polynomial size in the original optimization description.

### Global right inverse, rounding, and the factor two in denominators

For every global output monomial, the exponent split at lines 186–193 supplies two degree-at-most-`r` monomials in an empty-generator block. A diagonal pivot has coefficient one; an off-diagonal symmetric pair with entries one half has coefficient one. Distinct exponent sums cannot choose the same matrix position. These pivots therefore define a simultaneous global rational right inverse with the asserted Frobenius bound. Correction is performed after coefficient collection across all bags, so no overlapping-bag cancellation is lost.

Rounding all upper-triangular entries with error at most `h` gives aggregate Frobenius error at most `2 V_C h`. Each coefficient column has one-norm at most `2^(w+1)`, giving the displayed coefficient error. Applying the right inverse adds at most that coefficient error to the tuple norm. The combined bound `2^(w+2) V_C h` leaves block margin at least `tau/(2D_C)` when `h<=tau/(D_C 2^(w+3)V_C)`. The chosen rounding exponent has the stated polynomial size, while the outer bound controls rounded numerator sizes.

At lines 225–231, `L=lcm(2^B, input denominators)` clears the coefficient residual. The pivot correction introduces at most one further factor of two, so `2L` clears every final Gram entry. This is the correct bound also when an off-diagonal pivot halves an input coefficient with a higher two-adic denominator than the rounding grid. The exact coefficient identity and PSD margin, together with these numerator/denominator bounds, prove the short-witness theorem.

### Checking, approximate conversion, and the rate corollary

Lines 238–245 give a valid exact PSD test: eliminate positive diagonal pivots using Schur complements; a negative diagonal fails PSD; a zero diagonal with a nonzero corresponding off-diagonal entry fails PSD; an all-zero residual block is PSD. Determinant bounds control the rational intermediate sizes. Coefficient expansion has at most `M_C V_C` distinct map entries, so checking is polynomial in the expanded certificate encoding length. This is a checking-time claim, not a construction-time claim.

The optional approximate conversion estimate at lines 248–264 is also valid. An aggregate Frobenius error `e` bounds the upper-triangular error one-norm by `sqrt(V_C)e`; the coefficient map amplifies it by at most `2^(w+1)`. Applying the same right inverse and rounding estimate gives exactly the displayed bound. The sufficient closeness and margin conditions are explicit; an arbitrary numerical tuple is not promised to satisfy them.

In the corollary, the rational Chebyshev coefficient budgets are obtained from rational monomial data. The replacement `sqrt(2(D+1))<=2(D+1)` gives a rational majorant for the ordinary error. The box gap bound and finite-SDP Slater imply `rho_r>=lambda+tau` under the promise at lines 290–305, hence `f-lambda-tau` belongs to the *same* finite cone, even when the promise holds at equality. This is precisely the theorem premise. For the ordinary parameter choice, `D=O_w(s log s)` and `delta=O_w(s^-3)`, so the rational replacement contributes `O_w(log s/s^2)` and preserves the `log^3(r)/r^2` rate.

Lines 316–322 handle the no-continuous-variable constant separately and exclude automatic extensions to labelled, extra-generator, and reduced-basis cones. No claim about rational recourse certificates appears. Lines 324–337 properly attribute general strict-feasibility rational SOS recovery to Peyrl–Parrilo and Davis–Papp, consistent with the supplied preliminary literature evidence (pages 1–4/7–10 and 9–15/20–29, respectively). The box-specific conditioning argument is supplied inline. No external strong-feasibility theorem is cited or needed because no polynomial-time witness construction is claimed.

## Reviewed snapshots

SHA-256 hashes for this review:

```text
5600589262ae170d8ae6ac74bf2ebcd93e768b84a598ecd2fa2d54c204060c54  AGENTS.md
613c8c829190c229d570bf572efcdadf5ee8b7d09dfc5d984871281b7c379c85  evidence/BRIEF.md
1bc2a8bc24ef15e3fd766b55dae05156244a8d493d84824d5e94863fdf8c7a01  evidence/ARCHITECTURE.md
4666f3ed32a98012ac9ce844d9c5e934d55b5b57fdc2a168999f7480ef7bef7b  evidence/AUDIT-EXTENSIONS.md
9118df8f82002d9c64d04cc5f3b79555f86255f8ab626aaae4c50d8a36632f5f  evidence/reviews/developments-sol-r1.md
28e6a49a5b60663366bfc9aed098214bf8e3275389bc0d65b47d53ca5bc145fa  evidence/LITERATURE-PRELIMINARY.md
6db76f3db9195300a335e61feba66c387692e4e40dc59951fb2b50b020e8936b  sections/02-setting.tex
aa99f3f741b7fd0d61d4bd395b4a4f236589952d1c721645aac6985f7f1c8a2a  sections/03-kernels.tex
ca6da25fad4c8f14502e8599d96ecac40e327fd858bf49fd47a3712f07355197  sections/04-ordinary.tex
652761da6e0453aa04465ec823a75711b59caad3e296e42b456485c22a205f07  sections/08-extensions.tex
56351e2a33ed14724eabc185fa1e2536a54b9dd3b2d05be1eb3952709458f384  sections/09-certificates.tex
```

Except for the root `AGENTS.md`, paths in the hash record are relative to `paper-sparse-sos/`. Acceptance applies to these snapshots and the stated interfaces.

## Actual targeted verification

The review used targeted filesystem reads with `rg --files`, `rg -n`, `cat`, `nl -ba`, `sed -n`, `wc -l`, and `sha256sum`. These were inspection/document commands, not numerical tests or CI checks. Mathematical verification consisted of the independent identities, degree calculations, and boundary arguments recorded above. No experiment, primary literature search, CI inspection, project-wide verification, source TeX edit, other-paper edit, or delegation was performed. Only this review file was written.

Final targeted commands actually run were `wc -l -w paper-sparse-sos/evidence/reviews/extensions-manuscript-sol-r1.md` (123 lines, 2,784 words before this verification-record addition), `rg -n 'final verdict|Section 09|construction-time|mathematical repair|L1|L2|56351|652761' paper-sparse-sos/evidence/reviews/extensions-manuscript-sol-r1.md` (all verdict, dependency, construction-boundary, and hash markers found), and `sha256sum paper-sparse-sos/sections/08-extensions.tex paper-sparse-sos/sections/09-certificates.tex` (both final hashes match the record above). No CI result was inspected or inferred.
