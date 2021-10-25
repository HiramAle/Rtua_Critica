class ActivityNode:
    def __init__(self, time=0, adj_list=None) -> None:
        if adj_list is None:
            adj_list = []
        self.time = time
        self.adj_list = adj_list
        self.predecessors = []
        self.TPI = 0
        self.TPT = 0
        self.TUI = 0
        self.TUT = 0
        return

    def add_adj(self, node: str):
        self.adj_list.append(node)
        return


class Graph:
    def __init__(self, nodes=0) -> None:
        self.number_of_nodes = nodes
        self.node_list = {}
        for n in range(nodes):
            node = ActivityNode()
            self.node_list[str(chr(65 + n))] = node
        return

    def node_in_graph(self, node: str) -> bool:
        for n in self.node_list:
            if n == node:
                return True
        return False

    def add_node(self, name: str, time=0, adj_list=None):
        if adj_list is None:
            adj_list = []
        # Se revisa si el nodo a crear ya existe
        new_node = ActivityNode(time=time, adj_list=adj_list)
        if name in self.node_list:
            new_node = self.node_list[name]
        new_node.time = time
        new_node.adj_list = adj_list
        self.node_list[name] = new_node
        # Se itera sobre su lista de adjacencia
        for n in adj_list:
            node = ActivityNode()
            if n in self.node_list:
                node = self.node_list[n]
                node.predecessors.append(name)
            else:
                node.predecessors.append(name)
                self.node_list[n] = node
        return

    def print_node_list(self):
        print("---Node List---")
        for name in self.node_list:
            node = self.node_list[name]
            print(name, end="")
            print("(" + str(node.time) + ")", end="")
            if node.adj_list:
                print(":", node.adj_list, end="")
            if node.predecessors:
                print(":", node.predecessors, end="")
            print()
        return

    def get_critical_path(self):
        queue = ["Start"]
        path = []
        while queue:
            node_name = queue.pop(0)
            path.append(node_name)
            node = self.node_list[node_name]
            if node_name != "Start":
                times = []
                for p in node.predecessors:
                    predecessor = self.node_list[p]
                    times.append(predecessor.TPT)
                node.TPI = max(times)
            node.TPT = node.TPI + node.time
            for n in node.adj_list:
                if n not in queue and node not in path:
                    queue.append(n)

        queue = ["End"]
        path = []

        while queue:
            node_name = queue.pop(0)
            path.append(node_name)
            node = self.node_list[node_name]
            if node_name == "End":
                node.TUT = node.TPT
            else:
                times = []
                for p in node.adj_list:
                    predecessor = self.node_list[p]
                    times.append(predecessor.TUI)
                node.TUT = min(times)
            node.TUI = node.TUT - node.time
            for n in node.predecessors:
                if n not in queue and node not in path:
                    queue.append(n)

        queue = ["Start"]
        path = []
        cpm = []

        while queue:
            node_name = queue.pop(0)
            path.append(node_name)
            node = self.node_list[node_name]

            if node.TPI == node.TUI:
                cpm.append(node_name)

            for n in node.adj_list:
                if n not in queue and node not in path:
                    queue.append(n)

        return cpm

    def print_times(self):
        for name in self.node_list:
            print(name)
            print("TPI:", self.node_list[name].TPI, end=" | ")
            print("TPT:", self.node_list[name].TPT)
            print("TUI:", self.node_list[name].TUI, end=" | ")
            print("TUT:", self.node_list[name].TUT, end=" ")
            print()
        print()


def main() -> None:
    # graphA = Graph()
    # graphA.add_node("Start", time=0, adj_list=["A", "B"])
    # graphA.add_node("A", time=3, adj_list=["C"])
    # graphA.add_node("B", time=4, adj_list=["D"])
    # graphA.add_node("C", time=2, adj_list=["E"])
    # graphA.add_node("D", time=8, adj_list=["F"])
    # graphA.add_node("E", time=5, adj_list=["F"])
    # graphA.add_node("F", time=1, adj_list=["End"])
    # graphA.print_node_list()
    # print(graphA.get_critical_path())

    graph = Graph()
    graph.add_node("Start", adj_list=["A"])
    graph.add_node("A", time=4, adj_list=["B", "C", "D"])
    graph.add_node("B", time=2, adj_list=["E"])
    graph.add_node("C", time=3, adj_list=["E"])
    graph.add_node("D", time=1, adj_list=["End"])
    graph.add_node("E", time=5, adj_list=["End"])
    graph.print_node_list()
    print(graph.get_critical_path())

    return


if __name__ == '__main__':
    main()
