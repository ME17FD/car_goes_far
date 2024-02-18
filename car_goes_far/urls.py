from django.contrib import admin
from django.urls import path,include
from siteuser import views

urlpatterns = [
    path("profiles/",include("siteuser.urls")),
    path('admin/logout/', views.CustomLogoutView.as_view(), name='admin_logout'),
    #path("profiles/",include("django.contrib.auth.urls")),
    path("",include("carsite.urls")),
    path('admin/', admin.site.urls ),

]
