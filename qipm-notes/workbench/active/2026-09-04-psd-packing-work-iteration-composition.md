# When the PSD packing Pareto bound composes into total work

Status: Proved conditional frontier; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the geometric and conditional work theorems; novelty
pending specialist review

## Result

Let \(C=(B_2^s)^b\), put \(n=b(s-1)\), and consider a globally labelled
bi-\(C^1\) real-PSD factorization through blocks of orders \(r_i\leq R\).
Assume the factors are genuine affine-slice certificates for the restricted
standard log-determinant barrier.

There is a support objective for which the aggregate exposing slack has
block ranks \(q_i\), total rank \(Q=\sum_iq_i\), and

\[
                 \boxed{n\leq\sum_i p_iq_i,\qquad
                        p_i=\operatorname{rank}X_i\leq r_i-q_i.}       \tag{1}
\]

The same \(Q\) controls the path-independent Dikin distance to objective
accuracy. Thus curvature capacity and iteration movement can be composed;
one does not need to replace \(Q\) by the possibly larger barrier parameter
\(\nu\).

Define \(J_\omega=\sum_i r_i^\omega\). Consider a
**\(J_\omega\)-explicit bounded-Dikin method**: it starts at a fixed
interior reference point, every counted round moves intrinsic
standard-barrier distance at most \(B\), and every round performs at least
\(aJ_\omega\) charged work, for fixed \(a,B>0\). Examples include a
factor-synchronous block-touch contract at \(\omega=0\), a fresh
rank-length serialization contract at \(\omega=1\), and a fresh dense
block serialization contract at \(\omega=2\). These are model
requirements, not automatic costs of an implementation and not
consequences of sparse quantum oracle access.

For the objective selected above, every such method reaching
\(\epsilon<\Delta_c\) has total charged work

\[
\boxed{
 {\cal W}_\omega\geq {a\over B}\,{25\over6}\sqrt{5\over3}\,
 {n^{3/2}\over R^{(5-2\omega)/2}}
 \log{\Delta_c\over\epsilon},\qquad 0\leq\omega\leq{5\over2}.}        \tag{2}
\]

For dense real PSD cone coordinates,

\[
 M=\sum_i{r_i(r_i+1)\over2}\geq {1+1/R\over2}J_2,
\]

so an \(M\)-explicit method obeys

\[
 {\cal W}_M\geq {a\over B}\,{25\over12}\sqrt{5\over3}\,
 \left(1+{1\over R}\right){n^{3/2}\over\sqrt R}
 \log{\Delta_c\over\epsilon}.                              \tag{3}
\]

In divisible cap-active families, the \(p:c=3:2\) column packing and its
fiber-centered path attain the resource powers and sharp \(3:2\) aspect in
(2)--(3), up to replacing \(s-1\) by \(s\), the reference-scale logarithm,
and fixed step constants. The algebraic-resource ratio is
\((s/(s-1))^{3/2}\). This is a rigorous end-to-end asymptotic frontier
**inside the explicit per-round work model**.

The full-cone \(M\)-serialization contract counts public identity entries.
If a lifted implementation serializes only genuinely free affine
coordinates, the exact packed ledger is instead
\[
                V=bs+\sum_\ell {c_\ell(c_\ell+1)\over2}.
\]
For every barrier exponent, \(V\nu^\theta\) is minimized by
\(c_\ell=1\) and a largest feasible row width. Thus this more economical
materialization model selects grouped Schur blocks, not \(3:2\).

It does not give an oracle-query lower bound for a general QIPM. A fixed
instance can reveal or prepare its factor data once and reuse them at every
checkpoint; on the packed hard path, every center is obtained from the same
objective directions by public scalar rescaling. Consequently neither an
\(\Omega(J_\omega)\) input-query charge nor an independent output charge is
forced anew each round. Without an explicit synchronization/materialization
contract or a temporal direct-product theorem, \(J_\omega\sqrt{\nu}\) and
\(J_\omega\sqrt Q\) must remain QIPM proxies.

## 1. The aggregate contact rank carries all curvature

For positive weights \(\lambda_a\), form the weighted full slack

\[
 {\cal S}(x,z)=\sum_{a=1}^b\lambda_a(1-x_a^Tz_a)
   =\sum_i\operatorname{tr}\bigl(X_i(x)S_i(z)\bigr),\qquad
 S_i(z)=\sum_a\lambda_aY_i^a(z_a).                         \tag{4}
\]

