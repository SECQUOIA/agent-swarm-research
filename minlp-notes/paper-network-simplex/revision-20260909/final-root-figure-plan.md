# Root check of the adopted completion illustration

For the existing directed K4 example, all six arcs run from the smaller vertex
to the larger vertex. With one locally observed label j on arcs 13 and 14,
the unobserved edges are {12,23,24,34}. They are connected on four vertices,
so their undirected cycle rank is 4-4+1=1. Edges {12,23,34} form a spanning
tree; edge24 is the unique nonforest edge. Observing its product removes it
from the unobserved graph, leaves that spanning tree, and makes the residual
cycle rank 3-4+1=0. This yields exactly the observation pattern already treated
algebraically in ex:forest-k4, without changing the model or the theorem.

The illustration must depict undirected cycle rank despite directed arrows.
In particular, the triangle2,3,4 is an undirected cycle although the network
is acyclic. Draw distinct line styles for observed edges, unobserved forest,
and selected completion, so the figure does not depend on color. Describe the
formulation count for the block/label pair; do not assert a slice-dimension or
unrestricted extension-complexity lower bound. The existing caveats remain.

After correction, the root will inspect the actual rendered figure and source
and verify that all edges and labels match this description.
