# Independent final audit of the exactly consistent sparse Putinar transfer

Date: 2026-09-28. This audit independently reconstructs the proof in
[sparse-putinar-exact-consistency.md](sparse-putinar-exact-consistency.md)
and the kernel and duality lemmas it uses from
[sparse-putinar-kernel.md](sparse-putinar-kernel.md). It did not use the
earlier reviewers' conclusions as premises. A separate fresh reviewer
checked only the final parameter choice and its conversion to moment order.

No substantive proof defect was found. Under the stated box, ordinary
quadratic-module, total-degree, moment-consistency, and running-intersection
assumptions, the finite error bound is justified. The rate is uniform in
the number and arrangement of bags after dividing by the displayed local
Chebyshev coefficient budget. This finding is evidence from a proof audit,
not a machine-checked theorem or a conclusion about publication priority.

The following points are the main adversarial checks.

1. **Ordinary-module positivity is used only where it is available.**
   For fixed output coordinates, every source factor `Q` is globally SOS.
   A product of such factors is SOS. A single residual `r=1-n` is only
   interval nonnegative; its interval SOS representation has degree at
   most `D`. Multiplying that representation by other globally SOS factors
   uses one box generator per term, so the expansion terms with zero or
   one residual are ordinary-module nonnegative. Terms with two or more
   residuals are not assumed nonnegative. This distinction is essential.

2. **The residual-product estimate has sufficient degree.**
   For `G=prod Q` on the `v-j` complementary coordinates and
   `H=prod r` on `j` coordinates, each term certifying
   `G(delta^(2j)-H^2)` has degree at most `(v+j)D<=2R`.
   The certificate follows by telescoping `delta^2-r_i^2`, whose interval
   representation has degree at most `2D`. All remaining factors are
   SOS, including preceding residual squares. Thus no hidden product of
   distinct interval generators occurs.

   Write `G=sum_l q_l^2`. Every square in
   `G(a+bH)^2=sum_l(q_l(a+bH))^2` has squared degree at most
   `(v+j)D<=2R`. Positivity for all real `a,b` makes the associated
   two-by-two matrix positive semidefinite. Consequently

   \[
   |L(GH)|^2\le L(G)L(GH^2)\le\delta^{2j}L(G)^2.
   \]

   This remains valid when `L(G)=0`; no conditional density or positive
   denominator is needed. The proof really uses the full order `2R`.

3. **Coefficient evaluation uses the smaller, justified degree range.**
   The identity for `1-T_alpha^2` in the companion note is an ordinary
   module certificate through degree `2|alpha|`. Moment Cauchy–Schwarz
   then gives `|L(T_alpha)|<=1` for `|alpha|<=R`.
   In particular, `deg G<=(v-j)D<=R` gives
   `0<=L(G)<=B^(v-j)`. The bound
   `||Q(.,y)||_(1,cheb)<=s^2(N+1)/C_s` follows from the exact coefficient
   norm of the source geometric residual and Chebyshev submultiplicativity.
   It does not require bounding arbitrary degree-`2R` Chebyshev moments.

   For the objective calculation, both the transformed polynomial and
   the original objective have degree at most `vD<=R`: indeed
   `deg f_b<=v d_infty<=v s<=vD`, since `s>=2` and `N>=2`.
   This supplies the degree detail implicit in the author's text.

4. **The density correction preserves every required marginal.**
   Exact polynomial normalization of `Qbar=Q+r` gives signed bag densities
   of mass one whose separator marginals agree. Source degree is at most
   `vD`, so the given moment agreement is sufficient. Their common lower
   bound follows by summing the estimates in item 2. For `B>=1`,
   `Delta_v` is nondecreasing in `v`; one direct recurrence is

   \[
   \Delta_{v+1}=(B+\delta)\Delta_v+vB^{v-1}\delta^2.
   \]

   Adding the same `Delta_w` times the product-arcsine reference density
   and dividing by `1+Delta_w` preserves exact separator agreement even
   for bags of different sizes. It gives nonnegative probability laws.
   Standard tree gluing then applies, including where a separator density
   vanishes. Empty separators also cause no problem.

   The argument depends on a common shift, a consistent product reference
   family, and running intersection. Different bagwise shifts need not
   preserve consistency. Pairwise-consistent marginals on a cyclic
   hypergraph need not have a global extension.

