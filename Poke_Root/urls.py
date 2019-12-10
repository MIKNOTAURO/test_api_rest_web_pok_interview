from django.contrib import admin
from django.urls import path

from .views import list_pokemons, retrieve_poke, type_pokes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', list_pokemons, name='lista-pokes'),
    path('detail-poke/<id_poke>/', retrieve_poke, name='detail-poke'),
    path('poke-type/<type_poke>/', type_pokes, name='list-types')

]
