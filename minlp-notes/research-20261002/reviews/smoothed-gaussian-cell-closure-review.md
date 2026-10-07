# Independent review of Gaussian-weighted exact cell closure

Date: 2026-10-02. Verdict: the new probability and sampling arguments in
[the Gaussian cell-closure note](../new-direction/smoothed-gaussian-cell-closure.md)
pass mathematical review. No substantive correction is required. The
expected-work conclusion follows using the exact-QP, critical-region,
closure, and fallback interfaces already reviewed for the
[ambient theorem](../new-direction/smoothed-ambient-cell-closure.md).

This review independently checked the Gaussian decomposition, marginal
density comparison, weighted grid sum at every mesh scale, finite rational
sampler, support/precision budget, and probability transfer. It does not
claim a new audit or implementation of the reused exact-QP primitives.

## 1. Conditional distributions and local events

For the continuous proxy, the decomposition is orthogonal in the original
noise coordinates. In particular,

\[
 D\Pi=0,\qquad
 \operatorname{Cov}(d,r)=\sigma^2D\Pi=0,
 \qquad
 \operatorname{Cov}(d)=\sigma^2(TT^T)^{-1}.
\]

Joint Gaussianity therefore makes the entire vectors \(d\) and \(r\)
independent, even though the coordinates of \(d\) generally remain
dependent. Degeneracy of the residual covariance is harmless. Conditional
on any residual outside a null set, each factor-coordinate marginal has
the same Gaussian law as before conditioning.

The frame bounds imply that every principal covariance submatrix has
eigenvalues in \([\sigma^2,\sigma^2/c]\). For a subset of \(t\)
coordinates this gives

\[
 p_Q(z)\le c^{-t/2}\prod_{i\in Q}\phi_{\sigma/\sqrt c}(z_i).
\]

The density prefactor and inverse-covariance estimates both have the
correct direction. This is a product majorant, not an assertion that the
factor coordinates are independent.

At a grid node, the two neighboring comparisons give an interval of
length at most \(C\alpha h_i\), where \(C=1+2k\). The shared inner
witness in the upper model places the actual allowed values in the
deterministic interval

\[
 \alpha[\ell_i-v_i,u_i-v_i]
       +[-C\alpha h_i/2,C\alpha h_i/2].
\]

Only the event needs to lie in this interval; the larger interval obtained
from the neighboring comparisons need not do so. The draft states this
distinction correctly. Integrating the product density majorant over the
coordinate intervals gives its probability bound with the factor
\(c^{-t/2}\) outside the product of capped integrals.

## 2. The weighted grid sum covers coarse meshes and tails

Write \(\Delta=\alpha h_i\) and let the projected core have width
\(W=\alpha(u_i-\ell_i)\). The nodes whose enlarged interval contains
zero number at most \(W/\Delta+C+2\). Since each summand is capped
at one, their contribution is at most

\[
 CW\phi_s(0)+C+2.
\]

On each remaining tail the summand decreases with distance. The first
term is at most one, and the remaining sum is bounded by the integral
divided by the lattice spacing. Thus each tail contributes at most

\[
 1+\Delta^{-1}\int_0^\infty
       \min\{1,C\Delta\phi_s(t)\}\,dt
 \le 1+C/2.
\]

Their sum is exactly the stated upper bound
\(CW\phi_s(0)+2C+4\). This reasoning holds for arbitrary lattice
offset, zero core width, arbitrarily small mesh, and mesh much larger than
the Gaussian scale. Retaining the minimum with one is what prevents a
spurious factor proportional to the coarse mesh.

Adding the two boundary nodes in each coordinate and expanding over the
interior-coordinate subsets gives the displayed \(H_G\). The cancellation
\(c^{-1/2}\phi_{\sigma/\sqrt c}(0)=1/(\sigma\sqrt{2\pi})\)
is correct. No auxiliary-box width or ambient-dimension power is left in
this count.

The Gaussian proxy may have its auxiliary optimizer outside the finite
search box. This causes no gap: its local events are defined everywhere,
and the probability comparison uses those events. Containment of an
optimizer is needed only for actual finite-law draws, where the later
support bound supplies it.

## 3. The finite sampler has the claimed law and bit cost

Let \(K=p+20\) and \(e=2^{-(p+20)}\). The proposed mesh satisfies
\(\Delta\le e/K\). Its number of grid nodes can be a power of two,
so uniform proposals require only the logarithm of that number in fair
bits. Each grid node is rational with polynomial encoding length.

At least a \(1/(4K)\) fraction of this sufficiently fine grid lies in
\([-1,1]\), where the approximate acceptance weights exceed \(1/4\).
The per-attempt acceptance probability is therefore at least \(1/(16K)\).
After \(16K(p+20)\) attempts, the failure probability is at most

\[
 e^{-(p+20)}\le 2^{-(p+20)}=e.
\]

Conditional on any acceptance before the cap, the returned proposal has
law proportional to the deterministic approximate weights. The cap does
not otherwise bias that law: summing the geometric probabilities of the
possible acceptance times supplies the same factor for every node.
Returning zero on failure changes the distribution by at most the failure
mass.

