from pathlib import Path
from typing import Any, Final


# Size of a directory (recursive)
def dirsize(fs: dict[str, Any] | Any) -> int:
    if isinstance(fs, int):
        return fs

    size = 0
    for content in fs.values():
        size += dirsize(content)

    return size


# List of directory sizes for a given directory
def dirlist(fs: dict[str, Any] | Any) -> list[int]:
    lst: list[int] = []
    for dir, content in fs.items():
        if isinstance(content, dict):
            lst.append(dirsize(content))
            for size in dirlist(content):
                lst.append(size)

    return lst


def filesystem(input: Path) -> None:
    fs: dict[str, Any] = {}

    # Build filesystem
    curr: dict[str, Any] = fs
    path = Path("/")
    with input.open("r") as f:
        for line_raw in f:
            line = line_raw.strip()

            if line.startswith("$"):  # command
                cmd = line.split()[1:]
                if cmd[0] == "cd":
                    path = (path / cmd[1]).resolve()
                    curr = fs
                    if len(path.name) == 0:
                        continue  # root path
                    for parent in reversed(path.parents[:-1]):
                        curr = curr[parent.name]
                    curr = curr[path.name]
                # ignore ls, nothing to do

            else:  # listing files
                ls = line.split()
                size, loc = ls[0], ls[1]
                if size == "dir":  # it's a directory
                    curr[loc] = {}
                else:  # it's a file
                    assert size.isdecimal()
                    curr[loc] = int(size)

    threshold: Final = 100000
    sizes = sum([sz for sz in dirlist(fs) if sz <= threshold])
    print(f"The size of directories over {threshold} is {sizes}")


if __name__ == "__main__":
    filesystem(Path(__file__).parent / "input")
