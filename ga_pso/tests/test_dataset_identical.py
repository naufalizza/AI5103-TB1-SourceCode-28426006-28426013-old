import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
GA_DATA = HERE.parent / "data"
ITS_DATA = HERE.parents[1] / "its_mcttrp" / "instances"


def _digest(folder):
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(folder.iterdir())}


def test_ga_pso_data_is_identical_to_its_instances():
    assert _digest(GA_DATA) == _digest(ITS_DATA)
