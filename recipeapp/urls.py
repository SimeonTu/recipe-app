# project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from recipes.views import home, records  # Import directly
from .views import register_view, login_view, logout_view
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Home directly under '/'
    # Include recipes URLs under '/recipes/',
    path('recipes/', include('recipes.urls')),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files

# Add this at the end of your urlpatterns
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]