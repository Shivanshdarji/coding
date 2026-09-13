def kruskal(graph):
    parent = {}
    rank = {}

    def find(u):
        while parent[u] != u:
            parent[u] = parent[parent[u]]
            u = parent[u]
        return u

    def union(u, v):
        root_u = find(u)
        root_v = find(v)
        if root_u == root_v:
            return False
        if rank[root_u] < rank[root_v]:
            parent[root_u] = root_v
        else:
            parent[root_v] = root_u
            if rank[root_u] == rank[root_v]:
                rank[root_u] += 1
        return True

    edges = []
    for u in graph:
        for v, w in graph[u]:
            if (v, u, w) not in edges:
                edges.append((u, v, w))

    for node in graph:
        parent[node] = node
        rank[node] = 0

    edges.sort(key=lambda x: x[2])
    total_cost = 0
    mst_edges = []
    visited_nodes = []

    for u, v, w in edges:
        if union(u, v):
            mst_edges.append((u, v, w))
            total_cost += w
            if u not in visited_nodes:
                visited_nodes.append(u)
            if v not in visited_nodes:
                visited_nodes.append(v)

    return total_cost, visited_nodes, mst_edges

graph = {
    'E': [('F', 2), ('G', 3)],
    'F': [('E', 2), ('G', 1), ('H', 4)],
    'G': [('E', 3), ('F', 1), ('H', 5)],
    'H': [('F', 4), ('G', 5)]
}

cost, visited_nodes, mst = kruskal(graph)
print("Shivansh\n230410107124")
print("Total Cost:", cost)
print("Visited Nodes:", visited_nodes)
print("MST Edges:", mst)
