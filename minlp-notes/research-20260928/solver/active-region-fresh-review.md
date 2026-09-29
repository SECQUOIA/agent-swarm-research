# Independent review of the regular recourse rate theorem

Date: 2026-09-28. Reviewed
[active-region-rates.md](active-region-rates.md), including both regularity
theorems and the fixed sharp example, against the hierarchy in
[affine-recourse-kernel-upper.md](affine-recourse-kernel-upper.md).

**Finding:** no fatal gap or required mathematical correction was found.
The proof establishes its stated weighted-Chebyshev and coordinatewise
regularity results for the rectangular, full shared-box preordering
hierarchy. It does not establish the result for arbitrary multivariate
Lipschitz multiplier projections. This review is evidence of correctness,
not a formal verification or a priority determination.

## Proof audit

1. **KKT sign and use of projected multipliers.** With constraints
   `Cy <= e + Dv`, stationarity gives
   `q(v)+2Q(v)y*(v)=-C^T lambda(v)`. Direct expansion yields
   `f(v,y)-F(v)-lambda(v)^T(e+Dv-Cy)
   =(y-y*)^T Q(v)(y-y*)` after complementarity. In particular the sign in
   (15) is correct. At a source-feasible conditional mean, replacing
   `e+Dv-Cybar` by `e+D ubar-Cybar+D(v-ubar)` gives precisely the positive
   correction `a(v)^T(U-vh)` in (16). No norm or measurable selection of
   the full multiplier vector is needed: the subsequent expression uses
   only the bounded regular projection.

2. **The rectangular moment bound covers the actual frequencies.** The
   usual condition `|alpha|<=r` would be insufficient for the commutator.
   Lemma 3 supplies the stronger condition
   `sum_i ceil(alpha_i/2)<=r`. Its univariate input has the correct degree:
   for even `n=2q`,
   `1+T_n=2T_q^2` and
   `1-T_n=2(1-x^2)U_(q-1)^2`.
   For odd `n=2q+1`,
   `1+T_n=(1+x)(U_q-U_(q-1))^2` and
   `1-T_n=(1-x)(U_q+U_(q-1))^2`, with `U_(-1)=0`.
   Substituting
   `1+-x=((1+-x)^2+(1-x^2))/2` gives total certificate degree
   `2 ceil(n/2)`. The parity product identity (19) has the correct factor
   `2^(1-k)`. Products of the univariate certificates remain in the full
   preordering because the generators concern distinct coordinates.

3. **Degree reserve and commutator.** The source kernel certificate has
   square degree at most `k(m-1)-|I|<=r-1-|I|`. This permits the affine
   recourse localizers and the augmented source moment matrix on
   `(1,u,y)`. Multiplication by one source coordinate gives output
   frequencies at most `2m-1` in one coordinate and `2m-2` in the others.
   Therefore
   `sum_i ceil(alpha_i/2)<=k(m-1)+1<=r` for every nonzero commutator
   coefficient. The estimate is valid even when its total degree exceeds
   `r`. A coefficient of the original multiplier with frequency outside
   the kernel support may contribute through its immediately adjacent
   frequency; formulas (20)--(21) include that case. Frequencies farther
   outside the support vanish. The absolute convergence assumption
   justifies exchanging each finite kernel expansion with the series.

4. **Coefficient estimate.** For `k>=1`, the two commutator coefficients
   have absolute sum bounded by
   `((2k+1)+(2k-1))(1-g_1)/2=2k(1-g_1)`.
   For `k=0`, the coefficient is `(1-g_1)T_1`.
   Tensor factors from the remaining coordinates have absolute value at
   most one. Thus the directional weight `max(1,2 alpha_i)` in (8) is
   sufficient; no additional weights in the other directions are missing.

5. **Coordinatewise Hölder estimate.** Kernel normalization removes all
   other coordinates from each scalar summand. Independently expanding
   `int K(x,v)(x-v)^2 dmu(v)` gives
   `(1-g_2)/2+(1+g_2-2g_1)x^2`.
   The kernel identities reduce these coefficients to `V_m` and
   `(3-2m)/a_0`, respectively. The latter is negative for every admitted
   `m>=2`. The Hölder correction is bounded in absolute value by
   `H int K |x-v|^(1+beta)`, and Jensen's inequality gives the displayed
   power of `V_m`. Crucially, `epsilon_i-R_i` is a univariate polynomial
   of degree at most `2m-1`; its interval certificate needs degree at most
   `2m<=2r`. This transfers the pointwise estimate to the truncated
   functional and does not assume a representing measure.

