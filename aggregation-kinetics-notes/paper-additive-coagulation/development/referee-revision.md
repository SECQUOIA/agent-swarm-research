# Revision after external referee review (2026-09-07)

An independent journal-style review of the accepted manuscript found no
mathematical error in any formal statement but recommended a major revision
for framing, scope, missing references, and several presentational gaps in
proofs. This record lists the changes made in response. The accepted-snapshot
hashes in `final-accepted-snapshot.json` describe the pre-revision sources and
no longer match the current files.

## Framing

- "Sharp" is now qualified everywhere as sharp in the explicit instantaneous
  uniform sense, which is defined in the statement of the main theorem. The
  abstract, introduction, Remark on what the estimate compares, and the
  discussion state that the certified coefficients are Lyapunov bounds, not
  rates: the Golovin--Borel solution decays with exponent min(p, 1-p) and the
  archived critical runs show a fitted decay rate of the half-moment about
  0.45 b against the certified 0.17 b.
- The critical last-event exponent is reduced explicitly to the decay rate of
  the deterministic number--mass overlap, and a conjecture (exponent b/2 for
  monodisperse equal-split data) is stated with the archived numerical
  evidence and its caveats.
- The scalar power-law obstruction is demoted to a remark that states exactly
  what it refutes.
- "Exact critical observables" and "exact density" are now "exact
  representations" in terms of the unknown law.
- The finite-population discrepancy theorem is presented as a corollary of the
  critical moment bound plus the material ceiling of a finite vessel, with the
  count statement as the only part that uses particle dynamics. The constant
  is described as sufficient. A separate second-moment comparison states
  its dependence on the initial second moment and does not locate the first
  mass-CDF discrepancy.
- The Fourier identification section quantifies the low-frequency window,
  states that daughter-law recovery from it is an ill-posed analytic
  continuation, distinguishes the certified rate from an unproved optimal
  asymptotic rate, and renames the
  "certificate" a pointwise sampling bound.
- The introduction no longer claims "the boundary" of fractional-moment
  monotonicity for power kernels; only one-sided failure is proved.

## Scope and length

- The three sections on last-event tails, daughter envelopes, and critical
  representations are merged into one condensed section with redundant
  corollaries removed.
- The observation-design appendix is moved out of the paper into a standalone
  supplementary note, `supplement/observation-design.tex`.
- The numerical subsection is condensed and now reports the fitted decay-rate
  table used by the conjecture.

## References added

Golovin 1963; Aldous--Pitman 1998; Aldous 1999; Norris 1999; Bertoin 2002;
Bertoin--Yor 2005; Fournier--Laurençot 2005 and 2006; Escobedo--Mischler--Perthame
2002; Escobedo--Mischler--Rodriguez Ricard 2005; Menon--Pego 2008; Feller 1951;
Kawazu--Watanabe 1971; Vallender 1974; Wattis 2006.

## Proof-level gaps closed

Lemma on the pair inequality (all-positive second-derivative case); the
Duhamel loss identity in the well-posedness appendix written out; the
filtration of the auxiliary construction specified once; measurability of
quantile maps and weighted norms; the benchmark hazard ODEs derived rigorously;
the strong Markov and compensator steps in the general density proof
separated; the first-moment balance in the unbounded-moments appendix
explained; the elementary proof of the rational envelope bound; path-level
versus equation-level statements distinguished in the logarithmic limit
theorems.

## Minor

Notation collisions across sections resolved; the redundant paragraph on
hidden narrow limits removed; floating-point mass checks and their limits
stated; the reproduction script accepts an output directory so reruns do not
overwrite archived data.

## Corrections after the pre-commit review

- The first-event Jensen inequality has equality exactly when its hazard is
  almost surely constant. Vanishing fragmentation is sufficient, but
  fragmentation after coagulation activity has ended also leaves the hazard
  deterministic.
- The second-moment ceiling-crossing time includes the initial second moment.
  Its logarithmic scaling requires additional initial-moment bounds and does
  not determine the time of a macroscopic mass-CDF discrepancy.
- The 3.3% count-deviation statement is restricted to the largest population;
  the deviations for the two smaller populations are stated separately.
- Printed normalized masses of one are distinguished from exact arithmetic.
  An arithmetic audit of the reproduced n = 100,000, seed 47 run detected
  rounding in particle merges, tree updates, and snapshot sums while matching
  every archived CSV field.
- The faster decay in the Golovin benchmark is not generalized to all models.
  A stronger forcing bound can change the observation-time balance; when the
  fragmentation exponent has zero real part, the sampling exponent is already
  1/2 and does not improve with the decay coefficient.
- The pure-coagulation last-event benchmark uses the half-moment tail
  coefficient a_{1/2} = kappa/2, with an explicit reference to the
  constant-rate bound specialized to zero fragmentation.
- For critical equal splitting, the admissible Fourier set is stated as a
  union of bands centered at 2 pi j / log 2. The interval around zero is its
  central component; factorization in other bands does not by itself give
  the nonvanishing amplitude needed for quotient identification.
