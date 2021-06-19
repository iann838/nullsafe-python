from typing import Any
from nullsafe import _, undefined
from nullsafe.core import NullSafe


class TestClassOne:

    existent: int = 123
    inexistent: str
    subscriptable: dict


class TestClassTwo:

    existent: str
    inexistent: str

    def __init__(self) -> None:
        self.existent = "yeah"

    def __getitem__(self, k: str) -> str:
        return self.__dict__[k]

    def __setitem__(self, k: str, v: Any) -> str:
        self.__dict__[k] = v


class TestClassThree:

    existent: TestClassOne
    inexistent: TestClassOne

    def __init__(self) -> None:
        self.existent = TestClassOne()



def test_null_attr():
    o = TestClassOne()
    assert o.existent == 123
    try:
        o.inexistent
        assert False
    except AttributeError as e:
        assert "inexistent" in str(e)
    assert _(o).inexistent is undefined
    assert _(o).inexistent == NullSafe()
    assert _(o)
    assert bool(_(o).inexistent) is False
    assert not _(o).inexistent
    try:
        _(o).existent = 369
        assert False
    except AttributeError as e:
        assert True
    try:
        _(o).inexistent = 369
        assert False
    except AttributeError as e:
        assert True
    o.existent = 369
    assert o.existent == 369
    o.inexistent = 789
    assert o.inexistent == 789


def test_null_item():
    o = TestClassTwo()
    assert o["existent"] == "yeah"
    try:
        o["inexistent"]
        assert False
    except KeyError as e:
        assert "inexistent" in str(e)
    assert _(o)["inexistent"] is undefined
    assert _(o)
    assert bool(_(o).inexistent) is False
    assert not _(o).inexistent
    try:
        _(o)["existent"] = "nah"
        assert False
    except TypeError as e:
        assert True
    try:
        _(o)["inexistent"] = "nah"
        assert False
    except TypeError as e:
        assert True
    o["existent"] = "nah"
    assert o["existent"] == "nah"
    o["inexistent"] = "noyeah"
    assert o["inexistent"] == "noyeah"


def test_nested_null_attr():
    o = TestClassThree()
    assert o.existent.existent == 123
    try:
        o.inexistent
        assert False
    except AttributeError as e:
        assert "inexistent" in str(e)
    assert _(o).inexistent is undefined
    assert _(o).inexistent == NullSafe()
    assert _(o).inexistent.inexistent is undefined
    assert _(o).inexistent.inexistent == NullSafe()
    assert _(_(o).existent).inexistent is undefined
    assert _(_(o).existent).inexistent == NullSafe()
    assert _(_(o).existent).inexistent.inexistent is undefined
    assert _(_(o).existent).inexistent.inexistent == NullSafe()
    assert bool(_(o).inexistent) is False
    assert not _(_(o).existent).inexistent
    assert bool(_(o).inexistent.inexistent) is False
    assert not _(_(o).existent).inexistent.inexistent
    try:
        _(o).existent = 369
        assert False
    except AttributeError as e:
        assert True
    try:
        _(_(o).existent).inexistent = 369
        assert False
    except AttributeError as e:
        assert True
    _(o).existent.inexistent = 36953
    try:
        _(o).inexistent.inexistent = 369
        assert False
    except AttributeError as e:
        assert True
    try:
        o.inexistent.inexistent = 789
    except AttributeError as e:
        assert True
    o.existent.existent = 369
    assert o.existent.existent == 369
    o.inexistent = TestClassOne()
    o.inexistent.inexistent = 789
    assert o.inexistent.inexistent == 789
    o.inexistent.existent = 7891
    assert o.inexistent.existent == 7891
    

def test_nested_null_item():
    o = {"existent": {"existent": 123}}
    assert o["existent"]["existent"] == 123
    try:
        o["inexistent"]
        assert False
    except KeyError as e:
        assert "inexistent" in str(e)
    assert _(o)["inexistent"] is undefined
    assert _(o)["inexistent"] == NullSafe()
    assert _(o)["inexistent"]["inexistent"] is undefined
    assert _(o)["inexistent"]["inexistent"] == NullSafe()
    assert _(_(o)["existent"])["inexistent"] is undefined
    assert _(_(o)["existent"])["inexistent"] == NullSafe()
    assert _(_(o)["existent"])["inexistent"]["inexistent"] is undefined
    assert _(_(o)["existent"])["inexistent"]["inexistent"] == NullSafe()
    assert bool(_(o)["inexistent"]) is False
    assert not _(_(o)["existent"])["inexistent"]
    assert bool(_(o)["inexistent"]["inexistent"]) is False
    assert not _(_(o)["existent"])["inexistent"]["inexistent"]
    try:
        _(o)["existent"] = 369
        assert False
    except TypeError as e:
        assert True
    try:
        _(_(o)["existent"])["inexistent"] = 369
        assert False
    except TypeError as e:
        assert True
    _(o)["existent"]["inexistent"] = 369
    try:
        _(o)["inexistent"]["inexistent"] = 369
        assert False
    except TypeError as e:
        assert True
    try:
        o["inexistent"]["inexistent"] = 789
        assert False
    except KeyError as e:
        assert True
    o["existent"]["existent"] = 369
    assert o["existent"]["existent"] == 369
    o["inexistent"] = {}
    o["inexistent"]["inexistent"] = 789
    assert o["inexistent"]["inexistent"] == 789
    o["inexistent"]["existent"] = 7891
    assert o["inexistent"]["existent"] == 7891


def test_null_combined():
    one = TestClassOne()
    one.subscriptable = {"existent": 123}
    o = {"existent": one}
    assert o["existent"].subscriptable["existent"] == 123
    assert _(o)["inexistent"].subscriptable["existent"] is undefined
    assert _(o["existent"]).inexistent["existent"] is undefined
    assert _(o["existent"].subscriptable)["inexistent"] is undefined
    o = TestClassOne()
    o.subscriptable = {"existent": TestClassOne()}
    assert _(o).inexistent["existent"].subscriptable["existent"] is undefined
    assert _(o.subscriptable)["inexistent"].existent is undefined
    assert _(o.subscriptable)["inexistent"].existent is undefined
    assert o.subscriptable["existent"].existent == 123
