from django.contrib import admin
from django.urls import path, include
from apis.views import UserViewSet

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('apis/', include('apis.urls')),
                  path('login/', UserViewSet.as_view({'post': 'login'}), name='login'),
              ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
