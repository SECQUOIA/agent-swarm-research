# Sparse shell certificates for a proposed polynomial mixed-box optimum

Date: 2026-10-02. Status: complete derivation with fresh full-file and
input/bit reviews and targeted exact diagnostics. No substantive gap
remains in the reviewed argument. No priority claim is made.

A proposed rational point in a polynomial mixed box can be certified
without a supplied growth constant. The outer certificate uses physical
shells and coordinatewise upper curvature. A small inner box fixes all
lattice coordinates; a verified Taylor remainder transfers a quadratic
certificate there to the original polynomial. Higher-order coefficients
affect the shell count through their encoding lengths rather than a new
numerical conditioning parameter.

This is a candidate-certification theorem. It does not find an unknown
polynomial optimizer or assume that arbitrary polynomial optima are
rational. Its runtime guarantee requires positive pointwise quadratic
growth toward the proposed point; acceptance is sound without that promise.

## 1. Explicit polynomial model and curvature verification

Let \(X\) be a bounded rational product box. A coordinate is either
continuous or restricted to a rational lattice \(a_i+h_i\mathbb Z\),
with \(h_i>0\). Round lattice endpoints inward, reject empty domains,
and remove fixed coordinates. Let \(v\in X\) be a supplied rational
feasible point, including its lattice restrictions. A remaining singleton
problem is immediate; below the remaining dimension is \(n\ge1\).

The objective is supplied as
\[
 F(x)=\sum_{\ell=1}^m f_\ell(x_{S_\ell}),
 \tag{1}
\]
where each factor is an explicit list of rational monomials of total
degree at most a fixed constant \(d_0\). Every factor scope is contained
in a bag of a supplied tree decomposition with \(N\) bags, each of size
at most \(p\). The encoding length \(I\) includes all coefficients,
scopes, endpoints, lattice data, \(v\), the decomposition, the supplied
\(L\), and any additional curvature-certificate data. Constants
in polynomial input bounds may depend on the fixed \(d_0\).

Use a rational \(L>0\) satisfying
\[
 \partial_{ii}F(x)\le L
 \quad\text{for every coordinate and every }x
 \text{ in the full continuous box hull of }X.
 \tag{2}
\]
In particular, the bound holds between lattice labels. It is not enough
to verify (2) only at mixed-feasible points.

The certificate verifier must verify (2), not assume an untrusted
curvature claim. An elementary admissible format expands each
\(\partial_{ii}F\), computes rational interval bounds for each monomial
on the box, and sums the term upper bounds. The claimed \(L\) must
dominate all resulting bounds. Fixed degree makes this polynomial work
with polynomial-size rational data. Collecting equal monomials first
can preserve cancellations. This bound can be loose; the complexity
parameter uses the bound actually verified. The complexity theorem below
uses this format, or a substitute format verifiable in polynomial time
in the counted input. For any more expensive curvature verification,
its actual cost must instead be added separately.

The full-domain point-growth constant, when positive, is
\[
 g=\inf_{\substack{x\in X\\x\ne v}}
       \frac{F(x)-F(v)}{\|x-v\|_2^2}>0,\qquad
 \kappa=L/g.
 \tag{3}
\]
It is not given to the algorithm or verifier. Check feasibility of
\(v\) and the continuous first-order signs
\[
 \varepsilon\,\partial_iF(v)\ge0
 \quad\text{for each available continuous sign }\varepsilon.
 \tag{4}
\]
No derivative sign is imposed on lattice coordinates. Failure of (4)
rules out local optimality by a continuous coordinate direction.

## 2. A rational remainder on the fixed-lattice slice

Let \(\mathcal C,\mathcal Z\) be the continuous and lattice coordinates.
Set \(d_{\mathcal Z}=0\) and translate the explicit factors exactly:
\[
 F(v+d)-F(v)
   =q(d)+\sum_{|\alpha|\ge3}c_\alpha d_{\mathcal C}^{\alpha},
 \qquad
 q(d)=\nabla_{\mathcal C}F(v)^Td_{\mathcal C}
       +\tfrac12d_{\mathcal C}^T
                 \nabla^2_{\mathcal C\mathcal C}F(v)d_{\mathcal C}.
 \tag{5}
\]
The translation and degree-two truncation preserve the factor scopes.
It is also valid to keep the higher-order coefficients factorwise,
without collecting cancellations between factors. Put
\[
 M=\max\left\{1,\sum_{|\alpha|\ge3}|c_\alpha|\right\}.
 \tag{6}
\]
For factorwise coefficients use their total absolute sum instead.
All these quantities have polynomial encoding length at fixed degree.

