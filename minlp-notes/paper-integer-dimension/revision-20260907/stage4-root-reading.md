# Stage 4 root reading

Root read the entire vector file and the current abstract, introduction and
conclusion in preparation for this stage. The reading included every proof in
the common overlay, curvature basis, positive-polar oracle, separable vector,
scalarization obstruction, cap-set, exact product count, nonconvex polynomial,
compiled signed-vector, tilted-body and conditioning arguments.

Specific checks included deterministic monotonicity of mass bisection despite
nonmonotone approximate evaluations; the common-denominator requirement of the
sorted random-access overlay; exact central repair and fixed denominator bounds
in repeated spanner exchanges; the distinction between a weak polar separator
and exact membership; rounding in effective coordinates so errors stay in the
nonlinear image; and sharing one output basis over all separated inputs.

For the separation examples root checked all integer sections of the three-box
convex hull, rather than only pairwise initial label segments; the residue and
cap-set averaging arguments; the preservation of a connected polynomial graph
by Bernstein approximation; and the conditioning lower bound for tilted bodies.
The single-input convex-vector box question is a stated boundary, not a premise
of a claimed theorem. A shorter discussion of unsuccessful routes may improve
presentation, and the author was asked to assess it.

No concrete proof gap was found in this reading. Root will separately assess
the author's patch, source audit and all five reports before accepting the stage.

Root inspected the original Awerbuch--Kleinberg Section 2.3, Propositions 2.2
and 2.4, including the maximum-determinant and exchange proofs. They support
credit for barycentric spanners themselves. Root also read Section 3.3 of the
published Plevrakis--Hazan NeurIPS2020 paper: it explicitly discusses approximate
linear optimization within spanner construction. The former preprint locator
must therefore be updated if citing the published version. These passages do
not supply our exact rational repair and fixed-denominator interface, which the
manuscript proves directly. The originals and retrieval hashes are recorded in
stage4-retrievals.json.
