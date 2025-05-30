from django.contrib import admin
from django.urls import path, include  # N'oubliez pas d'importer 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # <---- AJOUTEZ CETTE LIGNE
]