import heapq

def misplaced_tiles(state, goal):
    count = 0

    for i in range(9):
        if state[i] != 0 and state[i] != goal[i]:
            count += 1

    return count


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


def print_puzzle(state):
    for i in range(0, 9, 3):
        print(state[i:i + 3])
    print()


def a_star(start, goal):

    priority_queue = []

    g = 0
    h = misplaced_tiles(start, goal)
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
            new_h = misplaced_tiles(next_state, goal)
            new_f = new_g + new_h

            new_path = path + [
                (next_state, move, new_g, new_h, new_f)
            ]

            heapq.heappush(
                priority_queue,
                (new_f, new_g, next_state, new_path)
            )

    return None, -1


print("8-PUZZLE A* SEARCH")
print("Heuristic: Misplaced Tiles")

print("\nEnter Initial State")
print("Use 0 for blank space")

start = []

for i in range(3):
    row = list(map(int, input().split()))
    start.extend(row)

start = tuple(start)

print("\nEnter Goal State")
print("Use 0 for blank space")

goal = []

for i in range(3):
    row = list(map(int, input().split()))
    goal.extend(row)

goal = tuple(goal)

print("\nInitial State:")
print_puzzle(start)

print("Goal State:")
print_puzzle(goal)

path, cost = a_star(start, goal)

if path is None:

    print("No solution found.")

else:

    print("Solution Found!")
    print("Total Cost / Depth:", cost)
    print("Heuristic: Misplaced Tiles")

    initial_g = 0
    initial_h = misplaced_tiles(start, goal)
    initial_f = initial_g + initial_h

    print("\nStep 0")
    print("Initial State:")
    print_puzzle(start)

    print("g =", initial_g,"h =", initial_h,"f =", initial_f)

    for i, (state, move, g, h, f) in enumerate(path):

        print("\nStep", i + 1)
        print("Move:", move)
        print_puzzle(state)

        print("g =", initial_g,"h =", initial_h,"f =", initial_f)


    print("\nGoal Reached!")
    print("Total Moves:", cost)
