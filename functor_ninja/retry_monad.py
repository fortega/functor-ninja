from functor_ninja.monad import Monad, A, B, Callable
from functor_ninja import Try

NO_ATTEMPTS = 0


class Retry(Monad[A]):
    def __init__(self, attempts: int, value: A):
        self.attempts = attempts
        self.value = value

    def map(self, f: Callable[[A], B]) -> "Retry[B]":
        def op(left: int) -> Try[B]:
            result = Try(self.value).map(f)
            if result.is_success():
                return Retry(attempts=self.attempts, value=result.value)
            else:
                if left > NO_ATTEMPTS:
                    new_left = left - 1
                    return op(left=new_left)
                else:
                    return Retry(attempts=NO_ATTEMPTS, value=result.value)
        return op(left=self.attempts) if self.is_success() else self

    def is_fail(self) -> bool:
        return self.attempts == NO_ATTEMPTS

    def is_success(self) -> bool:
        return not self.is_fail()

    @staticmethod
    def flat(v: "Retry[Retry[A]]") -> "Retry[A]":
        if v.is_fail():
            return v
        else:
            return v.value

    def flat_map(self, f: Callable[[A], "Retry[B]"]) -> "Retry[B]":
        nested = self.map(f)
        result = Retry.flat(nested)
        return result
