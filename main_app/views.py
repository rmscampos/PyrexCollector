from django.shortcuts import render
from django.http import HttpResponse

class Pyrex:
    def __init__(self, pattern, shape, year, origin): 
        self.pattern = pattern
        self.shape = shape
        self.year = year
        self.origin = origin

pyrexes = [
    Pyrex('Gooseberry', 'Oval Casserole', 1957, 'US'),
    Pyrex('Butterprint', 'Cinderella Round Casserole', 1957, 'US'),
    Pyrex('Friendship', 'Round Nesting Mixing Bowl', 1971, 'US')
]
 
# Define the home view
def home(request):
  return HttpResponse('<h1>Hello /ᐠ｡‸｡ᐟ\ﾉ</h1>')

def about(request):
  return render(request, 'about.html')

def pyrexes_index(request):
  return render(request, 'pyrexes/index.html', {
      'pyrexes': pyrexes
  })
