# Convex-vector precision for arbitrary unconditional bodies

The complete theorem and proof were promoted after two independent full audits and a bounded primary-source assessment to [the unconditional-body result](../results/convex-vector-unconditional-compiled-precision.md).

For one-input componentwise convex graphs, the finite overhead is `ceil(log2(4m-1))`. For dense rational polynomial outputs and a rational strong separation oracle with known radii, a polynomial-time rational MILP construction has at most `p_conv+14+ceil(log2 m)` binaries. The final MILP uses a rational inscribed box and needs no nonlinear error-body constraints. No output-independent overhead or new allocation algorithm is claimed.
