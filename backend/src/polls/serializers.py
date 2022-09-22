from rest_framework.serializers import ModelSerializer

from polls.models import Choice, Question


class ChoiceSerializer(ModelSerializer):
    class Meta:
        model = Choice
        fields = "__all__"
        read_only_fields = ["question", "votes"]


# [memo] レスポンス用の serializer は多くて2つというルールにしたいです。
#        ただし、権限ごとに参照可能なフィールドが異なるものが多くあったり、エンドポイントが異なる場合は、それぞれの Serializer を用意して良いです。
#
#        以下のようなルールで考えています
#        <Model名>Serializer: 基本的には自身のモデルのフィールドだけで、重要な関連項目(related field)は含めることを許します。
#        <Model名>Detail Serializer: 関連フィールドも含めます。
class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class QuestionDetailSerializer(ModelSerializer):
    choice_set = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = "__all__"


class QuestionUpdateSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = ["pub_date", "question_text"]
