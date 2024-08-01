# devmarketer_project/urls.py

from django.contrib import admin
from django.urls import path, include, re_path
from api.views import index  # Import the index view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Your API urls
    re_path(r'^.*', index, name='index'),  # This should be the last pattern
]


