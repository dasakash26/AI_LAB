import json
import glob
import time
import tracemalloc
from collections import deque
import heapq
import matplotlib.pyplot as plt

class State:
    def __init__(self, m, c, boat):
        self.m, self.c, self.boat = m, c, boat

    def is_valid(self):
        ml, cl = self.m, self.c
        mr, cr = total_m - ml, total_c - cl
        return (0 <= ml <= total_m and 0 <= cl <= total_c
                and (ml == 0 or ml >= cl)
                and (mr == 0 or mr >= cr))

    def is_goal(self):
        return self.m == 0 and self.c == 0 and self.boat == goal_boat

    def successors(self):
        for dm, dc in moves:
            m2 = self.m - dm if self.boat == 0 else self.m + dm
            c2 = self.c - dc if self.boat == 0 else self.c + dc
            nb = 1 - self.boat
            s = State(m2, c2, nb)
            if s.is_valid():
                yield s

    def __eq__(self, other):
        return (self.m, self.c, self.boat) == (other.m, other.c, other.boat)

    def __hash__(self):
        return hash((self.m, self.c, self.boat))

    def __repr__(self):
        return f"S(m={self.m},c={self.c},boat={'L' if self.boat == 0 else 'R'})"

total_m = total_c = 3
goal_boat = 1
moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]

def reconstruct_path(parent, node):
    path = []
    while node:
        path.append(node)
        node = parent.get(node)
    return list(reversed(path))

def bfs(start):
    frontier, parent = deque([start]), {start: None}
    while frontier:
        node = frontier.popleft()
        if node.is_goal():
            return reconstruct_path(parent, node)
        for nxt in node.successors():
            if nxt not in parent:
                parent[nxt] = node
                frontier.append(nxt)

def dfs(start, depth_limit=None):
    frontier, parent = [(start, 0)], {start: None}
    while frontier:
        node, d = frontier.pop()
        if node.is_goal():
            return reconstruct_path(parent, node)
        if depth_limit is None or d < depth_limit:
            for nxt in node.successors():
                if nxt not in parent:
                    parent[nxt] = node
                    frontier.append((nxt, d + 1))

def ids(start, max_depth):
    for depth in range(max_depth + 1):
        res = dfs(start, depth_limit=depth)
        if res:
            return res

def heuristic(state):
    return state.m + state.c

def ucs(start):
    pq = [(0, start.m, start.c, start.boat, start)]
    parent = {start: None}
    cost_so_far = {start: 0}
    while pq:
        cost, *_, node = heapq.heappop(pq)
        if node.is_goal():
            return reconstruct_path(parent, node)
        for nxt in node.successors():
            new_cost = cost_so_far[node] + heuristic(nxt)
            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                cost_so_far[nxt] = new_cost
                parent[nxt] = node
                heapq.heappush(pq, (new_cost, nxt.m, nxt.c, nxt.boat, nxt))

def ils(start):
    limit = heuristic(start)
    while True:
        path = limited_cost_search(start, limit)
        if path:
            return path
        limit += 1

def limited_cost_search(start, limit):
    pq = [(0, start.m, start.c, start.boat, start)]
    parent = {start: None}
    cost_so_far = {start: 0}
    while pq:
        cost, *_, node = heapq.heappop(pq)
        if node.is_goal():
            return reconstruct_path(parent, node)
        for nxt in node.successors():
            new_cost = cost_so_far[node] + heuristic(nxt)
            if new_cost <= limit and (nxt not in cost_so_far or new_cost < cost_so_far[nxt]):
                cost_so_far[nxt] = new_cost
                parent[nxt] = node
                heapq.heappush(pq, (new_cost, nxt.m, nxt.c, nxt.boat, nxt))

