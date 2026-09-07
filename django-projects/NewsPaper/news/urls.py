from django.urls import path
from .views import NewsDetail, NewsList

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsDetail.as_view()),
]