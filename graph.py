import threading
from collections import deque

class Graph:
    def __init__(self, directed=False):
        self.graph = {}
        self.directed = directed
        self.lock = threading.Lock()
    
    def add_vertex(self, vertex):
        if not isinstance(vertex, (int, str, tuple)):
            raise ValueError("Vertex must be a hashable type.")
        with self.lock:
            if vertex not in self.graph:
                self.graph[vertex] = []
    
    def add_edge(self, src, dest):
        if src not in self.graph or dest not in self.graph:
            raise KeyError("Both vertices must exist in the graph.")
        with self.lock:
            if dest not in self.graph[src]:
                self.graph[src].append(dest)
            if not self.directed and src not in self.graph[dest]:
                self.graph[dest].append(src)
    
    def remove_edge(self, src, dest):
        if not self.graph:
            raise ValueError("Graph is empty. No edges to remove.")
        with self.lock:
            if src in self.graph and dest in self.graph[src]:
                self.graph[src].remove(dest)
            if not self.directed and dest in self.graph and src in self.graph[dest]:
                self.graph[dest].remove(src)
    
    def remove_vertex(self, vertex):
        if not self.graph:
            raise ValueError("Graph is empty. No vertices to remove.")
        with self.lock:
            if vertex in self.graph:
                for adj in list(self.graph):
                    if vertex in self.graph[adj]:
                        self.graph[adj].remove(vertex)
                del self.graph[vertex]
            else:
                raise KeyError(f"Vertex '{vertex}' does not exist in the graph.")
    
    def get_adjacent_vertices(self, vertex):
        with self.lock:
            return self.graph.get(vertex, [])
    
    def bfs(self, start_vertex):
        with self.lock:
            if start_vertex not in self.graph:
                raise KeyError(f"Vertex '{start_vertex}' does not exist in the graph.")
            
            visited = set()
            queue = deque([start_vertex])
            result = []

            while queue:
                vertex = queue.popleft()
                if vertex not in visited:
                    visited.add(vertex)
                    result.append(vertex)
                    queue.extend(v for v in self.graph[vertex] if v not in visited)

            return result
    
    def dfs(self, start_vertex):
        with self.lock:
            if start_vertex not in self.graph:
                raise KeyError(f"Vertex '{start_vertex}' does not exist in the graph.")
            
            visited = set()
            stack = [start_vertex]
            result = []

            while stack:
                vertex = stack.pop()
                if vertex not in visited:
                    visited.add(vertex)
                    result.append(vertex)
                    stack.extend(v for v in reversed(self.graph[vertex]) if v not in visited)

            return result
    
    def __str__(self):
        with self.lock:
            return str(self.graph)

# Example usage:
try:
    g = Graph(directed=False)
    g.add_vertex('A')
    g.add_vertex('B')
    g.add_vertex('C')
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    g.add_edge('B', 'C')
    
    print("BFS:", g.bfs('A'))
    print("DFS:", g.dfs('A'))
except Exception as e:
    print(f"Error: {e}")