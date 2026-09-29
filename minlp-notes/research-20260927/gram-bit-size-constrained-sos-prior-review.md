The two papers establish large coefficients for constrained SOS certificates. Their lower-bound targets are linear polynomials, not globally nonnegative quartics.

O'Donnell, *SOS Is Not Obviously Automatizable, Even Approximately*, ITCS 2017, Theorem 1, p. 59:6, proves a degree-2 lower bound even with explicit bounds on every variable. With

\[
K=\{x_i^2=x_i,\quad 2x_i y_i=y_i,\quad
y_i^2=y_{i+1}\ (i<n),\quad y_n^2=0\},
\qquad p_n=\sum_i x_i-2y_1,
\]

a degree-2 SOS certificate of \(p_n\ge0\) exists, but every degree-2 certificate of \(p_n\ge-0.01\), including the constraints \(x_i^2,y_i^2\le1\), requires exponential bit complexity. The theorem states \(\Theta(2^n)\), with \(2n\) variables. For the exact target, the proof forces the SOS Gram diagonal corresponding to \(y_n^2\) to be at least \(2^{2^n}\). Footnote 4, p. 59:4, explicitly covers rational PSD matrix representations. These are Gram matrices for an SOS term **modulo the constraints**, not Gram matrices representing \(p_n\) itself. [Published primary PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol067-itcs2017/LIPIcs.ITCS.2017.59/LIPIcs.ITCS.2017.59.pdf).

Raghavendra–Weitz, *On the Bit Complexity of Sum-of-Squares Proofs*, [arXiv:1702.05139](https://arxiv.org/pdf/1702.05139), Theorem 1.2, numbered p. 3, becomes Theorem 2, p. 80:3, in the [ICALP publication](https://drops.dagstuhl.de/storage/00lipics/lipics-vol080-icalp2017/LIPIcs.ICALP.2017.80/LIPIcs.ICALP.2017.80.pdf). It gives quadratic equations on \(N\) variables, including every Boolean equation, and a degree-2 certificate, while every certificate of degree \(d\le\sqrt N\) has a coefficient of magnitude

\[
\Omega\!\left(N^{-d}2^{\exp(\sqrt N)}\right).
\]

Section 5.1 (arXiv pp. 9–10; published p. 80:10) gives the stronger dimension dependence without Boolean constraints: for \(y_i^2=y_{i+1}, y_m^2=0\) and fixed \(0<\epsilon<1/2\), the target \(\epsilon-y_1\) has a degree-2 certificate, but the multiplier of \(y_m^2\) in every degree-\(d\) certificate has a coefficient of magnitude

\[
\Omega\!\left(m^{-d}(1/(2\epsilon))^{2^m}\right).
\]

There is no degree cutoff in that chain argument. Section 5.2 substitutes Boolean block sums for the \(y_i\), yielding the theorem above. The forced large coefficient is an equality multiplier; the theorem does not identify an unconstrained polynomial Gram matrix.

For comparison, several distinctions follow directly from these formulations. The lower bounds apply over real coefficients, so they also bound rational numerators through coefficient magnitude. Their feasible sets are compact; the Booleanized example has explicit Boolean axioms. The shifted targets are strictly positive on their feasible sets. Neither theorem asserts global positivity, strong SOS-convexity, or a positive definite Gram representation of an unconstrained target. Do not equate strict positivity on the constrained domain with strict feasibility of either SDP, or claim these papers require failure of strict feasibility: they do not make that assertion.

Verification: read the original PDFs and checked theorem numbering, constraint definitions, coefficient norms, and the proofs in the cited sections. No project-wide checks or CI inspection were performed; no executable code changed.

The transfer boundary can be stated precisely. In O'Donnell's degree-2 argument, equations (4)–(5) and coefficient matching give

\[
|M_i|\le A_iB_i,\qquad A_i=1,\qquad
M_1=-2,\qquad M_{i+1}=-B_i^2.
\]

Thus \(B_n^2\ge2^{2^n}\). This is the actual Gram diagonal \(Q_{y_n,y_n}\), not merely a multiplier bound. However, Raghavendra–Weitz explicitly state that this original instance has a small degree-4 certificate (arXiv p. 3; published p. 80:3). A degree-4 transfer cannot invoke its degree-2 obstruction.

For the Raghavendra–Weitz non-Boolean chain, put \(a_i=(2\epsilon)^{2^{i-1}}\). Their functional is evaluation at \(a\). Applied to the certificate, it gives

\[
-\epsilon=\sum_j h_j(a)^2+
\lambda_m(a)(2\epsilon)^{2^m}.
\]

Consequently, the last multiplier must be large regardless of the SOS Gram. If an ordinary-polynomial transfer fixes all equality multipliers to small polynomials, this inequality rules out SOS feasibility of the transferred polynomial; it does not allow a large Gram matrix to compensate. The Boolean proof uses a pseudoexpectation with the same separation of roles. This is a limitation of the proposed transfer route, not a theorem about unconstrained quartic Gram size.
