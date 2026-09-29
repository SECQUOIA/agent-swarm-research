# Certified positive cubic-root comparison reduces to one PosSLP instance

Date: 2026-09-28. Status: proved and passed
[fresh independent adversarial review](posslp-certified-cubic-root-upper-independent-review.md).
The upper-bound method is an explicit adaptation of
classical algebraic separation and Newton approximation arguments. No
independent novelty is claimed for the upper bound.

Consider a triangular circuit
\[
 \xi_i^3=c_i+\sum_{j<i}(a_{ij}\xi_j+b_{ij}\xi_j^2),
 \qquad i=1,\ldots,n,                                      \tag{1}
\]
with rational coefficients, positive rational intervals
\([L_i,U_i]\), and a designated output \(\xi_o\). Assume that
direct signed interval evaluation of the right-hand side of each gate
lies in \([L_i^3,U_i^3]\). All cube roots are real cube roots.
The interval condition ensures inductively that every root is positive
and belongs to its supplied interval.

**Theorem.** Given (1), its intervals, and a rational threshold \(r\),
one can construct in deterministic polynomial time a division-free
integer arithmetic circuit whose output is positive if and only if
\(\xi_o>r\). Equality at the threshold is allowed. The construction
uses one final PosSLP comparison and makes no oracle calls while
constructing its circuit.

The interval condition is polynomial-time checkable by rational
arithmetic. Therefore the theorem can be read either as a promise
reduction or as a reduction of the language that rejects malformed or
uncertified inputs. The upper bound needs only the resulting positive
bounds on the actual roots, but the stronger interval condition gives a
convenient verifiable input format.

Together with the separately reviewed
[hardness construction](posslp-certified-cubic-root-reduction.md), this
classifies comparison in that restricted circuit language as
PosSLP-complete under polynomial-time many-one reductions. That
classification does not rely on an unproved mathematical conjecture.
It does not give a
PosSLP upper bound for arbitrary strongly convex quartic feasibility.

## Encoding conventions

Let \(L\ge2\) be the total binary input length, enlarged by a constant
if necessary. Use an ordinary explicit encoding in which

- \(n\le L\);
- every printed numerator and positive denominator has absolute value at
  most \(2^L\);
- the sum of the bit lengths of all printed denominators is at most
  \(L\).

These conditions can equivalently be obtained by choosing a
polynomially equivalent size parameter from the actual encoding.
Every actual root then satisfies
\[
                     2^{-L}\le\xi_i\le2^L.                \tag{2}
\]
Sharing in the circuit is retained throughout. No exponentially long
rational number or polynomial is expanded.

## An elementary uniform separation bound

Let \(D\) be the product of all denominators in the circuit
coefficients and in \(r\), excluding the interval endpoints if desired.
Thus \(1\le D\le2^L\). Set \(\alpha_i=D\xi_i\).
Equation (1) becomes
\[
 \alpha_i^3=D^3c_i+
       \sum_{j<i}\bigl(D^2a_{ij}\alpha_j+
                          Db_{ij}\alpha_j^2\bigr).        \tag{3}
\]
Every displayed rational scalar on the right is an integer. Induction
and transitivity of integrality show that every \(\alpha_i\) is an
algebraic integer. This uses one common scale \(D\) for the whole
triangular circuit.

Put \(K=\mathbb Q(\xi_1,\ldots,\xi_n)\). The tower law gives
\([K:\mathbb Q]\le3^n\). For every complex embedding of \(K\),
all conjugate root coordinates have absolute value at most
\[
                M=(2L+1)2^L\le2^{3L}.                   \tag{4}
\]
Indeed, if all previous magnitudes are at most \(M\), the next
radicand has magnitude at most
\(2^L(1+LM+LM^2)\le(2L+1)2^L M^2=M^3\).
The same argument applies to the first gate.

If \(\xi_o\ne r\), then
\(\beta=D(\xi_o-r)\) is a nonzero algebraic integer in \(K\).
Its norm is a nonzero integer. Each conjugate has magnitude at most
\(D(M+|r|)\le2^{4L+1}\). Isolating the actual real embedding
in the norm product proves
\[
 |\xi_o-r|\ge
 2^{-L-(4L+1)(3^L-1)}\ge 2^{-2^{6L}}=:g.                 \tag{5}
\]
For the last inequality, \(4L+2\le2^{2L}\) and
\(3^L\le2^{2L}\) for \(L\ge2\), so the exponent on the
left is at most \((4L+2)3^L\le2^{4L}\le2^{6L}\).
The rational number \(g\) has a circuit of size \(O(L)\):
start with \(1/2\) and square it \(6L\) times.

