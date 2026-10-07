# Final independent GPT review: constraints, finite states, and rational certificates

Date: 2026-10-05. This is internal review evidence, not submission text.

## Verdict and scope

The proofs in Sections 08 and 09 pass independent mathematical reconstruction. One minor clarification of the rational-input premise in Corollary `cor:rational-mod` was found, implemented by root, and independently rechecked. No unresolved mathematical finding remains. No fatal, major, or rate-changing defect was found. Section 08 and the short rational membership theorem needed no mathematical repair.

The review covers all of Sections 08 and 09, their mathematical interfaces with Sections 02–04, and their statements in the abstract, introduction, and discussion. The affine sharpness construction in Section 06 was inspected only to verify its use in Section 08's constrained-class sharpness statement. The other sections have separate final reviews. Acceptance here is a mathematical and exposition judgment on this scope, not a completed bibliography audit or a build result.

The proofs were reconstructed from the current TeX before consulting the earlier acceptance report. The research notes were used to check intended scope and to distinguish earlier constructions from the current statements. A delegated GPT cross-check separately challenged the rational proof and found the same premise precision issue. No literature search, experiment, historical checker, project-wide verification, CI inspection, or TeX edit was performed.

## Finding and exact repair

**P2, resolved — Make local rationality explicit in the rate specialization.** Original locations: `sections/09-certificates.tex:271–278` and `:298`; contract: `sections/02-setting.tex:44–46` and `:103–111`.

The sentence “Let the box objective and target ... be rational” can be read as requiring rational coefficients only for the global polynomial `f`. That does not ensure that the budgets `A` and `C_f`, defined from the supplied local `f_b`, are rational. For example, use two identical bags `{x}`, with

`f_1(x)=sqrt(2) x`, `f_2(x)=(1-sqrt(2)) x`.

Their sum is the rational polynomial `f=x`, but both supplied budgets equal `2 sqrt(2)-1`. The displayed preordering and ordinary budgets therefore need not be rational under the global-only interpretation. This matters because the corollary explicitly calls them rational gap budgets. It does not undermine the preceding theorem, whose premise is rational `p` and real membership of `p-tau` in a fixed finite cone.

Replace the corollary's opening with:

> Suppose every supplied local objective polynomial `f_b` has rational coefficients, let `lambda` be rational, and let `tau` be a positive rational number. Choose either of the following cones and rational gap budgets.

The existing proof then applies without any other change: rational monomial data in each `f_b` give rational tensor Chebyshev coefficients, coefficient budgets, and the two displayed gap budgets. Requiring only rationality of the global sum would instead need a separately chosen rational local decomposition and a recomputation of the decomposition-dependent budgets. The one-sentence local-data premise is the smallest coherent repair. Root implemented the explicit local-data premise; the narrow recheck below confirms resolution.

**Integration dependency, not a proof defect.** The current source audit and bibliography are being completed separately. This review does not certify the bibliographic identities or literature comparisons at `08:383–398`, `09:324–337`, or the shared citations for interval positivity, standard-Borel disintegration, and finite-SDP Slater. The mathematical contracts used here are correct: the interval theorem permits nonstrict positivity with the stated degree caps; the gluing proof uses regular conditional laws on standard Borel spaces; strictly feasible retained PSD blocks and finite primal value give attained finite-SDP duals. No stronger external result is needed. In particular, the current rational theorem makes no polynomial-time witness-construction claim and needs no ellipsoid theorem.

## Independently verified constrained contracts

### Geometry, measurability, and generator dependence

Locations: `08:14–96`.

The global error bound is stated for distance in all original coordinates to the common feasible intersection, using the sum of the supplied squared negative violations. Repeated generator assignments are counted repeatedly. The exponent and constant depend on this generator representation. The coefficient derivative budget gives a valid Euclidean Lipschitz bound: it bounds the sum of the magnitudes of the coordinate derivatives, which bounds the Euclidean gradient norm.

