from pathlib import Path
import enum
from typing import Final, Self


# type for a coordinate position (x,y)
Position = tuple[int, int]


class Direction(enum.Enum):
    Left = enum.auto()
    Right = enum.auto()
    Up = enum.auto()
    Down = enum.auto()

    @staticmethod
    def from_string(string: str) -> Self:
        match string:
            case "L":
                return Direction.Left
            case "R":
                return Direction.Right
            case "U":
                return Direction.Up
            case "D":
                return Direction.Down

        raise ValueError(f"Got {string}?")


def move(init: Position, direction: Self) -> Position:
    """
    Move a position towards a given direction and return the resulting position
    """
    x, y = init
    match direction:
        case Direction.Left:
            return x - 1, y
        case Direction.Right:
            return x + 1, y
        case Direction.Up:
            return x, y + 1
        case Direction.Down:
            return x, y - 1
    raise ValueError(f"Got {direction}?")


def react(head: Position, tail: Position) -> Position:
    """
    Position tail would result in given a head and tail positions
    """
    diff_x: Final = head[0] - tail[0]
    diff_y: Final = head[1] - tail[1]

    # if adjacent, return current pos (does not move)
    if abs(diff_x) <= 1 and abs(diff_y) <= 1:
        return tail

    direction_x: Final = Direction.Left if diff_x < 0 else Direction.Right
    direction_y: Final = Direction.Down if diff_y < 0 else Direction.Up

    if diff_x == 0:  # moves vertically
        return move(tail, direction_y)
    elif diff_y == 0:  # moves horizontally
        return move(tail, direction_x)
    else:  # moves diagonally
        return move(move(tail, direction_x), direction_y)


def rope(input: Path) -> None:
    # parse commands
    commands: list[tuple[Direction, int]] = []
    with input.open("r") as f:
        for line_raw in f:
            command_raw = line_raw.strip().split()
            if len(command_raw) != 2:
                continue

            direction_raw = command_raw[0]
            steps_raw = command_raw[1]
            direction = Direction.from_string(direction_raw)
            steps = int(steps_raw)
            commands.append((direction, steps))

    # compute path
    tail: list[Position] = [(0, 0)]
    head: list[Position] = [(0, 0)]
    for direction, steps in commands:
        for s in range(steps):
            new_head = move(head[-1], direction)
            head.append(new_head)
            tail.append(react(new_head, tail[-1]))

    print(f"The tail of the rope visited {len(set(tail))} different positions.")

    # Part two
    knots: list[list[Position]] = [[(0, 0)] for knot in range(10)]
    for direction, steps in commands:
        for s in range(steps):
            for k, knot in enumerate(knots):
                if k == 0:  # head
                    knot.append(move(knot[-1], direction))
                else:  # other
                    front = knots[k - 1][-1]
                    knot.append(react(front, knot[-1]))

    print(
        f"The tail of the rope with 10 knots visited {len(set(knots[-1]))} different positions."
    )


if __name__ == "__main__":
    rope(Path(__file__).parent / "input")
