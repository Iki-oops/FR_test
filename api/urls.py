from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PollViewSet,
    QuestionViewSet,
    login,
    delete_test_cookie,
    start_polling,
    get_answers,
    delete_test_cookie
)


router = DefaultRouter()
router.register('polls', PollViewSet)
router.register(
    r'polls/(?P<poll_id>[0-9]+)/questions',
    QuestionViewSet,
    basename='question',
)


urlpatterns = [
    path('login/', login),
    path('start-polling/', start_polling),
    path('delete-test-cookie/', delete_test_cookie),
    path('answers/', get_answers),
    path('', include(router.urls))
]
