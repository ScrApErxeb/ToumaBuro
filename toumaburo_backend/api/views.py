from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Prestataire, Service, OffreService, Avis, DemandeService
from .serializers import PrestataireSerializer, ServiceSerializer, OffreServiceSerializer, AvisSerializer, DemandeServiceSerializer
import requests
import math

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
        rayon_recherche = self.request.query_params.get('rayon')

        queryset = Prestataire.objects.filter(offreservice__service_id=service_id).distinct()

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
                    return filtered_prestataires
                else:
                    # Si la géocodage de la localisation échoue, retourner tous les prestataires pour le service
                    return queryset
            except requests.exceptions.RequestException as e:
                print(f"Erreur de requête de géocodage: {e}")
                return queryset
            except (KeyError, IndexError, ValueError) as e:
                print(f"Erreur de parsing de la réponse de géocodage: {e}")
                return queryset
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