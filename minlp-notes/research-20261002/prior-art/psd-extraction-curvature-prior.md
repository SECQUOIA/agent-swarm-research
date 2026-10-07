# Prior-art audit: a scaled-Horn obstruction to bounded-curvature extraction

Date: 2026-10-02. This note compares the construction in
[`psd-extraction-curvature-obstruction.md`](../new-direction/psd-extraction-curvature-obstruction.md)
with the copositive-cone literature. The construction has passed an
independent mathematical review; see
[`psd-extraction-curvature-obstruction-review.md`](../reviews/psd-extraction-curvature-obstruction-review.md).
The result is a limitation of one preprocessing strategy in the original
coordinates, not a hardness claim or an impossibility theorem for other
certificates. The reviewed note also gives a diagonal rescaling with a
uniform transformed curvature/growth ratio at most `13130`, so this family
does not obstruct combined PSD extraction and diagonal preconditioning.

The construction takes `A_d = D H D + εI`, where `H` is the 5-by-5 Horn
matrix, `D = diag(d,1,1,1,1)`, and fixed `ε = 1/100`. It proves that for
every decomposition `A_d = P + N + R` with `P` positive semidefinite, `N`
entrywise nonnegative, and `R` copositive, the residual satisfies
`R_11 ≥ 7d²/8`. The original orthant growth is `g = ε`, while negative
curvature and interaction width remain bounded. Thus strict-copositive
residuals have diagonal-curvature ratio `L_R/g_R ≥ 175d²`; for the specified
shared geometric grid, the number of coordinate nodes must grow at least
linearly in `d`.

## Closest established results

The Horn matrix and its zero rays are classical. Hildebrand’s 2012
classification states that the Horn form generates an extreme ray of
`COP_5` outside the SPN cone (`PSD + entrywise-nonnegative`); the same
classification treats positive diagonal scalings as the copositive-cone
group orbit. See the author manuscript [“The extreme rays of the 5×5
copositive cone”](https://optimization-online.org/wp-content/uploads/2011/03/2959.pdf),
pp. 1–2 and Theorem 3.1, together with the journal identity
[DOI 10.1016/j.laa.2012.04.017](https://doi.org/10.1016/j.laa.2012.04.017).
Theorem 3.1 classifies the other exceptional extreme rays after excluding
the Horn orbit; the introduction and conclusion identify the Horn orbit as
extremal. This is a qualitative cone-geometry result. It concerns `DHD`
itself and does not bound decompositions of the perturbed interior matrix
`DHD + εI`.

Hildebrand’s minimal-zero criterion is an even closer qualitative
comparison. A copositive matrix `A` is irreducible with respect to the PSD
cone precisely when its minimal zeros span the ambient space (Theorem 4.5).
For the Horn matrix, the five adjacent-pair zeros `e_i+e_{i+1}` are minimal
and linearly independent; positive diagonal scaling maps these zeros to
`D^{-1}(e_i+e_{i+1})` and preserves their span. Thus the unperturbed `DHD`
admits no nonzero PSD matrix that can be subtracted while keeping a
copositive remainder. See [Hildebrand, “Minimal zeros of copositive
matrices,” arXiv:1401.0134](https://arxiv.org/abs/1401.0134), Definition 2.1
and Theorem 4.5. The source defines irreducibility by the absence of any
positive amount of a nonzero PSD matrix that can be removed while staying
copositive.

These results explain the mechanism: the exact Horn zero rays block PSD
subtraction at `ε=0`. They do not provide a stability modulus when the
matrix is perturbed by `εI`, or a lower bound on one selected residual
diagonal in terms of the diagonal scaling `d`. The candidate’s elementary
estimate supplies that quantitative step: on each zero ray of `DHD`, the
total positive contribution from the PSD extraction is at most
`ε||z_i||²`; the five rays span the coordinate with coefficient `d/2`, so
Cauchy–Schwarz bounds `P_11` by `O(εd²)`. Subtracting from
`(A_d)_11 = d²+ε` forces `R_11 = Ω(d²)` for the fixed small `ε`.

The extension from PSD extraction to an additional entrywise-nonnegative
part is a direct algebraic reduction, not a separate prior theorem. Move
`diag(N)` into the PSD part and move `N-diag(N)` into the copositive part;
the latter is entrywise nonnegative with zero diagonal and does not change
the residual diagonal. This preserves the lower bound while covering
arbitrary dense real extractions.

## Scope of the comparison

The established literature already contains the scaled Horn ray, its
exceptional status outside SPN, and a minimal-zero criterion for exact
PSD-irreducibility. The present construction does not introduce those
facts. The narrower quantitative statement is about the fixed positive
perturbation `εI`: every separately nonnegative extraction in the stated
decomposition leaves a large residual diagonal, despite bounded growth and
negative-curvature parameters in the original problem. Its second bound
concerns one specified shared-grid rule after extraction.

Neither statement rules out optimizing the convex part and residual jointly,
using a different coordinate system or an anisotropic grid, or using another
global certificate. The construction itself is in fixed dimension five, so
it does not imply an optimization-complexity lower bound. It also does not
show that all methods must have cost growing with `d`.

The primary Hildebrand texts above were checked from the open Optimization
Online manuscript PDF and the open arXiv HTML/PDF, respectively. Both have
been routed to the designated literature reader for local source packaging;
no knowledge-base files were edited here.
