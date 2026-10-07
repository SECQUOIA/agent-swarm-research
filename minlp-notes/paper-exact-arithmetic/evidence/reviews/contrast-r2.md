# Round-two review of the quadratic contrasts and boundaries

Date: 2026-10-05. I read the full `contrast-r1.md` and
`authoring/repair-contrast-r1.md`, then checked the repaired actual J/K files.
This review covers the commissioned repairs and preservation of the
odd-prime feasible-output construction. Appendix L's Q13–Q14 work is outside
this round's scope.

All required local repairs are verified. One remaining low-severity value
approximation qualification was reported during this round and repaired by
the root before the final read. No new open mathematical objection remains
in this repair scope. The outstanding classical-source audit is separate
from this analytic verdict.

## Actual repairs verified

| Topic | Final location | Verification |
| --- | --- | --- |
| Block weights | J:1533–1535, 1574–1599 | The statement now requires \(1\le\omega_1\le\cdots\le\omega_k\). These conditions give \(a_i>1\) and \(\Sigma<k\omega_k\bar\gamma\), hence the claimed positive multipliers. The necessity remark correctly exhibits the large- and small-\(\omega_1\) failures through the two unique KKT multipliers for \(k=2\). Later uses have weights \(t^{i-1}\), \(t\ge1\), and satisfy the repaired statement. |
| QP rational constants | J:2549–2550, 2578–2589, 2611–2617 | The radius is rational and at least one. Uniform minor and entry bounds give rational polynomial-length Hoffman upper bounds without enumerating row subsets. \(U=nR\) and \(L_f=\mathfrak qU+\bar c\) are rational bounds. All constants precede the choices of rational penalty parameters. The existing approximation inequalities still apply with these upper bounds. |
| Zero/empty QP rows | J:2641–2652 | The denominator is \(\mathfrak C=\max\{1,\max_\iota\|C_\iota\|_1\}\), with empty inner maximum zero. Computed slacks differ from true slacks by at most \(\mathfrak g/4\); the \(\mathfrak g/2\) active-row threshold is valid. The empty active set also fits the rational pseudoinverse chart. |
| Native and explicit input lengths | J:96–104, 1542–1545, 1601–1624, 1665–1668, 1694–1725 | Quadratic exponent vectors cost \(O(n)\) bits per listed monomial. Thus the stated native bound \(O((k+1)n^2(1+k^2\log\ell_k))\) and explicit bound \(O((k+1)n^2(n+k^2\log\ell_k))\) both hold. For fixed \(k>3C\), native \(O_k(R^2\log R)\) and explicit \(O_k(R^3)\) inputs cannot print degree \(\Omega(R^k)\) scalar polynomials in \(\phi(k)L^C\) time. The shear preserves these bounds. The explicit-weight \(O_k(R^6\log R)\) bound dominates exponent-vector overhead. |
| Odd-prime feasible-output consequence | J:1748–1776, 1873–1941 | The prime-degree norm/Kummer proof, degree \(d^k\), primitive sum, full-dimensional ellipsoids, span \(3k\), actual-coordinate shear and full polynomial support are preserved. Its lengths are \(O(k^3d^2\log(kd\varpi_k))\) natively and \(O(k^3d^2[\log(kd\varpi_k)+kd])\) explicitly. With the first \(k\) primes fixed and \(k>3C\), these become \(O_k(d^2\log d)\) and \(O_k(d^3)\); the list of \(d^k+1\) coefficients defeats the claimed output-time bound in both formats. |
| Uncertain-data scope | K:14–17, 252–260 | The text now concerns accurate objective upper bounds from uncertain function values and explicitly distinguishes robust root existence and exact rational input. It no longer excludes every form of singular-equality certification. |
| Optimal comparison gaps | K:162–174 | The regularization argument names the nonzero gap \(\lvert m-c\rvert\), a rational threshold, and a supplied radius. The shared separation lemma applies to the singleton projection \(z=f(y)-c,\ \nabla f(y)=0\). For globally convex \(f\), every critical point has the attained minimum value. The passage describes a choice from a uniform bound and disclaims necessity for each individual instance. |
| Hesse value contract | K:30–35 | The final text specifies a globally convex rational quartic on a nonempty rational polyhedron with finite optimal value, an additive objective-gap guarantee, and no distance guarantee. This matches the vetted version-1 contract and the explicit fixed-degree input model. |
| Effective inequality and QE | K:378–394, 431–448 | Both imported contracts have the floor \(\mathfrak d\ge2\) and exact theorem locators. QE is applied after clearing denominators with degree two and one free variable. The compact domain and continuous graph descriptions satisfy the cleared inequality contract. The eliminated description and the graphs obey degree and coefficient bounds \(2^{\mathrm{poly}(L)}\), sufficient for the selected polynomial exponent. |
| Integer exponent and bounds | K:398–400, 418–424, 446–448, 475 | \(\mathfrak p\) has nonnegative integer coefficients and positive constant term, so \(\mathfrak p(L)\ge1\) is integral. Inward ceiling/floor bounds preserve exactly the permitted integer values. The binary expansion uses enough bits, excludes surplus codes with the retained upper row, and uses no bits on a singleton interval. Positive chain length is explicit. |
| Eliminated inequality versus fractional term | K:369–376, 477–481, 513–520 | Signed residuals are defined before use. Eliminating intermediate squaring variables leaves polynomial inequalities in \(s_0\) of degree \(2^{\mathfrak p(L)}\); minimizing over \(s_0\) returns the fractional term. The degree-two nonconvex lift and the non-polynomial fractional objective are correctly distinguished. |
| Small treewidth case | K:330–334 | The path bags are stated for \(k\ge2\); \(k=1\) has the single width-one bag \(\{x,y_1\}\). |

