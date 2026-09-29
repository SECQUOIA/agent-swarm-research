# Exact algebraic witnesses for SOCP at fixed squared-Hessian span

Date: 2026-09-27; coefficient-sensitive revision: 2026-09-28.
Status: complete proof;
[independent review](socp-exact-witness-recovery-review.md) found no
mathematical gap, including in the coefficient-sensitive running-time
refinement, conditional on the stated theorem inputs.
This is an algorithmic corollary of the linked feasibility, algebraic
certificate, and recovery results. It makes no separate novelty claim for
minimum-norm selection, algebraic recognition, or common-field construction.

Exact feasibility decisions can be extended to exact feasible-point recovery
for rational second-order cone systems of fixed squared-Hessian span. The
output is an algebraic point in one explicitly represented number field.
A rational feasible point need not exist, and the rational point returned by
the feasibility proof's LP need not satisfy the original conic constraints.

## 1. Statement and dependencies

Consider the continuous system

\[
 F=\{x\in\mathbb R^n:Lx\le a,\ Ex=e,
       \ \|A_ix+b_i\|_2\le c_i^Tx+d_i\quad(1\le i\le m)\},
                                                               \tag{1}
\]

possibly intersected with a supplied finite rational box \(B\). All data
are rational and explicitly encoded; \(N\ge2\) denotes their total
binary length, including the box when supplied. Set

\[
 q_i(x)=\|A_ix+b_i\|_2^2-(c_i^Tx+d_i)^2,
 \qquad
 h=\dim_{\mathbb Q}\operatorname{span}
             \{2(A_i^TA_i-c_ic_i^T):1\le i\le m\}.             \tag{2}
\]

The equivalent quadratic description retains the affine sign rows
\(c_i^Tx+d_i\ge0\), in addition to \(q_i\le0\). The parameter
depends on the given representation; the Hessians in (2) can be indefinite.

**Recovery corollary.** A deterministic algorithm either reports
infeasibility or returns an exactly feasible point \(x^*\), represented by
a primitive integer irreducible polynomial \(P\), a rational interval
isolating one real root \(\alpha\), and rational polynomials
\(b_1,\ldots,b_n\) of degree less than \(\deg P\), with

\[
                         x_j^*=b_j(\alpha).                   \tag{3}
\]

With a supplied box, \(x^*\) is the unique minimum-norm point of
\(F\cap B\). Without a supplied box, it is the unique minimum-norm
point of \(F\). With or without a supplied box, common-field degree,
total output length, and running time are \(N^{O(h+1)}\). Section 6
proves the running-time refinement by separating structural size from
coefficient bit length.

The earlier bounds that use total encoding length throughout remain valid:
running time \(N^{O((h+1)^2)}\) with a supplied box and
\(N^{O((h+1)^3)}\) without one. Sections 2--5 retain those independent
fallback derivations before the sharper accounting.

Thus recovery is polynomial time for every fixed \(h\), without Slater,
full-dimensionality, or a rational-point promise. These are not bounds of
the form \(f(h)N^C\) with an absolute exponent \(C\). The constants
are effective consequences of the linked algebraic bounds; no practical
precision estimate is supplied.

The proof uses three separate inputs:

1. The [SOCP feasibility theorem](socp-hessian-span-frontier.md) decides a
   rational boxed system of length \(M\) and squared-Hessian span \(s\)
   in \(M^{O(s+1)}\) time. It permits arbitrary additional rational
   affine rows and no strict-feasibility promise.
2. The [nonconvex algebraic certificate theorem](nonconvex-hessian-span-frontier.md)
   gives small feasible points without a box. Over a supplied box, its
   bounded-value theorem gives an optimal point of any rational quadratic
   objective with common-field degree and coordinate minimal-polynomial
   coefficient bits \(M^{O(s+1)}\). The objective Hessian is excluded
   from \(s\).
3. The [common-field recovery theorem](constructive-common-field-recovery.md)
   constructs (3) with polynomial overhead from effective bounds on that
   joint degree and the coordinate heights, and a certified approximation
   oracle for one fixed tuple. Its recognition step is the classical
   Kannan--Lenstra--Lovász algorithm.

