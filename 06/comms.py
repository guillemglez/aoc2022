from pathlib import Path
from typing import Final


def comms(input: Path) -> None:
    stream: Final = input.open("r").readlines()[0].strip()

    cursor = 0
    packet: list[str] = []
    while True:
        char = stream[cursor]
        cursor += 1

        if len(packet) < 4:
            packet.append(char)
            continue

        packet.pop(0)
        packet.append(char)

        if len(set(packet)) == 4:
            print(f"Start-of-packet is found at {cursor}")
            break


if __name__ == "__main__":
    comms(Path(__file__).parent / "input")
