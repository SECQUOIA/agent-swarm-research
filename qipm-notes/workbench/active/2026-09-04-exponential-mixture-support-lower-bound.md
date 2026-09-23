# A sharp support lower bound for exponential-recourse compression

Status: Proved; independently audited; targeted literature screen completed  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the theorem; moderate on novelty

## Result

Fix \(K>0\).  For a positive measure \(\mu\) on \([-1,1]\), write

\[
 M_\mu(z)=\int_{-1}^1 e^{zx}\,d\mu(x),
 \qquad |z|\leq K.
 \tag{1}
\]

Let \(\mathcal P_m[-1,1]\) be the positive measures supported on at most
\(m\) points of \([-1,1]\), and define the worst-case relative compression
error

\[
 \mathcal E_m(K)=
 \sup_{\mu\in\mathcal P[-1,1]}
 \inf_{\nu\in\mathcal P_m[-1,1]}
 \sup_{|z|\leq K}
 \frac{|M_\mu(z)-M_\nu(z)|}{M_\mu(z)}.
 \tag{2}
\]

Here the outer class consists of probability measures.  Requiring the
approximating measure \(\nu\) to be a probability measure or merely a finite
positive measure gives the same asymptotic conclusion.  Then

\[
 \boxed{
 -\log \mathcal E_m(K)=2m\log m+O_K(m).}
 \tag{3}
\]

The upper bound is furnished by \(m\)-node Gaussian quadrature.  The lower
bound already holds for the single, fixed source

\[
 d\mu_0(x)=\frac12\mathbf 1_{[-1,1]}(x)\,dx,
 \qquad
 M_{\mu_0}(z)=\frac{\sinh z}{z}.
 \tag{4}
\]

More explicitly, for every fixed \(K>0\) there is an \(m_0(K)\) such that, for
all \(m\geq m_0(K)\), every positive
\(m\)-atomic \(\nu\) on \([-1,1]\) obeys

\[
 \sup_{|z|\leq K}
 \frac{|M_{\mu_0}(z)-M_\nu(z)|}{M_{\mu_0}(z)}
 \geq
 \frac{e^{-K}}{2(2m+1)16^m}
 \left(\frac{K}{8em}\right)^{2m}.
 \tag{5}
\]

There is also a finite-scenario version with only \(m+1\) source atoms:
replace \(\mu_0\) by its \((m+1)\)-node Gauss--Legendre rule.  The proof below
is unchanged because that rule has the same moments through degree \(2m\).

Consequently, if \(m_*(\epsilon,K)\) is the least support size that guarantees
relative error at most \(\epsilon\) for every source probability measure,
then, for fixed \(K>0\),

\[
 \boxed{
 m_*(\epsilon,K)=
 \left(\frac12+o(1)\right)
 \frac{\log(1/\epsilon)}{\log\log(1/\epsilon)}.}
 \tag{6}
\]

Thus the fixed-\(K\) support order in the Gaussian-quadrature exponential-cone
compiler is worst-case optimal, including the leading constant after
logarithmic inversion.  The \(O_K(m)\) remainder in (3) is proved against
positive atomic mixtures with nodes in the permitted slope interval, not
only moment-matching or Gaussian rules.  The leading constant remains
optimal even against arbitrary real competitor nodes, as (6c)--(6d) show.

### Joint growing-sector corollary

The same proof is uniform in a varying sector width.  If \(K=K_m>0\) and
\(m/K_m\to\infty\), then

\[
 -\log \mathcal E_m(K_m)
 =2m\log\!\left(\frac{m}{K_m}\right)+O(m+K_m).
 \tag{6a}
\]

Indeed, the explicit lower bound (5) gives the upper side of (6a), while
the Gaussian bound (18) gives the lower side.  For the only additional
tail comparison, \(m/K\to\infty\) implies \(K<4m+1\) eventually, and (12)
obeys

\[
 \log R_{m,K}
 \leq -4m\log\!\left(\frac{m}{K}\right)+O(m+K).
\]

Since \(\log B_{m,K}=-2m\log(m/K)+O(m)\), it follows that
\(\log(R_{m,K}/B_{m,K})\to-\infty\), and hence \(R_{m,K}=o(B_{m,K})\).
The displayed relation for
\(\log R_{m,K}\) is deliberately an upper bound: retaining the extra
\(K/(4m+1)\) factor in (12) can make it strictly smaller when \(K\to0\).

