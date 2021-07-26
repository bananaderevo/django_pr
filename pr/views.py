from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import render, get_object_or_404
from .forms import NameForm, FeedbackForm
from django.http import HttpResponseRedirect

from django.urls import reverse
from django.views import generic
from django.core.mail import send_mail
from .forms import UserForm, ProfileForm

from .models import Post, Comments

from django.shortcuts import render


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


class ProfileUpdateView(UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'short_description', 'description']
    template_name = 'user/user_profile_edit.html'


class PostListView(ListView):
    model = Post
    paginate_by = 10
    fields = ['text', 'author']
    template_name = 'pr/list-post.html'


def show_post(request, id):
    post = get_object_or_404(Post, id=id)
    object_list = post.comments.all().order_by('-id')

    paginator = Paginator(object_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pr/detail-post.html', {'post': post,
                                                   'page_obj': page_obj,
                                                   })


# def create_com(request, id):
#
#     if request.method == 'POST':
#
#         form = NameForm(request.POST)
#
#         if form.is_valid():
#             # Сохранение формы
#             form.save()
#
#             # Редирект на ту же страницу
#             return HttpResponseRedirect(request.path_info)
#
#     else:
#     # метод GET
#
#         form = NameForm()
#
#         # Получение всех имен из БД.
#         names = Comments.objects.all()
#
#     # И добавляем names в контекст, чтобы плучить к ним доступ в шаблоне
#     return render(request, 'pr/list-comments.html', {'form': form, 'names': names})

def create_com(request, id):

    if request.method == 'POST':
        form = NameForm(request.POST)

        if form.is_valid():
            # Сохранение формы
            form.save()
            Post.objects.get(id=id).comments.add(Comments.objects.last().id)
            post = form.save(commit=False)
            if request.user.is_authenticated:

                post.user = request.user
                post.author = post.user
                post.author.id = request.user.id
                post.save()
            else:
                post.user = AnonymousUser()
                # post.author = AnonymousUser()
                # post.author.id = request.user.id
                post.save()
            # Редирект на ту же страницу
            return HttpResponseRedirect(reverse('post', kwargs={'id': id}))

    else:
    # метод GET

        form = NameForm()

        # Получение всех имен из БД.
        names = Comments.objects.all()

    # И добавляем names в контекст, чтобы плучить к ним доступ в шаблоне
    return render(request, 'pr/list-comments.html', {'form': form, 'names': names})


def feedback(request):

    if request.method == 'POST':
        form = FeedbackForm(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name'
                , '')
            contact_email = request.POST.get(
                'contact_email'
                , '')
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            send_mail(subject='Need feedback :(',
                      message=f'{form_content}\nMail to feedback: {contact_email}\n Name: {contact_name}',
                      from_email='admin@admin',
                      recipient_list=['test@test'])
            return HttpResponseRedirect('/')

    return render(request, 'pr/feedback.html', {
        'form': FeedbackForm,
    })


def handler404(request, *args, **argv):
    response = render(request, 'errors/404.html')
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, 'errors/500.html')
    response.status_code = 500
    return response
