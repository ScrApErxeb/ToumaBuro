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


class PrestatairesParServiceEtLocalisationListView(generics.ListAPIView):
    serializer_class = PrestataireSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        service_id = self.request.query_params.get('service')
        localisation = self.request.query_params.get('localisation')
        query = self.request.query_params.get('q')
        rayon_recherche = self.request.query_params.get('rayon')

        queryset = Prestataire.objects.all() # Commencez par tous les prestataires

        if service_id:
            queryset = queryset.filter(offreservice__service_id=service_id).distinct()

        if localisation:
            geocoding_api_url = f"VOTRE_API_DE_GEOCODAGE?q={localisation}&key=VOTRE_CLE_API"
            try:
                geocoding_response = requests.get(geocoding_api_url).json()
                if geocoding_response and geocoding_response.get('results'):
                    user_latitude = geocoding_response['results'][0]['geometry']['location']['lat']
                    user_longitude = geocoding_response['results'][0]['geometry']['location']['lng']

                    filtered_prestataires = []
                    for prestataire in queryset:
                        if prestataire.zone_couverture_rayon is not None and prestataire.etablissement:
                            etablissement_geocoding_url = f"VOTRE_API_DE_GEOCODAGE?q={prestataire.etablissement}&key=VOTRE_CLE_API"
                            etablissement_response = requests.get(etablissement_geocoding_url).json()
                            if etablissement_response and etablissement_response.get('results'):
                                prestataire_latitude = etablissement_response['results'][0]['geometry']['location']['lat']
                                prestataire_longitude = etablissement_response['results'][0]['geometry']['location']['lng']

                                distance = self.calculate_distance(user_latitude, user_longitude, prestataire_latitude, prestataire_longitude)

                                # Le rayon de couverture est en km dans le modèle, la distance est en mètres
                                if distance <= prestataire.zone_couverture_rayon * 1000:
                                    if rayon_recherche:
                                        if distance <= float(rayon_recherche) * 1000:
                                            filtered_prestataires.append(prestataire)
                                    else:
                                        filtered_prestataires.append(prestataire)
                    queryset = filtered_prestataires
                else:
                    # Si la géocodage de la localisation échoue, retourner tous les prestataires (déjà initialisé)
                    pass
            except requests.exceptions.RequestException as e:
                print(f"Erreur de requête de géocodage: {e}")
            except (KeyError, IndexError, ValueError) as e:
                print(f"Erreur de parsing de la réponse de géocodage: {e}")

        if query:
            queryset = queryset.filter(
                Q(nom__icontains=query) |
                Q(etablissement__icontains=query) |
                Q(offreservice__service__nom__icontains=query)
            ).distinct()

        return queryset

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        R = 6371000  # Rayon de la Terre en mètres
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c
        return distance





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