The interval bounds were not used to bound complex conjugates. In
particular, no claim that conjugates lie in the supplied real intervals
is needed.

## A fixed number of Newton steps

For a positive rational \(z\), suppose its positive cube root
\(\eta\) lies in \([2^{-(L+1)},2^{L+1}]\). Begin at
\(x_0=2^{L+1}\) and iterate
\[
                    x_{t+1}=\frac{2x_t+z/x_t^2}{3}.       \tag{6}
\]
Every iterate is positive and at least \(\eta\). For the relative
error \(e_t=(x_t-\eta)/\eta\ge0\), direct algebra gives
\[
 e_{t+1}=\frac{e_t^2(3+2e_t)}{3(1+e_t)^2}
       \le e_t^2,
 \qquad e_{t+1}\le\frac23e_t.                            \tag{7}
\]
Initially \(e_0\le2^{2L+2}\). After \(4L+6\) steps the
second bound and \((2/3)^2<1/2\) give \(e_t\le1/2\).
After a further \(10L\) steps the first bound gives
\[
 |x_{14L+6}-\eta|
      \le 2^{L+1-2^{10L}}=:\varepsilon.                  \tag{8}
\]
These are exact rational operations represented by an arithmetic
circuit. They are not floating-point operations, and the exponentially
many accurate bits are not printed.

## Error propagation through the triangular circuit

Evaluate the gates in order. At gate \(i\), use the previously
constructed rational approximations \(\widehat\xi_j\) to form
\[
 \widehat z_i=c_i+
          \sum_{j<i}(a_{ij}\widehat\xi_j+
                             b_{ij}\widehat\xi_j^2),
\]
and define \(\widehat\xi_i\) by the \(14L+6\) Newton
steps in (6), with \(z=\widehat z_i\).

Let \(E_i=\max_{j\le i}|\widehat\xi_j-\xi_j|\) and
\(E_0=0\). If \(E_{i-1}\le1\), then
\(|\widehat\xi_j|\le2^{L+1}\), and
\[
 |\widehat z_i-\xi_i^3|
 \le L\bigl(2^L+3\cdot2^{2L}\bigr)E_{i-1}
 \le2^{4L}E_{i-1}.                                      \tag{9}
\]
When \(E_{i-1}\le2^{-7L-1}\), this is at most
\(2^{-3L-1}\). Consequently \(\widehat z_i>0\), and its
positive cube root \(\eta_i\) lies in
\([2^{-(L+1)},2^{L+1}]\). The derivative of the cube-root
function on the segment between \(\widehat z_i\) and
\(\xi_i^3\) is at most \(2^{2L+2}\). Equations
(8)--(9) imply
\[
 E_i\le2^{6L+2}E_{i-1}+\varepsilon
       \le(2^{6L+2}+1)^i\varepsilon
       \le2^{(6L+3)i}\varepsilon.                       \tag{10}
\]
The first right-hand side also bounds \(E_{i-1}\), as required
by the definition of \(E_i\). The stated geometric bound follows
by induction, using \(2^{6L+2}+1\le2^{6L+3}\).

For completeness, the last displayed bound is small enough to justify
every previous use of positivity. For \(i\le n\le L\), its
base-two exponent is at most
\[
                  6L^2+4L+1-2^{10L}.
\]
The elementary inequalities
\[
 2^{10L}-2^{6L}\ge2^{6L}\ge20L^2
 \quad\text{and}\quad
 6L^2+11L+5\le20L^2 \qquad(L\ge2)
\]
show simultaneously that this exponent is at most
\(-7L-1\) and at most \(-2^{6L}-3\). Thus the induction
never leaves its claimed range, and
\[
                        E_n\le g/8.                    \tag{11}
\]

## One comparison, including the equality case

