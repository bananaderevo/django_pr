from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import render, get_object_or_404
from .forms import NameForm, FeedbackForm, UpdateProfile
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse

from django.urls import reverse
from django.core.mail import send_mail

from .models import Post, Comments

from .forms import ContactForm

from .tasks import send_mail_to

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_f'] = mod_feedback_c(self.request)
        return context


def profile(request):
    user = request.user
    return render(request, 'user/user_profile.html', {'user': user})


class PublicProfileDetailView(DetailView):
    model = User
    template_name = 'user/user_profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_f'] = mod_feedback_c(self.request)
        return context


class PostUpdateView(UpdateView):
    model = Post
    fields = ['subject', 'short_description', 'text', 'is_published']
    template_name = 'pr/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_f'] = mod_feedback_c(self.request)
        return context


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
    return render(request, 'pr/list-comments.html', {'form': form,
                                                     'names': names,
                                                     })


def mod_feedback(request):
    contact_name = request.POST.get(
        'contact_name'
        , '')
    contact_email = request.POST.get(
        'contact_email'
        , '')
    form_content = request.POST.get('content', '')

    send_mail(subject='Need feedback :(',
              message=f'{form_content}\nMail to feedback: {contact_email}\n Name: {contact_name}',
              from_email='admin@admin',
              recipient_list=['test@test'])
    return HttpResponseRedirect('/')


def mod_feedback_c(request):
    if request.method == 'POST':
        form = FeedbackForm(data=request.POST)
        if form.is_valid():
            mod_feedback(request)
            messages.success(request, 'Mail was successfully sent')
            return form
    else:
        return FeedbackForm()


def postlist(request):
    posts = Post.objects.filter(is_published=True)
    object_list = posts
    paginator = Paginator(object_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'posts': posts,
               'page_obj': page_obj,
               }

    if request.method == 'POST':
        context['messages'] = messages.success(request, 'Mail was successfully sent')

    return render(request, 'pr/list-post.html', context)


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
                                                     'author': author,
                                                     })


def formtobase(request, pk):
    return render(request, 'pr/create.html', {'form_f': mod_feedback_c(request)})


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
        names = Comments.objects.filter(is_published=True)

    # И добавляем names в контекст, чтобы плучить к ним доступ в шаблоне
    return render(request, 'pr/detail-post.html', {'post': post,
                                                   'page_obj': page_obj,
                                                   'form': form,
                                                   'names': names,
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

    return render(request, 'user/user_profile_edit.html', {'form': form,
                                                           })


def allp(request):
    data = dict()
    a = dict()
    o = 0
    for i in Post.objects.all():
        a[f'post{o}'] = {'author': i.author, 'short_description': i.short_description, 'text': i.text}

        o += 1
    data['posts'] = a

    print(a)
    return JsonResponse(a)


def handler404(request, *args, **argv):
    response = render(request, 'errors/404.html')
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, 'errors/500.html')
    response.status_code = 500
    return response


def save_contact(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            data['form_is_valid'] = True

        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            send_mail_to.delay('Support', f'From: {email}\nName: {name}\n{text}', ['admin@admin'])
        return HttpResponseRedirect(reverse('main'))
    else:
        form = ContactForm()
    return save_contact(request, form, 'pr/contact.html')