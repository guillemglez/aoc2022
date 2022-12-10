from pathlib import Path
from typing import Final
import numpy as np


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
    with np.nditer(grid, flags=["multi_index"], op_flags=["readonly"]) as it:
        for height in it:
            r, c = it.multi_index
            if r == 0 or c == 0 or r == maxr or c == maxc:  # border
                visible += 1
                continue

            for view in (grid[:r, c], grid[r + 1 :, c], grid[r, :c], grid[r, c + 1 :]):
                if view.max() < height:
                    visible += 1
                    break

    print(f"The number of trees visible from outside the grid is {visible}")


if __name__ == "__main__":
    trees(Path(__file__).parent / "input")
