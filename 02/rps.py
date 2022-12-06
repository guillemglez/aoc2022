from pathlib import Path
from typing import Final, NamedTuple
import enum


class Move(enum.Enum):
    Rock = enum.auto()
    Paper = enum.auto()
    Scissors = enum.auto()


class Round(NamedTuple):
    p1: Move
    p2: Move


def rock_paper_scissors(input: Path) -> None:
    p1_map: Final = {
        "A": Move.Rock,
        "B": Move.Paper,
        "C": Move.Scissors,
    }
    p2_map: Final = {
        "X": Move.Rock,
        "Y": Move.Paper,
        "Z": Move.Scissors,
    }
    scores_map: Final = {
        Move.Rock: 1,
        Move.Paper: 2,
        Move.Scissors: 3,
    }

    game: list[Round] = []
    with input.open("r") as f:
        for line in f:
            move_p1 = p1_map[line[0]]
            move_p2 = p2_map[line.strip()[-1]]
            round = Round(p1=move_p1, p2=move_p2)
            game.append(round)

    score = 0
    for round in game:
        score += scores_map[round.p2]
        if round.p1 == round.p2:
            score += 3
            continue
        if (
            (round.p1 == Move.Paper and round.p2 == Move.Scissors)
            or (round.p1 == Move.Scissors and round.p2 == Move.Rock)
            or (round.p1 == Move.Rock and round.p2 == Move.Paper)
        ):
            score += 6

    print(f"The score is {score}")


if __name__ == "__main__":
    rock_paper_scissors(Path(__file__).parent / "input")