The finite-net repair proof is complete. A nearest point in a finite net, with a fixed ordering for ties, defines a Borel map. Its distance is at most `dist(x,K)+epsilon`. The Lipschitz inequality and Jensen's inequality for `t^(alpha/2)` apply to the original probability law. Weak compactness of probability laws on compact `K`, followed by continuity of `f`, removes the error `L_f epsilon`. This proves existence of a supported law and a feasible point no worse than its mean, without assuming a measurable exact projection or an efficient projection algorithm.

The common concave Slater interpolation is correct, including the empty-family convention. With `v=max(-g)_+`, `theta=v/(sigma_0+v)` makes every generator nonnegative at the same repaired point. The box diameter gives `H=2 sqrt(n)/sigma_0`. The local/global example is also correct: its local repairs stay inside the bag boxes and have distance bounded by the respective negative residual; globally `K={x=y=0}` times the free `z` interval. At `(t,0,0)`, distance is `|t|` and squared violation is `t^4`, so no global exponent greater than `1/2` can hold near zero. Neither local Slater nor this geometric example is misrepresented as a hierarchy rate theorem.

### Constrained preordering and total degrees

Locations: `08:100–164`; interfaces: `03:58–115`, `03:135–194`, `02:116–129`, `02:241–260`.

The stated localizers require each box-generator product times squares and each *single* additional generator times those products. They do not assume products of distinct additional generators. Ordinary additional-generator localizers alone would not suffice for this kernel, and the manuscript says so.

The kernel certificate has degree `2 v_b(m-1)<=2(r-d)`. Multiplication by `(a+c g)^2` costs at most `2d`; multiplication by `g` uses the stated additional localizers and also stays within degree `2r`. Conditional positivity and Cauchy--Schwarz therefore establish

`(-g(u))_+^2 h_b(u) <= L_b(K_b(x,u)(g(x)-g(u))^2)`.

The zero-density case uses positivity and makes no division. Integrating gives the polynomial `J_b(g^2)-2g J_b g+g^2`, of degree at most `2d<=r`. This is within the half-range Chebyshev moment bound, rather than merely within the functional's degree `2r`. The multiplier bound applies also above the kernel frequency cutoff. The Chebyshev product rule gives `A(g^2)<=2 ||g||_Cheb A(g)`, yielding the displayed factor `12 ||g||_Cheb A(g)/D_m`. Summation controls all generator violations under the same exactly glued box law. The objective error, global repair, and infimum argument give the stated bound and `O(r^-alpha)` rate at fixed data and width.

### Ordinary difference certificate and squared displacement

Locations: `08:191–283`; interfaces: `02:328–346`, `04:59–235`.

For each tensor Chebyshev term, the normalized divided difference has degree `k-1` and interval modulus at most one. Each univariate complement `1-a^2` therefore has the degree-preserving interval certificate. Telescoping one minus a product of squared factors uses only square multipliers and at most one box generator in every term. Thus `1-R_l^2` has an ordinary-module certificate through degree `2(|beta|-1)`.

The displayed weighted identity is exact: its pairwise-square sum equals

`A sum_l w_l (t_l R_l)^2 - (sum_l w_l t_l R_l)^2`.

Adding the complement terms produces the claimed difference polynomial. Multiplication by `t_l^2` raises the cap only to `2|beta|`; the pairwise squares obey the same cap. Constant `g` gives the zero polynomial. This proves membership in the ordinary module and does not infer it from multivariate pointwise nonnegativity.

Integration of polynomial squares gives a positive semidefinite coefficient matrix for `J_s`, and multiplication by the globally SOS normalization polynomial gives globally SOS `j_s`. Their degree caps are `2s` and `D+2`. The reflection argument for the two Fejér factors and the cosine displacement inequality reduce the bound to Parseval's sum `sum_j(b_j-b_(j-1))^2=2/s`: exactly `2s` successive differences have modulus `1/s`. Hence `j_s<=4/(s C_s)<=6/s^2` on the interval. Its even degree cap permits an interval certificate for `c_s-j_s`.

Each mass factor `omega` is globally SOS, and `1-omega` is interval-certified through degree `D`. The product telescope and the displayed complement identity give an ordinary-module certificate for `c_s-j_s(x_i) prod_(l!=i) omega(x_l)` through degree `v_b D+2`. The subtracted product itself is SOS through that degree. The lemma's stronger reserve `r>=v_b D+2` is sufficient for both evaluations; it is supplied by the theorem because `d>=1`.

