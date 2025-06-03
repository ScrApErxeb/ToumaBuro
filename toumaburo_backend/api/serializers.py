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
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    services_offerts = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Service.objects.all()
    )
    # services_offerts_names = serializers.SerializerMethodField() # Alternative pour afficher les noms

    class Meta:
        model = Prestataire
        fields = '__all__'
        # exclude = ['service_principal'] # Si vous aviez un ancien champ

    # def get_services_offerts_names(self, instance):
    #     return [service.nom for service in instance.services_offerts.all()]


    
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


from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Prestataire

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Prestataire

class PrestataireInscriptionSerializer(serializers.Serializer):
    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    telephone = serializers.CharField(max_length=20) # Utilisation du nom 'telephone' pour correspondre au modèle
    mot_de_passe = serializers.CharField(write_only=True, min_length=6)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['telephone'], # Utilise le numéro de téléphone comme nom d'utilisateur
            password=validated_data['mot_de_passe']
        )
        prestataire = Prestataire.objects.create(
            user=user,
            nom=validated_data['nom'],
            prenom=validated_data['prenom'],
            telephone=validated_data['telephone'], # Assigne directement la valeur au champ 'telephone' du modèle
            email=validated_data.get('email'), # Si vous gérez l'email dans le formulaire
            etablissement=validated_data.get('etablissement'), # Si vous gérez l'établissement dans le formulaire
            zone_couverture=validated_data.get('zone_couverture'), # Si vous gérez la zone de couverture dans le formulaire
            description=validated_data.get('description'), # Si vous gérez la description dans le formulaire
            # Les services offerts (ManyToManyField) nécessitent une gestion spéciale après la création
        )
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