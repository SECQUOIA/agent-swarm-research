# Quadratic aggregation certificates: numerical checks

Supports `results/quadratic-aggregation-trivial-hull-certificate.md`.

```
conda run -n minlp-notes python code/quadratic_aggregation/check_examples.py
```

Checks (all passed on 2026-09-21, about 10 minutes, seed 20260921):

- Section 5 example (`n = 3`, `m = 4`): `S` bounded in `(x_1, x_2)`; every
  normalized convex certificate has `(A_lambda, b_lambda) = 0` up to `5e-12`
  (semidefinite programs via cvxpy/SCS); the image of the hyperplane
  `{x_1 = s t}` under `f^h` misses the midpoint of two of its points for
  `s = 1, 5, 50`; the image of `{t = 0}` is convex.
- Random two-quadratic systems: consistency of the SDP certificate test with an
  exact line-based midpoint test (`y` is the midpoint of two points of `S` along
  a random direction, with the feasible parameter set computed exactly from the
  roots of the two quadratics).
- Paired systems `f_2 = -f_1 + const`, `A_1` indefinite: only trivial
  certificates and every random target is a midpoint of two points of `S`, as
  Theorem 1 predicts.

- Three quadratics with PDLC of the quadratic parts only (negative
  coefficient), only trivial certificates: every random target is a midpoint of
  two points of `S`. All such instances also satisfy PDLC of the homogenized
  matrices, as the scope remark after Corollary 5 explains.

These are sanity checks of statements and examples, not a proof.

The main theorem and its three supporting lemmas now have separate
[Lean proofs](../../formal/topics/27-quadratic-aggregation/README.md).
That package includes the HHC specialization and verifies the original
coefficient-level theorem. It does not verify these numerical scripts,
the examples, or the source note's additional corollaries. Reproduction of
the formal checks is documented in the
[verification record](../../formal/topics/27-quadratic-aggregation/VERIFICATION.md).

The separate [consequences package](../../formal/topics/28-quadratic-aggregation-consequences/README.md)
now proves Corollaries 1, 3 and 4, Lemma 4, and the closed-system and strip
boundary examples, including actual HHC and the exact Shor witness. It
still does not verify these numerical programs or turn their floating-point
outputs into mathematical certificates.

The [infinite-aggregation package](../../formal/topics/29-infinite-aggregation/README.md)
separately verifies the explicit HHC construction, spectral goodness,
indispensable strict rays and the finite closed-hull obstruction. These
proofs also do not depend on the numerical programs in this directory.

The subsequent [exact hull](../../formal/topics/30-infinite-aggregation-hull/README.md)
and [accuracy](../../formal/topics/31-aggregation-accuracy/README.md) packages
verify the finite SDP lifts and quantitative finite-cut bounds, including
exact integer multiplier constructions. These mathematical results do not
certify the numerical scripts or their floating-point behavior.
