"""
URL configuration for aso_AYSA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from usuarios import views

urlpatterns = [
    path('', views.home, name='home'),
    path('iniciar-sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('demo/', views.demo_home, name='demo_home'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('microsoft/login/', views.microsoft_login, name='microsoft_login'),
    path('microsoft/callback/', views.microsoft_callback, name='microsoft_callback'),
    path('vale/', views.generar_vale, name='generar_vale'),
    path('prestamo/', views.pedir_prestamo, name='pedir_prestamo'),
    path('admin/', admin.site.urls),
]
