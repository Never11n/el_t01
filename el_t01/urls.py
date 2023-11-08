from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('el_t01/', include('el_t01_app.urls')),
    path('', include('el_t01_app.urls')),
    path('', include('el_t0001_app.urls')),
    path('', include('el_t0002_app.urls')),
    path('', include('el_t0003_app.urls')),
    path('', include('el_t0004_app.urls'))
]

