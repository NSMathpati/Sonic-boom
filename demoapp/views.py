from django.shortcuts import render
from itertools import chain

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from models import Album, Song, Shared_album
from .forms import  UserForm
from .models import Friend
from itertools import chain

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse

from .models import Friend
from .forms import AlbumForm, SongForm
from .models import Album, Song, Shared_album
from django.contrib.auth.models import User


# Create your views here.




def index(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html')
    else:
        followee = Friend.objects.filter(follower=request.user)
        friends_albums = []
        for follo in followee:
            x = Album.objects.filter(Q(user=follo.followee)).exclude(is_private=True)
            friends_albums = chain(friends_albums,x)

        received_albums = Shared_album.objects.filter(receiver__username__exact=request.user.username)
        public_albums = Album.objects.exclude(user=request.user).filter(is_private=False)
        albums = Album.objects.filter(user=request.user)
        song_results = Song.objects.all()
        query = request.GET.get("q")
        if query:
            public_albums_search = public_albums.filter(
                Q(album_title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()

            own_albums_search = albums.filter(
                Q(album_title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()

            received_albums_search = received_albums.filter(
                Q(album_title__album_title__icontains=query) |
                Q(album_title__artist__icontains=query)
            ).distinct()

            song_results = song_results.filter(
                Q(song_title__icontains=query)
            ).distinct()

            return render(request, 'users/index.html', {
                'public_albums_search': public_albums_search,
                'received_albums_search' : received_albums_search,
                'own_albums_search': own_albums_search,
                'query':query,
                'songs': song_results,
            })
        else:
            context = {
                'albums': albums , # unique albums
                'received_albums': received_albums,
                'public_albums': public_albums,
                'friends_albums': friends_albums
            }
            return render(request, 'users/index.html', context )

def home(request):
    return render(request,'home.html')

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'users/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            request.session['username'] = user.username
            request.session['id'] = user.id
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            request.session['email'] = user.email
            request.session['password'] = user.password
            if user.is_active:
                login(request, user)
                followee = Friend.objects.filter(follower=request.user)
                friends_albums = []
                for follo in followee:
                    x = Album.objects.filter(Q(user=follo.followee)).exclude(is_private=True)
                    friends_albums = chain(friends_albums, x)

                received_albums = Shared_album.objects.filter(receiver=request.user)
                public_albums = Album.objects.exclude(user=request.user).filter(is_private=False)
                albums = Album.objects.filter(user=request.user)
                context = {
                    'albums': albums,  # unique albums
                    'received_albums': received_albums,
                    'public_albums': public_albums,
                    'friends_albums': friends_albums
                }
                return render(request, 'users/index.html', context)
            else:
                return render(request, 'users/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'users/login.html', {'error_message': 'Invalid login'})
    return render(request, 'users/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        last_name = form.cleaned_data['last_name']
        first_name = form.cleaned_data['first_name']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        request.session['username'] = user.username
        request.session['id'] = user.id
        request.session['first_name'] = user.first_name
        request.session['last_name'] = user.last_name
        request.session['email'] = user.email
        request.session['password'] = user.password
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'users/index.html', {'albums': albums})
    context = {
        "form": form,
    }
    return render(request, 'users/register.html', context)

def profile(request):
    followee = Friend.objects.filter(follower__username__exact=request.user.username)
    following_count = followee.count()
    friends_albums = []
    for follo in followee:
        x = Album.objects.filter(Q(user=follo.followee)).exclude(is_private=True)
        friends_albums = list(chain(friends_albums, x))

    print(friends_albums)

    received_albums = Shared_album.objects.filter(receiver=request.user)

    public_albums = Album.objects.exclude(user=request.user).filter(is_private=False)
    private_albums = Album.objects.filter(user=request.user,is_private=True)

    #find folowers count
    followers = Friend.objects.filter(followee__username__exact=request.user.username)
    followers_count = followers.count()

    #find shared_albums which are private
    list_of_ids = []
    for pa in private_albums:
        list_of_ids.append(pa.id)

    shared_albums = Shared_album.objects.filter(album_title_id__in=list_of_ids)

    context = {
        'private_albums': private_albums,  # unique albums
        'received_albums': received_albums,
        'public_albums': public_albums,
        'shared_albums':shared_albums,
        'friends_albums': friends_albums,
        'following_count':following_count,
        'followers_count': followers_count
    }
    return render(request, 'users/profile.html', context)


def edit_profile(request):
    return render(request, 'users/edit_profile.html')


def update_profile(request):
    if request.method == "POST":
        server_firstname = request.POST['first_name']
        server_lastname = request.POST['last_name']
        server_password = request.POST['password']
        if server_password == request.POST['confirm_password']:
            try:
                user = User.objects.get(username = request.session['username'])
                user.first_name = server_firstname
                user.last_name = server_lastname
                user.password = server_password
                user.save()
                request.session['first_name'] = user.first_name
                request.session['last_name'] = user.last_name
                request.session['password'] = user.password
                return render(request,'users/profile.html')
            except:
                messages.error(request, 'ERROR: Invalid inputs, try again!')
                return render(request,'users/edit_profile.html')
        else:
            messages.error(request, 'ERROR: Passwords do not match, try again!')
            return render(request,'users/edit_profile.html')
    else:
        messages.error(request, 'ERROR: Invalid inputs, try again!')
        return render(request,'users/edit_profile.html')


def follow_users(request):
    context = {
        "notfriends": User.objects.exclude(id=request.session['id']).exclude(followers__follower_id=request.session['id']),
        "friends": User.objects.filter(followers__follower_id=request.session['id'])
    }
    return render(request, 'users/follow_users.html', context)


def follow(request, followee_id):
    Friend.objects.create(follower_id=request.session['id'], followee_id=followee_id)
    context = {
        "notfriends": User.objects.exclude(id=request.session['id']).exclude(
            followers__follower_id=request.session['id']),
        "friends": User.objects.filter(followers__follower_id=request.session['id'])
    }
    return render(request,'users/follow_users.html',context)


def unfollow(request, followee_id):
    Friend.objects.filter(followee_id=followee_id).delete()
    context = {
        "notfriends": User.objects.exclude(id=request.session['id']).exclude(
            followers__follower_id=request.session['id']),
        "friends": User.objects.filter(followers__follower_id=request.session['id'])
    }
    return render(request,'users/follow_users.html',context)


def my_followers(request):
    context = {
        "my_followers": Friend.objects.filter(followee__id=request.session['id'])
        }
    return render(request, 'users/my_followers.html', context)


def follower_profile(request, follower_id):
    context = {
        "friend": Friend.objects.get(id=follower_id)
    }
    return render(request, 'users/follower_profile.html', context)


AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_album(request):
    if not request.user.is_authenticated:
        return render(request, '../templates/users/login.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.is_private = form.cleaned_data['is_private']
            album.user = request.user
            album.album_logo = request.FILES['album_logo']
            file_type = album.album_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, '../templates/music/create_album.html', context)
            album.save()
            return render(request, '../templates/music/detail.html', {'album': album})
        context = {
            "form": form,
        }
        return render(request, '../templates/music/create_album.html', context)


def create_song(request, album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        albums_songs = album.song_set.all()
        for s in albums_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, '../templates/music/create_song.html', context)
        song = form.save(commit=False)
        song.album = album
        song.audio_file = request.FILES['audio_file']
        file_type = song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request, '../templates/music/create_song.html', context)
        album.total_songs = album.total_songs + 1
        album.save()
        song.save()
        return render(request, '../templates/music/detail.html', {'album': album})
    context = {
        'album': album,
        'form': form,
    }
    return render(request, '../templates/music/create_song.html', context)


def delete_album(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.delete()
    albums = Album.objects.filter(user=request.user)
    followee = Friend.objects.filter(follower=request.user)
    friends_albums = []
    for follo in followee:
        x = Album.objects.filter(Q(user=follo.followee)).exclude(is_private=True)
        friends_albums = chain(friends_albums, x)

    received_albums = Shared_album.objects.filter(receiver=request.user)
    public_albums = Album.objects.exclude(user=request.user).filter(is_private=False)
    context = {
        'albums': albums,  # unique albums
        'received_albums': received_albums,
        'public_albums': public_albums,
        'friends_albums': friends_albums
    }
    return render(request, 'users/index.html', context)


def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Song.objects.get(pk=song_id)
    album.total_songs -= 1
    album.save()
    song.delete()
    return render(request, '../templates/music/detail.html', {'album': album})


def detail(request, album_id):
    if not request.user.is_authenticated:
        return render(request, '../templates/users/login.html')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=album_id)
        return render(request, '../templates/music/detail.html', {'album': album, 'user': user})


def favorite(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def songs(request, filter_by):
    if not request.user.is_authenticated:
        return render(request, '../templates/users/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Album.DoesNotExist:
            users_songs = []
        return render(request, '../templates/music/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })

def toggle(request,album_id):
    print("inside toggle")
    w = get_object_or_404(Album, pk=album_id)
    w.is_private = not w.is_private
    w.save()
    user = request.user
    album = get_object_or_404(Album, pk=album_id)
    return render(request, '../templates/music/detail.html', {'album': album, 'user': user})


def share_album(request, album_id):
    album = get_object_or_404(Album,pk=album_id)
    already_shared_users = Shared_album.objects.filter(album_title=album)
    all_users_objects = User.objects.exclude(username=request.user.username)
    
    all_users = []
    for u in all_users_objects:
        all_users.append(u.username)

    shared_users_list = []
    for u in already_shared_users:
        shared_users_list.append(u.receiver.username)

    unshared_users = list(set(all_users) - set(shared_users_list))

    context = {
        "shared_users": shared_users_list,
        "unshared_users":unshared_users,
        "album_id": album_id
    }
    return render(request,'../templates/music/share_album.html',context)

def share_album_detail(request, album_id):
    if not request.user.is_authenticated:
        return render(request, '../templates/users/login.html')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=album_id)
        return render(request, '../templates/music/shared_album_detail.html', {'album': album, 'user': user})


def share(request,album_id,username):
    album = get_object_or_404(Album,pk=album_id)
    receiver = get_object_or_404(User,username=username)
    Shared_album.objects.create(owner=request.user,receiver=receiver,album_title=album)
    return share_album(request,album_id)

def unshare(request,album_id,username):
    album = Shared_album.objects.filter(receiver__username=username,album_title=get_object_or_404(Album,pk=album_id))
    print(album)
    album.delete()
    return share_album(request,album_id)