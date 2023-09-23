from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.activity.urls')),
    path('profiles/', include('apps.profiles.urls')),
    path('auth/', include('apps.accounts.urls')),
    path('books/', include('apps.books.urls')),
    path('chat/', include('apps.userschats.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
