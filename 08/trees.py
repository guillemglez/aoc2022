from pathlib import Path
from typing import Final
import numpy as np
import math


def trees(input: Path) -> None:
    grid = np.array([])

    # make grid
    with input.open("r") as f:
        for line_raw in f:
            line = line_raw.strip()

            if not len(line):  # empty line
                continue

            row = [int(t) for t in line]
            if grid.size == 0:  # first line
                grid = np.array(row)
                continue

            grid = np.vstack([grid, row])

    maxr: Final = grid.shape[0] - 1
    maxc: Final = grid.shape[1] - 1
    visible = 0
    max_scenic_score = 0
    with np.nditer(grid, flags=["multi_index"], op_flags=["readonly"]) as it:
        for height in it:
            r, c = it.multi_index
            if r == 0 or c == 0 or r == maxr or c == maxc:  # border
                visible += 1
                continue

            views: list[int] = [0, 0, 0, 0]
            vis = False
            for v, view in enumerate(
                (
                    np.flipud(grid[:r, c]),
                    grid[r + 1 :, c],
                    np.flipud(grid[r, :c].T),
                    grid[r, c + 1 :],
                )
            ):
                if view.max() < height:
                    vis = True

                for t in view:
                    views[v] += 1
                    if t >= height:
                        break

            visible += 1 if vis else 0
            scenic_score = math.prod(views)
            max_scenic_score = max([scenic_score, max_scenic_score])

    print(f"The number of trees visible from outside the grid is {visible}")
    print(f"The highest scenic score is {max_scenic_score}")


if __name__ == "__main__":
    trees(Path(__file__).parent / "input")
