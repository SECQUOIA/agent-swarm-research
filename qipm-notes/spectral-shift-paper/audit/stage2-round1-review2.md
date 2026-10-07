# Stage 2, round 1: independent review 2

**Severity counts: 0 major, 0 minor.** I found no required mathematical,
citation, or implementation repairs in the reviewed material.

I reviewed all of `sections/05-joint-accuracy.tex`, the new material in
`sections/04-fixed-accuracy.tex` beginning with Definition
`even-thresholds`, and `scripts/joint_accuracy_diagnostics.py`. I also read
the Stage 2 author audit and applicable project instructions. I did not
read another review or edit manuscript files. The checks below record the
substantive points behind the assessment; they are not a claim of formal
verification.

## Growing-index pinned construction

**Location:** `sections/05-joint-accuracy.tex:222–343`.

The construction keeps the degree-dependent factors needed for a uniform
result. In particular:

1. Pairing the shifts with opposite signs makes the gate even and
   pi-periodic in the angle. Its algebraic degree in `x` is bounded by the
   stated `4(r+1)^2(r+2)(k-1)`. The product definition gives `0 <= W <= 1`
   globally and exact pinning at every positive contact.

2. The nearest angular contact has `d <= C_rho/r`, and the error slack is
   bounded below by `c_rho G_r r^2 d^2`. Dividing the leakage bound by that
   slack gives, before suppressing fixed bases,

   \[
   \frac{[C_\rho r(k\delta)^2d^2]^{r+1}}
        {c_\rho\delta G_r r^2d^2}
   \leq C_{\rho,A}\delta^{1/r}
       \left(\frac{C_{\rho,A}R_0^2}{r}\right)^r.
   \]

   The powers of `r`, `delta`, and `R_0` agree with the manuscript.
   This controls the ratio even arbitrarily near contacts. The limiting
   ratio is zero at a contact, so the continuity interpretation is valid.
   The signed-error argument then proves error at most `G_r delta`, not
   merely `(G_r+o(1)) delta`.

3. The tail estimate correctly retains the factor `2^(n+4)`. On the
   middle region, `delta(k delta)^(-n) <= A^(-n)` produces a fixed base
   raised to `n`. On the outer region the linear term is bounded by
   `C r^2 2^n/k`, and the degree-`n` term by
   `C_rho r [2B_rho/(A R_0)]^n`. The first tends to zero because
   `n=o(D)`; one fixed sufficiently large `A` controls the second.
   The inner region is controlled by `delta Lambda_rho^n/r=o(1)`.
   These three estimates prove global contractivity without appealing
   to correctness on the promised bands or to numerical samples.

4. The two high-band powers are correct:

   \[
   (n+4)(1-1/n)-1=n+2-4/n,
   \qquad (n+4)(1-1/n)-n=3-4/n.
   \]

   They respectively control the gate term divided by `G_r delta` and
   the degree-`n` contribution. Both dominate the retained exponential
   bases under `n=o(D)`. The constant and linear terms in the blend are
   included. The choice of `N` gives the required high-band error, and
   `G_r <= K` implies `L=o(D)`, so its cost is `O_c(D)`.

5. Integer rounding uses inequalities rather than an expansion whose
   error might depend on `r`. The eventual inequalities follow from
   `r=o(D)`, and the leading query constant is independent of the growing
   index. The sufficiently-small-`delta` onset is explicitly allowed to
   depend on the chosen parameter path; the theorem does not assert a
   uniform onset over all little-o paths.

## Uniform lower bounds and the joint comparison

**Locations:** `sections/05-joint-accuracy.tex:22–218` and `:347–375`.

- The exterior proof uses Taylor polynomials of the exact sine target.
  This avoids an accuracy floor of order `delta^2` after rescaling.
  Convexity of `arcsin` gives the required negative extrapolation value
  uniformly in the chosen degree. Maximality of the odd index supplies
  a lower bound on `K` of order `R_0^(-n)/n`, and therefore makes the
  sine remainder negligible uniformly even for arbitrarily large `L`.
  The factorial root gives the stated factor of `n` in the query bound.
  No correctness assumption is made on other periodic completions.

- The Fejer–Riesz factor has degree at most the query count, and the
  analytic composition with `exp(i arcsin x)` has the stated growth on
  the complex circle. Squaring its truncated Taylor polynomial produces
  a real globally nonnegative polynomial, so the obstruction really is
  `G_r`, not an unconstrained approximation error.

- In the finite-margin theorem, endpoint separation gives
  `T >= d'_rho delta^(-1/2)`. Choosing the index constant at most
  `d'_rho/2` ensures `r+1 <= 2r <= T`. The adaptive radius is then
  admissible in the small-`T delta` branch. The other branch is stronger
  than the claimed lower bound. Solving the quadratic obstruction gives
  the factor `(G_r-K)^(1/(r+1))` with uniform constants.