Consequently, in the joint regime
\[
 L:=\log(1/\epsilon),\qquad
 L/K\to\infty,\qquad
 \frac{L}{W(L/(2K))}\to\infty,
\]
the least guaranteed support size satisfies

\[
 \boxed{
 m_*(\epsilon,K)
 =(1+o(1))\frac{L}{2W(L/(2K))},}
 \tag{6b}
\]

where \(W\) is the principal Lambert function.  At this value
\(m_*/K\sim [L/(2K)]/W(L/(2K))\to\infty\), so (6a) applies, its
\(O(m+K)\) remainder is \(o(L)\), and solving
\(L\sim2m\log(m/K)\) gives (6b).  For fixed \(K\), (6b) reduces to (6).
The last growth condition only excludes the integer-support regime in which
\(K\) shrinks exponentially fast in \(L\) and the predicted support remains
bounded; it follows, for example, from \(\log(1/K)=o(L)\).  Without such a
condition the continuous Lambert-\(W\) equivalent need not hold because
integer rounding is no longer lower order.

### Arbitrary real competitor nodes

The leading fixed-sector law does not in fact require the competitor nodes
to remain in \([-1,1]\).  Let \(\mathcal E_m^{\mathbb R}(K)\) be (2) with
the inner infimum enlarged to all finite positive measures on \(\mathbb R\)
supported on at most \(m\) points.  For every fixed \(K>0\),

\[
 \boxed{
 -\log\mathcal E_m^{\mathbb R}(K)
 =2m\log m+O_K(m\log\log m).}
 \tag{6c}
\]

Consequently,

\[
 m_*^{\mathbb R}(\epsilon,K)
 =\left(\frac12+o(1)\right)
 \frac{\log(1/\epsilon)}{\log\log(1/\epsilon)}.
 \tag{6d}
\]

Here is the strengthened obstruction.  For arbitrary real support points
\(\xi_j\), including appended roots if needed, define

\[
 r(x)=\prod_{j=1}^m\frac{x-\xi_j}{1+|\xi_j|}
     =\sum_{k=0}^m b_kx^k .
\]

Each factor has coefficient \(\ell_1\)-norm one, so the coefficient
\(\ell_1\)-norm of \(r^2\) is at most one.  If
\(\bar\xi_j\) is \(\xi_j\) clipped to \([-1,1]\), then, pointwise for
\(x\in[-1,1]\),

\[
 \left|\frac{x-\xi_j}{1+|\xi_j|}\right|
 \geq \frac{|x-\bar\xi_j|}{2}.
\]

The monic-Legendre extremality used in (9) therefore gives

\[
 \int r(x)^2\,d\mu_0(x)
 \geq \frac{1}{(2m+1)16^m}.
 \tag{6e}
\]

Since \(r\) vanishes on the support of the competitor, the same calculation
as in (10), now with coefficient norm at most one, singles out some
\(0\leq k\leq2m\) for which

\[
 |F^{(k)}(0)|\geq\eta_m
 :=\frac{1}{(2m+1)16^m}.
\]

It remains to replace the bounded-support Taylor estimate.  In the
nontrivial case of relative error below \(1/2\), endpoint evaluation gives

\[
 \int e^{K|x|}\,d|\mu_0-\nu|(x)
 \leq 4e^K.
 \tag{6f}
\]

Indeed, \(e^{K|x|}\leq e^{Kx}+e^{-Kx}\), and each of
\(M_\nu(K)\) and \(M_\nu(-K)\) is at most \(3e^K/2\).
Fix \(a=1/4\), let
\[
 n=\left\lceil4m\log(m+1)\right\rceil,
\]
and Taylor truncate \(F\) at degree \(n\).  For \(|z|\leq aK\), putting
\(t=K|x|\) and summing the exponential series gives

\[
 \left|e^{zx}-\sum_{j=0}^n\frac{(zx)^j}{j!}\right|
 \leq e^t\frac{a^{n+1}}{1-a}.
\]

Thus (6f) bounds the uniform Taylor remainder by
\[
 \frac{4e^K a^{n+1}}{1-a}.
 \tag{6g}
\]

The higher-order Markov inequality on \([-aK,aK]\) gives, for the derivative
selected above,

\[
 \|P_n\|_{[-aK,aK]}
 \geq
 \eta_m
 \left(\frac{2aKm}{en^2}\right)^{2m}
 =\exp\{-2m\log m-O_K(m\log\log m)\}.
 \tag{6h}
\]

