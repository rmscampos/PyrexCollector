from django.shortcuts import render
from .models import Pyrex
 
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

