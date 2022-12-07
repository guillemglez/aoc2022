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
    uniques: list[set[str]] = []
    priorities: list[int] = []

    with input.open("r") as f:
        for line in f:
            line = line.strip()
            assert len(line) % 2 == 0
            nb_items = len(line) // 2

            uniques.append(set(line))
            items = line[:nb_items], line[nb_items:]
            unique = set(items[0]), set(items[1])
            for item in unique[0]:
                if item in unique[1]:
                    priorities.append(priority(item))

    stickers: list[str] = []
    for group in range(len(uniques) // 3):
        rucksacks = uniques[group * 3 : group * 3 + 3]
        content = ["".join(list(items)) for items in rucksacks]
        overview: dict[str, int] = {}
        for item in "".join(content):
            if item not in overview.keys():
                overview[item] = 1
            else:
                overview[item] += 1

        for item, times in overview.items():
            if times == 3:
                stickers.append(item)
                break

    print(f"The sum of priorities for the repeated items is {sum(priorities)}")
    print(
        f"The sum of priorities for the stickers is {sum([priority(s) for s in stickers])}"
    )


if __name__ == "__main__":
    rucksack(Path(__file__).parent / "input")
