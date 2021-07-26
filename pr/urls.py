from django.urls import path

from .views import PostCreateView, PostListView, Profile, show_post, create_com


urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create'),
    path('<int:pk>', Profile.as_view(), name='profile'),
    path('', PostListView.as_view(), name='create'),
    path('post/<int:id>', show_post, name='post'),
    path('post/<int:id>/comment', create_com, name='comment'),
    # path('c/<int:id>', get_name, name='name'),

    # path('post/<int:pk>', CommentsListView.as_view(), name='post'),

]