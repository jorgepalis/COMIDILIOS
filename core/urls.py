from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # browser reload
    path("__reload__/", include("django_browser_reload.urls")),
    path('', include('Auth.urls')),
    path('api/', include('store.urls')),
    path('auth/', include('auth2.urls', namespace='auth2')),
    path('', include('main.urls', namespace='main')),
    path('store2/', include('store2.urls', namespace='store2')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
