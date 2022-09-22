from lib.api.exceptions import ApplicationAPIException
from lib.interfaces.application.exceptions import ApplicationException
from lib.interfaces.application.use_case import UseCaseExecutor


class APIUseCaseExecutor(UseCaseExecutor):
    @classmethod
    def perform_use_case(self, use_case, *args, **kwargs):
        try:
            return use_case(*args, **kwargs)
        except ApplicationException as e:
            # 400 エラーとするため exception を変更
            raise ApplicationAPIException(e.message)
