# Review of the positive-penalty growth obstruction

Date: 2026-10-02. Verdict: pass. This independent review read the complete
[four-variable construction](../new-direction/negative-curvature-penalty-barrier.md).
It found no substantive gap. No executable check was rerun.

The three residual equations with binary controls reduce exactly to
`B z_1+(B-1)z_2=B`, whose unique binary solution is `(1,0)` for
`B>=3`. Nonnegativity of every objective term therefore establishes
the stated unique optimizer on the full continuous box.

The fractional witness has all three residuals zero. Its objective is
`c(B-1)/B^2`, and its squared distance from the optimizer is
`1+(5/4)(1-1/B)^2`. This gives the claimed growth upper bound,
independently of the positive penalty weight. The local residual
identities and endpoint-penalty bound prove local quadratic growth;
compactness away from the unique zero extends this to some positive
global constant on each fixed instance.

The direction `((B-1)/2,0,B-1,-B)` belongs to the common residual
kernel. Its negative Rayleigh quotient is therefore unaffected by
the positive penalty. Its squared norm is at most `5/4` times the
squared norm of its two control components, yielding
`nu>=(8/5)c`; PSD addition gives `nu<=2c`. The witness displacement
is exactly minus this direction divided by `B`. Combining the two
inequalities proves the displayed lower bound on `nu/g`.

The graph and stated path bags are correct. The matrix encodings have
polynomial length, while the parameter lower bound grows with the
numerical value of `B`. The conclusion is properly restricted: this
is an obstruction to repairing that reduction by increasing its PSD
penalty, not optimization hardness, and not a negative answer to the
sparse negative-curvature target.

The note records 882 author-run rational checks. This review verifies
the algebra directly and does not claim to have rerun those checks.
No literature search, project-wide check, or CI inspection was used.
