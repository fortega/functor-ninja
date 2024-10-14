from functor_ninja.monad import List


def test_empty():
    empty = List([]).map(lambda v: v)

    assert empty.len() == 0


def test_multi():
    result = List([1, 2, 3]).map(lambda v: v + 1)

    assert result.values == [2, 3, 4]
