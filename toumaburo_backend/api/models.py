from django.db import models
from django.contrib.auth.models import User
from django.db import models

class Service(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    # ... autres champs du modèle Service ...

    def __str__(self):
        return self.nom

from django.db import models
from django.contrib.auth.models import User
from .models import Service # Assurez-vous que Service est importé correctement

class Prestataire(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)  # Ajoutez ce champ
    email = models.EmailField(unique=True, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    etablissement = models.CharField(max_length=200, blank=True, null=True)
    services_offerts = models.ManyToManyField(Service, related_name='prestataires')
    zone_couverture = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)  # Ajoutez ce champ


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

from django.db import models
from django.contrib.auth.models import User

class Avis(models.Model):
    prestataire = models.ForeignKey(Prestataire, on_delete=models.CASCADE, related_name='avis')
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.IntegerField(
        choices=[(1, '1 étoile'), (2, '2 étoiles'), (3, '3 étoiles'), (4, '4 étoiles'), (5, '5 étoiles')],
        default=5
    )
    commentaire = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('prestataire', 'utilisateur')

    def __str__(self):
        return f"Avis de {self.utilisateur} pour {self.prestataire}"

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

        # cool