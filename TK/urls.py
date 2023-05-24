"""
URL configuration for TK project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls', namespace='default')),
    path('mulai_rapat/', include('mulai_rapat.urls')),
    path('pembelian_tiket/', include('pembelian_tiket.urls')),
    path('mulai_pertandingan/', include('mulai_pertandingan.urls')),
    path('peminjaman_stadium/', include('peminjaman_stadium.urls')),
    path('list_pertandingan/', include('list_pertandingan.urls')),
    path('history_rapat/', include('history_rapat.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('authentication/', include('authentication.urls')),
    path('manage_pertandingan/', include('manage_pertandingan.urls')),
    path('pembuatan_pertandingan/', include('pembuatan_pertandingan.urls')),
]
