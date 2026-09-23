# Review record: wedge envelopes of two-variable monomials with real exponents

Subject: [results/monomial-wedge-envelopes-real-exponents.md](../results/monomial-wedge-envelopes-real-exponents.md).

**Status after the ten-agent corrective audit (2026-09-22).** The earlier
positive verdict below covered the six main regimes but missed the false
degree-zero hull claim and the omission of a zero individual exponent. The
result now treats these cases separately, with ordinary and closed hulls
distinguished. The checker also now fails on detected inconsistencies.
See [the corrective audit](review-minlp-developments-20260922.md) for findings
and targeted verification. Earlier verdicts are historical, not blanket
certification of later additions.

## Independent adversarial review (2026-09-22, subagent, read-only)

Checked by hand: Lemmas 1–6 (level points, parallel chords and the form `s`,
the quasi-convexity classification with the Hessian determinant
`a_1 a_2 (1 - beta) f^2/(x_1^2 x_2^2)`, chord comparison, the ray function `H`
and corner interpolant `L`, the convex hull of `D`, the level-value
decompositions) and the six regime proofs of Theorem 1, including the points
the author flagged as delicate: the identity `Y_A ∩ {s >= s_l} = conv(T)` in
regime I.2; regimes II/III.B1 when the `l`-lens crosses the `C_u` chord (the
ray argument never uses the other bound, so those points are covered); the
orientation of the `t'`, `t''` argument for `beta < 0`; the identification of
the envelope function with the hull of the epigraph; and the boundary
coincidences at `beta = 1` (`L = phi`, `H = f`).

Independent numerics (reviewer's own scripts, 18 parameter sets including
close bounds `u = 0.74` where the lens crosses the chord, and a wide wedge
`p = 0.05, q = 20`): predicted `conv(D)` agreed with the hull of dense samples;
points slightly outside the predicted half-plane or level set were never
convex combinations of points of `D`; predicted lower envelopes never exceeded
the LP lower envelope (`<= 1e-13`) and predicted upper envelopes never fell
below the LP upper envelope (`<= 1e-11`). Exactly one convex minorant and one
concave majorant among the four candidates in every regime.

Verdict: mathematically correct, no fatal or substantive gap. Novelty modest and
honestly described: regime II is Belotti's Section 6 guess with `l` and `u`
exchanged; III.A and III.B1 reuse the I.1 and II formulas; III.B2 (chord
function as concave majorant, ray function as convex minorant) is the one
structurally new configuration; the `kappa` classification and the Case A/B
organization are the contribution.

Presentational corrections requested and applied:

1. `x/y` removed from the motivating list (it has `beta = 0`, the trivial case);
   the Hazen–Williams example corrected to `Q^{1.852} D^{-4.87}`.
2. "unique convex minorant" and the "iff" entries of Table 2 softened to the
   proved "if" directions, with uniqueness recorded as a numerical observation.
3. "exactly on `P cup Q`" in Lemma 4 replaced by a remark on strictness.
4. Remark 3 relabeled a heuristic organizing principle, not a structural theorem.
5. "second-order-cone representable" replaced by "power-cone representable".
6. A half-sentence added to Lemma 5 on why `t'`, `t''` straddle `1` for both
   signs of `beta`.

## Literature check (2026-09-22, subagent)

No source treats negative or mixed exponents on a wedge with value bounds;
Belotti (Section 6) and Yang–Zhang (limitations) flag negative exponents as
untreated; the only found citer of Belotti 2025 is Yang–Zhang 2026. Closest
partial results (box domains, no value bounds, or relaxations rather than
envelopes) are listed in the note's Section 5.

## Not done

No Lean formalization or computational solver experiment. The subsequent
corrective audit is linked above.
