from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import render, get_object_or_404
from .forms import NameForm, FeedbackForm, UpdateProfile
from django.http import HttpResponseRedirect

from django.urls import reverse
from django.core.mail import send_mail

from .models import Post, Comments


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['subject', 'short_description', 'text', 'is_published']
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


def profile(request):
    user = request.user
    return render(request, 'user/user_profile.html', {'user': user})


class PublicProfileDetailView(DetailView):
    model = User
    template_name = 'user/user_profile.html'
    context_object_name = 'user'


class PostUpdateView(UpdateView):
    model = Post
    fields = ['subject', 'short_description', 'text', 'is_published']
    template_name = 'pr/create.html'


def profile_edit(request):

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


def postlist(request):
    posts = Post.objects.filter(is_published=True)
    object_list = posts
    paginator = Paginator(object_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pr/list-post.html', {'posts': posts,
                                                 'page_obj': page_obj})


def userpost(request, id):
    author = get_object_or_404(User, id=id)
    posts = Post.objects.filter(author=author)
    print(posts)
    object_list = posts
    paginator = Paginator(object_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pr/list-userpost.html', {'posts': posts,
                                                     'page_obj': page_obj,
                                                     'author': author})


def show_post(request, id):
    post = get_object_or_404(Post, id=id)
    object_list = post.comments.filter(is_published=True).order_by('-id')

    paginator = Paginator(object_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        form = NameForm(request.POST)

        if form.is_valid():
            # Сохранение формы
            form.save()
            Post.objects.get(id=id).comments.add(Comments.objects.last().id)
            email = Post.objects.get(id=id).author.email
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
            send_mail(subject='New comment!',
                      message=f'New comment was added for checking: {Comments.objects.last().name}\n'
                              f'Author: {Comments.objects.last().author}\n'
                              f'Link: domain.com{request.path}',
                      from_email='admin@admin',
                      recipient_list=[email, 'admin@admin'])
            return HttpResponseRedirect(reverse('post', kwargs={'id': id}))

    else:
    # метод GET

        form = NameForm()

        # Получение всех имен из БД.
        names = Comments.objects.all()

    # И добавляем names в контекст, чтобы плучить к ним доступ в шаблоне
    return render(request, 'pr/detail-post.html', {'post': post,
                                                   'page_obj': page_obj,
                                                   'form': form, 'names': names})


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


def update_profile(request):
    args = {}

    if request.method == 'POST':
        form = UpdateProfile(request.POST, instance=request.user)
        form.actual_user = request.user
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = UpdateProfile()

    return render(request, 'user/user_profile_edit.html', {'form': form})


def handler404(request, *args, **argv):
    response = render(request, 'errors/404.html')
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, 'errors/500.html')
    response.status_code = 500
    return response