### Exact-density domination, positive remainder, and the two logarithmic scales

Locations: `08:285–381`; interfaces: `04:271–320`, `04:333–386`, `04:418–480`, `04:498–562`.

The reserve `r>=wD+2d` covers conditional positivity for `1,g`, every additional-generator test, multiplication of the difference certificate by the SOS source kernel, and the displacement complement. These degrees are at most `v_b D+2d<=r` or, where only localizer evaluation is used, at most `2r`. At each fixed output, the certificates justify scalar inequalities before integration; no measurable selection of certificates is required.

The integrated source-density squared violation is bounded by `c_s A(g)^2`. Upper and lower source masses follow from product telescopes of `omega` and `omega-a_0`, with SOS preceding factors and nonnegative constant powers. They give `a_0^v_b<=Z_b<=1` at degree at most `v_b D`.

The residual expansion has the source density as its zero-residual term, nonnegative singleton terms, and higher terms summing to at least `-Delta_w`. Consequently

`h_b^+ >= h_b/(1+Delta_w)`.

The difference is a nonnegative density of mass `(1+Delta_w-Z_b)/(1+Delta_w)`. Bounding its squared violation by `||g||_Cheb^2` gives exactly the displayed `U`. The correction has the same scalar in all bags, so it preserves exact separator marginals and glues without an edge disagreement term. The estimates retain the sums of generator budgets, the supplied global `H`, and `L_f`; they are not absolute bounds uniform over generator families or problem size.

For the stated even `N`, `delta<=s^-c_w/2`, with `c_w>=3` and `2c_w>=w+1`. The residual sum satisfies `Delta_w=O_w(log^(max(w-2,0))(s)/s^3)=o_w(s^-2)`, including zero correction at width one. Also `1-a_0^v<=v delta`. Thus `U=O(s^-2)` and the separate objective error is `E=O(log(s)/s^2)`. The additive reserve leaves `s=Theta_w(r/log r)`. This proves squared violation `O(log^2 r/r^2)`, objective smoothing `O(log^3 r/r^2)`, and repaired objective gap `O((log r/r)^alpha)`. The objective term is smaller for every stated `0<alpha<=1`.

The constrained theorem correctly remains a primal statement. A global error bound does not imply an attained constrained dual. The reference to the affine example is valid: its actual supported local measures remain feasible for the stronger constrained local positivity conditions. In the unscaled variables, increasing `y_2` to `max(y_2,|x|)` stays in the box and repairs the two inequalities at displacement at most the largest negative residual, giving a global linear bound. Its inverse-order local-measure obstruction therefore establishes sharpness of the power one for this class, without establishing necessity of the ordinary logarithm.

## Independently verified finite-state contracts

Locations: `08:403–650`; interfaces: `02:22–28`, `02:134–165`, `02:359–385`.

The model states finite explicit label domains, running intersection for all continuous and finite variables, a nonempty global permitted-assignment set, and the same continuous box for every label. It includes neither extra continuous constraints nor label-dependent boxes. The degree policies concern continuous degrees only. Empty continuous bags and all-discrete order zero are expressly separated from the positive-width kernel formulas.

The separator equality is the sum over every label fiber, for every separator assignment and every polynomial through degree `2r`. It includes assignments absent on one side. Continuous marginalization deletes kernel factors; discrete marginalization sums extending labels. This proves equality of mixed separator laws, rather than incorrectly equating individual full-bag labels. Gluing preserves every bag marginal; arbitrary choices on null separators do not change those marginals. The finite union of forbidden local-label events is null, giving permitted global support.

The mass-scaled Chebyshev certificate and moment Cauchy--Schwarz give `|L(T_beta)|<=tau` for degree at most `r`. At zero mass, every diagonal in the degree-`r` Chebyshev moment basis is zero, so every matrix entry is zero. Splitting every monomial exponent through degree `2r` into two exponents of degree at most `r` proves that the *entire* functional vanishes. Empty continuous bags have only their mass, including at order zero.

