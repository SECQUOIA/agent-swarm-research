"""Convert poolinginstances random_haverly JSON (Luedtke et al. 2020 test set) to the literature JSON format."""
import json, sys
def convert(src, dst):
    d = json.load(open(src)); g = d["graph"]; nodes = g["nodes"]
    comps, prods, pools = [], [], {}
    for n in nodes:
        if n["type"] == "input":
            comps.append(dict(name=n["id"], lower=0, upper=n["C"], price=0.0, quality=n["lambda"]))
        elif n["type"] == "output":
            prods.append(dict(name=n["id"], lower=0, upper=n["C"], price=0.0, quality_lower=None, quality_upper=n["overbeta"]))
        else:
            pools[n["id"]] = n["C"]
    il, lj, ij = [], [], []
    for e in g["links"]:
        s, t = nodes[e["source"]], nodes[e["target"]]
        if t["type"] == "pool":
            il.append(dict(component=s["id"], pool=t["id"], fraction=1.0, cost=e["cost"]))
        elif s["type"] == "pool":
            lj.append(dict(pool=s["id"], product=t["id"], bound=t["C"], cost=e["cost"]))
        else:
            ij.append(dict(component=s["id"], product=t["id"], bound=t["C"], cost=e["cost"]))
    out = dict(name=src.split("/")[-1][:-5], objective=None, components=comps, products=prods, pool_size=pools,
               component_to_pool_fraction=il, pool_to_product_bound=lj, component_to_product_bound=ij)
    json.dump(out, open(dst, "w"))
if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
