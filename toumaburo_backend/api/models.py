from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Prestataire(models.Model):
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    etablissement = models.CharField(max_length=255, verbose_name="Établissement principal")
    zone_couverture_rayon = models.FloatField(blank=True, null=True, verbose_name="Rayon de couverture (km)")
    # ... autres champs du prestataire

    def __str__(self):
        return self.nom

class Service(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom

class OffreService(models.Model):
    prestataire = models.ForeignKey(Prestataire, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    tarif = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('prestataire', 'service')

    def __str__(self):
        return f"{self.prestataire.nom} - {self.service.nom}"

class Avis(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    prestataire = models.ForeignKey(Prestataire, on_delete=models.CASCADE)
    note = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    commentaire = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avis de {self.utilisateur.username} pour {self.prestataire.nom}"

class DemandeService(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    localisation_latitude = models.FloatField()
    localisation_longitude = models.FloatField()
    date_creation = models.DateTimeField(auto_now_add=True)
    # Ajoutez d'autres champs si nécessaire

    def __str__(self):
        return f"Demande de {self.utilisateur.username} pour {self.service.nom}"