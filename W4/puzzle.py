def read_input(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    N = int(lines[0])
    start = []
    goal = []
    for i in range(1, N + 1):
        start.extend(map(int, lines[i].split()))
    for i in range(N + 1, 2 * N + 1):
        goal.extend(map(int, lines[i].split()))
    return N, tuple(start), tuple(goal)

def get_neighbors(state, N):
    moves = []
    zero_index = state.index(0)
    x, y = divmod(zero_index, N)

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < N and 0 <= ny < N:
            new_index = nx * N + ny
            new_state = list(state)
            new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
            moves.append(tuple(new_state))
    return moves

def print_state(state, N):
    for i in range(N):
        print(" ".join(str(x) if x != 0 else "_" for x in state[i*N:(i+1)*N]))
    print()

def dfs(start, goal, N, output_file):
    stack = [(start, [start])]
    visited = set()

    while stack:
        state, path = stack.pop()

        with open(output_file, "a") as f:
            f.write(f"Step {len(path)-1}:\n")
            for i in range(N):
                f.write(" ".join(str(x) if x != 0 else "_" for x in state[i*N:(i+1)*N]) + "\n")
            f.write("\n")

        if state == goal:
            return path

        if state in visited:
            continue

        visited.add(state)

        for neighbor in get_neighbors(state, N):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))

    return None

if __name__ == "__main__":
    input_file = "input.txt"
    output_file = "output.txt"

    N, start, goal = read_input(input_file)

    open(output_file, "w").close()

    print("Start State:")
    print_state(start, N)
    print("Goal State:")
    print_state(goal, N)

    path = dfs(start, goal, N, output_file)

    if path:
        print(f"Solution found in {len(path)-1} moves!")
        with open(output_file, "a") as f:
            f.write(f"Solution found in {len(path)-1} moves!\n")
    else:
        print("No solution found.")
        with open(output_file, "a") as f:
            f.write("No solution found.\n")