from django.contrib import admin
from django.urls import path, include
import apps.bookmodule.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', apps.bookmodule.views.index),
    path('index2/<int:val1>/', apps.bookmodule.views.index2),
    path('books/', include('apps.bookmodule.urls')),
]
