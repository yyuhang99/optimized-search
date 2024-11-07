import heapq

class Pathfinding:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.distances = {}

    def d_star_step_by_step(self):
        current_position = self.start
        while current_position != self.goal:
            next_position = self.calculate_next_step(current_position)
            yield next_position
            current_position = next_position
        yield self.goal
        
    def d_star(self):
        self.distances = {self.goal: 0}
        priority_queue = []
        heapq.heappush(priority_queue, (0, self.goal))
        visited = set()

        while priority_queue:
            print("running")
            current_cost, current = heapq.heappop(priority_queue)
            if current == self.start:
                return self.reconstruct_path()
            visited.add(current)
            for neighbor in self.get_neighbors(current):
                if neighbor in visited:
                    continue
                new_cost = current_cost + 1  # TO BE CHANGE IN FUTURE
                if neighbor not in self.distances or new_cost < self.distances[neighbor]:
                    self.distances[neighbor] = new_cost
                    priority = new_cost + self.manhattan_distance(self.start, neighbor)
                    heapq.heappush(priority_queue, (priority, neighbor))
        print("done")
        return None  # No path found

    def reconstruct_path(self):
        path = []
        current = self.start 
        while current != self.goal:
            path.append(current)
            current = min((neighbor for neighbor in self.get_neighbors(current)),key=lambda x: self.distances.get(x, float("inf")),default=self.goal)
        path.append(self.goal)
        return path

    def manhattan_distance(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, pos):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for move in directions:
            neighbor = (pos[0] + move[0], pos[1] + move[1])
            if 0 <= neighbor[0] < len(self.grid) and 0 <= neighbor[1] < len(self.grid[0]) and self.grid[neighbor[0]][neighbor[1]] != -1:
                neighbors.append(neighbor)
        return neighbors