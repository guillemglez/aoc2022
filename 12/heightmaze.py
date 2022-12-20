from pathlib import Path
from typing import Final

# Priority queue which prioritizes nodes with minimum distance
class Queue:
    def __init__(self) -> None:
        self.data: dict[int, list[int]] = {}

    def pop(self) -> int:
        selected = min(self.data.keys())
        node = self.data[selected].pop()
        if len(self.data[selected]) == 0:
            self.data.pop(selected)
        return node

    def push(self, distance: int, node: int) -> None:
        if distance not in self.data.keys():
            self.data[distance] = [node]
        else:
            self.data[distance].append(node)

    def empty(self) -> bool:
        return len(self.data) == 0


# Inverse dijkstra: given an end position, gives all the distances as if it were started from that point    nd
def dijkstra(map: list[int], ncols: int, end_idx: int) -> list[int]:
    # Store edges as a dictionary of nodes which contains per each a list of nodes as a tuple (index, distance)
    edges: list[list[tuple[int, int]]] = [[]] * len(map)
    for index in range(len(map)):
        edges[index] = []
        neighbors = []

        # We store raveled (flattened-like) indexes: check boundaries
        if index - ncols in range(len(map)):
            neighbors.append(index - ncols)
        if index % ncols != 0:
            neighbors.append(index - 1)
        if index + ncols in range(len(map)):
            neighbors.append(index + ncols)
        if (index + 1) % ncols != 0:
            neighbors.append(index + 1)

        for neighbor in neighbors:
            height_diff = map[neighbor] - map[index]
            if (
                height_diff < -1
            ):  # If height is higher than 1 then it's an invalid neighbor
                continue
            edges[index].append((neighbor, 1))

    # Distance from start to end
    distance = [max(map) * len(map)] * len(map)
    distance[end_idx] = 0

    queue = Queue()
    queue.push(0, end_idx)

    processed = [False] * len(map)

    # Dijkstra’s algorithm
    while not queue.empty():
        a = queue.pop()
        if processed[a]:
            continue
        processed[a] = True
        for b, d in edges[a]:
            if distance[a] + d < distance[b]:
                distance[b] = distance[a] + d
                queue.push(distance[b], b)

    return distance


def height_maze(input: Path) -> None:
    maze: list[int] = []
    cols = 0
    start, end = 0, 0
    with input.open("r") as f:
        for line_raw in f:
            line = line_raw.strip()
            if len(line) == 0:
                continue
            if cols == 0:
                cols = len(line)
            assert cols == len(line)

            for char in line:
                if char == "S":
                    start = len(maze)
                    char = "a"
                elif char == "E":
                    end = len(maze)
                    char = "z"

                val = ord(char) - ord("a")
                maze.append(val)

    distances: Final = dijkstra(maze, cols, end)
    print(f"It will take {distances[start]} steps to reach the best signal")

    fewest = distances[start]
    for idx, elevation in enumerate(maze):
        if elevation == 0:
            fewest = min(fewest, distances[idx])
    print(
        f"It will take {fewest} steps to reach the best signal from any square at elevation a"
    )


if __name__ == "__main__":
    height_maze(Path(__file__).parent / "input")