The only new objection raised in this round was the pre-final wording of
K:30–34, which lacked a nonempty, finite-optimum qualification. The convex
quartic \(f(x,y)=x^4-y\) on \(\mathbb R^2\) has value \(-\infty\), so
it has no finite additive value enclosure. The root inserted both
qualifications. The final text resolves the objection.

## Source status

The round-one gates for Basu–Mohammad-Nezhad and Luo–Zhang are closed by
Luna's primary-source report. I read the vetted rows in
`evidence/literature-review.md` and checked their actual applications;
I did not conduct literature research.

- K cites publisher Theorem 4.1 for one-block QE and Theorem 2.2 for the
  effective inequality. The degree floor, compact domain, continuous graph
  descriptions, positive integer exponent and separate coefficient bound
  agree with the cleared contract.
- J:2382–2386 uses Luo–Zhang for the feasible convex epigraph problem with
  finite infimum. J:2525–2528 uses its polyhedral special case. Both name
  Corollary 2 in the 1997 report's numbering. The bibliography keeps the
  published 1999 metadata and records the lawful report's pp. 6–7 locator;
  it does not pretend that the subscription-only published theorem pages
  were inspected.
- K's final Hesse sentence uses the already vetted arXiv-v1 Corollary 1.2
  objective-gap contract, with the repaired finite/nonempty qualification.

Remaining classical contracts, metadata and precise locators listed in the
repair report remain under Luna's separate audit. This review neither
reopens the cleared gates nor treats pending source work as already accepted.
The local repairs are ready for integration; final source acceptance belongs
to that source audit.

## Final reviewed hashes and checks

The actual files after the root's final K qualification have these SHA-256
hashes:

```text
21361c5eb3eefa2f4decf1ae3c6b3a08755ba1cb59a4d77873a08f341d4aae4a  appendices/J-quadratic-contrast.tex
ed88ea5a7c14d38370861141adb3a613a41f7e2cfd4fef42ef663af098568b82  appendices/K-boundaries.tex
```

Verification used targeted `cat`, `rg`, `nl`, `sed` and `sha256sum` reads,
manual algebra, and independent delegated repair checks. No manuscript was
edited by this review. No experiments, mathematical scripts, historical
reruns, browsing, compilation, project-wide checks or CI inspection were
performed. A document-only newline/whitespace/control-character check of
this owned review passed. The targeted final commands were:

```text
sha256sum paper-exact-arithmetic/appendices/J-quadratic-contrast.tex paper-exact-arithmetic/appendices/K-boundaries.tex
python - <<'PY'
from pathlib import Path
p = Path('paper-exact-arithmetic/evidence/reviews/contrast-r2.md')
s = p.read_text()
assert s.endswith('\n')
assert all(line == line.rstrip() for line in s.splitlines())
assert all(ord(c) >= 32 or c in '\n\t' for c in s)
print('contrast-r2.md: newline, whitespace and control-character checks passed')
PY
```
