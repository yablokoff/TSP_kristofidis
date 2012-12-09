from collections import defaultdict

class TSP:

    dists = []
    vertex_queue = {}

    def __init__(self, cities_count):
        self.CITIES_COUNT = cities_count
        with open("15_cities.txt", "r") as cities_table:
            for city in cities_table:
                city_dists = [int(city_dist) for city_dist in city.split(" ")]
                self.dists.append(city_dists)
        for city_id in range(self.CITIES_COUNT):
            self.vertex_queue[city_id] = {"parent" : -1, "distance" : 10**6}

    def _extract_min(self):
        """
        Extract next vertex from queue.
        """
        current_city = min(self.vertex_queue.items(), key=lambda city: city[1]["distance"])
        del self.vertex_queue[current_city[0]]
        return current_city

    def find_MST(self):
        new_city = self._extract_min()
        MST_graph = list()
        MST_nodes = list()
        MST_nodes.append(new_city)
        while self.vertex_queue:
            new_city_id = new_city[0]
            for city in self.vertex_queue.items():
                city_id= city[0]
                if self.dists[new_city_id][city_id] < city[1]["distance"]:
                    self.vertex_queue[city_id]["distance"] = self.dists[new_city_id][city_id]
                    self.vertex_queue[city_id]["parent"] = new_city_id
            new_city = self._extract_min()
            MST_nodes.append(new_city)
        for node in MST_nodes[1:]:
            MST_graph.append( (node[1]["parent"], node[0]) )
        return MST_graph

    def find_odd_nodes(self, MST_graph):
        odd_nodes = list()
        adjacent_edges_count = defaultdict(int)
        for from_node, to_node in MST_graph:
            adjacent_edges_count[from_node] += 1
            adjacent_edges_count[to_node] += 1
        for node_id, count in adjacent_edges_count.iteritems():
            if count % 2:
                odd_nodes.append(node_id)
        return odd_nodes

    def _calc_cost_of_edges(self, edges):
        sum_cost = 0
        for edge in edges:
            sum_cost += self.dists[edge[0]][edge[1]]
        return sum_cost

    def _min_perfect_matching(self, chosen_edges, nodes):
        if len(nodes) == 2:
            chosen_edges.append((nodes[0], nodes[1]))
            cost = self._calc_cost_of_edges(chosen_edges)
            if cost < self.min_cost:
                self.min_cost = cost
                self.edges = chosen_edges
            return
        for first_node in nodes:
            nodes_wo_first = nodes[:]
            nodes_wo_first.remove(first_node)
            for sec_node in nodes_wo_first:
                nodes_wo_both = nodes_wo_first[:]
                nodes_wo_both.remove(sec_node)
                chosen_edges.append( (first_node, sec_node) )
                self._min_perfect_matching(chosen_edges[:], nodes_wo_both)
                chosen_edges.pop()

    def find_minimum_perfect_matching(self, nodes):
        self.min_cost = 10**6
        self.edges = list()
        self._min_perfect_matching([], nodes)
        return self.edges

    def extend_MST_with_perfect_matchings(self, MST):
        odd_nodes = self.find_odd_nodes(MST)
        perfect_matching_edges = self.find_minimum_perfect_matching(odd_nodes)
        MST.extend(perfect_matching_edges)
        return MST

    def _get_first_neighbor(self, node, edges):
        for first_node, sec_node in edges:
            if first_node == node:
                return sec_node
            elif sec_node == node:
                return first_node
        return None

    def find_euler_circuit(self, edges):
        path = [0]
        while len(edges):
            for node in path:
                if self._get_first_neighbor(node, edges):
                    break
            while self._get_first_neighbor(node, edges):
                neighbor = self._get_first_neighbor(node, edges)
                try:
                    edges.remove( (node, neighbor) )
                except ValueError:
                    edges.remove( (neighbor, node) )
                if not len(edges):
                    path.append(node)
                else:
                    path.append(neighbor)
                node = neighbor
        return path

if __name__ == "__main__":
    inst = TSP(15)
    MST_graph = inst.find_MST()
    extended_MST = inst.extend_MST_with_perfect_matchings(MST_graph)
    euler_path = inst.find_euler_circuit(extended_MST)