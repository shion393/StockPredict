import pandas as pd

from src.features.labeler import triple_barrier_label


def test_triple_barrier_label_has_binary_output():
    s = pd.Series([100, 102, 104, 106, 108, 107, 106, 105, 104, 103, 102, 101])
    y = triple_barrier_label(s, up=0.03, down=-0.03, horizon_days=5).dropna()
    assert set(y.unique()).issubset({0.0, 1.0})
