from django.urls import path

from .views import CommentsListView, PostCreateView, PostDetailView, PostListView, Profile


urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create'),
    path('<int:pk>', Profile.as_view(), name='profile'),
    path('', PostListView.as_view(), name='create'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post'),
    path('post/<int:pk>', CommentsListView.as_view(), name='post'),

]