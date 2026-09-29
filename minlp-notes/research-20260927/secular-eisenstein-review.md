# Review of an explicit secular Eisenstein construction

Date: 2026-09-27. Status: the modular identity, irreducibility,
optimal-value primitivity, and finite-family splitting construction below
have been checked independently. This reviewer supplied the simplification
of the constant-term argument and the local proof of value primitivity.
A fresh number-theory reviewer then checked those additions and the
compatible-embedding step. This is a constructive refinement of the
[generic sharpness argument](multihomogeneous-degree-sharpness.md), not a
claim of new Eisenstein or local-field theory.

## 1. A single explicit block

Let $p\equiv1\pmod4$ be prime, $r=p-1$, and choose

\[
 1\le\kappa\le p-1,\qquad \kappa^2\equiv-1\pmod p.
\]

For now take $K=\kappa$; the proof also permits any positive integer

\[
 K\equiv\kappa\pmod{p^2}.                                  \tag{1}
\]

Consider the strictly convex optimization problem

\[
 \min_{\sum_{i=1}^r x_i^2\le1}
 q(x)=\sum_{i=1}^r i x_i^2-2K\sum_{i=1}^r i x_i.           \tag{2}
\]

Its feasible set is compact and has a strictly feasible point. The
unconstrained minimizer has every coordinate equal to $K$, so it lies
outside the ball. The unique constrained optimizer is

\[
 x_i^*=\frac{Ki}{i+\lambda},\qquad \lambda>0,
 \qquad \sum_{i=1}^r\frac{K^2i^2}{(i+\lambda)^2}=1.        \tag{3}
\]

Existence and uniqueness of this positive multiplier also follow directly
from strict decrease of the left side for nonnegative multipliers: its value at zero
is $rK^2>1$, and its limit is zero.

Put

\[
 F(T)=\prod_{i=1}^r(T+i),\quad F_i(T)=F(T)/(T+i),\quad
 P(T)=F(T)^2-K^2\sum_{i=1}^r i^2F_i(T)^2.                  \tag{4}
\]

This monic integer polynomial has degree $2r$ and vanishes at
$\lambda$.

### The modular identity

Over $\mathbb F_p(T)$, $F=T^r-1$, $r=-1$,

\[
 F'=-T^{r-1},\qquad F''=2T^{r-2}.
\]

The logarithmic derivative identity gives

