# Independent review of binary-count lower bounds

Reviewed on 2026-09-05 by an agent independent of the original author.
Scope: `results/mip-relaxation-binary-lower-bounds.md` and
`code/mip_relaxation_binaries/check_bounds.py`.

The main claims pass mathematical review: the exact lower bound
`E >= 2^(-2p-2)` for the square, the strongly convex volume bound, and the
bilinear bound `E >= 1/(16 ln(2) 2^p)` follow from the stated lemmas. The
sawtooth and NMDT upper bounds match the cited construction formulas. This
review establishes internal proof confidence, not publication priority.

## Proof checks

- A fixed binary assignment projects to a polyhedron, so its graph preimage
  is compact on a compact box. The finite cover, measure argument, and
  existence of diameter witnesses are valid.
- The midpoint errors are exactly `Δx²/4` for the square and
  `|Δx Δy|/4` for the product. Strong convexity gives `m ||Δx||²/8`.
- The isodiametric inequality yields
  `(m/2)(V/(N omega_d))^(2/d)`, including the correct dimension-one factor.
- In the product lemma, vertical section length is at most
  `min(8ε/t,8ε/(X-t))`; integrating gives `16 ε ln 2`.
  The separate coordinate-width bound `XY <= 20ε` also follows: every
  point is within `8ε/X` vertically of one extreme-x witness, and the
  witness y-coordinates differ by at most `4ε/X`.
- The exact ceiling formulas hold when logarithmic constants are kept
  exact. The integer upper/lower gap for the product is at most two.
- The one-sided hypograph lower bound is valid. A graph relaxation itself
  need not contain a hypograph; taking downward closure gives the correct
  implication.

## Corrections applied to the source

1. Replaced the rounded constant `3.4712` inside the summary ceiling by
   `log2(16 ln 2)`. Rounding inside a ceiling changes the claim on small but
   nonempty intervals of tolerances.
2. Replaced the multidimensional upper-bound argument using convex hulls
   of smooth graphs by explicit affine Taylor tubes on grid cells.
   Smooth graph hulls need not be polyhedral. The corrected proof also
   uses at most `N` cells without asserting that every integer `N` admits
   a congruent grid partition with balanced side lengths.
3. Replaced the false statement that every two-sided relaxation contains
   the hypograph by its downward-closure argument.
4. Removed the purported open question about logarithmic LP extension
   size for square epigraph approximation. Standard face counting resolves
   its asymptotic order; the elementary proof is in the extension note.
5. Added the close precedent of Lubin–Vielma–Zadik's midpoint lemma and
   qualified the novelty discussion accordingly.

## Code audit

The sawtooth fixed-assignment LP correctly enforces each tooth branch,
upper interpolant, and lower tangent inequalities. The sampled dyadic
abscissae contain the analytic extrema. The random point-set tests check
pairwise feasibility and box widths; because finite sets have zero area,
they do not themselves test a positive-area volume statement. The separate
numerical envelope integration is the relevant area check. Numerical
checks support, and do not establish, the analytic assertions.

Independent execution completed successfully: sawtooth depths 1 through 6 passed;
300 random compatible sets and 200 sampled envelopes passed; final output
was `ALL OK`. Observed maximum box ratio was 15.404 against 20, and maximum
envelope-area ratio was 11.086 against `16 ln 2 = 11.090...`.

## Literature assessment

Targeted independent searches used combinations of binary-variable lower
bounds, approximation errors, sawtooth relaxations, fractional vertex cover,
and mixed-integer convex representability. Primary sources checked include
Beach et al., Parts I and II, and the repository full text of
Lubin–Vielma–Zadik, *Mixed-integer convex representability*.
Their Lemma 4.1 gives `MICP rank >= ceil(log2 w)` for a set containing `w`
points whose pairwise midpoints lie outside the represented set. Its proof
uses parity classes of integer lifts, including unrestricted integer
variables. See [[lubin2022-mixed-integer-convex-representability]] p.11-12.

The present elementary geometric mechanism is therefore established. The
exact approximation constants and bilinear area estimate were not found
as stated in this search, but square optimality in particular may be an
unrecorded standard consequence. No assertion of established novelty is
warranted. The interaction-graph and unequal-tolerance extensions appear
more substantial; they receive separate proof and literature reviews.
