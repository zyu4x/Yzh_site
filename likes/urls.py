from likes import views
from django.urls import path

urlpatterns =[
    path('like_change', views.like_change, name='like_change')

]