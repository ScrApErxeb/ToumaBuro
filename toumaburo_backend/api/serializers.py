from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Prestataire, Service, OffreService, Avis, DemandeService

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class PrestataireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestataire
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class OffreServiceSerializer(serializers.ModelSerializer):
    prestataire = PrestataireSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = OffreService
        fields = '__all__'

class AvisSerializer(serializers.ModelSerializer):
    utilisateur = UserSerializer(read_only=True)
    prestataire = PrestataireSerializer(read_only=True)

    class Meta:
        model = Avis
        fields = '__all__'

class DemandeServiceSerializer(serializers.ModelSerializer):
    utilisateur = UserSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = DemandeService
        fields = '__all__'
        read_only_fields = ('utilisateur',) # L'utilisateur sera déterminé par la requête