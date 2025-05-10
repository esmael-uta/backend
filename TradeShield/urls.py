from django.contrib import admin
from django.urls import path, include
from .views import get_supply_chain_routes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/supply-chain-routes/', get_supply_chain_routes, name='supply-chain-routes'),
]