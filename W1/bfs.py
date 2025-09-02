def bfs(adj, start):
    n = len(adj)
    vis = [False] * n
    q = [start]
    vis[start] = True
    print("BFS: ", end="")

    while len(q):
        node = q.pop(0)
        print(node, end=", ")

        for nbr in adj[node]:
            if not vis[nbr]:
                q.append(nbr)
                vis[nbr] = True

def main():
    n = int(input("Enter the number of nodes: "))
    adj = [[] for _ in range(n)]

    print("Enter the edges in the format: node1 node2")
    for _ in range(int(input("Enter number of edges: "))):
        u, v = map(int, input().split())

        adj[u].append(v)
        adj[v].append(u)

    start_node = int(input("Enter the starting node for BFS: "))

    bfs(adj, start_node)

main()
