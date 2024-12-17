import heapq
from collections import deque

class Pathfinding:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.distances = {}

    def d_star(self):
        self.distances = {self.goal: 0}
        priority_queue = []
        heapq.heappush(priority_queue, (0, self.goal))
        visited = set()
        node_expanded = 0

        while priority_queue:
           # print("running")
            node_expanded +=1
            current_cost, current = heapq.heappop(priority_queue)
            if current == self.start:
                return self.reconstruct_path(), node_expanded
            visited.add(current)
            for neighbor in self.get_neighbors(current):
                if neighbor in visited:
                    continue
                new_cost = current_cost + 1  # TO BE CHANGE IN FUTURE
                if neighbor not in self.distances or new_cost < self.distances[neighbor]:
                    self.distances[neighbor] = new_cost
                    priority = new_cost + self.manhattan_distance(self.start, neighbor)
                    heapq.heappush(priority_queue, (priority, neighbor))
       # print("done")
        return None, node_expanded  # No path found
    
    def a_star(self):
        self.distances = {self.start: 0}  # Start from the start node
        priority_queue = []
        heapq.heappush(priority_queue, (0, self.start))
        visited = set()
        came_from = {}
        node_expanded = 0

        while priority_queue:
            current_cost, current = heapq.heappop(priority_queue)
            node_expanded += 1
            if current == self.goal:
                return self.reconstruct_path2(came_from), node_expanded  # Use came_from to reconstruct path
            visited.add(current)
            for neighbor in self.get_neighbors(current):
                if neighbor in visited:
                    continue
                new_cost = current_cost + 1  # Customize this for variable costs
                if neighbor not in self.distances or new_cost < self.distances[neighbor]:
                    self.distances[neighbor] = new_cost
                    priority = new_cost + self.manhattan_distance(self.goal, neighbor)
                    heapq.heappush(priority_queue, (priority, neighbor))
                    came_from[neighbor] = current  # Track path

        return None, node_expanded  # No path found
    
    def bfs(self):
        queue = deque([self.start])
        came_from = {self.start: None}
        visited = set()

        while queue:
            current = queue.popleft()
            if current == self.goal:
                return self.reconstruct_path2(came_from)
            visited.add(current)
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited and neighbor not in came_from:
                    came_from[neighbor] = current
                    queue.append(neighbor)
        return None
    
    def greedy_best_first_search(self):
        priority_queue = [(self.manhattan_distance(self.start, self.goal), self.start)]
        came_from = {self.start: None}
        visited = set()
        node_expanded = 0  # Track the number of expanded nodes

        while priority_queue:
            _, current = heapq.heappop(priority_queue)
            node_expanded += 1  # Increment expanded node count

            if current == self.goal:
                return self.reconstruct_path2(came_from), node_expanded

            visited.add(current)

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited and neighbor not in came_from:
                    came_from[neighbor] = current
                    heapq.heappush(priority_queue, (self.manhattan_distance(neighbor, self.goal), neighbor))

        return None, node_expanded  # No path found

    def reconstruct_path(self):
        path = []
        current = self.start 
        while current != self.goal:
            path.append(current)
            current = min((neighbor for neighbor in self.get_neighbors(current)),key=lambda x: self.distances.get(x, float("inf")),default=self.goal)
        path.append(self.goal)
        return path
    
    def reconstruct_path2(self, came_from):
        path = []
        current = self.goal
        while current != self.start:
            path.append(current)
            current = came_from.get(current)
        path.append(self.start)
        path.reverse()  # Reverse path to start from the beginning
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