- In the all-index theorem, evaluating the exact threshold expression
  at `a+1/(2r)` yields the displayed explicit lower bound. The fixed
  radius rules out `T<r+1` simultaneously for every integer `r` once
  `delta` is small enough. This removes the index restriction before
  the adaptive-radius argument is applied. It supports the claimed
  unrestricted high-accuracy consequence and the `K=0` impossibility.

- The integrated-sign polynomial is globally in `[0,1]`, has the
  stated approximation error, and applies on the full interval
  `[delta,1]`. Comparing `L` and `D` when `L >= beta D` gives both
  matched laws with the stated parameter dependence.

- Applying the finite-margin bound at index `r-1` gives exactly the
  exponent in the pinned upper bound. The additional assumption
  `K <= (1-gamma)G_(r-1)` makes the margin root uniformly positive.
  At `K=G_r`, the ratio `G_r/G_(r-1) -> R_0^(-2)<1` supplies a fixed
  margin. The resulting `O(r^2)` multiplicative gap is justified.
  The final text appropriately retains the margin near the upper tier
  boundary and does not claim a uniform multiplicative Theta law there.

## New parity results

**Location:** `sections/04-fixed-accuracy.tex:295–383`.

The nonnegative-even feasible sets are closed under coefficient limits,
and bounded interpolation values supply compactness for attainment.
The Taylor-limit lower bound retains evenness and global nonnegativity.
The pinned upper construction works for an attained even minimizer:
its positive-contact set is nonempty, since otherwise adding a small
positive constant improves the approximation while preserving
feasibility. The resulting blend remains even. Minimality of the chosen
index handles possible threshold plateaus correctly.

The proof of `F_1=F_2=E_1` is valid: a quadratic polynomial in `v=y^2`
that is nonnegative on the positive half-line has a nonnegative leading
quadratic coefficient and is convex. Its endpoint upper bounds and the
chord gap of `sqrt(v)` force error at least `E_1`. The explicit cubic in
`y^2` for `rho=2` is globally positive and has the stated rigorous tail
bound, which is approximately `0.0200113 < 1/32`. Thus the even class
has the claimed matched exponent `5/6` in the comparison table.

For the odd class, the Taylor/exterior argument correctly converts
`q(0)=0` and near-one values on the low interval into the logarithmic
factor. The normalized sign-minus-linear construction is bounded on
both its transition region and its complement. It gives the matching
upper bound without depending on `c`. The table continues to restrict
the comparison to a single definite-parity transform.

## Diagnostics and their limits

I ran the script with the required interpreter and a separate output
directory:

```text
/workspace/local-home/miniconda3/envs/qipm/bin/python \
  spectral-shift-paper/scripts/joint_accuracy_diagnostics.py \
  --output /tmp/stage2-review2-diagnostics
```

It completed successfully. The sampled maximum normalized absolute
error was `1.0` for all three examples. The leakage/slack maxima were
`6.854487931452993e-25`, `1.937732525431207e-46`, and
`3.3320852703885618e-74`, matching the audit. Pin leakage was zero to
working precision. A separate calculation reproduced `G_1` to about
`4.5e-17` absolute error and checked the approach of
`G_r/G_(r-1)` to `R_0^(-2)`.

The kernel and positive-series evaluations implement the displayed
formulas. Evaluating the signed-error identity avoids subtracting two
quantities close to one. The script explicitly describes its output as
diagnostic, which is appropriate: floating-point clipping of the kernel,
finite meshes, and zero leakage to working precision do not certify
global bounds or exact equality. Its three finite examples also do not
establish the `r=o(D)` asymptotic theorem. Those claims are supported by
the analytic proof above, not by the script. No change is required for
the script's stated purpose.

## Source checks

The citations used for the new constructions and inequalities support
their applications:

- [Gilyen et al., Lemma 25 and Theorem 30](https://arxiv.org/pdf/1806.01838)
  give the bounded odd sign approximation and uniform singular-value
  amplification invoked in the manuscript.
- [Motlagh–Wiebe, proof of Theorem 4](https://arxiv.org/pdf/2308.01501)
  contains the reciprocal-root factorization argument used to recall
  Fejer–Riesz factorization.
- [Bos–Ma'u–Waldron, Proposition 2.1](https://www.math.auckland.ac.nz/~waldron/Preprints/Extremal-growth/BosMauWaldron1.pdf)
  states the exterior Chebyshev inequality for real polynomials, the
  version required by the new lower bounds.

No missing attribution affecting the validity or stated scope of the
reviewed results was found. A broader novelty or literature-completeness
assessment remains outside this bounded Stage 2 review.
