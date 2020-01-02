from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import uuid
import boto3
from .models import Pyrex, Food, Photo

S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'pyrexcollector'

def home(request):
  return render(request, 'home.html')
 
def about(request):
  return render(request, 'about.html')

@login_required
def pyrexes_index(request):
  pyrexes = Pyrex.objects.filter(user=request.user)
  return render(request, 'pyrexes/index.html', {'pyrexes': pyrexes})

@login_required
def pyrexes_detail(request, pyrex_id):
  pyrex = Pyrex.objects.get(id=pyrex_id)
  return render(request, 'pyrexes/detail.html', { 'pyrex': pyrex })

class PyrexCreate(LoginRequiredMixin, CreateView):
  model = Pyrex
  fields = '__all__'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)


class PyrexUpdate(LoginRequiredMixin, UpdateView):
  model = Pyrex
  fields = ['shape', 'year', 'origin']

class PyrexDelete(LoginRequiredMixin, DeleteView):
  model = Pyrex
  success_url = '/pyrexes/'

@login_required
def add_photo(request, pyrex_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, pyrex_id=pyrex_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', pyrex_id=pyrex_id)

@login_required
def assoc_food(request, pyrex_id, food_id):
  Pyrex.objects.get(id=pyrex_id).foods.add(food_id)
  return redirect('detail', pyrex_id=pyrex_id)

@login_required
def unassoc_food(request, pyrex_id, food_id):
  Pyrex.objects.get(id=pyrex_id).foods.remove(food_id)
  return redirect('detail', pyrex_id=pyrex_id)

class FoodList(LoginRequiredMixin, ListView):
  model = Food

class FoodDetail(LoginRequiredMixin, DetailView):
  model = Food

class FoodCreate(LoginRequiredMixin, CreateView):
  model = Food
  fields = '__all__'

class FoodUpdate(LoginRequiredMixin, UpdateView):
  model = Food
  fields = ['date_made', 'chef']

class FoodDelete(LoginRequiredMixin, DeleteView):
  model = Food
  success_url = '/foods/'


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
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)