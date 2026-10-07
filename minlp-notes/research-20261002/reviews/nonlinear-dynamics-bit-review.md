# Independent review of polynomial-dynamics bit certificates

Date: 2026-10-02.

Reviewed [the bit-complexity extension](../new-direction/nonlinear-dynamics-bit.md)
against [the exact-real theorem](../new-direction/nonlinear-dynamics.md).
This review covers the proof and arithmetic model, including the written
unknown-growth-constant schedule in Section 8, not novelty or a complete
solver implementation. No mathematical blocker was found.

## Proof and arithmetic checks

The backward adjoint cancels every dependent-state gradient at any ambient-box
center, including an infeasible center. Repair preserves the initial state and
controls, so its displacement pairs to zero with that gradient. The draft
correctly retains the graph-residual term in its configuration identity. A
Taylor expansion of the full adjusted objective would also have to retain its
nonzero residual constant at an infeasible center.

The midpoint Taylor objective minorant has error at most `Mp w_B^2/4`.
The graph strip contains the exact graph and has residual at most
`H w_B^2/2`. Intersecting coordinate intervals leaves at most eight LP
inequalities. Enumerating independent triples of active rows remains complete
for bounded lower-dimensional domains: a vertex has three independent active
normals in the original ambient space. This includes touching faces,
singletons, and exact affine graphs.

Forward evaluation must use the derivative-bound enclosure, not ordinary
polynomial interval arithmetic. Outward rounding followed by intersection with
the rational state interval preserves containment and gives
`r_next <= a r + q`. Clipping may introduce an input endpoint denominator, but
does not propagate previous polynomial-evaluation denominators. The objective
upper bound has error at most `4 G_b N q/(1-a)`; the factor four accounts for
both the midpoint objective error and the added upper-bound allowance.

Rounding all coordinates of each next center prevents inherited LP
denominators from multiplying bit length across stages. Fixed degree and
arity give polynomial heights for local evaluations; the backward adjoint
recurrence grows height additively across the horizon. Constant-dimensional
LP determinants and DP sums remain polynomial in bit length. The output must
retain the stated recurrence representation: expanded exact states can have
exponentially many bits.

The rounded-center contraction `3/17`, the displayed `B_round`, and the
final certificate gap bound are valid. At stage zero,
`e_(-1) <= p N h_0^2` gives
`e_0 <= (6p + 20C/g) N h_0^2 / 17 <= B_round N h_0^2`.
Subsequent induction uses `h_(j-1)^2 = 4 h_j^2`.

## Corrections and clarifications applied

The reviewed draft includes the following changes requested during this audit:

- A contraction-aware midpoint enclosure replaces natural interval evaluation.
- Every center coordinate, including controls and the initial state, is reset
  to prescribed precision.
- Initialization uses the rational box midpoint, with input-sized encoding.
- Rational upper bounds replace radical constants when selecting parameters.
  In particular, `1+a+b >= sqrt(1+a^2+b^2)`, `3 >= sqrt(6)`, and
  `2 >= sqrt(2)` justify the displayed conservative repair constants.
  Squaring nonnegative sides gives rational grading tests.

The conditioning explicitly includes objective first derivatives and the
resulting multiplier curvature. Supplied derivative and invariance bounds
remain substantive promises; the review does not establish them for general
input models.

## Unknown-growth-constant schedule

The schedule in Section 8 runs trial `mu` with grading ratio `2^-mu`, indefinitely
refining its own reset centers, and stops only upon a certified objective gap.
The stages use the supplied derivative bounds and a fixed rational positive
evaluation allowance, not the unknown growth constant. Unsafe grading ratios
may fail to converge, but their lower and upper bounds remain valid.

In round `r`, restarting each trial `1 <= mu <= r` with a budget of `2^r`
actual bit operations is sufficient. The budget must include setup,
arithmetic, and output; it cannot leave expensive trial preprocessing outside
the accounting. If a safe trial `mu_*` completes in `W_*` bit operations,
round `R = max(mu_*, ceil(log2 W_*))` completes that trial. The allocated
work through this round satisfies

```text
sum_(r=1)^R r 2^r = 2 + (R-1) 2^(R+1) < 2 R 2^R,
2^R <= 2 max(2^mu_*, W_*).
```

This is a polynomial overhead in the conditioned work bound. Simulator and
budget-counter overhead must also be counted; a polynomial logarithmic
overhead does not change the conclusion. No finite stage cap is needed.

## Targeted verification actually run

Three shell commands ran inline Python bodies using `python - <<'PY'`.
These bodies were not saved as repository test scripts. The following records
their actual inputs and assertions; no full DP implementation was executed.

1. **80 exact cancellation and enclosure cases.** Python `fractions.Fraction`
   and `Random(7102)`; horizons `1,2,5,11`, with 20 cases each. Centers,
   controls, and representative states used random eighths in `[-1,1]`.
   Dynamics were `phi(s,u)=s^2/4+u/2`, with contraction bound `1/2`;
   state gradients were `2c`. Assertions checked exact zero adjusted state
   gradients, zero repair pairing, and containment under midpoint propagation
   with outward `2^-14` rounding. A separate assertion used
   `phi(s)=3s/4-s^3/4` on `[99/100,1]`: natural interval width
   `59701/4000000` exceeds the contraction width bound `3/400`.
2. **6 LP cases, 27 constant cases, and 81 clipping cases.** An inline exact
   three-variable Gaussian elimination routine enumerated active triples.
   Cube, face, line, singleton, exact graph `z=x+y`, and empty-strip cases
   returned respectively `8,4,2,1,3,0` distinct vertices. Constant checks used
   `g in {1/100,3/4,7}`, `C in {0,1/13,100}`, and
   `omega in {1/1000,1,10}` with `p=3`, checking induction, stage zero, and
   the final gap inequality. Clipping tests used intervals
   `[1/d,(d-1)/d]`, `d in {3,7,11}`, dyadic exponents `2,5,9`, radii
   `0,1/100,1/5`, and each interval's lower endpoint, midpoint, and upper
   endpoint. Containment and the radius bound passed exactly.
3. **144 schedule arithmetic cases.** For `mu=1,...,12` and work counts
   `1,2,3,7,8,9,31,32,33,127,128,129`, assertions checked safe-trial inclusion,
   its sufficient round budget, the exact cumulative allocation formula,
   and both displayed overhead bounds.

All assertions passed. These checks support the algebra and boundary cases;
they do not replace the proof, measure performance, or verify a complete
certificate-generation program. No project-wide verification, CI inspection,
or literature search was performed.
