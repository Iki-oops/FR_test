from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PollViewSet, QuestionViewSet, AnswersViewSet


router = DefaultRouter()
router.register('polls', PollViewSet)
router.register(
    r'polls/(?P<poll_id>[0-9]+)/questions',
    QuestionViewSet,
    basename='question',
)
router.register('answers', AnswersViewSet, basename='answer')


urlpatterns = [
    path('', include(router.urls))
]
