from typing import Callable, TypeVar

T = TypeVar("T")


class UseCaseExecutor:
    """UseCase を実行するクラス"""

    def run_before_execute(self, *args, **kwargs):
        pass

    def run_after_execute(self, result: T, *args, **kwargs):
        pass

    def execute(self, use_case: Callable[..., T], *args, **kwargs) -> T:
        """ユースケースを実行します"""

        self.run_before_execute(*args, **kwargs)
        result = self.perform_use_case(use_case, *args, **kwargs)
        self.run_after_execute(result, *args, **kwargs)
        return result

    def perform_use_case(self, use_case, *args, **kwargs):
        return use_case(*args, **kwargs)
