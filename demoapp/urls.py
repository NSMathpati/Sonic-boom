from django.conf.urls import url
from . import views
from django.urls import path, include

from .views import toggle

app_name = 'music'

urlpatterns = [
    path('toggle/(<album_id>)', views.toggle, name='toggle'),
    path('(<album_id>[0-9]+)/', views.detail, name='detail'),
    path('(<song_id>[0-9]+)/favorite/', views.favorite, name='favorite'),
    path('songs/(<filter_by>[a-zA_Z]+)/', views.songs, name='songs'),
    path('create_album/', views.create_album, name='create_album'),
    path('(<album_id>[0-9]+)/create_song/', views.create_song, name='create_song'),
    path('(<album_id>[0-9]+)/delete_song/(<song_id>[0-9]+)/', views.delete_song, name='delete_song'),
    path('(<album_id>[0-9]+)/favorite_album/', views.favorite_album, name='favorite_album'),
    path('(<album_id>[0-9]+)/delete_album/', views.delete_album, name='delete_album'),
    path('(<album_id>[0-9]+)/share_album/', views.share_album, name='share_album'),
    path('(<album_id>[0-9]+)', views.share_album_detail, name='share_album_detail'),
    path('share/(<album_id>[0-9]+)/(<username>[\w\-]+)/', views.share, name="share"),
    path('unshare/(<album_id>[0-9]+)/(<username>[\w\-]+)/', views.unshare, name="unshare"),
]

from django.contrib.auth import views as auth_views
from django.urls import path,include

from . import views

app_name = 'users'

urlpatterns = [
    # path('index/', views.index, name='index'),
    # path('register/', views.register, name='register'),
    # path('login_user/', views.login_user, name='login_user'),
    # path('logout_user/', views.logout_user, name='logout_user'),
    # path('profile/', views.profile, name="profile"),
    # path('edit_profile/', views.edit_profile, name="edit_profile"),
    # path('update_profile/', views.update_profile, name="update_profile"),
    # path('logout/', views.logout, name="logout"),
    # path('follow_users/', views.follow_users, name="follow_users"),
    # path('follow/(?P<followee_id>\d+)/', views.follow, name="follow"),
    # path('unfollow/(?P<followee_id>\d+)/', views.unfollow, name="unfollow"),
    # path('my_followers/', views.my_followers, name="my_followers"),
    # path('follower_profile/(?P<follower_id>\d+)/', views.follower_profile, name="follower_profile")

    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('profile/', views.profile, name="profile"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('update_profile/', views.update_profile, name="update_profile"),
    path('logout/', views.logout, name="logout"),
    path('follow_users/', views.follow_users, name="follow_users"),
    path('follow/(<followee_id>)/', views.follow, name="follow"),
    path('unfollow/(<followee_id>)/', views.unfollow, name="unfollow"),
    path('my_followers/', views.my_followers, name="my_followers"),
    path('follower_profile/(<follower_id>)/', views.follower_profile, name="follower_profile")
]