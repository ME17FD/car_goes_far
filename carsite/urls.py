from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from . import views

urlpatterns = [

    path('', views.default_view , name = "homepage"),
    path('cars/', views.cars_view , name = "carpage"),
    path('car/<uuid:pk>/', views.CarDetailView.as_view(), name='car-detail'),#specific car page passed by pk
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

