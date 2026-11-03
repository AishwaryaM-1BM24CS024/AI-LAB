from __future__ import annotations

import argparse
import math
import random

BOARD_SIZE = 8


def conflicts(state: list[int]) -> int:
    total = 0
    for col_a in range(BOARD_SIZE):
        for col_b in range(col_a + 1, BOARD_SIZE):
            if abs(state[col_a] - state[col_b]) == col_b - col_a:
                total += 1
    return total


def anneal(
    rng: random.Random,
    initial_temperature: float = 5.0,
    cooling_rate: float = 0.995,
    steps_per_restart: int = 5000,
    restarts: int = 100,
) -> tuple[list[int] | None, int]:
    moves_examined = 0

    for _ in range(restarts):
        state = list(range(BOARD_SIZE))
        rng.shuffle(state)
        energy = conflicts(state)
        temperature = initial_temperature

        for _ in range(steps_per_restart):
            if energy == 0:
                return state, moves_examined

     
            col_a, col_b = rng.sample(range(BOARD_SIZE), 2)
            candidate = state.copy()
            candidate[col_a], candidate[col_b] = candidate[col_b], candidate[col_a]
            candidate_energy = conflicts(candidate)
            delta = candidate_energy - energy
            moves_examined += 1

           
            if delta <= 0 or rng.random() < math.exp(-delta / temperature):
                state, energy = candidate, candidate_energy

            temperature *= cooling_rate

        if energy == 0:
            return state, moves_examined

    return None, moves_examined


def print_board(state: list[int]) -> None:
    for row in range(BOARD_SIZE - 1, -1, -1):
        print(" ".join("Q" if state[col] == row else "." for col in range(BOARD_SIZE)))


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve 8-Queens using simulated annealing.")
    parser.add_argument("--seed", type=int, help="optional random seed for repeatable runs")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    solution, moves = anneal(rng)

    if solution is None:
        print("No solution found within the restart limit. Try running again.")
        return

    print("Solution found (Q = queen, . = empty):")
    print_board(solution)
    print(f"Diagonal conflicts: {conflicts(solution)}")
    print(f"Moves examined: {moves}")
    print(f"Queen rows by column (1-based): {[row + 1 for row in solution]}")


if __name__ == "__main__":
    main()
