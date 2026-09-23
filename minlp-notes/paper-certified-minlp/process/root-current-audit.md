# Coordinator audit for the resumed manuscript

The current authoring request requires sequential author/five-reviewer stages.
The earlier `root-initial-audit.md` describes the pre-repair implementation and
must not be used as the current acceptance verdict.

Before this writing process, the coordinator reran the complete certification
suite (152 passing tests), replayed the included quadratic certificate (11 cuts,
39 derivations, exact bound 1/4), independently counted the 289 historical replay
records (188 verified, 92 rejected, 9 missing), and checked the 13 evidence hashes
and 10 certification-source hashes recorded by the final repair audit. All
checked hashes matched. This was not another replay of all large proofs.

The coordinator read the exact-expression reconstruction, safe-cut evaluator,
complete checker interface, and discrete parser alongside the soundness and
review notes. The current complete interface defaults to internal exact replay;
partial mode cannot expose a verified bound. Numerical proposals are made on a
separate loaded model. Domain validation precedes symbolic differentiation and
cancellation. These findings agree with the repaired contract, subject to the
explicit trusted libraries and runtime. They are not a formal software proof.

Stage 2 must supply standalone proofs for interval correction, half-lines/free
coordinates, propagation, extension to the master, and incumbent-conditioned
discrete inference. It must distinguish the general support-vector theorem from
the implemented finite symbolic-gradient route, and distinguish domain checks
over declared bounds from propagation over the affine rows. Zero-coefficient
affine tautologies are omitted by serialization; contradictory constant rows
are rejected before serialization. No exact infeasibility pipeline should be
claimed merely because the discrete kernel supports infeasibility proofs.

Stage 4 has available IPOPT at
`/home/sgusev/miniconda3/envs/solvers/bin/ipopt` and the exact SCIP/VIPR tools at
`/home/sgusev/.local/opt/scip-exact/bin`. Generator attempts have separate search
and completion budgets; a solver time limit is not a total pipeline deadline.
The filesystem had approximately 158 GB available at inspection. Preserve the
historical artifacts and avoid unnecessary uncompressed copies of large proofs.

MINLPLib's official home/download pages, inspected during this process, identify
GAMS scalar as the primary format and display CC-BY 4.0 attribution. The final
supplement should provide exact input models with appropriate provenance and
license information, or a checked acquisition mechanism, without redistributing
the local literature PDFs. Authoring and local packaging are authorized;
uploading or contacting others has not been requested.