For \(\|d\|_\infty\le\rho\le1\), every higher-order monomial obeys
\[
 |d^\alpha|\le\rho\|d\|_2^2.
 \tag{7}
\]
Indeed, any two factors have product at most \(\|d\|_2^2\);
the remaining factors contribute at most
\(\rho^{|\alpha|-2}\le\rho\). Therefore
\[
 |F(v+d)-F(v)-q(d)|\le M\rho\|d\|_2^2.
 \tag{8}
\]
This is a coefficient-arithmetic remainder certificate, with no
unverified derivative norm. If the tail is identically zero, the
additional restriction involving \(M\) below can be omitted, but the
uniform definition (6) is harmless.

## 3. Trial radii and physical shell grids

For each coordinate and available sign, let \(w_i^\varepsilon\) be
the positive distance from \(v_i\) to the effective endpoint. Define
\[
 r_0=\min\bigl(
       \{h_i/2:i\in\mathcal Z\}
       \cup\{w_i^\varepsilon:i\in\mathcal C,\
                                      w_i^\varepsilon>0\}\bigr)>0,
 \qquad D=\max_{x\in X}\|x-v\|_\infty.
 \tag{9}
\]
The union is nonempty after preprocessing and \(D\ge r_0\).
At trial \(r=1,2,\ldots\), set
\[
 \delta=2^{-r},\qquad \sigma=L\delta^2/8,\qquad
 \rho=\min\{r_0,1,\sigma/M\}.
 \tag{10}
\]
Thus \(M\rho\le\sigma\). Every feasible point with infinity
distance at most \(\rho\) has its lattice coordinates fixed at \(v\),
and every available continuous side permits displacement \(\rho\).

Let \(J=\lfloor\log_2(D/\rho)\rfloor\). The physical shells
\[
 X_j=\{x\in X:S_j\le\|x-v\|_\infty\le2S_j\},
 \qquad S_j=2^j\rho,\quad 0\le j\le J,
 \tag{11}
\]
cover every feasible point at distance at least \(\rho\).

For completeness, each shell uses the grids of the
[mixed quadratic shell certificate](mixed-shell-certificate.md).
In displacement coordinates, treat each available sign separately and
include zero only once. Let \(U\le2S\) be the side's last feasible
displacement within the shell box.

- On a continuous side, begin at
  \(\min\{U,\delta S/(2n)\}\), multiply by \(1+\delta\), and
  clip at \(U\). Insert \(S\) when \(S\le U\).
- On a lattice side of spacing \(h_i\), begin at
  \(\min\{U,h_i\lceil\delta S/(2nh_i)\rceil\}\).
  After label \(a>0\), increment by
  \(h_i\max\{1,\lfloor\delta a/h_i\rfloor\}\), clipping at
  \(U\). Insert \(h_i\lceil S/h_i\rceil\) when feasible.

A zero side contributes no positive label. Threshold insertion preserves
the maximum interval length. All lattice grid points are feasible labels.
Call the translated product grid \(G_{S,\delta}\).

Mean-preserving independent endpoint rounding of any \(x\in X_j\)
produces a feasible \(Y\) still satisfying
\(\|Y-v\|_\infty\ge S\). A coordinate originally above its threshold
cannot round below it. Writing \(Z=Y-v\), the scalar grid construction
gives
\[
 4\operatorname{Var}(Y_i)
 \le\delta^2\mathbb E Z_i^2+\delta^2S^2/n^2.
 \tag{12}
\]
Continuous initial gaps are at most \(\delta S/(2n)\).
Lattice gaps of one step have zero variance at feasible targets; larger
initial gaps are at most \(\delta S/n\). Every later gap that can
produce variance is at most \(\delta\) times its smaller absolute
endpoint. These facts prove (12), including clipped and split intervals.

