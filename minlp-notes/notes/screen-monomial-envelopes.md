# Screen: envelopes of bounded monomials on wedges and boxes (2026-09-22)

Read-only screening agent over the local full texts of Belotti et al. (Math.
Program. 2025, `belotti2025-convex-envelopes-of-bounded-monomials`), Yang–Zhang
(IJOCTA 2026, `zhang2026-flat-lower-envelopes-solve-bounded`), Nguyen–Richard–
Tawarmalani 2018, Anstreicher–Burer–Park 2021, Locatelli–Schoen 2014 and
Khajavirad–Sahinidis 2013, plus web search. Selected as the next direction.

## Status of the Belotti et al. open items

- (a) Lower envelope on a wedge for `n > 2`: **resolved** by Yang–Zhang
  (Theorems 1.1, 3.1, 3.9, 3.11): the lower envelope is flat (`z >= l`) on
  `X ∩ W_ij`, independent of `u` and of `beta = sum a_i`; full graph hulls
  follow. The argument is Belotti's compensating-coordinate two-point
  construction at level `l`. Caveats: short note in a minor venue, AI-assisted.
  Their Section 4.3 leaves open negative exponents, several cones, side
  constraints. The repository ledger (`open-problems-from-literature.md`, row
  17) has been updated.
- (b) `n = 2` with negative exponents: open (Belotti p.20 guesses a hull similar
  to the `beta <= 1` case).
- (c) Hull of `{x_1^{a_1} x_2^{a_2} in [l, u]}` over a box: open; known only for
  `a_1 = 1 <= a_2` with bounds on the product (Nguyen–Richard–Tawarmalani 2018,
  Theorems 1–2, Corollary 4) and for the bilinear case with product bounds
  (Anstreicher–Burer–Park 2021: RLT plus up to three SOC pieces).
- Post-2025: Lee–Skipper–Speakman arXiv:2605.01493 (multilinear graph over a
  box with at most one positive lower bound), Zhang–Ouyang–Yang arXiv:2608.26639
  (`[1/2, 2]^2 ∩ {x_1 x_2 <= 1}`); neither touches (b) or (c).

## Candidate questions (agent's sketches, unverified)

- Q1: complete `n = 2` wedge classification for arbitrary real exponents
  (`beta != 0`), including ratio terms `x_1^{a}/x_2^{b}`; route via parallel
  chords (homogeneity only), quasi-convexity decided by `kappa = a_1/|a_2|`, and
  Belotti's conic majorant/minorant `h(f) = z_0 + c f^{1/beta}`; a 2x2 case
  table. Risk: sign of `h(t) - t` on `[l, u]` and tightness on the lens in
  each case.
- Q2: graph hull over a box with `z in [l, u]` for concave monomials
  (`a_i > 0`, `beta <= 1`): conjectured description `box ∩ {f >= l} ∩ H_u` with
  `E_U = min(f, u)` and a glued lower envelope (flat on the `l`-lens, polyhedral
  elsewhere); risk: global single description needs monotone facets; check
  against Tawarmalani–Sahinidis convex-extension folklore.
- Q3: negative/mixed exponents for `n >= 3` on a wedge (Yang–Zhang Section 4.3).
