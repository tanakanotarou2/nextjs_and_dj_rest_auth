from django.db import transaction
from django.db.models import Prefetch, QuerySet

from polls.models import Choice, Question


class QuestionFindAllAction:
    def __call__(self, *args, **kwargs) -> QuerySet:
        """
        QuerySet返すだけのような場合は view から直接読んでも良いことにする。
        業務的な処理が入る場合は UseCase(Action) に切り出す。
        例) ログインユーザーによって参照範囲を制限する場合など

        """
        choice_qs = Choice.objects.order_by("id")
        return Question.objects.all().prefetch_related(Prefetch("choice_set", queryset=choice_qs))


class QuestionCreateAction:
    def __init__(self, data: dict):
        self._data = data.copy()

    def __call__(self, *args, **kwargs) -> Question:
        with transaction.atomic():
            q = Question(
                question_text=self._data["question_text"],
                pub_date=self._data["pub_date"],
            )
            q.save()

            choices = []
            for data in self._data["choice_set"]:
                choices.append(Choice(choice_text=data["choice_text"], question=q))
            Choice.objects.bulk_create(choices)

        # 少し無駄だけど、choice_setの紐付いたQuestionを再取得する
        return Question.objects.prefetch_related("choice_set").get(id=q.id)


class QuestionUpdateAction:
    def __init__(self, instance: Question, data: dict):
        self._instance = instance
        self._data = data.copy()

    def __call__(self, *args, **kwargs) -> Question:
        # 業務的な validation があれば validation service を作る

        # 本当は1項目づつみるほうが適切と思う

        for k, v in self._data.items():
            setattr(self._instance, k, v)

        self._instance.save()

        # レスポンス用に加工が必要なら行う
        return self._instance


class QuestionDeleteAction:
    """
    削除のアクション
    検索同様に、業務ロジックを挟まないなら view だけで済ませても良い
    """

    def __init__(self, instance: Question):
        self._instance = instance

    def __call__(self, *args, **kwargs) -> None:
        self._instance.delete()
