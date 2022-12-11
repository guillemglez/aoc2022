import enum
import os
from pathlib import Path
from typing import Final


class Op(enum.Enum):
    Noop = enum.auto()
    Addx = enum.auto()


class Cpu:
    def __init__(self, instructions: list[tuple[Op, int | None]]) -> None:
        self.cycle = 0
        self.x = 1

        self.instructions = instructions
        self.strengths: dict[int, int | None] = {
            cycle: None
            for cycle in range(
                20,
                sum([(1 if op is Op.Noop else 2) for op, arg in instructions]),
                40,
            )
        }

        self.crt: list[list[bool]] = [[]]

    def strength(self) -> int:
        return self.cycle * self.x

    def increase_cycle(self) -> None:
        self.cycle += 1
        if self.cycle in self.strengths.keys():
            self.strengths[self.cycle] = self.strength()

        # Draw CRT
        pixel: Final = (self.cycle - 1) % 40
        if pixel == 0:
            self.crt.append([])
        assert len(self.crt[-1]) == pixel, f"{pixel}!={self.crt[-1]}"
        value: Final = abs(pixel % 40 - self.x) < 2
        self.crt[-1].append(value)

    def process(self, op: Op, arg: int | None) -> None:
        self.increase_cycle()
        if op == Op.Noop:
            return

        assert op == Op.Addx
        assert arg is not None
        self.increase_cycle()
        self.x += arg

    def run(self) -> int:
        for op, arg in self.instructions:
            self.process(op, arg)

        strengths: list[int] = []
        for strength in self.strengths.values():
            assert strength is not None
            strengths.append(strength)
        return sum(strengths)

    def printable_crt(self) -> str:
        lines: list[str] = []
        for line in self.crt:
            lines.append("".join(["\u2588" if pix else " " for pix in line]))
        return os.linesep.join(lines)


def cpu(input: Path) -> None:
    instructions: list[tuple[Op, int | None]] = []
    with input.open("r") as f:
        for line_raw in f:
            instruction_raw = line_raw.strip().split()
            if len(instruction_raw) == 0:
                continue

            if len(instruction_raw) == 1:
                assert instruction_raw[0] == "noop"
                instructions.append((Op.Noop, None))
            else:
                assert instruction_raw[0] == "addx"
                instructions.append((Op.Addx, int(instruction_raw[1])))

    cpu = Cpu(instructions)
    print(f"The sum of the final strengths is {cpu.run()}")
    print(f"The CRT screen draws:{cpu.printable_crt()}")


if __name__ == "__main__":
    cpu(Path(__file__).parent / "input")
