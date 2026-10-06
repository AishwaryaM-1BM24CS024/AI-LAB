import heapq


def manhattan_distance(state, goal):
    distance = 0

    for i in range(9):
        tile = state[i]

        if tile != 0:
            current_row = i // 3
            current_col = i % 3

            goal_index = goal.index(tile)

            goal_row = goal_index // 3
            goal_col = goal_index % 3

            distance += abs(current_row - goal_row)
            distance += abs(current_col - goal_col)

    return distance


def get_neighbors(state):
    neighbors = []

    blank = state.index(0)

    row = blank // 3
    col = blank % 3

    moves = [
        (-1, 0, "Up"),
        (1, 0, "Down"),
        (0, -1, "Left"),
        (0, 1, "Right")
    ]

    for dr, dc, move in moves:

        new_row = row + dr
        new_col = col + dc

        if 0 <= new_row < 3 and 0 <= new_col < 3:

            new_blank = new_row * 3 + new_col

            new_state = list(state)

            new_state[blank], new_state[new_blank] = \
                new_state[new_blank], new_state[blank]

            neighbors.append((tuple(new_state), move))

    return neighbors


def a_star(start, goal):

    priority_queue = []

    g = 0
    h = manhattan_distance(start, goal)
    f = g + h

    heapq.heappush(
        priority_queue,
        (f, g, start, [])
    )

    visited = set()

    while priority_queue:

        f, g, current, path = heapq.heappop(priority_queue)

        if current in visited:
            continue

        visited.add(current)

        if current == goal:
            return path, g

        for next_state, move in get_neighbors(current):

            if next_state in visited:
                continue

            new_g = g + 1
            new_h = manhattan_distance(next_state, goal)
            new_f = new_g + new_h

            new_path = path + [
                (next_state, move, new_g, new_h, new_f)
            ]

            heapq.heappush(
                priority_queue,
                (new_f, new_g, next_state, new_path)
            )

    return None, -1


def print_three_states(states):
    width = 18

    for row in range(3):
        line = ""

        for state in states:
            values = state[0][row * 3:row * 3 + 3]

            line += " ".join(map(str, values)).ljust(width)

        print(line)


def print_steps(path, start, goal):

    all_states = []

    initial_g = 0
    initial_h = manhattan_distance(start, goal)
    initial_f = initial_g + initial_h

    all_states.append(
        (start, "Start", initial_g, initial_h, initial_f)
    )

    for state, move, g, h, f in path:
        all_states.append(
            (state, move, g, h, f)
        )

    for i in range(0, len(all_states), 3):

        group = all_states[i:i + 3]

        print()

        for j, item in enumerate(group):
            print(
                f"Step {i + j}".ljust(18),
                end=""
            )

        print()

        for row in range(3):

            for state, move, g, h, f in group:

                values = state[row * 3:row * 3 + 3]

                print(
                    (" ".join(map(str, values))).ljust(18),
                    end=""
                )

            print()

        for state, move, g, h, f in group:

            print(
                f"g={g} h={h} f={f}".ljust(18),
                end=""
            )

        print()


print("====================================")
print("8-PUZZLE A* - MANHATTAN DISTANCE")
print("====================================")

print("\nEnter initial state (0 represents blank):")

start = []

for i in range(3):
    row = list(map(int, input().split()))
    start.extend(row)

start = tuple(start)

print("\nEnter goal state (0 represents blank):")

goal = []

for i in range(3):
    row = list(map(int, input().split()))
    goal.extend(row)

goal = tuple(goal)

path, cost = a_star(start, goal)

if path is None:

    print("\nNo solution found.")

else:

    print("\nSolution Found!")
    print("Total Cost / Depth:", cost)
    print("Heuristic: Manhattan Distance")

    print_steps(path, start, goal)

    print("\nGoal Reached!")
    print("Total Moves:", cost)
