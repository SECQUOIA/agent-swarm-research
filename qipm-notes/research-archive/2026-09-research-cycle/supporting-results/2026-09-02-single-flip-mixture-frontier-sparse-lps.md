# Multi-bit-per-coefficient supplement to the convex-mixture frontier

Date: 2026-09-02

> Verification update (2026-09-20): this is a historical supplement.
> The current paper and [Lean verification report](../../../formal/MIXTURE.md)
> give a stronger primal bound using maximum per-coefficient input degree,
> and a stronger one-bit KKT bound using signed dual multipliers directly.
> The uniform diagonal counterexample below loses centrality around the
> neighbors' **common parameter** but has zero point-centered width.
> The paper now includes a public-coordinate padding that also gives
> point-centered instability. The arbitrary-weight formulas and multibit
> KKT extension retained in this archive are not claimed as Lean-verified.

## Supplement status and main result

The canonical audited statement is
`2026-09-02-convex-mixture-local-input-obstruction.md`.  It contains the sharp
one-bit-per-coefficient bound \(2BH\sqrt{sM}/N\), the pair-margin
amplitude-state corollary, the three amplification currencies, and the
LDPC/XOR discussion.  This note is retained only for the genuinely broader
multi-bit dependency theorem and its primal--dual extension: one coefficient
may depend on a bounded set of input bits, giving the weaker bound
\(2BH\sqrt{dsM}/N\).  If duplicated wording ever differs, the canonical note
controls.

Fix an input \(\sigma\), flip each of its \(N\) bits separately, and average one
selected exact optimum from each neighboring instance. Convexity preserves
nonnegativity and the exact common objective value. Every neighboring witness
has opposite parity, but the average is a wrong-parity output only under an
affine, common-template, or pair-margin hypothesis. Coefficient locality alone
proves near-feasibility, not an amplitude-state conclusion.

The argument does **not** assume a path, graph propagation, cycle consistency,
a public null basis, or a particular LP gadget.  For row sparsity \(s\), row
input-degree \(d\), coefficient bound \(B\), exact-solution coordinate bound
\(H\), and \(M\) coefficient--input incidences, the adversarial point obeys

\[
 \boxed{
 \|A_\sigma\bar x-b\|_2
 \le \frac{2BH\sqrt{dsM}}{N}.}
\tag{1}
\]

Consequently constant relative-residual soundness at fixed \(\|b\|_2\)
requires

\[
                 MB^2H^2=\Omega(N^2)
\tag{2}
\]

when \(d,s=O(1)\).  In a linear-size sparse family, \(M=O(N)\), so bounded
coefficients force \(H=\Omega(\sqrt N)\).  This extends the separate
cut--resistance frontier from cycle-consistent signed graphs to arbitrary
sparse linear constraints under the explicit fixed-objective, bounded-witness,
and mixture-stable-output assumptions below. It extends the canonical one-bit
theorem only in the allowed dependency sets; its constant is weaker when every
coefficient depends on at most one bit.

## 1. Local coefficient model

For \(\sigma\in\{-1,+1\}^N\), consider

\[
       \min\{c^Tx:A_\sigma x=b,\ x\ge0\},
\tag{3}
\]

where \(b,c\) and the matrix support are independent of \(\sigma\).  The
actual values of nonzero entries may depend on the input.  Associate with
entry \((r,j)\) a set \(I_{rj}\subseteq[N]\) such that its value depends only
on \((\sigma_i)_{i\in I_{rj}}\), and assume

\[
 |(A_\sigma)_{rj}|\le B.
\tag{4}
\]

Define

\[
\begin{aligned}
 s&=\max_r|\{j:(r,j)\in\operatorname{supp}A\}|,\\
 d&=\max_r\left|\bigcup_j I_{rj}\right|,\\
 M&=\sum_{(r,j)\in\operatorname{supp}A}|I_{rj}|.
\end{aligned}
\tag{5}
\]

Thus \(M\) counts coefficient--input incidences, including repeated uses of
the same bit.  In the usual one-bit-per-entry local oracle, \(|I_{rj}|\le1\)
and \(d\le s\); for a row-\(s\)-sparse matrix with \(m\) rows,
\(M\le sm\).

Assume that for every input \(\xi\) there is a selected exact feasible optimum
\(x^\xi\) satisfying

\[
             0\le x_j^\xi\le H,
 \qquad c^Tx^\xi=v,
\tag{6}
\]

where the optimal value \(v\) is the same for all inputs.  Uniqueness is not
required; (6) merely fixes one uniformly bounded witness per input.

## 2. The mixture theorem

For a fixed base input \(\sigma\), let \(\sigma^{(i)}\) be \(\sigma\) with
bit \(i\) flipped and define

\[
                  \bar x=\frac1N\sum_{i=1}^N x^{\sigma^{(i)}}.
\tag{7}
\]

### Theorem 1 (single-flip residual bound)

The point \(\bar x\) is nonnegative, has exact objective value \(v\), and
satisfies (1).

#### Proof

Nonnegativity and \(c^T\bar x=v\) follow by convexity and (6).  Put

\[
 \Delta_i=A_\sigma-A_{\sigma^{(i)}},
 \qquad r_i=\Delta_i x^{\sigma^{(i)}}.
\]

Since \(A_{\sigma^{(i)}}x^{\sigma^{(i)}}=b\),

\[
 A_\sigma\bar x-b=\frac1N\sum_{i=1}^Nr_i.
\tag{8}
\]

For row \(r\), at most \(d\) of the vectors \(r_i\) can have a nonzero
\(r\)-th coordinate.  Hence Cauchy--Schwarz gives

