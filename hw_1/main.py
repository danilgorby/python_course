from walkers import Fib_Walker_v1, Fib_Walker_v2
import ast
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout


if __name__ == "__main__":
    with open('funcs.py', "r") as f:
        source = f.read()
    root = ast.parse(source).body[0]

    # v1
    plt.figure(figsize=(10, 10))
    walker1 = Fib_Walker_v1()
    walker1.visit(root)
    nx.draw(walker1.graph, labels=walker1.node2label, with_labels=True)
    plt.savefig("artifacts/AST_v1.png")

    # v2
    plt.figure(figsize=(30, 10))
    walker2 = Fib_Walker_v2()
    walker2.visit(root)
    pos = graphviz_layout(walker2.graph, prog="dot")
    options = {"edgecolors": "tab:gray", "alpha": 0.9,
               'node_size': 10000, 'with_labels': True}
    nx.draw(walker2.graph, pos, labels=walker2.node2label,
            node_color=walker2.node2color.values(), **options)
    plt.savefig("artifacts/AST_v2.png")
