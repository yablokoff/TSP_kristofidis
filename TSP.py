class MST:

    dists = []
    vertex_queue = {}
    MST_nodes=[]

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

    def find(self):
        new_city = self._extract_min()
        self.MST_nodes.append(new_city)
        while self.vertex_queue:
            new_city_id = new_city[0]
            for city in self.vertex_queue.items():
                city_id= city[0]
                if self.dists[new_city_id][city_id] < city[1]["distance"]:
                    self.vertex_queue[city_id]["distance"] = self.dists[new_city_id][city_id]
                    self.vertex_queue[city_id]["parent"] = new_city_id
            new_city = self._extract_min()
            self.MST_nodes.append(new_city)

if __name__ == "__main__":
    inst = MST(15)
    print inst.find()
