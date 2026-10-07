# Constrained moment/certificate closure: independent GPT audit

Date: 2026-10-06. Internal mathematical development and review evidence.

## Verdict

**ACCEPT.** Both constrained hierarchies in Section 08 have moment value equal to the supremum of real certificate values, and every level strictly below that moment value is certified at the same finite order. A global geometric error bound is unnecessary for this equality; nonemptiness of the original feasible set and the retained full box cones suffice. The existing error bounds therefore give real certificates with the same finite-order budgets plus arbitrary positive slack. No constrained moment Slater condition, closedness of the certificate cone, boundary certificate, rational certificate bound, or efficient construction follows from this argument.

This audit introduces no change to the primal rate proofs. The dense lift comparison is a separate source/claim issue; this argument does not turn a dense lift certificate into sparse membership.

## Exact spaces and cones

Fix a finite junction tree, an order `r>=1`, and objectives `f_b` of degree at most `2r`. Let

`V_b = R[x_(B_b)]_(<=2r)`, `U = direct_sum_b V_b`, and `W = sum_b V_b`

where `W` is a subspace of the global polynomial ring, with each coincident monomial collected once. The map `pi:U -> W` is `pi((p_b))=sum_b p_b`. By `lem:zero-decomposition` at `02-setting.tex:56–75`, its kernel consists exactly of signed edge-separator polynomial differences through degree `2r`. Thus `W` is canonically the stated direct-sum quotient. It is not the space of all degree-`2r` polynomials in all global variables: monomials spanning different bags need not belong to it.

For the ordinary constrained hierarchy, define the local cone

`C_b^mod = Mod_r(B_b) + sum_j g_(bj) SOS_(2(r-ceil(deg(g_(bj))/2)))(B_b)`.

For the single-extra-generator constrained preordering variant, define

`C_b^pre = Pre_r(B_b) + sum_(j,I subset B_b) g_(bj) q_I SOS_(2(r-|I|-ceil(deg(g_(bj))/2)))(B_b)`.

As throughout the paper, a negative allowance contributes only zero. A zero polynomial generator may simply be omitted. For a nonzero generator of degree `delta`, these allowances say exactly `delta+2|I|+2 deg(p)<=2r` for every square root `p`, with `I=empty` for the ordinary additional localizers. All displayed localizer terms belong to `V_b`. The cones are convex cones of finite sums of tested polynomials, without an assumption that their linear images are closed. Put `C=sum_b C_b` in `W`. This is exactly the cone dual to `08-extensions.tex:103–106` or `:169–173`, respectively. The preordering variant does not add products of two distinct extra generators.

Constants translated between bags do not change `W`: every local copy of `1` maps to the same global polynomial `1`. Edge consistency for the constant polynomial identifies these copies in the quotient, including on empty separators. In particular, the quotient unit is represented by `1` in one bag; the tuple having `1` in every bag represents the polynomial equal to the number of bags, not the unit.

## Interior of the box cone in the full coefficient space

The box-only cone `C_box=sum_b Mod_r(B_b)` or `sum_b Pre_r(B_b)` is contained in `C`. The Gram map for its full monomial bases is onto `W` as a linear map on symmetric tuples. Indeed, a basis monomial `x^beta` of `W` lies in some bag and has `|beta|<=2r`. Split `beta=alpha+zeta` with `|alpha|,|zeta|<=r`. In that bag's empty-generator block, a diagonal entry one when `alpha=zeta`, or two symmetric off-diagonal entries one half otherwise, maps exactly to `x^beta`. These are the pivots in current `09-certificates.tex:187–200`. Consequently there is a linear right inverse `Z` on global collected coefficients, and the supplied construction gives `||Z(c)||_F<=||c||_1`.

The complement identities of `lem:rat-interior`, current `09-certificates.tex:74–112`, give a tuple `H` with `G(H)=1` and every retained box block at least `I/D_C`. Their degree and retention contracts were independently rechecked: the monomial telescope uses singleton box blocks; the generator-product telescope uses prefixes of retained products and satisfies `|beta|+a<=r`. For the ordinary restriction, empty or singleton source products require only the allowed empty and singleton blocks. No additional-generator Gram block is used in this interior representation.

For every coefficient perturbation `c` with `||c||_1<1/D_C`, each block perturbation `Z(c)` has spectral norm less than `1/D_C`. Therefore `H+Z(c)` is positive definite in every box block and represents `1+c`. This proves an actual coefficient ball around `1` inside `C_box`, so

`1 in int_W(C_box) subset int_W(C)`.