At a simultaneous contact \(x_a=z_a=u_a\), its mixed derivative on the
two copies of \(\bigoplus_aT_{u_a}S^{s-1}\) is

\[
              -\sum_a\lambda_a\langle h_a,k_a\rangle,
\]

which has rank \(n\). Positivity and zero pairing give
\(X_i(u)S_i(u)=0\). Put

\[
 U_i=\operatorname{Ran}X_i(u),\qquad
 W_i=\operatorname{Ran}S_i(u)
      =\sum_a\operatorname{Ran}Y_i^a(u_a).                 \tag{5}
\]

The equality in (5) uses positivity of the weights. For a two-sided
\(C^1\) PSD-valued map, the derivative at a singular point has zero
kernel--kernel compression. Therefore the mixed form
\(\operatorname{tr}(DX_i[h]\,DS_i[k])\) can use only the common
off-diagonal channel
\(\operatorname{Hom}(W_i,U_i)\), of real dimension \(p_iq_i\).
Rank subadditivity proves (1); the transpose block is not a second
independent channel.

The weighted matrix \(S_i(u)\) is exactly the dual certificate block for
the support objective in (4), and its rank is \(q_i\). Hence the aggregate
rank in (1) is the same invariant used by the
[exposed-rank Dikin theorem](2026-09-04-symmetric-cone-exposed-rank-dikin-lower-bound.md),
not merely a boundary-nullity upper bound.

## 2. Universal work times movement

Enlarge \(p_i\), if necessary, to \(r_i-q_i\); this can only increase the
right side of (1). Write \(p_i=x_ir_i\), \(q_i=(1-x_i)r_i\). For
\(0\leq\omega\leq5/2\),

\[
 p_iq_i\leq K R^{(5-2\omega)/3}
       r_i^{2\omega/3}q_i^{1/3},\qquad
 K={3\over5}\left({2\over5}\right)^{2/3}.                 \tag{6}
\]

Indeed, the shape factor is \(x(1-x)^{2/3}\), uniquely maximized at
\(x=3/5\), and the residual scale power is nonnegative in the stated
range. Hölder and (1) give

\[
 n\leq K R^{(5-2\omega)/3}J_\omega^{2/3}Q^{1/3},
\]

or

\[
 J_\omega\sqrt Q\geq {25\over6}\sqrt{5\over3}\,
              {n^{3/2}\over R^{(5-2\omega)/2}}.           \tag{7}
\]

Starting at the reference point in the exposed-rank theorem, any path to
objective gap \(\epsilon\) has standard-barrier distance at least

\[
                         \sqrt Q\log(\Delta_c/\epsilon).   \tag{8}
\]

At distance at most \(B\) per round, (8) needs at least its right side
divided by \(B\) rounds. Multiplying by the model's \(aJ_\omega\)
per-round charge and applying (7) proves (2). Equation (3) follows from
\(r_i\leq R\).

For rounds containing at most \(m\) feasible chords of starting local norm
at most \(\rho<1\), one may take

\[
                         B=m\log{1\over1-\rho}.            \tag{9}
\]

Thus the model includes the usual bounded-short-step geometry but allows
arbitrary predictor, corrector, or geodesic directions inside each bounded
round.

## 3. Matching packed path

Let every source ball be split into \(h=s/p\) groups and pack \(c\) groups
per full order-\(R=p+c\) block. Put \(H=bh=bs/p\) and \(L=H/c\). Partial
minimization of the packed standard barrier gives

\[
       \bar F(x)=-h\sum_{a=1}^b\log(1-\|x_a\|^2)+H\log h. \tag{10}
\]

For the objective \(\ell(x)=\sum_ac_a^Tx_a\), \(\|c_a\|=1\), the
fiber-centered central path has \(x_a=r(\tau)c_a\). Its logarithmic speed
tends to \(\sqrt H\), and bounded-Dikin checkpoints reach gap \(\epsilon\)
in

\[
                       O\!\left(\sqrt H\log{b\over\epsilon}\right)     \tag{11}
\]

rounds. The matching lower bound is path-independent. If
\(\delta_a=1-c_a^Tx_a\) and \(D_\ell=S_\ell-W_\ell^TW_\ell\), then

\[
 \sum_{\gamma\in\Gamma_a}(D_{\ell(\gamma)})_{\gamma\gamma}
       =1-\|x_a\|^2\leq2\delta_a.                         \tag{12}
\]

