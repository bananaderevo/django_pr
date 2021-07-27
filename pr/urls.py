from django.urls import path

from .views import PostCreateView, PostListView, profile, update_profile, show_post, feedback, userpost


urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create'),
    path('feedback/', feedback, name='feedback'),
    path('', PostListView.as_view(), name='main'),
    path('post/<int:id>', show_post, name='post'),
    path('profile', profile, name='profile'),
    path('profile/edit', update_profile, name='profile-edit'),
    path('profile/<int:id>/posts', userpost, name='user-posts'),

]

handler404 = 'pr.views.handler404'
handler500 = 'pr.views.handler500'