The sharper complexity statement also uses the
[coefficient-sensitive refinement](nonconvex-finite-infimum.md#8-separate-structural-size-from-coefficient-bit-length),
whose [independent review](nonconvex-finite-infimum-review.md#6-the-coefficient-sensitive-refinement-is-valid)
checks that coefficient heights grow linearly in input coefficient bits,
times a structural factor with exponent \(O(h+1)\). Section 6 traces
the resulting algorithmic cost; an encoding bound alone would not suffice.

These dependencies are substantive: short algebraic certificates for arbitrary
nonconvex quadratic systems alone do not give an efficient recovery algorithm.

## 2. One canonical algebraic point in a supplied box

Write \(C=F\cap B\), and decide first whether \(C\) is empty.
Assume it is nonempty. It is compact and convex, since the original norm
constraints are convex and closed. Define

\[
 x^*=\operatorname*{argmin}_{x\in C}\|x\|_2^2,
 \qquad \nu=\|x^*\|_2^2.                                  \tag{4}
\]

Existence follows from compactness. Strict convexity of the objective gives
uniqueness, including when \(C\) is lower dimensional or a singleton.

Squaring the cone rows and retaining their signs gives a rational quadratic
description of \(C\) with constraint Hessian span \(h\). Polynomial
expansion increases explicit input length by a fixed polynomial factor.
Apply the bounded-value and optimal-point theorem to the objective
\(\|x\|_2^2\). It provides an algebraic optimal point; uniqueness
forces that point to be the \(x^*\) in (4). Consequently, for effective
uniform bounds \(D,H\),

\[
 [\mathbb Q(x_1^*,\ldots,x_n^*):\mathbb Q]\le D,
 \qquad
 \operatorname{bits}(\text{coefficients of }m_{x_j^*})\le H,
 \qquad D,H\le N^{O(h+1)}.                                  \tag{5}
\]

Here \(m_{x_j^*}\) is the primitive integer minimal polynomial.
Passing from an integer annihilator to its minimal-polynomial factor retains
the bound, as recorded in the
[recognition audit](algebraic-recognition-source-review.md#2-a-bound-for-an-arbitrary-annihilating-polynomial-suffices).
The common-field bound is supplied by the optimal-point theorem itself;
it is not inferred by multiplying coordinate degrees. The norm objective
does not increase \(h\) in (5).

## 3. Rational cone queries approximate that same point

Choose a rational \(R\ge1\), of bit length polynomial in \(N\),
with \(B\subseteq[-R,R]^n\). The case \(n=0\) is decided by
rational comparisons and has the empty tuple as its feasible output; suppose
\(n\ge1\). For a rational threshold \(r\ge0\), the norm sublevel
constraint has the rational SOC representation

\[
 \|x\|_2^2\le r
 \quad\Longleftrightarrow\quad
             \|(2x,r-1)\|_2\le r+1.                       \tag{6}
\]

Indeed, the right side is nonnegative, and subtracting its square from the
squared left side gives \(4\|x\|_2^2-4r\). Its squared Hessian
with respect to \(x\) is \(8I\). Thus (6) increases the constraint
Hessian span by at most one. The threshold \(r\) is fixed rational
data in each query; no algebraic coefficient or square root of \(r\)
is introduced.

For each accuracy request \(p\ge1\), restart from the original box
\(B\), and put \(\tau=2^{-p}\). A coordinate box retained for a
previous request need not contain \(x^*\), so it is not reused. Bisect
the interval \([0,nR^2]\) for the minimum \(\nu\), using exact
SOCP decisions for

\[
                         C\cap\{x:\|x\|_2^2\le r\}.         \tag{7}
\]

Maintain endpoints \(\ell\le\nu\le u\), with a feasible upper
threshold \(u\). The initial upper threshold is feasible. A feasible
midpoint replaces \(u\); an infeasible midpoint replaces \(\ell\).
Stop when \(u-\ell\le\tau^2/16\), and set

\[
 K=C\cap\{x:\|x\|_2^2\le u\}.
\]

Then \(K\ne\varnothing\) and \(u\le\nu+\tau^2/16\).
For every \(y\in C\), optimality in (4) and differentiation along
the feasible segment from \(x^*\) to \(y\) give

\[
 \langle x^*,y-x^*\rangle\ge0,
 \qquad
 \|y-x^*\|_2^2\le\|y\|_2^2-\nu.
\]

In particular,

\[
                     \|y-x^*\|_2\le\tau/4
                     \qquad(y\in K).                       \tag{8}
\]

Next bisect the rational coordinate intervals of \(B\), preserving a
nonempty intersection with \(K\). At each step test the lower closed
half by the same exact feasibility oracle. Keep it if feasible; otherwise
keep the upper closed half. Since their union is the current box, the
retained intersection remains nonempty even when feasible points lie only
on boundaries. Store only the current two endpoints per coordinate,
replacing an old endpoint after each step. This preserves all accumulated
restrictions without adding a new row for every bisection. Stop once every
interval has width at most \(\tau\),
and let \(c\) be its rational midpoint. Some \(y\in K\) lies
in the final box, so (8) gives

\[
 |c_j-x_j^*|\le |c_j-y_j|+|y_j-x_j^*|
             \le\tau/2+\tau/4<2^{-p}.                     \tag{9}
\]

The midpoint \(c\) itself need not be feasible. Equation (9) is a
certified approximation to the same canonical point at every precision.
This argument needs neither an error bound for the original constraints
nor a procedure to repair an approximate conic point.

There are polynomially many queries in \(N+p\). All endpoints are
obtained by rational bisection, so their bit lengths, the description length
of every queried system, and the output length of \(c\) are polynomial
in \(N+p\). Each query uses the supplied box, affine refinements, and
only the extra Hessian \(8I\). The boxed decision theorem therefore
gives total approximation time

\[
                             (N+p)^{O(h+2)}.                 \tag{10}
\]

## 4. Exact recognition and common-field recovery

Kannan, A. K. Lenstra, and Lovász's
[Theorem 1.19, printed p. 241](https://www.math.cmu.edu/~af1p/Teaching/AdditiveCombinatorics/LLLL.pdf)
recovers a primitive minimal polynomial in polynomial bit time from degree
bound \(D\), coefficient magnitude bound \(2^H\), and a certified
approximation with \(O(D^2+DH)\) accuracy bits. A further approximation
selects the intended real root using a separation bound polynomial in
\(D,H\) in its exponent. Their Explanation 1.18 also covers numbers
of modulus greater than one. The
[local source audit](algebraic-recognition-source-review.md) states the
precision requirements and the root-selection argument explicitly.

Applying coordinate recognition alone would not give a convenient common
representation of the tuple. Instead apply the full
[common-field construction](constructive-common-field-recovery.md) to
(5) and the oracle (9). It searches polynomially many integer linear forms
for a primitive generator, recognizes the required linear-form values,
and obtains the coordinate polynomials by interpolation and rational
linear algebra. The theorem permits polynomially many calls with
\(p\le\operatorname{poly}(n,D,H)\), and produces total output length
\(\operatorname{poly}(n,D,H)\). All coordinates use the same selected
embedding. This gives exactly (3).

For the supplied-box input, (5) implies
\(p\le N^{O(h+1)}\). Inserting that precision into (10), and
including the polynomial recovery overhead and number of calls, gives the
original conservative bounds

\[
 \text{time}\le N^{O((h+1)^2)},\qquad
 \text{output length}\le N^{O(h+1)}.                        \tag{11}
\]

The additional factor in this running-time exponent comes from feeding
precision back into an oracle estimate expressed using total encoding
length. The output-size bound alone does not remove it. Section 6 separates
coefficient bits from structural size throughout the oracle calculation.

The returned point has an independent polynomial-time feasibility check in
its input and output lengths. Substitute the \(b_j\) into each affine
row, including supplied or derived box inequalities, each squared cone row
\(q_i\), and each sign row \(c_i^Tx+d_i\). Reduce modulo \(P\)
and determine the resulting univariate signs at the selected root; check
original affine equalities as equalities. The common-field note proves the
required polynomial bit bound, including a verifier that does not trust an
unproved irreducibility label. Checking \(q_i\le0\) without the sign
row would not verify the SOC constraint. This feasibility certificate does
not by itself certify the minimum-norm property or another optimization
claim.

## 5. Deriving a box and recovering the global minimum-norm point

Suppose no box is supplied. The small-point theorem applied to the squared
rows and their affine signs gives an effective radius

\[
 R_0=2^{N^{C_0(h+1)}},
 \qquad
 F\ne\varnothing\ \Longrightarrow\
       \exists y\in F:\|y\|_\infty\le R_0,                 \tag{12}
\]

for one absolute effective constant \(C_0\). Assume \(n\ge1\).
Use the rational box

\[
                            B_0=[-nR_0,nR_0]^n.              \tag{13}
\]

Its intersection with \(F\) is nonempty exactly when \(F\) is.
It also contains the global minimum-norm point, not merely some witness.
To see this, choose \(y\) as in (12). The nonempty closed set
\(F\cap\{x:\|x\|_2\le\|y\|_2\}\) is compact, so the
norm attains its global minimum over \(F\). Convexity gives uniqueness.
The minimizer satisfies

\[
 \|x^*\|_\infty\le\|x^*\|_2
       \le\|y\|_2\le\sqrt n R_0\le nR_0.
\]

Thus the canonical point for \(F\cap B_0\) is the global canonical
point for \(F\). A witness box \([-R_0,R_0]^n\) alone would not
justify this last assertion, since a smaller norm need not mean smaller
absolute value in every coordinate.

The encoding length \(M\) after adding (13) is
\(N^{O(h+1)}\), and the new affine rows do not change \(h\).
Applying the supplied-box construction with input length \(M\) yields

\[
 \begin{aligned}
 [\mathbb Q(x^*):\mathbb Q],\ \text{output length}
       &\le M^{O(h+1)}=N^{O((h+1)^2)},\\
 \text{time}&\le M^{O((h+1)^2)}=N^{O((h+1)^3)}.
 \end{aligned}                                               \tag{14}
\]

These conservative compositions keep the cost of deriving the box and then
requesting recognition precision explicit. They remain valid without the
coefficient-sensitive refinement used next.

## 6. Sharper running time from coefficient-sensitive accounting

Let \(S\ge2\) bound the number of scalar coefficient positions, rows,
variables, cone coordinates, and the bit lengths of their indices. Let
\(\tau_0\ge1\) bound each rational coefficient's numerator and
denominator bit lengths, including supplied box endpoints. Dense encoding
and expansion of the squared cone maps increase structural size by only
a fixed polynomial factor. After absorbing this factor, the
[coefficient-sensitive certificate bounds](nonconvex-finite-infimum.md#8-separate-structural-size-from-coefficient-bit-length)
give

\[
 D\le S^{O(h+1)},\qquad
 H\le(\tau_0+1)S^{O(h+1)}.                                 \tag{15}
\]

The same accounting applies to the boxed optimal-point construction used
in Section 2: it changes the perturbation objective, but retains the
bounded-size affine determinants and the same finite-quotient calculation.
The objective coefficients add only polynomial structural overhead and
have constant bit length for \(\|x\|_2^2\). Thus uniqueness again
identifies the bounded-degree, bounded-height optimal point with \(x^*\).
Both the joint-field degree and each coordinate height have the bounds in
(15); no product of individual coordinate degrees is taken.

First trace an exact boxed feasibility query of structural size \(S_q\),
maximum coefficient bits \(\tau_q\), and span at most \(h+1\).
The gap proof in the
[SOCP theorem](socp-hessian-span-frontier.md) uses a boxed quadratic
epigraph system. It adds one variable and polynomially many coefficient
positions. Its absolute-coefficient bounds for the epigraph variable and
cone right sides have bit length \((\tau_q+1)S_q^{O(1)}\).
The coefficient-sensitive value theorem therefore gives a separation
threshold, and a cone approximation tolerance \(\epsilon\), with

\[
                 \log(1/\epsilon)
                     \le(\tau_q+1)S_q^{O(h+1)}.              \tag{16}
\]

The rational cone lifts are constructible in time polynomial in their
cone dimensions and \(\log(1/\epsilon)\). Substitution of the
rational affine cone maps and retention of the affine rows produce an LP
whose total encoding length is at most

\[
                         (\tau_q+1)^{O(1)}S_q^{O(h+1)}.
\]

An exact rational LP algorithm has an absolute polynomial exponent in
that encoding length. Consequently the complete feasibility decision,
including construction, costs

\[
                         (\tau_q+1)^{O(1)}S_q^{O(h+1)}.       \tag{17}
\]

The constants in \(O(1)\) are independent of \(h\). The lift's
number of auxiliary variables can grow with precision, but those variables
enter the rational LP algorithm only. They are not fed back into the
structural parameter of another algebraic certificate theorem.

For the approximation algorithm, all coordinate restrictions are stored
as the current box's \(2n\) endpoints. The one norm cone adds only
\(n+1\) cone coordinates. Thus \(S_q\le S^{O(1)}\), independently
of the requested accuracy \(p\). Rational bisection gives
\(\tau_q\le(\tau_0+p+1)S^{O(1)}\). The number of bisections,
and their rational arithmetic cost, are polynomial in
\(S,\tau_0,p\), with absolute exponents. Combining this with (17)
sharpens the approximation cost to

\[
                         (\tau_0+p+1)^{O(1)}S^{O(h+1)}.       \tag{18}
\]

The common-field recovery theorem's call count, requested accuracy, and
arithmetic overhead are fixed polynomials in \(n,D,H\). Their exponents
are absolute: the primitive-generator search uses \(O(nD^2)\) candidates,
followed by at most \(n(D+1)\) sample recognitions; KLL recognition,
interpolation, and rational matrix inversion each have polynomial bit cost
in those parameters. No exponent in this conversion depends separately on
\(h\). The linear forms used for recognition are evaluated from the
rational tuple approximations outside the SOCP oracle; they add no conic
variables or rows. By (15), every requested precision and the total conversion
overhead are bounded by

\[
                            (\tau_0+1)^{O(1)}S^{O(h+1)}.
\]

Substitution into (18), and multiplication by the number of calls, preserve
this form. This proves, with a supplied box,

\[
 \text{running time and output length}
                   \le(\tau_0+1)^{O(1)}S^{O(h+1)}.           \tag{19}
\]

Without a supplied box, replace the coarse numerical radius in (12) by
\(R_0=2^{\lceil(\tau_0+1)S^{C_1(h+1)}\rceil}\), with a sufficiently
large effective absolute \(C_1\), using the small-point coefficient bound.
The geometric argument and box (13) remain valid. This choice satisfies
\(\log R_0\le(\tau_0+1)S^{O(h+1)}\). The box (13) adds only
\(2n\) affine rows. Its structural size stays polynomial in \(S\),
while its maximum coefficient bit length is
\(\tau_B\le(\tau_0+1)S^{O(h+1)}\). Substituting \(\tau_B\)
for \(\tau_0\) in (15) and (19) again preserves their form, because
only an absolute constant power is applied to \(\tau_B+1\). Writing
this explicit box is also within (19). Hence the same running-time and
output-length bound holds without a supplied box, and the common-field
degree remains \(S^{O(h+1)}\).

Finally \(S\le N^{O(1)}\) and \(\tau_0\le N\) for the original
explicit input. Equation (19) gives \(N^{O(h+1)}\) in both cases.
This improves the earlier fallback bounds by tracing actual lift and LP
costs as well as algebraic encodings; it is not a conclusion from the
certificate-size refinement alone.

## 7. Integer fibers and the need for algebraic output

For a mixed-integer model, first fix a rationally encoded integer assignment
\(z\) whose continuous fiber is nonempty. Substitution leaves a rational
SOCP in the continuous variables, with squared-Hessian span at most the
original continuous span. Apply the corollary to that fiber. If integer
variables were given finite rational bounds, every such assignment has bit
length polynomial in the original model length, so the same bounds apply
uniformly after polynomial substitution overhead.

The [SOCP projection reduction](socp-hessian-span-frontier.md) supplies an
assignment with a nonempty fiber when its MILP is solved. This note recovers
the continuous witness once that assignment is available. It does not add
an algorithm for finding an assignment when integer dimension is unrestricted.
For fixed integer dimension and fixed \(h\), combining the reduction's
algorithm with this recovery gives an exact mixed-integer feasible point.

Even \(h=1\) does not guarantee a rational continuous witness. The two
rational cone constraints in one variable

\[
                         \|(1,1)\|_2\le x,
                         \|(x,x)\|_2\le2                    \tag{20}
\]

force \(x=\sqrt2\). Their squared residuals are \(2-x^2\)
and \(2x^2-4\), with Hessians \(-2\) and \(4\), whose span
has dimension one. A representation for the sole feasible point is
\(P(T)=T^2-2\), \(\alpha\in(1,2)\), and \(b_1(T)=T\).

The recovery mechanism is already developed in the
[convex quadratic witness note](algebraic-witness-recovery.md). Its use here
depends on the separate bounded nonconvex certificate theorem and exact SOC
decision oracle. No general exact SOCP algorithm without the fixed-span
restriction follows, and no attainment or recovery theorem for an arbitrary
linear objective on an unbounded conic set is asserted.

## 8. Verification record

The proof checks canonical-point uniqueness, the common-field input bound,
the rational norm cone and its squared Hessian, the feasible bisection
invariant, approximation to one fixed point, and both complexity
compositions. Kannan--Lenstra--Lovász's primary Theorem 1.19 and Explanation
1.18 were inspected for the recognition step. An independent reviewer read
the complete draft and found no mathematical gap, conditional on the linked
theorems; the [review record](socp-exact-witness-recovery-review.md) records
the checked dependencies and boundaries.

The reviewer separately checked the coefficient-sensitive revision,
including bounded optimal-point heights, query structure independent of
accuracy, absolute polynomial lift and LP costs, common-field conversion,
and the actual replacement radius. It found no substantive gap. The earlier
encoding-length compositions remain recorded as valid fallback bounds.

A targeted inline `python -` check passed for this file's local-link
existence, trailing whitespace, control characters, final newline, and paired
math delimiters. The same command used exact SymPy arithmetic to check the
norm-cone residual and Hessian in (6), and to verify that (20) has exactly
the feasible set \(\{\sqrt2\}\) with the stated Hessians. These
checks support the displayed identities, not the general theorem. No
project-wide verification or CI inspection was performed. After the
complexity revision, a targeted inline `python -` check of the updated
note passed the document checks again and checked sequential equation tags;
the review file passed its own targeted document checks.
