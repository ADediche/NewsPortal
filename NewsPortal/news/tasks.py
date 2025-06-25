from datetime import date, timedelta
from django.core.mail import send_mail

from .models import Post, Category
from django.contrib.auth.models import User


def mailing_news():
    # QuerySet with new news and information about their categories and subscribers emails
    weak_ago = date.today() - timedelta(days = 7)
    posts = Post.objects.filter(create_time__gte = weak_ago). \
        values('id', 'title', 'category__id', 'category__subscribers__email')

    # creating dict with keys - emails and values - list of dicts with information about posts
    dict_of_categories = dict()
    for post in posts:
        posts_information = []
        posts_information.append({'id' : post['id'], 'title' : post['title'], 'category_id' : post['category__id']})
        if post['category__subscribers__email'] not in dict_of_categories.keys():
            dict_of_categories.update({post['category__subscribers__email'] : posts_information})
        else:
            dict_of_categories[post['category__subscribers__email']].append({'id' : post['id'], 'title' : post['title'], 'category_id' : post['category__id']})

    # generation mails for each address and sending them
    for key, value in dict_of_categories.items():
        address = [key]
        mails_text = ''
        for item in value:
            mails_text += 'http://127.0.0.1:8000/news/' + str(item['id']) + '\n'

        send_mail(
           subject = 'Новости за неделю',
           message = mails_text,
           from_email = 'ODarkmanO@yandex.ru',
           recipient_list = address
        )