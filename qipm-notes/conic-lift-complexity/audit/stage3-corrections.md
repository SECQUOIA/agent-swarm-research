# Stage 3 correction report

The separate correction author read the root assessment and all five independent
review reports, then implemented all eleven accepted minor corrections. No
previously reviewed theorem was broadly rewritten, and no unresolved
classification problem was promoted to a theorem.

1. **Recession endpoint:** Section 6 now specifies that the compressed Slater
   endpoint is positive definite in each positive-rank complementary algebra.
   The compressed boundary endpoint may remain singular.
2. **Caps in the collapse statement:** The proposition now restates the fixed
   field, order cap R, and B=a(R-1). Its Lorentz extension explicitly states
   dimension cap d, B=d-2, optional rays, and the inherited hypotheses.
3. **Classification status:** The range is described as not resolved by the
   preceding results, without an exhaustive claim about outside literature.
4. **Packing Hessian:** The quadratic form is now written
   `D^2F[(H,K),(H,K)]`.
5. **North-pole positivity:** The necessary and sufficient rotated-certificate
   conditions explicitly include A_G>=0. The existing simplex conclusion and
   all exact parameters remain unchanged.
6. **Density matrices:** The trace-one PSD set contains normalized primitive
   rays and rank-two mixtures; it is not described as a projective line made
   of rank-two matrices.
7. **Companion attribution:** Section 7 explicitly identifies the shared
   standard norm-tree, grouped, and packed calculations in *The Cost of
   Following the Central Path*. Its bibliography entry has no invented author,
   identifies an unpublished anonymous companion manuscript, and uses n.d.
   because its local title page has no date. Self-contained reuse and the
   distinct arbitrary-barrier/formulation questions are explained.
8. **Escaping disk:** Example escaping-disk includes the three PSD blocks,
   exact closed-disk projection, a concrete Slater point (x=0,u=1,z=3), and
   the inequalities forcing every boundary completion to escape at (1,0).
9. **Local PSD3 pencil:** Example local-real-three-pencil is next to the global
   PSD3 exclusion. It gives the determinant, rank-two punctured-sphere Schur
   calculation, stereographic kernel chart, and rank-one north pole. The
   example invalidates only a local-to-global shortcut. The global exclusion
   by finite affine gluing remains explicit. The source audit rejects the
   obsolete source claim that this global exception remains open.
10. **Mandatory Stage 4A route:** The source map, author audit, and root Stage 4
    preparation now distinguish the single-ball fixed-field observation from
    the heterogeneous all-symmetric dimension-cap constant-nullity theorem.
    Both that product theorem and the every-boundary-tuple accessibility
    corollary are required Stage 4A coverage. Compactness of the full lifted
    extreme stratum and quantification over every tuple are retained. Nothing
    in this route is claimed already proved by Stage 3.
11. **Conic facet attribution:** The homogeneous independent-facet extra-unit
    principle is attributed to Hildebrand, Theorem 6.1. The tree-specific
    section and direct proof remain, with logarithmic homogeneity explicit.

## Independent checks

For the escaping example, the first 2-by-2 block has determinant 1-||x||^2
and nonnegative diagonals exactly on the disk. With delta>0, the Schur
conditions for the second and third blocks are u>=x2^2/delta and
z>=1+u^2/delta. At delta=0 the disk forces x2=0; positivity of the third
block forces u=0 and permits z>=1. At the chosen Slater point the three
blocks are I2, I2, and [[1,1],[1,2]], all positive definite. On the circle,
x2^2/delta=2-delta, and z>=4/delta-3+delta diverges. This proves escape for
every completion, without assuming a selected sheet.

For the local PSD3 pencil, direct determinant expansion gives
(1-x3)(1-x1^2-x2^2-x3^2). Multiplication by the cleared kernel vector
(1-x3,-x1,-x2) gives (1-||x||^2,0,0). The lower block is (1-x3)I2,
so Schur complementation proves PSD rank two on the punctured sphere;
the explicit north-pole diagonal matrix has rank one. The projective chart
is precisely the stereographic chart. These facts do not construct a global
constant-rank slack factorization.

Exact rational checks using the qipm Python interpreter and only the standard
library verified the determinant and cleared-kernel polynomial identities on
four distinct values of each variable. Each polynomial has coordinate degree
at most three, so this grid check certifies the identities by interpolation.
The Slater principal minors and escape-rate identity were also checked.

The correction author opened Hildebrand's primary preprint and inspected
Section 6 / Theorem 6.1:
https://optimization-online.org/wp-content/uploads/2011/06/3068.pdf.
The journal bibliography uses *Mathematical Programming* 142 (2013), 311–329,
DOI 10.1007/s10107-012-0576-1. The preprint has a different title; the manuscript
cites the journal title and does not confuse its publication year with the
preprint date.

## Build and scope

A clean build using `conda run -n qipm --live-stream make clean` followed by
`conda run -n qipm --live-stream make` succeeded. The integrated PDF has
37 pages. The final LaTeX and BibTeX logs contain no warnings, undefined
references or citations, or overfull/underfull boxes. The multipass build
transcript includes the normal first-pass unresolved references before BibTeX
and reruns; those are absent in the final logs.

- Build transcript: `audit/stage3-corrections-build.log`.
- Preserved final LaTeX log: `audit/stage3-corrections-final-latex.log`.

Only `conic-lift-complexity/` was changed. The companion manuscript, workbench,
and literature catalog were read but not modified. Root verification remains
the final step before closing Stage 3 and starting Stage 4A.
