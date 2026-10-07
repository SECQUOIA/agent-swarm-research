# Independent review of anisotropic Gaussian separable closure

Date: 2026-10-02. Verdict: the substantive argument in the
[anisotropic extension](../new-direction/anisotropic-gaussian-separable-closure.md)
passes independent mathematical review. No numerical conditioning promise
on the supplied full-row-rank factor is needed. The expected-work
parameter is the curvature of its supplied concave term, not intrinsic
negative curvature of the full objective.

The review checked rational row normalization, exact preservation of the
separable residual, anisotropic local comparisons, the Gaussian count,
critical-region closure, and the finite-law budget. A separate delegated
reviewer independently approved the normalization and mesh arguments,
including their polynomial bit complexity. The reused scalar-state and
fallback interfaces are those of the
[separable mixed theorem](../new-direction/smoothed-mixed-separable-closure.md);
the finite sampler and probability transfer were checked in the earlier
[Gaussian review](smoothed-gaussian-cell-closure-review.md).

## 1. Rational normalization preserves the objective exactly

For \(\Gamma=TT^T\succ0\), clearing denominators and bounding the
other eigenvalues by \(H\) gives

\[
 \lambda_{\min}(\Gamma)
 \ge D_0^{-k}H^{-(k-1)}=\mu>0.
\]

This remains valid when \(H<1\). The denominator product and powers
have polynomial encoding length. Rational Jacobi rotation with residual
operator norm at most \(\mu/64\) uses the per-entry threshold
\(\mu/(64k)\); its precision depends logarithmically on \(H/\mu\).
Exact orthogonality is retained throughout the construction.

Every rotated diagonal entry is a Rayleigh quotient, so
\(\mu\le a_i\le\|T\|_2^2\). Dyadic choices satisfying
\(2a_i\le d_i^2<8a_i\) exist at all positive scales. They give
diagonal entries in \((1/8,1/2]\), while the normalized off-diagonal
residual has norm at most \(1/128\). Consequently the frame eigenvalues
actually lie in

\[
 (15/128,65/128],
\]

which is stronger than the stated \([1/16,1]\) bound. Also
\(L_{\max}<8\alpha\|T\|_2^2\).

The crucial identity is exact:

\[
 U^TLU
 =\alpha T^TQ^TD^{-1}D^2D^{-1}QT
 =\alpha T^TT.
\]

Thus the Jacobi approximation is used only to prove conditioning of the
frame. No residual matrix is discarded or placed in the convex term.
Every original unary function remains unchanged, and no dense recourse
problem is introduced.

The branch \(k=0\) separates and is now explicitly handled. The review
also requested the distinction between operator-norm Jacobi tolerance and
per-entry tolerance; the draft now states both. These were clarity edits,
not changes to the construction.

The domain preprocessing is now explicit as well. Fixed coordinates may
be eliminated by absorbing their affine and constant contributions without
changing unary convexity. The full-row-rank promise applies after this
preprocessing: deleting fixed-coordinate columns can otherwise destroy row
rank. The theorem does not silently perform a dependent-row elimination.

## 2. The diagonal metric gives the claimed local intervals

The anisotropic penalty cancels the supplied concave term and leaves
scalar objectives with tilts \(u_j^TLa-r_j\). The existing integer
neighbor tests and continuous derivative tests therefore still return
global scalar winners and globally valid state regions. Square completion
with \(L^{-1}d\) is correct and preserves witness-gap transfer.

For dyadic \(\rho_i\) with \(1\le L_i\rho_i^2<4\), the
least power-of-two subdivisions are nested and number at most \(2^j\)
in each coordinate. Every refined coordinate satisfies

\[
 L_i h_{ij}^2>h_j^2/4,
 \qquad B_j=\tfrac18\sum_iL_i h_{ij}^2\le kh_j^2/2.
\]

Hence

\[
 L_i h_{ij}+4B_j/h_{ij}
 \le(1+8k)L_i h_{ij}.
\]

This proves the stated local interval length without a curvature ratio.
Unrefined coordinates have no interior nodes and require no such estimate.
The witness upper model gives the corresponding deterministic interval
location with half-width \((1+8k)L_i h_{ij}/2\). Neither argument
requires the mixed value function to be differentiable.

## 3. Gaussian counting loses neither ambient dimension nor conditioning

For the continuous Gaussian proxy, the factor coefficient and residual
remain independent because their linear projections have zero cross
covariance. The normalized frame gives factor covariance eigenvalues in
\([\sigma^2,16\sigma^2]\). The previous product density majorant
therefore applies with standard deviation \(4\sigma\) and prefactor
\(4^t\) for a marginal of dimension \(t\).

The earlier proof of that majorant works for every positive frame lower
bound at most one. Its previous restriction to \(c\ge1/2\) was not
used algebraically; using \(c=1/16\) here is valid.

The weighted lattice sum uses spacing \(L_i h_{ij}\), core width
\(L_i(u_i-\ell_i)\), and constant \(C_k=1+8k\). The probability
cap handles coarse meshes, while the Gaussian integral controls both
tails. Multiplying by the marginal prefactor cancels the wider Gaussian
scale in the coefficient of the core width. This yields exactly

\[
 H_L=\prod_i\left[
 2+4(2C_k+4)+
 \frac{C_kL_i(u_i-\ell_i)}{\sigma\sqrt{2\pi}}
 \right].
\]