Hadamard followed by AM--GM over all \(H\) diagonal residuals shows that
every point of gap at most \(\epsilon\) has

\[
 -\sum_\ell\log\det D_\ell\geq H\log{H\over2\epsilon}.    \tag{13}
\]

The analytic center has barrier value \(H\log h\), so the required barrier
increase is at least \(H\log(b/(2\epsilon))\). Since the restricted
gradient local norm is at most \(\sqrt H\), every path has length at least
\(\sqrt H\log(b/(2\epsilon))\). This proves the lower counterpart to (11)
without a central-neighborhood assumption.

At the support contact, the \(c\) dual contact vectors in every full packed
block are independent because their top coordinates are distinct basis
vectors. Thus \(q_i=c\) and \(Q=Lc=H\), so (7) is asymptotically tight.
Choosing \(p=3R/5\), \(c=2R/5\) gives

\[
 J_\omega\sqrt H={25\over6}\sqrt{5\over3}\,
        {(bs)^{3/2}\over R^{(5-2\omega)/2}},              \tag{14}
\]

and the exact cone-coordinate version has the common factor
\((1+1/R)/2\). Under the explicit per-round contract, writing or touching
the required records and using the closed-form centered update gives the
matching upper bound. Equations (2), (7), and (14) establish the claimed
asymptotic total frontier.

## 4. Why this is not a general QIPM query theorem

The per-round cost premise is indispensable.

1. **Ledger padding.** Public constant or zero-coupled cone blocks can be
   appended without changing the projected problem or any Newton
   direction. They increase \(L\), \(J_\omega\), and the ambient cone
   ledger, but an algorithm can ignore them. Thus no per-round lower bound
   can be a monotone function of the raw factor ledger without a
   minimality or explicit-processing contract.
2. **Input reuse.** Cone blocks and affine data describe one fixed
   optimization instance. Reading or preprocessing them once can support
   all later rounds. A one-shot query lower bound does not tensor across
   time.
3. **Ray collapse.** On the packed path above, all source directions
   \(c_a\) are fixed. Every center and predictor is obtained by public
   scalar functions of the path parameter. A reusable classical record or
   state-preparation circuit defeats a fresh \(\Omega(J_\omega)\) query
   charge at each checkpoint.
4. **Output contract.** A classical algorithm that explicitly overwrites
   every block record pays the stipulated work. A lazy representation, a
   queryable wrapper, a quantum state, one observable, and a final explicit
   iterate are different outputs. Only the first is charged automatically
   every round.

The fixed sparse-KKT ray in
[temporal collapse of repeated QLS costs](2026-09-04-fixed-instance-sparse-kkt-temporal-collapse.md)
makes the obstruction exact: the movement count can grow as
\(\log(1/\epsilon)\) while the normalized KKT solution state is identical
at every checkpoint. Therefore multiplying a one-shot QLS query lower
bound by (8) is invalid even on one fixed sparse conic program.

