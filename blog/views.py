from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Post, Category, Author, Comment
from .forms import CommentForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import translation
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SubscriberForm
from .models import Author
from django.utils.translation import gettext_lazy as _

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().filter(status='published')
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, Q(slug=category_slug) | Q(slug_en=category_slug))
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class AuthorPostListView(ListView):
    model = Post
    template_name = 'blog/author_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))

        if not user.has_perm('blog.add_post'):
            raise Http404("Bu kullanıcının yazar profili bulunmamaktadır.")

        author = get_object_or_404(Author, user=user)
        return Post.objects.filter(author=author, status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['author'] = get_object_or_404(Author, user=user)
        return context


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.filter(active=True, parent__isnull=True)
    active_comments_count = post.comments.filter(active=True).count()
    comment_form = CommentForm(user=request.user)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST, user=request.user)
        if comment_form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except (ValueError, TypeError):
                parent_id = None

            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)

            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.parent = parent_obj

            if request.user.is_authenticated:
                new_comment.user = request.user
                if not new_comment.name:
                    new_comment.name = request.user.get_full_name() or request.user.username
                if not new_comment.email:
                    new_comment.email = request.user.email

            new_comment.save()
            return redirect(post.get_absolute_url() + f'#comment-{new_comment.id}')

    current_language = translation.get_language()
    display_title = post.title
    display_content = post.content
    if current_language == 'en' and post.title_en and post.content_en:
        display_title = post.title_en
        display_content = post.content_en

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'active_comments_count': active_comments_count,
        'display_title': display_title,
        'display_content': display_content,
    }
    return render(request, 'blog/post_detail.html', context)


def search_view(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) |
            Q(title_en__icontains=query) | Q(content_en__icontains=query),
            status='published'
        ).distinct()

    paginator = Paginator(results, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,
                  'blog/search_results.html',
                  {'query': query,
                   'page_obj': page_obj})


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Author.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} için hesap oluşturuldu! Şimdi giriş yapabilirsiniz.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.author)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profiliniz başarıyla güncellendi!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.author)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'blog/profile.html', context)


def newsletter_subscribe_view(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Bültenimize başarıyla abone oldunuz! Teşekkürler.'))
        else:
            error_message = form.errors.get('__all__') or form.errors.get('email')
            messages.error(request, error_message)
    return redirect(request.META.get('HTTP_REFERER', '/'))