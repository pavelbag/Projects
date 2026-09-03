from django.db import models
from django.db.models import Q
from django.db.models import Sum
from django.contrib.auth.models import User


class Author(models.Model):
    rating = models.IntegerField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    objects = models.Manager

    def update_rating(self):
        # Выбираем все посты автора
        posts = Post.objects.filter(author=self)
        # Выбираем все комментарии автора
        own_comments = Comment.objects.filter(user=self.user)
        # Выбираем все комментарии не автора
        not_own_comments = Comment.objects.filter(~Q(user=self.user))

        rating_1 = posts.aggregate(Sum("rating"))["rating__sum"]
        rating_2 = own_comments.aggregate(Sum("rating"))["rating__sum"]
        rating_3 = not_own_comments.filter(post__in=posts).aggregate(Sum("rating"))["rating__sum"]

        rating_1 = 0 if rating_1 is None else rating_1
        rating_2 = 0 if rating_2 is None else rating_2
        rating_3 = 0 if rating_3 is None else rating_3

        self.rating = rating_1 * 3 + rating_2 + rating_3
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    objects = models.Manager


class Post(models.Model):
    type_article = 'A'
    type_news = 'N'

    POST_TYPES = [
        (type_article, 'Статья'),
        (type_news, 'Новость')
    ]

    post_type = models.CharField(max_length=1, choices=POST_TYPES, default=type_article)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, through='PostCategory')

    objects = models.Manager

    def dislike(self):
        self.rating -= 1
        self.save()

    def like(self):
        self.rating += 1
        self.save()

    def preview(self):
        return self.text[0:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    objects = models.Manager


class Comment(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = models.Manager

    def dislike(self):
        self.rating -= 1
        self.save()

    def like(self):
        self.rating += 1
        self.save()