There is an equally explicit obstruction inside the present packed family.
Choose dense sign objectives
\[
                      c_{aj}={\sigma_{aj}\over\sqrt s},
                      \qquad \sigma_{aj}\in\{-1,1\}.
\]
With the canonical phase oracle for \(\sigma\), one query applied to the
public uniform superposition prepares
\[
             {1\over\sqrt{bs}}\sum_{a,j}\sigma_{aj}|a,j\rangle.       \tag{15a}
\]
Every nonzero projected center \(x(\tau)=r(\tau)c\), \(\tau>0\), and predictor
\(\dot x(\tau)=r'(\tau)c\) has exactly this normalized state, independently
of \(\tau\). The public grouping map relabels the same amplitudes as the
packed \(W\)-coordinate state. Thus fresh state preparation at each of
\(T\) checkpoints costs one phase query per checkpoint, not
\(\Omega(L)\), even when \(L\) grows. A reusable preparation circuit makes
the temporal redundancy more explicit. This does not upper-bound the cost
of every other QIPM subroutine, but it is a direct counterexample to any
claim that factor count alone forces \(\Omega(L)\) state-preparation
queries per round.

For a classical implementation whose interface requires a fresh
serialization each round, the conditional model is a literal
memory-bandwidth or materialization lower bound. It is not an unconditional
lower bound for every classical implementation, because a structured or
lazy representation can also reuse data.
For a QIPM, (2) becomes an end-to-end theorem only after one proves a
fresh-information direct product, mandates classical factor output each
round, or otherwise derives the \(aJ_\omega\) charge from the access and
output contract. None of those properties follows from sparsity,
conditioning, or the number of IPM rounds alone.

## 5. The conventional reduced-work frontier is different

The packed formulation has an
[exact auxiliary-centered Newton forest](2026-09-04-psd-column-packing-newton-forest.md).
After eliminating the residual variables, a Newton solve can be performed
in \(O(bs+H)=O(bs)\) arithmetic and storage, independently of the
column-to-block packing, where

\[
                         H=b\left\lceil{s\over p}\right\rceil .
\]

Together with the bounded-Dikin round upper bound from Section 3, the
standard reduced-work upper certificate is

\[
 O\!\left(bs\sqrt{b\left\lceil{s\over p}\right\rceil}
                 \log{b\over\epsilon}\right).             \tag{15}
\]

If the interface requires a fresh explicit projected iterate at every
checkpoint and the selected objective directions are dense, its
\(\Omega(bs)\) word writes per round, together with the path lower bound,
make (15) a matching \(\Theta\) bound. Within
that explicit projected-coordinate model, (15) is minimized by

\[
                         p=\min\{s,R-1\}.                  \tag{16}
\]

In the cap-active branch this leaves \(c=1\), the grouped Schur point.
Thus \(3:2\) is the correct optimum when factor or block serialization is
the charged bottleneck, while the largest possible row width is optimal
when the exactly reduced Newton arithmetic is charged. This is a genuine
model-dependent Pareto split, not a contradiction.

Even the projected-write lower bound disappears if checkpoints may retain
a lazy ray representation and only the final iterate must be explicit.
Equation (15) should therefore be read as an exact frontier for the stated
explicit-checkpoint contract and as an upper bound for ordinary reduced
classical implementations.

## Scope and novelty boundary

Equation (1) needs globally labelled bi-\(C^1\) factors. Equations
(2)--(3) additionally need affine-slice dual certificates, the standard
log-determinant, a fixed interior reference, bounded Dikin movement, and
the explicit per-round work contract. The matching construction assumes
full divisible packed blocks; exact ceilings are enumerated in
[the PSD packing Pareto ledger](2026-09-04-psd-column-packing-pareto.md).

The aggregate-capacity/Dikin composition appears not to be stated in the
screened literature, but priority is not established. The negative QIPM
conclusion is a model-separation result, not an unconditional quantum
lower bound.

## Independent-audit checklist

1. Verify the aggregate mixed-rank inequality (1), including the absence
   of a spurious factor two.
2. Check that the dual rank \(Q\) in (1) is exactly the exposing rank in
   the Dikin theorem.
3. Recheck Hölder, constants, and the range \(0\leq\omega\leq5/2\).
4. Verify the packed barrier-height proof for arbitrary block sharing.
5. Check the upper-bound claim under the stated explicit-work contract and
   the fixed-instance reuse obstruction outside it.

## Independent hostile audit

The audit rederived (1) from the common
\(\operatorname{Hom}(\operatorname{Ran}S_i,\operatorname{Ran}X_i)\)
off-diagonal channel and confirmed that positive row weights make
\(\operatorname{Ran}S_i=\sum_a\operatorname{Ran}Y_i^a\). Thus the rank
\(Q\) in the curvature bound is exactly the rank of the exposing slack in
the Dikin-distance theorem. It independently checked the Hölder exponents,
the constant \((25/6)\sqrt{5/3}\), and the full range
\(0\leq\omega\leq5/2\).

For arbitrary column sharing, the audit verified (12), Hadamard and AM--GM
over all \(H\) residual diagonals, the center value \(H\log h\), and the
resulting path-independent distance
\(\sqrt H\log(b/(2\epsilon))\). At a packed support contact, the distinct
top basis coordinates make the \(c\) dual vectors in each block
independent, so \(Q=H\); the \(3:2\) substitution and common triangular
coordinate factor are correct.

Finally, the audit confirmed that upper and lower total-work bounds match
only under the stated fresh materialization contract. Ledger padding,
fixed-input reuse, scalar ray rescaling, and differing output formats all
invalidate an unconditional per-round query charge. No mathematical
correction was required.

A follow-up audit checked the phase-state obstruction (15a). The
concatenated sign direction has norm \(\sqrt b\), so every nonzero center
and predictor normalizes to the displayed state; padding and grouping are
public relabelings with known zero amplitudes. The qualification
\(\tau>0\) excludes only the zero center, whose normalized state is
undefined.
