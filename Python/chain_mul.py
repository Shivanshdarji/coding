from collections import deque

class Graph:
    def __init__(self):
        self.adj = {}

    def add_edge(self, u, v):
        if u not in self.adj:
            self.adj[u] = []
        self.adj[u].append(v)

    def dfs_util(self, v, visited, result):
        visited.add(v)
        result.append(v)
        for neighbor in self.adj.get(v, []):
            if neighbor not in visited:
                self.dfs_util(neighbor, visited, result)

    def dfs(self, start):
        visited = set()
        result = []
        self.dfs_util(start, visited, result)
        return result

    def bfs(self, start):
        visited = set()
        queue = deque([start])
        result = []
        visited.add(start)
        while queue:
            v = queue.popleft()
            result.append(v)
            for neighbor in self.adj.get(v, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return result

g = Graph()
g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(1, 2)
g.add_edge(2, 0)
g.add_edge(2, 3)
g.add_edge(3, 3)

print("Shivansh Darji\n230410107124")
print("DFS:", g.dfs(2))
print("BFS:", g.bfs(2))