5. **The objective bound does not apply probability inequalities to a
   signed law.** The operator `Abar` fixes constants and has the same
   action as `A` on positive Chebyshev degrees. Tensor telescoping gives
   the claimed coefficient error. For the correction, the exact identity

   \[
   \int f_b h_b^+\,d\mu-\int f_b\bar h_b\,d\mu
   =\Delta_w\left(\int f_b\,d\mu-\int f_bh_b^+\,d\mu\right)
   \]

   compares two probability laws on the right. Its bound is therefore
   `Delta_w osc(f_b)`. Summing introduces `W<=2C_f`, with no edge count
   or tree diameter. Local additive constants cancel exactly.

6. **The sparse polynomial certificate follows from finite SDP duality.**
   Product-arcsine moments make every permitted nonzero square, and every
   permitted square times `1-x_i^2`, integrate strictly positively.
   They satisfy all separator equalities. Thus the primal finite SDP has
   a point with all PSD blocks positive definite; redundant equality
   constraints do not invalidate this Slater condition. The objective is
   bounded using item 3. The attained finite dual therefore supplies local
   SOS identities whose separator polynomials cancel on summation.
   Adding the nonnegative scalar between the actual gap and the error
   bound proves the stated membership for `f-f*+E`.

   This is real-coefficient certificate existence. It is not attainment
   of a finite polynomial separator dual for the infinite moment problem,
   and by itself gives no rational output or bit-complexity guarantee.

The final, smaller parameter choice also survives independent derivation.
Put `kappa=max(3,(w+1)/2)`. Equation (15) gives

\[
\kappa\log_2s\le N<\kappa\log_2s+2,
\qquad\delta\le(2s^\kappa)^{-1}.
\]

For `w>=2`, Taylor's formula with nonnegative coefficients gives

\[
\Delta_w\le {w\choose2}\delta^2(B+\delta)^{w-2}
=O_w\!\left(
 {\log^{w-2}s\over s^{\max(6,w+1)-w+2}}
\right).
\]

The denominator exponent is `6,5,4,3,3,...` for `w=2,3,4,5,6,...`.
It is therefore at least three, so this is
`o_w(log(s)/s^2)` for each fixed width. For `w=1`, the correction vanishes.
Increasing `N` does not invalidate the companion estimate for `eta`:
with `M=N+1`, `D+1<=2sM` and `delta<=1/(2s^3)` imply

\[
\sqrt{2(D+1)}\delta\le {\sqrt M\over s^{5/2}}
\le {M\over s^2}.
\]

Thus `eta<=(3d_infty^2+1)(N+1)/s^2` still holds. Once `w eta<=1`,
the tensor error is at most `e w eta`.

For an explicit choice that works at every sufficiently large order, use

\[
s=\left\lfloor{R\over2w(\kappa+3)\log_2(R+2)}\right\rfloor
\]

and then equation (15). When `s>=2`,
`wD<=2ws(kappa+3)log_2(s)<=R`. Eventually `s>=d_infty` and `w eta<=1`
also hold. This proves the claimed
`C_f O_(w,d_infty)(log^3(R)/R^2)` rate without an order subsequence.
The constants and threshold can depend strongly on width; the theorem
does not assert uniformity when width grows.

There is an elementary reason why the normalization issue is real.
Suppose `K(x,y)` is a polynomial, `K(.,y)` is globally nonnegative on the
real source line for every `y` in the reference interval, the reference
probability measure has full support, and `int K(x,y)dmu(y)=1`
identically in `x`. Then `K` is independent of `x` on that interval.
If its highest nonzero source coefficient is `a_m(y)`, a globally
nonnegative polynomial forces `m` even and `a_m(y)>=0`. Normalization
forces `int a_m dmu=0`. Continuity and full support force `a_m=0`
throughout the interval, contradicting the choice of `m`. Iteration
removes every positive source degree. In particular, a useful polynomial
kernel cannot simultaneously be globally SOS in the source and exactly
normalized. This observation explains the role of the signed correction;
it is not asserted to be a new lemma.

