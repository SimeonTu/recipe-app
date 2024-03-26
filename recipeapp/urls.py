# project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from recipes.views import home, records  # Import directly
from .views import login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Home directly under '/'
    path('records/', records, name='records'),  # 'Records' directly under '/'
    path('recipes/', include('recipes.urls')),  # Include recipes URLs under '/recipes/'
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files