Preordering errors are weighted by `tau_(b,a)` before summation. The data-only maxima over labels are valid because bag masses sum to one. Label-dependent constants are preserved. With no continuous variables, these are consistent finite bag probabilities already at order zero, and their exact gluing preserves the objective; no division by width is used.

For the ordinary cone, the residual-square and weighted Cauchy--Schwarz proof is homogeneous in mass. Its degree is `(v_b+j)D<=2r`, while coefficient control is used only at `(v_b-j)D<=r`. The source and transformed costs have degree at most `v_b D<=r`. The correction is `Delta_w tau_(b,a)`, and the explicit separator formula sums both the signed-density term and the mass term over the same fibers. Both agree. Absent fibers remain zero. A bare constant per label would fail with unequal fiber cardinalities; the current formula does not make that error.

The correction objective identity compares nonnegative measures of the same mass, so its oscillation bound is valid at zero and positive mass. The data-only estimate uses bag normalization and `osc(f_(b,a))<=2 C_(b,a)`; it introduces no label-count factor. Explicit labels can still make the SDP large, as the manuscript states. All-constant labelled costs are exactly preserved even if continuous coordinates exist.

Pruning nonextendable labels preserves feasible objectives: the scalar masses glue to a permitted global finite law, so each such label has zero mass and therefore a zero whole functional. Removal and insertion of zero blocks preserve all equalities. A distribution positive on every permitted global assignment, independent of continuous product uniform measure, gives positive mass to each retained label and positive definite retained moment/localizing blocks. Empty continuous bags retain positive scalar blocks. Monomial telescopes and Cauchy--Schwarz bound all moments through `2r`, proving compactness and primal attainment. Finite-SDP Slater then gives dual equality and attainment after pruning.

The resulting certificate has a scalar per bag and a polynomial per edge and separator label, with the stated degree cap. For each permitted global assignment, separator terms cancel and the local cone memberships sum correctly. This is a real identity on the labelled assignment space, not an unlabelled polynomial identity in surrogate integer variables, an unpruned dual-attainment claim, or a rational witness-size theorem.

## Independently verified rational contracts

Locations: `09:13–264`; rate specialization: `09:269–322`; interfaces: `02:288–318`, `03:231–276`, `04:418–562`.

The theorem assumes real membership of rational `p-tau` in the prescribed finite cone with full monomial Gram bases. Pointwise positivity is not substituted for this premise. Preordering generator sets with cardinality greater than `r` are absent; ordinary singleton blocks are valid because `r>=1`. All generator expansion monomials have degree at most `2r` and support in the same bag. Coincident global monomials are collected into one row. Running intersection is unnecessary for this conditional rationalization theorem, although it is needed by the preceding sparse rate and finite-duality interfaces.

The interior complement identity is exact: its first sum is `1-x^(2 beta)`, and the second is `x^(2 beta)(1-q_I)`. A second-sum term has monomial degree `|beta|+1` and a generator prefix of size `a-1`, so its allowance is valid because `|beta|+a<=r`. The first sum uses retained singleton blocks. For ordinary empty or singleton `I`, the second sum uses only an empty-generator block. Averaging over every diagonal position gives its own positive baseline `1/D_C`, with only nonnegative further contributions. Each source identity has `1+|beta|+|I|<=r+1` terms, proving the trace and encoding bounds. Adding `tau H` gives an exact real representation with margin `epsilon_*=tau/D_C` in every block.

The weighted product-uniform moment matrices are positive definite because the weights are positive on the open box. Their univariate integrals are correct. The integer `q_0=((2r+3)!)^(2w)` clears all denominators. For a size-`s` block, positivity of the scaled integer determinant gives `det(W)>=q_0^-s`; diagonal entries at most one give every eigenvalue at most `s`. Thus `lambda_min(W)>=q_0^-s s^-(s-1)>=kappa_0`. Applying one global uniform expectation to the global identity yields `sum tr(W Q)=ell(p)` without an overlap multiplicity. Positive semidefiniteness gives the total-trace bound and aggregate Frobenius bound. The encoded bound is polynomial in expanded dimensions and input because `r+1<=S_C` for a nonempty bag and width is bounded by the explicit bag-list length.