The source comparison is favorable but does not establish novelty.
This audit directly opened the following primary texts on 2026-09-28:

- [Gribling–de Klerk–Vera, arXiv:2605.31496v1](https://arxiv.org/html/2605.31496v1),
  especially Sections 3–4: the squared kernel, geometric SOS multiplier,
  dense `log^3(R)/R^2` rate, and coefficient method are prior. Its
  theorem is a dense statement. The present addition is the overlapping
  bag transfer with exactly consistent corrected laws, and the resulting
  uniformity after normalization by `C_f`.
- [Korda–Magron–Ríos-Zertuche, published Theorem 8](https://link.springer.com/article/10.1007/s10107-024-02071-6):
  equation (5), with local Lojasiewicz exponent one, has epsilon exponent
  `2+(5/3)(w+4)(11/3)=(238+55w)/9`. Its degree-squared bound therefore
  gives the slower exponent `18/(238+55w)` for fixed data. Equation (6)
  has epsilon exponent `26/3` and does not dominate that requirement.
  The earlier theorem handles broader constrained domains; the new box
  theorem does not subsume that scope.
- [Gamertsfelder–Mourrain, arXiv:2501.09385v4](https://arxiv.org/html/2501.09385v4),
  equation (3), Assumption 9, and Theorem 13: the dual uses finitely
  supported multipliers and assumes attainment. It can transfer a local
  rate under that assumption. The present argument establishes the box
  rate without requiring a polynomial separator optimizer.

Searches combining sparse Putinar or quadratic-module convergence with
squared kernels and normalization did not locate an equivalent theorem.
That small search is not a citation census. The earlier public assertions
of a sparse **preordering** inverse-square rate, retained and analyzed in
[sparse-putinar-prior.md](sparse-putinar-prior.md), prevent any broad claim
of the first second-order sparse rate. This audit did not independently
rerender those slides. The prior audit's passages about an additional
tree-size term describe the companion approximate-consistency theorem;
they should be updated when summarizing this stronger variant.

The mathematical solver implication is a degree guarantee for the ordinary
sparse box hierarchy with `v+1` local PSD block types, normalized by the
total local coefficient norm. It permits arbitrarily many bounded-width
bags without an additional deterioration of this normalized degree bound.
The number of blocks still grows with the number of bags. No practical
runtime improvement, numerically stable extraction, preservation of hard
constraints or integrality, or small rational certificate follows from
this proof alone.

The explicit bounds are conservative. The targeted calibration script
[calibrate_sparse_putinar_bound.py](calibrate_sparse_putinar_bound.py)
evaluates the formula with `d_infty=2`, choosing the largest admissible
`s` for the prescribed `N` in equation (15):

| Width | Moment order R | s | N | Approximate E/C_f |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 10,000 | 109 | 22 | 0.03539 |
| 5 | 10,000 | 53 | 18 | 0.59993 |
| 10 | 100,000 | 122 | 40 | 186,872,642 |

These are evaluations of a worst-case formula, not observed relaxation
gaps. The asymptotic prescription is not optimized for finite orders:
at width ten and order 100,000, the also admissible `s=82,N=60` gives
approximately `1.20563`. The large prescribed bound therefore diagnoses
its constants, not an intrinsic limitation of every admissible parameter
choice. Decimal values are approximate and are not directed-rounding
certificates.

Targeted commands actually run in this audit:

```text
python3 -B research-20260928/solver/check_signed_density_review.py
python3 -B research-20260928/solver/check_sparse_putinar_fresh_review.py
python3 -B research-20260928/solver/calibrate_sparse_putinar_bound.py
```

The first passed its exact residual identities, degree ledgers, common-shift
identities, ordinary-module obstruction, and 256 finite parameter cases.
The second passed 52 kernel identities, 24 SOS/normalization cases, and
156 coefficient-error cases. The third computed the displayed calibration
and checked parameter admissibility exactly. These finite computations
support the algebra; they cannot establish positivity for all truncated
functionals, all-degree certificates, or arbitrary trees. Those conclusions
depend on the proof and its stated standard theorems. No Lean proof,
project-wide verification, or CI inspection was performed for this audit.
