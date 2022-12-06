from pathlib import Path
from typing import Final, NamedTuple
import enum


class Move(enum.Enum):
    Rock = enum.auto()
    Paper = enum.auto()
    Scissors = enum.auto()


class Outcome(enum.Enum):
    Win = enum.auto()
    Lose = enum.auto()
    Draw = enum.auto()


class Round(NamedTuple):
    p1: Move
    p2: Move
    outcome: Outcome


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
    outcome_map: Final = {
        "X": Outcome.Lose,
        "Y": Outcome.Draw,
        "Z": Outcome.Win,
    }
    scores_map: Final = {
        Move.Rock: 1,
        Move.Paper: 2,
        Move.Scissors: 3,
        Outcome.Win: 6,
        Outcome.Draw: 3,
        Outcome.Lose: 0,
    }

    game: list[Round] = []
    with input.open("r") as f:
        for line in f:
            move_p1 = p1_map[line[0]]
            move_p2 = p2_map[line.strip()[-1]]
            outcome = outcome_map[line.strip()[-1]]
            round = Round(p1=move_p1, p2=move_p2, outcome=outcome)
            game.append(round)

    score1, score2 = 0, 0
    for round in game:
        score1 += scores_map[round.p2]
        score2 += scores_map[round.outcome]

        # Part one
        if round.p1 == round.p2:  # Draw
            score1 += scores_map[Outcome.Draw]
        elif (
            (round.p1 == Move.Paper and round.p2 == Move.Scissors)
            or (round.p1 == Move.Scissors and round.p2 == Move.Rock)
            or (round.p1 == Move.Rock and round.p2 == Move.Paper)
        ):  # Win
            score1 += scores_map[Outcome.Win]
        else:  # lose
            score1 += scores_map[Outcome.Lose]

        # Part two
        if round.outcome == Outcome.Draw:
            score2 += scores_map[round.p1]
        elif round.p1 == Move.Paper:
            score2 += scores_map[
                Move.Scissors if round.outcome == Outcome.Win else Move.Rock
            ]
        elif round.p1 == Move.Scissors:
            score2 += scores_map[
                Move.Rock if round.outcome == Outcome.Win else Move.Paper
            ]
        elif round.p1 == Move.Rock:
            score2 += scores_map[
                Move.Paper if round.outcome == Outcome.Win else Move.Scissors
            ]

    print(f"The score is {score1} according to us")
    print(f"The score is {score2} when following the Elf's instructions")


if __name__ == "__main__":
    rock_paper_scissors(Path(__file__).parent / "input")
