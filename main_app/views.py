from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

import uuid
import boto3
from .models import Pyrex, Food, Photo

S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'pyrexcollector'

def home(request):
  return render(request, 'home.html')
 
def about(request):
  return render(request, 'about.html')

def pyrexes_index(request):
  pyrexes = Pyrex.objects.all()
  return render(request, 'pyrexes/index.html', {'pyrexes': pyrexes})

def pyrexes_detail(request, pyrex_id):
  pyrex = Pyrex.objects.get(id=pyrex_id)
  return render(request, 'pyrexes/detail.html', { 'pyrex': pyrex })

class PyrexCreate(CreateView):
  model = Pyrex
  fields = '__all__'

class PyrexUpdate(UpdateView):
  model = Pyrex
  fields = ['shape', 'year', 'origin']

class PyrexDelete(DeleteView):
  model = Pyrex
  success_url = '/pyrexes/'

def add_photo(request, cat_id):
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

def assoc_food(request, pyrex_id, food_id):
  Pyrex.objects.get(id=pyrex_id).foods.add(food_id)
  return redirect('detail', pyrex_id=pyrex_id)

def unassoc_food(request, pyrex_id, food_id):
  Pyrex.objects.get(id=pyrex_id).foods.remove(food_id)
  return redirect('detail', pyrex_id=pyrex_id)

class FoodList(ListView):
  model = Food

class FoodDetail(DetailView):
  model = Food

class FoodCreate(CreateView):
  model = Food
  fields = '__all__'

class FoodUpdate(UpdateView):
  model = Food
  fields = ['date_made', 'chef']

class FoodDelete(DeleteView):
  model = Food
  success_url = '/foods/'