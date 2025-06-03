from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Prestataire, Service, OffreService, Avis, DemandeService

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'nom']

class PrestataireSerializer(serializers.ModelSerializer):
    services_offerts = serializers.SerializerMethodField()

    class Meta:
        model = Prestataire
        fields = '__all__'

    def get_services_offerts(self, obj):
        return obj.services_offerts.values('id', 'nom')

class OffreServiceSerializer(serializers.ModelSerializer):
    prestataire = PrestataireSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = OffreService
        fields = '__all__'

class AvisSerializer(serializers.ModelSerializer):
    utilisateur = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
    utilisateur_nom = serializers.CharField(source='utilisateur.username', read_only=True)

    class Meta:
        model = Avis
        fields = ['id', 'prestataire', 'utilisateur', 'utilisateur_nom', 'note', 'commentaire', 'date_creation', 'date_modification']
        read_only_fields = ['id', 'prestataire', 'utilisateur_nom', 'date_creation', 'date_modification']
        extra_kwargs = {'prestataire': {'write_only': True}} # L'ID du prestataire est fourni lors de la création/mise à jour

class DemandeServiceSerializer(serializers.ModelSerializer):
    utilisateur = UserSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = DemandeService
        fields = '__all__'
        read_only_fields = ('utilisateur',) # L'utilisateur sera déterminé par la requête

class PrestataireInscriptionSerializer(serializers.Serializer):
    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    telephone = serializers.CharField(max_length=20)
    mot_de_passe = serializers.CharField(write_only=True, min_length=6)
    services_offerts = serializers.ListField(child=serializers.CharField(max_length=100), max_length=3) # Nouveau champ dans le sérialiseur

    def create(self, validated_data):
        telephone = validated_data['telephone']
        if User.objects.filter(username=telephone).exists():
            raise serializers.ValidationError({"telephone": "Ce numéro de téléphone est déjà enregistré."})

        user = User.objects.create_user(
            username=telephone,
            password=validated_data['mot_de_passe']
        )
        prestataire = Prestataire.objects.create(
            user=user,
            nom=validated_data['nom'],
            prenom=validated_data['prenom'],
            telephone=telephone,
            # ... autres champs
        )

        # Gestion des services offerts
        services_data = validated_data.get('services_offerts', [])
        for service_name in services_data:
            service, created = Service.objects.get_or_create(nom=service_name.strip())
            prestataire.services_offerts.add(service)

        return prestataire

    def update(self, instance, validated_data):
        instance.nom = validated_data.get('nom', instance.nom)
        instance.prenom = validated_data.get('prenom', instance.prenom)
        instance.telephone = validated_data.get('telephone', instance.telephone)
        instance.email = validated_data.get('email', instance.email)
        instance.etablissement = validated_data.get('etablissement', instance.etablissement)
        instance.zone_couverture = validated_data.get('zone_couverture', instance.zone_couverture)
        instance.description = validated_data.get('description', instance.description)
        # Gestion des services offerts (ManyToManyField) - nécessite une logique spécifique
        instance.save()
        return instance