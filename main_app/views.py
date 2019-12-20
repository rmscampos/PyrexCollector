from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from .models import Pyrex, Food

 
# Define the home view
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