Positive definiteness of one Gram tuple alone would not be enough without surjectivity onto the chosen coefficient space; the preceding full-basis argument supplies that missing logical step explicitly. No surjectivity onto polynomials spanning several bags is claimed or needed.

Empty bags do not obstruct this argument. Their polynomial space is the constants and their box Gram block is the scalar basis `(1)`. The same complement proof includes their sole diagonal position, whose complement is zero, and gives it its own positive baseline. Alternatively, their constant terms can be assigned to a nonempty bag. The latter reassignment does not remove any essential extra constraint: an empty-bag generator is constant and must be nonnegative when `K` is nonempty. Its tested cone contribution is then already a nonnegative constant. The direct scalar-block treatment is simpler when retaining the original local moment formulation.

For the shortest manuscript proof, the same interior fact also follows directly without a forward reference to Section 09. Split each bag-supported monomial exponent as `beta=alpha+zeta` with both total degrees at most `r`. The identity

`1 +/- x^beta = ((1-x^(2 alpha))+(1-x^(2 zeta))+(x^alpha +/- x^zeta)^2)/2`

lies in the ordinary box module through degree `2r`: each monomial complement telescopes into singleton box generators times squares of degree at most `r-1`, and the remaining square has degree at most `2r`. Thus `1+e` and `1-e` belong to `C_box` for every monomial basis element `e` of `W`. For `q=sum_e c_e e` with `sum_e |c_e|<=1`, write `1+q=(1-sum_e |c_e|)1+sum_e |c_e|(1+sign(c_e)e)`. This gives the coefficient ball around the unit immediately, exactly as in `06:427–437`. It proves the same full-degree contract and is a simpler presentation of this closure result; the Gram reconstruction above separately validates the proposed Section 09 route.

## Correspondence with normalized dual functionals

Define `D={F in W*: F(c)>=0 for all c in C, F(1)=1}`. A feasible local family determines

`F(sum_b p_b)=sum_b L_b(p_b)`.

This is well defined because the difference of two decompositions is an edge-separator decomposition of zero and every separator moment equality holds through degree `2r`. It gives `F(1)=1` since the global unit can be represented in any single bag, and `F>=0` on `C` since each local cone is tested nonnegatively. The objective is `F(f)=sum_b L_b(f_b)`.

Conversely, restrict `F in D` to each embedded local space `V_b`. Each local unit is the same global unit, so every restriction has mass one. Positivity on each embedded local cone gives precisely the required moment and localizing inequalities. A separator polynomial is the same element of `W` from either endpoint, so all separator equalities hold. This proves exact correspondence and

`rho_r = min_(F in D) F(f)`.

Here the minimum is justified, not assumed. Evaluation at any point of nonempty `K` is in `D`. The box tests bound every local monomial moment through degree `2r` by one, by `lem:compact` at `02-setting.tex:268–286`: even monomial squares telescope down to the unit, and a split into two degree-at-most-`r` monomials permits Cauchy--Schwarz. Extra localizers preserve these bounds. The feasible family set is a nonempty closed bounded subset of a finite moment space, hence compact. Equivalently, `D` is closed and its coordinates in a monomial basis of `W` are bounded. Its objective minimum is finite and attained. This does not mean that its matrices are strictly positive definite.

## Separation gives exact strict-level membership

Let `lambda<rho_r` and suppose `p=f-lambda` is outside `C`. A convex set with nonempty interior in a finite-dimensional space can be weakly separated from a point outside it, even if the set is not closed. Applying that separation fact to `C` gives a nonzero `F in W*` such that

`F(c)>=F(p)` for every `c in C`.

Taking `c=0` gives `F(p)<=0`. If `F(c_0)<0` for some `c_0 in C`, its arbitrarily large positive multiples contradict this inequality; hence `F>=0` on `C`. Interior of `1` now forces `F(1)>0`: nonnegativity gives `F(1)>=0`, and if it were zero, the ball of `1+q` and `1-q` in `C` would force `F(q)=0` in every direction, contradicting `F!=0`.

Thus `G=F/F(1)` belongs to `D`, and `F(p)<=0` gives `G(f)<=lambda<rho_r`, a contradiction. Therefore

`f-lambda in C` for every `lambda<rho_r`.

This is membership in the cone of finite SOS sums itself, not only in its closure. The argument is the separation step of `prop:rec-dual`, current `06-recourse.tex:448–458`, with the scalar full-box interior supplied above in place of the recourse order-unit lemma. No constrained primal Slater theorem is being invoked. Weak duality gives the converse inequality for every feasible certificate, so

