from pathlib import Path
from typing import Callable, Final
from collections import Counter


class Monkey:
    def __init__(self, index: int) -> None:
        self.index = index
        self.items: list[Item] = []
        self.operation: list[str] = []
        self.test_call: Callable | None = None
        self.test_conditions: dict[bool, int] = {}
        self.inspected = 0

    def add_item(self, item: "Item") -> None:
        self.items.append(item)

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

    def process(self) -> list[tuple["Item", int]]:
        outcome: list[tuple[Item, int]] = []
        for item in self.items:
            new_worry_level = self.operate(item.worry) // 3
            item.inspect(new_worry_level, self)
            throw_to = self.throw_to(new_worry_level)
            outcome.append((item, throw_to))
            self.inspected += 1
        self.items = []
        return outcome


class Item:
    def __init__(self, worry: int) -> None:
        self.worry = worry
        self.inspected: dict[int, int] = {}
        self.history: list[int] = []

    def inspect(self, new_worry: int, monkey: Monkey) -> None:
        self.history.append(monkey.index)
        self.worry = new_worry
        self.inspected[monkey.index] = self.inspected.get(monkey.index, 0) + 1

    def can_simulate(self) -> bool:
        return self.inspected[self.history[-1]] > 1

    def simulate(self, up_until: int) -> dict[int, int]:
        assert self.can_simulate()
        path: list[int] = self.history.copy()

        done_rounds: Final = sum(self.inspected.values())
        if done_rounds == up_until:
            return self.inspected

        assert (
            done_rounds == len(self.inspected) + 1
        ), f"{done_rounds} != {len(self.history)}+1"

        last_monkey: Final = path.pop()
        while not path[0] == last_monkey:
            path.pop(0)

        tours: Final = (up_until - done_rounds) // len(path)
        for monkey in path:
            self.inspected[monkey] += tours

        rounds_left: Final = up_until - sum(self.inspected.values())
        for r in range(rounds_left):
            self.inspected[path[r]] += 1

        assert sum(self.inspected.values()) == up_until
        return self.inspected

    def try_simulate(self, up_until: int) -> bool:
        if not self.can_simulate():
            return False
        self.simulate(up_until)
        return True


class Jungle:
    def __init__(self) -> None:
        self.monkeys: list[Monkey] = []
        self.current_round = 0
        self.simulated: list[Item] = []

    def add_monkey(self, monkey: Monkey) -> None:
        assert monkey.index == len(self.monkeys)
        self.monkeys.append(monkey)

    def make_round(self) -> None:
        self.current_round += 1
        for monkey in self.monkeys:
            for item, recipient in monkey.process():
                self.monkeys[recipient].add_item(item)

    def run(self, rounds: int) -> None:
        while sum([len(monkey.items) for monkey in self.monkeys]):
            self.make_round()
            for monkey in self.monkeys:
                for item in monkey.items.copy():
                    if item.try_simulate(rounds):
                        self.simulated.append(item)
                        monkey.items.remove(item)

    def business_level(self) -> int:
        simulation: Counter = Counter()
        for sim in self.simulated:
            simulation.update(Counter(sim.inspected))
        inspected = list(simulation.values())
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
                    worry = int(item_raw.strip())
                    jungle.monkeys[-1].add_item(Item(worry))

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
    monkeys(Path(__file__).parent / "test")