## 4. Outer bounds use semiconcavity, not quadratic cancellation

For any \(C^2\) function \(H\) with \(\partial_{ii}H\le L\),
replace the coordinates of \(x\) by their independent rounded values
one at a time. Conditional on all coordinates already replaced, the
one-dimensional function
\(H-\tfrac L2x_i^2\) is concave. Its chord inequality gives
an expected increase of at most
\((L/2)\operatorname{Var}(Y_i)\). Telescoping yields
\[
 \mathbb E H(Y)-H(x)
 \le\tfrac L2\sum_i\operatorname{Var}(Y_i).
 \tag{13}
\]
Every intermediate coordinate vector lies in the continuous box hull,
which explains the domain required in (2).

Apply (13) to
\(R(x)=F(x)-F(v)-\sigma\|x-v\|_2^2\), whose coordinate
second derivatives are at most \(L-2\sigma\le L\).
Using (12) and (10) gives
\[
 \mathbb E R(Y)-R(x)
 \le\sigma\mathbb E\|Y-v\|_2^2+\sigma S^2/n.
 \tag{14}
\]
Compute the exact finite minimum
\[
 m_{S,\delta}=
 \min_{\substack{y\in G_{S,\delta}\\\|y-v\|_\infty\ge S}}
     [F(y)-F(v)-2\sigma\|y-v\|_2^2].
 \tag{15}
\]
An empty minimum is \(+\infty\). The sound outer bound is
\[
 F(x)-F(v)-\sigma\|x-v\|_2^2
       \ge m_{S,\delta}-\sigma S^2/n
       \qquad(x\in X_j).
 \tag{16}
\]
Thus all checks
\[
 m_{S_j,\delta}\ge\sigma S_j^2/n
 \tag{17}
\]
certify growth \(\sigma\) outside the inner box, without any growth
assumption on the input.

## 5. One quadratic boundary certificate closes the inner box

If there are no continuous coordinates, the core contains only \(v\)
and needs no further check. Otherwise use the continuous part of the
same signed grid, now restricted to displacements of absolute value
at most \(\rho\) on every available side; all lattice displacements
are zero. Include the endpoints \(\pm\rho\) where available.
Let \(G_{\rm core}\) be this grid and compute
\[
 m_{\rm core}=
 \min_{\substack{z\in G_{\rm core}\\\|z\|_\infty=\rho}}
       [q(z)-3\sigma\|z\|_2^2].
 \tag{18}
\]
The check is
\[
 m_{\rm core}\ge\sigma\rho^2/n.
 \tag{19}
\]

At a continuous boundary point of the core, a coordinate equal to
\(\pm\rho\) stays fixed under rounding. The rounded vector remains
on that boundary. Apply (13) to \(q-2\sigma\|d\|^2\), whose
coordinate second derivatives are at most
\(\partial_{ii}F(v)-4\sigma\le L\).
The same variance calculation proves from (19) that
\[
 q(d)\ge2\sigma\|d\|^2
             \quad\text{on the core boundary}.
 \tag{20}
\]
For an interior displacement, write \(d=tz\), where
\(\|z\|_\infty=\rho\) and \(0<t<1\).
Condition (4) gives
\(\nabla F(v)^Tz\ge0\), so quadratic expansion yields
\[
 q(tz)\ge t^2q(z)\ge2\sigma\|tz\|^2.
 \tag{21}
\]
Only continuous coordinates move in this radial step. Combining (8),
(10), and (21) proves
\[
 F(v+d)-F(v)\ge\sigma\|d\|^2
                   \quad\text{throughout the core}.
 \tag{22}
\]
Together, (17) and (19) therefore certify (22) for every feasible
displacement. Every acceptance is an unconditional, independently
checkable proof of unique global optimality and the displayed margin.
The proof does not assert that \(q\) is nonnegative on the original box.

## 6. Discovery and fixed-parameter bit complexity

