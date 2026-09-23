# A dimension-independent sparse-SQ estimator for Newton decrements

Status: Proved; independently audited and targeted literature screen completed  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the theorem; moderate on the precise novelty claim

## Main theorem

Let \(H\in\mathbb C^{N\times N}\) be Hermitian positive definite, with at
most \(d\) nonzeros in each row, and suppose that

\[
 \kappa^{-1}I\preceq H\preceq I.                         \tag{1}
\]

Assume sparse-location/value access to the rows of \(H\), and exact sampling
and query access \(SQ(b)\) to a nonzero vector \(b\).  For
\(0<\epsilon\leq1/2\) and failure probability \(0<\zeta<1/2\), there is a
classical randomized algorithm that returns a relative-\(\epsilon\) estimate
of the squared Newton decrement

\[
 \Lambda^2=b^*H^{-1}b                                      \tag{2}
\]

using, in ideal arithmetic,

\[
 \boxed{
 \widetilde O\!\left(
   \kappa\epsilon^{-2}\log(1/\zeta)\,
   (d+1)^{\,O(\sqrt\kappa\log(1/\epsilon))}
 \right)}                                                  \tag{3}
\]

matrix and vector queries and arithmetic operations.  In particular, the
bound is independent of \(N\), and its exponential part is

\[
 \exp\!\left(
 O(\sqrt\kappa\log(d+1)\log(1/\epsilon))
 \right).                                                  \tag{4}
\]

Full \(SQ(H)\) is unnecessary.  Row-sparse access to \(H\), including the
locations of its nonzeros, is enough.  For an unnormalized public interval
\(\mu I\preceq H\preceq LI\), apply the theorem to \(H/L\); the condition
number is \(\kappa=L/\mu\), and multiply the answer by \(1/L\).

The polynomial factor in (3) improves from the immediate
\(O(\kappa^2\epsilon^{-2})\) second-moment bound to
\(O(\kappa\epsilon^{-2})\).  Positivity is essential for this improvement:
a Kantorovich inequality controls the coefficient of variation of the
one-coordinate estimator.

## Relative inverse polynomial

Put \(a=\kappa^{-1}\), and, for \(\kappa>1\), define

\[
 c=\frac{1+a}{1-a},\qquad
 x(\lambda)=\frac{1+a-2\lambda}{1-a},\qquad
 \theta=\frac{\sqrt\kappa-1}{\sqrt\kappa+1}.              \tag{5}
\]

For an integer \(m\geq1\), let

\[
 r_m(\lambda)=\frac{T_m(x(\lambda))}{T_m(c)},\qquad
 P_{m-1}(\lambda)=\frac{1-r_m(\lambda)}{\lambda}.          \tag{6}
\]

The quotient is a polynomial because \(r_m(0)=1\).  Exterior Chebyshev
growth gives

\[
 \max_{\lambda\in[a,1]}|r_m(\lambda)|
 \leq 2\theta^m.                                          \tag{7}
\]

Choose \(m\) so that \(2\theta^m\leq\eta\), where eventually
\(\eta=\epsilon/4\).  Thus

\[
 m=O(\sqrt\kappa\log(1/\eta)).                            \tag{8}
\]

One explicit admissible order is

\[
 m=\left\lceil
 \frac{\log(2/\eta)}
 {\log((\sqrt\kappa+1)/(\sqrt\kappa-1))}
 \right\rceil.                                             \tag{8a}
\]

Writing \(P=P_{m-1}(H)\), equations (6)--(7) imply

\[
 \|I-HP\|\leq\eta,
 \qquad
 (1-\eta)H^{-1}\preceq P\preceq(1+\eta)H^{-1}.            \tag{9}
\]

In particular \(P\succ0\),

\[
 1-\eta\leq\lambda_{\min}(P),\qquad
 \lambda_{\max}(P)\leq\kappa(1+\eta),\qquad
 \kappa(P)\leq\kappa\frac{1+\eta}{1-\eta}.              \tag{10}
\]

