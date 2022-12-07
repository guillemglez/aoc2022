from pathlib import Path


def cleanup(input: Path) -> None:
    occurrences = 0
    with input.open("r") as f:
        for line in f:
            assignements = [
                assignement.split("-") for assignement in line.strip().split(",")
            ]
            pair = (
                (int(assignements[0][0]), int(assignements[0][1])),
                (int(assignements[1][0]), int(assignements[1][1])),
            )
            second_in_first = (pair[0][0] <= pair[1][0]) == (pair[0][1] >= pair[1][1])
            first_in_second = (pair[0][0] >= pair[1][0]) == (pair[0][1] <= pair[1][1])
            if second_in_first or first_in_second:
                occurrences += 1

    print(f"{occurrences} pairs contain fully contained ranges.")


if __name__ == "__main__":
    cleanup(Path(__file__).parent / "input")