`sup{lambda: f-lambda in C}=rho_r`.

The proof does not establish `f-rho_r in C`. Nonclosedness of `C` is allowed throughout. Every strict-level membership is an identity of global polynomials `f-lambda=sum_b c_b`, with `c_b in C_b` of total degree at most `2r`; equivalently, it has the corresponding local Gram multipliers and cancelling separator polynomials. No dense certificate or higher degree is introduced.

## Consequence for the current rate statements

For either error budget `E_r` already proved in Section 08, the inequality `f*-rho_r<=E_r` implies, for every `epsilon>0`,

`f-f*+E_r+epsilon in C`

at that exact same order and with the stated localizer family. Specifically, use

- `E_r=3 A/D_m + L_f H (12 G/D_m)^(alpha/2)` from `thm:constr-pre`, current `08-extensions.tex:113–125`;
- `E_r=E+L_f H U^(alpha/2)` from `thm:constr-mod`, current `08-extensions.tex:285–299`.

Indeed `lambda=f*-E_r-epsilon<rho_r`, so the strict-level result applies. Any chosen positive `epsilon_r` of the same or smaller asymptotic order retains `O(r^-alpha)` and `O((log r/r)^alpha)`, respectively. The exact displayed budget without extra slack is not justified as a boundary membership statement by this proof. The constant-objective case can of course be certified directly.

A concise manuscript proposition can assert, for either Section 08 cone, compact primal attainment, equality of the moment value and certificate supremum, strict-level certificates, and these two budget-plus-slack consequences. Its proof should name the global coefficient space, invoke decomposition of zero for the functional correspondence, invoke the full box Gram interior together with onto coefficient map, and reproduce the short separation contradiction. The current sentence at `08:372–374` and the matching discussion scope should then distinguish the proved strict-level certificates from unproved boundary attainment, instead of describing all constrained conclusions as primal only. The global error bound still does not supply strict moment feasibility or boundary dual attainment.

## Boundary and scope checks

- The proposition needs the objective to belong to `W`, i.e. each `deg(f_b)<=2r`. Both current rate theorems satisfy a stronger degree reserve.
- Generators whose allowance is negative have no Gram block or localizer term. Their absence does not remove the box cone or invalidate the correspondence or separation argument. Odd generator degrees require the ceiling in the SOS allowance stated above.
- Equalities expressed as opposite inequalities and feasible sets with empty interior are allowed. Point evaluation supplies feasibility, while the *certificate* box cone supplies the interior unit.
- Empty bags and empty separators are handled as above. The quotient is by all separator differences, including constants; omission of those constant equalities would change the correspondence.
- Section 08's continuous theorems use `r>=1`. If this algebraic proposition is separately extended to order zero with all negative-degree blocks omitted, `W` consists only of constants, box cones are nonnegative constants, and the same conclusion is immediate for objectives in that space. There is no need to extend the current kernel theorems to order zero or divide by width.
- Full monomial bases, or an explicitly proved equivalent full box cone, are essential to this particular interior argument. Arbitrary reduced Gram bases are not covered.
- The result proves real certificates with strict slack. It supplies no rational bit bound for extra-generator cones and no certificate-construction algorithm. Those remain outside this closure task.

## Snapshot and actual verification record

Current SHA-256 hashes of the files supplying the proof contracts:

```text
0b69c1dd6bf4d8712d2891ca579ca9004099f12f1aea0ba9957aa399774315c6  sections/02-setting.tex
afc7a509b9c4828b28873ad9a82de539d5c9a352f9421a7ac0500bb251bd9042  sections/06-recourse.tex
afb8e1903402dc41977f9a5d15783ce3f71967ed2cb12ea6eee330818819b7e8  sections/08-extensions.tex
16f211c8a1f5b5a99ca18dc5f0db761d1b6ad228433b28f3c586f1673f82548a  sections/09-certificates.tex
```

Targeted commands actually run were `cat AGENTS.md`, `sed -n` on the identified portions of Sections 02/06/08/09, `rg -n` for their exact labels and the report's verdict/contract markers, `wc -l -w` on this report, and `sha256sum` on those four source files and this report. Mathematical verification consisted of the coefficient-domain and kernel identification, Gram-map surjectivity and interior ball, direct monomial order-unit identity, normalized functional correspondence, moment compactness, weak-separation contradiction, and strict-slack rate transfer recorded above. No TeX was edited. Only this report was written. No browsing, children, experiments, tests, CI inspection, or project-wide verification was performed.

