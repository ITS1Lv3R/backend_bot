from django.urls import path

from rest_framework import routers
from .views import *
from .api_fns import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = 'api'

router = routers.SimpleRouter()
router.register('users', UserViewSet, basename='users')
router.register('settings', ProjectSettingsViewSet, basename='settings')

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
   # swagger
   path('swager', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   # api
   path('sending_sms/', api_sending_sms, name='sending_sms'),
   path('api_to_fns/', api_to_fns, name='api_to_fns'),
   path('send_email/', send_mail, name='send_mail'),
   path('check_user_auth/', check_user_auth, name='check_user_auth')
]

urlpatterns += router.urls
