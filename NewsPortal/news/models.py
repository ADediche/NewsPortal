from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    rating = models.IntegerField(default = 0)

    def update_rating(self):
        posts_rating = Post.objects.filter(author = self).values('rating')
        comments_rating = Comment.objects.filter(user=self.user).values('rating')
        comments_posts_rating = Comment.objects.filter(post__author=self).values('rating')
        posts_rating_values = 0
        comments_rating_values = 0
        comments_posts_rating_values = 0
        for i in posts_rating:
            posts_rating_values = posts_rating_values + i['rating']
        for i in comments_rating:
            comments_rating_values = comments_rating_values + i['rating']
        for i in comments_posts_rating:
            comments_posts_rating_values = comments_posts_rating_values + i['rating']
            self.rating = posts_rating_values * 3 + comments_rating_values + comments_posts_rating_values
            self.save()

class Category(models.Model):
    name = models.CharField(max_length = 40,
                            unique = True,
                            null=False)

    def __str__(self):
        return f'{self.name.title()}'

class Post(models.Model):
    news = 'NE'
    article = 'AR'

    TIPE = [
        (news, 'Новость'),
        (article, 'Статья'),
    ]

    author = models.ForeignKey('Author', on_delete = models.CASCADE, null = False)
    tipe = models.CharField(max_length = 2,
                            choices = TIPE,
                            null = False)
    create_time = models.DateTimeField(auto_now_add = True)
    category = models.ManyToManyField(Category, through = 'PostCategory')
    title = models.CharField(max_length = 100, null = False)
    text = models.TextField(max_length = 5000, null = False)
    rating = models.IntegerField(default = 0)

    def __str__(self):
        return f'{self.title} {self.create_time} {self.text[:20]}'

    def preview(self):
        return self.text[0 : 124] + '...'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.TextField(max_length = 1000)
    create_time = models.DateTimeField(auto_now_add = True)
    rating = models.IntegerField(default = 0)

    def like(self):
        self.rating = self.rating + 1
        self.save()

    def dislike(self):
        self.rating = self.rating - 1
        self.save()