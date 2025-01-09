from functor_ninja.monad import Monad, A, B, Callable
from functor_ninja import Try
from time import sleep

NO_ATTEMPTS = 0


class Retry(Monad[A]):
    def __init__(self, attempts: int, value: A, wait_secs: float = 3.0):
        self.attempts = attempts
        self.value = value
        self.wait_secs = wait_secs

    def map(self, f: Callable[[A], B]) -> "Retry[B]":
        def op(left: int) -> Try[B]:
            result = Try(self.value).map(f)
            if result.is_success():
                return Retry(attempts=self.attempts, value=result.value)
            else:
                if left > NO_ATTEMPTS:
                    new_left = left - 1
                    print("wait", self.wait_secs, "secs")
                    sleep(self.wait_secs)
                    return op(left=new_left)
                else:
                    return Retry(attempts=NO_ATTEMPTS, value=result.value)
        return op(left=self.attempts) if self.is_success() else self

    def is_fail(self) -> bool:
        return self.attempts == NO_ATTEMPTS

    def is_success(self) -> bool:
        return not self.is_fail()

    def flatten(self) -> "Retry[A]":
        if self.is_fail():
            return self
        else:
            return self.value

    def flat_map(self, f: Callable[[A], "Retry[B]"]) -> "Retry[B]":
        nested = self.map(f)
        result = nested.flatten()
        return result
