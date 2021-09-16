from pathlib import Path  # pylint: disable=unused-import
from os.path import expanduser  # pylint: disable=unused-import

import pandas as pd
import pytest
from .context import load_food_review_train, load_food_review_test, FOOD_CLASS_VALUES


@pytest.mark.skipif('not Path(expanduser("~/.sadedegel_data/food_review")).exists()')
def test_dataset_import():
    raw_train = load_food_review_train()
    raw_test = load_food_review_test()

    for i, rev in enumerate(raw_train):
        assert isinstance(rev, dict)
        assert rev.get("id") is not None
        assert rev.get("text") is not None
        assert rev.get("sentiment_class") is not None
    assert i + 1 == 470396

    for i, rev in enumerate(raw_test):
        assert isinstance(rev, dict)
        assert rev.get("id") is not None
        assert rev.get("text") is not None
        assert rev.get("sentiment_class") is not None
    assert i + 1 == 117599


@pytest.mark.skipif('not Path(expanduser("~/.sadedegel_data/food_review")).exists()')
def test_sentiment_class():
    assert FOOD_CLASS_VALUES[0] == "NEGATIVE"
    assert FOOD_CLASS_VALUES[1] == "POSITIVE"


@pytest.mark.skipif('not Path(expanduser("~/.sadedegel_data/food_review")).exists()')
def test_from_records():
    raw_train = load_food_review_train()
    raw_test = load_food_review_test()

    train_df = pd.DataFrame().from_records(raw_train)
    test_df = pd.DataFrame().from_records(raw_test)

    assert set(train_df.columns.tolist()) == {"id", "text", "sentiment_class", "speed", "service", "flavour"}
    assert set(test_df.columns.tolist()) == {"id", "text", "sentiment_class", "speed", "service", "flavour"}