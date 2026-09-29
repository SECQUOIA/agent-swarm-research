"""Door (line-graph) reformulation of order-1 motion planning through boxes.
GCS vertices: start, goal, and one door D_uv = X_u cap X_v per overlapping pair {u,v}.
Edges: between two vertices lying in a common region v (segment stays in X_v by
convexity), cost ||x' - x||_2, no edge constraints. Paths may re-enter a region
(physically valid), so OPT_door <= OPT_region."""
import numpy as np
from gcs import Inst
from mp import MP


def door_inst(m: MP):
    R = len(m.boxes)
    sets = {'s': ('point', m.start), 't': ('point', m.goal)}
    member = {'s': {i for i in range(R) if np.all(m.start >= m.boxes[i][0] - 1e-12) and np.all(m.start <= m.boxes[i][1] + 1e-12)},
              't': {i for i in range(R) if np.all(m.goal >= m.boxes[i][0] - 1e-12) and np.all(m.goal <= m.boxes[i][1] + 1e-12)}}
    for u in range(R):
        for v in range(u + 1, R):
            lo = np.maximum(m.boxes[u][0], m.boxes[v][0]); hi = np.minimum(m.boxes[u][1], m.boxes[v][1])
            if np.all(lo <= hi + 1e-12):
                name = f"D{u}_{v}"
                sets[name] = ('box', lo, hi)
                member[name] = {u, v}
    names = list(sets)
    E = []
    for a in names:
        for b in names:
            if a == b or a == 't' or b == 's':
                continue
            if member[a] & member[b]:
                E.append((a, b))
    return Inst(sets, E, 's', 't', m.d)
