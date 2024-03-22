from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from . import views

urlpatterns = [

    path('', views.default_view , name = "homepage"),
    path('cars/', views.cars_view , name = "carpage"),
    path('car/<uuid:pk>/', views.CarDetailView, name='car-detail'),#specific car page passed by pk
    path('requests/',views.car_request_view,name='requests'),
    path('requests/<uuid:request_id>/', views.car_request_view, name='requests'),
    path('manager/', views.manager_page, name='manager_page'),
    path('manager/addcar', views.add_car, name='add_car'),
    path('manager/edit_car/<uuid:car_id>/', views.edit_car, name='edit_car'),#specific car page passed by pk

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

