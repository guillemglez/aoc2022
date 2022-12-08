from pathlib import Path
from typing import Final


def marker(stream: str, length: int) -> int:
    cursor = 0
    packet: list[str] = []
    while True:
        char = stream[cursor]
        cursor += 1

        if len(packet) < length:
            packet.append(char)
            continue

        packet.pop(0)
        packet.append(char)

        if len(set(packet)) == length:
            return cursor


def comms(input: Path) -> None:
    stream: Final = input.open("r").readlines()[0].strip()

    print(f"Start-of-packet is found at {marker(stream, 4)} when its length is 4")
    print(f"Start-of-packet is found at {marker(stream, 14)} when its length is 14")


if __name__ == "__main__":
    comms(Path(__file__).parent / "input")