For completeness, the common last expression in (6h) is valid for every
\(0\leq k\leq2m\): once \(m\) is large, the logarithm of
\((aKk/(en^2))^k\) decreases with \(k\), and the \(k=0\) case is larger
still.  The logarithm of (6g) is at most
\(-4(\log4)m\log m+O_K(m)\), so (6g) is \(o\) of (6h).  Dividing by
\(M_{\mu_0}(z)\leq e^K\) proves the lower-error side of (6c).  Its other
side follows from the same in-range Gaussian rule as (18).  Inverting (6c)
proves (6d).

## Lower bound

Let \(\nu\) have distinct support points \(\xi_1,\ldots,\xi_s\), where
\(s\leq m\).  Append arbitrary roots in \([-1,1]\) if \(s<m\), and form the
monic support-annihilating polynomial

\[
 p(x)=\prod_{j=1}^m(x-\xi_j),
 \qquad
 p(x)^2=\sum_{k=0}^{2m}a_kx^k.
 \tag{7}
\]

The appended roots need not be support points.  Since all roots are in
\([-1,1]\),

\[
 \sum_{k=0}^{2m}|a_k|
 \leq \prod_{j=1}^m(1+|\xi_j|)^2
 \leq4^m.
 \tag{8}
\]

Among monic degree-\(m\) polynomials, the monic Legendre polynomial minimizes
the \(L_2(\mu_0)\) norm.  The standard Legendre polynomial \(P_m\) has leading
coefficient

\[
 L_m=2^{-m}\binom{2m}{m}\leq2^m
\]

and squared \(L_2(\mu_0)\) norm \(1/(2m+1)\).  Therefore

\[
 \int p(x)^2\,d\mu_0(x)
 \geq \frac{1}{(2m+1)L_m^2}
 \geq\frac{1}{(2m+1)4^m}.
 \tag{9}
\]

Put \(F=M_{\mu_0}-M_\nu\).  Because \(p\) vanishes on the support of
\(\nu\), equations (8)--(9) imply

\[
 \sum_{k=0}^{2m}a_kF^{(k)}(0)
 =\int p^2\,d(\mu_0-\nu)
 =\int p^2\,d\mu_0,
\]

so, for some \(0\leq k\leq2m\),

\[
 |F^{(k)}(0)|\geq
 \eta_m:=\frac{1}{(2m+1)16^m}.
 \tag{10}
\]

This is the moment-rank obstruction.  What remains is to convert it to a
uniform error on a fixed real interval without losing another factor
\(\exp(\Theta(m\log m))\) in the exponent.

Take \(n=4m\), and let

\[
 P_n(z)=\sum_{j=0}^n\frac{F^{(j)}(0)}{j!}z^j.
 \tag{11}
\]

First suppose that the relative error in (5) is less than \(1/2\); otherwise
(5) is automatic for large \(m\).  Evaluation at \(z=0\) then shows that the
mass of \(\nu\) is at most \(3/2\).  Hence the total variation of
\(\mu_0-\nu\) is at most \(5/2\), and the exponential Taylor remainder gives

\[
 \|F-P_n\|_{[-K,K]}
 \leq R_{m,K}:=
 \frac52 e^K\frac{K^{n+1}}{(n+1)!}.
 \tag{12}
\]

For a polynomial \(Q\) of degree at most \(n\), the higher-order Markov
inequality on \([-K,K]\) is

\[
 \|Q^{(k)}\|_{[-K,K]}
 \leq K^{-k}
 \frac{n^2(n^2-1^2)\cdots(n^2-(k-1)^2)}
      {1\cdot3\cdots(2k-1)}
 \|Q\|_{[-K,K]}.
 \tag{13}
\]

Since \((2k-1)!!\geq k!\geq(k/e)^k\), its multiplier is at most

\[
 \left(\frac{en^2}{Kk}\right)^k.
 \tag{14}
\]

For \(n=4m\), fixed \(K\), and \(0\leq k\leq2m\), this is at most
\((8em/K)^{2m}\) once \(m\) is sufficiently large.  Applying (13) to the
derivative singled out by (10) yields

\[
 \|P_n\|_{[-K,K]}
 \geq
 B_{m,K}:=
 \frac{1}{(2m+1)16^m}
 \left(\frac{K}{8em}\right)^{2m}.
 \tag{15}
\]

