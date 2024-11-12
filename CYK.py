import json

class CYKGrammarParser:
    def __init__(self, grammar: dict) -> None:
        self.grammar = grammar
        self.table = []
        self.parse_tree = []
        
    def parse(self, sentence: str) -> bool:
        words = sentence.split()
        n = len(words)
        self.table = [[set() for _ in range(n)] for _ in range(n)]
        self.parse_tree = [[None for _ in range(n)] for _ in range(n)]
        
        for j in range(n):
            for variable, productions in self.grammar["REGLAS"].items():
                if words[j] in productions:
                    self.table[j][j].add(variable)
                    self.parse_tree[j][j] = TreeNode(variable, children=[])

            for i in range(j - 1, -1, -1):
                for k in range(i, j):
                    for variable, productions in self.grammar["REGLAS"].items():
                        for production in productions:
                            symbols = production.split()
                            if len(symbols) == 2:
                                B, C = symbols
                                if B in self.table[i][k] and C in self.table[k + 1][j]:
                                    self.table[i][j].add(variable)
                                    left_node = self.parse_tree[i][k]
                                    right_node = self.parse_tree[k + 1][j]
                                    if left_node and right_node:
                                        self.parse_tree[i][j] = TreeNode(variable, [left_node, right_node])
        
        return self.grammar["INICIAL"] in self.table[0][n - 1]
    
    def print_table(self):
        for row in self.table:
            print("\t".join(["|".join(cell) if cell else "-" for cell in row]))

    def generate_parse_tree_graph(self, output_file="parse_tree"):
        from graphviz import Digraph
        dot = Digraph(comment='Parse Tree')
        start_node = self.parse_tree[0][-1]
        if start_node:
            self._add_tree_to_graph(dot, start_node)
        dot.render(output_file, format='png', view=True)
        return dot

    def _add_tree_to_graph(self, dot, node, parent_id=None):
        node_id = str(id(node))
        dot.node(node_id, node.label)
        if parent_id:
            dot.edge(parent_id, node_id)
        for child in node.children:
            self._add_tree_to_graph(dot, child, node_id)

class TreeNode:
    def __init__(self, label: str, children: list = None) -> None:
        self.label = label
        self.children = children if children else []

    def __str__(self):
        return self.label