There is no factor involving the auxiliary-box width,
\(L_{\max}/L_{\min}\), or an ambient-dimension power. Since
\(\|U\|\le1\), each projection width is at most
\(\operatorname{diam}(X)\). Each factor is therefore bounded by

\[
 8C_k+18+
 \frac{8C_k\beta\operatorname{diam}(X)}{\sigma\sqrt{2\pi}},
 \qquad\beta=\alpha\|T\|_2^2.
\]

This explicitly supplies the numerical parameter dependence claimed by
the theorem. The Gaussian proxy need not have its optimizer inside the
finite search box; only actual sampled draws need that containment.

## 4. Exact piece closure and the exceptional tubes remain valid

The extracted branch Hessian is

\[
 H_J=L-\sum_{j\in\mathcal F_J}
       (Lu_j)(Lu_j)^T/p_{j,J}.
\]

The stated \(H_0\) bounds its operator norm by the triangle inequality
and is independent of sampled coefficients. Regions retain fixed normals
and offsets affine in residual noise. Their state count and scalar-line
section complexity are unchanged. The algebraic branch gradient identity
holds at ties and on lower-dimensional regions, even where the full
envelope is nonsmooth.

Minimizing the global witness upper model gives
\(g^TL^{-1}g\le2(V(v)-\min V)\). At the retained near-optimal
corner this implies

\[
 \|g\|\le\sqrt{2kL_{\max}}\,h_j,
 \qquad
 \operatorname{diam}(\text{cell})\le h_j\sum_i\rho_i.
\]

The rational bound
\(\sqrt{2kL_{\max}}\le k(1+L_{\max})\) is valid for
\(k\ge1\). The sum defining \(C_{\rm tube}\) therefore covers
both the active-vector error and the branch-gradient variation across
the cell.

For an invertible branch Hessian, a violated region boundary produces the
usual gradient-image hyperplane. For a singular Hessian, its gradient
image lies in a proper affine hyperplane. A zero region row cannot become
violated elsewhere in a cell containing the queried point. Thus the
previous hyperplane count covers degenerate branches and ties as well.

Pulling a normalized factor hyperplane back to ambient coordinates gives
an ambient normal \(v\) with \(Uv=u\), where \(\|u\|=1\).
Since \(\|U\|\le1\), its norm is at least one. The same Gaussian
tube probability and coordinatewise Kolmogorov transfer bounds apply.
Small \(L_i\) may enlarge the tube coefficient, but its encoding length
remains polynomial and its magnitude affects only the logarithmic cutoff.

## 5. Fixed finite law and exact bit-work accounting

For trial support \(R_s\), the enlarged auxiliary box contains an
optimizer for every draw with \(\|\gamma\|_\infty\le R_s\sigma\),
by square completion and the row-sum bound on \(A_U\gamma\).
All box widths are positive because the frame has full row rank.

The scaled width obeys \(S(t)\le2^tS(0)\), while the tube coefficient
does not depend on support. Thus \(J(t)\le J(0)+t\). Taking the
logarithm of the deterministic node-count budget gives precision growth
of order \(kt\), plus logarithmic and polynomial base-input terms.
The stopping condition \(2^t\ge b+20\) is therefore attainable with
polynomial \(t,J,b\). No quantity in this loop depends on the eventual
sampled denominators.

Normalization increases the input length only polynomially, so composing
its bit bound with the sampler and exact arithmetic retains an absolute
polynomial exponent. The sampler runs at radius \(b+20\); it does not
enumerate the trial support or the exponentially large finite grid.

Uniform scalar-line section bounds allow replacement of the independent
Gaussian coordinates by the specified finite rational coordinates. The
precision budget makes the summed local-event discrepancy at most one.
At the terminal level the Gaussian tube contribution and finite-law
correction are each at most \(1/(4B)\). This pays for the exact fallback
on the same draw, including atoms on exceptional hyperplanes.

The proof supplies exact correctness at every atom and expected work under
the particular base-chosen finite product law. It supplies neither an exact
real-Gaussian input model nor the same expectation guarantee for arbitrary
coarse approximations. The output optimizes the sampled objective.

The parameter \(\beta\) can be much larger than the negative curvature
remaining after the unary convex terms are included. Replacing it by
intrinsic negative curvature, or replacing \(k\) by negative inertia,
would need an additional argument that preserves separability. The draft
correctly makes neither claim.

## 6. Verification record

The new proof and its two relevant predecessors were read with `cat` and
checked algebraically. The delegated reviewer also read the cited Jacobi
construction and performed no executable tests. The author's targeted
normalization and mesh checks are separate validation and are not counted
as reviewer-run experiments. No project-wide verification or CI inspection
was performed.

The targeted formatting and relative-link command run for this report was:

```sh
python - <<'PY'
from pathlib import Path
import re
p = Path('research-20261002/reviews/anisotropic-gaussian-separable-closure-review.md')
s = p.read_text()
assert s.endswith('\n')
assert all(line == line.rstrip() for line in s.splitlines())
links = re.findall(r'\]\(([^)]+)\)', s)
for link in links:
    assert (p.parent / link.split('#', 1)[0]).resolve().is_file(), link
print(f'PASS: {p}; whitespace and {len(links)} relative links')
PY
```

It passed for all three relative links.