For fixed \(K>0\), Stirling's bound in (12) shows

\[
 \log R_{m,K}=-4m\log m+O_K(m),
 \qquad
 \log B_{m,K}=-2m\log m+O_K(m).
 \tag{16}
\]

Thus \(R_{m,K}\leq B_{m,K}/2\) for all sufficiently large \(m\).  Equations
(12) and (15) give

\[
 \|F\|_{[-K,K]}\geq B_{m,K}/2.
 \tag{17}
\]

Finally, \(M_{\mu_0}(z)\leq e^K\) on this interval, so (17) proves (5).

For the finite-source claim, let \(\mu_m\) be the probability measure of the
\((m+1)\)-node Gauss--Legendre rule for \(\mu_0\).  It is exact through degree
\(2m+1\), so (9) is exactly the same with \(\mu_m\) in place of \(\mu_0\).
All support and Taylor bounds also remain unchanged.

## Matching upper bound and inversion

For every probability measure \(\mu\) on \([-1,1]\), its \(m\)-node Gaussian
rule \(\nu_m\) satisfies

\[
 0\leq M_\mu(z)-M_{\nu_m}(z)
 \leq
 \frac{4^{1-m}e^KK^{2m}}{(2m)!},
 \qquad |z|\leq K.
 \tag{18}
\]

For completeness, if \(\pi_m\) is the monic node polynomial, Hermite
interpolation at the Gaussian nodes gives the sign and the bound in (18),
with factor
\(\int\pi_m^2\,d\mu\).  This factor is at most the squared uniform norm of
the monic Chebyshev polynomial, namely \(4^{1-m}\).  If \(\mu\) has fewer than
\(m\) support points, take \(\nu_m=\mu\) and the error is zero.

Because \(M_\mu(z)\geq e^{-K}\),

\[
 \mathcal E_m(K)
 \leq\frac{4^{1-m}e^{2K}K^{2m}}{(2m)!}
 =\exp\{-2m\log m+O_K(m)\}.
 \tag{19}
\]

The lower bound (5) has the same logarithmic expansion.  This proves (3).
Standard inversion of
\(\log(1/\epsilon)=2m\log m+O_K(m)\) gives (6).

## Consequence for exponential-cone formulations

Take normalized slopes \(x_i\in[-1,1]\), probabilities \(w_i\), and

\[
 q(U,V)=W_0V\sum_iw_i
 \exp(\Lambda x_iU/V),
 \qquad |U|\leq LV,\quad K=\Lambda L.
 \tag{20}
\]

An \(m\)-term positive exponential mixture is exactly a formulation with at
most \(m\) local three-dimensional exponential cones before aggregation.
For every fixed nonzero sector width \(K\), equations (3) and (6) show that
the worst-case number of such cones needed for relative modeling error
\(\epsilon\) is

\[
 \left(\frac12+o(1)\right)
 \frac{\log(1/\epsilon)}{\log\log(1/\epsilon)}.
 \tag{21}
\]

This is a support lower bound for the direct positive-mixture representation.
At leading order it still applies if that representation may use arbitrary
real exponent nodes.  It does not rule out a smaller representation using
signed coefficients, rational functions, or a different conic lift.

## Novelty and literature boundary

The proof uses classical ingredients: support-annihilating polynomials,
Legendre extremality, the higher-order Markov brothers inequality, and
Gaussian quadrature.  Gaussian quadrature is classically optimal in
polynomial degree of exactness, and there is extensive work on worst-case
quadrature over analytic function spaces.  Those results ask for one
quadrature rule that integrates an entire function class; (2) instead asks
how well an arbitrary positive atomic measure can approximate one source
measure's whole bounded Laplace-transform curve.

A targeted search found work on Gaussian-quadrature exponential-sum
approximations of finite completely monotone functions and on minimax
exponential fits of particular special functions, but no theorem matching
(3), (5), (6), or (6c) for positive atomic approximation of bounded moment-
generating functions.  The claim should nevertheless be presented as a new
application and matching minimax synthesis of classical tools, not as a new
Markov or quadrature inequality.

Primary and authoritative antecedents:

