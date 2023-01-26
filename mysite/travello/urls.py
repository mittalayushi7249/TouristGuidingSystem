from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('place',views.place,name='place'),
    path('register',views.signup,name='register'),
    path('login',views.signin,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('places/<str:place>',views.view_place,name='places'),
    path('feedback',views.feedback,name='feedback'),
]