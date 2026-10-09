from .filters import PostsFilter
from .forms import PostForm
from .models import Post
from .services import RequestsService
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)


@login_required
def add_user_to_authors(request):
    if not request.user.groups.filter(name='authors').exists():
        group = Group.objects.get(name='authors')

        request.user.groups.add(group)
        request.user.save()

    return redirect('/')


class PostCreate(PermissionRequiredMixin, CreateView):
    model = Post

    form_class = PostForm
    template_name = 'post_edit.html'

    permission_required = ('news.add_post')

    def dispatch(self, request, *args, **kwargs):
        if 'articles' in request.get_full_path():
            self.model.post_type = Post.POST_TYPE_ARTICLE
        else:
            self.model.post_type = Post.POST_TYPE_NEWS

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Получаем обычный контекст
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст
        if self.model.post_type == Post.POST_TYPE_ARTICLE:
            context['title'] = 'Article Create'
        else:
            context['title'] = 'News Create'
        context['url_back'] = RequestsService.peek().get_full_path()
        # Возвращаем контекст
        return context


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post

    context_object_name = 'post'
    template_name = 'post_delete.html'

    permission_required = ('news.delete_post')

    def get_context_data(self, **kwargs):
        # Получаем обычный контекст
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст
        context['url_back'] = RequestsService.peek().get_full_path()
        # Возвращаем контекст
        return context

    def get_success_url(self):
        params = RequestsService.peek().GET.copy()
        # Удаляем параметр page
        if params.get('page'):
            params.pop('page')
        # Формируем и возвращаем новый url
        if len(params) == 0:
            return f'{RequestsService.peek().path}'
        else:
            return  f'{RequestsService.peek().path}?{params.urlencode()}'


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post

    context_object_name = 'post'
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        # Получаем обычный контекст
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст
        context['url_back'] = RequestsService.peek().get_full_path()
        # Возвращаем контекст
        return context


class PostEdit(PermissionRequiredMixin, UpdateView):
    model = Post

    form_class = PostForm
    template_name = 'post_edit.html'

    permission_required = ('news.change_post')

    def get_context_data(self, **kwargs):
        # Получаем обычный контекст
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст
        context['title'] = 'Post Edit'
        context['url_back'] = RequestsService.peek().get_full_path()
        # Возвращаем контекст
        return context


class PostsList(LoginRequiredMixin, ListView):
    model = Post

    ordering = '-date'
    paginate_by = 10

    context_object_name = 'posts'
    template_name = 'posts_list.html'

    def dispatch(self, request, *args, **kwargs):
        RequestsService.push(request)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Получаем обычный контекст
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст
        context['is_user_author'] = self.request.user.groups.filter(name='authors').exists()
        context['posts_count'] = Post.objects.count()
        # Возвращаем контекст
        return context


class PostsSearch(LoginRequiredMixin, ListView):
    model = Post

    ordering = '-date'
    paginate_by = 10

    context_object_name = 'posts'
    template_name = 'posts_search.html'

    def dispatch(self, request, *args, **kwargs):
        RequestsService.push(request)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем класс фильтрации
        self.filterset = PostsFilter(self.request.GET, queryset)
        # Возвращаем отфильтрованный список
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        # Получаем обычный контекст
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст
        context['filterset'] = self.filterset
        context['is_user_author'] = self.request.user.groups.filter(name='authors').exists()
        context['posts_count'] = Post.objects.count()
        context['posts_find'] = self.filterset.qs.count()
        # Возвращаем контекст
        return context