Construct the rational circuit output
\[
                  q=\widehat\xi_o-r-g/2.               \tag{12}
\]
If \(\xi_o>r\), (5) and (11) give \(q\ge3g/8>0\).
If \(\xi_o=r\), they give \(q\le-3g/8<0\).
If \(\xi_o<r\), they give \(q\le-11g/8<0\).
In particular \(q\) is never zero on a certified input, and its
sign answers the desired strict comparison. Reversing the threshold
shift gives the analogous test for a weak comparison.

All rational divisions can be removed with polynomial overhead.
Represent every circuit value by a numerator-denominator pair
\((N,D)\), with integer circuit outputs and \(D>0\).
Addition, subtraction and multiplication use the usual pair formulas.
For a division \(a/b\), where \(b\ne0\), use
\[
 (N_a,D_a),(N_b,D_b)
 \longmapsto (N_aD_bN_b,\ D_aN_b^2).                    \tag{13}
\]
The new denominator is positive, so this formula does not require a
sign test. All divisions in (6) have nonzero divisors by the preceding
proof. Constants given in binary can be built from zero and one by
binary doubling and addition. Retain all shared nodes.

The construction uses \(O(L)\) Newton steps for each of at most
\(L\) root gates, plus the explicit radicand evaluations and constant
circuits. It therefore has polynomial size and is printed in polynomial
time. The numerator in (13), applied to (12), is the required single
PosSLP instance. For an invalid interval certificate, print a fixed
negative integer instead.

## Prior work and the scope of the contribution

The relevant upper-bound technique is classical. Allender, Bürgisser,
Kjeldgaard-Pedersen and Miltersen,
[*On the Complexity of Numerical Analysis*](https://people.cs.rutgers.edu/~allender/papers/slp.pdf),
Section 1.4 and Proposition 1.1, explain the reduction from the sum of
square roots to PosSLP using Tiwari's polynomial-size Newton
approximation circuits. Their Proposition 1.3 also uses separate
numerator and denominator circuits. Section 3, before Theorem 3.9,
discusses small rational circuits for accurate algebraic-function
approximation. These passages were read directly in the author PDF and
the repository's 2009 full text. They establish the method's precedent;
their displayed sum-of-square-roots input does not by itself specify the
nested cubic language in (1).

Tiwari's 1992 article, *A problem that is easier to solve on the
unit-cost algebraic RAM*, is cited here through the preceding primary
paper. Its own full text was not obtained in this audit, so no claim is
made about the exact limits of its original theorem.

Balaji, Nosan, Shirmohammadi and Worrell,
[*Identity Testing for Radical Expressions*](https://arxiv.org/abs/2202.07961),
study identity testing for arithmetic circuits over unnested radical
inputs. That language and its equality question differ from the nested
root gates and sign question above; its presence also cautions against
equating every radical-comparison problem with this restricted one.
The repository's source summary and introduction were checked for this
scope comparison; no use of that paper's algorithm is made here.

The useful consequence is a matching classification for the root
circuit language used in the quartic hardness reduction. The upper
bound alone should be treated as a tailored proof of a standard
separation-and-approximation argument, rather than as a new general
theorem about radical circuits. Whether this exact restricted
classification has appeared under different terminology remains open
in the literature audit.

## Verification and limitations

This version was checked by hand for the common integral scale, the
complex-conjugate bound, the norm argument, Newton's two error bounds,
propagation, and fraction conversion. The fresh reviewer independently
reconstructed those arguments and checked the primary literature scope.
Their separate checker, run as
`python research-20260927/check_posslp_upper_independent_review.py`,
passed exact symbolic Newton and fraction identities and checked the
constant margins for \(2\le L\le128\). The finite range check does
not replace the all-\(L\) inequalities in the proof. The author read
the review but did not rerun that independent checker. The targeted
command `git diff --check --
research-20260927/posslp-certified-cubic-root-upper.md` passed before
this status update. No project-wide verification or CI inspection was
performed.

No polynomial bound on expanded rational numerator sizes is asserted.
No inverse-polynomial separation of \(\xi_o\) from \(r\) is
assumed. Positivity and the printed interval bounds are essential to
the uniform Newton initialization used in this proof. More general
root degrees, singular radicands, or unspecified real branches require
separate arguments. The result gives an exact complexity comparison,
not a practical numerical algorithm or an NP-hardness theorem.
