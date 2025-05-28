from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'prestataires', views.PrestataireViewSet)
router.register(r'services', views.ServiceViewSet)
router.register(r'offres-service', views.OffreServiceViewSet)
router.register(r'avis', views.AvisViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('demandes/', views.DemandeServiceCreateView.as_view(), name='creer-demande'),
    path('prestataires-par-service/', views.PrestatairesParServiceEtLocalisationListView.as_view(), name='prestataires-par-service'),
]