"""Translate a MINLPLib.jl instance file (2017 format, JuMP 0.18 syntax) into
a GAMS scalar model, so that it can be canonicalized with GAMS Convert and
compared with the current MINLPLib files.

Handled statements (all that occur in the 2017 files used here):
  @variable(m, objvar)                    free variable
  X_Idx = Any[...]; @variable(m, X[X_Idx])  variables X<k> (X in x, b, i)
  setlowerbound(X[k], v), setupperbound(X[k], v)
  setcategory(X[k], :Bin | :Int)
  @constraint(m, name, lhs REL rhs), @NLconstraint(m, name, lhs REL rhs)
      REL in ==, <=, >=
  @objective(m, Min|Max, expr)
Expressions are parsed with Python's ast (after ^ -> **) and printed in GAMS
syntax; integer powers become power(a, n), other powers a**b. Continuous
variables without bounds are free. Integer variables follow the convention of
the MINLPLib.jl converter: a missing lower bound means the GAMS default 0, and
an upper bound of 1e20 means +inf (literal JuMP semantics would make them
free; the files print every bound that differs from the GAMS default, e.g.
spring i4 has lower bound 1 and upper bound 100).

Initial levels are set to 1 clipped to the bounds (the 2017 files carry no
starting point, and GAMS stops on 1/0 when evaluating the model at 0).

Usage: python3 jl2gms.py in.jl out.gms
"""
import ast
import re
import sys

sys.setrecursionlimit(100000)

REL = {"==": "=E=", "<=": "=L=", ">=": "=G="}


