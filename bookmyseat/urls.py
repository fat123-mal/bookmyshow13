from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('movies.urls')),
    
    # 🔁 Redirect /login/ to /users/login/
    path('login/', lambda request: redirect(f'/users/login/?next={request.GET.get("next", "/")}')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
