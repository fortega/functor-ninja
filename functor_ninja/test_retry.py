from functor_ninja.retry_monad import Retry, linear_wait
from copy import copy


def test_map_fail():
    output = Retry(
        attempts=5, value=0,
        wait_funtion_secs=linear_wait(0.1),
    ).map(lambda _: 1/0)
    assert output.is_fail()


def test_map_ok():
    output = Retry(attempts=1, value=0).map(str)
    assert not output.is_fail()


def test_flat_map():
    ok = Retry(attempts=1, value=0)
    error = Retry(attempts=0, value=Exception())

    assert ok.flat_map(lambda _: error).is_fail()
    assert error.flat_map(lambda _: ok).is_fail()
    assert error.flat_map(lambda _: error).is_fail()

    assert ok.flat_map(lambda _: ok).is_success()
