from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'prestataires', views.PrestataireViewSet, basename='prestataire')
router.register(r'services', views.ServiceViewSet, basename='service')
router.register(r'offres', views.OffreServiceViewSet, basename='offre')
router.register(r'avis', views.AvisViewSet, basename='avis')
router.register(r'demandes', views.DemandeServiceViewSet, basename='demande')

urlpatterns = [
    path('', include(router.urls)),
    path('prestataires-par-service/', views.PrestatairesParServiceEtLocalisationListView.as_view(), name='prestataires-par-service'),
    path('demandes/creer/', views.DemandeServiceCreateView.as_view(), name='creer-demande'),
    path('prestataires/<int:prestataire_id>/avis/', views.AvisParPrestataireListView.as_view(), name='avis-prestataire'),
    path('prestataires/<int:prestataire_id>/avis/create_update/', views.AvisCreateUpdateView.as_view(), name='avis-create-update'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]