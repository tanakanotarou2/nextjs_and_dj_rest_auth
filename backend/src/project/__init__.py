# # from django.conf import settings
# def _build_container():
from django.utils.functional import SimpleLazyObject

from lib.api.use_case import APIUseCaseExecutor


def build_container():
    """
    DI の関数でモデルを利用できるように
    公式の example を遅延ローディングするようにしている

    https://python-dependency-injector.ets-labs.org/examples/django.html
    """
    from lib.context.date_util import DjangoDateUtil

    from . import settings
    from .containers import Container

    container = Container(date_util=DjangoDateUtil(), use_case_executor=APIUseCaseExecutor())
    container.config.from_dict(settings.__dict__)
    return container


container = SimpleLazyObject(build_container)
