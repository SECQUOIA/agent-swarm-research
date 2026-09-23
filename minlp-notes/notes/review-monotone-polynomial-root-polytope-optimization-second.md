# Second independent audit of exact monotone polynomial root optimization

Date: 2026-09-05. Reviewer: `spatial_sdp_review`.

**Verdict: PASS after two clarifications already applied.** The [candidate](monotone-polynomial-root-polytope-optimization.md) proves polynomial bit-time exact optimization under its strict-monotonicity and bracket promises, including dense variable degree, unrestricted polytope dimension, repeated polynomial roots, and lower-dimensional polytopes. The output polynomial has polynomial coefficient **bit length**, rather than necessarily polynomial coefficient magnitude. The author corrected this wording and added the uniform encoding invariant for lexicographic LP extraction. No separation constant or algorithmic step needs changing.

## 1. Threshold equivalence and vertex attainment

For every fixed theta, continuity, strict increase on the nontrivial bracket, and the endpoint signs imply exactly one root in that bracket. Strict increase need not imply a positive derivative everywhere; the proof uses no such stronger property.

For a rational z in the bracket, the root is at least z exactly when `H(z,theta)<=0`, and at most z exactly when `H(z,theta)>=0`. Taking the appropriate existential statement over the compact polytope gives the two LP tests with exactly the displayed signs. Equality is correctly retained. Polynomial evaluation at a rational z has polynomial bit complexity in the dense degree, coefficient lengths, and the length of z.

Every point of the nonempty bounded polytope is a convex combination of finitely many vertices. At that point's root, its H value is the same combination of the vertex H values, because the dependence on theta is affine, including h0. Some vertex value is nonpositive and another is nonnegative. Their roots therefore bracket the given root. Consequently a smallest and a largest vertex root are global extrema. This proves existence without any hidden continuity assumption about an optimizer. It does not assert that all optimizing parameter vectors must be vertices.

## 2. Common vertex polynomial bounds

A vertex has t linearly independent active inequality normals. Otherwise a nonzero direction orthogonal to every active normal, and a sufficiently small displacement in either direction, would contradict extremality. This argument also applies when the polytope is lower dimensional.

After clearing each row's denominators, Cramer's rule and expansion of the determinant give a common nonzero denominator d and numerators bounded by `Delta=t! C^t`. Common polynomial coefficient denominator R then gives

```
R d H(q,theta_vertex)=d (R h0(q))+sum_j n_j (R hj(q)).
```

Each coefficient has magnitude at most `(t+1)Delta P0`. A negative d has no effect on this magnitude bound or on the roots. The resulting polynomial cannot be identically zero because H is strictly increasing on a nontrivial interval. It has degree at least one and at most D, even when leading coefficients cancel at particular vertices.

Clearing denominators by products requires only polynomially many bits: the sum of their original bit lengths bounds the bit length of the product. The same observation applies to C, R, P0, and the factorial/power expression for Delta. H0 may have exponential numerical magnitude, but its binary encoding length is polynomial. This is why the theorem statement must use coefficient bit length or logarithmic height.

## 3. Squarefree factor bound and distinct-root separation

Let F and G be any two nonzero integer vertex polynomials. Their product Q has degree at most 2D and coefficient height at most `(D+1)H0^2`, by the convolution formula. This includes F=G and different polynomials sharing roots.

The primitive squarefree part S is an integer divisor of Q: factor the primitive part of Q into primitive irreducible integer factors and retain each once. Gauss's lemma shows that the quotient remains integral. No monic normalization over the rationals is being mistaken for an integer factor.

I directly checked Theorem 1.2 of Nahshon and Shpilka's primary research article, which states the required Mignotte inequality for integer factors: the coefficient l1 norm of a factor h is at most `2^deg(h)` times the coefficient l2 norm of the original polynomial f. Applying this with h=S, and bounding the l2 norm of Q by the square root of its coefficient count times its height, proves the candidate's displayed bound for Hs. [Primary article, Theorem 1.2](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/new-bound-on-cofactors-of-sparse-polynomials/2CADDB77D2E5CBFB7B803CCCAC49D2FD).

Set `Bstar=2(1+Hs)`. All complex roots of S have modulus at most `1+Hs` by Cauchy's bound; its leading coefficient is a nonzero integer. If S has degree n at least two, the discriminant is a nonzero integer. Taking absolute values in its root-product formula gives

```
1 <= Hs^(2n-2) delta^2 Bstar^(n(n-1)-2).
```

The selected delta can be the distance between any distinct pair of roots. Complex roots among the remaining factors satisfy the same bound. Since `Hs<=Bstar`, rearrangement yields

```
delta >= Bstar^(-(n^2+n-4)/2).
```

