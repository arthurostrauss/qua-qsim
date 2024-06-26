from quaqsim.program_ast._for import For
from quaqsim.program_to_quantum_pulse_sim_compiler.context import Context
from quaqsim.program_to_quantum_pulse_sim_compiler.visitors.expression_visitors.expression_visitor import \
    ExpressionVisitor
from quaqsim.program_to_quantum_pulse_sim_compiler.visitors.visitor import Visitor


class ForVisitor(Visitor):
    def visit(self, node: For, context: Context):
        condition = ExpressionVisitor().visit(node.cond, context)

        from quaqsim.program_to_quantum_pulse_sim_compiler.visitors.node_visitor import \
            NodeVisitor
        node_visitor = NodeVisitor()
        while condition:
            for inner_node in node.body:
                inner_node.accept(node_visitor, context)
            condition = ExpressionVisitor().visit(node.cond, context)
