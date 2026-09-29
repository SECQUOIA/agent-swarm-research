# Independent review of the quantitative star moment obstruction

Date: 2026-09-25.

Status: accepted as a theorem for the specified subsetwise relaxation,
including the completed rational refinement. The proof gives additive and
relative gaps of order at least `k^-2` with uniform spectral bounds and
bounded means and costs. This review does not establish publication novelty.

## Scope and conclusion

I independently checked [the quantitative note](star-subset-accuracy-lower.md),
its square-completion transfer, and the relevant geometry in the
[uniform-conditioning construction](star-uniform-condition-subset-gaps.md).
The real-data theorem and the rational refinement are correct as stated.
No substantive correction to either theorem was needed.

The quantifiers matter. For every order `k`, the construction has `2k`
leaves. Every subset of at most `k` leaves has its own joint pattern
matrices. All subsets share the center matrix and the individual leaf
matrices, but they do not share higher-order pattern marginals on their
intersections. The result concerns exactly that relaxation. It proves
neither a lower bound for every moment hierarchy nor a lower bound for
arbitrary conic formulations or optimization algorithms on stars.

The rational refinement is now complete in the quantitative note. Its
gap bound is `1/(466560 k^2)`, its relative gap bound is
`1/(56920320 k^2)`, and the total nonzero-data encoding length is
`O(k^2 log(k+1))`. These assertions go beyond the earlier rational
construction, which only treated compatibility on every proper subset.

## Geometry and local realizability

For the real construction, the perimeter of a selected set with span
`s` and `m` directions is

\[
 4\left[\sum_{j=1}^{m-1}\sin(d_j/2)+\cos(s/2)\right].
\]

Concavity bounds its first term by equal angular gaps. The resulting
expression increases with the span for `s <= pi/6`, and increases with
the number of selected directions. This proves the displayed bound
`U_k` for every subset of size at most `k`, not just consecutive subsets.
For `f(u)=u sin(beta/u)`, the integral identity

\[
 f'(u)=\int_0^{\beta/u}t\sin t\,dt
 \ge\frac{\beta^2\sin\beta}{3u^3}
\]

is valid because `u>=1` and sine is concave on `[0,beta]`. Integrating
from `k-1` to `2k-1` gives the note's lower bound for `k>=2`. The
separate `k=1` calculation is correct; applying the derivative argument
there would have been invalid. The displayed asymptotic constant also
follows from the cubic term in the sine expansion. It describes the
certificate, not an upper bound on the actual optimization gap.

The prior planar compatibility criterion is used correctly. Strict
perimeter slack permits a slightly larger noise parameter `eta'` that
is still compatible. Mixing that parent with the uniform parent
`2^{-|J|} I` makes every pattern matrix positive definite at `eta`.
Every resulting matrix has positive mass and is the moment matrix of a
finite scalar measure with at most two atoms. Thus the local witnesses
are actual scalar laws. The argument does not mistake the closure of a
moment cone for exact realizability.

For the rational refinement, consecutive short-arc gaps are at least
`g=1/[9(N-1)]`: apply the derivative bound for `4 arctan(t)` on
`[-1/64,1/64]` to its rational grid spacing. The long gaps satisfy the
same lower bound. Deletion can only increase surviving gaps. At a
deleted vertex, the neighboring gaps `A,B` have `A+B<=pi` while at
least two opposite vertex pairs remain. The loss upon deleting one
opposite pair is exactly

\[
 16\sin(A/4)\sin(B/4)\sin((A+B)/4)
 \ge\frac{AB(A+B)}{32}
 \ge\frac{g^3}{16}
 =\frac1{11664(N-1)^3}.
\]

The lower bound uses `sin(t)>=t/2` on `[0,pi/4]`. It remains valid
for the deletion from two opposite pairs to a segment, with perimeter
convention four. Removing at least `k` pairs from `N=2k` therefore
proves the bound `U=P-k ell` for every required subset. Since any
nonempty selected symmetric polygon contains a unit diameter, its
perimeter is at least four, so `U>=4`. This justifies every denominator
and the strict compatibility margin in the rational construction.

Finally, `U<P<5` gives

\[
 \Delta=\frac{k\ell}{U}
 >\frac{k}{58320(2k-1)^3}
 >\frac1{466560k^2}.
\]

The weak inequality used in the theorem is consequently safe, including
`k=1`. The rational change of noise parameter preserves the polynomial
encoding estimate; no enumeration of subsets is needed to construct it.

## Original epigraph separation and closure

The important transfer is the affine cut in the original variables.
It prevents the incompatibility witness from proving only a gap in
auxiliary matrices. A useful general form includes both constructions.
Let `w_i=b_i^2/d_i`, `W=sum w_i`, `C=sum c_i`,
`a=1+W/2`, and `gamma=1-W/2`. The cut is

