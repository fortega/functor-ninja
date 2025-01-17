from functor_ninja.monad import Monad, A, B, Callable
from functor_ninja import Try
from time import sleep

NO_ATTEMPTS = 0


def fixed_wait(v: float) -> Callable[[int], float]:
    return lambda _: v


def linear_wait(factor: float) -> Callable[[int], float]:
    return lambda v: factor * v


class Retry(Monad[A]):
    def __init__(self, attempts: int, value: A, wait_funtion_secs: Callable[[int], float] = fixed_wait(3.0)):
        self.attempts = attempts
        self.value = value
        self.wait_funtion_secs = wait_funtion_secs

    def map(self, f: Callable[[A], B]) -> "Retry[B]":
        def op(attempt: int) -> Try[B]:
            result = Try(self.value).map(f)
            if result.is_success():
                return Retry(attempts=self.attempts, value=result.value)
            else:
                if attempt >= self.attempts:
                    return Retry(attempts=NO_ATTEMPTS, value=result.value)
                else:
                    new_attempt = attempt + 1
                    wait_secs = self.wait_funtion_secs(attempt)
                    sleep(wait_secs)
                    return op(attempt=new_attempt)
        return op(attempt=1) if self.is_success() else self

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
