from django.urls import include, path
from rest_framework_nested import routers

from polls import views

router = routers.SimpleRouter()
router.register("questions", views.QuestionViewSet)

questions_router = routers.NestedSimpleRouter(router, "questions", lookup="question")
questions_router.register("choices", views.ChoiceViewSet, basename="question-choices")

urlpatterns = [path("", include(router.urls)), path("", include(questions_router.urls))]
