from django import (
    urls,
    utils,
)
from django.contrib import auth
from django.db import models


class Author(models.Model):
    rating = models.IntegerField(default=0)

    user = models.OneToOneField(auth.models.User, on_delete=models.CASCADE)

    def update_rating(self):
        # Выбираем все посты автора
        posts = Post.objects.filter(author=self)
        # Выбираем все комментарии автора
        own_comments = Comment.objects.filter(user=self.user)
        # Выбираем все комментарии не автора
        not_own_comments = Comment.objects.filter(~models.Q(user=self.user))

        rating_1 = posts.aggregate(models.Sum('rating'))['rating__sum']
        rating_2 = own_comments.aggregate(models.Sum('rating'))['rating__sum']
        rating_3 = not_own_comments.filter(post__in=posts).aggregate(models.Sum('rating'))['rating__sum']

        rating_1 = 0 if rating_1 is None else rating_1
        rating_2 = 0 if rating_2 is None else rating_2
        rating_3 = 0 if rating_3 is None else rating_3

        self.rating = rating_1 * 3 + rating_2 + rating_3
        self.save()

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name}'


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    POST_TYPE_ARTICLE = 'A'
    POST_TYPE_NEWS = 'N'

    POST_TYPES = [
        (POST_TYPE_ARTICLE, 'Статья'),
        (POST_TYPE_NEWS, 'Новость'),
    ]

    date = models.DateTimeField(default=utils.timezone.now)
    post_type = models.CharField(max_length=1, choices=POST_TYPES, default=POST_TYPE_ARTICLE)
    rating = models.IntegerField(default=0)
    title = models.CharField(max_length=255)
    text = models.TextField()

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, through='PostCategory')

    def dislike(self):
        self.rating -= 1
        self.save()

    def like(self):
        self.rating += 1
        self.save()

    def preview(self):
        return self.text[0:124] + '...'

    def get_absolute_url(self):
        return urls.reverse('post_detail', args=[str(self.pk)])


class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    text = models.TextField()

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(auth.models.User, on_delete=models.CASCADE)

    def dislike(self):
        self.rating -= 1
        self.save()

    def like(self):
        self.rating += 1
        self.save()