\[
 \begin{aligned}
 \sum_{i=1}^r\frac{i^2}{(T+i)^2}
 &=T^2\left[\left(\frac{F'}F\right)^2-\frac{F''}F\right]
       -2T\frac{F'}F+r\\
 &=\frac{T^{2r}}{F^2}-1.
 \end{aligned}                                            \tag{5}
\]

Multiplying by $F^2$, and using $K^2=-1$ in $\mathbb F_p$, proves

\[
                  P(T)\equiv T^{2r}\pmod p.              \tag{6}
\]

### The constant term already has valuation one

No coefficient adjustment is needed when $K=\kappa$. Write

\[
 \kappa^2+1=kp.
\]

The chosen representative satisfies $1\le k\le p-2$. Since

\[
 1-r\kappa^2=p(1-rk),\qquad 1-rk\equiv1+k\not\equiv0\pmod p,
\]

the integer $1-r\kappa^2$ has $p$-adic valuation exactly one.
Congruence (1) preserves this valuation for $1-rK^2$. Finally,

\[
                P(0)=(r!)^2(1-rK^2),                    \tag{7}
\]

and $r!$ is a $p$-adic unit. Thus (6) and (7) make $P$
Eisenstein at $p$, so it is irreducible and

\[
 [\mathbb Q(\lambda):\mathbb Q]=2r.
\]

Equation (3) and its inverse $\lambda=Ki/x_i^*-i$ show that every individual optimizer coordinate
generates this same degree-$2r$ field.

## 2. The optimal value generates the whole field

Let $\beta=q(x^*)$. Using (3) and the active norm constraint gives

\[
 \beta=-\lambda-K^2\sum_{i=1}^r\frac{i^2}{i+\lambda}.     \tag{8}
\]

Embed $\mathbb Q(\lambda)$ in $\overline{\mathbb Q}_p$, and normalize the valuation by $v_p(p)=1$.
Eisensteinness gives

\[
 v_p(\lambda)=\frac1{2r}.
\]

The following convergent series has coefficients in $\mathbb Z_p$:

\[
 \beta=c_0+c_1\lambda+\sum_{j\ge2}c_j\lambda^j,
\]

where

\[
 c_0=-K^2\frac{r(r+1)}2,\quad c_1=rK^2-1,\quad
 c_j=(-1)^{j+1}K^2\sum_{i=1}^r i^{1-j}\quad(j\ge2).       \tag{9}
\]

Here $v_p(c_0)=v_p(c_1)=1$. For $2\le j\le r$, the
power sum in (9) vanishes modulo $p$, because $1-j$ is not a
multiple of $r$. At $j=r+1$, each summand reduces to one, so
$c_{r+1}$ is a unit. Thus the term $c_{r+1}\lambda^{r+1}$
has strictly smaller valuation than every other term: its valuation is

\[
              v_p(\beta)=\frac{r+1}{2r}<1.               \tag{10}
\]

The infinite tail does not cause a cancellation: for $j>r+1$ its
terms have valuations at least $j/(2r)$, which tend to infinity.
Since $r$ is even, $\gcd(r+1,2r)=1$. The ramification index of $\mathbb Q_p(\beta)$ is therefore divisible by $2r$. Containment in
the degree-$2r$ extension $\mathbb Q_p(\lambda)$ forces equality.
Consequently,

\[
 \mathbb Q(\beta)=\mathbb Q(\lambda)=\mathbb Q(x^*),\qquad
 [\mathbb Q(\beta):\mathbb Q]=2r.                        \tag{11}
\]

This proves the sharp one-constraint degree $2r$ for the explicit
dimensions $r=p-1$, without Hilbert irreducibility. It does not address
every dimension or the full sharp multi-constraint formula.

## 3. Explicit finite families with independent fields

Choose increasing primes

\[
 p_1<\cdots<p_h,\qquad p_j\equiv1\pmod4.
\]

For block $j$, let $r_j=p_j-1$, choose $\kappa_j$ as before, and
set

\[
 L_j=\prod_{\ell>j}p_\ell,\qquad
 t_j\in\{1,\ldots,p_j^2-1\},\quad L_jt_j\equiv1\pmod{p_j^2},
 \qquad K_j=\kappa_jL_jt_j.                              \tag{12}
\]

For the empty product take $L_h=t_h=1$. Then $K_j$ satisfies
(1) at its own prime and is divisible by every later prime. Formula
(12) is explicit and uses integers of bit length

\[
 O\!\left(\sum_{\ell>j}\log p_\ell+\log p_j\right).
\]

### Splitting at a later prime

Fix one block with $a_i=i$, $b_i=Ki$, and a later prime $q>p$
dividing $K$. The $a_i$ are distinct modulo $q$, and every
$b_i$ is divisible by $q$. Fix an index $i$, and substitute

\[
 T=-a_i+b_i u,\qquad c_j(u)=a_j-a_i+b_i u\quad(j\ne i).
\]

There is an exact polynomial identity

\[
 \begin{aligned}
 P(-a_i+b_i u)&=b_i^2H_i(u),\\
 H_i(u)&=(u^2-1)\prod_{j\ne i}c_j(u)^2
      -u^2\sum_{j\ne i}b_j^2\prod_{k\ne i,j}c_k(u)^2.
 \end{aligned}                                            \tag{13}
\]

Modulo $q$, this becomes

\[
 H_i(u)\equiv C_i(u^2-1),\qquad
 C_i=\prod_{j\ne i}(a_j-a_i)^2\not\equiv0\pmod q.         \tag{14}
\]

The roots $u=1,-1$ are simple because $q$ is odd. Hensel lifting
therefore supplies roots $u_i^+,u_i^-\in\mathbb Z_q$, with the
respective residues. Their two corresponding roots of $P$ are distinct
since $b_i\ne0$ and $u_i^+-u_i^-$ is a unit. Roots from different
indices are distinct modulo $q$, since they reduce to the distinct
$-a_i$. Hence all $2r$ roots of $P$ belong to $\mathbb Q_q$.

The simple-root lifting used here is Proposition 7.31 of
[Milne, *Algebraic Number Theory*](https://www.jmilne.org/math/CourseNotes/ANTc.pdf),
printed page 120. The same source develops the valuation and ramification
facts used in (10)–(11) in Chapter 7. These are classical ingredients.

### Compatible embeddings and degree multiplication

Before adjoining block $j$, every earlier block polynomial splits
completely over $\mathbb Q_{p_j}$. Embed their joint splitting field
into $\overline{\mathbb Q}_{p_j}$. Every generating root maps into
$\mathbb Q_{p_j}$, so the entire image lies there. This gives one
compatible embedding of the actual earlier compositum, rather than
unrelated embeddings of its individual factors.

The new block polynomial is Eisenstein over $\mathbb Q_{p_j}$, so it
is irreducible over that embedded compositum. Induction gives

\[
 [\mathbb Q(\lambda_1,\ldots,\lambda_h):\mathbb Q]
                  =\prod_{j=1}^h 2r_j.                 \tag{15}
\]

This is also the joint optimizer field degree of the separable optimization
problem formed from the blocks. Each block value generates its own field,
by (11). Section 5 gives explicit positive integer weights making their
weighted sum generate the compositum. A bare unweighted sum is not asserted
to have that property.

## 4. Boundaries and checks

Distinct Eisenstein primes alone do not prove field independence:
$T^2-6$ is Eisenstein at both 2 and 3 but defines the same field.
The simultaneous splitting property (14) supplies the missing condition.
It is also stronger than merely requiring unramified earlier blocks.

The alternative of forcing squarefree reduction at all earlier primes
would be unsuitable here. If $r>q$, two of the $a_i$ coincide modulo
$q$, forcing a repeated factor in the secular polynomial's reduction.
This observation concerns its polynomial discriminant; it does not itself
prove ramification of the underlying number field.

Targeted command run:

```text
python research-20260927/check_secular_eisenstein.py
```

Result: passed. The script checks Eisenstein coefficients and the value
series for $p=5,13,17,29,37$, computes and factors the exact degree-eight
value resultant for $p=5$, and verifies five digits of each lifted root for every
local branch in the CRT examples $5\to13$, $5\to17$, and
$13\to17$. These exact finite checks support the formulas and catch
arithmetic errors. The general arguments, local-field facts, and all-prime
claims rest on the proofs above. No project-wide verification or CI checks
were run.

## 5. Explicit weights with polynomial bit length

The following addition was checked separately by the reviewer and a fresh
reviewer. It removes the need to search for a primitive linear combination
of the block values. Let $P_*=p_h$, $K_*=\max_j K_j$, and define

\[
 C=4K_*^2(P_*+1)^{2P_*+4},\qquad s=3P_*+1,
 \qquad H=s\left(\lceil\log_2s\rceil+\lceil\log_2C\rceil\right)+1.
                                                               \tag{16}
\]

For one block, distinguish the full product $F$ from its quotients
$F_a=F/(T+a)$. Its value polynomial is

\[
 R(Y)=\operatorname{Res}_T\left(P(T),\,
       (Y+T)F(T)+K^2\sum_{a=1}^r a^2 F_a(T)\right).       \tag{17}
\]

The two arguments have degrees $2r$ and $r+1$ in $T$, so their
Sylvester matrix has size $3r+1\le s$. For the coefficient sum norm,

\[
 \|F\|_1,\|F_a\|_1\le(P_*+1)^{P_*},
\]

and hence

\[
 \begin{aligned}
 \|P\|_1
 &\le(1+K_*^2P_*^3)(P_*+1)^{2P_*}\le C,\\
 \|(Y+T)F+K^2\sum_a a^2F_a\|_1
 &\le(2+K_*^2P_*^3)(P_*+1)^{P_*}\le C.
 \end{aligned}                                            \tag{18}
\]

Each Sylvester entry therefore has coefficient sum norm at most $C$
as a polynomial in $Y$. Determinant expansion gives

\[
                   \|R\|_1\le s!C^s<2^H.               \tag{19}
\]

This resultant has degree exactly $2r$ in $Y$. Indeed,

\[
 P(-a)=-K^2a^2F_a(-a)^2\ne0,
\]

so $P$ and $F$ are coprime. The leading coefficient of (17) in $Y$
is their nonzero resultant. By (11), the block value has degree $2r$.
Thus $R$ is a nonzero integer multiple of its primitive integer minimal
polynomial. Dividing by the integer content lowers the norm, so every
coefficient of that minimal polynomial has absolute value less than $2^H$.
There is no factor-height loss at this step.

### Uniform separation of conjugates

Set $d=2P_*$ and $M=2^{H+1}$. Cauchy's root bound gives absolute value
at most $M$ for every conjugate of every block value. If a block minimal
polynomial has degree $m\le d$ and leading coefficient $a$, its nonzero
integer discriminant gives, for any two distinct conjugates at distance
$\Delta$,

\[
 1\le |a|^{2m-2}\Delta^2(2M)^{m(m-1)-2}.
\]

Consequently,

\[
 \Delta\ge
 2^{-H(m-1)-(H+2)(m(m-1)/2-1)}
 \ge\delta:=2^{-(H+2)d^2}.                               \tag{20}
\]

Every block has $m\ge8$, so the displayed pairwise estimate never needs
an interpretation for a degree-one polynomial.

### An explicit primitive weighted value

Take the integer

\[
 t=1+2^{(H+2)d^2+H+3},\qquad
                 \Theta=\sum_{j=1}^h t^{j-1}\beta_j.    \tag{21}
\]

For two distinct embeddings of the compositum into $\mathbb C$, let
$j$ be the largest index at which the two images of $\beta_j$ differ.
Such an index exists because the block values generate the compositum.
The contribution from that index has magnitude at least
$\delta t^{j-1}$. The preceding indices contribute in total less than

\[
 2M\sum_{i<j}t^{i-1}
 <\frac{2M}{t-1}\,t^{j-1}
 =\frac\delta2\,t^{j-1}.                                \tag{22}
\]

For $j=1$, the preceding sum is zero and the same strict conclusion
holds. No cancellation is possible. All embeddings therefore give
distinct images of $\Theta$, proving that it generates the entire
compositum. This uses separability in characteristic zero, and does not
require that the block fields or their compositum be Galois.

Replacing the separable objective by the weighted sum in (21) preserves
every optimizer, since all weights are positive. If block objectives are
instead normalized so that their values are $\beta_j/2$, the resulting
optimal value is $\Theta/2$ and generates the same field.

Finally, (12) gives $\log_2K_*=O(h\log P_*)$, so

\[
 H=O\!\left((P_*^2+hP_*)\log P_*\right),\qquad
 \log_2t=O\!\left((P_*^4+hP_*^3)\log P_*\right).
\]

The largest objective weight has bit length

\[
 O\!\left((hP_*^4+h^2P_*^3)\log P_*\right).              \tag{23}
\]

In particular, these explicit weights have polynomial bit length in the
total dimension and the number of blocks. Their construction does not use
the degree of the combined field. The constants are conservative; this
argument establishes existence and explicit constructibility, not useful
conditioning or efficient exact arithmetic in the resulting large field.
