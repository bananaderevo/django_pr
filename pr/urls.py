from django.urls import path

from .views import PostCreateView, PublicProfileDetailView, profile, update_profile, show_post, feedback, userpost, PostUpdateView, postlist


urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create'),
    path('feedback/', feedback, name='feedback'),
    path('', postlist, name='main'),
    path('post/<int:id>', show_post, name='post'),
    path('profile', profile, name='profile'),
    path('profile/edit', update_profile, name='profile-edit'),
    path('profile/<int:id>/posts', userpost, name='user-posts'),
    path('post/<int:pk>/edit', PostUpdateView.as_view(), name='post-edit'),
    path('profile/<int:pk>', PublicProfileDetailView.as_view(), name='public-profile'),

]

handler404 = 'pr.views.handler404'
handler500 = 'pr.views.handler500'

