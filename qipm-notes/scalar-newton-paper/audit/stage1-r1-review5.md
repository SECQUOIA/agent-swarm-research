# Stage 1, round 1, independent review 5

Verdict: **no major issues; one minor interface issue to correct**.

I reviewed `sections/02-models.tex`, all of `sections/03-classical.tex`, the
classical diagnostic script, and the relevant active upper-bound notes. I did
not consult other review reports. Later-stage claims and unwritten sections
are outside this verdict.

## Numbered findings

1. **Minor — define the finite-precision algorithm on off-support samples.**
   In `sections/03-classical.tex`, lines 294–298, total-variation error permits
   a reported index with `b_i = 0`, but the referenced exact estimator divides
   by `b_i`. The exact sampling algorithm never encounters this case, whereas
   the approximate sampling algorithm can. The coupling proof already puts
   such events inside its `L delta` allowance, so the rate and conclusion do
   not change. Specify that an approximate sample outside the support returns
   an arbitrary fixed finite value, such as zero, and impose the arithmetic
   error condition only on sampled indices in the support. Also phrase the
   comparison with the exact-oracle output as existing under a coupling; this
   is what the proof establishes. No new argument is needed.

## Mathematical checks

- The Chebyshev residual construction has the claimed degree and relative
  operator bounds, including the `K = 1` boundary. The ratio determining the
  degree remains positive for every `K > 1`.
- The complex coordinate estimator is unbiased. Its second moment is a sum
  over the support of the sampling vector, so the inequality (rather than an
  unconditional equality with the full norm) is essential and correct.
- Maximizing the stated spectral expression gives the Kantorovich constant;
  the diagonal example really attains the second-moment bound. The manuscript
  correctly limits this sharpness statement to the estimator.
- The chosen group size gives group failure at most one quarter. The
  polynomial bias and median-of-means error leave the stated spare error
  budget for the perturbation proposition.
- The bilinear variance bound uses `P(H)^2 <= kappa (1+eta)^2 H^{-1}`
  correctly; neither the algorithm nor its stopping rule requires knowing the
  energy norms. Separate real/imaginary medians preserve the promised complex
  error with the supplied slack.
- The rejection sampler's raw output probabilities sum to the claimed
  distribution, including zero coordinates of the right-hand side. Its
  expected cost uses both row and column materialization and the lower
  singular-value bound. It supplies no hidden norm oracle.
- For general complex, nonnormal matrices, `q(A* A) A* A = q(A* A)(A* A)`
  gives the residual identity on the actual solution. The singular-value
  calculation and resulting condition bound are valid without an eigenvector
  or spectral-radius assumption. The general inverse-overlap theorem has
  the correct extra logarithmic dependence on the supplied solution-norm
  ratio.
- The necessary logarithmic conditioning scales follow from the exponential
  upper bounds at fixed sparsity and accuracy. They are not stated as
  universal hardness claims.
- Rational residual coefficients and exact finite local sums establish
  implementability, while the paper appropriately declines a uniform bit-cost
  bound. The finite-error transfer is otherwise valid by sequential coupling
  and the Lipschitz property of the median.

## Literature and coverage checks

The classical section attributes sparse polynomial evaluation and coordinate
importance sampling to prior work and makes no unqualified priority claim for
those ingredients. I independently checked Andoni–Krauthgamer–Pogrow's
[primary full text](https://arxiv.org/html/1809.02995), Section 1.4: it explicitly
poses the right-hand-side-sampler to solution-sampler question. The citation
in the manuscript is therefore substantively appropriate, despite that
paper's main theorems studying a different coordinate output contract.

The stage covers the substantive classical algorithm developments assigned
to it: scalar, energy-normalized bilinear, solution sampling, norm-sensitive
general inverse overlaps, normalization, and precision limitations. The
source notes' stronger lower-bound comparisons are correctly deferred to
later stages. I found no missing stage-1 theorem necessary to make the
delivered results valid.

## Diagnostics

Ran `/home/sgusev/miniconda3/envs/qipm/bin/python
scalar-newton-paper/scripts/verify_classical.py`: PASS. The diagnostics check
distinct useful failure modes (complex conjugation, support zeros, sharp
moment constants, full rejection probability, and arithmetic perturbation).
They support rather than replace the algebraic verification above.
