from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Prestataire, Service, OffreService, Avis, DemandeService
from .serializers import PrestataireSerializer, ServiceSerializer, OffreServiceSerializer, AvisSerializer, DemandeServiceSerializer

class PrestataireViewSet(viewsets.ModelViewSet):
    queryset = Prestataire.objects.all()
    serializer_class = PrestataireSerializer
    permission_classes = [AllowAny] # Pour le moment, on autorise tout le monde

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
        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')

        queryset = Prestataire.objects.filter(offreservice__service_id=service_id).distinct()

        if latitude and longitude:
            try:
                latitude = float(latitude)
                longitude = float(longitude)
                # Ici, vous ajouteriez la logique de filtrage par localisation
                # par exemple, en utilisant une fonction pour calculer la distance
                # et en filtrant les prestataires dans un certain rayon.
                # Pour l'instant, on ne fait PAS de filtrage géographique.
                pass
            except ValueError:
                # Gérer le cas où la latitude ou la longitude ne sont pas des nombres valides
                pass

        return queryset