For

\[
 \Lambda_P^2=b^*Pb,
\]

the deterministic approximation error is already relative to the desired
quadratic form:

\[
 |\Lambda_P^2-\Lambda^2|\leq\eta\Lambda^2.                \tag{11}
\]

The case \(\kappa=1\) is immediate because \(H=I\).

## One-coordinate unbiased estimator

Sample \(I\) with probability

\[
 \Pr[I=i]=\frac{|b_i|^2}{\|b\|^2}
\]

and return

\[
 X=\|b\|^2\frac{(Pb)_I}{b_I}.                             \tag{12}
\]

Only indices with \(b_I\neq0\) are sampled.  The complex formula is correct
because \(|b_i|^2/b_i=\overline b_i\).  It follows that

\[
 \mathbb E X=b^*Pb=\Lambda_P^2,
 \qquad
 \mathbb E|X|^2
 \leq\|b\|^2\|Pb\|^2.                                   \tag{13}
\]

For any positive definite \(P\) with spectrum in
\([\alpha,\beta]\), the scalar Kantorovich inequality gives

\[
 \frac{\|b\|^2\|Pb\|^2}{(b^*Pb)^2}
 \leq\frac{(\alpha+\beta)^2}{4\alpha\beta}.              \tag{14}
\]

One short proof is to regard the eigenvalues of \(P\) as a random variable
\(Y\in[\alpha,\beta]\), under the spectral weights of \(b\), and maximize
\(\mathbb E[Y^2]/\mathbb E[Y]^2\).  The maximum is the right side of
(14).  By (10), for \(\eta\leq1/8\),

\[
 \frac{\mathbb E|X|^2}{(\Lambda_P^2)^2}=O(\kappa).         \tag{15}
\]

Because the target mean is real, apply median of means to
\(\operatorname{Re}X\).  Its variance is at most
\(\mathbb E|X-\Lambda_P^2|^2\), hence at most the second-moment bound in
(15).  A median of means with

\[
 O\!\left(\kappa\epsilon^{-2}\log(1/\zeta)\right)       \tag{16}
\]

samples therefore estimates \(\Lambda_P^2\) to relative error
\(\epsilon/4\).  Combining this with (11), with
\(\eta=\epsilon/4\), proves the statistical part of the theorem.

The order-\(\kappa\) relative second moment is tight for estimator (12).
Take \(P=\operatorname{diag}(\alpha,\beta)\) and choose the squared spectral
weights of \(b\) to be \(\beta/(\alpha+\beta)\) on \(\alpha\) and
\(\alpha/(\alpha+\beta)\) on \(\beta\).  Equality holds in (14), giving
\(\Theta(\beta/\alpha)\) when the condition number grows.  This is a
tightness statement for the simple one-coordinate estimator, not a general
query lower bound.  A companion
[two-by-two sign-block construction](2026-09-04-inverse-quadratic-polyfactor-lower.md)
supplies the missing algorithm-independent statement: even for two-sparse
SPD matrices, relative inverse-quadratic estimation requires
\(\Omega(\min\{N,\kappa\epsilon^{-2}\})\) randomized queries.  Its row and
column norms, Frobenius norm, and every squared-magnitude sampling
distribution are public, so the lower bound survives full matrix SQ.
For \(N\) large enough to support the requested confidence, the same family
and a Bernoulli two-point information argument give
\(\Omega(\kappa\epsilon^{-2}\log(1/\zeta))\), so the confidence logarithm in
(16) is sharp as well.

## Local evaluation cost

The affine matrix \(x(H)\) in (5) is \((d+1)\)-sparse.  A requested coordinate
of \(P(H)b\) can be evaluated by recursively expanding the Chebyshev
recurrence, or by enumerating the matrix walks of length at most \(m\) from
that coordinate.  This takes