Suppose now that (3) holds. Every outer grid point has
\(\|y-v\|^2\ge S^2\), so (17) holds whenever
\(\sigma\le g/3\).
On the inner slice, (8) and \(M\rho\le\sigma\) imply directly
\[
 q(d)\ge(g-\sigma)\|d\|^2.
 \tag{23}
\]
When \(\sigma\le g/5\), in particular \(g-4\sigma\ge0\), every
core grid point satisfies
\[
 q(z)-3\sigma\|z\|^2
     \ge(g-4\sigma)\rho^2.
 \tag{24}
\]
Condition (19) follows if \(\sigma\le g/5\). This direct growth
transfer needs no critical-cone separation or positive-multiplier gap.
The continuous sign checks also hold under (3).

Trying successive dyadic \(\delta\) therefore terminates. At first
success,
\[
 \sigma\ge\min\{L/32,g/20\},\qquad
 L/\sigma\le\max\{32,20L/g\},\qquad
 \delta^{-1}\le\max\{2,\sqrt{5L/(2g)}\}.
 \tag{25}
\]
The initial margin is \(L/32\); a later successful trial has a failed
predecessor with parameter \(4\sigma>g/5\). The accepted certificate
also gives \(\sigma\le g\).
The number of trials is \(O(1+\log^+(L/g))\).

Each coordinate grid has
\[
 K=O(\delta^{-1}\log(2n/\delta))
 \tag{26}
\]
labels, independently of physical shell radius and lattice spacing.
This follows from the multiplicative continuous grid and, on lattice
sides, at most \(O(1/\delta)\) one-step labels before increments grow
by a constant fraction of \(\delta a\). Clipping and a threshold
label add only constants.

Assign each polynomial factor to a containing bag and unary corrections
to variable owners. The ordinary tree DP adds a Boolean flag recording
whether an owned coordinate has absolute displacement at least \(S\),
or exactly \(\rho\) in the core. Combine child flags successively by
OR. This computes (15) or (18) in
\(\operatorname{poly}(p,d_0,I)O(NK^p)\) arithmetic operations;
branching degree introduces no exponential factor. No polynomial
interaction beyond the input scopes is created by translation or Taylor
truncation.

Since \(M\) has polynomial bit length and \(\sigma\) has bit length
\(\operatorname{poly}(I)+O(r)\),
\[
 J+1=O(1+\log(D/\rho))=\operatorname{poly}(I)+O(r).
 \tag{27}
\]
Thus higher-order coefficients enter through a logarithmic radius cost.
One must not replace the right side by a polynomial in \(I\) alone:
for nonlinear input, a very small true \(g\) can require a large \(r\).
Its effect is charged to \(\kappa\).

Shell radii and lattice labels have
\(\operatorname{poly}(I+r)\) bits; continuous geometric labels have
\(\operatorname{poly}(I+r+rK)\) bits. A common denominator can be
chosen for all labels at a trial. If its bit length is \(B\), a degree
\(d_0\) factor value has denominator dividing the product of a common
coefficient denominator and the \(d_0\)-th power of the label
denominator. Its bit length is polynomial in \(I+r+K\).
Unary corrections require only an additional dyadic denominator.
Bellman messages add selected factor values with a shared denominator;
minimization creates no denominator multiplication across bags.

Powers of \(\log n\) in \(K^p\) are absorbed into a function of
\(p\) times an absolute power of \(n\). Equations (25)--(27) give
deterministic search, certificate size, and verification cost
\[
 f_{d_0}(p,\max\{1,L/g\})\operatorname{poly}(I),
 \tag{28}
\]
with an absolute input exponent for each fixed degree bound.
The certificate contains the checked curvature bound, first-order
signs, rational Taylor/remainder data, grids, and exact shell/core
Bellman tables. It does not require a numerical global-optimization
oracle, a growth estimate, or a polynomial optimum represented by
an irrational algebraic number.

## 7. Necessary limits and useful counterexamples

The [pruned coordinate-grid theorem](pruned-coordinate-grid.md) already
states that its arithmetic argument extends to exactly evaluable
coordinate-semiconcave factors. This note does not introduce that
extension or a new rounding algorithm. Its additional completion is a
finite certificate for the rational candidate: physical shells handle
lattice feasibility, and an explicitly verified local Taylor core
removes the infinite refinement near that candidate. Fixed-degree
coefficient arithmetic supplies the bit model. The related exact QP
shell theorem is the direct algorithmic predecessor.

