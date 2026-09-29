# Rational ellipsoid source for a monotone-map warm start

Date: 2026-09-28.

Status: primary-source audit and a derived stopping lemma. This note does not
review the separate inequalities used to construct the monotone-map cuts.

## Primary source inspected

Martin Grötschel, László Lovász, and Alexander Schrijver, *Geometric Algorithms
and Combinatorial Optimization*, second edition (1993), Chapter 3,
[open chapter PDF](https://www.mpi-inf.mpg.de/fileadmin/inf/d1/ellipsoid-lovasz.pdf).
The PDF starts at printed page 64.

Theorem 3.2.1, printed page 87 (PDF page 24), gives an oracle-polynomial
rounded central-cut algorithm. Its oracle either accepts proximity to a closed
convex set or supplies a normalized rational approximate separating normal.
The alternative output is a rational containing ellipsoid of prescribed small
volume. The update appears on page 88. Lemmas 3.2.8--3.2.10 establish bounded
encoding length, containment, and volume contraction; their proofs occupy
pages 89--93. Remark 3.2.33 on page 94 explicitly allows the cuts to retain only
a fixed subset of the larger set used for the acceptance condition.

The source uses finite precision and enlarges its updated ellipsoid to absorb
rounding errors. Thus it supports rational bit complexity, not only a bound on
the number of ideal arithmetic iterations. The proof is directly applicable to
an exact central cut because such a cut satisfies every positive oracle error
tolerance. The chapter treats dimension at least two; dimension one is handled
separately below.

## Derived stop-or-cut lemma

Let an unknown fixed ball \(B(p,\delta)\subseteq B(0,R)\) be given implicitly,
with a known rational radius \(\delta>0\) and rational outer bound
\(R\geq1\). Suppose a
deterministic routine, at every rational query point \(x\), either:

1. returns an application-specific success flag; or
2. returns a nonzero rational vector \(a\) such that
   \[
   B(p,\delta)\subseteq\{y:a^T(y-x)\leq0\}.
   \]

Assume the routine's running time and output length are polynomial in its
fixed input length and the query encoding length. Then a rational rounded
ellipsoid algorithm reaches a success flag in polynomial time in the input
length, \(n\), \(\log R\), and \(\log^+(1/\delta)\). In particular, the
successful query has polynomial encoding length. The routine need not decide
membership in the unknown ball.

**Proof.** Normalize a returned normal exactly by
\(c=a/\|a\|_\infty\). This preserves the cut and has polynomial rational
encoding length. Put \(d=\min\{1,\delta\}\) and prescribe terminal volume
\[
\varepsilon=\left(\frac{d}{2n}\right)^n.
\]
Run the rounded updates in the proof of Theorem 3.2.1, stopping only on the
routine's success flag. If no flag occurs, each update retains the same ball:
the source's containment argument uses the cut inequality and does not use
the semantics of the acceptance flag. Its bit-length and contraction
arguments likewise do not use those semantics. Consequently the final
ellipsoid contains \(B(p,\delta)\) and has volume at most \(\varepsilon\).
But the ball contains
\(p+[-\delta/n,\delta/n]^n\), which has volume
\((2\delta/n)^n>\varepsilon\). This is a contradiction.

The required iteration and precision bounds are polynomial because
\[
\log(1/\varepsilon)
=n\bigl(\log(2n)+\log(1/d)\bigr).
\]
In dimension one, retain the interval half selected by each returned cut;
rational bisection gives the same conclusion. This proves the lemma. \(\square\)

The lemma is a consequence of the existing proof. It is not asserted as a
new ellipsoid result or as the literal statement of Theorem 3.2.1.

## Checks needed in the monotone-map application

These are application requirements, not extra assumptions supplied by GLS.

- The same ball must survive every rejected query. Retaining only the zero
  \(p\), or a query-dependent ball, does not give the volume contradiction.
- An outer cube cut must retain the whole ball. A proved interior margin for
  \(p\) and a sufficiently small \(\delta\) are needed. To circumscribe a cube
  \([-C,C]^n\), the rational radius \(nC\), enlarged to at least one, suffices.
- A residual test may accept points outside the retained ball. This causes no
  problem, provided every accepted point satisfies the claimed warm-start
  condition. It would be incorrect to describe that test as a membership
  oracle for the ball without proving the claim.
- A nonzero rational cubic-map value at a polynomial-bit rational query has
  polynomial encoding length. Evaluate it exactly, normalize afterward, and
  test a squared residual to avoid an unnecessary square root. A zero map
  value must be accepted before normalization.
- The rounded ellipsoid centers can leave the outer cube. The domain-cut
  branch must run before applying bounds on the map that are valid only
  inside the cube.
- Use the rounded algorithm, including its enlargement, rather than merely
  rounding the ideal update. Arbitrary rounding can lose containment or
  positive definiteness. The number of ideal iterations alone does not prove
  polynomial rational bit complexity.

## Verification scope

The primary theorem, update, three supporting lemmas, and weaker-oracle remark
were read directly in the cited chapter. The stopping-flag corollary and the
explicit volume threshold above were checked independently. No implementation,
formal proof, or repository-wide checks were used. The monotonicity, residual,
and retained-radius inequalities remain the responsibility of the main proof.
