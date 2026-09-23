# Sharp vanishing-residual threshold for the all-unit plateau family

## Result

The bounded all-unit parity LP becomes robust at the sharp vanishing scale
\(\Theta(N^{-1/2})\) after replacing the individual equations \(h_i=1\) by one
pinned unit recurrence.  This replacement preserves the exact feasible set,
central path, scalar reduced Hessian, public centered Newton start, and exact
Newton direction.  It changes the right-hand-side norm from \(\Theta(\sqrt N)\)
to

\[
 \|b\|_2=\sqrt2.
\]

For \(P=17N+1\), every nonnegative point with

\[
 \|Ax-b\|_2\le\frac1{16\sqrt N}                            \tag{1}
\]

has the correct signed difference at **every** one of the \(16N\) output
plateau nodes.  Its normalized amplitude state has constant parity bias.  Thus
preparing such a state to constant trace error takes
\(\Omega(N)=\Omega(P)\) raw coefficient queries.  In relative form, (1) is

\[
 \frac{\|Ax-b\|_2}{\|b\|_2}
 \le\frac1{16\sqrt{2N}}.                                  \tag{2}
\]

The order is sharp.  There is a nonnegative zero-output-signal point with
absolute residual \(1/\sqrt N\), and a point whose entire plateau has the wrong
parity with residual \(2/\sqrt N\).  Their relative residuals are respectively
\(1/\sqrt{2N}\) and \(\sqrt{2/N}\).

## 1. Reference-recurrence formulation

Let \(N\ge2\), \(K=16N\), and \(P=N+K+1=17N+1\).  At node
\(i=0,\ldots,P-1\), use nonnegative variables \((u_i,v_i,h_i,t_i)\), with

\[
 d_i=u_i-v_i,\qquad q_i=u_i+v_i.
\]

Let \(a_i=\sigma_i\) for \(1\le i\le N\) and \(a_i=1\) afterward.  The
equalities are

\[
\begin{aligned}
 d_0&=1,&d_i-a_id_{i-1}&=0 &&(1\le i<P),\\
 h_0&=1,&h_i-h_{i-1}&=0 &&(1\le i<P),\\
 &&q_i+t_i-2h_i&=0 &&(0\le i<P).
\end{aligned}                                               \tag{3}
\]

Use the same public objective as the bounded exact-state family,

\[
 c^Tx=\sum_i\left[\frac{43}{36}(u_i+v_i)+h_i+t_i\right].  \tag{4}
\]

Only the two root anchors in (3) have nonzero right-hand sides, proving
\(\|b\|_2=\sqrt2\).  The pinned signed-difference block and pinned reference
block are nonsingular, and every cap row has a private \(t_i\) pivot.  Hence the
\(3P\) rows have full rank.  Row and column sparsity are at most four and three,
respectively, and every matrix coefficient has magnitude at most two.

Exact feasibility still gives

\[
 d_i=\tau_i,\qquad h_i=1,
 \qquad t_i=2-q_i,qquad1\le q_i\le2,                     \tag{5}
\]

where \(\tau_i=\prod_{j\le i}a_j\).  Thus every exact feasible-set, optimum,
strict-complementarity, and nondegeneracy calculation in
`2026-09-02-bounded-range-exact-only-condition-one-hardness.md` is unchanged.
The input-independent orthonormal null basis remains

\[
 W_i=\sqrt{\frac23}
 \left(\frac12e_{u_i}+\frac12e_{v_i}-e_{t_i}\right).      \tag{6}
\]

The exact central point, public complementarity-centered start, secant identity,
and primal Newton direction are also unchanged.  In particular, the reduced
central Hessian is a scalar identity for every \(\mu>0\), and the start reduced
Newton matrix is \((22/27)I\).  Replacing separate \(h_i\) anchors by the pinned
recurrence changes only the row representation, not the feasible affine space or
the nullspace.

## 2. Parameterized recurrence stability

Let \(x\ge0\), \(x\ne0\), and set

\[
 E:=\|Ax-b\|_2.
\]

Write the signed-difference residuals as

\[
 e_0^d=d_0-1,qquad e_i^d=d_i-a_id_{i-1},
\]

