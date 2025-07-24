from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
from blog import views as blog_views

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    path('signup/', blog_views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('profile/', blog_views.profile_view, name='profile'),
    path('subscribe-newsletter/', blog_views.newsletter_subscribe_view, name='subscribe_newsletter'),
    path('', include('blog.urls', namespace='blog')),
    # Düzelt! Dil değiştirme sisteminin çalışma şeklinden dolayı kullanmak sorunlu
    # prefix_default_language=False # Ana sayfada /tr/ olmamasını sağlar.
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

