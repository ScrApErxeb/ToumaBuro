from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import CustomTokenObtainPairView


router = DefaultRouter()
router.register(r'prestataires', views.PrestataireViewSet, basename='prestataire')
router.register(r'services', views.ServiceViewSet, basename='service')
router.register(r'offres-service', views.OffreServiceViewSet, basename='offre-service')
router.register(r'avis', views.AvisViewSet, basename='avis')
router.register(r'demandes', views.DemandeServiceViewSet, basename='demande')

urlpatterns = [
    path('prestataires/inscription/', views.PrestataireInscriptionView.as_view(), name='prestataire-inscription'),
    path('prestataires-accueil/', views.PrestatairesAccueilView.as_view(), name='prestataires-accueil'), # Utilisation de .as_view()
    # path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('', include(router.urls)),
    path('prestataires-par-service/', views.PrestatairesParServiceEtLocalisationListView.as_view(), name='prestataires-par-service'),
    path('demandes/creer/', views.DemandeServiceCreateView.as_view(), name='creer-demande'),
    path('prestataires/<int:prestataire_id>/avis/', views.AvisParPrestataireListView.as_view(), name='avis-prestataire'),
    path('prestataires/<int:prestataire_id>/avis/create_update/', views.AvisCreateUpdateView.as_view(), name='avis-create-update'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Ajoutez cette ligne pour la route d'inscription
]