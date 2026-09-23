# Independent review: spectral bounds and complete parametric dictionaries

Date: 2026-09-22. Reviewer: `review_spectral_parametric_oracle`.

Reviewed source: [Exact smoothed message construction from additive approximation oracles](research-20260922-oracle-all-messages.md).

**Verdict.** The complete-message theorem is correct under its stated assumptions. I found no substantive mathematical correction. The proof supplies the conditional bounds, restricted approximation oracle, enumeration procedure, and bit bounds needed for the claimed algorithm; a bound on the expected representation size alone would not suffice. The polynomial dependence on numerical spectral and coefficient bounds, fixed treewidth, bounded prescribed parameter domain, and supplied polynomial-size decomposition are essential qualifications. This review does not establish priority or practical efficiency.

## 1. Conditional spectral bounds

The conditional problem uses the principal matrix `Q_AA` and the shifted linear coefficient `c_A+2Q_AS t`. Principal submatrices retain lower spectral bound `mu`; coordinate restriction also gives `||Q_AS||_2<=H`. Thus

```
||x_A(t)||_2 <= (C sqrt(n)+2H sqrt(k) R)/(2mu)
             <= (nC+2HkR)/(2mu)=M.
```

The last bound is rational and uniform over supports, boundary points, and fixed-bit restrictions. It is valid also when the active support is empty. For positive integer `n,k`, the replacements `sqrt(n)<=n` and `sqrt(k)<=k` have the required direction; when `k=0` the boundary contribution vanishes. Differentiating the full Schur-complement value gives `gradient q_A(t)=2Q_SA x_A(t)`, so `L=2HM` is valid on the entire box. Large deterministic penalties affect offsets but not this derivative.

Using only a root-problem coordinate bound would be incorrect. For example, with `Q=[[1,1/2],[1/2,1]]`, zero linear coefficients, and second coordinate prescribed as `t=2`, the first conditional optimizer is `-1`; the zero-linear-term root optimizer is zero. The reviewed source includes the required boundary term and does not make this substitution.

The formula is for an unconstrained continuous optimizer on its selected support. No bounds on intermediate recursively computed messages are being assumed. Computing each requested dictionary directly is precisely what makes this sufficient.

## 2. Restricted grid oracle

Every fixed indicator assignment permits zero continuous coordinates. An active bit does not force a nonzero coordinate. The oracle correctly retains an active zero state as well as the inactive zero state, with their different penalty costs.

For a true optimal support under any fixed-bit restrictions, round only its active coordinates. The exact support optimizer lies in the grid box by the preceding conditional bound. Stationarity on that support removes the first-order error, giving

```
grid value - exact support value = e'Q_II e
                                  <=H nM^2/B^2<=epsilon.
```

The optimal grid assignment cannot be worse than this rounded assignment. Reoptimizing continuously on the grid assignment's support can only improve its objective and preserves all fixed bits. Its exact continuous value is consequently within `epsilon` of the restricted optimum, with the correct one-sided feasible-value guarantee. This remains true when penalties are negative or when an optimal active coordinate equals zero.

The grid problem is a finite-domain pairwise graphical optimization problem on the induced internal graph. Restricting bags to internal vertices preserves width. Assigning every unary and edge cost exactly once gives an exact dynamic program. A child table can be minimized over variables outside its separator before being added to compatible parent states; a parent-child Cartesian product of full bag tables is unnecessary. The claimed `poly(n)(B+2)^(w+1)` operation bound is therefore justified for a polynomial-size supplied decomposition.

One may choose the smallest even positive integer satisfying the rational inequality for `B` using integer arithmetic. Its magnitude is polynomial in the stated numerical bounds and inverse accuracy. Its encoding length is polynomial in the input encoding length and the logarithm of those quantities. This does not give dependence polynomial only in the logarithm of `1/mu` or the coefficient magnitudes.

## 3. Enumeration, net coverage, and noise

I independently checked the strong Sauer induction. For projected families `A_0,A_1`, shattered sets of their union give shattered sets without the last coordinate, and shattered sets of their intersection give shattered sets with that coordinate. The collections are disjoint and induction gives `|A|<=|Sh(A)|`. Conditioning outside a fixed shattered coordinate set makes the zero-pattern and unit-pattern class minima deterministic. Shattering by near-optimal supports places each remaining noise coordinate in a fixed interval of length `2a`; independence is used only at this point. The resulting first-moment inequality is valid for arbitrary deterministic support costs and finite-grid ties.

The first-difference cells always partition precisely the unextracted supports. Cached oracle candidates remain valid within their unchanged cells. The fixed initial incumbent satisfies `v<=U<=v+epsilon`; consequently every extracted candidate is within `delta+2epsilon` of `v`. Conversely the certified lower bound of the cell containing a support of cost at most `v+delta` prevents stopping before that support is extracted. This is valid even if the oracle always chooses the worst permitted approximate candidate.

