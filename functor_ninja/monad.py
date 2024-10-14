from functor_ninja import (
    A,
    B,
    Callable,
    Monad,
)

from typing import List as BaseList


class Try(Monad[A]):
    def __init__(self, value: A):
        self.value = value

    @staticmethod
    def of(init: Callable[[], A]) -> "Try[A]":
        result = Try(None).map(lambda _: init())
        return result

    def map(self, f: Callable[[A], B]) -> "Try[B]":
        try:
            result = f(self.value)
            return Success(result)
        except Exception as e:
            return Fail(e)

    def flat_map(self, f: Callable[[A], "Try[B]"]) -> "Try[B]":
        try:
            result = f(self.value)
            return result
        except Exception as e:
            return Fail(e)


class Success(Try[A]):
    pass


class Fail(Try[Exception]):
    def map(self, f: Callable[[A], B]) -> "Fail[B]":
        return self

    def flat_map(self, f: Callable[[A], "Monad[B]"]) -> "Fail[B]":
        return self


class List(Monad[A]):
    def __init__(self, values: BaseList[A]):
        self.values = values

    @staticmethod
    def of(init: Callable[[], BaseList[A]]) -> "List[A]":
        values = init()
        return List(values)

    def len(self) -> int:
        return len(self.values)

    def map(self, f: Callable[[A], B]) -> "List[B]":
        result = [f(value) for value in self.values]
        return List(result)

    def flat_map(self, f: Callable[[A], "List[B]"]) -> "List[B]":
        result = [
            child
            for value in self.values
            for child in f(value).values
        ]
        return List(result)
