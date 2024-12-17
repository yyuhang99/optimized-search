import heapq

class JumpStart:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.distances = {}
        self.came_from = {}
        self.node_expanded = 0
    
    def jump_point_search(self):
        self.distances = {self.start: 0}
        priority_queue = []
        heapq.heappush(priority_queue, (0, self.start))
        visited = set()

        while priority_queue:
            current_cost, current = heapq.heappop(priority_queue)
            self.node_expanded += 1
            if current == self.goal:
                return self.reconstruct_path(), self.node_expanded
            
            visited.add(current)
            for neighbor in self.get_neighbors(current):
                if neighbor in visited:
                    continue
                
                jump_point = self.jump(current, neighbor)
                if not jump_point:
                    continue

                new_cost = current_cost + self.manhattan_distance(current, jump_point)
                if jump_point not in self.distances or new_cost < self.distances[jump_point]:
                    self.distances[jump_point] = new_cost
                    priority = new_cost + self.manhattan_distance(jump_point, self.goal)
                    heapq.heappush(priority_queue, (priority, jump_point))
                    self.came_from[jump_point] = current

        return None, self.node_expanded  # No path found

    def jump(self, current, direction):
        """Recursive jump method to determine valid jump points."""
        next_pos = (current[0] + direction[0], current[1] + direction[1])
        if not self.is_valid(next_pos):
            return None
        if next_pos == self.goal:
            return next_pos

        # Forced neighbor check
        if self.has_forced_neighbors(next_pos, direction):
            return next_pos

        # Continue in the same direction
        return self.jump(next_pos, direction)

    def has_forced_neighbors(self, pos, direction):
        """Check for forced neighbors."""
        x, y = pos
        dx, dy = direction

        # Check perpendicular neighbors for forced conditions
        if dx != 0:  # Horizontal movement
            return (
                self.is_valid((x, y - 1)) and not self.is_valid((x - dx, y - 1)) or
                self.is_valid((x, y + 1)) and not self.is_valid((x - dx, y + 1))
            )
        elif dy != 0:  # Vertical movement
            return (
                self.is_valid((x - 1, y)) and not self.is_valid((x - 1, y - dy)) or
                self.is_valid((x + 1, y)) and not self.is_valid((x + 1, y - dy))
            )
        return False

    def get_neighbors(self, pos):
        """Get all valid neighbors for a given position."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for move in directions:
            neighbor = (pos[0] + move[0], pos[1] + move[1])
            if self.is_valid(neighbor):
                neighbors.append(move)
        return neighbors

    def is_valid(self, pos):
        """Check if a position is valid and not an obstacle."""
        x, y = pos
        return 0 <= x < self.rows and 0 <= y < self.cols and self.grid[x][y] != -1

    def reconstruct_path(self):
        """Reconstruct the path from start to goal."""
        path = []
        current = self.goal
        while current != self.start:
            path.append(current)
            current = self.came_from.get(current)
        path.append(self.start)
        path.reverse()
        return path

    def manhattan_distance(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