and the reference residuals as

\[
 e_0^h=h_0-1,qquad e_i^h=h_i-h_{i-1}.
\]

Gauge the difference recurrence by \(z_i=\tau_i d_i\).  Since
\(\tau_i=a_i\tau_{i-1}\),

\[
 z_i-z_{i-1}=\tau_i e_i^d.
\]

Telescoping and Cauchy--Schwarz give, simultaneously for every node,

\[
 |z_i-1|
 \le\sqrt{i+1}\,\|(e_0^d,\ldots,e_i^d)\|_2
 \le\sqrt P\,E.                                           \tag{7}
\]

The unsigned reference recurrence gives identically

\[
 |h_i-1|\le\sqrt P\,E.                                    \tag{8}
\]

The factor \(\sqrt{i+1}\) in (7) is exact: equality is attained when the
anchor and all preceding transition residuals are equal after the gauge.
Consequently \(E<1/\sqrt P\) is the sharp recurrence-only threshold that
forces the correct sign through the final plateau node.

Concretely, take \(z_i=1-(i+1)/P\) for \(0\le i<P\), set
\(d_i=\tau_i z_i\), and keep \(h_i=q_i=t_i=1\).  The anchor and every
difference transition then have residual \(-1/P\) after gauging, so the total
residual is exactly \(1/\sqrt P\) and the final node has \(z_{P-1}=0\).
All variables remain nonnegative.  Thus the strict inequality and constant in
the recurrence-only sign threshold cannot be improved.

Put

\[
 \delta:=\sqrt P\,E.
\]

When \(\delta<1\), every plateau node obeys

\[
 \tau_Nd_i=z_i\ge1-\delta>0.                              \tag{9}
\]

Thus the signed difference has the correct parity throughout the plateau, not
only on average.

## 3. Automatic coordinate and state-norm bounds

Let

\[
 r_i^c=q_i+t_i-2h_i
\]

be a cap residual.  Since \(|r_i^c|\le E\) and \(q_i,t_i\ge0\), equations
(8) and the cap give

\[
 q_i,t_i\le2h_i+|r_i^c|
 \le2(1+\delta)+E=:B.                                    \tag{10}
\]

Also \(u_i^2+v_i^2\le q_i^2\).  Hence

\[
 \|x\|_2^2
 \le P\left[2B^2+(1+\delta)^2\right].                    \tag{11}
\]

This bound uses no objective or centrality promise.  The pinned reference
recurrence and nonnegative cap variables automatically prevent a large-norm
coordinate loophole at the same residual scale as the parity recurrence.

For the concrete threshold (1), \(P/N\le35/2\) for \(N\ge2\), so

\[
 \delta\le\frac{\sqrt{35/2}}{16}<\frac4{15},
 \qquad E<\frac1{20}.                                    \tag{12}
\]

Therefore

\[
 z_i>\frac{11}{15},\qquad h_i<\frac{19}{15},
 \qquad B<\frac{31}{12},                                 \tag{13}
\]

and

\[
 \|x\|_2^2
 <P\left[2\left(\frac{31}{12}\right)^2
          +\left(\frac{19}{15}\right)^2\right]
 <15P.                                                     \tag{14}
\]

## 4. Constant-bias decoder and query lower bound

Let \(S=\{N+1,\ldots,N+K\}\) be the \(K=16N\) copy-plateau nodes.  On a
computational-basis measurement, report \(+1\) on \(u_i\), \(-1\) on \(v_i\)
for \(i\in S\), and report a fair sign elsewhere.  Since nonnegativity gives
\(q_i\ge|d_i|\), (9) and (13) imply

\[
 \tau_Nd_iq_i\ge\left(\frac{11}{15}\right)^2
 \qquad(i\in S).                                         \tag{15}
\]

The ideal amplitude-state bias toward \(p_N=\tau_N\) is therefore

\[
 \beta
 =\frac1{2\|x\|_2^2}\sum_{i\in S}\tau_Nd_iq_i
 >\frac{16N(11/15)^2}{30P}
 \ge\frac{16(121/225)}{30(35/2)}
 >\frac1{70}.                                              \tag{16}
\]