Every output monomial has a containing bag and an exponent split into two degree-at-most-`r` monomials. An empty-block diagonal pivot one, or symmetric off-diagonal entries one half, maps to that monomial exactly and has Frobenius norm at most one. Distinct monomials cannot share a matrix position because a position has one exponent sum. Hence the pivots form a simultaneous rational right inverse on global collected coefficients, with the claimed norm bound.

Rounding upper-triangular entries to a dyadic grid gives the stated tuple and coefficient-error bounds. Right-inverse correction makes the identity exact and changes the tuple by at most `2^(w+2) V_C h`. Choosing `h<=epsilon_*/(2^(w+3) V_C)` leaves margin at least `epsilon_*/2` blockwise. The outer bound controls numerator sizes. The final denominator divisor is correctly `2 lcm(2^B, input coefficient denominators)`: the additional factor two is needed when an off-diagonal pivot halves an input coefficient with a higher power of two in its denominator. Coefficient formation and correction use polynomially many rational operations. The rounding exponent and all numerator/denominator lengths are polynomial in the stated expanded parameters and input length.

The per-column upper bound `2^w` does not cause a hidden exponential checking claim: each column's distinct actual expansion monomials lie among the `M_C` output rows, so full expansion has at most `M_C V_C` entries. In fact, simultaneous pivots imply `M_C<=V_C`. Exact PSD elimination is complete: positive diagonal pivots permit Schur complements; negative diagonals fail PSD; a zero diagonal with a nonzero corresponding row fails PSD; a zero row can be discarded; an all-zero residual block is PSD. After denominator clearing, Schur entries are ratios of minors, so determinant bounds give polynomial intermediate bit length. Identity matching and supplied-witness checking are therefore polynomial in expanded certificate encoding length.

The approximate conversion estimate is also correct. Aggregate Frobenius error `e` bounds the upper-triangular one-norm by `sqrt(V_C)e`; each coefficient column has one-norm at most `2^(w+1)`. The same right inverse and rounding estimate give the displayed sufficient margin condition. Arbitrary numerical output is not promised to meet it. The proof rounds an unspecified real witness and establishes polynomial witness size; it does not establish polynomial-time construction. This deliberate restriction is respected throughout Sections 09 and 10.

After the local rationality clarification, both rate budgets are rational. The ordinary replacement `sqrt(2(D+1))<=2(D+1)` is a valid majorant, and monotonicity gives the correct gap budget for the ordinary cone itself. With the stated parameter choice, `D=O_w(s log s)` and `delta=O_w(s^-3)`, so the rational replacement contributes `O_w(log s/s^2)` and preserves `C_f O_(w,d_infty)(log^3 r/r^2)`. For `d_infty=0`, all local costs are constant and `C_f=A=0`, so both budgets vanish even though the auxiliary `eta_Q` is positive.

Finite box dual attainment gives `f-rho_r` in the same cone. The slack promise gives `rho_r>=lambda+tau`, including equality, and adding the nonnegative constant proves `f-lambda-tau` membership. The rational theorem then applies. All-unlabelled-constant/no-continuous-variable cases are stated separately. Nothing in this argument supplies rational recourse certificates or automatic rationalization for labelled cones, extra generators, or reduced Gram bases, and the manuscript expressly excludes those extrapolations.

## Front and discussion interfaces

Locations: abstract final paragraph; `01:252–270`; `10:73–93`, `10:108–125`.

The front matter identifies the global geometric assumption, the two constrained rates, squared ordinary violation at the two-logarithm scale, and primal-only constrained conclusions. It does not silently replace global error bounds by local bounds. Finite-state results are confined to their stated common-box model. Rational certificates require objective slack beyond the finite-order budget and use expanded SDP size. The discussion does not turn existence of repair into an efficient algorithm, certificate checking into construction time, or expanded certificate size into polynomial size in the original optimization input. Ordinary recourse and general multivariate multiplier extensions remain explicitly open.

## Snapshot hashes

SHA-256 of the full reviewed snapshots before the P2 premise repair. The final Section 09 hash and resolution are recorded immediately below. Manuscript paths are relative to `paper-sparse-sos/`; research-note paths are relative to the repository root.

