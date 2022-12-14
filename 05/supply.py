from pathlib import Path
import copy


def supply(input: Path) -> None:
    supplies: list[list[str]] = []
    ops: list[tuple[int, int, int]] = []
    with input.open("r") as f:
        # Parse stacks
        for line_raw in f:
            if len(supplies) == 0:
                # first pass, check how many stacks
                number_of_stacks = (len(line_raw)) // 4
                supplies = [[] for s in range(number_of_stacks)]

            if line_raw[1] == "1":
                # done parsing crates
                break

            for s in range(len(supplies)):
                content = line_raw[s * 4 + 1]
                if content.isalpha():
                    # has a container
                    supplies[s].append(content)

        # reverse containers
        for s in range(len(supplies)):
            supplies[s].reverse()

        # parse operations
        for line_raw in f:
            # expect empty lines
            if len(line_raw) == 1:
                continue

            split = line_raw.split()
            ops.append((int(split[1]), int(split[3]), int(split[5])))

    # Create copy for CM 9001
    supplies_cm_9001 = copy.deepcopy(supplies)

    # perform processing
    for op in ops:
        times, frm, to = op
        for n in range(times):
            supplies[to - 1].append(supplies[frm - 1].pop())
            supplies_cm_9001[to - 1].append(supplies_cm_9001[frm - 1][-times + n])

        # empty moved crates in CM 9001 version
        [supplies_cm_9001[frm - 1].pop() for n in range(times)]

    top_crates = [stack.pop() for stack in supplies]
    top_crates_cm_9001 = [stack.pop() for stack in supplies_cm_9001]
    print(f"Give the Elves the message {''.join(top_crates)}")
    print(
        f"Give the Elves the message {''.join(top_crates_cm_9001)} as they use the CrateMover 9001"
    )


if __name__ == "__main__":
    supply(Path(__file__).parent / "input")
