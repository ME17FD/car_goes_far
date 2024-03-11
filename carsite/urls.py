from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from . import views

urlpatterns = [

    path('', views.default_view , name = "homepage"),
    path('cars/', views.cars_view , name = "carpage"),
    path('car/<uuid:pk>/', views.CarDetailView.as_view(), name='car-detail'),#specific car page passed by pk
    path('requests/',views.car_request_view,name='requests'),
    path('requests/<uuid:request_id>/', views.car_request_view, name='requests'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