```text
5600589262ae170d8ae6ac74bf2ebcd93e768b84a598ecd2fa2d54c204060c54  ../AGENTS.md
613c8c829190c229d570bf572efcdadf5ee8b7d09dfc5d984871281b7c379c85  evidence/BRIEF.md
c5818b22fd00210470838f9e8f119e09daeff4d2df1cb516c6cc3a3654784f79  sections/00-abstract.tex
11d457039c8bfe203a03106cd404a010989259897b6d8982e07fd2a43d3c77d8  sections/01-introduction.tex
6db76f3db9195300a335e61feba66c387692e4e40dc59951fb2b50b020e8936b  sections/02-setting.tex
aa99f3f741b7fd0d61d4bd395b4a4f236589952d1c721645aac6985f7f1c8a2a  sections/03-kernels.tex
c259609d74d3ef5520d2bf1773eb363391c119ec2df0202abf278aa0191556e4  sections/04-ordinary.tex
b8b88edc1f966255db50470c754ff123b43dab7aeb7a54d1c62656a083c31ba6  sections/06-recourse.tex
652761da6e0453aa04465ec823a75711b59caad3e296e42b456485c22a205f07  sections/08-extensions.tex
56351e2a33ed14724eabc185fa1e2536a54b9dd3b2d05be1eb3952709458f384  sections/09-certificates.tex
4cbcc0716204ffc2375a37d467c4577bf35dbb8f0c7bf2a09c9026fe12413137  sections/10-discussion.tex
f5a1ad76af4428a8f4c1db6e8d18f5f2f2ce62cbdcc913d05d4a064065a44e80  research-20260928/solver/general-constraints-kernel.md
b2b1b14ccbd61abd583dcc19e77c233fcbd7349aef090bb7c22d26bc28a95c76  research-20260928/solver/mixed-discrete-extension.md
725fa58113ac6fc54a6b74bd89f1a7efee5b69c6d12cb29449c0186927617e8e  research-20260928/solver/rational-sparse-certificates.md
020e99ad48fa78ca4345e346339a16602f8bdd54992e11da923c5e74e78bac43  research-20260928/closing-research-results.md
```

## Narrow recheck of the implemented repair

Current `sections/09-certificates.tex:271–272` now reads:

> Let every supplied local objective polynomial `f_b` have rational coefficients, and let `lambda` be rational and `tau` be a positive rational number.

The source uses the precise mathematical forms `lambda in Q` and `tau in Q_(>0)`. This supplies exactly the rational local-data premise required by the unchanged budgets and proof at current lines 279, 285–288, and 299–314. No modification to the underlying real-membership, rationalization, or rate arguments is needed. The P2 finding is resolved. Section 08 and the reviewed Section 04, introduction, and discussion hashes were rechecked and remain unchanged.

Final accepted Section 09 snapshot:

```text
8d3819602848dc43441ae99e090f60ee4f46e703de8a86560544e96966b582a2  sections/09-certificates.tex
```

Line references elsewhere in this report to Section 09 at or below the corollary refer to the original full snapshot; the repair adds one source line from original line 273 onward. The core theorem and proof through line 264 retain their locators.

## Actual targeted verification

Commands actually run for inspection were `rg --files`, `rg -n`, `cat`, `nl -ba`, `sed -n`, and `sha256sum`, on the named manuscript and research-note files. The final narrow recheck used `sed -n '266,315p' sections/09-certificates.tex | nl -ba -v266` and `sha256sum sections/08-extensions.tex sections/09-certificates.tex sections/04-ordinary.tex sections/01-introduction.tex sections/10-discussion.tex`, confirming the repaired premise and the final hash above. A document inspection used `wc -l -w evidence/reviews/final-extensions-gpt-r1.md`. The mathematical checks were the independent identities, degree bounds, mass/measure arguments, error estimates, and bit-length arguments recorded above. The delegated cross-check was read-only and performed no tests or literature research. Only this review file was written by this reviewer. No build, numerical experiment, historical checker, CI check, or project-wide verification was run or inferred.

Final disposition: **accept the scoped mathematics and implemented premise repair; no unresolved mathematical finding. Retain the separate source-integration dependency.**
