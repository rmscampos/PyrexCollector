from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('pyrexes/', views.pyrexes_index, name='index'),
    path('pyrexes/<int:pyrex_id>/', views.pyrexes_detail, name='detail'),
    path('pyrexes/create/', views.PyrexCreate.as_view(), name='pyrexes_create'),
    path('pyrexes/<int:pk>/update/', views.PyrexUpdate.as_view(), name='pyrexes_update'),
    path('pyrexes/<int:pk>/delete/', views.PyrexDelete.as_view(), name='pyrexes_delete'),

    path('pyrexes/<int:pyrex_id>/assoc_food/<int:food_id>/', views.assoc_food, name='assoc_food'),
    path('pyrexes/<int:pyrex_id>/unassoc_food/<int:food_id>/', views.unassoc_food, name='unassoc_food'),
    
    path('foods/', views.FoodList.as_view(), name='foods_index'),
    path('foods/<int:pk>/', views.FoodDetail.as_view(), name='foods_detail'),
    path('foods/create/', views.FoodCreate.as_view(), name='foods_create'),
    path('foods/<int:pk>/update/', views.FoodUpdate.as_view(), name='foods_update'),
    path('foods/<int:pk>/delete/', views.FoodDelete.as_view(), name='foods_delete'),


]