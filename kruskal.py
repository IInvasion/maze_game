"""Kruskal algorithm."""


class Kruskal:
    """Kruskal algorithm executor."""

    def __init__(self, edges):
        """Constructor."""
        self.edges = edges
        self.disjoints = []
        self.tree = []

    def debug_print(self):
        """Debug print."""
        print('Current tree is:')
        print(self.tree)
        print('Current disjoints are:')
        print(self.disjoints)
        input('Press <Enter> to continue...\n')

    def find_indicies(self, vertex1, vertex2):
        """Find disjoint indices for vertices."""
        idx1 = None
        idx2 = None
        for i, disjoint in enumerate(self.disjoints):
            if vertex1 in disjoint:
                assert idx1 is None
                idx1 = i
            if vertex2 in disjoint:
                assert idx2 is None
                idx2 = i
        return idx1, idx2

    def merge_disjoints(self, idx1, idx2):
        """Merge disjoints."""
        disjoint1 = self.disjoints[idx1]
        disjoint2 = self.disjoints[idx2]
        new_disjoint = disjoint1 | disjoint2
        self.disjoints[idx1] = new_disjoint
        del self.disjoints[idx2]

    def run(self, debug=False):
        """Run algorithm."""
        if debug:
            print(self.edges)
        for i, edge in enumerate(self.edges, 1):
            if debug:
                print(f'\nStep number {i}')
            self.step(edge, debug)
            if debug:
                self.debug_print()
        disjoints_count = len(self.disjoints)
        assert disjoints_count == 1, f"Disjoints count is {disjoints_count}"
        edges_count = len(self.tree)
        vertecies_count = len(self.disjoints[0])
        assert edges_count == vertecies_count - 1, \
            f"Edges count is {edges_count}; " \
            f"Vertecies count is {vertecies_count}"
        return self.tree

    def step(self, edge, debug=False):
        """Algorithm step."""
        vertex1 = edge[0]
        vertex2 = edge[1]
        idx1, idx2 = self.find_indicies(vertex1, vertex2)
        if debug:
            print(f'Vertex #1 is {vertex1}; index is {idx1}')
            print(f'Vertex #2 is {vertex2}; index is {idx2}')
        if idx1 == idx2:
            if idx1 is None:
                if debug:
                    print('New disjoint set')
                self.tree.append((vertex1, vertex2))
                self.disjoints.append({vertex1, vertex2})
            elif debug:
                print('Cycle case')
            return

        self.tree.append((vertex1, vertex2))
        if idx1 is not None and idx2 is not None:
            if debug:
                print('Merge disjoint sets case')
            self.merge_disjoints(idx1, idx2)
            return

        if debug:
            print('Join a new vertex case')
        idx = idx1 if idx1 is not None else idx2
        self.disjoints[idx] |= {vertex1, vertex2}


def build_tree(edges, debug=False):
    """Build a minimum spinning tree."""
    return Kruskal(edges).run(debug)
