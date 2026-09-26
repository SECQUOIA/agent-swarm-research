# Independent review of near-optimal enumeration and complete messages

Date: 2026-09-22. Reviewer: `/root/review_nearopt_enumeration`.

Reviewed [the complete-message draft](research-20260922-oracle-all-messages.md),
including its first-moment count, enumeration algorithm, parameter net,
spectral conditional oracle, and expected bit complexity.

Promoted text (pointer added 2026-09-25): the reviewed draft path now holds
only a promotion notice; the full proof is in
[the promoted result](../results/smoothed-spectral-indicator-messages.md).
This review did not record a revision or digest of the draft it read.

**Verdict.** The mathematical argument is correct under its stated oracle
and spectral assumptions. It constructs the claimed complete dictionaries,
including supports active only at ties or on the box boundary. The proof does
not require higher moments, a general-position assumption, or algebraic
decomposition of an envelope. One minor convention should be explicit in the
general parameter theorem: the compact parameter set is nonempty. The
indicator-QP boxes already satisfy this convention. A direct citation for the
classical sandwich inequality should also be included.

## Probability bound

The inequality `|A| <= |Sh(A)|` is the upper half of the classical sandwich
theorem. The draft's induction using the union and intersection of the two
coordinate slices is valid, including an empty slice or empty intersection.
An empty family shatters no set; a nonempty family shatters the empty set.

For a fixed coordinate subset `I`, condition on all noise outside `I`.
The pattern-class minima `C_b` then depend on none of the remaining noise
coordinates. If the near-optimal family shatters `I`, every class minimum
after its pattern penalty belongs to `[v,v+a]`. In particular,

```
|C_ei + xi_i - C_0| <= a,  for each i in I.
```

These are separate fixed intervals of length `2a`. Independence therefore
gives the product bound `(2 phi a+tau)^|I|`. It would be invalid to use
coordinate thresholds depending on each other's unconditioned noise; the
pattern conditioning here avoids that problem. The argument allows arbitrary
deterministic support costs and exact ties. Summing over shattered subsets
gives exactly `(1+2 phi a+tau)^m`.

For a uniform grid including both endpoints of `[-sigma,sigma]`, the
closed-interval count proves `tau=1/N` and `phi=1/(2sigma)`. It remains valid
when an endpoint is an atom. With `epsilon=1/(12n phi)`, `N>=2n`, and
`a=3epsilon`, the exponent is at most

```
m(6 phi epsilon+1/N) <= m/n <= 1.
```

Thus the expected number of all near-optimal support labels is at most `e`.
Deduplicating identical polynomial formulas is unnecessary for this bound:
it already counts distinct tied supports. Rare realizations can still have
exponentially many such supports.

## Approximate enumeration and its certificate

First-difference children partition the parent cell minus its extracted
candidate, for every feasible family, not only the full binary cube. Each
remaining support has a unique first free coordinate where it differs from
the candidate. Empty child cells are harmless when the oracle recognizes
them. Caching one candidate per cell avoids repeated oracle calls during
priority comparisons.

The root is nonempty because `Z` is assumed nonempty. Its candidate value
satisfies `v<=U<=v+epsilon`. Every support of cost at most `v+delta` has a
remaining-cell lower bound at most its cost and hence at most `U+delta`.
The stopping rule cannot discard such a support. On extraction,

```
V = LB+epsilon <= U+delta+epsilon <= v+delta+2epsilon.
```

Consequently the output contains every `delta`-near support and only
`delta+2epsilon`-near supports. Neither conclusion presumes sorted exact
objective values. In particular, a deliberately poor oracle returning the
worst allowed approximate candidate still satisfies the proof.

Each output is distinct and produces at most `m` child calls. The total is
at most `1+m|E|`. There are deterministically at most `1+m2^m` cells ever
generated. A heap therefore has a logarithmic overhead bounded by a
polynomial in `m`, even on an unusually large realization. This is why the
first moment of `|E|` suffices for expected work. An implementation that
rescanned all cells at every extraction would instead introduce a quadratic
output-size cost and would not be justified by this first-moment argument.

The same proof would allow a decreasing feasible incumbent between `v` and
the original `U`, but the draft's fixed threshold is simpler and sufficient.
Adaptively chosen cells cause no conditioning issue: the output inclusion is
a pointwise statement about the original complete noise realization.

## Parameter coverage and exact dictionary construction

An optimal support at any parameter is `2Lr`-near-optimal at a net point at
distance at most `r`. Taking `r=epsilon/(2L)` puts it inside the enumerated
set. This argument includes a support optimal only at an isolated tie or a
boundary point. It never assumes a region with positive volume.

The product midpoint net on a rational box has the stated covering radius.
Using the conservative bound `kR/B` for the Euclidean radius is valid.
For `L=0`, all branches are constant on a nonempty parameter set and one
point suffices. A zero-dimensional or zero-radius box is a singleton.

The net must be deterministic and independent of the penalty noise, as it
is here. The same perturbation vector may be used for every net point and
every message: linearity of expectation needs no independence across these
computations. The output is a list of full branch functions, so no arrangement
algorithm or polynomial-time region classification is hidden in the claim.

## Spectral conditional oracle and tree messages

For every active set `A`, `Q_AA` has minimum eigenvalue at least `mu` and
`||Q_AS||_2<=H`. Hence

