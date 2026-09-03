from django.contrib.auth.models import User
from news.models import Author, Category, Comment, Post

# Шаг 1
user_1 = User.objects.create(username='user_1')
user_2 = User.objects.create(username='user_2')

# Шаг 2
author_1 = Author.objects.create(user=user_1)
author_2 = Author.objects.create(user=user_2)

# Шаг 3
category_1 = Category.objects.create(name='Спорт')
category_2 = Category.objects.create(name='Техника')
category_3 = Category.objects.create(name='Здоровье')
category_4 = Category.objects.create(name='Общество')

# Шаг 4 и 5
post_1 = Post()
post_1.post_type = Post.type_news
post_1.title = 'Новость 1'
post_1.text = ('Текст новости 1 Текст новости 1 Текст новости 1 Текст новости 1 Текст новости 1 Текст новости 1 Текст '
               'новости 1')
post_1.author = author_1
post_1.save()
post_1.categories.add(category_1)
post_1.categories.add(category_2)
post_1.save()

post_2 = Post()
post_2.title = 'Статья 1'
post_2.text = ('Текст статьи 1 Текст статьи 1 Текст статьи 1 Текст статьи 1 Текст статьи 1 Текст статьи 1 Текст статьи '
               '1 Текст статьи 1')
post_2.author = author_1
post_2.save()
post_2.categories.add(category_3)
post_2.save()

post_3 = Post()
post_3.title = 'Статья 2'
post_3.text = ('Текст статьи 2 Текст статьи 2 Текст статьи 2 Текст статьи 2 Текст статьи 2 Текст статьи 2 Текст статьи '
               '2 Текст статьи 2')
post_3.author = author_2
post_3.save()
post_3.categories.add(category_4)
post_3.save()

# Шаг 6
comment_1 = Comment.objects.create(text='Комментарий 1 Новость 1', post=post_1, user=user_1)

comment_2 = Comment.objects.create(text='Комментарий 1 Статья 1', post=post_2, user=user_1)
comment_3 = Comment.objects.create(text='Комментарий 2 Статья 1', post=post_2, user=user_2)

comment_4 = Comment.objects.create(text='Комментарий 1 Статья 2', post=post_3, user=user_2)

# Шаг 7
post_1.like()
post_1.like()
post_1.like()
post_1.dislike()

post_2.like()
post_2.like()
post_2.like()

post_3.like()
post_3.like()
post_3.like()
post_3.like()

comment_1.like()
comment_2.like()
comment_2.like()
comment_3.like()
comment_3.like()
comment_3.like()
comment_4.like()
comment_4.like()
comment_4.like()
comment_4.like()

# Шаг 8
author_1.update_rating()
author_2.update_rating()

# Шаг 9
best_author = Author.objects.order_by("-rating")[0]

print("Лучший пользователь:")
print("Имя -", User.objects.get(id=best_author.user_id).username)
print("Рейтинг -", best_author.rating)

# Шаг 10
best_post = Post.objects.order_by("-rating")[0]

print("Лучшая статья:")
print("Дата добавления -", best_post.date)
print("Имя автора -", User.objects.get(id=best_post.author_id).username)
print("Рейтинг -", best_post.rating)
print("Заголовок -", best_post.title)
print("Превью -", best_post.preview())

# Шаг 11
best_post_comments = Comment.objects.filter(post=best_post)

print("Комментарии к лучшей статье:")
for comment in best_post_comments:
    print("Дата добавления -", comment.date)
    print("Имя пользователя -", User.objects.get(id=comment.user_id).username)
    print("Рейтинг -", comment.rating)
    print("Текст -", comment.text)

"""
author_1 = Author.objects.get(user=User.objects.get(username='user_1'))
author_2 = Author.objects.get(user=User.objects.get(username='user_1'))
"""