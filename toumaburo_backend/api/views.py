from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Prestataire, Service, OffreService, Avis, DemandeService
from .serializers import PrestataireSerializer, ServiceSerializer, OffreServiceSerializer, AvisSerializer, DemandeServiceSerializer
import requests
import math
from django.db.models import Q

class PrestataireViewSet(viewsets.ModelViewSet):
    queryset = Prestataire.objects.all()
    serializer_class = PrestataireSerializer
    permission_classes = [AllowAny]

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]

class OffreServiceViewSet(viewsets.ModelViewSet):
    queryset = OffreService.objects.all()
    serializer_class = OffreServiceSerializer
    permission_classes = [AllowAny]

class AvisViewSet(viewsets.ModelViewSet):
    queryset = Avis.objects.all()
    serializer_class = AvisSerializer
    permission_classes = [AllowAny]

class DemandeServiceViewSet(viewsets.ModelViewSet):
    queryset = DemandeService.objects.all()
    serializer_class = DemandeServiceSerializer
    permission_classes = [AllowAny]

class DemandeServiceCreateView(generics.CreateAPIView):
    queryset = DemandeService.objects.all()
    serializer_class = DemandeServiceSerializer
    permission_classes = [IsAuthenticated] # Les utilisateurs connectés peuvent créer des demandes

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)


from rest_framework import generics
from .models import Prestataire, Service
from .serializers import PrestataireSerializer
from django.db.models import Q

class PrestatairesParServiceEtLocalisationListView(generics.ListAPIView):
    serializer_class = PrestataireSerializer

    def get_queryset(self):
        service_nom = self.request.query_params.get('service')
        localisation = self.request.query_params.get('localisation')
        query = self.request.query_params.get('q')
        queryset = Prestataire.objects.all()

        if service_nom:
            try:
                service = Service.objects.get(nom__iexact=service_nom)
                queryset = queryset.filter(services_offerts=service)
            except Service.DoesNotExist:
                queryset = Prestataire.objects.none()

        if query:
            queryset = queryset.filter(
                Q(nom__icontains=query) |
                Q(description__icontains=query) |
                Q(services_offerts__nom__icontains=query) |
                Q(etablissement__icontains=query) |
                Q(zone_couverture__icontains=query)
            ).distinct()

        if localisation:
            queryset = queryset.filter(zone_couverture__icontains=localisation)

        return queryset




class AvisParPrestataireListView(generics.ListAPIView):
    serializer_class = AvisSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        prestataire_id = self.kwargs['prestataire_id']
        return Avis.objects.filter(prestataire_id=prestataire_id).order_by('-date_creation')




from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Prestataire, Avis
from .serializers import AvisSerializer

class AvisCreateUpdateView(generics.CreateAPIView):
    serializer_class = AvisSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        prestataire_id = self.kwargs['prestataire_id']
        prestataire = Prestataire.objects.get(pk=prestataire_id)
        try:
            # Tenter de récupérer un avis existant de l'utilisateur pour ce prestataire
            existing_avis = Avis.objects.get(prestataire=prestataire, utilisateur=self.request.user)
            # Mettre à jour l'avis existant avec les nouvelles données
            serializer.update(existing_avis, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Avis.DoesNotExist:
            # Créer un nouvel avis
            serializer.save(prestataire=prestataire, utilisateur=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class AvisParPrestataireListView(generics.ListAPIView):
    serializer_class = AvisSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        prestataire_id = self.kwargs['prestataire_id']
        return Avis.objects.filter(prestataire_id=prestataire_id).order_by('-date_creation')
    

from rest_framework import generics, permissions
from .serializers import PrestataireInscriptionSerializer

class PrestataireInscriptionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PrestataireInscriptionSerializer(data=request.data)
        if serializer.is_valid():
            prestataire = serializer.save()
            return Response({'id': prestataire.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Prestataire

class PrestatairesAccueilView(APIView):
    """
    Vue pour afficher les prestataires en vedette (Class-Based View).
    """
    def get(self, request):
        """
        Gère les requêtes GET pour récupérer et afficher les prestataires en vedette.
        """
        try:
            prestataires_en_vedette = Prestataire.objects.filter(is_featured=True).values('id', 'nom')
            return Response(list(prestataires_en_vedette))
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Prestataire
from .serializers import ServiceSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Ajouter les infos utilisateur
        data['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }

        # Ajouter les infos prestataire
        try:
            prestataire = Prestataire.objects.get(user=user)
            data['prestataire'] = {
                'id': prestataire.id,
                'nom': prestataire.nom,
                'prenom': prestataire.prenom,
                'telephone': prestataire.telephone,
                'email': prestataire.email,
                'etablissement': prestataire.etablissement,
                'zone_couverture': prestataire.zone_couverture,
                'description': prestataire.description,
                'is_featured': prestataire.is_featured,
                'services_offerts': ServiceSerializer(prestataire.services_offerts.all(), many=True).data
            }
        except Prestataire.DoesNotExist:
            data['prestataire'] = None

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