```
||x_A(t)||_2 <= (C sqrt(n)+2H R sqrt(k))/(2mu)
             <= (nC+2HkR)/(2mu) = M.
```

This is a bound on conditional optimizers, not merely the root optimizer.
That distinction matters: fixing a boundary can push internal coordinates
beyond a box derived for the unconditional problem. The draft uses the
correct larger conditional bound. Differentiating the Schur formula gives
`gradient q_A=2Q_SA x_A`, so `L=2HM` is valid uniformly over supports and
fixed-bit restrictions. Empty support and empty interior cause no problem.

The grid contains zero because its subdivision count is even. Each fixed
support's continuous minimizer lies inside the grid box. Rounding active
coordinates leaves inactive coordinates zero, and stationarity on the active
support cancels the linear error term. The objective increase is at most
`HnM^2/B^2`. Exact continuous minimization of the optimal grid support can
only improve its grid value. It therefore supplies both a feasible support
and the exact support value required by the enumeration oracle.

The finite-domain dynamic program works on the induced graph, whose width
is no larger than the supplied width. Unary and internal edge costs can be
assigned exactly once to containing bags. Minimizing child tables over their
internal states before joining avoids a product over a bag and a second
independent child bag. Arbitrary fixed bits only delete states. Active zero
and inactive zero remain separate states, as required for signed penalties.

For a child-subtree message, the running-intersection property excludes
edges from its interior to vertices outside the interior and separator.
The resulting Hessian is the principal matrix `Q_II`. It is important that
the message does not use an arbitrary partial collection of quadratic terms
assigned to bags; that collection need not remain positive definite. The
draft explicitly uses the principal-matrix formulation.

Boundary-only terms and boundary penalties are omitted from the internal
message. A boundary indicator equal to zero restricts its coordinate to zero;
it does not change the internal objective on that face. Thus the same
dictionary handles both boundary indicator states without losing the
active-zero distinction in the full optimization problem.

All grid data and support Schur coefficients are rational. Their encoding
lengths are polynomial in the rational input and the logarithms of grid and
net sizes. Exact principal linear solves have polynomial bit complexity.
The numerical bounds `C,H,1/mu,R,1/sigma` control the grid and net cardinalities;
the theorem correctly does not claim polynomial dependence on their binary
encoding lengths alone. Sampling the smallest power-of-two grid of at least
`2n` points uses `O(log(n+1))` bits per coordinate.

The bounded-perturbation lower and upper bounds in the final corollary are
also correct. They provide an additive original-objective certificate, not
exact optimization of the original instance or a relative FPTAS.

## Literature and significance

I opened [Kozma and Moran, *Shattering, Graph Orientations, and
Connectivity* (2013), Theorem 5 and its proof](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v20i3p44/pdf).
It explicitly gives the sandwich inequality and credits Pajor, Bollobas and
Radcliffe, Dress, and Holzman and Aharoni. This is a suitable direct
attribution for the combinatorial inequality; calling it a new counting
principle would be incorrect.

The [Lawler publisher record](https://pubsonline.informs.org/doi/10.1287/mnsc.18.7.401)
states the classical `O(K n c(n))` enumeration conversion from an exact
optimizer. The first-difference partition is an established ingredient.
Here the certified approximate oracle changes the output guarantee to a
near-optimal inclusion, and this inclusion connects its work to the smoothing
bound.

I also reopened the [Roglin--Teng FOCS 2009 manuscript](https://www.roeglin.org/publications/FOCS09.pdf).
Its higher-gap and expected smoothed optimization results remain major
antecedents. The present proof's useful outcome is a constructive complete
parametric dictionary, combined with the spectral fixed-treewidth oracle.
Expected smoothed exact optimization and the use of perturbation gaps are
not themselves new. This review does not establish publication priority for
the near-optimal first-moment formula or the complete-message theorem.
Searches using near-optimal counts, shattering, perturbations, and smoothed
enumeration did not resolve that priority question; an unsuccessful search
is not evidence of novelty.

## Reproducible targeted verification

I created and ran:

```text
python3 code/research_20260922/check_nearopt_enumeration.py
```

The exact `fractions.Fraction` checker passed:

- 3,276 first-moment cases across 18,270 complete noise outcomes. It used
  every nonempty binary feasible family in dimensions one through three,
  two offset functions, two grid sizes, and three near-optimal widths,
  including zero and atomic ties.
- 12,420 adversarial approximate-enumeration runs, with 75,522 extractions
  and 182,948 oracle calls. It used exhaustive small cost tables and seeded
  arbitrary feasible families through dimension six. The mock oracle chose
  the worst permitted approximate value. The checker verified exact disjoint
  coverage by pending cells after every extraction, absence of duplicate
  outputs, completeness for all `delta`-near supports, containment in the
  `delta+2epsilon`-near set, and the call bound. Both fixed and decreasing
  incumbents passed, including zero accuracy, zero tolerance, ties, and
  empty child cells.

These finite checks challenge the probabilistic bound and enumeration
invariants in small cases. They do not establish the general theorem,
asymptotic bit complexity, or novelty. The spectral and tree-decomposition
arguments were checked mathematically above. No Lean proof, project-wide
verification, or CI inspection was performed. The reviewed source was not
edited by this reviewer.