6. **Matrix cost, zero densities, and selection.** The matrix cost
   estimate uses `d<=r`, unlike the larger commutator degree allowance.
   The private square bounds and reserved source square bounds force all
   entries of the conditional moment matrix to vanish where `h=0`.
   Hoffman continuity applies because the constraint matrix, including
   the box rows, is fixed and every fiber is nonempty. The strongly
   convex regularized minimizer is continuous on the compact parameter
   box; as its coefficient decreases to zero it converges to the unique
   minimum-norm unregularized minimizer. This proves the claimed Borel
   selection. It does not require selecting the same optimizer that was
   used to exhibit regular KKT projections. The shared laws glue using
   their exact separator marginals. No hidden strong-duality premise is
   used in the gap argument.

7. **Sharp example and scope.** For `x,z in [0,1]`, the two conditional
   minima are exactly `-u_+^2` and `u_+^2`. Writing `z>=u` as `-z<=-u`
   shows that multiplier `2u_+` produces projection `-2u_+`, with the
   sign and Lipschitz constant stated in the note. It is a valid choice
   also at `u=0` and the endpoints. Affine scaling of the private variables
   preserves private degree two and maps the example into the stated
   box model. The lower-bound witnesses are actual local measures and
   therefore satisfy every rectangular matrix constraint. Their common
   moments through `2r` meet exactly the required separator conditions.
   This proves the claimed order, without requiring the relaxation value
   to equal the ideal exact-local-measure value at each finite order.
   The subsequently added explicit bound (27a) also checks independently:
   the only nonconstant matrix coefficient after scaling is
   `[[-1,-1/2],[-1/2,0]]`, giving `A=2`; the projected multiplier has
   `M=H=2`, so Theorem 2 gives `12/(2r^2+1)+2V_r`, which is strictly
   smaller than `24/(2r^2+1)<12/r^2` because `V_r<6/(2r^2+1)`.

## Limitations checked

- The full shared-box preordering is used in Lemma 3 and the conditional
  kernel construction. The proof cannot be read as an ordinary-module
  theorem at the same private degree.
- Coordinatewise dependence is a substantive restriction for bags with
  more than one shared coordinate. The scalar-network caveat in the note
  is accurate: when every shared bag has size at most one and private
  blocks are disjoint, the objective and feasible set separate across
  distinct shared coordinates. Distinct coordinate groups can meet only
  across empty separators. Larger bags under Theorem 2 can still contain
  arbitrary coupled polynomial master terms, because those terms do not
  enter private KKT stationarity.
- Constant positive-definite private Hessians and Lipschitz primal
  solutions do not guarantee regular projected multipliers. Example
  (29) correctly separates those assumptions. Conversely, LICQ is only
  a sufficient route to regularity, and the sharp example need not meet
  LICQ at all points.
- Neither small numerical constants, a way to compute the regularity
  bounds efficiently, nor numerical SDP complexity follows from the
  convergence theorem. Publication priority is outside this proof review;
  the separate prior-work audit is needed for that assessment.

## Targeted independent numerical challenge

Ran exactly:

```sh
python3 -B research-20260928/solver/check_active_region_sdp_review.py
```

The checker independently assembles the two rectangular moment SDPs for
the sharp example after `x=(1+v)/2`, `z=(1+w)/2`. It includes the full
shared preordering, private square bounds, the affine row `z>=u` with its
reserved degree, and all separator moments through `2r`. It passed 4,165
exact rational comparisons of assembled Dirac matrix entries against
their independent rank-one formulas at feasible optimal points.

CVXPY 1.9.3 with CLARABEL produced:

| Shared order `r` | Numerical objective | Smallest PSD eigenvalue | Largest equality residual |
| --- | ---: | ---: | ---: |
| 2 | -0.0369846834 | -2.98e-10 | 5.49e-12 |
| 3 | -0.0106354741 | -2.15e-9 | 6.94e-17 |
| 4 | -0.0055493930 | -1.78e-9 | 2.36e-16 |

All three solver statuses were `optimal_inaccurate`. These values are
consistent with the positive finite-order gaps and the proved bounds,
but are not rigorous upper or lower certificates and do not establish an
asymptotic rate. The numerical experiment is complementary to the proof
audit and the author's exact algebra checker. No project-wide checks or
CI inspection were performed.
