from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .forms import CommentsForm

from django.urls import reverse_lazy
from django.views import generic
from django.core.mail import send_mail
from .forms import UserForm, ProfileForm

from .models import Post, Comments


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['text']
    success_url = '/'
    template_name = 'pr/create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.author = post.user
        post.author.id = self.request.user.id
        post.save()
        send_mail(subject='New Post',
                  message=f'New post was added: {post.text}\nAuthor: {post.author}',
                  from_email='admin@admin',
                  recipient_list=['test@test'])
        self.object = post
        return super().form_valid(form)


class Profile(DetailView):
    model = User
    template_name = 'user/user_profile.html'
    context_object_name = 'user'


class PostListView(ListView):
    model = Post
    paginate_by = 10
    fields = ['text', 'author']
    template_name = 'pr/list-post.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'pr/detail-post.html'
    context_object_name = 'post'


class CommentsListView(ListView):
    model = Comments
    fields = ['text', 'author', 'post']
    template_name = 'pr/list-comments.html'
# def post_detail(request, id):
#     post = get_object_or_404(Post, id=id,)
#     # List of active comments for this post
#     comments = post.comments.all()
#
#     if request.method == 'POST':
#         # A comment was posted
#         comment_form = CommentsForm(data=request.POST)
#         if comment_form.is_valid():
#             # Create Comment object but don't save to database yet
#             new_comment = comment_form.save(commit=False)
#             # Assign the current post to the comment
#             new_comment.post = post
#             # Save the comment to the database
#             new_comment.save()
#     else:
#         comment_form = CommentsForm()
#     return render(request,
#                   'pr/detail-post.html',
#                  {'post': post,
#                   'comments': comments,
#                   'comment_form': comment_form})