Every support optimal anywhere on the box is within `epsilon` of optimality at an appropriate net point. This includes supports optimal only on the boundary or at isolated ties. The Cartesian midpoint grid has the stated rational covering bound: its Euclidean covering radius is at most `sqrt(k)R/B<=kR/B`. Taking the union of extracted supports preserves exactness because every additional support is a valid full branch.

The choices `epsilon=delta=1/(12n phi)` and `N>=2n` give

```
2phi(3epsilon)+1/N <=1/n,
E|E_j|<=(1+1/n)^m<=e.
```

The noise vector is sampled once. The parameter net is deterministic, and the near-optimality inclusion for an adaptive enumeration is a pointwise statement about that complete vector. No argument conditions independent coordinates on an adaptive query history. Dependence between net points or overlapping subtree messages does not affect the expectation sum. A power-of-two grid needs exactly `log_2 N=O(log(n+1))` random bits per coordinate. Rare realizations with exponentially many exact ties remain correct and may take exponential time.

## 4. Output-sensitive work and exact arithmetic

There are at most `1+m|E_j|` oracle calls at one net point, including calls for child cells whose lower bounds later exceed the stopping threshold. This accounts for the fringe of the search, not just its extracted cells. The total number of generated cells is bounded by `1+m2^m`, so the heap's logarithmic overhead is `O(m+log(m+1))` per operation on every realization. Creating and storing partial assignments adds a deterministic polynomial factor. Tries deduplicate support strings in linear time in their length. These facts make a first-moment output bound sufficient; no hidden second-moment bound is needed.

Exact oracle values and full quadratic coefficients use rational principal-system solves. Determinant bounds give bit lengths polynomial in the original rational encoding length and dimension. Grid coordinates and deterministic net coordinates have polynomial bit length. A finite-domain table value sums only polynomially many rational local costs; taking minima does not create new denominators or algebraic numbers. Thus queue comparisons, Schur computations, and support-map recovery all have polynomial bit cost per operation under the theorem's numerical parameter dependence.

The algorithm outputs a minimum of full rational quadratics. It never needs to compute a multivariate envelope arrangement, its connected cells, or algebraic sample points. Avoiding these tasks is material to the proof, since their cost is not implied by the first-moment dictionary estimate.

## 5. All messages, boundary indicators, and the certificate

For a rooted decomposition edge, the running-intersection property ensures that the internal vertex set has no edge to vertices outside its union with the separator. Its contribution is therefore exactly the principal-submatrix conditional problem stated in the source. Boundary-only quadratic terms, linear terms, and penalties are excluded. Whether a separator bit is zero or one affects this internal minimization only by requiring its continuous coordinate to be zero in the former case. Restriction to the corresponding face is sufficient; the active-zero and inactive-zero distinction is subsequently handled by the excluded boundary penalty.

Computing each subtree dictionary independently avoids consistency requirements between separately enumerated supports. The separate empty-boundary call on all vertices supplies an exact global optimizer. Summing work over a polynomial number of messages uses linearity of expectation, not independence. The theorem does not promise all functions on an unbounded domain.

The unperturbed certificate also has the correct direction. For every feasible pair, subtracting its perturbation from its perturbed value gives an original value at least `v_xi-sum_i max(xi_i,0)`. Evaluating the perturbed optimizer in the original objective gives the stated upper bound. Their difference is at most `sum_i |xi_i|<=n sigma`. The inequality is classical; the algorithm is what makes the exact perturbed value available here. The consequence is additive approximation, not a relative FPTAS or exact optimization of the original instance.

## 6. Targeted verification and limits

I ran:

```
python3 /tmp/review_spectral_parametric_oracle.py
```

The temporary exact-rational checker examined all finite-grid noise states for three affine support families on binary cubes of dimensions one, two, and three. At each net point its mock restricted oracle deliberately returned the worst permitted approximate candidate. It checked both enumeration inclusions, distinct outputs, the oracle-call bound, the sharper expected-output inequality, and inclusion of every support active anywhere in the interval by solving its exact affine inequalities. All **530 noise states, 1,060 enumerations, 1,238 outputs, and 546 active-support inclusions** passed.

It also checked **16 conditional support optimizers and 16 roundings** for a positive-definite matrix that is not diagonally dominant: diagonal entries one and all off-diagonal entries `3/5`, with spectral bounds `2/5` and `11/5`. Exact calculations verified the conditional norm bound, support-stationarity identity, and additive rounding error for four boundary points. This is a challenge to the conditional argument, not an implementation or test of the complete tree-decomposition dynamic program.

These finite checks do not prove the probability inequality, asymptotic complexity, or general dynamic program. Those conclusions rely on the mathematical arguments reviewed above. No Lean proof, project-wide checks, or CI inspection were performed. I did not edit the source. I did not independently reopen the cited prior papers in this review; its positive mathematical verdict should not be read as an independent novelty determination.
