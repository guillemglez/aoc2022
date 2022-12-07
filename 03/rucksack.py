from pathlib import Path


def priority(char: str) -> int:
    assert char.isalpha()
    assert len(char) == 1

    if char.islower():
        return ord(char) - 96
    else:
        assert char.isupper()
        return ord(char) - 65 + 27


def rucksack(input: Path) -> None:
    priorities: list[int] = []

    with input.open("r") as f:
        for line in f:
            line = line.strip()
            assert len(line) % 2 == 0
            nb_items = len(line) // 2

            items = line[:nb_items], line[nb_items:]
            unique = set(items[0]), set(items[1])
            for item in unique[0]:
                if item in unique[1]:
                    priorities.append(priority(item))

    print(f"The sum of priorities for the repeated items is {sum(priorities)}")


if __name__ == "__main__":
    rucksack(Path(__file__).parent / "input")