\[
 \left(\sum_i r_{i,r}\right)^2
 \le d\sum_i r_{i,r}^2.
\tag{9}
\]

Let \(t_{ir}=|\{j:i\in I_{rj}\}|\).  At most \(s\) summands occur in
\(r_{i,r}\), every changed coefficient has magnitude at most \(2B\), and
every witness coordinate is at most \(H\).  A second Cauchy--Schwarz bound
therefore gives

\[
 r_{i,r}^2
 \le 4sB^2H^2t_{ir}.
\tag{10}
\]

Summing (9)--(10) and using \(\sum_{i,r}t_{ir}=M\),

\[
 \left\|\sum_i r_i\right\|_2^2
 \le4dsB^2H^2M.
\tag{11}
\]

Equations (8) and (11) prove (1). \(\square\)

In the important one-bit-per-entry specialization \(|I_{rj}|\le1\), the
factor \(d\) can be removed.  Let \(m_r\) be the number of input-dependent
positions in row \(r\).  Expand \(\sum_i r_{i,r}\) into one scalar term for
each such position.  This remains valid when the same input bit labels several
positions: those terms use the same neighboring witness, but there are still
only \(m_r\) of them.  Each term has magnitude at most \(2BH\), so
\[
 \left|\sum_i r_{i,r}\right|^2
 \le4B^2H^2m_r^2
 \le4sB^2H^2m_r.
\]
Summing over rows yields the sharper bound
\[
 \boxed{\ \|A_\sigma\bar x-b\|_2
       \le \frac{2BH\sqrt{sM}}N\ }
\tag{11a}
\]
for one-bit-local coefficient positions, with repeated bit labels fully
allowed.

### Corollary 1.1 (size--coefficient--range frontier)

Suppose a claimed soundness property excludes every nonnegative,
exact-objective point with relative residual at most \(\eta\).  If \(\bar x\)
violates the desired parity output, then necessarily

\[
 MB^2H^2>
 \frac{\eta^2\|b\|_2^2N^2}{4ds}.
\tag{12}
\]

For constant \(d,s,\eta,\|b\|_2\), bounded coefficients, and \(M=O(P)\),
this is

\[
                   PH^2=\Omega(N^2).
\tag{13}
\]

Thus \(P=\Theta(N)\) forces \(H=\Omega(\sqrt N)\).  The gain--plateau LP
saturates this general frontier; the bounded-height parallel construction
saturates its quadratic-size endpoint.

For one-bit-per-entry dependence, (11a) sharpens the denominator in (12) from
\(4ds\) to \(4s\).  This improves the constant/locality dependence but not the
linear-size exponent.

### Corollary 1.2 (primal--dual QIPM output contracts)

The same obstruction applies simultaneously to primal feasibility, dual
feasibility, and objective gap. Consider the LP pair with fixed \(b,c\) and
input-dependent \(A_\sigma\):
\[
 \min\{c^\top x:A_\sigma x=b,\ x\ge0\},
\qquad
 \max\{b^\top y:A_\sigma^\top y+s=c,\ s\ge0\}.
\]
Suppose every instance has a selected exact optimal triple
\((x^\sigma,y^\sigma,s^\sigma)\), all coordinates have magnitude at most
\(H\), and the common optimum is \(v\). Split the free dual variable into its
positive and negative parts, \(y=y^+-y^-\), and stack the linear equations:
\[
 \begin{bmatrix}
 A_\sigma&0&0&0\\
 0&A_\sigma^\top&-A_\sigma^\top&I
 \end{bmatrix}
 \begin{bmatrix}x\\y^+\\y^-\\s\end{bmatrix}
 =
 \begin{bmatrix}b\\c\end{bmatrix}.                       \tag{13a}
\]
Apply Theorem 1 to the selected nonnegative vectors
\((x^\sigma,(y^\sigma)^+,(y^\sigma)^-,s^\sigma)\). The single-flip mixture
has small combined primal--dual Euclidean residual and preserves
\[
 c^\top\bar x=v,
 \qquad
 b^\top(\bar y^+-\bar y^-)=v.
\]
It therefore has exactly zero objective gap despite being only approximately
primal and dual feasible. Any affine or pair-margin parity decoder satisfying
Section 2 or Corollary 2 of the canonical note is still driven to the wrong
parity.

If \(A_\sigma\) has bounded row and column degree, bounded coefficients, and
one-bit-local entries with \(O(N)\) coefficient--input incidences, the stacked
system has bounded row sparsity and \(O(N)\) incidences as well: an entry of
\(A_\sigma\) appears once in the primal block and twice in the split-dual
block. Thus bounded neighboring primal--dual optima produce a wrong-output,
zero-gap point with combined residual \(O(N^{-1/2})\).

More explicitly, let \(s_r\) and \(s_c\) be the maximum row and column
sparsities of \(A_\sigma\), let \(M\) count its one-bit-dependent positions,
and put
\[
 s_{\rm KKT}=\max\{s_r,\,2s_c+1\},\qquad
 B_{\rm KKT}=\max\{B,1\}.
\]
The stacked system has row sparsity at most \(s_{\rm KKT}\), and every
input-dependent entry of \(A_\sigma\) occurs in three stacked positions.
The sharp one-bit theorem therefore gives
\[
 \left\|
 \begin{bmatrix}
 A_\sigma\bar x-b\\
 A_\sigma^\top(\bar y^+-\bar y^-)+\bar s-c
 \end{bmatrix}
 \right\|_2
 \le
 \frac{2B_{\rm KKT}H\sqrt{3s_{\rm KKT}M}}{N}.
\tag{13aa}
\]
This is an explicit simultaneous feasibility-and-stationarity bound, not just
an asymptotic application of Theorem 1.

