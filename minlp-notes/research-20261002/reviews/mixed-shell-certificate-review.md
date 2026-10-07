# Independent review of the physical mixed-box shell certificate

Date: 2026-10-02. Verdict: **PASS**. The final integrated
[mixed-shell theorem](../new-direction/mixed-shell-certificate.md)
has no substantive gap in the reviewed argument. This review freshly read
its physical shell grids, the unified inner-region completion, the
nonpositive-diagonal branch, and the final arithmetic statement.

The reviewer authored the earlier signed normalized continuous certificate
but did not author this physical mixed-shell theorem. The review does not
transfer the earlier metric or radial assumptions to integer coordinates.
The new theorem avoids both side-normalization distortion and inflation
of the curvature scale by linear endpoint values.

## Feasible lattice rounding and the shell flag

After shifting by the feasible proposed point, every lattice displacement
is an integer multiple of its original spacing. The initial positive grid
point and every subsequent point have that property. Clipping the upper
side bound to the last feasible lattice label and inserting
\(h_i\lceil S/h_i\rceil\) also preserve feasibility.

For a feasible lattice target inside one grid interval, a gap of exactly
one lattice step contributes zero rounding variance: the target must be
an endpoint. This observation is necessary; treating such a gap as an
arbitrary continuous interval would introduce an unwanted lattice-spacing
term. If the initial gap has at least two steps, the ceiling estimate
bounds its length by \(\delta S/n\). Every subsequent nonunit gap
is at most \(\delta a\), where \(a\) is the smaller absolute label.
Threshold insertion can only shorten those intervals.

The resulting variance inequality is valid for every coordinate:

\[
 4\operatorname{Var}(Y_i)
 \le\delta^2\mathbb E(Y_i-s_i)^2+\delta^2 S^2/n^2.
\]

The inserted threshold matters independently of variance. If a target
coordinate witnesses \(|x_i-s_i|\ge S\), all its rounded outcomes
still satisfy that inequality. For a lattice coordinate this uses the
ceiling threshold rather than the possibly infeasible value \(S\).
Negative displacements are reflected, so the same statement holds on
both sides. Independent coordinate rounding therefore produces only
feasible points in the shell-constrained DP domain.

Linear and cross-term expectations are exact. The only objective error
is diagonal variance, bounded above using \(A_{ii}-\sigma\le L/2\).
Thus the correction \(2\sigma\|y-s\|^2\) and root threshold
\(\sigma S^2/n\) have the stated signs and constants. Every successful
shell inequality certifies a lower bound on the continuous or mixed
shell, without assuming optimality or growth.

## The innermost region changes no lattice coordinate

The chosen positive rational radius is at most half of every lattice
spacing and at most every available positive continuous side distance.
Consequently any feasible displacement of infinity norm below this radius
has all lattice coordinates zero. Scaling only its continuous coordinates
out to exactly the bottom radius remains feasible: their absolute values
are at most that radius on the same available signs.

The continuous first-order checks imply a nonnegative linear term on
this ray. For a scaling factor \(t\in[0,1]\), quadratic expansion
therefore gives

\[
 F(s+tv)-F(s)\ge t^2[F(s+v)-F(s)].
\]

This extends the bottom shell's certified physical Euclidean margin to
the entire inner region. No integer derivative check or scaling of a
nonzero integer displacement is used. The construction covers pure
continuous and pure lattice cases as well as mixed boxes; no normalized
metric or separately supplied slice certificate remains in the final
version.

For a unique global minimum, the feasible region outside the bottom
radius is compact, excludes the proposed point, and has a positive
attained objective gap. Its bounded diameter gives positive Euclidean
growth there. The same inner-region argument extends growth inward.
Thus uniqueness implies a positive full-domain modulus in this setting,
and suffices for positive-branch termination. A finite failed trial is
still inconclusive in the general nonunique or incorrect case.

## The preserved curvature scale and discovery bound are correct

The proof needs only a supplied positive \(L\) with \(A_{ii}\le L/2\),
not a bound on linear coefficients, endpoint values, or off-diagonal
coefficients. The input length now explicitly includes this supplied
number.

All shell inequalities succeed when \(\sigma\le g/3\), since shell
points have squared distance at least \(S^2\). Success at the initial
trial returns \(L/32\); later first success returns more than
\(g/12\) because the preceding margin was four times larger. Combining
this with global soundness gives

\[
 0<\sigma\le g,\qquad
 \sigma\ge\min\{L/32,g/12\},\qquad
 L/\sigma\le\max\{32,12L/g\}.
\]