Trace distance \(1/400\) reduces this measurement bias by at most \(1/400\),
leaving a positive constant.  A fixed number of independently prepared copies
therefore computes parity with bounded error.

Each coherent fixed-position sparse row, column, position, or value query to
(3) exposes at most one \(\sigma_i\) and is simulated by at most one standard
sign-oracle query.  Quantum parity needs \(\Omega(N)\) queries.  We obtain:

**Theorem 1 (all-unit vanishing-residual state hardness).**  If an algorithm
outputs an unconditional density operator \(\rho\) for which there is a nonzero
\(x\ge0\) satisfying (1) and

\[
 D_{\rm tr}\left(\rho,
 |x/\|x\|_2\rangle\langle x/\|x\|_2|\right)
 \le\frac1{400},                                          \tag{17}
\]

then it makes \(\Omega(N)=\Omega(P)\) raw sparse coefficient queries.  The same
holds for a constant-success heralded branch after its repetition overhead is
charged.  No objective, dual-feasibility, or centrality promise is used.

More generally, (7)--(11) give an explicit bias formula for every
\(E<1/\sqrt P\):

\[
 \beta(E)\ge
 \frac{K(1-\sqrt P E)^2}
 {2P\left\{2[2(1+\sqrt P E)+E]^2+(1+\sqrt P E)^2\right\}}.
                                                               \tag{18}
\]

Thus any fixed margin below the sharp sign threshold \(1/\sqrt P\) gives a
constant normalized-state bias when \(K=\Theta(P)\).

## 5. Matching drift obstructions

The \(N^{-1/2}\) order cannot be improved for this family.  Keep
\(h_i=q_i=t_i=1\), so every reference and cap equation is exact and all variables
remain nonnegative whenever \(|d_i|\le1\).

For a zero-signal plateau, set

\[
 z_i=1-\frac{i}{N}\quad(0\le i\le N),
 \qquad z_i=0\quad(i>N),
 \qquad d_i=\tau_i z_i.                                   \tag{19}
\]

The anchor and all plateau transitions are exact; each of the \(N\) signed input
transitions has residual magnitude \(1/N\).  Hence

\[
 \|Ax-b\|_2=\frac1{\sqrt N},
 \qquad
 \frac{\|Ax-b\|_2}{\|b\|_2}=\frac1{\sqrt{2N}}.           \tag{20}
\]

Every plateau pair has \(u_i=v_i=1/2\), so it contains no parity signal.

For an entirely wrong plateau, instead take

\[
 z_i=1-\frac{2i}{N}\quad(0\le i\le N),
 \qquad z_i=-1\quad(i>N).                                \tag{21}
\]

Now every input transition residual has magnitude \(2/N\), and

\[
 \|Ax-b\|_2=\frac2{\sqrt N},
 \qquad
 \frac{\|Ax-b\|_2}{\|b\|_2}=\sqrt{\frac2N}.              \tag{22}
\]

The whole plateau has difference \(-\tau_N\).  Both witnesses have the exact
optimal objective value because \(q_i=h_i=t_i=1\).  Equation (22) is the same
linear-drift/neighbor-mixture obstruction underlying the earlier exact-only
result.

Equations (1) and (20)--(22) leave only constant-factor gaps.  They prove that
the absolute and relative robustness scales are respectively
\(\Theta(N^{-1/2})\) and \(\Theta(N^{-1/2})\) when \(\|b\|=\sqrt2\).  The
constant-relative-residual theorem remains false, but calling the family
``exact-only'' is too strong after the reference-recurrence normalization: it has
a sharp vanishing-residual robustness window.

## Scope

The residual is the global Euclidean right-hand-side residual, not a row-normalized
RMS residual or scale-invariant backward error.  The output is an
original-primal amplitude state.  The theorem does not apply if a prefix table,
feasible-offset oracle, or batch oracle is supplied for free.  Its novelty, if
used, is the LP-native threshold statement quantifying over every nonnegative
point in the residual tube; the signed recurrence, Cauchy--Schwarz threshold, and
parity query lower bound are standard ingredients.
