from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.http import FileResponse
import os

def serve_manifest(request):
    path_ = os.path.join(settings.BASE_DIR, 'static', 'manifest.json')
    return FileResponse(open(path_, 'rb'), content_type='application/manifest+json')

def serve_sw(request):
    path_ = os.path.join(settings.BASE_DIR, 'static', 'js', 'sw.js')
    return FileResponse(open(path_, 'rb'), content_type='application/javascript')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
    path('manifest.json', serve_manifest, name='manifest'),
    path('sw.js', serve_sw, name='sw'),
    path('accounts/', include('accounts.urls')),
    path('groups/', include('groups.urls')),
    path('', include('expenses.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
