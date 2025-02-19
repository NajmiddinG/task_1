from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('edu_app.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
