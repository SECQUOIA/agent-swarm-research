# Independent source review of the strong-convex quartic upper-bound prior audit

Date: 2026-09-28. Scope: source attribution, reduction type, and the
significance wording in
[the prior audit](strong-convex-quartic-posslp-upper-prior.md).
The mathematical upper proof was assigned to a separate reviewer and
is not verified here. The inspected draft calls it a proof candidate.

The central comparison passes this narrow review. The full method of
combining Newton iteration, an algebraic gap, arithmetic circuits, and
division removal to obtain a many-one PosSLP reduction has an explicit
predecessor. The possible new statement is the application to the
specified globally strongly convex quartic class and its combination
with the separately reviewed lower bounds. This review establishes
neither that application nor publication priority.

## Source findings

- **Etessami--Stewart--Yannakakis:**
  [arXiv:1201.2374v2](https://arxiv.org/pdf/1201.2374v2),
  Appendix C, printed pages 48--53, supports the strongest methodological
  attribution. Corollary C.8 on page 52 explicitly gives polynomial-time
  many-one equivalence with PosSLP for each strict comparison of a least
  fixed-point coordinate with a rational threshold. Its proof on pages
  52--53 uses polynomially many Newton steps, determinant circuits,
  repeated squaring for the gap scale, and separate numerator and
  denominator circuits. Theorem C.4 and Lemma C.5 supply convergence
  and separation; Theorem C.7 selects the precision. The convergence
  statement uses simple normal form and removal of coordinates equal
  to zero or one. Corollary C.8 includes that preprocessing. These are
  probabilistic polynomial systems, not general gradient systems.
  The note correctly limits its direct many-one attribution to strict
  comparisons; the printed corollary states the nonstrict case in
  \(\mathrm P^{\mathrm{PosSLP}}\). Page 8 confirms that this extension
  was absent from the STOC 2012 version.
- **Allender--Bürgisser--Kjeldgaard-Pedersen--Miltersen:**
  [author PDF](https://people.cs.rutgers.edu/~allender/papers/slp.pdf),
  Proposition 1.1, is an oracle characterization of the Boolean part
  of constant-free real computation. It permits adaptive calls at
  branch tests. Proposition 1.3 explicitly states Turing equivalence.
  Neither alone proves a one-instance reduction for the proposed
  optimization language. Theorem 3.9 concerns a fixed constant; its
  advice bit is not an oracle-query bound. The audit preserves these
  distinctions. The attribution to Tiwari remains explicitly indirect.
- **Kung--Traub:**
  [author PDF](https://www.eecs.harvard.edu/~htk/publication/1978-jacm-kung-traub.pdf),
  Theorem 8.1 on printed page 257, bounds field operations for algebraic
  function expansions. Its coefficient-growth and multivariate limits
  do not supply the proposed uniform bit-complexity theorem.
- **Approximation and elimination:**
  [Hesse, v1](https://arxiv.org/html/2511.03440v1), Corollary 1.2,
  supports the approximation dependency. Its dated exact-complexity
  table cannot establish later unresolved status.
  [Basu's author survey](https://www.math.purdue.edu/~sbasu/raag_survey2011.pdf),
  Theorem 2.16 on printed page 12, includes degree and integer
  coefficient-bit bounds for quantifier elimination, including one
  quantified block. It does not require a finite complex solution set.
  Checking its application and all quantitative bounds in the new
  upper proof remains the mathematical reviewer's task.
- **Hansen et al.:**
  [primary PDF](https://arxiv.org/pdf/1202.3898), Theorem 23 on printed
  page 19, treats isolated real solutions. Lemma 26 on page 22 gives
  \(|\gamma|\ge(2\|R\|_\infty)^{-1}\); the page-23 proof instead
  uses \(|\gamma|>\|R\|_\infty^{-1}\). The positive root of
  \(t^2+3t-1\) lies below \(1/3\), so that intermediate strengthening
  is false in general. This confirms the audit's local source caveat,
  not a disproof of the final theorem or of the ESY result. Retaining
  the separate Basu-based dependency is a justified audit choice.

## Wording corrections incorporated

No material source-scope correction was needed. The author incorporated
the following four refinements, and the revised paragraphs were reread:

1. The opening now includes a supplied rational curvature lower bound.
2. Section 5's proposed completeness conclusion now specifies
   polynomial-time many-one reductions.
3. The rational-circuit witness consequence now remains conditional on
   the upper proof passing review.
4. Section 4 removed an uncited alternative through classical weak
   convex optimization. It retains Hesse Corollary 1.2 as the verified
   optimization dependency and separately explains the elementary
   radius bound available from supplied strong convexity.

The significance assessment is appropriately conditional. The
restricted lower-bound construction may reasonably be judged the
larger contribution; this is a judgment, not a literature theorem.
The claims about all general strongly convex quartics remain distinct
from the inspected PPS results unless a reduction between the input
classes is supplied. Neither distinct wording nor the absence of an
identified reduction establishes novelty.

## Verification record and limits

The relevant primary statements were read directly in this review or
its earlier source-checking turn. A second reviewer independently
checked the new audit's reduction-type and conditional wording.
Tiwari's original article and Hesse's final proceedings text were not
obtained. No general literature exclusion search was performed here.

Targeted checks: `git diff --no-index --check /dev/null` on this file
reported no whitespace errors; a Python check verified its local
Markdown targets and balanced math delimiters. No project-wide
verification or CI inspection was performed.

## Follow-up: monotone-gradient prior comparison

Also reviewed on 2026-09-28:
[monotone-gradient-posslp-prior.md](monotone-gradient-posslp-prior.md).
Its approximation-versus-exact comparison passes the narrow source
check. No new upper proof or construction was reviewed.

[Anagnostides et al., arXiv:2504.03432v3](https://arxiv.org/pdf/2504.03432v3),
Theorem 4.7 on printed page 24, assumes an isotropic compact convex
domain, the Minty condition, and Assumption 2.4. The latter requires
exact polynomial-time rational evaluation at rational inputs, bounded
output encoding length, and rational Lipschitz and magnitude bounds.
The output is an approximate SVI solution. Section 4.1 explicitly
rounds ellipsoid data. Lemma A.1 uses affine normalization and claims
preservation of the evaluation assumptions; its exact covariance
normalization cannot silently be regarded as rational arithmetic.
However, the paragraph following Assumption B.5 on printed page 50
explicitly permits approximate rational evaluation oracles. The revised
audit acknowledges this and limits its caution to instantiating the
bit model. It does not reject the approximation theorem.

The audit's distance deduction is valid with the stated zero in the
domain: substituting that zero in Definition 1.1 gives the required
upper bound on the inner product. Strong monotonicity supplies the
lower bound. This elementary deduction is correctly separated from
the source's theorem and from later exact comparison.

[Network Cournot Competition](https://arxiv.org/pdf/1405.1794),
Theorem 10 on printed page 17, explicitly outputs an approximate
complementarity pair with normalized gap at most the requested
tolerance. Its displayed iteration bound does not establish an exact
threshold algorithm.
[Kapron--Samieefar, arXiv:2411.04392v1](https://arxiv.org/pdf/2411.04392v1),
Section 5.8 and Theorem 5.11, concern approximate VI search; their
Section 6 on printed page 28 explicitly leaves exact versions
unconsidered. No globally strongly monotone restriction appears in
that VI input definition. Appendix C records the gradient connection,
which by itself supplies no exact complexity bound.

The added clarification was reread. Local links, math delimiters, and
whitespace were rechecked after this addition. The older primary
abstracts were not independently reopened in this follow-up, and no
claim about their full text is endorsed. No exclusion search or
novelty conclusion follows from these checks.
