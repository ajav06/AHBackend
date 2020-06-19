from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'table', views.TableViewSet, 'Table')

user_auth = views.UserViewSet.as_view()

player_retrieve = views.PlayerViewsSet.as_view({'get': 'retrieve'})
player_current = views.PlayerViewsSet.as_view({'get': 'current_card'})
player_table = views.PlayerViewsSet.as_view({'get': 'get_table'})

table_init = views.TableViewSet.as_view({'get': 'init_game'})
table_cards = views.TableViewSet.as_view({'get': 'set_cards'})
table_black = views.TableViewSet.as_view({'get': 'set_black'})


urlpatterns = [
    path('player/', player_retrieve , name='player'),
    path('player/card/<pk>/', player_current, name='player-card'),
    path('player/table/', player_table, name='player-table'),
    path('table/init/<pk>/', table_init, name='init-tb'),
    path('table/black-card/<pk>/', table_black, name='black-tb'),
    path('table/white-cards/<pk>/', table_cards, name='white-tb'),
    path('auth/register/', user_auth, name='register')
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    path('', include('djoser.urls')),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken'), name='djoser'),
    path('rest-auth/', include('rest_framework.urls'), name='rest_framework')
]
