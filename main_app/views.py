from django.shortcuts import render, redirect
from .models import Music, Artist, Session, Photo
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import SessionForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
import os


# Define the home view
def home(request):
  return render(request, 'home.html')

@login_required
def music_index(request):
    songs = Music.objects.filter(user=request.user)
    return render(request, 'music/index.html', {'songs': songs})

# class MusicList(ListView):
#     model = Music
#     template_name = 'music/index.html'

def about(request):
  return render(request, 'about.html')

@login_required
def song_detail(request, song_id):
  song = Music.objects.get(id=song_id)
  id_list = song.artist.all().values_list('id')
  available_artists = Artist.objects.exclude(id__in=id_list)
  session_form = SessionForm()
  return render(request, 'music/detail.html', { 'song': song,  'session_form':session_form, 'available_artists': available_artists})

# class SongDetail(DetailView):
#   model = Music
#   template_name='music/detail.html'
#   form_class= SessionForm()

class SongCreate(LoginRequiredMixin, CreateView):
  model = Music
  fields = ['title', 'album', 'release_date']
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class SongUpdate(LoginRequiredMixin, UpdateView):
  model = Music
  fields = ['album', 'release_date']

class SongDelete(LoginRequiredMixin, DeleteView):
  model = Music
  success_url = '/music/'

@login_required
def add_session(request, song_id):
  form = SessionForm(request.POST)
  if form.is_valid():
    new_session = form.save(commit=False)
    new_session.song_id = song_id
    new_session.save()
  return redirect('detail', song_id=song_id)

class ArtistList(ListView):
  model = Artist

class ArtistDetail(DetailView):
  model = Artist

class ArtistCreate(LoginRequiredMixin, CreateView):
  model = Artist
  fields = '__all__'

class ArtistUpdate(LoginRequiredMixin, UpdateView):
  model = Artist
  fields = ['name', 'bio']

class ArtistDelete(LoginRequiredMixin, DeleteView):
  model = Artist
  success_url = '/artists/'

def assoc_artist(request, song_id, artist_id):
  Music.objects.get(id=song_id).artist.add(artist_id)
  return redirect('detail', song_id=song_id)

def remove_artist(request, song_id, artist_id):
  Music.objects.get(id=song_id).artist.remove(artist_id)
  return redirect('detail', song_id=song_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('music_index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def add_photo(request, song_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, song_id=song_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', song_id=song_id)