This covers QIPM output contracts stated through primal residual, dual
residual, and objective gap. It does not automatically cover a separate
coordinatewise complementarity or central-neighborhood contract. Convex
averaging does not preserve complementarity: two neighboring central pairs
may have
\[
 (x_j,s_j)=(H,\mu/H)
 \quad\text{and}\quad
 (x_j,s_j)=(\mu/H,H).
\]
Both obey \(x_js_j=\mu\), whereas their midpoint obeys
\[
 \bar x_j\bar s_j=\frac14(H+\mu/H)^2,
\]
which is of order \(H^2\), not \(\mu\), when \(\mu\ll H^2\). Extending the
mixture obstruction to central-path-only outputs therefore requires an
additional stability hypothesis relating neighboring central pairs.

### Corollary 1.3 (convex-conic and parity-neutral extension)

The proof of Theorem 1 does not use coordinatewise nonnegativity until the
amplitude-pair decoder.  Let \({\cal K}\subseteq\mathbb R^n\) be any convex
set or convex cone, replace \(x\ge0\) in (3) by \(x\in{\cal K}\), and retain
the coordinate bound \(\|x^\xi\|_\infty\le H\) in a fixed basis.  Then the
mixture (7) belongs to \({\cal K}\), and the residual and common-objective
conclusions of Theorem 1 hold verbatim.

There is also a parity-neutral version.  Suppose a fixed linear map \(L\) and
fixed nonzero vector \(y\) obey

\[
                         Lx^\xi=p(\xi)y
\tag{13b}
\]

for every selected witness.  Define

\[
 \widehat x=\frac12x^\sigma+\frac1{2N}
                  \sum_{i=1}^Nx^{\sigma^{(i)}}.
\tag{13c}
\]

Then \(\widehat x\in{\cal K}\), its objective value is exactly \(v\), and
\(L\widehat x=0\). Since the base witness has zero residual and the second
term in (13c) is \(\bar x/2\),

\[
 A_\sigma\widehat x-b
 =\frac12(A_\sigma\bar x-b).
\]

Thus Theorem 1 improves by a factor two:

\[
 \|A_\sigma\widehat x-b\|_2
 \le\frac{BH\sqrt{dsM}}{N},
\tag{13d}
\]

or \(BH\sqrt{sM}/N\) in the one-bit-per-entry case.

This is a neutral **linear-output** obstruction: it defeats a contract that
requires every residual-accurate, objective-exact point to have a uniform
nonzero margin under \(L\). It does not say that \(\widehat x\) has the wrong
parity, that its normalized amplitude state is easy or parity-neutral, or that
it satisfies a central-neighborhood condition.

For a real sparse SDP, fix once and for all a linear coordinate isomorphism
\(\operatorname{svec}:\mathbb S^r\to\mathbb R^{r(r+1)/2}\), for example the
standard Frobenius-isometric symmetric vectorization. Then
\({\cal K}=\operatorname{svec}(\mathbb S_+^r)\) is a convex cone, and a
constraint \(\langle F_{\sigma,k},X\rangle=b_k\) is a row of the vectorized
linear system. Convex averaging preserves positive semidefiniteness. The
quantities \(H,M,d,s,B\) must be measured **after this fixed vectorization**:
\(H\) bounds the selected matrix-coordinate vectors, and \(M,d,s,B\) describe
the resulting measurement rows. Under these explicit hypotheses, the same
size--coefficient--range obstruction applies to sparse SDP and general conic-IPM
parity gadgets with a fixed linear output.

No amplitude-state conclusion follows merely by vectorizing a PSD matrix:
off-diagonal coordinates may be signed, and the quadratic normalization is not
preserved by convex averaging. Such a conclusion still needs a common template,
the nonnegative pair-margin hypothesis of Section 3, or another explicit
mixture-stability assumption. Likewise, the mixture does not preserve nonlinear
centrality, complementarity, rank, or determinant-barrier neighborhoods. If all
selected SDP witnesses are positive definite, their finite convex mixture is
positive definite as well, but no uniform eigenvalue margin follows unless one
is assumed for the witnesses.

### Corollary 1.4 (stationarity-preserving central mixture)

