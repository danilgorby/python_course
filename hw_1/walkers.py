from collections import defaultdict
import ast
import networkx as nx


class Fib_Walker_v1(ast.NodeVisitor):
    def __init__(self, ):
        self.stack = []
        self.graph = nx.Graph()
        self.node2label = dict()
        self.label2count = defaultdict(int)

    def add(self, node, node_label):
        label = type(node).__name__
        label_cnt = self.label2count[label]
        self.label2count[label] += 1

        if len(self.stack) != 0:
            parent_name = self.stack[-1]
        else:
            parent_name = None

        node_name = f"{label} ({label_cnt})"
        self.stack.append(node_name)
        self.graph.add_node(node_name)
        self.node2label[node_name] = node_label

        if parent_name:
            self.graph.add_edge(parent_name, node_name)

        super(self.__class__, self).generic_visit(node)
        self.stack.pop()

    def generic_visit(self, node):
        label = type(node).__name__
        self.add(node, label)

    def visit_FunctionDef(self, node):
        label = f"{type(node).__name__}\nname: {node.name}"
        self.add(node, label)

    def visit_Name(self, node):
        label = f"{type(node).__name__}\nid: {node.id}"
        self.add(node, label)

    def visit_arg(self, node):
        label = f"{type(node).__name__}\nname: {node.arg}"
        self.add(node, label)


class Fib_Walker_v2(ast.NodeVisitor):
    def __init__(self, ):
        self.stack = []
        self.graph = nx.DiGraph()
        self.node2label = dict()
        self.node2color = dict()
        self.label2count = defaultdict(int)

    def add(self, node, node_label, node_color):
        label = type(node).__name__
        label_cnt = self.label2count[label]
        self.label2count[label] += 1

        if len(self.stack) != 0:
            parent_name = self.stack[-1]
        else:
            parent_name = None

        node_name = f"{label} ({label_cnt})"
        self.stack.append(node_name)
        self.graph.add_node(node_name)
        self.node2label[node_name] = node_label
        self.node2color[node_name] = node_color

        if parent_name:
            self.graph.add_edge(parent_name, node_name)

        super(self.__class__, self).generic_visit(node)
        self.stack.pop()

    def generic_visit(self, node):
        label = type(node).__name__
        self.add(node, label, '#e5e5e5')

    # stmt
    def visit_Assign(self, node):
        self.add(node, str(type(node).__name__), '#64b5f6')

    def visit_Return(self, node):
        self.add(node, str(type(node).__name__), '#64b5f6')

    def visit_For(self, node):
        self.add(node, str(type(node).__name__), '#64b5f6')

    def visit_Add(self, node):
        self.add(node, str(type(node).__name__), '#64b5f6')

    def visit_FunctionDef(self, node):
        label = f"Function\nname: {node.name}"
        self.add(node, label, '#64b5f6')

    # expr
    def visit_BinOp(self, node):
        self.add(node, str(type(node).__name__), '#b9fbc0')

    def visit_Call(self, node):
        self.add(node, str(type(node).__name__), '#b9fbc0')

    def visit_Tuple(self, node):
        self.add(node, str(type(node).__name__), '#b9fbc0')

    def visit_Name(self, node):
        label = f"{type(node).__name__}\nid: {node.id}"
        self.add(node, label, '#b9fbc0')

    # args
    def visit_arg(self, node):
        label = f"{type(node).__name__}\nname: {node.arg}"
        self.add(node, label, '#ed6a5a')

    def visit_arguments(self, node):
        self.add(node, str(type(node).__name__), '#ed6a5a')

    # nums
    def visit_Num(self, node):
        label = f"{type(node).__name__}\nvalue: {node.n}"
        self.add(node, label, '#fbf8cc')
