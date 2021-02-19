from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler400, handler403, handler404, handler500, url

from apps.main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('apps.account.urls')),
    path('api/', include('apps.api.urls')),
    path('', include('apps.main.urls', namespace='main')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler400 = 'apps.main.views.page_not_found'
handler403 = 'apps.main.views.page_not_found'
handler404 = 'apps.main.views.page_not_found'
handler500 = 'apps.main.views.page_not_found_500'