- [NIST DLMF, Section 3.5, *Quadrature*](https://dlmf.nist.gov/3.5), for
  Gaussian quadrature and monic Legendre conventions.
- [Kalmykov--Nagy--Totik, *Bernstein- and Markov-type
  inequalities*](https://arxiv.org/abs/2104.02348), Section 6, for the sharp
  higher-derivative Markov inequality used in (13).
- [Gautschi--Varga, *Error Bounds for Gaussian Quadrature of Analytic
  Functions*](https://doi.org/10.1137/0720087), for classical analytic-
  integrand Gaussian error analysis.
- [Werschulz--Kowalski, *Is Gauss Quadrature Optimal for Analytic
  Functions?*](http://eudml.org/doc/133024), for the distinct worst-case
  analytic-function-space optimality problem.
- [Koyama, *Exponential sum approximations of finite completely monotonic
  functions*](https://arxiv.org/abs/2301.08931), for positive exponential
  sums produced by Gaussian quadrature after a variable transformation.
- [Goda--Kazashi--Tanaka, *How sharp are error bounds? Lower bounds on
  quadrature worst-case errors for analytic
  functions*](https://arxiv.org/abs/2401.07196), for recent lower bounds in
  weighted analytic function spaces, again a different minimax problem.
- [Monien, *Gaussian Summation: An Exponentially Converging Summation
  Scheme*](https://arxiv.org/abs/math/0611057), for Gaussian summation with
  discrete source measures.
- [Polyanskiy--Wu, *Note on approximating the Laplace transform of a
  Gaussian on a complex disk*](https://arxiv.org/abs/2008.13372), for the
  closely analogous use of Gaussian quadrature to obtain an
  \(\exp\{-\Theta(a^2\log a)\}\) Laplace-transform approximation rate.  Their
  constraint is a growing support interval for the approximating measure,
  rather than a bound on its number of atoms, and their norm is over a
  complex disk rather than the fixed real interval in (2).

## Independent audit record

The audit checked the argument also when \(\nu\) is not normalized.  Under
the only nontrivial case, relative error below \(1/2\), evaluation at zero
bounds its mass by \(3/2\), so the total-variation constant in (12) is valid.
The coefficient \(\ell_1\) bound in (8), monic-Legendre norm in (9), and
moment mismatch in (10) give exactly the displayed factor \(16^{-m}\).

For \(n=4m\), the logarithm of the upper bound in (14) is increasing over
\(1\leq k\leq2m\) once \(m\) is large compared with fixed \(K\): its maximum is
at \(k=2m\) and equals \((8em/K)^{2m}\).  The \(k=0\) case is covered as well.
Thus (15) loses only \(\exp\{2m\log m+O_K(m)\}\), while the Taylor remainder
in (12) is \(\exp\{-4m\log m+O_K(m)\}\); this verifies (16)--(17).  The
\((m+1)\)-node Gauss--Legendre source has identical moments through degree
\(2m\), unit mass, and support in \([-1,1]\), so every step of the finite-source
transfer remains valid.  Finally, the two-sided relation
\(-\log\mathcal E_m(K)=2m\log m+O_K(m)\) inverts to (6), including its
leading factor \(1/2\).

The growing-sector audit uses the explicit bounds rather than fixed-\(K\)
notation.  Their logarithms differ from
\(-2m\log(m/K)\) by \(O(m+K)\), and the Taylor comparison is uniform once
\(m/K\to\infty\).  The Lambert-\(W\) statement additionally requires its
continuous predicted support to diverge; \(L/K\to\infty\) alone is
insufficient if \(K\) shrinks exponentially in \(L\).

For arbitrary real competitor nodes, normalization makes the support
polynomial's coefficient norm at most one, while clipping gives the
pointwise factor \(1/2\) and hence (6e).  Endpoint approximation controls
the weighted total variation in (6f), which is exactly what is needed for
the smaller-interval Taylor bound (6g).  The Markov multiplier in (6h) is
worst at \(k=2m\), and its logarithm dominates the Taylor tail of degree
\(\lceil4m\log(m+1)\rceil\) by a positive multiple of
\(m\log m\).  This verifies (6c)--(6d), including nonnormalized competitors.

## Open extensions

1. Sharpen the arbitrary-real-node remainder in (6c) from
   \(O_K(m\log\log m)\) to \(O_K(m)\), or determine whether out-of-range
   nodes change that second-order scale.
2. Determine the minimax exponential constant hidden in the \(O_K(m)\) term
   for in-range nodes.
3. Prove or disprove a comparable lower bound for signed exponential sums or
   for arbitrary small conic lifts.
