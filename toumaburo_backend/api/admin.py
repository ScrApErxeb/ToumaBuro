from django.contrib import admin
from .models import Prestataire, Service, OffreService, Avis, DemandeService

admin.site.register(Prestataire)
admin.site.register(Service)
admin.site.register(OffreService)
admin.site.register(Avis)
admin.site.register(DemandeService)