The Taylor quadratic need only work locally. For
\[
 F(x)=x-x^2+x^3\quad\text{on }[0,2],\qquad v=0,
 \tag{29}
\]
one has \(F(x)-x^2=x(x-1)^2\ge0\), so \(g=1\).
Its Taylor quadratic \(x-x^2\) is negative for \(x>1\).
The shrinking core, rather than a global Taylor replacement, is essential.

Curvature at lattice points is insufficient. On the lattice
\(\{0,1,2\}\), the polynomial
\[
 h(x)=\bigl[5(x-1)^4-2(x-1)^6\bigr]/3
 \tag{30}
\]
has endpoint values one, middle value zero, and
\(h''(0)=h''(1)=h''(2)=0\).
Rounding the middle point equally to the endpoints increases expectation
by one with variance one, contradicting the \(L/2\) estimate for
\(L=1\). Its continuous curvature is larger between labels.

The explicit fixed-degree encoding is also substantive. With a binary
exponent \(d=2^k\), consider
\[
 F(x,y)=x^2-\tfrac12x^d+y^2
       \quad\text{on }[0,1]^2,\qquad v=0.
 \tag{31}
\]
It has \(g=1/2\), coordinate upper curvature \(L=2\), and singleton
bags. At the initial trial, \(M=1,\sigma=\rho=1/16\), so the
shell of radius \(S=1\) is present and contains the literal grid
node \((1/8,1)\). There,
\[
 F(1/8,1)=65/64-2^{-(3d+1)}
 \tag{32}
\]
has reduced denominator \(2^{3d+1}\). Exact rational factor tables
can require exponentially many bits in the succinct exponent input.
Likewise a circuit can generate \(H=2^{2^k}\) by repeated squaring:
\(x^2+Hx(1-x)+y^2\) has degree two, \(g=1,L=2\), but
the same rational point has an exponentially long numerator.
These are obstructions to an explicit rational-table bit bound under
succinct input, not lower bounds for every symbolic algorithm.

Numerical degree can be charged as an additional parameter with further
bookkeeping. No such generalization is needed for (28). Coupled nonlinear
constraints, arbitrary succinct circuits, nonrational proposed optima,
and zero-growth unique minima such as \(x^4\) remain outside the result.
A successful certificate is valid without any promise; finite
termination is asserted only under (3).

## 8. Review and verification status

The outer semiconcavity argument and local Taylor argument were
independently challenged by separate agents. The parent researcher
independently derived the sharper core test with corrections
\(2\sigma\) and \(3\sigma\). A
[full-file independent review](nonlinear-shell-independent-review.md)
and a separate [input/bit review](nonlinear-shell-bit-review.md) found
no substantive gap after the stated sign and input-accounting
clarifications.

The targeted command

```sh
python3 -B research-20261002/new-direction/check_nonlinear_shell_certificate.py
```

passed six positive fixtures in seven trials and three rejected
wrong-candidate trials. The
[checker](check_nonlinear_shell_certificate.py) evaluated 2,154 bag
assignments over 49 shell/core tables, comparing every minimum with
direct normalized-grid enumeration. It checked 145 rational rounding
cases and 66 core remainder/growth cases. Fixtures include nonlinear
cross terms, a globally invalid Taylor quadratic, negative lattice
derivatives, nonunit rational lattices, signed continuous displacements,
pure integer quartics, and a sparse polynomial path. A wrong candidate
with valid first-order signs and positive local Taylor quadratic is
rejected by the outer checks.

The independent reviewer separately tested sequential rounding with
genuine higher-order expectation contributions; those checks are
recorded in its review. Finite diagnostics do not establish the
general proof or asymptotic complexity, and this checker is not a
production global solver. No project-wide verification, CI inspection,
or literature knowledge-base edits are part of this note.

A scoped inline Python check passed whitespace, paired mathematical
delimiters, local links in the theorem and both reviews, and checker syntax.