The centrality limitation can be partly overcome under a sharp stability
hypothesis. Fix a base input \(\sigma\), a common right-hand side \(b\), and a
common cost vector \(c\). Suppose the selected triples
\((x^{\sigma^{(i)}},y^{\sigma^{(i)}},s^{\sigma^{(i)}})\) for its \(N\)
single-bit neighbors are exact central points at the same barrier parameter
\(\mu>0\). Thus \(x^{\sigma^{(i)}}>0\),
\(s^{\sigma^{(i)}}>0\), primal and dual feasibility hold for
\(A_{\sigma^{(i)}}\), and
\[
 x_j^{\sigma^{(i)}}s_j^{\sigma^{(i)}}=\mu
 \qquad\text{for every }i,j.
\tag{13e}
\]
Even without a stability bound, the complementarity defect of the average is
given exactly by the multiplicative-variance identity (13i*) below.
Assume coordinatewise neighbor stability: for every primal coordinate \(j\),
\[
 \frac{\max_i x_j^{\sigma^{(i)}}}
      {\min_i x_j^{\sigma^{(i)}}}\le R.
\tag{13f}
\]
Here and below \(R\ge1\).
Then their single-flip averages obey
\[
 \mu\le \bar x_j\bar s_j\le K(R)\mu,
 \qquad
 K(R)=\frac{(R+1)^2}{4R}
      =1+\frac{(R-1)^2}{4R},
\tag{13g}
\]
and hence
\[
 \|\bar X\bar S\mathbf1-\mu\mathbf1\|_\infty
 \le \frac{(R-1)^2}{4R}\,\mu.
\tag{13h}
\]
For \(R=1\), the averaged pair is exactly complementary:
\(\bar x_j\bar s_j=\mu\) for every \(j\). In general the product is
one-sided: Cauchy--Schwarz forces
\(\bar x_j\bar s_j\ge\mu\), and it can be strictly larger.
If the neighborhood parameter is defined in the standard way from the
averaged complementarity,
\[
 \bar\mu=\frac{\bar x^\top\bar s}{n},
\]
then \(\mu\le\bar\mu\le K(R)\mu\) and the same estimate implies
\[
 \|\bar X\bar S\mathbf1-\bar\mu\mathbf1\|_\infty
 \le [K(R)-1]\mu
 \le [K(R)-1]\bar\mu.
\]
Thus the conclusion holds both for a neighborhood centered at the original
\(\mu\) and for the usual neighborhood centered at \(\bar\mu\).
More explicitly, with
\[
 {\cal N}_\infty(\nu,\theta)
 =\{(x,s)>0:\|Xs\mathbf1-\nu\mathbf1\|_\infty\le\theta\nu\},
\]
the averaged pair belongs both to
\({\cal N}_\infty(\mu,K(R)-1)\) and to
\({\cal N}_\infty(\bar\mu,K(R)-1)\).  The second is the standard
point-centered convention.

For the proof, fix \(j\), put \(t_i=x_j^{\sigma^{(i)}}\),
\(\alpha=\min_i t_i\), and \(\beta=\max_i t_i\). Equation (13e) gives
\[
 \bar x_j\bar s_j
 =\mu\left(\frac1N\sum_i t_i\right)
       \left(\frac1N\sum_i\frac1{t_i}\right).
\tag{13i}
\]
More precisely, symmetrizing the double sum gives the exact identity
\[
 \left(\frac1N\sum_i t_i\right)
 \left(\frac1N\sum_i\frac1{t_i}\right)-1
 =
 \frac1{2N^2}\sum_{i,k}
 \left(\frac{t_i}{t_k}+\frac{t_k}{t_i}-2\right)
 =
 \frac1{2N^2}\sum_{i,k}\frac{(t_i-t_k)^2}{t_it_k},
\]
and therefore
\[
 \boxed{
 \frac{\bar x_j\bar s_j}{\mu}-1
 =
 \frac1{2N^2}\sum_{i,k=1}^N
 \frac{(t_i-t_k)^2}{t_it_k}.}
\tag{13i*}
\]
Thus the complementarity excess is exactly the multiplicative pairwise
variance of the neighboring primal coordinates. It vanishes if and only if
all \(t_i\) are equal, and it is always nonnegative. This also proves the
lower bound in (13g) directly.
In particular, without invoking \(R\), the smallest width of an
\(\ell_\infty\) neighborhood centered at the original \(\mu\) that contains
the mixture is exactly
\[
 \theta_{\rm mult}
 =
 \max_j\frac1{2N^2}\sum_{i,k}
 \frac{(x_j^{\sigma^{(i)}}-x_j^{\sigma^{(k)}})^2}
      {x_j^{\sigma^{(i)}}x_j^{\sigma^{(k)}}}.
\]

