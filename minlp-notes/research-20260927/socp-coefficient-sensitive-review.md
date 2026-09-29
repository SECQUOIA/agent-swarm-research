# Independent review of coefficient-sensitive SOCP bounds

Date: 2026-09-28. Status: the revised coefficient accounting in Sections
2--5 of the [SOCP theorem](socp-hessian-span-frontier.md) passes this
independent review. No substantive mathematical gap was found, conditional
on the stated algebraic and rational-lift inputs. The earlier conservative
bounds remain valid. This supplement does not establish novelty or repeat
the original theorem's complete source audit.

## Inputs and uniformity over integer fibers

The reviewer read the saved core note, with particular attention to its
actual definitions of the gap in equation (6) and radius in equation (10).
The [coefficient-sensitive algebraic refinement](nonconvex-finite-infimum.md#8-separate-structural-size-from-coefficient-bit-length)
and its [independent review](nonconvex-finite-infimum-review.md#6-the-coefficient-sensitive-refinement-is-valid)
supply degree \(S^{O(h+1)}\) and coefficient-bit bound
\((\tau+1)S^{O(h+1)}\). Here \(S\) measures structural size,
and \(\tau\) bounds input rational numerator and denominator bits.
This supplement treats that refinement as an accepted input.

Every integer coordinate within a supplied rational box has
\(O(\tau+1)\) bits. Substituting a boxed integer assignment into
the conic maps and squared quadratic rows uses a structurally bounded
number of additions and products. A common denominator can be taken over
structurally many input coefficients. The resulting coefficient bits are
\((\tau+1)S^{O(1)}\), uniformly over the assignments; structural
size remains polynomial in \(S\). Thus no enumeration of integer
assignments and no power of \(\tau\) depending on \(h\) is hidden
in the substitution step. The continuous Hessians remain those in the
definition of \(h\).

## The actual boxed gap and tolerance

The maximum-residual formulation includes zero, every squared cone row,
the affine inequality residuals, both signs of affine equalities, and the
negative affine cone right sides. Its minimum over the continuous box
exists and vanishes exactly for nonempty original fibers.

Adding the epigraph variable and its upper bound changes structural size
only polynomially. Absolute-coefficient bounds for that variable have
\((\tau+1)S^{O(1)}\) bits. The constraint Hessians append a zero
row and column, preserving span at most \(h\). The bounded-value
theorem therefore gives an annihilator of the residual minimum with
coefficient bits \((\tau+1)S^{O(h+1)}\).

For a positive root, removing the polynomial's initial power of its
variable leaves a nonzero integer constant term. Comparing that term with
the other coefficients gives the stated lower bound \(2^{-H-1}\).
Increasing an effective absolute integer constant absorbs the extra bit
and the structural polynomial overhead. Consequently the actual choice

\[
 \Delta=2^{-B},\qquad B=(\tau+1)S^{C(h+1)}
\]

in equation (6) is a valid uniform gap. The proof does not first choose
the much longer coarse value \(2^{-N^{C(h+1)}}\) and then ascribe
a smaller encoding length to that different number.

The affine cone right-side bound \(T\ge1\) has
\((\tau+1)S^{O(1)}\) bits on the supplied boxes. Hence the chosen
\(\epsilon=\Delta/(6T^2)\) has encoding length and inverse-logarithm
bounded by \((\tau+1)S^{O(h+1)}\). In the rational cone lift,
the right side remains nonnegative and

\[
 q_i\le((1+\epsilon)^2-1)T^2
      \le3\epsilon T^2=\Delta/2.
\]

All affine rows are retained exactly. Therefore a lifted point with
integer \(z\) gives residual minimum below \(\Delta\), forcing
that minimum to zero. Compactness supplies an exact original continuous
witness for the same integer assignment. The lifted point's displayed
continuous coordinates need not be that witness.

## Lift construction and decision cost

The [rational-lift construction](socp-rational-lift-source.md) has an
absolute polynomial dependence on cone dimension and tolerance encoding
length. Rational substitution and retention of affine rows also have
absolute polynomial bit cost. The output polyhedron's length and its
construction time are consequently

\[
                     (\tau+1)^{O(1)}S^{O(h+1)}.
\]

An exact rational LP algorithm has an absolute polynomial exponent in
that output length. This proves the same bound for pure continuous
feasibility decisions, where \(k=0\). For arbitrary \(k\), the
claim is construction of an MILP preserving the integer projection;
solving that MILP is not included in this polynomial bound. The saved
note distinguishes those consequences in Section 5. After the reviewer
requested a local qualification, the Section 4 sentence was changed to
state \(k=0\) explicitly and exclude unrestricted-dimension MILP
solution from the bound. The saved correction was independently checked.

The lift may have precision-dependent auxiliary dimension. This is
harmless because it is built after the gap is proved, then passed to a
linear algorithm. Its new dimension is never inserted into another
Hessian-span certificate bound.

## Removing the continuous box

The small-point coefficient bound, together with Cauchy's root bound,
provides the actual uniform choice

\[
                         R=2^{(\tau+1)S^{C_0(h+1)}}
\]

in equation (10), after increasing an effective absolute integer
\(C_0\). The added box meets every nonempty integer fiber. It need
not contain every feasible point, nor the global minimum-norm point;
the core theorem needs only preservation of the integer projection.

Adding the \(2n\) box rows keeps structural size polynomial in \(S\).
Their coefficient bits increase the bound to
\(\tau'\le(\tau+1)S^{O(h+1)}\). The second gap calculation has
height bound

\[
                  (\tau'+1)S^{O(h+1)}
                         =(\tau+1)S^{O(h+1)}.
\]

The structural exponents add; they are not composed with themselves.
The same accounting applies to the right-side bound \(T\), the
tolerance, and the final lift. An absolute polynomial power of their
encoding length preserves \((\tau+1)^{O(1)}S^{O(h+1)}\).
Writing the explicit large box is itself within that bound.

Since \(S\le N^{O(1)}\) and \(\tau\le N\), both boxed and
unboxed constructions have length and time \(N^{O(h+1)}\). The
same bound holds for the continuous LP decision algorithm. The former
\(N^{O((h+1)^2)}\) unboxed construction bound remains a valid
fallback when only total-length algebraic estimates are used.

The counterexample \(\|(2,y)\|_2\le y\) correctly explains why
the box and right-side bound cannot be omitted from the relative
approximation argument. Its squared residual is four, but multiplying the
right side by any factor \(1+\epsilon>1\) permits sufficiently large
positive \(y\). The revised proof supplies the needed bound before
choosing its tolerance.

The saved note also links the independently reviewed exact-witness
recovery theorem, with an integer assignment fixed when present. Its
additional integer-only objective statement follows directly from equality
of feasible integer projections: every objective depending only on \(z\)
has the same feasible objective values. A linear such objective gives an
exact MILP formulation. This does not extend the polynomial-time solution
claim to unrestricted integer dimension or to arbitrary continuous
objectives.

## Verification record

This was a proof and bit-complexity review. No algorithm implementation
was executed, and the accepted algebraic refinement was not reproved.
A targeted inline `python -` document check passed for this supplement's
local links, math delimiters, whitespace, control characters, and final
newline. No project-wide verification or CI inspection was performed.
