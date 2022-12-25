from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('music/', views.music_index, name='music_index'),
    path('music/<int:song_id>/', views.song_detail, name='detail'),
    path('music/create/', views.SongCreate.as_view(), name='music_create'),
    path('music/<int:pk>/update/', views.SongUpdate.as_view(), name='music_update'),
    path('music/<int:pk>/delete/', views.SongDelete.as_view(), name='music_delete'),
    path('music/<int:song_id>/add_session/', views.add_session, name='add_session'),
    path('artists/<int:pk>/', views.ArtistDetail.as_view(), name='artists_detail'),
    path('artists/', views.ArtistList.as_view(), name='artists_index'),
    path('artists/create/', views.ArtistCreate.as_view(), name='artists_create'),
    path('artists/<int:pk>/update/', views.ArtistUpdate.as_view(), name='artists_update'),
    path('artists/<int:pk>/delete/', views.ArtistDelete.as_view(), name='artists_delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('music/<int:song_id>/assoc_artist/<int:artist_id>/', views.assoc_artist, name='assoc_artist'),
    path('music/<int:song_id>/remove_artist/<int:artist_id>/', views.remove_artist, name='remove_artist'),
    path('music/<int:song_id>/add_photo/', views.add_photo, name='add_photo'),

]