## Recheck of the integrated manuscript

Date: 2026-10-06. **ACCEPT the actual integrated sources; no remaining mathematical finding.** This recheck reads the written proposition and interfaces, rather than merely accepting the proposed proof above.

At current `08-extensions.tex:378–390`, the two certificate cones consist of the precise tested finite SOS sums, with each summand through total degree `2r`, full bases, and absent blocks with no allowed monomials. This gives the correct odd-degree generator allowances implicitly and does not include products of distinct extra generators. The proposition's assumptions at `:393` require nonempty `K`, positive finite order, and every local objective in the coefficient space. They are sufficient without the global geometric bound.

At `08:405–419`, the coefficient space is the sum of bag-supported degree-`2r` polynomial spaces. The monomial split and exact order-unit identity are valid in the ordinary box module at order `r`, including the constant monomial. The complement telescopes use only individual box generators and degree at most `2r`. The nonnegative combination of the identities gives a coefficient ball about the global unit in this space. This avoids any unproved surjectivity or dense-to-sparse inference.

At `08:421–426`, the decomposition-of-zero lemma supplies the exact normalized-functional correspondence, including local units and separator constants. Point evaluation on `K` supplies feasibility, and the existing box moment bound supplies closedness and boundedness of the dual-functional/moment set. Thus the primal minimum is finite and attained. Empty bags contribute only the same global constant, so their presence does not change the argument.

At `08:428–437`, separation from the interior of the possibly nonclosed convex cone gives the nonzero functional with the stated signs; continuity extends its inequality from the interior to the cone. Interior of the unit forces a positive unit value, and normalization contradicts `lambda<rho_r`. This proves membership in the exact finite cone at every strict level, then weak duality gives equality of the supremum and moment value. The proposition expressly withholds boundary membership at `:401–402`.

At `08:439–449`, the error budgets are exactly those in the two preceding primal theorems. Adding positive `epsilon` makes the target level strictly lower than `rho_r`, so the certificate is at the same order with those budgets plus arbitrary positive slack. Equality constraints and empty feasible interior need no moment Slater assumption for this conclusion. No extra rationalization or construction conclusion is inserted.

The matching introduction at `01-introduction.tex:264–267` and discussion at `10-discussion.tex:88–92` correctly describe the strict-slack consequence and lack of established boundary attainment. Their remaining rational statements apply to box-only certificates. At `08:465–470`, the lift comparator now explicitly concerns a dense formulation and dense certificate cone; the text does not assert that its lifted certificate preserves bags. This scope correction is accepted. The underlying literature-derived dense composition and its priority qualification remain the responsibility of the designated literature/source audit, not a new primary-source verification in this recheck.

Accepted integrated snapshot hashes:

```text
e4896d54f29bc7f4491942d115285c96101a92dd2b7b82697f63bd95377b05d9  sections/01-introduction.tex
0b69c1dd6bf4d8712d2891ca579ca9004099f12f1aea0ba9957aa399774315c6  sections/02-setting.tex
afc7a509b9c4828b28873ad9a82de539d5c9a352f9421a7ac0500bb251bd9042  sections/06-recourse.tex
e3ffdc703db3b03c2736dc8b97ebaf85c53d93f9296c6e2e52f4754ad35ab595  sections/08-extensions.tex
16f211c8a1f5b5a99ca18dc5f0db761d1b6ad228433b28f3c586f1673f82548a  sections/09-certificates.tex
0f7309dc8c9de7d7fab20a01c48eb7ef7a7d4c8089d47b94b88443827a26582f  sections/10-discussion.tex
```

Actual added inspection commands were `sed -n '360,490p' sections/08-extensions.tex | nl -ba -v360`, `sed -n '246,283p' sections/01-introduction.tex | nl -ba -v246`, `sed -n '74,106p' sections/10-discussion.tex | nl -ba -v74`, and `sha256sum` on the six files above. Report checks used `wc -l -w` and `sha256sum`. No manuscript edit, browsing, child agent, experiment, test, build, or CI inspection was performed.

Final notation-only recheck (2026-10-06): **ACCEPT** `08:378–403`, where `sigma^g_(bj)` now distinguishes additional-generator multipliers from box multipliers; `sed -n '378,403p' sections/08-extensions.tex | nl -ba -v378` and `sha256sum sections/08-extensions.tex` confirm accepted updated SHA-256 `88f01b9ad4b122be22dd617bd9b96164b5337647b783afbcfce98972293d3d98`. The theorem and proof conclusions above are unchanged.