def run_from_file(fname, log_file):
    with open(fname) as f:
        cfg = json.load(f)
    global total_m, total_c, goal_boat
    total_m, total_c = cfg.get("m", 3), cfg.get("c", 3)
    goal_boat = cfg.get("goal_boat", 1)
    initial = cfg["initial_state"]
    depth_limit = cfg.get("depth_limit")
    algs = cfg["search_type"]

    start = State(*initial)
    results = []
    for alg in algs:
        fn_map = {
            "BFS": lambda: bfs(start),
            "DFS": lambda: dfs(start),
            "DLS": lambda: dfs(start, depth_limit),
            "IDS": lambda: ids(start, depth_limit),
            "UCS": lambda: ucs(start),
            "ILS": lambda: ils(start)
        }
        fn = fn_map[alg.upper()]
        tracemalloc.start()
        t0 = time.time()
        path = fn()
        elapsed = time.time() - t0
        _, mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        elapsed_ms = elapsed * 1000
        mem_kb = mem / 1024

        alg_name = alg.upper()
        if alg_name in ["DLS", "IDS"] and depth_limit is not None:
            alg_name += f"_d{depth_limit}"

        # --- LOGGING BLOCK ---
        log_file.write(f"\n--- [{alg_name}] ---\n")
        if path:
            log_file.write(f"Solution found in {len(path) - 1} moves ({len(path)} states).\n")
            log_file.write("Solution Path:\n")
            log_file.write(f"  Start State: {path[0]}\n")
            for i in range(1, len(path)):
                prev_state = path[i-1]
                curr_state = path[i]

                dm = abs(curr_state.m - prev_state.m)
                dc = abs(curr_state.c - prev_state.c)
                direction = "Left to Right" if prev_state.boat == 0 else "Right to Left"

                log_file.write(f"  Step {i}: Move {dm}M, {dc}C {direction}.  -->  New State: {curr_state}\n")
        else:
            log_file.write("No solution found.\n")

        log_file.write(f"\nTime taken: {elapsed_ms:.3f} ms\n")
        log_file.write(f"Memory used: {mem_kb:.2f} KB\n")
        log_file.write("-" * 25 + "\n")

        results.append({
            "alg": alg_name,
            "time": elapsed_ms,
            "memory": mem_kb,
            "steps": len(path) if path else None
        })
    return results

if __name__ == "__main__":
    log_filename = "solve_log.txt"
    with open(log_filename, 'w') as log_file:
        aggregated = []
        for fname in glob.glob("*_input.json"):
            print(f"Running tests from {fname}...")
            log_file.write(f"===== Running tests from {fname} =====\n")
            aggregated.extend(run_from_file(fname, log_file))

    print(f"\nDetailed logs saved to {log_filename}")
    print("Comparison plot saved to comparison_plot.png")

    if not aggregated:
        print("No input files found (e.g., 'test_input.json'). Exiting.")
    else:
        names = [r["alg"] for r in aggregated]
        times = [r["time"] for r in aggregated]
        mems = [r["memory"] for r in aggregated]

        x = range(len(names))
        width = 0.4

        fig, ax1 = plt.subplots(figsize=(12, 7))

        color = 'tab:blue'
        ax1.set_xlabel('Algorithm')
        ax1.set_ylabel('Time (ms)', color=color) # Use ms
        bar1 = ax1.bar([i - width/2 for i in x], times, width, label='Time (ms)', color=color) # Use ms
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.set_xticks(x)
        ax1.set_xticklabels(names, rotation=45, ha='right')

        ax2 = ax1.twinx()

        color = 'tab:orange'
        ax2.set_ylabel('Memory (KB)', color=color) # Use KB
        bar2 = ax2.bar([i + width/2 for i in x], mems, width, label='Memory (KB)', color=color) # Use KB
        ax2.tick_params(axis='y', labelcolor=color)

        plt.title('Algorithm Performance Comparison')
        fig.legend(handles=[bar1, bar2], labels=['Time (ms)', 'Memory (KB)'], loc='upper left', bbox_to_anchor=(0.1, 0.9))

        fig.tight_layout()
        plt.savefig("comparison_plot.png")
        plt.show()