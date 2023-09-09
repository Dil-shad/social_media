from django.urls import path
from . import views


urlpatterns = [

    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login', views.signin, name='login'),
    path('logout', views.logout, name='logout'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    path('profile/<str:pk>', views.ProfileView, name='profile'),
    path('like-post', views.like_post, name='like-post'),
    path('delete-post/<str:pk>', views.deletePost, name='delete-post'),
    



]
