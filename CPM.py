import networkx as nx
import matplotlib.pyplot as plt
import tabulate as tab


class TaskNode:
    def __init__(self, time=0, adj_list=None) -> None:
        """
        Constructor from TaskNode
        :param time: time it takes to complete a task
        :param adj_list: list of nodes adjacent to the nodes
        """
        # adj_list as optional parameter
        if adj_list is None:
            adj_list = []
        # Attributes from ActivityNode
        self.time = time
        self.adj_list = adj_list
        self.pred_list = []
        self.TPI = 0
        self.TPT = 0
        self.TUI = 0
        self.TUT = 0
        return


class TasksGraph:
    def __init__(self, nodes=0) -> None:
        self.number_of_nodes = nodes
        self.node_list = {}
        self.critical_path = []
        for n in range(nodes):
            node = TaskNode()
            self.node_list[str(chr(65 + n))] = node
        return

    def node_in_graph(self, node: str) -> bool:
        for n in self.node_list:
            if n == node:
                return True
        return False

    def add_node(self, name: str, time=0, adj_list=None) -> None:
        if adj_list is None:
            adj_list = []
        new_node = TaskNode(time=time, adj_list=adj_list)
        if name in self.node_list:
            new_node = self.node_list[name]
        new_node.time = time
        new_node.adj_list = adj_list
        self.node_list[name] = new_node
        for n in adj_list:
            node = TaskNode()
            if n in self.node_list:
                node = self.node_list[n]
                node.pred_list.append(name)
            else:
                node.pred_list.append(name)
                self.node_list[n] = node
        return

    def print_node_list(self) -> None:
        print("------Node List------")
        data = []
        for name in self.node_list:
            node = self.node_list[name]
            line = [name, node.adj_list if node.adj_list else "", node.pred_list if node.pred_list else "", node.time]
            data.append(line)
        print(tab.tabulate(data, headers=["Task", "Next", "Predecessor", "Time"], tablefmt="psql"))
        return

    def critical_path_method(self) -> None:
        # First part from CPM
        # Go through the graph from start to calculate TPI and TPT using BFS
        queue = ["Start"]
        path = []
        while queue:
            node_name = queue.pop(0)
            path.append(node_name)
            node = self.node_list[node_name]
            if node_name != "Start":
                times = []
                for p in node.pred_list:
                    predecessor = self.node_list[p]
                    times.append(predecessor.TPT)
                node.TPI = max(times)
            node.TPT = node.TPI + node.time
            for n in node.adj_list:
                if n not in queue and node not in path:
                    queue.append(n)

        # Second part from CPM
        # Go through the graph from end to calculate TUI and TPI using BFS
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
            for n in node.pred_list:
                if n not in queue and node not in path:
                    queue.append(n)

        # Third part from CPM
        # Go through the graph using only the nodes that have slack 0
        # Add to self.cpm all the nodes used in the slack 0 path
        queue = ["Start"]
        path = []

        while queue:
            node_name = queue.pop(0)
            path.append(node_name)
            node = self.node_list[node_name]

            if node.TPI == node.TUI:
                self.critical_path.append(node_name)

            for n in node.adj_list:
                if n not in queue and node not in path:
                    queue.append(n)
        return

    def print_cpm(self) -> None:
        self.critical_path_method()
        print("------Critical Path------")
        for node in self.critical_path:
            if node == self.critical_path[0]:
                print(node, end=" ")
            else:
                print(" ->", node, end=" ")
        print()
        return

    def print_times(self) -> None:
        for name in self.node_list:
            print(name)
            print("TPI:", self.node_list[name].TPI, end=" | ")
            print("TPT:", self.node_list[name].TPT)
            print("TUI:", self.node_list[name].TUI, end=" | ")
            print("TUT:", self.node_list[name].TUT, end=" ")
            print()
        print()
        return

    def print_graph(self) -> None:
        graph = nx.DiGraph()
        for node1 in self.node_list.keys():
            for node2 in self.node_list.get(node1).adj_list:
                graph.add_edge(node1, node2)

        nx.draw(graph, with_labels=True, font_weight='bold', node_size=1000, width=2.5, node_color='darkcyan',
                font_color='white')

        plt.show()
        return


def main() -> None:
    # graphA = TasksGraph()
    # graphA.add_node("Start", time=0, adj_list=["A", "B"])
    # graphA.add_node("A", time=3, adj_list=["C"])
    # graphA.add_node("B", time=4, adj_list=["D"])
    # graphA.add_node("C", time=2, adj_list=["E"])
    # graphA.add_node("D", time=8, adj_list=["F"])
    # graphA.add_node("E", time=5, adj_list=["F"])
    # graphA.add_node("F", time=1, adj_list=["End"])
    # graphA.print_node_list()
    # graphA.print_cpm()

    graph = TasksGraph()
    graph.add_node("Start", adj_list=["A"])
    graph.add_node("A", time=4, adj_list=["B", "C", "D"])
    graph.add_node("B", time=2, adj_list=["E"])
    graph.add_node("C", time=3, adj_list=["E"])
    graph.add_node("D", time=1, adj_list=["End"])
    graph.add_node("E", time=5, adj_list=["End"])
    graph.print_node_list()
    graph.print_cpm()

    return


if __name__ == '__main__':
    main()