\[
 (d+1)^{O(m)}                                              \tag{17}
\]

sparse-matrix and coordinate queries.  It never constructs a length-\(N\)
vector.  Equations (8), (16), and (17) prove (3).

This statement uses exact arithmetic, consistently with the companion
sparse-SQ sampling theorem.  A finite-precision implementation can use a
Chebyshev expansion and Clenshaw recurrence.  Since \(P\) is bounded by
\(\kappa(1+\eta)\) on the spectral interval, each Chebyshev coefficient is
at most \(2\kappa(1+\eta)\); guard precision polynomial in
\(m\log(d+1)+\log\kappa+\log(1/\epsilon)\), in addition to the input bit
length, controls the accumulated local arithmetic error.  A full bit-model
theorem would also need a precise approximate-\(SQ\) interface and is not
claimed here.

## Bilinear inverse forms

The same method gives a useful two-vector statement.  Suppose \(SQ(a)\) and
query access to \(b\) are available, and define the inverse-energy norms

\[
 A=a^*H^{-1}a,\qquad B=b^*H^{-1}b.                        \tag{18}
\]

Sampling \(I\sim |a_i|^2/\|a\|^2\) and returning

\[
 X_{a,b}=\|a\|^2\frac{(Pb)_I}{a_I}                       \tag{19}
\]

has mean \(a^*Pb\).  Moreover,

\[
 |a^*(P-H^{-1})b|\leq\eta\sqrt{AB},                      \tag{20}
\]

and, since \(P^2\preceq\kappa(1+\eta)^2H^{-1}\),

\[
 \mathbb E|X_{a,b}|^2
 \leq\|a\|^2\|Pb\|^2
 \leq\kappa(1+\eta)^2AB.                                \tag{21}
\]

Consequently, applying median of means separately to the real and imaginary
parts (and splitting the failure budget) gives, with the same query bound up
to constants, an estimate of \(a^*H^{-1}b\) to additive error

\[
 \epsilon\sqrt{(a^*H^{-1}a)(b^*H^{-1}b)}.                \tag{22}
\]

For a relative-error bilinear estimate one must assume a noncancellation
promise

\[
 |a^*H^{-1}b|\geq\gamma\sqrt{AB}.                         \tag{23}
\]

Replacing \(\epsilon\) by \(\gamma\epsilon\) in the degree and sample count
then gives relative error \(\epsilon\).  No uniform relative theorem is
possible without such an overlap promise.  The Newton-decrement case has
\(a=b\), hence \(\gamma=1\), which is exactly where positivity removes this
obstruction.

## Match to the parameterized SOCP lower bound

In the cyclic SOCP family, write

\[
 \chi=\kappa(H_0)=K^2,
\]

and let \(s\) be the sparsity of the reduced Hessian.  The normalized-tilt
construction makes the squared Newton decrement a public constant-scale
quantity whose hard additive, and hence relative, accuracy is

\[
 \epsilon_{\rm rel}
 =\Theta_k\!\left(\frac{\delta}{\chi^{1/4}}\right).        \tag{24}
\]

The lower theorem gives

\[
 Q_{\rm lower}
 =\exp\!\left(
   \Omega_k(\sqrt\chi\log s\log(1/\delta))
 \right),                                                 \tag{25}
\]

up to its displayed polynomial denominator.  The present upper theorem gives

\[
 Q_{\rm upper}
 =\exp\!\left(
   O\!\left(\sqrt\chi\log(s+1)
   \log\frac{\chi^{1/4}}{\delta}\right)
 \right)                                                  \tag{26}
\]

up to polynomial factors in \(\chi,1/\delta\).  Thus the scalar
Newton-decrement frontier is matched, within constants in the exponent, for
fixed condition number and throughout the high-accuracy regime

\[
 \log(1/\delta)=\Omega(\log\chi).                         \tag{27}
\]

