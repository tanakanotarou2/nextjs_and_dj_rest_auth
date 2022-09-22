from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from lib.views import ModelViewSet, UseUseCaseMixin
from polls.models import Choice, Question
from polls.serializers import (
    ChoiceSerializer,
    QuestionDetailSerializer,
    QuestionSerializer,
    QuestionUpdateSerializer,
)
from polls.use_cases.choice.actions import UpvoteAction
from polls.use_cases.question.actions import (
    QuestionCreateAction,
    QuestionFindAllAction,
    QuestionUpdateAction,
)


class QuestionViewSet(UseUseCaseMixin, ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionDetailSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        action = QuestionFindAllAction()
        return self.use_case_executor.execute(action).order_by("-created")

    def _update(self, request, *args, **kwargs):
        # format などの validation は serializer で行いたいのでインスタンスの取得も妥協します
        instance = self.get_object()
        serializer = QuestionUpdateSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        action = QuestionUpdateAction(instance, serializer.validated_data)

        res_instance = self.use_case_executor.execute(action)
        response_data = QuestionSerializer(res_instance).data

        # [memo]
        # prefetch, select_related の再取得は use case 側で行います。
        # view 側は 帰ってきた値を serialize し、response に追加することを責務とします。
        # if getattr(instance, '_prefetched_objects_cache', None):
        #     # If 'prefetch_related' has been applied to a queryset, we need to
        #     # forcibly invalidate the prefetch cache on the instance.
        #     instance._prefetched_objects_cache = {}

        return Response(response_data)

    # serializer が異なる場合は指定します
    # update では List と異なる Serializer を使うので、それに合わせて指定しています。
    @extend_schema(
        request=QuestionUpdateSerializer,
        responses=QuestionSerializer,
    )
    def partial_update(self, request, *args, **kwargs):
        return super(QuestionViewSet, self).partial_update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # POSTで /api/polls/questions/ を実行した場合に実行されるmethod

        request_serializer = self.get_serializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        # QuestionCreateActionに処理委譲
        action = QuestionCreateAction(request_serializer.validated_data)

        # model instance をやりとりすることは許容
        instance = self.use_case_executor.execute(action)

        # response時のシリアライザ
        response_serializer = self.get_serializer(instance)
        return self.wrap_success_create_response(response_serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Questionデータを削除します"""

        # このような validation のない場合は、ModelView の機能をそのまま使ってもOKです。
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChoiceViewSet(UseUseCaseMixin, ModelViewSet):
    # とくに validation が必要だったり, こみいった更新などがないので drf の標準の使い方で済ませます
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # filter by nested-router-keyword
        return Choice.objects.filter(question=self.kwargs["question_pk"])

    def perform_create(self, serializer):
        return serializer.save(question_id=int(self.kwargs["question_pk"]))

    @extend_schema(
        request=None,
        # responses={200: None},
        responses=ChoiceSerializer,
        methods=["POST"],
    )
    @action(detail=True, methods=["post"])
    def upvote(self, request, question_pk, pk=None):
        # [memo]
        # upvote は question のアクションでも良いかもしれません。
        # question に対し「私はこの項目を選択します」というアクションでも、意味は合っていると思います。

        # choice の存在を確認するため get_object する
        self.get_object()

        action = UpvoteAction(pk)
        choice = self.use_case_executor.execute(action)
        response_data = ChoiceSerializer(instance=choice).data
        return Response(data=response_data, status=status.HTTP_200_OK)
