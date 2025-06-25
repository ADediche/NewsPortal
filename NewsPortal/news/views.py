from django.db.models.signals import m2m_changed, post_save
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect

from django.contrib.auth.models import User
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm


# sending welcome letter
def welcome_letter(instance, **kwargs):
    html_content = render_to_string(
        'appointment_created.html',
        {
            'user': User,
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'Добро пожаловать',
        body=instance.username,
        from_email='ODarkmanO@yandex.ru',
        to=[instance.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return redirect('/')



post_save.connect(welcome_letter, sender = User)

# sending mails about a new news
def inform_about_news(instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for value in pk_set:
            qs_of_emails = Category.objects.filter(id=value).values('subscribers__email')
        set_of_emails = set()
        for value in qs_of_emails:
            set_of_emails.add(value['subscribers__email'])
        link = f'http://127.0.0.1:8000/news/{ instance.id }',
        send_mail(
            subject = instance.title,
            message = f'{instance.text} ,{link}',
            from_email = 'ODarkmanO@yandex.ru',
            recipient_list = set_of_emails
        )

m2m_changed.connect(inform_about_news, sender = Post.category.through)

class PostsList(ListView):
    model = Post
    ordering = '-create_time'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')


class CategoriesList(ListView):
    model = Category
    ordering = 'name'
    template_name = 'categories.html'
    context_object_name = 'categories'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # getting a dict with user's categories and adding it in context
        users_categories = Category.objects.all().filter(subscribers=self.request.user.id)
        context['users_categories'] = {}
        for category in users_categories:
            context['users_categories'][category.id] = category.name
        return context


def subscribing(request, pk):
    """adding m2m relationships between categories and user
        get id of category
    """
    category = Category.objects.get(id = pk)
    category.subscribers.add(request.user)
    return redirect('../../categories')
