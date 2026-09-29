"""Targeted exact and structural checks; run this file directly with Python."""

from fractions import Fraction
from itertools import product
import unittest

from sign_compiler_reference import (
    EvaluationLimit, IntegerDAG, PrecisionSchedule, RationalBuilder,
    RationalNode, compile_sign_circuit, tiny_query_interpreter,
)


def integer_node(dag: IntegerDAG, value: int) -> int:
    """Construct small test constants from 0, 1 using binary gates."""
    if value < 0:
        return dag.node("-", dag.zero, integer_node(dag, -value))
    result = dag.zero
    for bit in bin(value)[2:]:
        result = dag.node("+", result, result)
        if bit == "1":
            result = dag.node("+", result, dag.one)
    return result


def pair_value(pair: RationalNode, values: list[int]) -> Fraction:
    return Fraction(values[pair.numerator], values[pair.denominator])


class SignCompilerChecks(unittest.TestCase):
    def assert_behavior(self, source, output, labels, *, schedule=None):
        compiled = compile_sign_circuit(source, output, schedule=schedule)
        for assignment in product((0, 1), repeat=len(labels)):
            inputs = dict(zip(labels, assignment))
            original = source.evaluate(inputs)[output]
            self.assertIn(original, (0, 1), "Fixture violates Boolean-output promise")
            values = compiled.dag.evaluate(inputs)
            self.assertEqual(int(values[compiled.output] > 0), original, inputs)
            for pair in compiled.pairs:
                self.assertGreater(values[pair.denominator], 0)
            if compiled.uses_theorem_schedule:
                approximate = pair_value(compiled.pairs[output], values)
                self.assertLess(abs(approximate - original), Fraction(1, 4))
        return compiled

    def assert_structure(self, compiled):
        self.assertLessEqual(compiled.dag.gate_count, compiled.construction_gate_bound())
        for index, node in enumerate(compiled.dag.nodes):
            self.assertIn(node.op, ("zero", "one", "input", "+", "-", "*"))
            self.assertTrue(all(0 <= arg < index for arg in node.args))
            self.assertEqual(len(node.args), 2 if node.op in ("+", "-", "*") else 0)
        self.assertEqual(compiled.compressor_calls,
                         compiled.threshold_count * compiled.schedule.compressor_index)
        self.assertEqual(compiled.refinement_calls,
                         compiled.threshold_count * compiled.schedule.refinement_steps)

    def test_pair_identities_with_negative_zero_and_fractional_values(self):
        samples = [(-3, 2), (0, 3), (1, 1), (4, 3)]
        for left, right in product(samples, repeat=2):
            dag = IntegerDAG()
            builder = RationalBuilder(dag)
            a, b = [RationalNode(integer_node(dag, p), integer_node(dag, q))
                    for p, q in (left, right)]
            results = [builder.arithmetic(op, a, b) for op in ("+", "-", "*")]
            values = dag.evaluate({})
            x, y = Fraction(*left), Fraction(*right)
            for pair, expected in zip(results, (x + y, x - y, x * y)):
                self.assertGreater(values[pair.denominator], 0)
                self.assertEqual(pair_value(pair, values), expected)
        for p, q in samples:
            for scale in (1, 2, 4, 16):
                dag = IntegerDAG()
                builder = RationalBuilder(dag)
                value = RationalNode(integer_node(dag, p), integer_node(dag, q))
                compressed = builder.compress(value, integer_node(dag, scale))
                refined = builder.refine(value)
                shifted = builder.shift(value)
                boolean = builder.to_boolean(value)
                values = dag.evaluate({})
                x = Fraction(p, q)
                expected = (2*scale*x/(scale+x*x), 2*x/(1+x*x), 4*x-2, (1+x)/2)
                for pair, want in zip((compressed, refined, shifted, boolean), expected):
                    self.assertGreater(values[pair.denominator], 0)
                    self.assertEqual(pair_value(pair, values), want)

    def test_full_schedule_strict_sign_and_cancellation(self):
        # Every fixture has one threshold and at most two source gates. No
        # reduced precision is used here, including the exact zero boundary.
        for fixture in ("input", "zero", "one", "negative", "cancellation"):
            dag = IntegerDAG()
            x = dag.input("x")
            argument = {"input": x, "zero": dag.zero, "one": dag.one}.get(fixture)
            if fixture == "negative":
                argument = dag.node("-", dag.zero, dag.one)
            if fixture == "cancellation":
                argument = dag.node("-", x, x)
            output = dag.node("H", argument)
            compiled = self.assert_behavior(dag, output, ("x",))
            self.assertTrue(compiled.uses_theorem_schedule)
            self.assert_structure(compiled)

    def test_arithmetic_boolean_logic_and_shared_subcircuit(self):
        dag = IntegerDAG()
        x, y = dag.input("x"), dag.input("y")
        shared = dag.node("*", x, y)
        self.assertEqual(shared, dag.node("*", x, y))
        # XOR = x + y - 2xy; reference the shared xy twice.
        output = dag.node("-", dag.node("+", x, y), dag.node("+", shared, shared))
        compiled = self.assert_behavior(dag, output, ("x", "y"))
        self.assertEqual(dag.gate_count, 4)
        self.assertEqual(compiled.threshold_count, 0)
        self.assert_structure(compiled)
        fanout = [0] * len(compiled.dag.nodes)
        for node in compiled.dag.nodes:
            for arg in node.args:
                fanout[arg] += 1
        self.assertGreater(max(fanout), 1)
        self.assertEqual(len(set(compiled.dag.nodes)), len(compiled.dag.nodes))

    def test_full_schedule_arithmetic_after_a_threshold(self):
        for operation in ("complement", "square"):
            dag = IntegerDAG()
            threshold = dag.node("H", dag.input("x"))
            if operation == "complement":
                output = dag.node("-", dag.one, threshold)
            else:
                output = dag.node("*", threshold, threshold)
            compiled = self.assert_behavior(dag, output, ("x",))
            self.assertEqual(compiled.source_size, 2)
            self.assertTrue(compiled.uses_theorem_schedule)
            self.assert_structure(compiled)

    def test_reduced_schedule_nested_adaptive_selection(self):
        dag = IntegerDAG()
        x, y = dag.input("x"), dag.input("y")
        first = dag.node("H", dag.node("-", x, y))
        # Select a later query from the earlier strict sign answer.
        selected = dag.node("+", dag.node("*", first, x),
                            dag.node("*", dag.node("-", dag.one, first), y))
        output = dag.node("H", selected)
        reduced = PrecisionSchedule(1, 1)
        compiled = self.assert_behavior(dag, output, ("x", "y"), schedule=reduced)
        self.assertFalse(compiled.uses_theorem_schedule)
        full = compile_sign_circuit(dag, output)
        self.assertTrue(full.uses_theorem_schedule)
        self.assert_structure(full)  # Deliberately do not evaluate this DAG.

    def test_tiny_variable_query_interpreter(self):
        dag = IntegerDAG()
        labels = ("high", "low", "left", "right")
        high, low, left, right = (dag.input(label) for label in labels)
        output = tiny_query_interpreter(dag, high, low, left, right)
        for assignment in product((0, 1), repeat=4):
            h, l, a, b = assignment
            expected = {0: int(a+b > 0), 1: int(a-b > 0), 2: int(a*b > 0), 3: 0}[2*h+l]
            self.assertEqual(dag.evaluate(dict(zip(labels, assignment)))[output], expected)
        reduced = self.assert_behavior(dag, output, labels, schedule=PrecisionSchedule(2, 2))
        self.assertFalse(reduced.uses_theorem_schedule)
        full = compile_sign_circuit(dag, output)
        self.assertGreater(full.source_size, 20)  # Decoder and selectors count.
        self.assert_structure(full)

    def test_later_query_opcode_depends_on_earlier_answer(self):
        dag = IntegerDAG()
        x = dag.input("x")
        earlier_answer = dag.node("H", x)
        # Earlier 0: opcode 00 computes 1+1, hence answer 1.
        # Earlier 1: opcode 01 computes 1-1, hence answer 0.
        output = tiny_query_interpreter(dag, dag.zero, earlier_answer, dag.one, dag.one)
        for value in (0, 1):
            self.assertEqual(dag.evaluate({"x": value})[output], 1-value)
        reduced = self.assert_behavior(dag, output, ("x",), schedule=PrecisionSchedule(1, 1))
        self.assertFalse(reduced.uses_theorem_schedule)
        self.assert_structure(compile_sign_circuit(dag, output))

    def test_reduced_schedule_has_an_explicit_counterexample(self):
        dag = IntegerDAG()
        first = dag.node("H", dag.one)
        multiplier = integer_node(dag, 32)
        leakage = dag.node("*", multiplier, dag.node("-", dag.one, first))
        output = dag.node("H", dag.node("-", dag.one, leakage))
        compiled = compile_sign_circuit(dag, output, schedule=PrecisionSchedule(1, 1))
        self.assertFalse(compiled.uses_theorem_schedule)
        self.assertEqual(dag.evaluate({})[output], 1)
        values = compiled.dag.evaluate({})
        self.assertLessEqual(values[compiled.output], 0)
        self.assertEqual(pair_value(compiled.pairs[first], values), Fraction(9, 10))

    def test_full_schedule_quadratic_size_without_integer_expansion(self):
        for size in (1, 2, 4, 8, 16, 32, 64, 128):
            dag = IntegerDAG()
            output = dag.input("x")
            for _ in range(size):
                output = dag.node("H", output)
            compiled = compile_sign_circuit(dag, output)
            self.assertEqual(compiled.source_size, size)
            self.assertEqual(compiled.schedule, PrecisionSchedule(size + 2, 2*size + 5))
            self.assertLessEqual(compiled.dag.gate_count, 17*size*size + 49*size + 5)
            self.assert_structure(compiled)
            # Nodes contain operation names and references, never expanded M_j.
            self.assertTrue(all(node.op in IntegerDAG.ARITY for node in compiled.dag.nodes))

    def test_evaluation_budget_and_boolean_input_contract(self):
        dag = IntegerDAG()
        x = dag.input("x")
        with self.assertRaises(ValueError):
            dag.evaluate({"x": 2})
        with self.assertRaises(ValueError):
            dag.evaluate({"x": 0.0})
        with self.assertRaises(ValueError):
            dag.node("+", x, len(dag.nodes))
        value = dag.node("+", dag.one, dag.one)
        for _ in range(8):
            value = dag.node("*", value, value)
        with self.assertRaises(EvaluationLimit):
            dag.evaluate({"x": 0}, max_bits=64)


if __name__ == "__main__":
    unittest.main(verbosity=2)
