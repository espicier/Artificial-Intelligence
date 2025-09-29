from enum import Enum
import copy
import heapq
import time, random
from itertools import count

ENDING_STATE: list = [[1, 2, 3],
                      [8, 0, 4],
                      [7, 6, 5]]


class Move(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


def find_blank(grid, k):
    for i in range(k):
        for j in range(k):
            if grid[i][j] == 0:
                return (i, j)
    return None


def h(grid: list, k: int) -> int:
    """Heuristique : tuiles mal placées (admissible)."""
    n: int = 0
    for i in range(k):
        for j in range(k):
            if grid[i][j] != 0 and grid[i][j] != ENDING_STATE[i][j]:
                n += 1
    return n


def get_possible_moves(grid: list, blank_pos: tuple, k: int) -> list:
    x, y = blank_pos
    possible_moves = []

    if x > 0:
        new_grid = copy.deepcopy(grid)
        new_grid[x][y] = new_grid[x - 1][y]
        new_grid[x - 1][y] = 0
        possible_moves.append((new_grid, (x - 1, y), Move.UP))

    if x < k - 1:
        new_grid = copy.deepcopy(grid)
        new_grid[x][y] = new_grid[x + 1][y]
        new_grid[x + 1][y] = 0
        possible_moves.append((new_grid, (x + 1, y), Move.DOWN))

    if y > 0:
        new_grid = copy.deepcopy(grid)
        new_grid[x][y] = new_grid[x][y - 1]
        new_grid[x][y - 1] = 0
        possible_moves.append((new_grid, (x, y - 1), Move.LEFT))

    if y < k - 1:
        new_grid = copy.deepcopy(grid)
        new_grid[x][y] = new_grid[x][y + 1]
        new_grid[x][y + 1] = 0
        possible_moves.append((new_grid, (x, y + 1), Move.RIGHT))

    return possible_moves


def grid_to_tuple(grid):
    return tuple(tuple(row) for row in grid)


def best_first_stats(grid: list, k: int):
    start = time.perf_counter()
    blank_pos = find_blank(grid, k)
    initial_h = h(grid, k)
    open_list = [(initial_h, 0, grid, blank_pos, [])]
    closed_set = set()
    grid_id = 1
    expanded = 0  # pour compter le nombre de noeuds

    while open_list:
        _, _, current_grid, current_blank, moves = heapq.heappop(open_list)
        expanded += 1

        if h(current_grid, k) == 0:
            return moves, expanded, time.perf_counter() - start

        grid_tuple = grid_to_tuple(current_grid)
        if grid_tuple in closed_set:
            continue
        closed_set.add(grid_tuple)

        for new_grid, new_blank, move in get_possible_moves(current_grid,
                                                            current_blank, k):
            new_grid_tuple = grid_to_tuple(new_grid)
            if new_grid_tuple not in closed_set:
                new_h = h(new_grid, k)
                heapq.heappush(open_list,
                               (new_h, grid_id, new_grid, new_blank,
                                moves + [move]))
                grid_id += 1

    return None, expanded, time.perf_counter() - start


def astar_stats(grid: list, k: int):
    blank_pos = find_blank(grid, k)
    start = time.perf_counter()
    tie = count()
    open_list = [(h(grid, k), next(tie), 0, grid, blank_pos, [])]
    best_g = {grid_to_tuple(grid): 0}
    expanded = 0

    while open_list:
        f, _, g, current_grid, current_blank, path = heapq.heappop(open_list)
        expanded += 1

        if h(current_grid, k) == 0:
            return path, expanded, time.perf_counter() - start

        for new_grid, new_blank, mv in get_possible_moves(current_grid,
                                                          current_blank, k):
            state = grid_to_tuple(new_grid)
            new_g = g + 1
            if state not in best_g or new_g < best_g[state]:
                best_g[state] = new_g
                new_f = new_g + h(new_grid, k)
                # heapq = file de priorité
                heapq.heappush(open_list,
                               (new_f, next(tie), new_g, new_grid,
                                new_blank, path + [mv]))

    return None, expanded, time.perf_counter() - start


def print_solution(grid, moves):
    if not moves:
        print("No solution found!")
        return

    print("Initial state:")
    for row in grid:
        print(row)

    current_grid = copy.deepcopy(grid)
    blank_pos = find_blank(current_grid, len(grid))

    for i, move in enumerate(moves):
        print(f"\nStep {i + 1}: Move {move.value}")

        x, y = blank_pos
        if move == Move.UP:
            current_grid[x][y] = current_grid[x - 1][y]
            current_grid[x - 1][y] = 0
            blank_pos = (x - 1, y)
        elif move == Move.DOWN:
            current_grid[x][y] = current_grid[x + 1][y]
            current_grid[x + 1][y] = 0
            blank_pos = (x + 1, y)
        elif move == Move.LEFT:
            current_grid[x][y] = current_grid[x][y - 1]
            current_grid[x][y - 1] = 0
            blank_pos = (x, y - 1)
        elif move == Move.RIGHT:
            current_grid[x][y] = current_grid[x][y + 1]
            current_grid[x][y + 1] = 0
            blank_pos = (x, y + 1)

        for row in current_grid:
            print(row)


def random_puzzle(k: int, scramble: int = 40) -> list:
    """On crér une disposition random des tuiles"""
    grid = [row[:] for row in ENDING_STATE]  # copie profonde
    blank = find_blank(grid, k)
    for _ in range(scramble):
        moves = get_possible_moves(grid, blank, k)
        grid, blank, _ = random.choice(moves)
    return grid


def benchmark(samples: int = 20, scramble: int = 40, k: int = 3):
    print(f"\n=== Benchmark sur {samples} puzzles aléatoires "
          f"(scramble={scramble}) ===")
    print("Idx |  Algo   | path | nodes |  temps (s)")
    print("-" * 44)

    mean_path_a = mean_path_b = 0.0
    mean_nodes_a = mean_nodes_b = 0.0
    mean_time_a = mean_time_b = 0.0

    for idx in range(1, samples + 1):
        puzzle = random_puzzle(k, scramble)

        path_b, nodes_b, t_b = best_first_stats(puzzle, k)
        path_a, nodes_a, t_a = astar_stats(puzzle, k)

        len_b = len(path_b) if path_b else 0
        len_a = len(path_a) if path_a else 0

        print(f"{idx:>3} | Greedy | {len_b:>4} | {nodes_b:>6} | {t_b:>8.4f}")
        print(f"    |   A*   | {len_a:>4} | {nodes_a:>6} | {t_a:>8.4f}")
        print("-" * 44)

        mean_path_a += len_a
        mean_path_b += len_b
        mean_nodes_a += nodes_a
        mean_nodes_b += nodes_b
        mean_time_a += t_a
        mean_time_b += t_b

    # moyennes
    mean_path_a /= samples
    mean_path_b /= samples
    mean_nodes_a /= samples
    mean_nodes_b /= samples
    mean_time_a /= samples
    mean_time_b /= samples

    print("\n======= RÉSUMÉ MOYEN =======")
    print("            |  path | nodes |  temps (s)")
    print("----------------------------")
    print(f"A*      --->| {mean_path_a:>5.2f} | {mean_nodes_a:>6.2f} | {mean_time_a:>9.4f}")
    print(f"Greedy  --->| {mean_path_b:>5.2f} | {mean_nodes_b:>6.2f} | {mean_time_b:>9.4f}")
    print("----------------------------")


def main():
    input_grid: list = [
        [2, 8, 3],
        [1, 6, 4],
        [7, 0, 5],
    ]

    benchmark()


if __name__ == '__main__':
    main()