The Riemann estimates have ample slack. The unnormalized initial-segment
and total errors are at most \(2K\Delta+2\Delta\), while the
normalizing integral exceeds one. Normalization therefore fits within
the stated \(10K\Delta\) allowance. Replacing the sampled weights
by approximations with error at most \(e/K\) gives total scaled mass
error at most \((2K+\Delta)e/K\), which also fits within the stated
\(10e\) distribution-function allowance. Gaussian truncation and the
failure atom each cost at most \(e\). The total \(22e\) is below
\(2^{-p}\).

The exponential weights do not require a real-number oracle. Argument
reduction needs \(O(\log K)\) squarings, and the alternating Taylor
series on \([0,1/2]\) converges geometrically. A fixed dyadic precision
with the stated guard bits controls the initial approximation, subsequent
rounding, and at most twofold error amplification per squaring. Clamping
to \([0,1]\) does not increase the error. A common precision can be
chosen for all proposals using the maximum number of squarings.

The cap is \(O(p^2)\), so both the number of attempts and their bit cost
are polynomial in \(p\), in the worst case. The same deterministic
sampler applied with separate independent random bits gives independent
original coefficients. Rejected internal proposals are part of sampling
the specified law; the optimization algorithm never discards a completed
coefficient draw because it is exceptional.

## 4. The support and precision choices are not circular

For trial support multiplier \(2^t\), all quantities used to choose the
terminal level and precision depend only on the base rational input and
that trial multiplier. In particular the critical-piece Hessian bound
does not include denominators of sampled coefficients.

The stated bounds

\[
 J\le A_0+t,\qquad
 p\le A_1+O(kt+\log(A_0+t+1))
\]

follow from the logarithmic dependence of the auxiliary width on
\(2^t\), and from
\(\log Q_{\rm all}=\log(J+1)+k\log(2^J+1)\).
The powers and products in the budget formula have polynomial encoding
length and can be computed without enumerating grid nodes.

Exponential \(2^t\) eventually exceeds the bound for \(p+20\),
after polynomially many trial steps. This already makes the resulting
\(p\) polynomial in the base input, with an absolute exponent. The
actual sampler radius is \(p+20\); its running time is not proportional
to the potentially larger trial support multiplier. Once the loop stops,
the support lies in the fixed auxiliary box on every draw.

## 5. Transfer and exact-work accounting

A scalar Kolmogorov error \(\delta\) changes the probability of a union
of at most \(C_{\rm sec}\) intervals by at most
\(2C_{\rm sec}\delta\). One-sided limits cover open endpoints and
singletons. The uniform section bound from the ambient theorem holds
when the other coefficients are fixed arbitrarily, including at atoms of
the finite law. Replacing independent coordinates one at a time therefore
gives the stated \(2nC_{\rm sec}\delta\) bound for each local event.

Summation over all deterministic grids through the terminal level costs
at most \(Q_{\rm all}\) such errors. The precision formula makes their
total at most one, yielding the claimed expected local-event count.

The exceptional hyperplanes are fixed in ambient coordinates. For the
Gaussian proxy, an ambient Euclidean tube of radius \(\tau\) has
probability at most \(2\tau/(\sigma\sqrt{2\pi})\le\tau/\sigma\).
Every axis section of a tube is an interval, empty, or the whole line,
so product replacement adds at most \(2n\delta\) per tube. The
terminal-level choice makes the Gaussian union contribution at most
\(1/(4B)\), and the precision choice makes the finite-law correction
at most \(1/(4B)\). Hence unresolved probability is at most \(1/(2B)\),
which pays for the \(B\operatorname{poly}(I)\) exact fallback.

Correctness holds for every atom because it comes from deterministic
closure and fallback, not from a probability-one genericity argument.
The Gaussian law is used only for the expectation comparison. The note
does not assert an exact Turing-model algorithm on continuous Gaussian
input or a bound for arbitrary coarser Gaussian approximations.

With the supplied spectral normalization, the projected widths are at
most \(\operatorname{diam}(X)\), the frame constant is absolute, and
\(\alpha<4\nu\). The resulting dependence has the claimed form
\(f(k,\nu\operatorname{diam}(X)/\sigma)\operatorname{poly}(I)\),
with an absolute polynomial exponent. It concerns optimization of the
sampled objective; it supplies no accuracy-independent guarantee for the
original unperturbed objective.

## 6. Verification record

The proof checks above were algebraic. The reviewer read the new note and
its ambient predecessor with `cat`; no numerical or solver experiment was
needed for this independent audit. The author's separate targeted checks
are not counted as reviewer-run validation.

The new review received a scoped relative-link and whitespace check. No
project-wide verification or CI status/log inspection was performed.

The targeted check actually run was:

```sh
python - <<'PY'
from pathlib import Path
import re
p = Path('research-20261002/reviews/smoothed-gaussian-cell-closure-review.md')
s = p.read_text()
assert s.endswith('\n')
assert all(line == line.rstrip() for line in s.splitlines())
links = re.findall(r'\]\(([^)]+)\)', s)
for link in links:
    assert (p.parent / link.split('#', 1)[0]).resolve().is_file(), link
print(f'PASS: {p}; whitespace and {len(links)} relative links')
PY
```

It passed for both relative links.
