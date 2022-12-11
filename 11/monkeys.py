from pathlib import Path
from typing import Callable, Final


class Monkey:
    def __init__(self, index: int) -> None:
        self.index = index
        self.items: list[int] = []
        self.operation: list[str] = []
        self.test_call: Callable | None = None
        self.test_conditions: dict[bool, int] = {}
        self.inspected = 0

    def add_item(self, worry_level: int) -> None:
        self.items.append(worry_level)

    def record_operation(self, op_raw: str) -> None:
        assert "new" not in op_raw  # Should only include what's at right of = sign
        self.operation = op_raw.split()

    def operate(self, old: int) -> int:
        assert len(self.operation) == 3
        assert self.operation[0] == "old"  # seems to be a generic thing

        arg: int | None = None
        if self.operation[2].isnumeric():
            arg = int(self.operation[2])
        else:
            assert self.operation[2] == "old"
            arg = old

        match self.operation[1]:
            case "+":
                return old + arg
            case "*":
                return old * arg

        raise ValueError(f"Invalid operation {self.operation}")

    def record_test(self, test_raw: str) -> None:
        assert "Test" not in test_raw  # Should only include what's at right of colon
        assert test_raw.startswith("divisible by"), f"Unexpected test {test_raw}"
        divisor: Final = int(test_raw.split()[-1])
        self.test_call = lambda worry: (worry % divisor) == 0

    def test(self, worry: int) -> bool:
        assert self.test_call is not None
        return self.test_call(worry)

    def record_test_condition(self, cond: bool, recipient: int) -> None:
        self.test_conditions[cond] = recipient

    def throw_to(self, worry: int) -> int:
        outcome = self.test(worry)
        return self.test_conditions[outcome]

    def process(self) -> list[tuple[int, int]]:
        outcome: list[tuple[int, int]] = []
        for item in self.items:
            new_worry_level = self.operate(item) // 3
            throw_to = self.throw_to(new_worry_level)
            outcome.append((new_worry_level, throw_to))
            self.inspected += 1
        self.items = []
        return outcome


class Jungle:
    def __init__(self) -> None:
        self.monkeys: list[Monkey] = []
        self.current_round = 0

    def add_monkey(self, monkey: Monkey) -> None:
        assert monkey.index == len(self.monkeys)
        self.monkeys.append(monkey)

    def make_round(self) -> None:
        self.current_round += 1
        for monkey in self.monkeys:
            for worry, recipient in monkey.process():
                self.monkeys[recipient].add_item(worry)

    def run(self, rounds: int) -> None:
        for round in range(rounds):
            self.make_round()

    def business_level(self) -> int:
        inspected: list[int] = []
        for monkey in self.monkeys:
            inspected.append(monkey.inspected)
        inspected.sort()
        return inspected[-1] * inspected[-2]


def monkeys(input: Path) -> None:
    jungle = Jungle()
    with input.open("r") as f:
        for line_raw in f:
            if "Monkey" in line_raw:
                monkey_index = int(line_raw.split()[-1][:-1])
                jungle.add_monkey(Monkey(monkey_index))
                continue

            if "items" in line_raw:
                item_list = line_raw.strip().split(":")[-1]
                for item_raw in item_list.split(","):
                    jungle.monkeys[-1].add_item(int(item_raw.strip()))

            if "Operation" in line_raw:
                operation_raw = line_raw.split("=")[-1].strip()
                jungle.monkeys[-1].record_operation(operation_raw)

            if "Test" in line_raw:
                test_raw = line_raw.strip().split(":")[-1].strip()
                jungle.monkeys[-1].record_test(test_raw)

            if "If" in line_raw:
                recipient = int(line_raw.strip().split()[-1])
                if "true" in line_raw:
                    jungle.monkeys[-1].record_test_condition(True, recipient)
                if "false" in line_raw:
                    jungle.monkeys[-1].record_test_condition(False, recipient)

    rounds: Final = 20
    jungle.run(rounds)
    print(f"After {rounds} rounds, business level is {jungle.business_level()}")


if __name__ == "__main__":
    monkeys(Path(__file__).parent / "input")
