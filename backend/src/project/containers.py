from dependency_injector import containers, providers

from lib.interfaces.application.use_case import UseCaseExecutor
from lib.interfaces.context.date_util import DateUtil

date_util_provider: providers.Provider[DateUtil] = providers.Dependency(instance_of=DateUtil)


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    date_util = providers.Dependency(instance_of=DateUtil)

    # REST API から UseCase をコールするためのオブジェクト
    use_case_executor = providers.Dependency(instance_of=UseCaseExecutor, default=UseCaseExecutor())
