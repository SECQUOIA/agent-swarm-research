# Closing source checks for two supporting results

Date: 2026-09-05. This bounded primary-source check closes pending-search
wording; it is not an exhaustive priority determination.

## Facial pooling specifications

The [facial characterization](../results/pooling-facial-quality-integrality.md)
has a completed mathematical audit. The necessary-and-sufficient statement
concerns universal existence of an integral optimum over all network
topologies and linear objectives for a fixed input-quality cloud and
allowed output regions. It does not assume discrete flows in the model.

Fresh searches combined “pooling problem”, “integrality”, “quality”,
“face”, and “specifications”. They did not locate this precise statement.
A relevant distinction is Boland, Kalinowski, and Rigterink's
[2015 discrete-flow pooling paper](https://optimization-online.org/2015/07/5041/).
Its author abstract explicitly models flows in prescribed discrete units
for coal transport and compares continuous and discretized formulations.
This is different from proving that a continuous pooling model always has
an integral optimum under facial quality restrictions. Only the author
abstract and model summary were inspected in this closing check; no
full-paper exclusion of an implicit special case is claimed.

The geometric face property and integral network-flow machinery are
classical and already credited in the result. The retained assessment is
an elementary useful characterization with qualified priority, potentially
implicit in compatibility models. No broader novelty clearance is pending
as an active task, and no absence-of-literature theorem is asserted.

## Relative-gap spatial branch-and-bound

The [relative-gap construction](../results/spatial-bb-relative-gap-exponential-lower-bound.md)
has a completed proof audit. Fresh searches combined spatial branching,
direct products, sum-of-squares, relative gaps, and exponential lower
bounds. They did not expose the precise continuous-box/direct-product
statement. This does not establish priority.

[Jarre's 2018 primary manuscript](https://optimization-online.org/wp-content/uploads/2018/07/6729.pdf)
was checked again, particularly its branching definition and Section 3.
It proves exponential branching effort despite a specified semidefinite
relaxation; nodes fix binary coordinates. The general phenomenon is
therefore established. Our stated difference is the particular spatial-box
and global fixed-order SOS certificate model and its relative-gap count.
The known root cuts and decomposition methods that defeat the repository
examples remain essential limitations.

The newer [Hübner–Gupte–Rebennack article](https://pubsonline.informs.org/doi/10.1287/ijoc.2024.0755)
studies spatial branching for separable piecewise-linear functions. Its
abstract and background sections describe convex underestimators and
convergence conditions, rather than the matching certificate lower bound.
That limited inspection is an additional scope check, not a full exclusion
of every result in the article. The broader
[existing source comparison](spatial-bb-strengthening-novelty.md) remains
the main record. We retain this result as a reviewed, model-specific
supporting lower bound with qualified novelty.