def gexpr(node):
    if isinstance(node, ast.Expression):
        return gexpr(node.body)
    if isinstance(node, ast.Constant):
        return repr(float(node.value)) if isinstance(node.value, float) else str(node.value)
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Subscript):
        idx = node.slice
        if isinstance(idx, ast.Index):  # python < 3.9
            idx = idx.value
        return f"{node.value.id}{idx.value}"
    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.USub):
            return f"(-({gexpr(node.operand)}))"
        if isinstance(node.op, ast.UAdd):
            return f"({gexpr(node.operand)})"
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
        # flatten left-associative chains iteratively (long sums would nest deeply)
        add = isinstance(node.op, (ast.Add, ast.Sub))
        kinds = (ast.Add, ast.Sub) if add else (ast.Mult, ast.Div)
        rest = []
        while isinstance(node, ast.BinOp) and isinstance(node.op, kinds):
            sym = {ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/"}[type(node.op)]
            rest.append((sym, node.right))
            node = node.left
        parts = [f"({gexpr(node)})"] + [f" {sym} ({gexpr(r)})" for sym, r in reversed(rest)]
        return "(" + "".join(parts) + ")"
    if isinstance(node, ast.BinOp):
        a, b = gexpr(node.left), gexpr(node.right)
        if isinstance(node.op, ast.Pow):
            r = node.right
            neg = False
            if isinstance(r, ast.UnaryOp) and isinstance(r.op, ast.USub) and isinstance(r.operand, ast.Constant):
                neg, r = True, r.operand
            if isinstance(r, ast.Constant) and float(r.value) == int(float(r.value)):
                k = int(float(r.value)) * (-1 if neg else 1)
                return f"power({a}, {k})"
            return f"({a} ** {b})"
    if isinstance(node, ast.Call):
        fn = node.func.id
        args = ", ".join(gexpr(x) for x in node.args)
        return f"{fn}({args})"
    raise NotImplementedError(ast.dump(node))


def wrap(line, width=200):
    """break a long GAMS statement at spaces or commas (statements may span lines)"""
    out, cur = [], ""
    for tok in re.split(r"(?<=[ ,])", line):
        if len(cur) + len(tok) > width and cur:
            out.append(cur)
            cur = ""
        cur += tok
    out.append(cur)
    return "\n  ".join(out)  # indent: a '*' in column 1 would start a GAMS comment


def split_rel(body):
    """split 'lhs REL rhs' at the last top-level relational operator"""
    depth, pos = 0, None
    i = 0
    while i < len(body):
        c = body[i]
        if c in "([":
            depth += 1
        elif c in ")]":
            depth -= 1
        elif depth == 0 and body[i:i + 2] in REL:
            pos = i
            i += 1
        i += 1
    assert pos is not None, body[:200]
    return body[:pos], body[pos:pos + 2], body[pos + 2:]


def py(s):
    # The 2017 MINLPLib.jl files write GAMS sqr(a)**b as "(a)^2^b". Julia's ^ is
    # right-associative, so read literally this is a^(2^b); the GAMS model means
    # (a^2)^b. Only lukvle10 contains this pattern; restore the GAMS meaning.
    s = re.sub(r"\((\w+\[\d+\])\)\^2\^", r"((\1)^2)^", s)
    return ast.parse(s.replace("^", "**").strip(), mode="eval")


def translate(src):
    groups = {}
    order = []
    free = []
    lb, ub, cat = {}, {}, {}
    cons = []
    obj = None
    for line in src.split("\n"):
        s = line.strip()
        m = re.match(r"(\w+)_Idx = Any\[(.*)\]$", s)
        if m:
            groups[m.group(1)] = [int(k) for k in m.group(2).split(",") if k.strip()]
            continue
        m = re.match(r"@variable\(m, (\w+)\)$", s)
        if m:
            free.append(m.group(1))
            continue
        m = re.match(r"@variable\(m, (\w+)\[(\w+)_Idx\]\)$", s)
        if m:
            order += [f"{m.group(1)}{k}" for k in groups[m.group(2)]]
            continue
        m = re.match(r"set(lower|upper)bound\((\w+)\[(\d+)\], (.*)\)$", s)
        if m:
            (lb if m.group(1) == "lower" else ub)[f"{m.group(2)}{m.group(3)}"] = float(m.group(4))
            continue
        m = re.match(r"setcategory\((\w+)\[(\d+)\], :(\w+)\)$", s)
        if m:
            cat[f"{m.group(1)}{m.group(2)}"] = m.group(3)
            continue
        m = re.match(r"@(NL)?constraint\(m, (\w+), (.*)\)$", s)
        if m:
            lhs, rel, rhs = split_rel(m.group(3))
            cons.append((m.group(2), gexpr(py(lhs)), REL[rel], gexpr(py(rhs))))
            continue
        m = re.match(r"@(NL)?objective\(m, (Min|Max), (.*)\)$", s)
        if m:
            obj = (m.group(2), m.group(3).strip())
            continue
        if s and not s.startswith(("#", "using", "m = ", "m=")):
            raise ValueError("unhandled line: " + s[:120])

    def key(v):
        mm = re.match(r"([a-z]+)(\d+)$", v)
        return (int(mm.group(2)) if mm else 10 ** 9, v)

    allv = sorted(order, key=key) + free
    out = []
    out.append("Variables " + ",".join(allv) + ";")
    bins = [v for v in allv if cat.get(v) == "Bin"]
    ints = [v for v in allv if cat.get(v) == "Int"]
    if bins:
        out.append("Binary Variables " + ",".join(bins) + ";")
    if ints:
        out.append("Integer Variables " + ",".join(ints) + ";")
    out.append("Equations " + ",".join(c[0] for c in cons) + (",objdef" if obj and obj[1] != "objvar" else "") + ";")
    for name, l, r, rhs in cons:
        out.append(f"{name}.. {l} {r} {rhs};")
    objvar = "objvar"
    if obj and obj[1] != "objvar":
        out.append(f"objdef.. objvar =E= {gexpr(py(obj[1]))};")
        if "objvar" not in allv:
            out[0] = out[0][:-1] + ",objvar;"
    for v in allv:
        c = cat.get(v)
        lo = lb.get(v, None)
        hi = ub.get(v, None)
        if c == "Bin":  # [0,1] by default in both JuMP and GAMS; explicit bounds override
            if lo is not None:
                out.append(f"{v}.lo = {repr(lo)};")
            if hi is not None:
                out.append(f"{v}.up = {repr(hi)};")
            continue
        if c == "Int":
            # MINLPLib.jl convention (2017 files): bounds equal to the GAMS defaults
            # of an integer variable (lower 0) are omitted, and +inf is written as
            # 1e20. Literal JuMP semantics would make such variables free.
            out.append(f"{v}.lo = {repr(lo) if lo is not None else '0'};")
            out.append(f"{v}.up = {repr(hi) if hi is not None and hi < 1e20 else 'inf'};")
            continue
        if lo is not None:
            out.append(f"{v}.lo = {repr(lo)};")
        if hi is not None:
            out.append(f"{v}.up = {repr(hi)};")
    # initial levels: 1 clipped to the bounds (the 2017 files carry no starting
    # point; GAMS evaluates the model at the levels and stops on 1/0 at 0)
    for v in allv:
        lo, hi = lb.get(v), ub.get(v)
        if cat.get(v) == "Bin":
            lo, hi = (0.0 if lo is None else lo), (1.0 if hi is None else hi)
        lev = 1.0
        if lo is not None:
            lev = max(lev, lo)
        if hi is not None:
            lev = min(lev, hi)
        out.append(f"{v}.l = {repr(lev)};")
    disc = bool(bins or ints)
    out.append("Model m / all /;")
    out.append("m.limrow=0; m.limcol=0;")
    sense = "minimizing" if obj is None or obj[0] == "Min" else "maximizing"
    out.append(f"Solve m using {'MINLP' if disc else 'NLP'} {sense} {objvar};")
    return "\n".join(wrap(l) for l in out) + "\n", dict(nvars=len(allv), ncons=len(cons), bins=len(bins), ints=len(ints),
                                       bounded_bins=[v for v in bins if v in lb or v in ub])


if __name__ == "__main__":
    txt, info = translate(open(sys.argv[1]).read())
    open(sys.argv[2], "w").write(txt)
    print(info)