\[
 t+CX+\sum_i\frac{2d_i c_i}{b_i}Y_i
 +\sum_i\left(w_i+\frac{c_i^2}{w_i}\right)Z_i
 +\gamma\ge0.
\]

For an active support `S`, its left side at the quadratic cost is

\[
 \sum_{i\in S}d_i
 \left(Y_i+\frac{b_i}{d_i}X+\frac{c_i}{b_i}\right)^2
 +\frac{(2+h_z)X^2-2h_xX+2-h_z}{2},
\]

where `(h_x,h_z)=sum_i (2Z_i-1)(c_i,-w_i)`. The signed-sum norm
bound gives `h_x^2+h_z^2<=4`, so the final scalar quadratic is
nonnegative. This proves validity on every original feasible point,
even when its center indicator is zero. Affine continuity then proves
validity on the closed convex hull without any assumption about closure
of a lifted projection.

Substituting the prescribed means and candidate cost gives exactly
`2-eta P/2=-Delta`. The coefficient of `t` is one, so the true hull
cost exceeds the candidate relaxed cost by at least `Delta`. A separate
global realization of the candidate moments is neither available nor
needed. The candidate's local laws establish its relaxed feasibility.

## Uniform bounds and relative error

For the real matrix, the two nontrivial eigenvalues have trace below
three and determinant `gamma=1-sqrt(3)/2>1/8`. Thus the lower spectral
bound `1/24` and upper bound three are valid uniformly in `k`.
The rotated gradient angle interval gives
`|c_i|/w_i<=cot(pi/24)`. The rotated directions give the stated
leaf activity interval. These imply the stated bounded mean norm.

For both constructions the candidate cost is

\[
 F^*=a+\sum_i z_i c_i^2/w_i-\sum_i w_i r_i^*\ge a-W>0.
\]

The true hull cost has a finite upper bound from the law with `X=0`,
independent activity indicators, and active values `y_i/z_i`. Its cost
is `sum_i d_i y_i^2/z_i`. The PSD inequality
`(s_i^*)^2/z_i<=r_i^*<=1` and the bounds on `c_i/w_i` give precisely
the upper bounds in the note. Thus the denominator of the relative
gap is both positive and bounded independently of `k`.

For the rational normalization, the gradient has positive first
coordinate and slope `|t|<sqrt(3)<7/4`. Consequently

\[
 \frac{|c_i|}{w_i}
 =\frac{|5+12t|}{12-5t}<8.
\]

Also the rotated point coordinate is at least `-197/208` and negative,
so `11/416<=z_i<1/2`. The dyadic choice gives `b_i^2>=w_i`, hence
`|y_i|<=9 sqrt(w_i)/2`. Summing proves `||y||^2<=486/13`.
The true cost is at most `66 W=1584/13<122`. Multiplying 122 by
466560 gives exactly 56920320, the stated relative-gap denominator.
The normalized rational arrow matrix and its diagonal congruence give
the spectral bounds `1/39` and 12 as claimed.

For any feasible relaxed tuple, singleton compatibility gives
`0<=r_i<=v`. Every square term in the objective is nonnegative, so
the relaxed cost is at least `(a-W)v>=0`. This justifies the full
ordering of costs in the theorem. The result is a necessary order
bound `Omega(epsilon^-1/2)` for a uniform relative-error guarantee by
this relaxation. It is not a matching convergence theorem.

## Verification and remaining limitations

I wrote and ran:

```text
python research-20260925/check_star_subset_accuracy_review.py
```

It passed exact symbolic cut identities on all eight supports of a
generic three-leaf star with arbitrary positive leaf diagonals, and the
generic candidate-cut identity. These symbolic checks verify algebraic
identities, not the geometric norm inequality or the all-order theorem.
It also checked 4,706 subsets for real-family orders `k=1,...,7` in
floating point. Those finite checks support the perimeter formulas and
constants but do not certify inequalities for all `k`.

I inspected and independently ran the author's exact rational checker:

```text
python research-20260925/check_star_subset_accuracy.py
```

It passed five instances (`k=1,...,5`), 852 exact subpolygon checks,
and the gap, mean, and cost bounds using `Fraction` arithmetic. This
checks finite cases and the implementation of the construction. The
general deletion argument above proves the all-order rational assertion.
No project-wide checks or CI inspection were performed.

This review used the self-contained mathematical arguments and local
literature comparisons; it did not conduct a new independent literature
search. The note correctly qualifies novelty. Prior compatibility theory
and planar polygon approximation supply essential ingredients, and the
strongest quantitative comparison with existing optimization hierarchies
remains unestablished. The result's useful content is their simultaneous
realization as a rational, uniformly conditioned star epigraph gap with
bounded original means and true cost. It supplies a concrete limitation
of the stated formulation, rather than a solver performance claim.
