import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        self.graph = nx.Graph()

    def add_vertex(self, v):
        self.graph.add_node(v)

    def add_edge(self, u, v):
        self.graph.add_edge(u, v)

    def remove_vertex(self, v):
        self.graph.remove_node(v)

    def remove_edge(self, u, v):
        if self.graph.has_edge(u, v):
            self.graph.remove_edge(u, v)

    def find_match(self, LHS):
        """ Find a match between LHS and self (host graph) """
        mapping = {}
        for lv in LHS.graph.nodes:
            if lv in self.graph.nodes:
                mapping[lv] = lv  # A simple identity match for illustration
            else:
                return None  # No match found
        return mapping

    def single_pushout(self, LHS, RHS):
        """ Perform a single pushout rewriting from LHS to RHS """
        # Step 1: Find the match between LHS and the current graph
        match = self.find_match(LHS)
        if match is None:
            print("No match found between LHS and host graph.")
            return

        # Step 2: Delete the matched part of the host graph that corresponds to LHS
        for lv in LHS.graph.nodes:
            gv = match[lv]
            self.remove_vertex(gv)

        for (lu, lv) in LHS.graph.edges:
            gu, gv = match[lu], match[lv]
            self.remove_edge(gu, gv)

        # Step 3: Add the RHS graph into the host graph
        new_mapping = {}
        for rv in RHS.graph.nodes:
            if rv not in match.values():
                self.add_vertex(rv)
                new_mapping[rv] = rv
            else:
                new_mapping[rv] = match[rv]  # Merge with existing vertices

        for (ru, rv) in RHS.graph.edges:
            self.add_edge(new_mapping[ru], new_mapping[rv])

        print("Graph after transformation:")
        print(f"Vertices: {self.graph.nodes}")
        print(f"Edges: {self.graph.edges}")

    def visualize_graph(self):
        """ Visualize the current graph using networkx and matplotlib """
        plt.figure(figsize=(6, 6))
        pos = nx.spring_layout(self.graph)  # Layout for visualization
        nx.draw(self.graph, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=2000,
                font_size=16)
        plt.show()


# Example usage

# Define the LHS (pattern to find)
LHS = Graph()
LHS.add_vertex("A")
LHS.add_vertex("B")
LHS.add_edge("A", "B")

# Define the RHS (replacement graph)
RHS = Graph()
RHS.add_vertex("C")
RHS.add_vertex("D")
RHS.add_edge("C", "D")

# Host Graph (the graph in which we perform rewriting)
G = Graph()
G.add_vertex("A")
G.add_vertex("B")
G.add_vertex("E")
G.add_edge("A", "B")
G.add_edge("A", "E")

print("Initial Graph:")
LHS.visualize_graph()

RHS.visualize_graph()



# Perform the single pushout
G.single_pushout(LHS, RHS)

G.visualize_graph()
