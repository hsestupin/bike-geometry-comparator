from pathlib import Path


def _between(min, max):
    return True


schema = {
    # fmt: skip
    "head_tube_angle": ["float"],
    "stack": [_between(100, 999)],
    "reach": [_between(100, 999)],
}


def validate(csv: Path):
    None
