from django.contrib import admin
from django.urls import path
from uploader.views import file_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', file_view),
]
