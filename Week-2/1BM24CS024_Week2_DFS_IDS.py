class EightPuzzle:

    def __init__(self, initial):
        self.initial = tuple(initial)
        self.goal = (0, 1, 2,
                     3, 4, 5,
                     6, 7, 8)

    def getMoves(self, state):
        blank = state.index(0)
        row = blank // 3
        col = blank % 3

        moves = []

        if row > 0:
            moves.append(blank - 3)

        if row < 2:
            moves.append(blank + 3)

        if col > 0:
            moves.append(blank - 1)

        if col < 2:
            moves.append(blank + 1)

        return moves

    def makeMove(self, state, position):
        blank = state.index(0)

        newState = list(state)
        newState[blank], newState[position] = \
            newState[position], newState[blank]

        return tuple(newState)

    def depthLimitedDFS(self, state, depth, path, visited):

        if state == self.goal:
            return path

        if depth == 0:
            return None

        visited.add(state)

        for move in self.getMoves(state):

            newState = self.makeMove(state, move)

            if newState not in visited:

                result = self.depthLimitedDFS(
                    newState,
                    depth - 1,
                    path + [newState],
                    visited
                )

                if result:
                    return result

        visited.remove(state)

        return None

    def printSolution(self, solution):

        for start in range(0, len(solution), 8):

            group = solution[start:start + 8]

            for row in range(3):

                for state in group:

                    print(
                        state[row * 3],
                        state[row * 3 + 1],
                        state[row * 3 + 2],
                        end="       "
                    )

                print()

            print()

    def DFS(self):

        print("\nDFS Solution:")

        for depth in range(25):

            solution = self.depthLimitedDFS(
                self.initial,
                depth,
                [self.initial],
                set()
            )

            if solution:

                self.printSolution(solution)

                print("Number of moves:", len(solution) - 1)
                return

        print("No solution found.")

    def IDS(self):

        print("\nIDS Solution:")

        for depth in range(25):

            solution = self.depthLimitedDFS(
                self.initial,
                depth,
                [self.initial],
                set()
            )

            if solution:

                self.printSolution(solution)

                print("Depth:", depth)
                print("Number of moves:", len(solution) - 1)
                return

        print("No solution found.")


while True:

    try:

        values = list(map(int, input(
            "Enter initial state (9 numbers, use 0 for blank): "
        ).split()))

        if len(values) != 9:
            print("Enter exactly 9 numbers.")
            continue

        if set(values) != set(range(9)):
            print("Enter numbers from 0 to 8 without repetition.")
            continue

        break

    except ValueError:
        print("Invalid input. Enter numbers only.")


puzzle = EightPuzzle(values)

print("\nInitial State:")
print("5 4 0")
print("6 1 8")
print("7 3 2")

print("\nGoal State:")
print("0 1 2")
print("3 4 5")
print("6 7 8")

puzzle.DFS()
puzzle.IDS()
