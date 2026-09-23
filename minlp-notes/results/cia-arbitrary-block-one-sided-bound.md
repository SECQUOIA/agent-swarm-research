# An explicit one-sided CIA bound for any number of activation blocks

Status: developed 2026-09-04 and [independently proof-reviewed](../notes/review-cia-arbitrary-block-one-sided.md). Targeted primary-literature comparison in [the novelty audit](../notes/cia-novelty.md) found no matching statement; this does not certify novelty. The result follows from an inductive construction that removes one mode and distributes its relaxed allocation among the remaining modes. No higher-order distinct-reach conjecture is assumed.

Let α:[0,T]→Δ_n be measurable, let A_i(t)=∫_0^tα_i(u)du, and let W_i(t)=∫_0^tω_i(u)du for an integer-mode control ω. Define the one-sided error

\[
 D^-(\alpha,\omega)=\max_i\sup_{0\le t\le T}(W_i(t)-A_i(t)).
\]

**Theorem.** For every n≥2 and integer 1≤k<n, a schedule using at most k distinct activation blocks satisfies

\[
 \boxed{D^-(\alpha,\omega)\le C_{n,k}T,\qquad
 C_{n,k}=\frac{n(n-1)+(n-k)(n-k-1)}{nk(2n-k-1)}.} \tag{1}
\]

Each selected mode is used in only one block. This is an upper bound, not an exact finite-n minimax claim.

## Mode removal and the inductive step

We prove a recurrence before solving it. The base k=1 is C_{n,1}=(n−1)/n: choose a mode of maximum terminal mass a≥T/n and activate it throughout. Its negative discrepancy is t−A_i(t), which is nondecreasing and ends at T−a≤(n−1)T/n. Every unselected mode has nonpositive negative discrepancy.

Suppose a one-sided upper coefficient C=C_{n-1,k-1} is available in n−1 modes with at most k−1 distinct blocks and satisfies C≥1/(n−1). Put

\[
 E=\frac{(n-1)^2C+1}{n(n-1)(1+C)}T. \tag{2}
\]

In particular E≥T/n, because subtracting 1/n from the coefficient in (2) gives

\[
 \frac{(n-2)((n-1)C-1)}{n(n-1)(1+C)}\ge0.
\]

Choose q of maximum terminal mass a=A_q(T). If a≥T−E, activate q throughout; its negative discrepancy is at most E. Otherwise set

\[
 L=T-a-E>0,\qquad E'=E-\frac a{n-1}>0.
\]

The latter positivity follows from a<T−E≤(n−1)E. On the remaining n−1 modes define

\[
 \widehat\alpha_i=\alpha_i+\frac{\alpha_q}{n-1},
 \qquad \widehat A_i=A_i+\frac{A_q}{n-1}.
\]

These completed rates are simplex-valued. Apply the inductive schedule to their restriction to [0,L]. It has negative discrepancy at most CL, which is at most E' provided

\[
 E\ge\frac{CT+(1/(n-1)-C)a}{1+C}. \tag{3}
\]

Since C≥1/(n−1), the right side is nonincreasing in a. Using a≥T/n shows that (2) implies (3).

For each prefix mode, its negative discrepancy against the original relaxed control is at most

\[
 E'+\frac{A_q(t)}{n-1}\le E.
\]

Append q on [L,T]. Its negative discrepancy during that block is t−L−A_q(t), a nondecreasing function ending at E. Earlier modes receive no more service, so their negative discrepancies cannot increase. The prefix avoids q, hence all selected modes remain distinct. This proves the recurrence (2).

## Closed form

Write D_{n,k}=nC_{n,k}. The recurrence becomes

\[
 D_{n,k}=\frac{(n-1)D_{n-1,k-1}+1}{n-1+D_{n-1,k-1}}.
\]

Under the transform η=(D−1)/(D+1), this is

\[
 \eta_{n,k}=\frac{n-2}{n}\eta_{n-1,k-1}.
\]

Since D_{m,1}=m−1, telescoping gives

\[
 \eta_{n,k}=\prod_{j=n-k+1}^n\frac{j-2}{j}
 =\frac{(n-k)(n-k-1)}{n(n-1)}.
\]

Solving for D yields (1). The expression has C_{n,k}≥1/n whenever k<n, so every inductive hypothesis concerning this inequality holds. At k=n−1 the coefficient is exactly 1/n. ∎

## Consequences and limits

If every terminal mode mass is at most C_{n,k}T, the same schedule has both signs of cumulative error at most C_{n,k}T: positive discrepancies are bounded by terminal masses. In particular this applies to all controls with equal terminal masses T/n, regardless of their temporal profile.

Let G^-_{n,k}(T) be the unrestricted-profile one-sided minimax with at most k blocks. Let G^=_{n,k}(T) be the two-sided minimax over profiles with equal terminal masses. The exact uniform-control one-sided lower bound is

\[
 L_{n,k}=\frac1{n((n/(n-1))^k-1)}.
\]

For every fixed k and n→∞,

\[
 \begin{aligned}
 C_{n,k}&=\frac1k-\frac{k+1}{2kn}
 +\frac{k^2-1}{4kn^2}+O_k(n^{-3}),\\
 L_{n,k}&=\frac1k-\frac{k+1}{2kn}
 +\frac{k^2-1}{12kn^2}+O_k(n^{-3}).
 \end{aligned}
\]

Uniform controls are admissible in both minimax problems. Since their two-sided value is at least their one-sided value, the bounds squeeze both quantities:

\[
 \boxed{G^\bullet_{n,k}(T)
 =\frac Tk-\frac{(k+1)T}{2kn}+O_k(T/n^2),\qquad \bullet\in\{-,=\}.} \tag{4}
\]

Each minimax quantity has the displayed expansion through order 1/n; equality of their exact finite-n values is not asserted. The difference between the explicit upper and uniform lower coefficients is

\[
 C_{n,k}-L_{n,k}=\frac{k^2-1}{6kn^2}+O_k(n^{-3}).
\]

The leading T/k is already a known coarse-block rounding consequence. The matching first mode-count correction for arbitrary fixed k, including the full two-sided equal-total problem, is the claim requiring literature comparison. No universal two-sided bound is asserted for profiles with large terminal mode masses.


## Verification

`code/cia_tv_conjecture/arbitrary_block_certificate.py` checked 330 arbitrary and 66 equal-total exact-rational inputs, including every 1≤k<n through n=12. A separate independent implementation checked 360 rational recursive constructions and all 928 intermediate recursive contracts, plus 241 full-error mass-qualified cases. These computations support the analytic proof rather than replace it.