For `n<=2D` and `D>=1`, `(n^2+n-4)/2<=2D^2+D-2<=4D^2`. Therefore `sigma=Bstar^(-4D^2)` is a valid, deliberately conservative lower bound. If S has degree one, there are no distinct roots of this pair to separate. Squarefree extraction correctly handles repeated roots, including a monotone polynomial such as q cubed whose derivative vanishes at its root.

The exponentiation defining sigma creates a rational number of polynomial bit length: `log Hs=O(D+log(D+1)+log H0)` and `log(1/sigma)=O(D^2 log Bstar)`. Dense encoding is essential to counting numerical D as polynomial input size. No polynomial dependence on the logarithm of a sparsely encoded degree is asserted.

## 4. Exact recovery and polynomial LP size

The maximum-root bisection retains a bracket containing the true maximum. At a true LP test, raising the lower endpoint preserves `lower<=maximum`; at a false test, lowering the upper endpoint preserves `maximum<upper`. Initialization and equality cases work even when every root equals an endpoint. The number of bisections is bounded by a polynomial because both `log(1/sigma)` and the binary size of the initial interval length are polynomial.

At the final lower endpoint l, a vertex minimizing H has root at least l. Its root cannot exceed the global maximum. The maximum itself is a vertex root, so both roots belong to the uniformly separated family. Their distance is less than sigma, which forces equality. The minimum-root construction reverses the bracket test and uses a maximizing vertex at the upper endpoint; its inequalities are also correct.

Lexicographic extraction after imposing the rational optimal objective value returns a vertex of the original P. Each successive optimum set is a face of the preceding face, hence a face of P. After minimizing all coordinates, the final face is a singleton. Every intermediate face contains a vertex of P, so every newly fixed coordinate value is a coordinate of an original vertex and has the original Cramer bit bound. The initial objective optimum is the rational objective evaluated at an original vertex and likewise has polynomial size. This gives a uniform size bound on all added equalities, rather than relying on repeated composition of generic polynomial LP size bounds. I recommended making this invariant explicit in the candidate.

Exact rational LP is therefore sufficient throughout. The algorithm does not require an algebraic LP oracle, an approximation gap in the LP objective, a derivative lower bound, or enumeration of parametric LP bases.

## 5. Root encoding and scope

Once the rational optimizing vertex is known, substituting it gives a nonzero integer polynomial of polynomial coefficient bit length. Standard univariate real root isolation is polynomial in the degree and bit length; repeated roots can first be removed by a polynomial gcd. The claimed final isolation step is valid.

There is also a simpler output option here. Evaluate the endpoint values exactly. If an endpoint is a root, return that rational value. Otherwise the given rational bracket already contains exactly one real root of the selected polynomial by the promise. Its squarefree polynomial together with this bracket is an ordinary isolating representation, so there is no need to isolate all its other roots. This optional simplification was sent to the author.

The strict-monotonicity condition is a promise, not an algorithmically verified property in this result. A constant polynomial cannot meet it, so D=0 is excluded by the assumptions. The t=0 case reduces to the promised single polynomial. A nonempty bounded rational polytope, including a singleton, has the needed vertices. Dense variable degree causes no additional issue. Piecewise polynomials and unknown branches remain outside the stated theorem.

This is a proof and imported-bound audit, not a novelty determination. The factor bound and LP tools are classical; whether this precise combination is already stated in root-optimization literature remains a separate source-review question. No numerical test is needed to establish the uniform separation argument: its constants and encoding bounds were checked directly above.

## Addendum: fixed rational breakpoints

The subsequently added Section 6 piecewise-polynomial extension also passes. The partition is fixed independently of theta, and continuity makes the LP coefficient function at a breakpoint unambiguous on P. At each fixed test point H is still affine in theta, so both threshold equivalence and vertex attainment remain valid.

Use a common coefficient denominator and height bound over every supplied piece. After deleting zero-width pieces, strict increase makes the specialized polynomial on every piece nonconstant for every vertex profile. An interior root belongs to its piece polynomial; a breakpoint root belongs to an adjacent nonzero piece polynomial by continuity. The same separation argument therefore bounds every distinct pair of possible vertex roots, even if they arise from different pieces. Dependence on the number of pieces enters through total input size and coefficient bounds, not through a product of their possible active combinations.

The final LP vertex recovery is unchanged. At that vertex, exact signs at the ordered rational breakpoints either identify an exact rational root or locate its unique positive-width sign-changing interval. The corresponding polynomial and interval give the exact algebraic encoding. Breakpoint endpoints of the overall bracket are included in these tests. All arithmetic is polynomial in the total dense piecewise input. No further correction is needed.
