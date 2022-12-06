from pathlib import Path
from typing import NewType

Elf = NewType("Elf", list[int])


def calories(input: Path) -> None:
    elves: list[Elf] = [Elf([])]
    with input.open("r") as f:
        for line in f:
            if len(line.strip()):
                elves[-1].append(int(line.strip()))
            else:
                elves.append(Elf([]))

    calories = [sum(elf) for elf in elves]
    print(f"The elf carrying the most calories is carrying {max(calories)} calories")


if __name__ == "__main__":
    calories(Path(__file__).parent / "input")
