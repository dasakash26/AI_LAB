from collections import deque

def get_next_states(jug1, jug2, cap1, cap2):
    states = []
    states.append((cap1, jug2))
    states.append((jug1, cap2))
    states.append((0, jug2))
    states.append((jug1, 0))
    pour = min(jug1, cap2 - jug2)
    states.append((jug1 - pour, jug2 + pour))
    pour = min(jug2, cap1 - jug1)
    states.append((jug1 + pour, jug2 - pour))
    return states

def bfs_water_jug(cap1, cap2, target):
    start = (0, 0)
    queue = deque([start])
    visited = set([start])
    parent = {start: None}

    while queue:
        jug1, jug2 = queue.popleft()

        if jug1 == target:
            path = []
            while True:
                path.append((jug1, jug2))
                prev = parent[(jug1, jug2)]
                if prev is None:
                    break
                jug1, jug2 = prev
            path.reverse()
            return path

        for next_state in get_next_states(jug1, jug2, cap1, cap2):
            if next_state not in visited:
                visited.add(next_state)
                parent[next_state] = (jug1, jug2)
                queue.append(next_state)

    return None

def print_solution(path):
    if not path:
        print("No solution found.")
        return
    print("Steps to measure target:")
    for i, (jug1, jug2) in enumerate(path):
        print(f"Step {i}: Jug1 = {jug1}L, Jug2 = {jug2}L")

def main():
    capacity_4_liter = 4
    capacity_3_liter = 3
    target_liters = 2

    solution = bfs_water_jug(capacity_4_liter, capacity_3_liter, target_liters)
    print_solution(solution)

main()