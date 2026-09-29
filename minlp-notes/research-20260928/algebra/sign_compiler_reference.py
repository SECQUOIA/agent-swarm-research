"""Reference DAG construction for adaptive integer sign-circuit compilation.

Only 0, 1, Boolean inputs, binary +, -, *, and unary strict H are source
operations. The result contains no H or division gates. This is a construction
check, not an efficient implementation of PosSLP. Its default precision is the
schedule proved in adaptive-integer-sign-circuit-compilation.md; experimental
schedules have no general correctness guarantee.
"""

from dataclasses import dataclass
from typing import Mapping


class EvaluationLimit(ValueError):
    """An explicit integer evaluation exceeded its configured bit budget."""


@dataclass(frozen=True)
class Node:
    op: str
    args: tuple[int, ...] = ()
    label: str | None = None


class IntegerDAG:
    """Hash-consed nodes with backward references and bounded gate fan-in."""

    ARITY = {"zero": 0, "one": 0, "input": 0,
             "+": 2, "-": 2, "*": 2, "H": 1}

    def __init__(self) -> None:
        self.nodes: list[Node] = []
        self._intern: dict[Node, int] = {}
        self.zero = self.node("zero")
        self.one = self.node("one")

    def node(self, op: str, *args: int, label: str | None = None) -> int:
        if op not in self.ARITY or len(args) != self.ARITY[op]:
            raise ValueError("Unknown operation or wrong arity")
        if any(type(arg) is not int or not 0 <= arg < len(self.nodes)
               for arg in args):
            raise ValueError("Operands must refer to preceding nodes")
        if (op == "input") != (isinstance(label, str) and bool(label)):
            raise ValueError("Only input nodes have nonempty labels")
        node = Node(op, tuple(args), label)
        if node not in self._intern:
            self._intern[node] = len(self.nodes)
            self.nodes.append(node)
        return self._intern[node]

    def input(self, label: str) -> int:
        return self.node("input", label=label)

    @property
    def gate_count(self) -> int:
        # Count all arithmetic and threshold gates, including decoder/selector
        # logic. Constants and input leaves do not contribute to S.
        return sum(node.op in ("+", "-", "*", "H") for node in self.nodes)

    def evaluate(self, inputs: Mapping[str, int], *,
                 max_bits: int = 500_000) -> list[int]:
        """Evaluate exactly with a guard before potentially huge products.

        Returns every node value so checks can inspect all denominators. The
        bit limit concerns each integer, not a theorem about evaluation cost.
        """
        if max_bits < 1:
            raise ValueError("max_bits must be positive")
        values: list[int] = []
        for node in self.nodes:
            if node.op == "zero":
                value = 0
            elif node.op == "one":
                value = 1
            elif node.op == "input":
                value = inputs[node.label]
                if value not in (0, 1) or not isinstance(value, int):
                    raise ValueError("Source inputs must be Boolean integers")
            elif node.op == "H":
                value = int(values[node.args[0]] > 0)
            else:
                left, right = (values[arg] for arg in node.args)
                if node.op == "+":
                    value = left + right
                elif node.op == "-":
                    value = left - right
                else:
                    if (left and right and
                            left.bit_length() + right.bit_length() > max_bits + 1):
                        raise EvaluationLimit("Product exceeds integer bit budget")
                    value = left * right
            if value.bit_length() > max_bits:
                raise EvaluationLimit("Node exceeds integer bit budget")
            values.append(value)
        return values


@dataclass(frozen=True)
class RationalNode:
    numerator: int
    denominator: int


class RationalBuilder:
    """Integer DAG formulas representing rationals with positive denominators."""

    def __init__(self, dag: IntegerDAG) -> None:
        self.dag = dag
        self.two = dag.node("+", dag.one, dag.one)
        self.four = dag.node("*", self.two, self.two)

    def integer(self, node: int) -> RationalNode:
        return RationalNode(node, self.dag.one)

    def arithmetic(self, op: str, left: RationalNode,
                   right: RationalNode) -> RationalNode:
        d = self.dag
        p, q = left.numerator, left.denominator
        r, s = right.numerator, right.denominator
        denominator = d.node("*", q, s)
        if op == "*":
            numerator = d.node("*", p, r)
        elif op in ("+", "-"):
            numerator = d.node(op, d.node("*", p, s), d.node("*", r, q))
        else:
            raise ValueError("Expected a binary arithmetic operation")
        return RationalNode(numerator, denominator)

    def shift(self, value: RationalNode) -> RationalNode:
        d = self.dag
        p, q = value.numerator, value.denominator
        return RationalNode(d.node("-", d.node("*", self.four, p),
                                   d.node("*", self.two, q)), q)

    def compress(self, value: RationalNode, scale: int) -> RationalNode:
        # scale is a node for a positive integer M.
        d = self.dag
        p, q = value.numerator, value.denominator
        numerator = d.node("*", self.two,
                           d.node("*", scale, d.node("*", p, q)))
        denominator = d.node("+", d.node("*", scale, d.node("*", q, q)),
                             d.node("*", p, p))
        return RationalNode(numerator, denominator)

    def refine(self, value: RationalNode) -> RationalNode:
        d = self.dag
        p, q = value.numerator, value.denominator
        numerator = d.node("*", self.two, d.node("*", p, q))
        denominator = d.node("+", d.node("*", q, q), d.node("*", p, p))
        return RationalNode(numerator, denominator)

    def to_boolean(self, value: RationalNode) -> RationalNode:
        d = self.dag
        p, q = value.numerator, value.denominator
        return RationalNode(d.node("+", q, p), d.node("*", self.two, q))