For the ratio-dependent upper bound, note that every
\(t\in[\alpha,\beta]\) obeys
\[
 t+\frac{\alpha\beta}{t}\le \alpha+\beta.
\]
Averaging this inequality and maximizing the product of its two nonnegative
terms under the resulting linear constraint gives the Kantorovich bound
\[
 \left(\frac1N\sum_i t_i\right)
 \left(\frac1N\sum_i\frac1{t_i}\right)
 \le\frac{(\beta+\alpha)^2}{4\alpha\beta}
 \le\frac{(R+1)^2}{4R}.
\tag{13j}
\]
This is precisely the classical scalar Kantorovich inequality, not a new
inequality.  See Kantorovich,
[*Functional analysis and applied
mathematics*](https://www.mathnet.ru/eng/rm8775), Uspekhi Mat. Nauk 3(6)
(1948), and Householder,
[*The Kantorovich and some related
inequalities*](https://doi.org/10.1137/1007104).  Its use here proves
(13g)--(13h); the LP-specific issue is how it combines with neighboring
central triples and the sparse residual estimate.

Assume also that the coordinates of \(x^{\sigma^{(i)}}\),
\(s^{\sigma^{(i)}}\), and the signed free vector
\(y^{\sigma^{(i)}}\) have magnitude at most \(H\). For the stacked
nonnegative system, use the canonical split
\[
 (y^{\sigma^{(i)}})^+_k=\max\{y^{\sigma^{(i)}}_k,0\},
 \qquad
 (y^{\sigma^{(i)}})^-_k=\max\{-y^{\sigma^{(i)}}_k,0\}.
\]
Then \(\bar y=\bar y^+-\bar y^-\) is exactly the arithmetic average of the
signed neighboring dual vectors.  The central points are not optima at
\(\mu>0\), so formally it is the residual proof of Theorem 1, not that
theorem's common-optimum conclusion, that is used here.

In the one-bit-per-position model, the stacked matrix in (13a) has
\[
 s_{\rm KKT}=\max\{s_r,2s_c+1\},\qquad
 B_{\rm KKT}=\max\{B,1\},\qquad M_{\rm KKT}=3M.
\]
Indeed, each input-dependent position of \(A_\sigma\) appears once in the
primal block and twice in the split-dual block; the fixed identity block adds
no input incidence.  Consequently the averages obey the exact bound
\[
 \left\|
 \begin{bmatrix}
 A_\sigma\bar x-b\\
 A_\sigma^\top\bar y+\bar s-c
 \end{bmatrix}
 \right\|_2
 \le
 \frac{2B_{\rm KKT}H\sqrt{3s_{\rm KKT}M}}{N}.
\tag{13k}
\]
For the multi-bit model, one must also control column input-degree.  Put
\[
 d_{\rm KKT}=\max\left\{
 \max_r\left|\bigcup_j I_{rj}\right|,
 \max_j\left|\bigcup_r I_{rj}\right|\right\}.
\]
The general estimate is the right-hand side of (13k) multiplied by
\(\sqrt{d_{\rm KKT}}\).  The second maximum is necessary because each row of
the dual residual block corresponds to a column of \(A_\sigma\).

Exact primal and dual feasibility gives
\[
 c^\top x^{\sigma^{(i)}}-b^\top y^{\sigma^{(i)}}
 =(x^{\sigma^{(i)}})^\top s^{\sigma^{(i)}}=n\mu.
\]
Here \(n\) is the number of primal variables.
The mixture therefore preserves the gap \(n\mu\) exactly, even if the primal
and dual objective values individually vary among neighboring instances:
\[
 c^\top\bar x-b^\top\bar y=n\mu.
\]
Thus no common central-point objective value is assumed; only the data
\(b,c\) and barrier parameter \(\mu\) are common.
The complementarity mean can exceed the gap parameter:
\[
 0\le n\bar\mu-
       (c^\top\bar x-b^\top\bar y)
 \le n[K(R)-1]\mu.
\]
This discrepancy is unavoidable for an infeasible averaged point, but it is
controlled by the same neighborhood width.
If the neighboring points also satisfy the affine or pair-margin output
hypothesis in Section 3, the preceding estimates construct a wrong-output
point having the primal--dual residual (13k), algebraic objective difference
\(n\mu\), and membership in an inexact multiplicative central neighborhood of
width
\[
 \theta=\frac{(R-1)^2}{4R}.
\]
For an amplitude-state output, the pair margin and normalization must refer to
the state actually decoded.  A primal-only state uses the primal dimension and
the bound on \(x\); a state of \((x,y^+,y^-,s)\) uses the full stacked
dimension and its coordinate bound.  A pair margin on \(x\) alone does not
prevent the additional stacked coordinates from diluting a full-state
amplitude measurement.
Equivalently, if neighboring log-coordinates have oscillation at most
\(\rho\), take \(R=e^\rho\); then
\[
 \theta=\sinh^2(\rho/2).
\]
For a prescribed \(\theta\), it is enough that
\[
 R\le 1+2\theta+2\sqrt{\theta(1+\theta)}.
\]
All these inequalities hold for arbitrary \(R\ge1\).  If the term
“central neighborhood” is reserved for the conventional range
\(0\le\theta<1\), then one additionally needs \(R<3+2\sqrt2\).

The theorem also has a weighted form that gives a residual upper bound
together with an exact centrality identity. For weights \(w_i\ge0\),
\(\sum_iw_i=1\), set
\[
 (x_w,y_w,s_w)=\sum_iw_i
 (x^{\sigma^{(i)}},y^{\sigma^{(i)}},s^{\sigma^{(i)}}).
\]
If \(M_i\) is the number of one-bit-dependent positions of \(A_\sigma\)
designated by bit \(i\), the stacked one-bit residual satisfies
\[
 \left\|
 \begin{bmatrix}
 A_\sigma x_w-b\\
 A_\sigma^\top y_w+s_w-c
 \end{bmatrix}
 \right\|_2^2
 \le
 12s_{\rm KKT}B_{\rm KKT}^2H^2\sum_iM_iw_i^2.
\tag{13l}
\]
Meanwhile the complementarity defect is exactly
\[
 \frac{(x_w)_j(s_w)_j}{\mu}-1
 =
 \frac12\sum_{i,k}w_iw_k
 \frac{(t_i-t_k)^2}{t_it_k}.
\tag{13m}
\]
Equation (13l) is the stacked version of Corollary 1.2 in the canonical
one-bit note; (13m) follows from the same symmetrization as (13i*).
Every weighting also preserves the exact algebraic objective difference
\(n\mu\) and a uniform wrong-output affine or pair margin.

If every \(M_i>0\), the weights that minimize the residual upper bound alone
are
\[
 w_i=\frac{M_i^{-1}}{\sum_hM_h^{-1}},
\]
and (13l) becomes
\[
 \left\|
 \begin{bmatrix}
 A_\sigma x_w-b\\
 A_\sigma^\top y_w+s_w-c
 \end{bmatrix}
 \right\|_2^2
 \le
 \frac{12s_{\rm KKT}B_{\rm KKT}^2H^2}
      {\sum_iM_i^{-1}}.
\tag{13n}
\]
This choice need not minimize any joint residual--centrality objective,
because (13m) depends on the actual coordinate ratios \(t_i/t_k\), not only
on the incidence counts.  If some \(M_i=0\), putting all weight on that
neighbor gives zero base-instance residual; it also gives zero complementarity
defect because a single exact central pair is used.  Under the stated uniform
output condition this already defeats the base-instance robust-output
contract.

The weighted formulas give a direct soundness dichotomy.  Define
\[
 \delta_j(w)=\frac12\sum_{i,k}w_iw_k
 \frac{(t_{ij}-t_{kj})^2}{t_{ij}t_{kj}},
 \qquad
 \bar\delta(w)=\frac1n\sum_j\delta_j(w).
\]
There are two central-neighborhood conventions.  Around the neighbors' common
barrier parameter \(\mu\), the exact relative width is
\[
 \Theta_\mu(w)=\max_j\delta_j(w).
\]
For the conventional point-centered parameter
\[
 \mu_w=\frac{x_w^\top s_w}{n}=\mu[1+\bar\delta(w)],
\]
the exact relative width is instead
\[
 \Theta_{\rm pt}(w)
 =\max_j\frac{|\delta_j(w)-\bar\delta(w)|}
                  {1+\bar\delta(w)}.
\]

Suppose a claimed output contract requires the base input's output from every
triple with \(x,s>0\) and free \(y\) whose **absolute Euclidean** combined
feasibility-and-stationarity residual is at most \(\varepsilon\), whose
algebraic objective difference is \(n\mu\), and whose complementarity width
under one specified convention \(\Theta\in\{\Theta_\mu,\Theta_{\rm pt}\}\) is
at most \(\theta\).  Under the uniform wrong-output margin hypothesis,
soundness requires, for every probability vector \(w\),
\[
 \boxed{
 12s_{\rm KKT}B_{\rm KKT}^2H^2\sum_iM_iw_i^2
 >\varepsilon^2
 \quad\text{or}\quad \Theta(w)>\theta.}
\tag{13o}
\]
Here \(t_{ij}=x_j^{\sigma^{(i)}}\).  If neither strict inequality holds, the
upper bound (13l) and the exact identities above show that the weighted
mixture meets every stated certificate, including equality at either allowed
threshold, and has the wrong output.  This explains both the universal
quantifier over \(w\) and the strict inequalities in (13o).

For uniform weights and the ratio bound (13f), the simpler necessary
dichotomy is, for either convention (because both widths are at most
\(K(R)-1\)),
\[
 \frac{12s_{\rm KKT}B_{\rm KKT}^2H^2M}{N^2}
 >\varepsilon^2
 \quad\text{or}\quad
 \frac{(R-1)^2}{4R}>\theta.
\tag{13p}
\]
Thus a linear-size, unit-scale family can support such a central-output
contract only through sufficiently unstable neighboring central coordinates.
The algebraic objective difference in this statement remains \(n\mu\), not
\(n\mu_w\); the two differ because the weighted point need not be feasible.
Thus (13o) does not cover a different contract that explicitly requires the
gap to equal \(n\mu_w\).

Equations (13o)--(13p) use no implicit residual normalization.  If a contract
instead uses \(\|r(w)\|_2/D(w)\le\varepsilon_{\rm rel}\), with a positive
specified denominator \(D(w)\), the first comparison in (13o) must be
replaced by
\[
 12s_{\rm KKT}B_{\rm KKT}^2H^2\sum_iM_iw_i^2
 >\varepsilon_{\rm rel}^2D(w)^2.
\]
A denominator-free corollary needs an independently proved uniform lower
bound on \(D(w)\); it cannot be obtained by silently reinterpreting
\(\varepsilon\).

Thus restricting a robustness theorem to central-neighborhood outputs does not
by itself escape the mixture frontier. It escapes if neighboring central points
can change by sufficiently large coordinate ratios, or if another hypothesis
of the mixture theorem fails. The two-coordinate example preceding Corollary
1.3 shows that some stability condition is necessary.

There is an exact one-bit-local diagonal LP witness showing that upper bounds
on coefficients and central coordinates do not imply this stability. Fix
\(\mu\in(0,1)\), put \(b=\mu\mathbf1\), \(c=0\), and consider
\[
 \min 0
 \quad\text{subject to}\quad
 \operatorname{Diag}(a_1,\ldots,a_N)x=b,\qquad x\ge0.
\]
Let bit \(j\) select \(a_j\in\{\mu,1\}\), independently. The dual equations
are \(a_jy_j+s_j=0\). At barrier parameter \(\mu\), the exact central point is
\[
 x_j=\frac{\mu}{a_j},\qquad s_j=a_j,\qquad y_j=-1.
\]
Take the base input with every \(a_j=\mu\). In the neighbor obtained by
flipping bit \(i\), coordinate \(i\) has
\((x_i,s_i,y_i)=(\mu,1,-1)\), while every other coordinate has
\((x_j,s_j,y_j)=(1,\mu,-1)\). The matrix has row and column sparsity one,
each bit controls one coefficient, and all matrix coefficients and central
coordinates have magnitude at most one. Yet every coordinate of the
single-flip average obeys
\[
 \bar x_j\bar s_j
 =
 \frac{N-1+\mu}{N}\,
 \frac{1+(N-1)\mu}{N},
\]
which is of order \(1/N\) when \(\mu\ll1/N\), rather than of order \(\mu\).
For the base instance, the averaged primal residual norm is
\(\mu(1-\mu)/\sqrt N\), and the dual-stationarity residual norm is
\((1-\mu)/\sqrt N\), both vanishing with \(N\). This example does not encode
parity; its role is to prove that no centrality conclusion follows from
sparsity, one-bit locality, and upper coordinate bounds alone.

For arbitrary weights, this diagonal example makes the tradeoff exact:
\[
 \|(A_\sigma x_w-b,\,
     A_\sigma^\top y_w+s_w-c)\|_2^2
 =(1+\mu^2)(1-\mu)^2\sum_jw_j^2,
\]
\[
 \frac{(x_w)_j(s_w)_j}{\mu}-1
 =\frac{(1-\mu)^2}{\mu}w_j(1-w_j).
\]
Concentrating the weights preserves centrality but, in the regime
\(\mu\ll1/N\), leaves constant-order stationarity residual; spreading them
makes the residual small but destroys centrality. This rules out obtaining a
stability-free central-mixture theorem merely by choosing nonuniform weights.

There is no conflict with the exact central-state parity gadgets elsewhere in
these notes. Their signed output pair has, up to a hidden swap,
\[
 (u,v)=(H+z/2,z/2).
\]
A parity-changing input flip can swap these coordinates, so the neighboring
coordinate ratio is
\[
 R=1+\frac{2H}{z},
\]
which becomes large on the late central path as \(z\) decreases. Those gadgets
deliberately violate the neighbor-stability premise of Corollary 1.4 even when
their reduced Hessian is perfectly conditioned.

## 3. Applying the canonical output criterion to the multi-bit bound

The residual theorem is independent of how parity is represented.  Section 2
and Corollary 2 of the canonical note give the affine and pair-margin
amplitude-state criteria, including the exact factor of two between observable
expectation and binary success-probability bias.  Apply those criteria without
change to the multi-bit residual estimate (1).  They are not restated here so
there is only one authoritative set of decoder assumptions and constants.

## 4. Consequences and limits

1. **Beyond graph propagation.**  The proof permits arbitrary sparse linear
   rows and arbitrary local coefficient functions.  It strictly contains the
   graph setting when all assumptions above hold, although the electrical
   theorem can give sharper instance-specific constants and weighted bounds.
2. **The three amplification currencies.**  The sharp one-bit endpoint table
   and its normalization qualifications are consolidated in the canonical
   note.  The multi-bit theorem here adds the row input-degree factor \(d\) to
   the denominator in (12).
3. **Fixed public objective is essential.**  Exact objective preservation uses
   one common \(c\) and one common optimal value.  If \(c\) depends on the
   input, the neighboring optima need not average to an exact-objective point
   for the base instance.
4. **Bounded selected optima are essential.**  The theorem charges the largest
   coordinate of the neighboring witnesses.  It does not rule out dynamic
   range as an amplification resource; it quantifies it.
5. **Mixture stability is essential for the parity conclusion.** The residual
   bound always holds, but an arbitrary nonlinear or input-dependent output
   decoder need not be preserved by convex averaging.  The canonical note
   states the affine, common-template, and pair-margin sufficient conditions.
6. **No whole-state easiness claim.**  Internal coordinates of \(\bar x\) may
   retain substantial information about \(\sigma\).  The theorem constructs
   a wrong amplified output region, not an input-independent state.
7. **No query lower bound by itself.**  This is a structural impossibility
   theorem for robust parity embeddings.  The separate parity reductions are
   what turn a valid robust embedding into a quantum query lower bound.
8. **Equality-form scope.**  An input-dependent right-hand side can be included
   by applying the theorem to \([A_\sigma,-b_\sigma](x,1)=0\), increasing row
   sparsity by one, counting the dependent right-hand-side positions in \(M\),
   replacing \(H\) by \(\max\{H,1\}\), and using a coefficient bound \(B\)
   that also covers \(b_\sigma\). Linear inequalities are covered
   after ordinary slack conversion only when the selected slack coordinates
   obey the same bound.  Without these qualifications, “arbitrary sparse
   linear constraints” would overstate the theorem.

### Hostile-audit verdict

The residual constants are correct. The multi-bit proof uses one
Cauchy--Schwarz factor \(d\) for the number of input bits touching a row and one
factor \(s\) for the coefficient positions changed by a fixed bit, giving
\(4dsB^2H^2M/N^2\). In the one-bit-per-position model, regrouping directly by
positions removes \(d\) and gives the sharper (11a).

Exact objective preservation is also correct, but only because both the
objective vector \(c\) and the optimum value \(v\) are common to all neighboring
instances. The word “optimal” must not be applied to \(\bar x\) for the base LP,
because \(\bar x\) is generally infeasible; it is an **objective-exact** point.

Finally, residual and objective promises alone say nothing about the normalized
amplitude-state decoder. The quadratic claim is valid under the pair-margin
hypothesis (14) of the canonical note: nonnegativity
turns the signed linear pair margin into

\[
 -p(\sigma)(\bar u_\ell^2-\bar v_\ell^2)
 =[-p(\sigma)(\bar u_\ell-\bar v_\ell)]
   (\bar u_\ell+\bar v_\ell)\ge a^2,
\]

and normalization costs at most \(nH^2\). Without that hypothesis, a common
output template, or another explicit mixture-stability property, no
amplitude-state conclusion is valid. The construction is an existential
contract obstruction, not an efficient procedure for preparing \(\bar x\) and
not a query lower bound by itself.

Corollary 1.3 also survives audit. Convexity is the only cone property used, and
the half-base mixture has residual exactly one half of the neighboring mixture's
residual. Its SDP specialization is basis-dependent: all sparsity, locality,
coefficient, and coordinate bounds refer to the fixed `svec` representation. The
parity-neutral conclusion concerns only the fixed linear map \(L\); it supplies no
amplitude-state or centrality claim.

Corollary 1.4 survives audit as well. Strict positivity makes every minimum in
(13f) positive. The two bounds in (13g) are exactly Cauchy--Schwarz and the
Kantorovich inequality; the latter is sharp for a distribution supported at
the coordinate extremes. The result controls both common central-neighborhood
conventions: centering at the original barrier parameter \(\mu\), or at
\(\bar\mu=\bar x^\top\bar s/n\). The averaged products are generally above
\(\mu\), not equal to it. Fixed \(b,c\) and the signed averaged dual vector
\(\bar y=\bar y^+-\bar y^-\) give the exact algebraic objective difference
\(n\mu\); a common primal objective value is not needed. Because the averaged
point is only approximately feasible, this is not itself a weak-duality
certificate. The approximate stationarity bound still requires bounded
split-dual coordinates and the row-and-column locality accounted for in
(13aa) and (13k).

## 5. Novelty status

The averaging identity and both Cauchy--Schwarz estimates are elementary.
The apparent new point is their use as a general LP gadget frontier tying
input locality, coefficient scale, solution dynamic range, and robust
amplitude-state parity output.  It removes the cycle-consistency and graph
assumptions of the Nash--Williams note.

The boundary is representation- and contract-specific, not an extension-
complexity theorem. Carr--Konjevod's dynamic-programming construction gives an
\(O(N)\)-size extended formulation of the parity polytope
([*Polyhedral Combinatorics*, Section
2.6.3](https://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15854-f05/www/handouts/carr-konjevod.pdf));
Ermel--Walter give modern parity-polytope formulations
([arXiv:1803.10561](https://arxiv.org/abs/1803.10561)). These results show why
one must not summarize (12) as ``parity needs a quadratic-size LP.'' The theorem
instead says that a formulation satisfying the stated common-objective,
bounded-witness, local-input, and mixture-stable robust-output promises must pay
through \(M\), \(B\), or \(H\).

The LDPC literature already establishes the qualitative fractional-point
phenomenon behind the failed sparse-check repair. Feldman--Wainwright--Karger
study LP decoding and pseudocodewords
([DOI:10.1109/TIT.2004.842696](https://doi.org/10.1109/TIT.2004.842696)), while
Koetter--Li--Vontobel--Walker and Vontobel--Koetter relate the fundamental
polytope to finite graph covers
([arXiv:cs/0508049](https://arxiv.org/abs/cs/0508049),
[arXiv:cs/0512078](https://arxiv.org/abs/cs/0512078)). They do not state the
neighbor-instance residual estimate (1). Expander LP decoding can even correct
a constant fraction of errors, so this note does not rule out LDPC/expander
robustness in general: that decoding problem uses a received-word-dependent
objective, whereas (6) requires one common objective and optimum.

Neighboring-input averaging is likewise close in spirit to hybrid/adversary
query arguments such as Ambainis
([arXiv:quant-ph/0002066](https://arxiv.org/abs/quant-ph/0002066)), but those
bound changes in quantum algorithm states. The present identity averages
classical LP witnesses and is not itself an oracle lower-bound technique.
Robust-optimization uncertainty sets and convex adversarial-example
certificates provide further analogies, not theorem matches
([DOI:10.1287/opre.1030.0065](https://doi.org/10.1287/opre.1030.0065),
[arXiv:1711.00851](https://arxiv.org/abs/1711.00851)).

A separate targeted search for convex averages of central points found
well-established neighboring notions, but no theorem with the conjunction in
Corollary 1.4.  Kojima--Megiddo--Mizuno,
[*A primal-dual infeasible-interior-point algorithm for linear
programming*](https://doi.org/10.1007/BF01582151), already place primal and
dual residual bounds beside a complementarity neighborhood.  Mizuno--Todd--Ye,
[*A surface of analytic centers and primal-dual infeasible-interior-point
algorithms for linear programming*](https://doi.org/10.1287/moor.20.1.135),
study a surface of analytic centers determined by one primal--dual problem and
an infeasible start.  Yildirim--Wright,
[*Warm-start strategies in interior-point methods for linear
programming*](https://doi.org/10.1137/S1052623400369235), transfer interior
iterates to a perturbed LP and bound reoptimization effort using perturbation
size and conditioning.  These sources establish that an inexact point may be
judged jointly by feasibility residual and centrality, and that cross-instance
central-path stability is classical.  They do not average the exact centers
of all single-bit neighbors of a base coefficient oracle, nor derive the
\(O(N^{-1/2})\) locality residual and exact algebraic gap \(n\mu\).

The name “Kantorovich” also has two different roles in the nearby literature.
Potra,
[*The Kantorovich Theorem and interior point
methods*](https://doi.org/10.1007/s10107-003-0501-8), applies the
Newton--Kantorovich convergence theorem to path following.  Corollary 1.4
instead uses the scalar arithmetic--harmonic-mean inequality (13j).  Potra's
result is therefore not a collision.  The exact multiplicative-variance
identity (13i*) is elementary, and (13g) is a direct Kantorovich bound; only
their combination with the sparse neighboring-instance residual and output
contract is a defensible apparent-novelty claim.  This is a targeted, not
exhaustive, novelty check.

A targeted primary-literature search through 2026-09-02 found no exact
\(MB^2H^2=\Omega(N^2)\) theorem under this sparse, locally input-dependent LP
contract. Apparent novelty is defensible only for that quantitative conjunction;
the averaging identity, parity extended formulations, pseudocodewords, and
neighboring-input proof pattern are established.

Status: **supplement, proof complete after hostile audit.**  This note retains
the bounded multi-bit-per-coefficient theorem and primal--dual extension.  The
one-bit theorem, pair-margin amplitude-state criterion, and three-currency
frontier are canonical in
`2026-09-02-convex-mixture-local-input-obstruction.md`.  The targeted
primary-literature audit found no exact collision.