The minimum is essential when linear growth makes \(g\) much larger
than curvature. Requiring a constant-factor approximation of such a
\(g\) would unnecessarily enlarge the scale. The manuscript's
\(H(x+y-2xy)+\varepsilon(x^2+y^2)\) example correctly shows that
an endpoint-based scale can instead be much larger than curvature even
when \(g=\varepsilon\). The physical theorem does not make that
replacement.

## Nonpositive diagonals have a complete endpoint certificate

When every \(A_{ii}\le0\), coordinate concavity prevents a unique
minimum at an interior value of any unfixed coordinate. Holding the
others fixed, one feasible endpoint has no larger value. This argument
also holds on a finite lattice interval.

For a proposed product endpoint, the Boolean flag for an endpoint
assignment different from the proposal computes the exact other-endpoint
gap \(\Delta\). If it is positive, independent mean-preserving
endpoint rounding gives

\[
 F(x)-F(s)\ge\Delta\Pr(Y\ne s)
 \ge\frac{\Delta}{\sum_iw_i^2}\|x-s\|^2.
\]

The inequality uses \(t_i^2\le\max_jt_j\) for the endpoint mixture
probabilities \(t_i\in[0,1]\). Every rounded endpoint is lattice
feasible where required. Nonpositive \(\Delta\) gives a direct witness
against unique optimality. Hence this branch needs neither an artificial
positive curvature nor a growth search and has ordinary endpoint-DP
complexity. The manuscript appropriately identifies this as a classical
case, not a separate novelty claim.

## Grid size, shared shell index, and rational bits

On a continuous side the initial scale restricts the ratio traversed by
geometric labels to \(4n/\delta\). On a lattice side there are only
\(O(1/\delta)\) unit-sized increments below \(2h_i/\delta\), and
subsequent increments grow labels by a factor at least \(1+\delta/2\).
Unless the initial node is already clipped to the endpoint, it is at
least \(\delta S/(2n)\), giving the same ratio bound. The clipped
case has only the endpoint and possibly the inserted threshold.

Thus coordinate-state counts are independent of shell radius, box aspect
ratio, and lattice spacing. The number of shells is instead
\(O(1+\log(D/r_0))\), polynomial in input length. Each shell has its
own DP, or a single globally shared shell index. No shell index is chosen
independently for each variable; the cost is a sum of shell costs and
does not raise the number of shells to the bag size.

The owned-variable OR flag and sequential child convolutions preserve
ordinary treewidth complexity, including arbitrarily many occurrences
of a variable. Powers of the logarithmic grid-size dependence on \(n\)
can be absorbed into a parameter-dependent factor times an absolute
power of \(n\), as in the homogeneous predecessor.

Shell radii, lattice labels, and clipped endpoints have polynomial bit
length. Continuous labels add the usual \(rK\) geometric-grid bits.
The final common-denominator argument explicitly includes the input
lattice spacings and computed bottom radius; floors and ceilings create
integer multipliers, not new denominators. Factor-once message sums avoid
multiplying denominators along the decomposition. The claimed
\(f(p,L/g)\operatorname{poly}(I)\) bit bound has an absolute input
exponent. It does not claim an arithmetic shell count independent of
coefficient height or encoded widths.

## Distinct targeted checks

The reviewer ran

```sh
python research-20261002/reviews/check_mixed_shell_review.py
```

The [independent diagnostic](check_mixed_shell_review.py) passed 47 full
shell DPs, each matched against direct grid enumeration. These include:

- Forty-one physical shells for \(x^2\) on an asymmetric interval with
  side ratio \(2^{40}\); the largest coordinate grid had only 14 labels
  and every shell passed the initial trial.
- Mixed binary/continuous versions of the endpoint-scale counterexample,
  including coefficient \(H=2^{200}\), while retaining \(L=2\).
- A coupled star decomposition with an interior integer candidate and
  two-sided continuous coordinates, testing owner flags and child messages.

Two further fixtures remove the inserted lattice threshold and show that
shell preservation then fails, for native and rational lattice spacings.
The same diagnostic passed 162 exact growth checks for the zero-curvature
endpoint branch. These checks add full-DP composition and scale tests to
the author's separate scalar-variance and small-shell diagnostics; the
author's command was not duplicated.

The diagnostics are exact rational fixtures, not a proof of asymptotic
complexity or a production certificate generator. No project-wide checks,
CI inspection, or external literature search were performed for this
review.
