# Stage 3 development to verify

The sparse LP source's factor-state upper bound is stated only up to logarithms
and invokes generic rectangular QLSA. For this explicit one-parameter family,
both state upper bounds can instead be elementary and exactly order-matching
at fixed trace error. Known singular bases isolate a canonical rotation with
parameter t (normal access) or sqrt(t) (factor access). Constant-success phase
or amplitude estimation to additive O(delta), respectively O(sqrt(delta)),
costs O(1/delta), respectively O(1/sqrt(delta)). The estimated parameter then
specifies the two-dimensional normalized Newton state by a free rotation.
The success probability can be a sufficiently high fixed constant, depending
on the prescribed fixed error, so no logarithm in delta is necessary. Define
the output/error model and the canonical factor oracle precisely and prove
these statements before sharpening the source's factor bound to Theta.

This is a state-output algorithm; measurement is permitted here, unlike the
reusable coherent compiler. A coherent implementation followed by discarding
the estimate is also possible. The error in the averaged density operator
must account for unsuccessful estimation, not merely conditional success.

An especially simple implementation uses the standard amplitude-estimation
bound |a_hat-a| <= 2*pi*sqrt(a*(1-a))/M + pi^2/M^2 with probability at least
8/pi^2 (Brassard et al. 2002, Theorem 12). Preparing u_- and querying H gives
success probability a=t^2; M=C/delta estimates t to O(delta/C). Preparing
q_- and querying A gives a=t; M=C/sqrt(delta) estimates t to O(delta/C).
Clamp the estimate to [delta,rho*delta]. Repeating a fixed number of times
and taking a median makes the failure probability as small as the fixed
trace error needs. Local full text is in
literature/papers/brassard2002-quantum-amplitude-amplification-and-estimation/.

For the lower bounds, count both the matrix/factor and right-side preparation
oracles, allow their controlled inverses, and use a fixed target error smaller
than one quarter of the endpoint trace separation. Parameter rho is fixed.
No free t-dependent digital LP data is present. Explicitly show the right-side
preparation rotation varies by O(delta) between endpoints, so it cannot bypass
the matrix lower bound. Known basis changes are independent of t, although
they may depend on the public delta.

The compiler transfer does not necessarily permit the right-side preparation
oracle as an extra input: its canonical matrix-only scalar polynomial proof
is immediate; adding a nontrigonometric right-side oracle would need a new
argument. State the compiler and state tasks separately and transparently.

Check that 1-s^2 is a real even bounded QSVT polynomial implementing I-AA*,
with the output on the row space (two-dimensional here). Its degree is two.
The normal family has high eigenvalue exactly 1, so its coarse tier is the
singleton-high-band constant tier, not the positive-width logarithmic tier.

Correction found by Stage 3 author: its eigenspaces are also public and fixed,
so the specialized LP-family coarse tier actually uses ZERO queries. Encode
(1-m_rho*delta) P_- directly when K>=G0. The general c=1 worst-case theorem
has unknown eigenspaces/support and retains Theta(1). Transfer all positive
index tiers and high-accuracy laws, but state this coarse exception explicitly.