Outside (27), there is an additive
\(O(\sqrt\chi\log(s+1)\log\chi)\) gap in the exponents.  It should not be
hidden: the lower construction encodes a source gap \(\delta\), whereas the
requested relative decrement precision is smaller by \(\chi^{1/4}\).

This comparison is stronger than the solution-sampling comparison.  A scalar
decrement does not require sampling the rare clock plateau, and the classical
upper bound likewise estimates the quadratic form directly, without building
an \(SQ(H^{-1}b)\) interface.

## Literature screen and novelty boundary

[Li--Sra--Jegelka](https://proceedings.mlr.press/v48/lig16.html) develop
Gauss and Gauss--Radau quadrature bounds for \(b^*H^{-1}b\), with geometric
convergence through Lanczos iterations.  Their standard sparse-matrix model
charges a full matrix-vector product and is not dimension-independent.

[Gharibian--Le Gall](https://arxiv.org/abs/2111.09079) already give the core
sampling identity behind (12): a coordinate sampled from one vector estimates
its overlap with a low-degree sparse polynomial transform in time exponential
in the degree.  Their general bounded-polynomial theorem is the closest prior
result.  The present argument should therefore not be advertised as a new
importance-sampling primitive.  The added specialization is the relative
Chebyshev inverse residual for SPD matrices, the Kantorovich
\(O(\kappa)\)-variance bound for a positive quadratic form, and its match to
the new conditioning--sparsity--accuracy lower families.

[Montanaro--Shao](https://arxiv.org/abs/2311.06999) give a general
approximate-degree framework for classical and quantum local-query estimation
of entries of \(f(H)\) for sparse Hermitian matrices, including
exponential-in-degree classical bounds.  Their input vectors are basis
vectors, and they do not state the arbitrary-\(SQ(b)\), relative positive
quadratic-form estimator or its \(O(\kappa)\) coefficient-of-variation bound.
Their framework is nevertheless a close prior result for the local-walk and
approximation-degree parts, so neither of those parts is novel by itself.

[Cifuentes--Wang--Silva--Berta--Aolita](https://arxiv.org/abs/2410.13937)
catalog classical sparse-access algorithms and hardness for inverse matrix
elements.  Their generic Hermitian inverse upper bound uses degree
\(O(\kappa\log(\kappa^2/\epsilon))\); it does not state the SPD
\(\sqrt\kappa\) quadratic-form/SQ frontier above.

The open search found no statement combining all of: sparse local access,
\(SQ(b)\), dimension-independent relative Newton-decrement estimation, the
\(\sqrt\kappa\log d\log(1/\epsilon)\) exponent, and a matching conic
lower family.  This is evidence of apparent novelty only, not a priority
guarantee.  The safest paper framing is as the matching classical half of the
new scalar lower frontier, built from known Chebyshev, importance-sampling,
and Kantorovich ingredients.  The affine-shift/box-LP lower matches the full
exponential dependence for all constant-or-smaller accuracies.  The companion
sign-block lower separately
makes the \(O(\kappa\epsilon^{-2})\) statistical factor sharp.  These are two
different endpoint families.  Distributional block averaging now gives a
single-form, same-instance lower
\(\epsilon^{-2}s^{\Omega(\sqrt\kappa)}\), but no result multiplies the full
\(\kappa\epsilon^{-2}\) prefactor by the full-accuracy local-walk exponent.

## Limits

- The theorem estimates one scalar.  It does not output the Newton direction,
  sample from that direction, or update a dense iterate.
- The dimension independence relies on \(SQ(b)\).  Coordinate access alone
  does not implement (12).
- Positive definiteness is used twice: for the
  \(O(\sqrt\kappa\log(1/\epsilon))\) residual degree and for the relative
  quadratic-form variance bound.  An indefinite system needs a different
  statement.
- The exponential dependence on local walk depth is real.  It becomes
  polynomial in \(N\) at precisely the conditioning scales exhibited by the
  cyclic lower family.
