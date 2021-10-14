from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url

from .views import (
    PollViewSet,
    QuestionViewSet,
    get_token,
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

schema_view = get_schema_view(
   openapi.Info(
      title="Poll API",
      default_version='v1',
      description=("Документация для тестового приложения "
                   "для компании 'Фабрика решений'"),
      contact=openapi.Contact(email="bambagaevdmitrij@gmail.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('get_token/', get_token),
    path('start-polling/', start_polling),
    path('delete-test-cookie/', delete_test_cookie),
    path('answers/', get_answers),
    path('', include(router.urls)),
    url(r'^swagger(?P<format>\.json|\.yaml)$', 
       schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), 
       name='schema-swagger-ui'),
]