@dataclass(frozen=True)
class PrecisionSchedule:
    compressor_index: int
    refinement_steps: int

    def __post_init__(self) -> None:
        if self.compressor_index < 1 or self.refinement_steps < 1:
            raise ValueError("Both schedule parameters must be positive")

    @classmethod
    def theorem(cls, source_size: int) -> "PrecisionSchedule":
        size = max(1, source_size)
        return cls(size + 2, 2 * size + 5)


@dataclass
class CompiledCircuit:
    dag: IntegerDAG
    output: int
    pairs: tuple[RationalNode, ...]
    schedule: PrecisionSchedule
    source_size: int
    threshold_count: int
    compressor_calls: int
    refinement_calls: int

    @property
    def uses_theorem_schedule(self) -> bool:
        return self.schedule == PrecisionSchedule.theorem(self.source_size)

    def construction_gate_bound(self) -> int:
        """Upper bound for these templates; sharing may reduce actual size."""
        j, r = self.schedule.compressor_index, self.schedule.refinement_steps
        arithmetic_count = self.source_size - self.threshold_count
        return j + 1 + 4 * arithmetic_count + self.threshold_count * (7*j + 5*r + 5) + 2


def compile_sign_circuit(source: IntegerDAG, output: int, *,
                         schedule: PrecisionSchedule | None = None) -> CompiledCircuit:
    """Construct a division-free DAG; output must be Boolean on Boolean inputs.

    The caller owns the Boolean-output promise. Explicitly supplying a reduced
    schedule is useful for experiments but does not preserve the theorem.
    """
    if type(output) is not int or not 0 <= output < len(source.nodes):
        raise ValueError("Invalid source output")
    size = source.gate_count
    schedule = schedule or PrecisionSchedule.theorem(size)
    dag = IntegerDAG()
    builder = RationalBuilder(dag)
    scales = [builder.two]
    for _ in range(schedule.compressor_index):
        scales.append(dag.node("*", scales[-1], scales[-1]))
    pairs: list[RationalNode] = []
    h_count = compressor_calls = refinement_calls = 0
    for node in source.nodes:
        if node.op in ("zero", "one", "input"):
            pairs.append(builder.integer(dag.node(node.op, label=node.label)))
        elif node.op in ("+", "-", "*"):
            pairs.append(builder.arithmetic(node.op, *(pairs[arg] for arg in node.args)))
        else:
            h_count += 1
            value = builder.shift(pairs[node.args[0]])
            for scale in reversed(scales[1:]):
                value = builder.compress(value, scale)
                compressor_calls += 1
            for _ in range(schedule.refinement_steps):
                value = builder.refine(value)
                refinement_calls += 1
            pairs.append(builder.to_boolean(value))
    final_pair = pairs[output]
    result = dag.node("-", dag.node("*", builder.two, final_pair.numerator),
                      final_pair.denominator)
    return CompiledCircuit(dag, result, tuple(pairs), schedule, size, h_count,
                           compressor_calls, refinement_calls)


def tiny_query_interpreter(dag: IntegerDAG, high_opcode: int, low_opcode: int,
                           left_address: int, right_address: int) -> int:
    """One-instruction PosSLP interpreter for a complete fixed-width encoding.

    Registers 0 and 1 contain the corresponding constants. Boolean one-bit
    addresses select them. Opcode bits 00, 01, 10 mean +, -, *; 11 is malformed
    and returns zero. The only output slot is the new instruction. This tests
    variable instruction control, not the note's general parsing construction.
    """
    one = dag.one
    not_high = dag.node("-", one, high_opcode)
    not_low = dag.node("-", one, low_opcode)
    add_flag = dag.node("*", not_high, not_low)
    sub_flag = dag.node("*", not_high, low_opcode)
    mul_flag = dag.node("*", high_opcode, not_low)
    valid = dag.node("-", one, dag.node("*", high_opcode, low_opcode))

    def select(address: int) -> int:
        # Keep the selector circuit explicit although the selected value equals
        # the address bit for these two initial constant registers.
        first = dag.node("*", dag.node("-", one, address), dag.zero)
        second = dag.node("*", address, one)
        return dag.node("+", first, second)

    left, right = select(left_address), select(right_address)
    candidates = [dag.node(op, left, right) for op in ("+", "-", "*")]
    selected = [dag.node("*", flag, candidate)
                for flag, candidate in zip((add_flag, sub_flag, mul_flag), candidates)]
    value = dag.node("+", dag.node("+", selected[0], selected[1]), selected[2])
    return dag.node("*", valid, dag.node("H", value))
